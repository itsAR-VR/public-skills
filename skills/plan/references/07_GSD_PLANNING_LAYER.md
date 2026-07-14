# 07 — GSD Planning Layer

Deep reference for the GSD-absorbed planning mechanisms invoked from
`phase-plan`. This layer adds adversarial validation to the default phase-plan
flow so a plan is not trusted until it passes discussion, research,
plan-checker, and integration-checker gates.

## Intent

The default phase-plan flow writes a plan.md and hands off. GSD adds four
quality gates:

1. **Pre-flight discussion** — prevents over-scoped or under-specified plans
2. **Parallel research wave** — gathers targeted context before decomposition
3. **Plan-checker gate** — verifies the plan will achieve the goal
4. **Integration-checker gate** — verifies the plan slots cleanly alongside prior phases

All four are additive. If you bypass them (for example, a trivial phase),
record the reason in the plan's Context section.

## Pre-flight Discussion Template

Absorbed from `/gsd-discuss-phase`. Use this turn BEFORE drafting plan.md:

```
Before I write phase-N/plan.md, let me align on a few things:

1. Goal (one sentence): <state what you think the phase should deliver>
2. Prior context: <scan prior phases, list what's already established>
3. Open questions: <list anything that needs research before planning>
4. Out of scope: <what this phase explicitly does NOT do>

Is this right? Any of these need correction?
```

If the user surfaces ambiguity, pause and clarify. If clear, proceed to the
research wave if needed, then draft.

## Parallel Research Wave — Agent Invocation

Each agent is installed at `~/.claude/agents/gsd-<name>.md`. Invoke only the
relevant agents, preferably in parallel, then synthesize their outputs into one
planning brief before drafting the plan graph.

### `gsd-project-researcher`

**When:** First phase of a project, unfamiliar repo, or project has evolved
significantly.

**Prompt template:**
```
Investigate the project at <working-dir>. Return a structured brief:
- Tech stack (languages, frameworks, key deps)
- Architecture style (monolith/modular/microservices)
- Existing patterns (state management, data access, auth)
- Constraints discovered (license, performance, platform)
- Recent activity (last 10 commits, active areas)

User's phase goal: <one-sentence goal>

Surface anything that would change how the plan should be structured.
```

### `gsd-phase-researcher`

**When:** Phase domain is specialized and needs targeted investigation.

**Prompt template:**
```
Deep-dive the following domain/question for phase-N:
<domain question>

User's phase goal: <goal>
Known constraints: <from prior phases>

Return: relevant patterns, pitfalls, library options, decision factors.
```

### `gsd-assumptions-analyzer`

**When:** Draft plan contains assumptions that, if wrong, would invalidate the
plan.

**Prompt template:**
```
Surface hidden assumptions in this draft plan:
<paste draft plan.md>

User request (verbatim): <original prompt>

Return: list of assumptions ranked by plan-invalidating impact (high/med/low), with verification steps for each high-impact item.
```

### `gsd-advisor-researcher`

**When:** Similar problems have been solved elsewhere and borrowing would save
work.

**Prompt template:**
```
Find 2-3 prior art examples for this problem:
<problem statement>

Preference: battle-tested libraries or open-source projects over hand-rolled.

Return: comparison table (approach, tradeoffs, effort-to-adopt), recommendation.
```

### `gsd-ui-researcher`

**When:** Phase touches UI surfaces — new screens, flows, affordances, or
interaction patterns.

**Prompt template:**
```
Research UI/UX patterns for <feature>.

Existing design system: <link or describe>
Platform: <web/iOS/Android/desktop>
Accessibility requirements: <WCAG level>

Return: recommended patterns, anti-patterns to avoid, reference implementations.
```

### `gsd-user-profiler`

**When:** The user's preferences, expertise level, or priorities are not clear
from the conversation and would materially change the plan.

**Prompt template:**
```
Build a user profile from this conversation history:
<conversation excerpt>

Return:
- Expertise level (novice/intermediate/expert) in domain
- Stated priorities (speed/quality/safety/learning)
- Workflow preferences (tight iteration vs. big batch)
- Known constraints (time, team, budget)

The plan should match this profile.
```

### Synthesis Requirement

After the wave completes, produce one planning brief that answers:

- What are the likely parallel lanes?
- What dependencies force serialization?
- What assumptions could break the parallel plan?
- Which tasks need stronger models or reviewers?
- What integration lane is required?

## Plan-Checker Gate — Invocation

After drafting plan.md in memory (NOT on disk yet), invoke:

