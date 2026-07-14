---
name: phantom
description: "Coordinate a Claude terminal co-pilot through tmux or cmux; use for Phantom, Phantom Ultra, Claude runner, terminal co-pilot, or Codex-to-Claude automation."
---

# Phantom

Use when the user asks for `Phantom`, `Phantom Ultra`, a Claude runner, a
terminal co-pilot, or Codex-to-Claude automation.

Phantom is an orchestration skill. It composes:

- `interactive-agent-control` for tmux sessions, durable pipe-pane logs, and
  safe send/capture/wait operations.
- `tmux` for low-level prompt/control fallback.
- `claude` for Claude CLI flags, model defaults, and effort handling.
- `control-cli` for bounded automation loops and cleanup discipline.
- `ecc-dmux-workflows` or CMUX/Ghostty only as optional visibility layers.

## Modes

- `Phantom`: preserve the user's normal Claude setup. Do not force a model or
  effort setting unless the user asks.
- `Phantom Ultra`: after Claude is live and the prompt is ready, send
  `/effort ultracode`. If Claude rejects it, try `/effort xhigh` and report the
  fallback.

## Runner Contract

1. Prefer a separate side-agent/cloud-runner when the current host supports
   subagents. The parent Codex session stays the integrator and user-facing
   owner.
2. If no side runner is available, run Phantom directly in the current agent.
3. Start a real interactive Claude terminal session. Do not use `claude -p`.
4. Use tmux plus pipe-pane logs as the control and proof surface. CMUX/Ghostty
   may show the session, but they are not the proof layer.
5. Drive Claude in a loop until it reaches a conclusion, asks a true blocker
   question, or hits the stop condition.
6. Summarize Claude's useful result back to the parent agent with the session
   name, log path, completion marker, and any unresolved blocker.
7. Stop the child session unless the user explicitly asks to keep it open.

## Start

Resolve the helper from the installed skill tree first, then the repo copy:

```bash
HELPER="${PHANTOM_CONTROL_HELPER:-$HOME/.codex/skills/interactive-agent-control/scripts/agent-tmux-control.sh}"
if [ ! -x "$HELPER" ]; then
  HELPER="skills/interactive-agent-control/scripts/agent-tmux-control.sh"
fi

NAME="phantom-$(date +%s)"
"$HELPER" start-claude \
  --name "$NAME" \
  --cwd "$PWD" \
  -- --permission-mode plan --setting-sources user --name phantom
```

For `Phantom Ultra`, wait for the Claude prompt, then set UltraCode:

```bash
"$HELPER" wait --name "$NAME" --pattern "Do you want|Yes|No|>|❯" --timeout 90
"$HELPER" send --name "$NAME" --text "/effort ultracode"
"$HELPER" wait --name "$NAME" --pattern "ultracode|xhigh|>|❯" --timeout 90
```

## Prompt Shape

Use `send-file` for large prompts. Include:

- Objective and desired output.
- Current repo/path/branch/status when relevant.
- Allowed actions and forbidden actions.
- Whether edits are allowed.
- Whether external systems may be mutated.
- A unique completion marker such as
  `PHANTOM_DONE_<timestamp>_<short-random>`.
- Instruction to ask at most one blocker question at a time.
- Instruction to avoid secrets, raw env values, cookies, tokens, and private
  transcript dumps.

Minimal prompt skeleton:

```text
You are Phantom, a Claude terminal co-pilot controlled by Codex.

Objective:
<task>

Scope:
<repo/path, branch, allowed files, non-goals>

Rules:
- Do not edit files unless explicitly allowed.
- Do not approve tool or permission prompts yourself.
- Do not expose secrets, tokens, cookies, raw env values, or private logs.
- Ask at most one blocker question at a time.
- When complete, end with exactly: PHANTOM_DONE_<token>

Return:
- Findings or recommended changes.
- Commands/proof you used.
- Blockers, if any, in plain English.
```

## Control Loop

1. Send the initial prompt with `send-file`.
2. Wait on the log for a fresh marker, blocker question, permission prompt, or
   timeout.
3. If Claude asks a bounded question and the answer is known from current
   context, answer it through `send`.
4. If Claude asks for permission, capture the prompt and ask the user unless
   the permission is already explicit, low-risk, and task-scoped.
5. If Claude reports a final answer, inspect enough log output to verify the
   completion marker came from Claude's response, not from the prompt echo.
6. Continue until the final marker appears, the user stops the run, or a real
   external blocker remains.

Useful commands:

```bash
"$HELPER" send-file --name "$NAME" --file /tmp/phantom-prompt.txt
"$HELPER" wait-log --name "$NAME" --pattern "PHANTOM_DONE_|Do you want|Yes|No|permission" --fresh --timeout 600
"$HELPER" log --name "$NAME" --tail 220 --plain
"$HELPER" capture --name "$NAME" --tail 120
"$HELPER" stop --name "$NAME"
```

## Safety

- Do not silently approve destructive, external, production, credential,
  payment, legal, or customer-facing actions.
- Do not send secrets or raw credential material to Claude.
- Do not run multiple write-capable child agents in the same checkout unless
  paths are explicitly non-overlapping.
- Do not paste raw pane logs into user-facing answers when they may contain
  sensitive material; summarize and cite the local log path instead.
- Keep the parent Codex agent responsible for final judgment. Claude's agreement
  is a signal, not proof.
