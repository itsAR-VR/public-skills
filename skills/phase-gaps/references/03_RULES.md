# Rules (RED TEAM) — non-negotiable

## Scope rules

- This skill is a **RED TEAM plan refinement** skill.
- Do **NOT** implement product/code changes.
- Only modify planning docs inside `docs/planning/phase-<N>/`.
- Do not modify older phases.

## RED TEAM rigor rules

- **RED TEAM means adversarial:** assume the plan will fail in production; find how and why.
- **RED TEAM means verify:** do not trust plan statements about repo structure; confirm paths, file names, and existing helpers.
- **RED TEAM means specificity:** every “gap” must include a concrete fix (add a step, add a constraint, add a validation, add a fallback).

## Edit rules (protect completed work)

- Do not rewrite completed subphases.
  - If a subphase has Output + Handoff, treat it as immutable.
- If new work is required after some subphases are complete:
  - add a new subphase folder (append next letter)
  - update the root Subphase Index by appending the new entry
  - write the new subphase plan using the same template style

## Plan quality rules

When refining:

- Correct wrong file references (e.g., `actions/settings-actions.ts` vs `actions/settings.ts`).
- Replace vague steps with actionable ones (specific functions/files/commands).
- Add missing cross-cutting concerns:
  - timeouts + budgets
  - idempotency + dedupe
  - telemetry + observability
  - schema migration + backfill
  - permissions + admin gating
  - rollback/fallback behavior
- Keep success criteria measurable.

## Confidence & human-input rules

- If you are **< 90% confident** about a requirement/decision (product intent, UX choice, integration behavior, rollout policy), do **not** silently “pick one”:
  - capture it as an explicit **Open Question (Need Human Input)** in the root phase plan (and in the relevant subphase plan when applicable)
  - ask the user at the end of the run (see procedure)
- If you are **≥ 90% confident** in your recommendation, proceed without asking, but still:
  - list the assumption you made (so humans can correct it)
  - include a mitigation question/check (optional) (“if this assumption is wrong, we should change X to Y”)

## Minimal-change rule

Refine, don’t rewrite from scratch.
- Prefer patching the existing plan structure.
- Add sections only when they reduce ambiguity or prevent failure.
