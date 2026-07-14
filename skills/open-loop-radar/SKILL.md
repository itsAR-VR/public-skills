---
name: open-loop-radar
description: >
  Finds unresolved business and build loops: blockers, approvals, reviews,
  stale PRs, overdue issues, unassigned follow-ups, waiting decisions,
  commitments, proof gaps, unclosed work, and items to close, archive, or carry
  forward. Use when asked "what is open?", "what needs me/Matt?", "what is
  blocked?", "what can Codex advance?", "who is waiting?", "what is hanging?",
  "watch this", "keep an eye on this", "alert me if this goes stale", or during
  daily/weekly sweeps. Route through business-context-intelligence first for
  broad operating context; use this skill when the primary job is unresolved-work
  inventory.
related_skills:
  - business-context-intelligence
  - daily-business-context-sweep
  - commitment-ledger
  - proof-aware-status
  - priority-sensemaker
---

# Open Loop Radar

Find the work that is not safely closed.

An open loop is anything that needs a decision, proof, owner, follow-up,
approval, live test, merge, deployment, reply, or explicit cancellation.

## Scope Boundary

Own inventory of unresolved work. Use `commitment-ledger` for explicit promises
and `proof-aware-status` for judging whether one item is done.

Open-loop classification is read-only by default. Move or close Linear/GitHub
state only when the user asked for it or standing workflow rules explicitly
allow it, and only after citing proof that no approval/live-test/privacy gate
remains.

## Fast Path

Scan active issues, PRs, handoffs, and proof gaps. Return only loops with a
clear owner or clear next proof.

## Escalate Only If Needed

Check meetings, email, Slack, or relationship sources only when the loop likely
came from a person, commitment, or client/prospect follow-up.

## Safe Automatic Actions

- Inspect PR/CI, Linear issue state, local git status, and handoffs.
- Gather missing proof and recommend owners or closure candidates.
- Recommend status moves, but apply them only when allowed by user request or
  standing workflow rules.
- Stop before sends, deploys, money, credentials, public/customer actions, or
  ambiguous durable writes.

## Triage Lens

For each loop, determine owner, consequence, next proof, and age. A loop is
actionable only when a specific person or agent can do a specific next step.

## Proactive Watch Signals

Surface before Matt asks when a watch exists and:

- PR waits for review for more than 2 business days.
- CI/deployment fails for more than 24 hours.
- Blocked item is unchanged for more than 2 business days.
- Commitment is due within 24 hours or overdue.
- "Waiting on Matt" appears and one decision unlocks work.
- Same blocker appears in two sweeps.

Do not alert on low-risk cleanup, duplicate task noise, or items with no
available next action.

If the user asked to watch an item but no automation, heartbeat, or scheduled run
exists, treat the result as a one-time watch recommendation and say it is not
actively monitoring yet.

## Scan

Look for:

- Linear issues in Todo, In Progress, In Review, blocked, or stale states.
- PRs that are draft, failing, unmerged, waiting for review, or detached from
  their issue.
- Dirty worktrees with active project context.
- Handoffs with a next action or blocker.
- User promises, meeting follow-ups, client commitments, and approval asks.
- Proof gaps where something is described as done but lacks a test, screenshot,
  receipt, deployment, PR, or source readback.

## Classify Loops

- Matt decision needed.
- Codex/Jarvis can act next.
- Teammate/client/vendor needed.
- Proof missing.
- Stale and needs refresh.
- Should be closed or archived.
Use `overdue` for commitments past an explicit due date.

## Checklist

- Each loop has owner, next step, and proof to close.
- Matt-needed loops are separated from Codex-actionable loops.
- Stale loops name the refresh needed.
- Tiny/noisy fixes stay inside existing work.

## Loop Record

```text
Loop
- Item:
- Owner:
- Needed next:
- Proof to close:
- Age/freshness:
- Risk if ignored:
```

## Output

For normal inventory:

```text
Open Loops

Needs Matt
- ...

Codex/Jarvis Can Advance
- ...

Waiting Elsewhere
- ...

Stale Or Proof-Missing
- ...
```

For proactive watch alerts:

```text
Proactive Open-Loop Alert
Checked at: YYYY-MM-DD HH:MM TZ
Registration: active | proposed | not registered
Stop condition: ...

Triggered Because
- ...

Needs Matt
- ...

Codex/Jarvis Can Advance
- ...

Proof / Blind Spots
- ...

Recommended Next Action
1. ...
```

## Guardrails

- Do not create noisy tasks for tiny fixes.
- Do not close a loop just because a branch or note exists.
- If evidence only supports a recommendation, output "Recommended status move"
  instead of applying it.
- If the loop affects money, credentials, production, public/customer comms, or
  privacy, require explicit approval before action.
