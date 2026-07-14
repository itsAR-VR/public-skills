---
name: deep-clean
description: Remove accidental complexity after a working implementation without changing behavior. Use after deep-build when the diff needs a focused simplification pass.
license: MIT
related_skills: [deep-build]
---

# Deep Clean

Start from working, tested code. Preserve behavior.

Remove only complexity introduced or exposed by the current change:

- unused imports, variables, branches, and helpers
- duplicate logic that has a clear existing home
- speculative abstractions and configuration
- comments that repeat the code
- needless dependencies or wrappers
- temporary debugging and proof scaffolding

Do not reformat unrelated files, rename unrelated symbols, modernize neighboring code, or turn cleanup into a refactor. Run the same verification before and after. If cleanup makes the diff harder to review, revert the cleanup.
