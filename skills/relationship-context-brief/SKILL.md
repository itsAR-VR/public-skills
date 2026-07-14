---
name: relationship-context-brief
description: >
  Prepares concise work-relevant context for people, companies, clients,
  prospects, partners, and teammates. Use before calls, meetings, messages,
  proposals, sales follow-ups, onboarding, teammate handoffs, "prepare me for my
  meeting", "what do we know about this prospect/client/person/company?", "last
  interaction", "open promise", "follow-up angle", or proposal conversation
  framing. Route through business-context-intelligence first for broad context;
  use this skill when the primary job is relationship history.
related_skills:
  - business-context-intelligence
  - conversation-context-hydrator
  - context-freshness-gate
  - commitment-ledger
  - open-loop-radar
  - priority-sensemaker
  - briefing
---

# Relationship Context Brief

Load who someone is, why they matter, and what history affects the next
conversation.

## Fast Path

Find who they are, the latest relevant interaction, open loops, and the next
recommended angle.

## Escalate Only If Needed

Check email, Slack, Fireflies, Drive, or calendar only when the brief depends on
recent communications or meeting context.

Use the narrowest relevant query. Prefer summaries, metadata, or snippets before
opening raw private communications.

## Safe Automatic Actions

- Gather work-relevant context from available sources.
- Draft but do not send follow-ups, emails, Slack replies, or proposals.
- Propose CRM, relationship-note, memory, or task updates when rules allow.
- Stop before broad private-source scans, sends, public/customer-facing actions,
  sensitive personal inference, money, credentials, or ambiguous durable writes.

## Brief Modes

- Call prep: concise context, likely goal, tone, and questions.
- Message draft: context plus recommended angle and commitments to mention.
- Proposal/sales: pain, prior asks, decision process, proof, and next ask.
- Teammate handoff: ownership, open loops, blockers, and next useful action.

## Freshness Rules

Check or label:

- Latest reply or interaction.
- Next meeting date or event.
- Last confirmed deal/project stage.
- Open promise owner and due date.
- Age of last meaningful interaction.

If recent interaction cannot be checked, mark the brief `partial`.

## Proactive Prep Triggers

When a watch or schedule exists, prepare a brief before:

- A call or meeting with a client, prospect, partner, or teammate.
- A proposal, follow-up, onboarding, or sales conversation.
- A commitment due date tied to that person/company.

Do not send messages automatically. Draft only.

## Gather

Use available sources:

- Existing person/company/client pages or repo docs.
- Meeting notes and Fireflies transcripts.
- Linear/GitHub context when tied to work.
- Email, Slack, CRM, Drive, or calendar when available and relevant.
- Prior commitments, open loops, proposals, and follow-ups.

Prefer recent direct interaction over old profile notes. If recent interaction
is unavailable, mark the brief as partial.

## Brief Shape

```text
Relationship Brief: [person/company]

Who They Are
- ...

Current Context
- ...

Recent History
- ...

Open Loops / Commitments
- ...

Recommended Tone / Angle
- ...

Blind Spots
- ...
```

## Use Cases

- Before a call or meeting.
- Before drafting an email, Slack, proposal, or follow-up.
- Before answering "what do we know about X?"
- Before deciding whether an idea or request is strategically important.

## Guardrails

- Do not invent relationship history.
- Flag stale or missing context.
- Keep sensitive raw communications out of the user-facing brief unless the
  user explicitly asks and the channel is appropriate.
- Keep the brief strictly work-relevant.
- Do not infer or summarize health, family, finances, politics, protected
  characteristics, or other sensitive personal attributes unless explicitly
  requested and necessary for the task.
- Never reuse private-channel content as a draft outbound message unless the
  user explicitly requests it.
