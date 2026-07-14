---
name: plan
description: Convert the current conversation into a new numbered planning phase; creates docs/planning/phase-N/ with a root plan and agent-ready subphase plan.md scaffolds. Plans are built as a dependency graph of parallel workstreams instead of a linear checklist. Absorbs the GSD planning layer — pre-flight discuss mode, plan-checker validation gate, integration-checker, and research agent subroutines (project-researcher, phase-researcher, assumptions-analyzer, advisor-researcher, ui-researcher, gsd-roadmapper, gsd-user-profiler).
related_skills: [skill-oracle, phase-gaps, phase-review, verify, phase-implement, terminus-maximus, deep-sweep, deep-build, gepetto, requirements-clarity]
---

# Instructions

Read all references in `references/` before using this skill.

This skill is a planner for multi-agent execution. The default output is a
dependency graph of subphases that can run in parallel when their file
surfaces, contracts, and risks are isolated.

## Distilled Planning Model

The planning contract for `/phase-plan` absorbs the cross-cutting logic from
the attached Everything Claude Code skills:

1. Start by validating the product goal, user pain, anti-goal, and success
   metric before decomposing work.
2. Break work into agent-sized packets with one dominant risk and a clear done
   condition.
3. Prefer parallel workstreams over alphabetical handoff when outputs and file
   surfaces are safely separable.
4. Treat each subphase as a dispatchable mission with an explicit role, model
   tier, context brief, retrieval plan, verification plan, and recovery path.
5. Require evals and tests as first-class plan artifacts, not execution-time
   afterthoughts.
6. Capture meaningful architecture decisions as ADR candidates inside the plan.
7. Add safety, rollback, observability, and kill-switch expectations for
   long-lived or autonomous agent work.
8. Add an explicit synthesis or integration lane whenever parallel workstreams
   converge on shared contracts or files.

See `08_PARALLEL_AGENT_ARCHITECTURE.md` for the distilled source mapping.

## Skill Discovery (Required)

Before creating a new phase and before drafting each subphase, run skill
discovery for each distinct capability the plan requires:

1. `/skill-oracle "<capability needed>"` — primary discovery path.
2. If `/skill-oracle` is unavailable in the current harness, fall back to
   `find-local-skills` and `find-skills`.

Use the output to:

- Keep only implementable skills in the plan.
- Add a short "Skills available for implementation" note in the root plan and
  each subphase plan.
- If a desired skill is missing, add it to risks/assumptions and propose a
  fallback path (or install from ClawHub if available).

The agent should call `/skill-oracle` at planning time and again during
execution-time updates when scope changes, so RED TEAM passes and subsequent
subphases use current capability signals.

## Multi-Agent Awareness

**IMPORTANT:** Multiple agents may be working on different phases concurrently.
Before creating a new phase:

1. **Scan the last 10 phases** for potential file/domain overlaps
2. **Check git status** for uncommitted changes from other agents
3. **Document dependencies** on other active phases in your plan
4. **Map isolation boundaries** for each planned subphase:
   - target files/directories
   - shared contracts or schemas
   - merge or synthesis points
5. **Cap live parallelism** at the smallest safe team size:
   - prefer 2-5 active lanes
   - if you need more than 5, consolidate or recommend `deep-sweep` /
     `claude-devfleet`

If you detect overlap with an active phase, note it in your plan's Context
section and specify how the phases should coordinate.

See `06_MULTI_AGENT_COORDINATION.md` for detailed procedures.

## Original User Request (verbatim)

When creating the new phase plan, the first section in
`docs/planning/phase-<N>/plan.md` must be a verbatim copy of the original user
request that triggered `/phase-plan`.

Place this section immediately after the phase title and before
`## Product Frame`, with the user's text unchanged (no paraphrasing or
summary).

Use this heading:

## Original User Request (verbatim)

and paste the exact wording of the triggering prompt beneath it.

## Adaptive Gate Selection (harness-aware)

This skill runs across multiple harnesses (Claude Code, OpenClaw, Codex,
OpenCode, Kilo, Gemini, MiniMax). Before invoking each internal gate below, the
skill runtime checks what the harness already protects against and skips
duplicative gates with a documented reason — never silently.

- **Full procedure + gate↔harness overlap map**:
  `~/.claude/skills/lib/adaptive-gate-selection.md`
- **Examples**: on Claude Code with ECC, the plan-checker's commit-message
  subset skips because `pre:bash:commit-quality` already enforces Conventional
  Commits + secret scan (strict superset). On OpenClaw, plan-checker's
  goal-backward audit still runs (no overlap).

**Every gate decision MUST be logged** so future invocations learn from prior
ones:

```bash
bash $HOME/.claude/skills/lib/skill-gate-logger.sh \
  --skill phase-plan \
  --gate <gate-name> \
  {--verdict PASS|FAIL|ESCALATE|PARTIAL  OR  --skipped "<why>"} \
  --reason "<one-line reason>"
```

Logs route per-harness automatically (`~/.claude/logs/skill-gates.jsonl` on
Claude Code, `~/.openclaw/logs/skill-gates.jsonl` on OpenClaw, etc.).

## GSD Planning Layer (absorbed)

Deep detail in `references/07_GSD_PLANNING_LAYER.md`. High-level integration:

