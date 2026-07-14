# Templates

## Root Plan Template

```md
# Phase <N> — <derived title>

## Original User Request (verbatim)
(Paste the full original user request that triggered /phase-plan with no edits)

## Product Frame
- User / operator:
- Pain / job to be done:
- Why now:
- Smallest acceptable win:
- Anti-goal:
- Success metric:

## Purpose
(One or two sentences summarizing the user's objective)

## Context
(Extract key reasoning from the conversation so intent/rationale is preserved)

## Distilled Planning Principles
- Agents execute dependency-isolated packets, not a linear checklist.
- Every packet is independently verifiable and has one dominant risk.
- Parallel lanes are allowed only when file, contract, and rollout overlap is explicit.
- Every convergence point has a named synthesis owner.

## Skills Available for Implementation
- `<capability>` → `/skill-oracle` output: <summarize relevant skills>
- Fallback discovery output (if used): <find-local-skills / find-skills summary>
- Selected implementable skills: <list>

## Concurrent Phases
(Optional — include if overlaps detected during conflict check)

| Phase | Status | Overlap | Coordination |
|-------|--------|---------|--------------|
| Phase N-1 | Active/Complete | Files: X, Y | Wait for completion / Merge changes |
| Phase N-2 | Active | Domain: Z | Independent, no action needed |

## Agent Team
| Lane | Subphase | Role | Model Tier | Depends On | Notes |
|------|----------|------|------------|------------|-------|
| Lane 1 | a | <owner> | <tier> | — | <focus> |
| Lane 2 | b | <owner> | <tier> | a | <focus> |

## Evaluation Strategy
- Baseline / RED signals:
- Verification / GREEN signals:
- Regression checks:
- Coverage or audit requirements:

## Constraints
(Include relevant technical/architectural rules mentioned in the discussion)

## Safety and Ops
- Permissions / environment boundaries:
- Rollback strategy:
- Observability / audit expectations:
- Kill switch / pause condition:

## ADR Candidates
- <decision worth recording, or "None yet">

## Success Criteria
(Concrete closure conditions for this phase)

## Subphase Index
| ID | Slice Type | Feature ID | Workstream | Goal | Depends On | Can Run In Parallel With | Dominant Risk | Outputs |
|----|------------|------------|------------|------|------------|--------------------------|---------------|---------|
| a | vertical | <feature_id> | <lane name> | <goal> | — | b, c | <risk> | <artifacts> |
| b | vertical | <feature_id> | <lane name> | <goal> | a | c | <risk> | <artifacts> |
| c | horizontal | — | <integration lane> | <goal> | a, b | — | <risk> | <artifacts> |

## Dispatch Recommendation
- Start immediately: <subphase IDs>
- Blocked until dependencies resolve: <subphase IDs>
- Recommended next skill: <deep-build / deep-sweep / execute / terminus-maximus / phase-gaps>
```

## Subphase Plan Template

```md
# Phase <N><letter> — <Subtask Name>

## Mission
(What this subphase is doing and why it exists)

## Agent Assignment
- Role:
- Model tier:
- Parallel lane:
- Depends on:
- Can run with:
- Target files / contracts:

## Inputs
(Artifacts or reasoning from root context or predecessor subphases)

## Context Brief
(Self-contained context a fresh agent needs without rereading the full phase)

## Iterative Retrieval Plan
- Cycle 1 query:
- Likely gaps to refine for:
- Stop condition for retrieval:

## Skills Available for This Subphase
- `/skill-oracle` output: <high-signal skills that can be invoked>
- Fallback discovery output (if used):
- Planned invocations: <only include confirmed available skills>

## Acceptance Criteria
(Clear done condition for this subphase)

## Evaluation Plan
- Baseline / RED:
- GREEN / regression:
- Additional checks:

## Work
(Steps/decisions needed; include checks and validations)

## Output Contract
- `status`:
- `summary`:
- `next_actions`:
- `artifacts`:

## Failure Modes and Recovery
- Likely failure mode:
- Safe retry instruction:
- Explicit stop condition:

## Safety / Rollback
- Boundaries:
- Rollback path:

## ADR Candidates
- <decision worth recording, or "None">

## Downstream Consumers
(Which later subphases or reviewers consume this output)
```

The template above is the **horizontal** variant. It is used when
`slice_type: horizontal` (cross-cutting refactor / migration / cleanup
layer). For new user-visible capabilities, use the Vertical Subphase Plan
Template below — it is the default when `phase_intent: feature`.

## Vertical Subphase Plan Template

Default for `phase_intent: feature`. Each subphase owns one full-stack
feature slice (DB + API + UI + tests).

```md
---
slice_type: vertical
feature_id: comment-threading
goal: Users can reply to feedback comments in nested threads
user_value: Reduces fragmented async discussion across separate cards
parent_milestone: phase-12-feedback-improvements
surfaces:
  db:    [migrations/2026_04_29_thread_parent_id.sql, prisma/schema.prisma]
  api:   [app/api/comments/route.ts, lib/comments/threads.ts]
  ui:    [components/feedback/CommentThread.tsx]
  tests: [tests/integration/comment-threads.spec.ts]
acceptance_criteria:
  - User can reply to any top-level comment
  - Replies render nested ≤3 levels
  - Existing flat comments still render unchanged (back-compat)
out_of_scope:
  - Email notifications on reply
depends_on: []
integration_contracts:
  - { with: notification-prefs, contract: comment_event_emitter }
ship_gate:
  unit_tests: required
  integration_tests: required
  visual_qa: required
  scoped_clean: feature:comment-threading
---

# Phase <N><letter> — <Feature Name>

## Mission
(One paragraph: the user-visible capability this slice delivers and why it
exists. Reference the `feature_id` and the `user_value` from front-matter.)

## Acceptance Criteria
(Mirror the front-matter list. Must include at least one back-compat
criterion guaranteeing existing behavior when this slice ships alone.)

## Approach
- DB layer: <migrations and schema changes from `surfaces.db`>
- API layer: <endpoints and services from `surfaces.api`>
- UI layer: <components and routes from `surfaces.ui`>
- Tests: <unit + integration coverage from `surfaces.tests`>
- Integration contracts: <typed contracts named in `integration_contracts`>

## Output Contract
- `status`:
- `summary`:
- `next_actions`:
- `artifacts`: <full-stack diff covering all surfaces>
```

## Worktree Plan JSON Template — Feature Lanes

Used by `/deep-build` Gear 0 when root `isolation: worktree` AND there are
2+ independent vertical slices. Emits one worker per `feature_id`.

```json
{
  "phase": "phase-{N}",
  "default_slice_type": "vertical",
  "coordinationDir": "/tmp/phase-{N}-coord",
  "workers": [
    {
      "name": "feature-{feature_id}",
      "branchName": "feature/{feature_id}",
      "seedPaths": ["<every path from this slice's surfaces[]>"],
      "taskFilePath": "docs/planning/phase-{N}/{letter}/plan.md",
      "handoffFile": "/tmp/phase-{N}-coord/{feature_id}-handoff.md",
      "statusFile": "/tmp/phase-{N}-coord/{feature_id}-status.md"
    }
  ]
}
```

Note: `orchestrate-worktrees.js` consumes this directly; no code changes to
that script needed.
