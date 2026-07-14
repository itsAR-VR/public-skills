# Implementation Lanes

The core differentiator of Deep Build. How parallel implementation with cross-model
verification works at the subphase level.

---

## Lane Architecture

Each subphase gets its own **named implementation lane**:

```
Subphase A (independent)     Subphase B (independent)     Subphase C (depends on A)
┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
│  impl-a (primary)    │    │  impl-b (primary)    │    │  (waits for A)       │
│  ↓ implements        │    │  ↓ implements        │    │  impl-c (primary)   │
│  ↓ commits           │    │  ↓ commits           │    │  ↓ implements        │
│  openai-verify-a     │    │  openai-verify-b     │    │  ↓ commits           │
│  ↓ reviews diff      │    │  ↓ reviews diff      │    │  openai-verify-c     │
│  ↓ findings → fix    │    │  ↓ findings → fix    │    │  ↓ reviews diff      │
└──────────────────────┘    └──────────────────────┘    └──────────────────────┘
         │                           │                           │
         └──────────┬────────────────┘                           │
                    ↓                                            │
            cross-monitor                                        │
            (after every 2nd                                     │
             subphase completes)                                 │
                    │                                            │
                    └────────────────────────────────────────────┘
```

## Vertical Slice Loop

Vertical mode runs each feature slice through the gear loop end-to-end before
ship. Independent slices run in parallel feature lanes (worktree-isolated);
dependent slices serialize. All lanes converge into a phase-level integration QA
gate before Gear 6.

```
Vertical Slice Loop (per feature, in worktree):

  impl-{fid} [terminus-maximus + TDD]
       ↓
  openai-diff [verification-before-completion]
       ↓
  scoped-review [ECC code-reviewer + lang-specific]
       ↓
  scoped-clean [deep-clean --scope]
       ↓
  scoped-QA [ECC e2e-runner]
       ↓
  merge-ready [verification-before-completion]
       │
       (after all slices)
       ↓
  phase integration QA
       ↓
  Gear 6 Ship

Parallel feature lanes (when independent, worktree-isolated):

  Lane A: impl-A [terminus-maximus + TDD] → openai-diff [verification-before-completion]
          → scoped-review [ECC code-reviewer + lang-specific] → scoped-clean [deep-clean --scope]
          → scoped-QA [ECC e2e-runner] → merge-ready [verification-before-completion] ─┐
                                                                                        │
                                                                                        ├─→ phase integration QA → Gear 6 Ship
                                                                                        │
  Lane B: impl-B [terminus-maximus + TDD] → openai-diff [verification-before-completion]
          → scoped-review [ECC code-reviewer + lang-specific] → scoped-clean [deep-clean --scope]
          → scoped-QA [ECC e2e-runner] → merge-ready [verification-before-completion] ─┘
```

## Spawning the Implementation Agent

Each primary-model implementation agent follows the terminus-maximus pattern:

```
Agent(
  name: "impl-{sub}",
  model: "<active-primary-model>",
  subagent_type: "general-purpose",
  prompt: "
    You are implementing subphase {sub} of phase {N}.

    ## Context
    Working directory: {working_directory}
    Phase plan: docs/planning/phase-{N}/plan.md
    Subphase plan: docs/planning/phase-{N}/{sub}/plan.md

    ## Your Task
    1. Read the subphase plan thoroughly
    2. Read all files you'll modify (current state, not cached)
    3. Implement the changes described in the plan
    4. Run lint and build after changes
    5. Write tests for new functionality
    6. Update the subphase plan with Output and Handoff sections

    ## Rules
    - Follow $karpathy-guidelines: minimal changes, explicit assumptions
    - Re-read files before modifying (don't rely on cached content)
    - Run $skill-oracle if you need capabilities you don't have
    - Check git status before and after your changes
    - Only modify files in scope for this subphase
    - If blocked, document why in the subphase plan and STOP

    ## Output
    When done, report:
    - Files modified (list)
    - Tests written (list)
    - Lint/build status
    - Any concerns or open questions
  "
)
```

## OpenAI-Family Diff Verification

After each implementation agent completes and commits:

