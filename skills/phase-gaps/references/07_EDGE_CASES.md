# Edge Cases (RED TEAM)

## Missing phase plans

If `docs/planning/` has no `phase-*` folders, you cannot **RED TEAM** a plan.

- Ask the user if they want you to run `phase-plan` first.

## Missing subphase files

If the root plan’s Subphase Index references a subphase folder that doesn’t exist:

- Create the missing folder + scaffold `plan.md` using the phase’s template style.

## Some subphases already completed

If one or more subphases have Output + Handoff:

- Do **not** edit those subphase plans.
- Apply refinements to:
  - the root plan
  - incomplete subphases
  - new appended subphases (next letter) when needed

## Plan is already strong

A **RED TEAM** still produces value:

- confirm repo reality
- add small hardening steps (validation, rollback, telemetry)
- tighten success criteria

## User asks for implementation

If the user pivots from **RED TEAM** to execution:

- stop here and switch to `phase-implement` (execution) only after the plan is refined.
