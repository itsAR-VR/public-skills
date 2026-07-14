# Intent (RED TEAM)

This skill performs a **RED TEAM** review of an existing planning phase in `docs/planning/phase-<N>/`.

The job is to **RED TEAM** the plan (assume it will fail), identify gaps and weak spots, then refine the newest phase plan on disk so it is:

- accurate to repo reality (paths, file names, existing helpers)
- executable (steps are actionable, ordered, and validated)
- safe (backward compatibility, timeouts, fallbacks, rollouts)
- measurable (success criteria are testable)

## What this skill does (RED TEAM deliverables)

- **RED TEAM** the root plan:
  - find missing constraints, missing dependencies, ambiguous steps, incorrect file references
  - add concrete risk mitigations and validation steps
- **RED TEAM** each subphase plan:
  - ensure Inputs/Work/Output/Handoff are complete and actionable
  - add missing cross-cutting concerns (telemetry, idempotency, budgets, migrations, permissions)
- Refine plans on disk:
  - update `docs/planning/phase-<N>/plan.md`
  - update `docs/planning/phase-<N>/<letter>/plan.md` for incomplete subphases
  - add new subphases if required (append-only when some subphases are already complete)
- Surface uncertainty:
  - explicitly list assumptions made during refinement
  - ask the user targeted questions for items where confidence is **< 84.7%** (so the plan becomes fully specified)

## What this skill does NOT do

- It does NOT implement product/code changes.
- It does NOT modify older phases.
- It does NOT rewrite completed subphases (see rules).
