---
name: priority-sensemaker
description: >
  Turns messy business/build context into ranked priorities and next actions.
  Use for "what should I do first/next?", "what matters most?", "rank these",
  "leverage and urgency", "what can wait?", "what should I ignore?", "fake
  urgency", "which decision unlocks the most work?", "sequence today", "best
  next action", or choosing between projects. Route through
  business-context-intelligence first for broad context; use this skill when
  the primary job is ranking known options.
related_skills:
  - business-context-intelligence
  - daily-business-context-sweep
  - open-loop-radar
  - proof-aware-status
---

# Priority Sensemaker

Convert noisy context into a short priority call.

The job is not to list everything. The job is to separate leverage, urgency,
risk, and blocked work.

## Fast Path

Rank the known options by unlock value, urgency, risk, and proof proximity.
Return the smallest actionable list.

When ranking depends on current status, deadlines, deployments, PR state, or
commitments, run `context-freshness-gate` first.

## Escalate Only If Needed

Run a daily sweep or open-loop scan only when the option set is incomplete or
the user asks for a broad operating view.

## Safe Automatic Actions

- Rank known work, identify stale inputs, and propose one to three next actions.
- Run freshness/proof checks when priority depends on current state.
- Suggest task updates only when they are project-level and allowed.
- Stop before changing priorities in Linear/GitHub, sending messages, spending,
  deploying, or touching credentials.

## Time Horizon

Choose the horizon first:

- Now: next 1-2 actions that unblock work today.
- Today: the best order for active work.
- Week: strategic sequencing, stale work, and commitments.
- Watch: only items that crossed a threshold or need escalation.
- Later: capture ideas without letting them hijack active priorities.

## Inputs

Use current context from:

- Daily business sweep.
- Open loop radar.
- Linear and GitHub state.
- Meetings, client/prospect context, and commitments.
- Active builds and proof status.

## Ranking Heuristics

Rank higher when:

- Matt is the blocker and one decision unlocks work.
- A client/prospect/team commitment is time-sensitive.
- A build is close to proof, merge, demo, or revenue impact.
- A stale or broken automation could create hidden drift.
- Risk grows if ignored.

Rank lower when:

- It is interesting but not connected to a current outcome.
- It is blocked by someone else with no action available.
- It is cleanup with no immediate risk.
- It is a micro-fix that belongs inside existing work.

## Score Quickly

Use this rough scoring when context is messy:

- Unlocks people or revenue: +3
- Matt is the blocker: +3
- Proof/merge/demo is close: +2
- Risk grows with time: +2
- No clear next action: -2
- Duplicate/noisy/micro-fix: -3

## Output

```text
Priority Call

Do First
1. ...

Do Next
2. ...

Can Wait
- ...

Ignore For Now
- ...

Why
- ...
```

## Guardrails

- Keep the list short enough to act on.
- Do not confuse loud with important.
- If evidence is thin, mark the recommendation as tentative.
- If freshness or proof is weak, mark the ranking tentative and name what needs
  verification.
- In proactive mode, surface fewer items with stronger evidence. Suppress
  interesting-but-not-actionable items.
