# 08 — Parallel Agent Architecture

This reference distills the Everything Claude Code skills requested for the
`phase-plan` rewrite into one planning contract. The goal is to promote
cross-cutting principles into the planner instead of keeping them trapped in
individual source skills.

## Core Rules

1. Plan as a dependency graph, not a serial checklist.
2. Decompose into agent-sized packets with one dominant risk and a clear done
   condition.
3. Prefer parallel lanes when files, contracts, and rollout surfaces are
   separable.
4. Add an explicit synthesis / integration owner whenever branches converge.
5. Require product framing before decomposition: user, pain, anti-goal, metric.
6. Require evals and tests in the plan itself, especially for implementation
   work.
7. Make each subphase cold-startable with a context brief and retrieval plan.
8. Standardize outputs with status, summary, next actions, and artifacts.
9. Every subphase needs a recovery path, safe retry guidance, and a stop
   condition.
10. Long-lived agent work needs safety boundaries, rollback, observability, and
    audit expectations.
11. Record architectural decisions as ADR candidates when the plan picks
    durable patterns or trade-offs.

## Source Mapping

| Source skill | Distilled principle | Phase-plan impact |
|--------------|---------------------|-------------------|
| `agent-harness-construction` | Use narrow, explicit work packets with deterministic output and recovery contracts | Each subphase must define role, outputs, recovery path, and artifacts |
| `agentic-engineering` | Define completion criteria first; decompose into independently verifiable units | Root plan includes success criteria and each subphase has a clear done condition |
| `ai-first-engineering` | Favor explicit boundaries, stable contracts, and deterministic tests | Root plan captures constraints; subphases require eval / regression plans |
| `architecture-decision-records` | Surface important trade-offs as durable records | Root and subphase templates include ADR candidate sections |
| `blueprint` | Generate cold-startable steps with dependency edges, parallel detection, and review gates | Root plan uses a dependency graph and self-contained subphase briefs |
| `claude-devfleet` | Parallel work should be dispatchable as mission DAGs with isolated worktrees | Subphases are modeled as dispatchable missions with explicit dependencies |
| `continuous-agent-loop` | Continuous execution needs quality gates and stop conditions | Plans include recovery controls and pause / kill conditions |
| `iterative-retrieval` | Context should be refined in cycles, not guessed upfront | Each subphase includes an iterative retrieval plan |
| `team-builder` | Parallel teams need role selection and bounded team size | Root plan names lane owners and caps parallel lanes at a sane size |
| `tdd-workflow` | Tests and evals must lead implementation | Subphases include RED / GREEN / regression expectations |
| `product-lens` | Validate the why before building | Root plan starts with user, pain, anti-goal, and metric |
| `enterprise-agent-ops` | Long-running agents need observability, rollback, and audit | Root plan includes Safety and Ops expectations |
| `rules-distill` | Promote repeated, actionable rules with clear violation risk | This reference centralizes the repeated planning rules and turns them into the default contract |

## Practical Planning Heuristics

### When to Parallelize

**Vertical-mode parallel rule** (default for `default_slice_type: vertical`):

Parallelize feature slices when ALL are true:

- Feature IDs are disjoint (each lane owns one `feature_id`)
- `integration_contracts` are explicit and typed (Zod / Pydantic / JSON
  Schema or equivalent), not prose
- Each slice owns a complete vertical surface set (db + api + ui + tests as
  applicable)
- Cross-feature shared-file hotspots flagged by the cross-monitor are absent
  (or one slice depends on the other)

**Horizontal-mode parallel rule** (default for `default_slice_type: horizontal`):

Parallelize layer subphases when ALL are true:

- File surfaces are mostly disjoint
- Dependencies are explicit
- Outputs can be validated independently
- Convergence point has a named owner

### When to Stay Serial

Stay serial when any are true:

- multiple tasks touch the same schema or contract
- the team lacks a clean synthesis lane
- the goal is small enough that orchestration cost dominates
- failure isolation would be poor

### Lane Count

- Prefer 2-5 live lanes.
- If more than 5 are needed, consolidate or recommend heavier orchestration.

### Minimum Subphase Contract

Every subphase should answer:

- What is the mission?
- Which role and model tier should own it?
- What inputs are required?
- What context should be retrieved first?
- How do we know it is done?
- What is the failure / retry / stop behavior?
- Who consumes the output next?
