---
name: audit-inline-complexity
description: Audit inline complexity and recommend variable extraction; produces a report with flattening suggestions for nested expressions.
related_skills: [code-refactoring, code-review, naming-analyzer, audit-semantic-noise]
---

# Instructions

Read all references in `references/` before using this skill.

## Signals

- Reviewing code for nested calls or deep attribute chains
- Compound expressions that should be flattened with named intermediates
- The user asks to "audit complexity" or "flatten expressions"
- Readability concerns in conditionals, returns, or argument lists

## References

**Directory:** `references/`

- `01_GOAL.md`
- `02_DEFINITIONS.md`
- `03_INVARIANTS.md`
- `04_SCOPE.md`
- `05_CHECKS.md`
- `06_OUTPUT.md`
