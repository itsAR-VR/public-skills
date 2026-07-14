# Preconditions

Before reviewing, establish the target phase and load the plan artifacts.

## Step 1 — Verify planning folder exists

1. Confirm `docs/planning/` exists.
2. List phase directories under it.

## Step 2 — Determine the target phase `<N>`

- If the user specifies a phase number, use it.
- Otherwise, choose the highest numbered `docs/planning/phase-*/` directory.

## Step 3 — Verify required plan files

For `docs/planning/phase-<N>/` verify:

- `plan.md` exists
- each subphase folder in the root Subphase Index has `<letter>/plan.md`

If the Subphase Index references a folder that doesn’t exist, create it and scaffold the missing `plan.md` using the phase’s existing structure.

## Step 4 — Load plans

Read:

- Root: `docs/planning/phase-<N>/plan.md`
- Every subphase: `docs/planning/phase-<N>/<letter>/plan.md`

## Step 5 — Determine “completion” state (plan hygiene)

A subphase is considered complete if its `plan.md` includes non-empty **Output** and non-empty **Handoff**.

- If a subphase is incomplete, the review should still proceed, but you must clearly note it in `review.md` and in the root Phase Summary.
