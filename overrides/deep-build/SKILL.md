---
name: deep-build
description: Execute an approved implementation plan in small verified slices. Use after deep-sweep when building, fixing, or refactoring nontrivial software.
license: MIT
related_skills: [deep-sweep, deep-clean, goal-post]
---

# Deep Build

Build the smallest complete version of an approved plan.

1. Read the plan, repository instructions, target files, nearby patterns, and tests.
2. Confirm the branch and working tree are safe. Preserve unrelated local work.
3. Name the first independently useful slice and its success check.
4. Before changing shared symbols, inspect callers and downstream impact.
5. For bugs, reproduce the failure before changing code.
6. Implement one slice at a time. Keep every changed line tied to the plan.
7. Run the narrowest meaningful check after each slice.
8. Run regression checks proportional to risk before handoff.
9. Inspect the final diff for scope creep, secrets, private data, and dead code created by the change.
10. Record what changed, what passed, and any external or human gate still open.

Stop when the plan is satisfied and proven. Do not add speculative abstractions, unrelated cleanup, dependencies, or configuration.
