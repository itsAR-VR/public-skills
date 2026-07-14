# Procedure

Execute these steps literally, in order.

## Step 1 — Select the phase

Follow `02_PRECONDITIONS.md` to pick `<N>`.

## Step 2 — Load phase plans

Read:

- `docs/planning/phase-<N>/plan.md`
- every `docs/planning/phase-<N>/<letter>/plan.md`

## Step 3 — Collect evidence

Gather high-signal evidence for what shipped:

- `git status` (are there uncommitted changes?)
- `git diff --name-only` (what files changed?)
- Optionally: `git diff` for key files referenced by the phase

If your environment is not a git checkout, document what you can (file mtimes, known artifacts).

## Step 4 — Run quality gates

From repo root, run:

- `npm run lint`
- `npm run build`

If `prisma/schema.prisma` changed:

- run `npm run db:push`

Record pass/fail + short error summaries in `review.md`.

## Step 5 — Review success criteria (evidence mapping)

In `docs/planning/phase-<N>/review.md`, create a section mapping:

- each Success Criterion → evidence (file paths, commands, screenshots/log snippets)

If a criterion is partially met, say so and list what remains.

## Step 6 — Update the phase plan docs

### 6.1 Root plan updates

Update `docs/planning/phase-<N>/plan.md`:

- check off success criteria that are met
- append a **Phase Summary** section:
  - what shipped
  - key decisions
  - links to artifacts / key files
  - any open issues

### 6.2 Subphase updates

For each subphase plan:

- If Output/Handoff is missing:
  - fill them from evidence (git diff, commands run, artifacts created)
- If Output/Handoff exists:
  - optionally append a short **Review Notes** section with validation/evidence references

## Step 7 — Finalize

Confirm the repository now contains:

- `docs/planning/phase-<N>/review.md` with a quick summary + evidence mapping + command results
- updated `docs/planning/phase-<N>/plan.md` with checked success criteria + Phase Summary