```text
IF active_harness == "codex":
  Agent(
    name: "openai-diff-{sub}",
    subagent_type: "reviewer",
    prompt: "Read the saved subphase diff. Review for bugs, edge cases, security, type safety, API contract mismatches, and test gaps. For each finding: severity, file:line, description, fix."
  )

ELSE IF active_harness == "claude":
  # Get the diff for this subphase's work — write to file, don't pipe via stdin
  git diff HEAD~{N_commits}..HEAD > /tmp/deep-build-diff-{sub}.patch

  # Run Codex verification — reads diff from disk in read-only sandbox
  # 2026-07-09 snapshot; refresh per references/model-currency.md before changing.
  OPENAI_LATEST_MODEL="${OPENAI_LATEST_MODEL:-gpt-5.6-sol}"
  CODEX_BIN="${CODEX_BIN:-codex}"
  "$CODEX_BIN" exec --model "$OPENAI_LATEST_MODEL" \
    -c model_reasoning_effort=ultra \
    --sandbox read-only \
    --skip-git-repo-check \
    "Read /tmp/deep-build-diff-{sub}.patch. You are reviewing a code diff produced by another AI model implementing subphase '{sub}'.

     Find:
     1. Bugs — logic errors, off-by-ones, null/undefined risks
     2. Edge cases — unhandled inputs, race conditions, boundary values
     3. Security — injection, XSS, auth bypass, secrets exposure
     4. Type safety — incorrect types, unsafe casts, missing validation
     5. API contracts — does the implementation match the plan?
     6. Test gaps — what scenarios aren't tested?

     For each finding: severity (CRITICAL/HIGH/MEDIUM/LOW), file:line, description, fix.
     If no issues found, say VERIFIED CLEAN.
    " 2>/dev/null

ELSE IF native_subagents_available:
  Agent(name: "openai-diff-{sub}", subagent_type: "reviewer", prompt: <same verifier prompt>)

ELSE:
  STOP and ask user before degraded single-provider verification.
```

## Cross-Subphase Monitor

Runs after every 2nd subphase completes (or after all complete). Same agent
name, mode-aware prompt: the prompt's `## Check For` block swaps based on root
`default_slice_type`.

**Horizontal mode** (existing behavior, unchanged):

```
Agent(
  name: "cross-monitor",
  model: "<active-primary-model>",
  subagent_type: "general-purpose",
  prompt: "
    You are monitoring parallel implementation lanes for conflicts.

    ## Completed Subphases
    {list of completed subphases with their diffs}

    ## Check For
    1. File conflicts — did two subphases modify the same file incompatibly?
    2. Type conflicts — did one subphase change a type another depends on?
    3. Import conflicts — circular dependencies introduced?
    4. Test conflicts — do tests from different subphases interfere?
    5. Migration conflicts — database migration ordering issues?
    6. API contract breaks — did one subphase break another's assumptions?

    ## Output
    For each conflict: affected subphases, severity, description, resolution.
    If no conflicts: LANES CLEAR.
  "
)
```

**Vertical mode** (new). Runs after every 2nd merge-ready slice. Same agent
shape, slice-aware `## Check For` block:

```
Agent(
  name: "cross-monitor",
  model: "<active-primary-model>",
  subagent_type: "general-purpose",
  prompt: "
    You are monitoring parallel feature slices for cross-slice conflicts.

    ## Merge-Ready Slices
    {list of merge-ready slices with feature_id, surfaces, integration_contracts, diffs}

    ## Check For
    1. Contract drift between slices — emit shape A vs consumer shape B; missing event types declared in integration_contracts.
    2. Schema migration ordering between slices — does slice A's migration break slice B's existing query? Does slice B assume slice A's column exists before its migration runs?
    3. Shared-module touch hotspots — any file appearing in surfaces[] of 2+ slices. If found, demote one slice to depend on the other and serialize.
    4. Event/notification fan-out conflicts — slice A emits an event slice B was supposed to handle but doesn't (or vice versa).
    5. UI prop-shape changes — did one slice change a prop shape that breaks a sibling slice's component?
    6. Cross-feature feature-flag toggles — does slice A's flag gate slice B's surface? Are flag defaults consistent?

    ## Output
    For each conflict: affected slices (feature_id), severity, description, resolution (serialize, refactor contract, escalate to user).
    If no conflicts: LANES CLEAR.
  "
)
```

## Dependency Ordering

Before launching lanes, analyze subphase dependencies:

```
IF all subphases are independent:
  → Launch ALL lanes in a single message (maximum parallelism)

IF some subphases have dependencies:
  → Build dependency graph
  → Launch Tier 1 (no dependencies) in parallel
  → After Tier 1 completes + OpenAI-family verifier passes: launch Tier 2
  → Continue until all tiers complete

IF circular dependency found:
  → STOP. This is a plan structure problem.
  → Either merge the coupled subphases or extract shared dependency.
  → Update plan before proceeding.
```

## Handling OpenAI-Family Verifier Findings

```
FOR EACH OpenAI-family verifier finding:
├── CRITICAL?
│   └── MUST fix before proceeding to next gear
│       ├── impl-{sub} agent still running? → SendMessage with fix request
│       └── Agent done? → Spawn fix agent for that subphase
├── HIGH?
│   └── Fix before next gear (batch fixes after all subphases)
├── MEDIUM?
│   └── Fix if easy, otherwise note in plan for follow-up
└── LOW?
    └── Note in plan, don't block
```

## Maximum Concurrency

The theoretical maximum parallelism for a 5-subphase plan:
- 5 primary-model implementation agents (1 per subphase)
- 5 OpenAI-family verification calls (1 per subphase, after impl completes)
- 2-3 cross-monitor checks
- Total: ~12-13 agent invocations

Practical limit: Agent tool handles up to ~8 parallel agents well.
For 8+ subphases, batch into groups of 5-6.
