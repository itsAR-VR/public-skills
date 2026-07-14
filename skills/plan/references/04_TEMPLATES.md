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
| ID | Workstream | Goal | Depends On | Can Run In Parallel With | Dominant Risk | Outputs |
|----|------------|------|------------|--------------------------|---------------|---------|
| a | <lane name> | <goal> | — | b, c | <risk> | <artifacts> |
| b | <lane name> | <goal> | a | c | <risk> | <artifacts> |
| c | <integration lane> | <goal> | a, b | — | <risk> | <artifacts> |

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
