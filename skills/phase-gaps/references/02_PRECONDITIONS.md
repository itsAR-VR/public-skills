# Preconditions (RED TEAM)

Before you **RED TEAM** anything, establish the target phase and load the plan artifacts.

## Step 0 — Verify planning folder exists

1. Confirm `docs/planning/` exists.
2. List phase directories under it.

## Step 1 — Determine the target phase `<N>`

- If the user specifies a phase number, use it.
- Otherwise, **do not guess**: choose the highest numbered `docs/planning/phase-*/` directory.

## Step 2 — Verify required plan files

For `docs/planning/phase-<N>/` verify:

- `plan.md` exists
- each subphase folder in the root Subphase Index has `<letter>/plan.md`

If the Subphase Index references a folder that doesn’t exist, create it and scaffold the missing `plan.md` using the phase’s existing structure.

## Step 3 — Determine which subphases are “completed”

A subphase is complete if its `plan.md` contains non-empty **Output** and non-empty **Handoff** sections.

- Completed subphases are **read-only** for this skill.
- Incomplete subphases are eligible for refinement.

## Step 4 — Load plans

Read:

- Root: `docs/planning/phase-<N>/plan.md`
- Every subphase plan: `docs/planning/phase-<N>/<letter>/plan.md`

You cannot **RED TEAM** what you haven’t read.
