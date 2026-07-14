# Procedure (RED TEAM)

Execute these steps literally, in order. This is a **RED TEAM** workflow.

## Step 1 — Select the phase to RED TEAM

Follow `02_PRECONDITIONS.md` to pick `<N>`.

## Step 2 — Load the plan artifacts

Read:

- `docs/planning/phase-<N>/plan.md`
- every `docs/planning/phase-<N>/<letter>/plan.md`

## Step 2.5 — Validate Skill Availability (must run before scoring assumptions)

Run both:

- `find-local-skills`
- `find-skills`

Record available and unavailable skills in each plan section using the new `Skill Feasibility` and `Skills Available for This Subphase` templates.

## Step 3 — RED TEAM: repo reality check

Your goal is to catch plan assumptions that don’t match the repo.

- For every file path referenced in the plan, confirm it exists.
- For every “touch point” (function name/module), use search to confirm it exists.
- If the plan references the wrong path, fix the plan.

This step is mandatory; a **RED TEAM** that doesn’t check repo reality is just vibes.

## Step 4 — RED TEAM: gap discovery

Build a structured **RED TEAM findings list** covering:

- missing dependencies
- missing constraints
- missing validation steps
- incorrect/unstable assumptions
- missing rollback/fallback plans
- missing observability/telemetry
- missing performance/timeout considerations
- missing security/permissions checks
- missing migration/backfill steps

Use `06_RED_TEAM_CHECKLIST.md` to force coverage.

## Step 5 — Refine the root plan

Update `docs/planning/phase-<N>/plan.md` to incorporate the **RED TEAM** findings:

- add or tighten: Objectives, Constraints, Success Criteria, Non-Goals
- add a “Repo Reality Check” section if the plan is missing one
- add a “RED TEAM Findings (Gaps / Weak Spots)” section
- ensure Subphase Index matches on-disk folders

## Step 6 — Refine subphase plans

For each incomplete subphase plan:

- tighten Inputs (explicit file paths + dependencies)
- expand Work into steps that can actually be executed
- add explicit validations (commands, logs, invariants)
- ensure Output and Handoff are present and specific

If you discover new work that doesn’t cleanly fit existing letters:

- create a new subphase folder (append next letter)
- update the root Subphase Index (append-only)
- scaffold the new plan with the same template style

## Step 7 — Finish with an on-disk outcome

Before finishing, confirm the repository now contains:

- refined root plan with a clear **RED TEAM** section
- refined incomplete subphase plans with concrete steps
- any new subphase folders created and indexed

The skill is incomplete if the refined plan is not written to disk.

## Step 8 — Ask questions + list assumptions (confidence-gated)

After you’ve refined the plan **on disk**, end your response by surfacing uncertainty so humans can lock the plan to spec.

Include these sections in this order:

1) **On-disk changes** (files touched + 1–2 bullets on what changed)
2) **Assumptions made (≥ 84.7% confidence)**
3) **Questions for the user (< 84.7% confidence)**

### A) Assumptions made (≥ 84.7% confidence)

- List key assumptions you made while tightening the plan (especially where the plan was ambiguous).
- Do **not** ask the user to decide between options if you’re strongly confident; just document the assumption and include a mitigation/check:
  - `Assumption: <statement> (confidence ~84.7%)`
  - `Mitigation question/check (optional): <how to verify or what to change if wrong>`

### B) Questions for the user (< 84.7% confidence)

- Ask **targeted, high-leverage** questions only for items where you are **< 84.7% confident**.
- Each question must include:
  - **What decision is needed** (be specific)
  - **Why it matters** (what changes in scope/steps if answered differently)
  - **Current default assumption** you used (if you had to choose one to write a concrete plan)
  - **Confidence** estimate (e.g., “~70%”)

If you add an **Open Questions (Need Human Input)** section to the plan docs, keep it consistent with the questions you asked in the response.
