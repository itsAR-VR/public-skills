---
name: deep-sweep
description: Red-team a plan before implementation by checking assumptions, scope, failure modes, security, dependencies, and proof. Use before deep-build on nontrivial work.
license: MIT
related_skills: [deep-build, goal-post]
---

# Deep Sweep

Review the plan, not the implementation.

Check:

- Does the goal describe an observable outcome?
- Are assumptions separated from verified facts?
- Is the scope the smallest useful version?
- Does the plan follow existing repository patterns?
- Are trust boundaries, permissions, private data, and destructive actions handled?
- Are failure, empty, retry, rollback, and partial-success paths covered?
- Are dependencies necessary, maintained, and already available where possible?
- Can every success claim be proven by a test, readback, rendered artifact, or live surface?
- Are human or external gates named with an owner?

Return only material findings. For each one, give the failing assumption, consequence, and smallest correction. If there are no material findings, return `NO FINDINGS`.