### 1. Pre-flight Discuss Mode (before drafting plan.md)

Absorbed from GSD's `/gsd-discuss-phase`. Before writing any file, run one
"discuss" turn to align on:

1. **Phase goal** — what this phase delivers (one sentence)
2. **Prior context** — what prior phases established (scan
   `docs/planning/phase-*/plan.md` summaries)
3. **Known unknowns** — what needs research before the plan is written
4. **Scope boundary** — what is explicitly OUT of scope

If any answer is ambiguous or the user's goal isn't crisp, ask a focused
clarifying question (one at a time) before proceeding. For heavy
unknown-surface, recommend `deep-sweep` first.

### 2. Parallel Research Wave (invoke as sub-agents via Agent tool)

For light, targeted research during planning, dispatch only the relevant
research agents in parallel, then synthesize their outputs into one planning
brief. For heavy research, prefer `deep-sweep`.

| Agent | Invoke when |
|-------|------------|
| `gsd-project-researcher` | First phase of a project, or unfamiliar repo |
| `gsd-phase-researcher` | Need domain deep-dive for current phase only |
| `gsd-assumptions-analyzer` | Draft plan contains assumptions that could break the phase |
| `gsd-advisor-researcher` | Similar prior art exists and would inform approach |
| `gsd-ui-researcher` | UI-heavy phase requiring pattern/affordance study |
| `gsd-user-profiler` | User preferences unclear — build profile from conversation |

Pass each agent: the verbatim user request, the phase goal, the specific
question, and the target subdomains. Consolidate outputs before plan drafting.

The synthesized brief must explicitly call out:

- likely parallel lanes
- shared dependencies or integration points
- open assumptions that could invalidate parallel execution
- recommended model tiers / agent roles for each lane

### 3. Plan-Checker Gate (mandatory before writing plan.md to disk)

Before `Write`ing `docs/planning/phase-<N>/plan.md`:

1. Draft the full plan.md in memory
2. Invoke `gsd-plan-checker` via the Agent tool. Pass:
   - The draft plan.md content
   - The verbatim user request
   - The phase goal (one-sentence)
   - Prior phase summaries (if any)
   - The subphase dependency graph
3. Interpret the checker's verdict:
   - **PASS** — write plan.md to disk, proceed
   - **FAIL** — revise plan.md per checker notes, re-invoke (max 3 attempts)
   - **ESCALATE** — surface unresolved checker issues to the user before writing

The checker verifies goal-backward: *"Will executing this plan deliver the
phase goal?"* — not just that the plan looks complete. It must also verify that
parallel lanes have explicit dependencies, evaluations, and synthesis points.

### 4. Integration-Checker (mandatory after writing plan.md, before handoff)

Before handing the plan to `deep-sweep` (for red-team research) or `deep-build`
(for execution):

1. Invoke `gsd-integration-checker` via the Agent tool. Pass:
   - The freshly written plan.md path
   - List of prior phase directories (`ls -dt docs/planning/phase-*`)
2. Checker verifies:
   - No duplicate scope with prior phases
   - Correct dependency declarations
   - Consistent terminology / file path conventions
   - No contradictions with decisions recorded in prior phases
   - Parallel lanes do not secretly contend on the same files or contracts
3. If FAIL → revise plan.md before handoff

### 5. UI Pre-Check (for UI-heavy phases)

When the phase touches UI surfaces, invoke `gsd-ui-checker` after
plan-checker but before integration-checker. It validates that the UI approach
matches existing design system / patterns.

### 6. Roadmap Update (optional, multi-phase projects)

For projects with 3+ planned phases, after plan.md is finalized invoke
`gsd-roadmapper` to refresh `docs/planning/ROADMAP.md` — updates phase
timeline, dependency graph, milestone mapping, and parallel execution lanes.

## Handoff Contract

When `/phase-plan` completes, the next step depends on the phase:

| Next step | When |
|-----------|------|
| `deep-sweep` | Plan has 3+ subphases, touches multiple domains, or high-stakes (auth/payments/data) |
| `phase-gaps` | Plan is smaller but still benefits from a red-team pass |
| `deep-build` | Plan is well-understood, ready to execute with cross-verification |
| `execute` / `terminus-maximus` | Single-model execution is sufficient |
| `verify` | (post-execution) audit and cleanup pass |

Report the recommended next step to the user at the end of the phase-plan turn.
If the plan contains parallel workstreams, also report:

- the recommended dispatch order
- which subphases can start immediately
- which subphase is the synthesis / integration owner

## Signals

- The conversation reaches a new direction or architecture decision
- The user says "create a phase plan", "materialize this", "capture this into
  planning", "phase-plan this", "/phase-plan"
- A "we should plan this" moment where structure would help
- Existing phase plan needs refresh after scope change

## References

**Directory:** `references/`

- `01_INTENT.md`
- `02_PRECONDITIONS.md`
- `03_PROCEDURE.md`
- `04_TEMPLATES.md`
- `05_EDGE_CASES.md`
- `06_MULTI_AGENT_COORDINATION.md`
- `07_GSD_PLANNING_LAYER.md` ← absorbed discuss-mode, checkers, research subroutines
- `08_PARALLEL_AGENT_ARCHITECTURE.md` ← distilled ECC source logic for parallel planning
