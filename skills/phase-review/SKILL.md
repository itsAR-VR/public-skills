---
name: phase-review
description: Review the newest docs/planning/phase-N after implementation; verify outcomes (lint/build), map evidence to success criteria, and write a post-implementation review.
related_skills: [skill-oracle, plan, phase-gaps, phase-implement, terminus-maximus, qa-test-planner]
---

# Instructions

Read all references in `references/` before using this skill.

**Target-phase input:** when the invocation names a specific
`docs/planning/<name>/` directory containing a `plan.md` — numbered
`phase-<N>` or a named plan dir, both allowed in the project (e.g. an orchestrator
like workflow-orchestrator pinning its phase) — review THAT phase: announce the resolved
directory first, and never substitute a newer concurrent phase. Default to
the newest phase only when no target is named.

## Skill Discovery

During review, run `/skill-oracle "<review concern>"` to discover skills that can assist with verification (e.g., qa-test-planner, code-review, seo-audit). Use matched skills to deepen the review where gaps are found.

## Multi-Agent Awareness

**IMPORTANT:** Multiple agents may be working on different phases concurrently. Post-implementation review must verify:

1. **Integration with concurrent work** — Did other phases modify the same files during implementation?
2. **Merge correctness** — If merges occurred, were they done correctly?
3. **Build stability** — Does the combined state of all concurrent work pass quality gates?
4. **Documentation alignment** — Do coordination notes (if any) match what actually happened?

When reviewing, always:
- Check git status for changes from other agents
- Verify build/lint against the current combined state (not just this phase's changes)
- Note any multi-agent coordination that occurred in the review

See `08_MULTI_AGENT_COORDINATION.md` for detailed procedures.

## Signals

- The user says: "review the phase", "post-implementation review", "did we finish phase N", "wrap up the phase", "verify the plan", "phase review".
- A `docs/planning/phase-<N>/plan.md` exists and implementation work has occurred.
- You need to confirm quality gates (at minimum: `npm run lint`, `npm run build`) and document results.

## References

**Directory:** `references/`

- `01_INTENT.md`
- `02_PRECONDITIONS.md`
- `03_RULES.md`
- `04_PROCEDURE.md`
- `05_TEMPLATES.md`
- `06_REVIEW_CHECKLIST.md`
- `07_EDGE_CASES.md`
- `08_MULTI_AGENT_COORDINATION.md`
