---
name: business-memory-signal-capture
description: >
  Captures durable business signal from conversation without over-tracking or
  task noise. Use for "remember this", "capture this", "durable memory",
  "future chats", corrections, decisions, preferences, operating rules, project
  facts, client facts, meeting signal, repeated friction, system improvement
  notes, build ideas, and reusable context that should survive later sessions.
  Route through business-context-intelligence first for broad context; use this
  skill when the primary job is durable signal capture.
related_skills:
  - business-context-intelligence
  - commitment-ledger
  - idea-to-build-intake
  - memory-systems
---

# Business Memory Signal Capture

Capture useful signal without turning every sentence into a task.

This skill is for durable business/build memory: decisions, corrections,
commitments, project facts, customer/client context, reusable rules, and ideas
with future value.

## Fast Path

Classify the signal, choose the canonical target, and either capture safely or
return a proposed capture when writing is not allowed.

Default to read-only collection and recommendation. Do not write memory, repo
docs, issue comments, CRM notes, or task updates unless the user asked for that
write or standing workspace rules explicitly allow that exact target.

## Escalate Only If Needed

Check existing memory/docs/issues only when duplication or sensitivity is
unclear.

## Safe Automatic Actions

- Propose a capture target and wording.
- Write only when the current instruction/workspace rules explicitly allow the
  exact target.
- Prefer project docs or issue comments for project facts, and cross-project
  memory only for reusable operating rules.
- Stop before saving sensitive raw content, secrets, credentials, private logs,
  or broad private communications.

## Signal Test

Capture only if at least one is true:

- Future agents would make a worse decision without it.
- It changes an operating rule, preference, project truth, or relationship
  context.
- It creates or closes a commitment.
- It is a reusable idea or repeated friction pattern.

## Capture

Capture when the message includes:

- A correction to agent behavior or naming.
- A durable decision or strategic preference.
- A project or client fact future work will need.
- A commitment, promise, deadline, or approval condition.
- A repeated friction point that should become a system improvement.
- A build idea that has enough shape to revisit.

Skip:

- Casual chatter.
- Duplicate facts already in the right source.
- Sensitive raw data, secrets, credentials, private logs, cookies, or auth state.
- Tiny implementation details with no future relevance.

## Route

- Project-specific facts -> target repo docs, plans, ADRs, or issue comments.
- Cross-project operating rules -> Codex/Alo memory or instructions.
- Commitments -> `commitment-ledger`.
- Build candidates -> `idea-to-build-intake`.
- Corrections -> corrections memory or canonical instruction layer.

If the current environment forbids direct memory writes or the target is
ambiguous, produce a proposed capture instead of writing.

## Output

When visible output is useful:

```text
Captured Signal
- Type:
- Canonical target:
- Why it matters:
- Proof/source:
- Next action:
```

## Guardrails

- Store summaries, not raw private content.
- Ask before saving when target or sensitivity is ambiguous.
- Prefer the most specific source of truth over duplicate memory entries.
