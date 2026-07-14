# Detailed Procedure

Expanded decision trees and implementation details for each phase of Deep Sweep.

---

## Pre-Invocation Checklist

Before running Deep Sweep, verify:

- [ ] Problem set is clear (user has stated what they want analyzed)
- [ ] Working directory is the project root
- [ ] Git state is clean (or at least understood — note uncommitted changes)
- [ ] No conflicting active phases in docs/planning/
- [ ] OpenAI-family verifier route is selected for the active harness
- [ ] Model currency check completed against official docs and local CLI support

If no OpenAI-family verifier route is available:
- Inform user: "No valid OpenAI-family verifier route is available for this harness."
- Do not silently downgrade or switch to single-provider verification.
- Ask before degraded mode. Degraded mode uses a second primary-model agent with a devil's-advocate prompt and must be logged as non-cross-model verification.

---

## Phase 0: Preflight — Decision Tree

```
START
├── Run $skill-oracle
│   ├── Skills found? → Note available capabilities
│   └── No skills? → Proceed with built-in tools only
├── Check git status
│   ├── Clean? → Proceed
│   ├── Uncommitted changes? → Note them, warn user, proceed
│   └── Merge conflict? → STOP. Resolve first.
├── Check active phases
│   ├── No overlaps? → Proceed
│   ├── Overlapping domain? → Note conflict, add to analysis
│   └── Same files targeted? → WARN user of potential conflict
└── Extract problem set
    ├── Problems clear from conversation? → Number them P1..P(N)
    ├── Ambiguous? → Ask user to clarify before proceeding
    └── Single problem? → Still proceed (1 subphase plan)
```

---

## Phase 1: Primary-Model Deep Analysis — Parallelism Rules

**Independence test:** Can problem P(A) be analyzed without knowing the results of P(B)?

```
IF problems are independent:
  → Spawn ALL primary-model agents in a single message (parallel execution)
  → Maximum concurrency: up to 8 agents simultaneously

IF problems have dependencies:
  → Group into dependency tiers
  → Tier 1 runs in parallel
  → Tier 2 waits for Tier 1, then runs in parallel
  → etc.

IF single problem:
  → Still spawn dedicated agent (context isolation benefit)
```

**Agent naming convention:** `primary-deep-1`, `primary-deep-2`, etc.

**What to include in each agent's prompt:**
1. The specific problem description (not all problems)
2. Relevant file paths (glob for related files)
3. The working directory path
4. Brief context about the overall project (1-2 sentences)
5. The output format template from references/agent-prompts.md

**What NOT to include:**
- Other problems' details (context isolation)
- Previous conversation history (irrelevant to analysis)
- Other agents' findings (they haven't run yet)

---

## Phase 2: OpenAI-Family Verifier — Invocation Patterns

### Harness-Routed Invocation

```text
IF active_harness == "codex":
  Agent(
    name: "openai-verify-phase-{N}",
    subagent_type: "reviewer",
    prompt: "Read docs/planning/phase-{N}/deep-sweep-findings.md and all subphase plans. Cross-verify for gaps, contradictions, over/under-engineering."
  )

ELSE IF active_harness == "claude":
  # IMPORTANT: Never pipe large content via stdin — causes exit code 2.
  # Let Codex read files from disk in read-only sandbox instead.
  OPENAI_LATEST_MODEL="${OPENAI_LATEST_MODEL:-gpt-5.6-sol}"
  CODEX_BIN="${CODEX_BIN:-codex}"
  "$CODEX_BIN" exec --model "$OPENAI_LATEST_MODEL" \
    -c model_reasoning_effort=ultra \
    --sandbox read-only \
    --skip-git-repo-check \
    "Read docs/planning/phase-{N}/deep-sweep-findings.md and all subphase plans. Cross-verify for gaps, contradictions, over/under-engineering." \
    2>/dev/null

ELSE IF native_subagents_available:
  Agent(name: "openai-verify-phase-{N}", subagent_type: "reviewer", prompt: <same verifier prompt>)

ELSE:
  STOP and ask user before degraded single-provider verification.
```

In Codex main harness, nested `codex exec` is forbidden. Use native sub-agents.
In Claude Code, `codex exec` is allowed only after `which -a codex`,
`codex --version`, and model support checks pass. If multiple Codex binaries are
installed, set `CODEX_BIN` to the highest supported version before invoking CLI.
If the latest model is unsupported, upgrade Codex or stop; do not downgrade to an
older model.

### Model Currency Check

