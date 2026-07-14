---
name: daily-business-context-sweep
description: >
  Sweeps current business and build context into a dated operating picture.
  Use for daily sweep, morning briefing, EOD/end-of-day recap, weekly business
  review, "what should I know today?", "what needs Matt today?", "what
  finished?", "what carries forward?", stale issues, failed automations, open
  PRs, blockers, proof, blind spots, wake-up briefings, proactive checks,
  drift prevention, or recurring watch reports. Route through
  business-context-intelligence first for broad ambiguous context; use this
  skill when the primary job is a dated operating sweep.
related_skills:
  - business-context-intelligence
  - open-loop-radar
  - priority-sensemaker
  - proof-aware-status
  - context-freshness-gate
  - briefing
---

# Daily Business Context Sweep

Create a daily operating picture across active business, product, and build
work. This is wider than a task list and wider than Linear.

## Fast Path

Check the current handoff, active Linear/GitHub work, dirty active repos, and
automation status. Then summarize only what matters today.

## Escalate Only If Needed

Use Fireflies, Gmail, Slack, Drive, or calendar only when the sweep depends on
meetings, people, client comms, or missing relationship context.

## Run Modes

- Morning: focus on what changed, what needs Matt, and the first useful action.
- End of day: focus on proof created, loops still open, and tomorrow's first
  action.
- Weekly: focus on aging work, recurring blockers, shipped proof, and strategic
  priorities for the next week.
- Proactive watch: focus only on watched objects that crossed thresholds or
  require a decision.

## Proactive Cadence

- Daily morning: active work, Matt-needed decisions, failed checks, and failed
  automations.
- End of day: proof created, unresolved loops, and tomorrow's first action.
- Weekly: stale PRs, blocked issues, overdue commitments, repeated friction, and
  ideas worth promoting or ignoring.
- Event-triggered: after CI/deploy failure, PR review request, automation
  failure, meeting transcript, or commitment due-date change.

If no schedule or heartbeat exists, recommend the watch contract instead of
claiming the sweep will recur.

## Sweep Order

Check only reachable sources:

1. Current handoff and durable decisions.
2. Active Linear lanes and issues relevant to Matt, AI builds, and company work.
3. GitHub PRs, CI, deployments, and recent repo activity.
4. Dirty or blocked local repos that are part of active work.
5. Codex automations, setup jobs, radar memories, and failed scheduled work.
6. Calendar/meeting context, Fireflies, Slack, Gmail, and Drive when available
   and relevant.
7. Recent user corrections, decisions, commitments, and approvals.

For each source, record whether it was checked, skipped as irrelevant, or
unavailable. Do not let one unavailable connector block the sweep.

## Checklist

- Dated output.
- Sources checked or named as blind spots.
- Matt-needed items separated from Codex-actionable work.
- Done claims backed by proof.
- One to three best next actions.

## Classify

For each item, mark:

- Active: work is moving.
- Waiting on Matt: decision, approval, review, credential, live test.
- Waiting on someone else: teammate, client, vendor, platform.
- Blocked: exact blocker is known.
- Stale: context likely drifted and needs refresh.
- Done: proof exists and no next action remains.

## Output

Use this shape:

```text
Daily Business Context - YYYY-MM-DD
Checked at: YYYY-MM-DD HH:MM TZ

Top Picture
- ...

Needs Matt
- ...

Active Work
- ...

Blocked Or Stale
- ...

Proof / Blind Spots
- ...

Best Next Actions
1. ...
```

For proactive mode, use the report shape in
`../business-context-intelligence/references/proactive-operating-loop.md`.

## Autonomous Follow-Through

- Summarize without asking when the task is read-only.
- Update Linear, docs, or memory only when current workspace rules allow it and
  the update is project-level, proof-backed, and non-duplicative.
- Prefer one strong recommendation over a long todo list.
- For private connectors, use narrow project/person/time-window queries. Stop
  and ask before broad private-history scans.

## Safe Automatic Actions

- Inspect active PR/CI, local git status, Linear issue state, and automation
  status when available.
- Gather missing proof and summarize it.
- Propose memory, Linear, or docs updates when rules allow, but avoid duplicate
  task noise.
- Stop before sends, deploys, money, credentials, customer/public actions, or
  ambiguous durable writes.

## Guardrails

- Linear is one source, not the whole operating picture.
- Do not mark work done without proof.
- Do not create or move tasks unless the task explicitly asks for it or normal
  workspace rules permit it.
- Name blind spots instead of filling them with guesses.
