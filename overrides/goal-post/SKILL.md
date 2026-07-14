---
name: goal-post
description: Turn an outcome into a machine-checkable goal contract with actor, verifier, stop conditions, evidence, and human gates. Use before autonomous or multi-step execution.
license: MIT
related_skills: [deep-sweep, deep-build]
---

# Goal Post

Write a compact goal contract containing:

- **Outcome:** the observable end state
- **Scope:** allowed systems, files, and non-goals
- **Actor:** who or what performs the work
- **Verifier:** an independent check that does not trust the actor's claim
- **Evidence:** exact tests, readbacks, artifacts, or live surfaces required
- **Stop conditions:** success, unsafe state, repeated failure, budget, and time limits
- **Human gates:** sends, publishing, payments, credentials, production changes, and destructive actions
- **Ledger:** attempts, results, and remaining blockers

The verifier must test the outcome, not the actor's explanation. A loop without an independent verifier and explicit stop conditions is not ready to run.
