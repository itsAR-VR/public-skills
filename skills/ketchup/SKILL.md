---
name: ketchup
description: >
  Use when the user wants to catch up after time away and act on what needs
  them now. Triggers: "ketchup", "catch me up", "what did I miss", "what's
  new", "what do I need to do", "what needs me", "any fires?", a morning or
  return-from-away briefing, or a resync right after a meeting. Covers Slack,
  meeting transcripts, Linear, and email, plus calendar, GitHub, and handoffs.
related_skills:
  - grill-me
  - priority-sensemaker
  - open-loop-radar
  - daily-business-context-sweep
  - commitment-ledger
  - proof-aware-status
  - context-freshness-gate
---

# Ketchup

Catch up. Pull everything that landed while you were away into one ranked
picture of what needs you, then clear the fast stuff on approval instead of
just listing it.

Two jobs, in order: **(1) surface and rank** what needs you, **(2) execute the
quick wins** you approve. Be proactive: surface fires nobody asked about yet,
flag what is about to slip, and propose the next concrete move on each item. Go
deep inside each source, but keep the catch-up read-only. Only the quick-win arm
acts, and only after you approve.

## When to Use

- "Ketchup", "catch me up", "what did I miss", "what's new", "what needs me?"
- Returning from being away (overnight, a flight, a deep-work block, PTO).
- Resyncing right after a meeting or at the start of the day.
- You suspect something is slipping and want a fast, deep scan with action.

Not for: ranking a known list (use `priority-sensemaker`), a pure
unresolved-work inventory (use `open-loop-radar`), or a dated operating sweep
with no action arm (use `daily-business-context-sweep`). `ketchup` is the
comms-first catch-up that also *finishes* the small things.

## Fast Path

Lead with the four sources the user named (Slack, transcripts, Linear, email),
read recent narrow windows, rank what needs you, and surface the quick wins.
Widen to calendar, GitHub, and handoffs only when the named sources leave the
picture incomplete.

## Sweep Order (comms-first, go deep)

Use narrow, recent queries (default window: since the last catch-up, else last
24 to 72 hours). For each source record **checked**, **skipped (irrelevant)**,
or **unavailable**, so one dead connector never blocks the rest.

1. **Slack**: DMs, @-mentions, threads you are in, unread priority channels.
   Catch asks, decisions, and "can you..." pings aimed at you.
2. **Transcripts**: recent meeting transcripts (Fireflies / Granola). Action
   items assigned to you, decisions, and commitments you made out loud.
3. **Linear**: issues assigned to you, review requests, status changes,
   comments and mentions, and items that went stale or overdue.
4. **Email**: unreplied threads needing you, time-sensitive asks, and anything
   waiting on your reply.
5. Calendar: today's meetings, prep needed, conflicts.
6. GitHub: PRs awaiting your review, failing CI, review comments on your PRs.
7. Handoffs, memory, commitments, and recent decisions or approvals.

Read the thread, not just the preview, but stay inside narrow project, person,
and time windows. Stop and ask before any broad private-history scan.

## Rank by Priority

Rank what you found before showing it. Borrow `priority-sensemaker`'s lens:

- **Higher**: you are the blocker and one move unlocks others; a client or team
  commitment is time-sensitive; a deadline or meeting is imminent; risk grows if
  ignored.
- **Lower**: interesting but not tied to a current outcome; blocked on someone
  else with no action for you; cleanup with no immediate risk.

When ranking depends on live state (PR/CI, deploy, deadlines, commitments), run
`context-freshness-gate` first so the call is not built on stale inputs.

## Classify

Sort every surfaced item into one bucket:

- **Needs you**: a decision, reply, review, or approval only you can give.
- **Quick win**: a ~5-minute, reversible or draft step you can clear now.
- **Waiting on others**: a teammate, client, or vendor owes the next move.
- **Blocked**: the exact blocker is known and named.
- **Done**: proof exists and no next action remains.

