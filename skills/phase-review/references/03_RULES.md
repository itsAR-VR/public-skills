# Rules — non-negotiable

## Scope rules

- This is a review + verification skill.
- Do **NOT** implement new product/code changes.
- Only modify:
  - `docs/planning/phase-<N>/plan.md`
  - `docs/planning/phase-<N>/<letter>/plan.md` (only to fill missing Output/Handoff or append Review Notes)
  - `docs/planning/phase-<N>/review.md` (create/update)

## Truthfulness rules

- Do not claim checks passed unless you actually ran them.
- Record exact commands executed and whether they passed.
- If something fails (lint/build/db push), capture the error summary and list next steps.

## Quality gate rules

- Always run (from repo root):
  - `npm run lint`
  - `npm run build`

- If `prisma/schema.prisma` changed in the working tree:
  - attempt `npm run db:push`
  - if it fails (missing env/DB), record the failure and what’s needed to complete it

## Plan edit rules

- Do not rewrite completed subphases unless the content is factually wrong.
  - Prefer appending a short **Review Notes** section instead of rewriting.
- If Output/Handoff are missing, you may fill them based on evidence (git diff, commands run, produced artifacts).

## Minimal-change rule

Refine documentation, don’t refactor the entire plan.
- Keep changes small and directly tied to verification + accuracy.
