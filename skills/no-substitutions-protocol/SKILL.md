---
name: no-substitutions-protocol
description: "Use when the user gives a list, asks for a specific approach, invokes /ns, says no substitutions/no subs, or when the agent is tempted to narrow scope, defer work, switch approaches, or give up before exhausting the requested path."
---

# No-Substitutions Protocol

The default is: do all of it, exactly as asked. Obstacles are gone through, not around.

Use this when the user lists multiple items, directs a specific approach, or invokes `/ns`, `NS`, "no subs", or "no substitutions".

## Rule

- If the user gives a list, do every item in a sensible order.
- If the user asks for X, deliver X, not a lighter substitute.
- If X hits an obstacle, try to solve the obstacle before asking to change direction.
- Do not unilaterally defer, narrow, simplify, or replace the requested work.
- Giving up or substituting is a user-level decision, not an agent-level convenience.

## What This Rules Out

- "Which should I focus on first?" when the user already gave a list.
- "I'll skip this for now."
- "Since the requested route is hard, I'll do this other route."
- "Let's simplify this by doing less."
- "I verified by code review instead of using the browser tool you asked for."

## Legitimate Exceptions

Ask the user only when there is genuine ambiguity or a structural blocker that changes the nature of the work. Use the judgment-call protocol: explain the situation in plain English, recommend one path, and let the user decide.

## Recovery When Invoked

If the user types `/ns`, identify what was substituted or deferred, undo that direction if possible, and return to the exact requested scope.