## Quick Wins: Approve and Finish

This is the part that makes `ketchup` more than a briefing. After ranking,
separate out the **quick wins** and offer to clear them.

**A quick win is one concrete step that is all of:**
- about 5 minutes or less,
- reversible, internal, or a draft you can review,
- unambiguous owner = you or the agent,
- needs no new decision.

Examples: reply or draft to a Slack or email thread, triage or label a Linear
issue, add a comment, file a follow-up issue or task, snooze or close a resolved
loop, book a calendar hold, jot a decision to memory or docs, request a review.

**Not a quick win** (route to the ranked list, never auto-run): anything
multi-step, anything needing a real decision, sending consequential external
comms, money, credentials, deploys, deletes or overwrites, or public and
customer actions. Draft these; never finish them on a batch approval.

**The loop:**
1. Present the quick wins as one batch and ask which to run (an approval prompt,
   multi-select, e.g. `AskUserQuestion`). Show the exact drafted content for
   anything that sends or writes.
2. On approval, execute them as **dynamic workflows**: fan the independent ones
   out in parallel and run dependent ones in sequence (e.g. the `Workflow` tool).
3. Report each as **done with proof** (link, ID, draft text, status change). If
   one fails, say so with the error. Never claim done without proof.
4. Leave un-approved and non-quick items in the ranked list as next actions.

Send-class items (external email or Slack of consequence) stay drafts until the
user approves the exact text. The batch approval covers internal and reversible
actions, not new outward sends.

## When Confused, Grill Me

If the catch-up is genuinely ambiguous, **invoke `grill-me`** before acting. Do
not guess and do not dump a vague list. Trigger it when:

- Priorities conflict or two "urgent" items compete and the right order is unclear.
- It is unclear what "done" means for a surfaced item.
- A quick win could be read more than one way (which thread, what reply, whose ask).
- Sources disagree (a transcript commitment contradicts a Linear status).

`grill-me` interviews one question at a time with a recommended answer. It also
persists each resolved branch to disk (under `docs/references/`). Keep the
sweep's read-only promise: do not let that persistence run silently mid-catch-up.
Resolve the ambiguity in-conversation, then fold any decision-log write into the
quick-win approval batch (or skip persistence if you decline). Continue the
catch-up once aligned. If nothing is ambiguous, skip grill-me. Do not grill for
its own sake.

## Output

```text
Ketchup - YYYY-MM-DD HH:MM TZ
Window: since <last catch-up / last 24 to 72 hours>
Sources checked: Slack, Transcripts, Linear, Email, Calendar
Sources skipped or unavailable: GitHub (name each and why)

Needs You First
1. <item> - <why it is top> - <next step>

Then
2. ...

Quick Wins (approve to finish)
[ ] <draft reply to ...>
[ ] <label or triage issue ...>
[ ] <file follow-up ...>

Waiting On Others / Blocked
- ...

Proof / Blind Spots
- <what was verified> · <what could not be checked>
```

After approval, append:

```text
Finished
- <quick win> -> <proof: link / ID / status>
Still open
- <anything that needs you next>
```

## Safe Automatic Actions

- Read Slack, transcripts, Linear, email, calendar, GitHub, and handoffs, then
  summarize.
- Rank, classify, and gather missing proof, all read-only.
- After explicit approval, run reversible or internal quick wins and report proof.
- Stop before sends of consequence, deploys, money, credentials, deletes, or
  public and customer actions. Draft and confirm exact content first.

## Guardrails

- The catch-up sweep is read-only; nothing writes or executes before approval,
  including `grill-me`'s decision-log persistence. Fold that write into the
  approval batch; never let it run silently mid-sweep.
- One unavailable connector never blocks the rest. Name it as a blind spot.
- Do not confuse loud with important; surface fewer items with stronger evidence.
- Never mark a quick win done without proof.
- Keep narrow private queries; ask before broad private-history scans.
- If you are confused, grill. Do not guess.