Read `references/model-currency.md` before changing model IDs, aliases, effort
controls, or verifier routing. Its current source check is 2026-07-09 and must be
refreshed after an OpenAI or Anthropic model release, a local CLI model-support
failure, or 90 days, whichever comes first.

### Reasoning Effort Selection

| Problem complexity | OpenAI verifier reasoning effort |
|--------------------|----------------------|
| Simple (1-2 problems, narrow scope) | medium |
| Standard (3-5 problems, moderate scope) | high |
| Complex (6+ problems, wide scope, security) | xhigh |

---

## Phase 3: Plan Creation — Subphase Decomposition Rules

How to split problems into subphases:

```
IF problems map 1:1 to logical areas:
  → One subphase per problem (a=P1, b=P2, etc.)

IF one problem is very large:
  → Split into sub-problems, each becomes a subphase

IF problems are tightly coupled:
  → Group coupled problems into single subphase
  → Note coupling in plan

IF problems span layers (frontend/backend/DB):
  → Consider splitting by layer OR by feature
  → Prefer feature-based splits (reduces cross-subphase dependencies)
```

**Root plan template:**

```markdown
# Phase {N}: {Title}

## Original Request
> {verbatim user request — exactly as stated}

## Problem Set
{numbered list of problems with consolidated analysis}

## Cross-Model Findings
### Primary-Model Analysis Summary
{key findings}

### OpenAI-Family Cross-Verification Summary
{gaps, contradictions, corrections}

## Success Criteria
- [ ] {criterion 1}
- [ ] {criterion 2}
...

## Subphase Index
| ID | Title | Scope | Dependencies |
|----|-------|-------|-------------|
| a  | ...   | ...   | none        |
| b  | ...   | ...   | a           |
...

## Risk Register
| Risk | Severity | Mitigation | Owner |
|------|----------|------------|-------|

## Cross-Cutting Concerns
{populated in Phase 7}

## Open Questions
{anything below 84.7% confidence}

## Phase Summary
{populated in Phase 7}
```

---

## Phase 4: Parallel Subphase Analysis — Orchestration

Total agents = (subphases) x 3. For a 5-subphase plan, that's 15 parallel agents.

**Spawning order:**
1. Launch ALL agents for ALL subphases in a SINGLE message
2. Each subphase gets: RED TEAM agent + primary-model deep dive agent + OpenAI-family verification
3. All 15 (or however many) agents run simultaneously

**Collecting results:**
- Agent tool returns results as they complete
- Collect all results before proceeding to Phase 5
- If any agent fails or times out: note the failure, proceed with available results

**OpenAI verifier rate limiting:**
- If the OpenAI verifier rate-limits, queue subphase verifier calls sequentially
- RED TEAM and primary-model agents are not affected when the verifier is a different model family

---

## Phase 5: Cross-Comparison — What to Feed

The cross-comparison pair needs:
1. ALL subphase plans (full content from disk)
2. ALL Phase 4 findings (RED TEAM + primary-model + OpenAI-family verifier per subphase)
3. The root plan's Success Criteria and Risk Register
4. Any dependency relationships between subphases

This is the ONLY phase where agents see the complete picture.
Context may be large — if it exceeds reasonable limits:
- Summarize Phase 4 findings to key findings per subphase
- Include full subphase plans (these are shorter)
- Prioritize CRITICAL and HIGH findings

---

## Phase 6: Lane Communication — Decision Tree

```
FOR EACH finding from Phase 4-5:
├── Severity = LOW?
│   └── Record in plan, no communication needed
├── Severity = MEDIUM?
│   └── Record in plan, communicate if it changes approach
├── Severity = HIGH?
│   └── MUST communicate to lane owner
│       ├── Agent still addressable? → SendMessage
│       └── Agent done? → Spawn new agent to update plan file
└── Severity = CRITICAL?
    └── MUST communicate + verify incorporation
        ├── Communicate finding
        ├── Verify subphase plan was updated
        └── If not resolved in 3 rounds → escalate to user
```

**Multi-lane findings (affects 2+ subphases):**
1. Communicate to ALL affected lane owners
2. Add to root plan's Cross-Cutting Concerns
3. Assign a primary owner (the most affected subphase)
4. Secondary owners acknowledge and cross-reference

---

## Phase 7: Final Consolidation — Completion Criteria

The Deep Sweep is complete when:

- [ ] Root plan has non-empty Cross-Cutting Concerns section
- [ ] Risk Register populated with all CRITICAL/HIGH findings
- [ ] Each subphase has confidence rating
- [ ] All subphases at >= 84.7% confidence (or Open Questions raised)
- [ ] $phase-review passes on the complete plan
- [ ] Summary presented to user with actionable next steps
