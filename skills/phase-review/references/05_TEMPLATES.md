# Templates

Use these templates when writing or updating the review.

## `docs/planning/phase-<N>/review.md` template

```md
# Phase <N> — Review

## Summary
- <1–5 bullets: what shipped, what passed, what remains>

## What Shipped
- <bullets + key file paths>

## Verification

### Commands
- `npm run lint` — <pass/fail> (<timestamp>)
- `npm run build` — <pass/fail> (<timestamp>)
- `npm run db:push` — <pass/fail/skip> (only if schema changed)

### Notes
- <short error summaries or confirmations>

## Success Criteria → Evidence

1. <criterion>
   - Evidence: <files/commands/logs>
   - Status: <met/partial/not met>

## Plan Adherence
- Planned vs implemented deltas (if any):
  - <delta> → <impact>

## Risks / Rollback
- <risk> → <mitigation>

## Follow-ups
- <action item>
- (Optional) Suggested next phase: Phase <N+1> — <title>
```

## Root plan Phase Summary appendix

```md
## Phase Summary

- Shipped:
  - <bullets>
- Verified:
  - `npm run lint`: <pass/fail>
  - `npm run build`: <pass/fail>
  - `npm run db:push`: <pass/fail/skip>
- Notes:
  - <open issues / follow-ups>
```

## Subphase Review Notes appendix

```md
## Review Notes

- Evidence:
  - <file paths / commands>
- Deviations:
  - <planned vs actual>
- Follow-ups:
  - <next steps>
```