```
Agent({
  subagent_type: "gsd-plan-checker",
  description: "Validate phase-N plan before writing to disk",
  prompt: `
Verify this plan will achieve the stated goal.

<phase_goal>
<one-sentence goal>
</phase_goal>

<user_request_verbatim>
<original user prompt>
</user_request_verbatim>

<prior_phase_summaries>
<list of prior phase goals + outputs>
</prior_phase_summaries>

<draft_plan_md>
<paste full draft>
</draft_plan_md>

Check goal-backward: does executing every task in this plan produce the goal?
Flag:
- Missing product frame (user / pain / metric / anti-goal)
- Requirements with no corresponding task
- Tasks that don't actually achieve their stated requirement
- Broken / circular / implicit dependencies
- Parallel lanes that secretly share the same file surface or contract
- Missing synthesis / integration ownership after parallel branches
- Planned artifacts without wiring between them
- Scope that will exceed context budget
- Subphases with no evaluation plan or recovery path
- Contradictions with user decisions in prior phases

Return one of: PASS | FAIL (with specific revisions) | ESCALATE (with unresolved questions).
`
})
```

### Revision Loop

- Attempt 1: FAIL → revise per checker notes → re-invoke
- Attempt 2: FAIL → revise → re-invoke
- Attempt 3: FAIL → ESCALATE to user with the checker's persistent issues

Do not exceed 3 revision loops. If the plan cannot pass in 3 tries, the
problem is likely upstream.

## Integration-Checker Gate — Invocation

After plan.md is written to disk, before handoff:

```
Agent({
  subagent_type: "gsd-integration-checker",
  description: "Verify phase-N plan integrates with prior phases",
  prompt: `
Verify this new phase plan integrates cleanly with the existing phase history.

<new_plan_path>
docs/planning/phase-<N>/plan.md
</new_plan_path>

<prior_phase_dirs>
<ls -dt docs/planning/phase-* output>
</prior_phase_dirs>

Check:
- Scope overlap with prior phases (should be zero or explicit)
- Dependency declarations match reality
- Terminology consistency
- File path conventions
- No contradictions with decisions recorded in prior phase plans
- No unsafe parallel lanes against active or prior work
- Integration subphase ownership is explicit when branches converge

Return: PASS | FAIL (with specific conflicts and required plan edits).
`
})
```

On FAIL, revise plan.md in place, then re-invoke once. If it still fails,
surface to the user.

## UI Pre-Check

For UI-heavy phases, between plan-checker PASS and integration-checker, invoke
`gsd-ui-checker`:

```
Agent({
  subagent_type: "gsd-ui-checker",
  prompt: `
Validate the UI approach in this plan against the project's design system and patterns.

<plan_md_path>...</plan_md_path>
<design_system_location>...</design_system_location>

Flag: off-pattern components, accessibility gaps, inconsistent spacing/typography tokens, missing empty/error states.
`
})
```

## Roadmap Refresh

For multi-phase projects (3+ phases planned), after plan.md is finalized:

```
Agent({
  subagent_type: "gsd-roadmapper",
  prompt: `
Refresh docs/planning/ROADMAP.md to include phase-<N>.

Inputs: all docs/planning/phase-*/plan.md files.

Produce:
- Updated phase timeline (sequential / parallel lanes)
- Dependency graph (which phase blocks which)
- Milestone mapping (which phases ship together)
- Risk roll-up (from each phase's risks section)
`
})
```

## Skip / Bypass

Some phases are small enough that the full gate ceremony is overhead. You MAY
skip gates when ALL of:

- Phase scope is < 50 LOC
- Single file, single concern, single outcome
- No dependency on prior phases
- User has approved the draft plan inline

Record the skip reason in the plan's Context section:
`Gates skipped: <reason>. Approved by user inline.`

Do NOT skip gates for:

- Multi-subphase plans
- Parallel multi-agent plans
- Auth / payments / data migration
- Anything touching production schemas
- First phase of a new project

## Failure Recovery

If a gate surfaces a problem that is upstream (for example, the user's goal is
ambiguous), do not iterate inside the gate loop. Pause and re-discuss.

## Related

- `03_PROCEDURE.md` — base phase-plan procedure
- `06_MULTI_AGENT_COORDINATION.md` — concurrent phase coordination
- `deep-sweep` — when research scope warrants parallel wave instead of inline agents
- `deep-build` — next step after phase-plan for cross-verified execution
- `verify` — post-execution audit + cleanup
