# Intent

This skill performs a **post-implementation review** of an existing planning phase in `docs/planning/phase-<N>/`.

The job is to verify what shipped, confirm the phase meets its success criteria, and leave a clean, auditable paper trail in the planning docs.

## Deliverables (written to disk)

1. Update the root plan: `docs/planning/phase-<N>/plan.md`
   - check off success criteria that are met
   - append a short **Phase Summary** (what shipped, key decisions, links)
   - optionally append a **Review Notes** section (what worked, what didn’t, follow-ups)

2. Write a dedicated review artifact: `docs/planning/phase-<N>/review.md`
   - includes a quick summary up top
   - records verification results (at minimum: `npm run lint`, `npm run build`)
   - maps each success criterion to evidence
   - lists gaps/follow-ups and (optionally) suggests a next phase

## What this skill does NOT do

- It does NOT implement new product/code changes.
- It does NOT modify older phases.
- It does NOT rewrite completed historical narrative unless strictly necessary for accuracy.
