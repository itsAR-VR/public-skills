---
name: commitment-ledger
description: >
  Extracts and tracks explicit promises, owed actions, approvals, deadlines,
  decisions owed, owners, due dates, and follow-ups across business and build
  work. Use for "I promised", "we committed", "who owes what?", "track the
  promise", "send by Friday", "due before Monday", "after this call/meeting",
  "client reply", "build review", approvals, waiting-on items, or handoff
  commitments. Route through business-context-intelligence first for broad
  context; use this skill when the primary job is explicit owner-action
  commitment tracking.
related_skills:
  - business-context-intelligence
  - open-loop-radar
  - business-memory-signal-capture
  - relationship-context-brief
  - proof-aware-status
---

# Commitment Ledger

Track commitments so they do not disappear across chats, meetings, or builds.

## Scope Boundary

Own explicit owner-action commitments. Use `open-loop-radar` for unresolved
work without a promise and `idea-to-build-intake` for vague future ideas.

## Fast Path

Extract owner, owed-to, action, due/trigger, source, status, and proof needed to
close.

Default to read-only extraction and recommendation. Do not write memory, repo
docs, issue comments, CRM notes, or task updates unless the user asked for that
write or standing workspace rules explicitly allow that exact target.

## Escalate Only If Needed

Check source systems only when the commitment's current status or due date is
unclear.

## Safe Automatic Actions

- Extract commitments from the current prompt, handoff, or checked source.
- Propose ledger entries and carry-forward items.
- Write/update a ledger, issue, docs, or memory only when rules allow the exact
  target.
- Stop before sends, public/customer-facing actions, money, credentials, or
  ambiguous durable writes.

## Commitment Test

Record a commitment only when there is an owner plus an owed action. If either
is missing, treat it as a possible open loop or idea, not a commitment.

## What Counts

Record commitments when there is:

- Owner: Matt, Codex/Jarvis, teammate, client, vendor, or partner.
- Action: reply, review, approve, send, build, test, decide, pay, sign, deploy.
- Timing: explicit date, relative deadline, event, or "before X".
- Dependency: waiting on a person, proof, credential, meeting, or decision.

## Ledger Entry

```text
Commitment
- Owner:
- Owed to:
- Action:
- Due / trigger:
- Source:
- Status: open / waiting / done / canceled
- Status may also be overdue when past an explicit due date.
- Proof needed to close:
```

## Routing

- Personal or cross-project commitment -> memory/handoff or daily sweep output.
- Project commitment -> target repo docs or Linear issue comment.
- Client/prospect commitment -> relationship context and appropriate CRM/source.
- Build approval -> proof-aware status and open-loop radar.

If the commitment has a date or external person attached, include it in the
next daily sweep or relationship brief even if no task is created.

Carry unresolved dated commitments into the weekly review until closed with
proof or explicitly canceled.

## Proactive Commitment Rules

- Surface commitments due within 24 hours.
- Mark commitments overdue after the explicit due date.
- Carry overdue commitments into daily sweeps until closed or canceled.
- Before a relationship brief, include commitments tied to that person/company.
- Do not create new tasks for vague "we should" language; route those to
  `idea-to-build-intake`.

## Guardrails

- Do not create a commitment from vague brainstorming.
- Do not mark done without proof or explicit cancellation.
- Do not store sensitive raw content; summarize safely.
