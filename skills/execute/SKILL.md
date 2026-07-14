---
name: phase-implement
description: Execute an existing docs/planning/phase-N plan sequentially; completes subphases in order, appending outputs and handoffs.
related_skills: [skill-oracle, plan, phase-review, terminus-maximus, build, karpathy-guidelines]
---

# Instructions

Read all references in `references/` before using this skill.

## Skill Discovery

Before starting each subphase, run `/skill-oracle "<subphase task description>"` to discover relevant skills that can assist with implementation. Use matched skills as subroutines during execution. If a skill referenced in the plan is no longer available, note it in the subphase Output section and adapt.

## Multi-Agent Awareness

**IMPORTANT:** Multiple agents may be working on different phases concurrently. During execution:

1. **Before each subphase:** Run `git status` and re-read files you plan to modify
2. **When you encounter unexpected file state:** Another agent may have modified the file — check the last 10 phases
3. **When builds fail unexpectedly:** Check for schema changes or API changes from other phases
4. **Document conflicts:** Log any coordination issues in your subphase Output section

If a file you need has been modified by another phase:
- Read the other phase's plan.md to understand their changes
- Merge semantically (don't just overwrite)
- Note the integration in your Output section

See `06_MULTI_AGENT_COORDINATION.md` for detailed procedures.

## Signals

- The user says "execute the phase", "work through the subphases", "continue the plan"
- A phase folder exists with a root `plan.md` and subphase folders ready
- Work needs to proceed through an established planning structure

## References

**Directory:** `references/`

- `01_INTENT.md`
- `02_PRECONDITIONS.md`
- `03_RULES.md`
- `04_PROCEDURE.md`
- `05_OUTPUT.md`
- `06_MULTI_AGENT_COORDINATION.md`
