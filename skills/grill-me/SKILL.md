---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, explore the codebase instead.

## Persist what you resolve

Do not leave resolved decisions in chat — that is the seam where intent gets
lost on the next session or handoff. As each branch settles, write it to disk:

- If `docs/references/vision-lock.md` exists, record the resolved decision in its
  Amendments log (or the relevant field) so the frozen intent stays current and
  `goal-post`'s verifier can grade against it.
- Otherwise, append a short dated decision log to
  `docs/references/grill-me-decisions.md` (create it, and the `docs/references/`
  directory, if absent) — one line per resolved branch (decision + why). Record
  the decisions, not a transcript.

This makes the grill durable across sessions and gives downstream stages a real
record to build and verify against.
