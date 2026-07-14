---
name: context-freshness-gate
description: >
  Checks whether context is current enough to trust before Codex/Jarvis answers
  or acts. Use for "is this stale?", "verify live", "browse or memory?", "old
  meeting notes", "checked-at timestamp", "source timestamp", old proof,
  PR/repo drift, deployments, schedules, pricing, laws, docs, automations,
  people/company state, proactive refresh, or any claim that may have changed.
  Route through business-context-intelligence first for broad context; use this
  skill when the primary job is deciding whether to verify or label staleness.
related_skills:
  - business-context-intelligence
  - conversation-context-hydrator
  - proof-aware-status
  - daily-business-context-sweep
---

# Context Freshness Gate

Use this before relying on facts that can drift.

The gate decides whether the agent can answer from known context, must verify
live/current state, or must label the answer as stale.

## Fast Path

Decide whether the claim can drift, whether verification is cheap, and whether a
wrong answer would matter. Then verify, label stale, or answer.

## Escalate Only If Needed

Do broader source checks only when the answer affects priority, status, external
action, money, production, privacy, or public/customer communication.

## Safe Automatic Actions

- Check current repo, PR, CI, deployment, automation, issue, or docs state when
  safe and available.
- Return stale/unknown labels with exact refresh steps.
- Stop before external actions, state changes, sends, money, production, privacy
  exposure, credentials, or broad private-source searches.

## Freshness Defaults

- Current chat instruction: current for intent, not proof.
- Local repo/git/PR/CI/deployment/automation status: verify when cheap.
- Calendar, pricing, laws, schedules, docs, people/company state: verify live
  when the answer depends on current truth.
- Memory/handoff: useful context, but stale for current status unless recently
  refreshed or backed by live proof.

## Proactive Refresh Triggers

Refresh proactively when a watch exists and:

- Proof is older than the latest commit, PR update, deployment, or automation
  run.
- A customer-facing claim depends on old proof.
- Relationship context is older than 14 days before a call.
- Schedule, pricing, laws, docs, or vendor state could affect a decision.
- A connector was unavailable in the last sweep and the item is still important.

## Drift Check

Ask:

- Could this have changed since the last memory or handoff?
- Is the claim about current status, price, schedule, deployment, PR, CI, legal
  rule, API docs, connector auth, automation, or person/company state?
- Is verification cheap and safe?
- Would a wrong answer cause bad work, external action, or bad prioritization?

## Actions

- Verify live/current when cheap and relevant.
- If verification is unavailable, label the answer as memory-derived or stale.
- If the source is stale but still useful, separate "known last state" from
  "needs refresh."
- If high stakes, do not proceed on stale context.

## Decision Table

| Situation | Action |
| --- | --- |
| Cheap live check exists | Verify before answering |
| Connector unavailable | Say unavailable, use fallback, name blind spot |
| High-stakes or external action | Stop or ask until current proof exists |
| Stable background fact | Answer without unnecessary refresh |

## Checklist

- Drift risk identified.
- Verification cost considered.
- Stakes considered.
- Current, likely current, stale, or unknown label assigned.
- Blind spot or refresh step named when needed.

## Output

```text
Freshness: current / likely current / stale / unknown
Checked at: YYYY-MM-DD HH:MM TZ
Basis:
- ...
Source timestamps:
- ...
Refresh needed:
- yes/no, because ...
```

## Guardrails

- Do not use old memory to override current source truth.
- Do not browse or hit external systems unnecessarily for stable facts.
- Do not claim a refresh was done if it was not.
