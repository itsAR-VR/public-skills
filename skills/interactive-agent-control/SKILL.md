---
name: interactive-agent-control
description: "Launch and steer interactive Claude/Codex agents through tmux with durable pipe-pane logs; use CMUX/Ghostty only as optional visibility."
---

# Interactive Agent Control

Use when the user wants this agent to manage another live agent through a real
terminal session. This skill is for **interactive TUI control**, not one-shot
`claude -p` / `codex exec`.

## Contract

- Launch Claude/Codex inside tmux so the child agent behaves like a normal
  interactive session.
- Attach `tmux pipe-pane` immediately. The log file is the durable proof
  surface; pane capture is for current state and prompt detection.
- Send prompts with `tmux send-keys -l -- "<text>"` followed by `Enter`.
- Capture with `tmux capture-pane -p -S -` for full scrollback when it fits,
  and read the pipe log for complete output.
- Use CMUX or Ghostty only for operator visibility. Do not rely on GUI
  screenshots as the source of truth.

## Start

Prefer the helper script:

```bash
skills/interactive-agent-control/scripts/agent-tmux-control.sh start-claude \
  --name claude-ui \
  --cwd "$PWD"
```

This starts normal interactive `claude`. It does not use `claude -p`.

For Codex:

```bash
skills/interactive-agent-control/scripts/agent-tmux-control.sh start-codex \
  --name codex-backend \
  --cwd "$PWD" \
  -- --no-alt-screen
```

Use `REAL_CODEX=1` in the environment when the local Codex round-robin wrapper
is quarantined or when you need the real Codex binary:

```bash
REAL_CODEX=1 skills/interactive-agent-control/scripts/agent-tmux-control.sh \
  start-codex --name codex-backend --cwd "$PWD" -- --no-alt-screen
```

The helper passes the parent environment through to the child process; there is
no separate `REAL_CODEX` flag.

## Steer

```bash
skills/interactive-agent-control/scripts/agent-tmux-control.sh send \
  --name claude-ui \
  --text "Read the repo, then tell me the safest next action. Do not edit files."
```

Use `send-file` for large prompts:

```bash
skills/interactive-agent-control/scripts/agent-tmux-control.sh send-file \
  --name claude-ui \
  --file /tmp/agent-prompt.txt
```

## Observe

```bash
skills/interactive-agent-control/scripts/agent-tmux-control.sh capture \
  --name claude-ui --tail 120

skills/interactive-agent-control/scripts/agent-tmux-control.sh log \
  --name claude-ui --tail 200 --plain
```

Use `--plain` for human readback. The raw pipe log intentionally keeps the
original TUI stream.

Wait for a visible pane prompt or marker before sending follow-up:

```bash
skills/interactive-agent-control/scripts/agent-tmux-control.sh wait \
  --name claude-ui \
  --pattern "Human:|Do you want|Yes|No|❯|>"
```

For long-running jobs, wait against the durable pipe log. Use `--fresh` when
the marker must appear after the wait command starts:

```bash
skills/interactive-agent-control/scripts/agent-tmux-control.sh wait-log \
  --name claude-ui \
  --pattern "DONE|PASS|FAIL" \
  --fresh \
  --timeout 300
```

List managed sessions:

```bash
skills/interactive-agent-control/scripts/agent-tmux-control.sh list
```

## CMUX

CMUX is useful for visible teams:

```bash
/Applications/cmux.app/Contents/Resources/bin/cmux claude-teams
/Applications/cmux.app/Contents/Resources/bin/cmux codex-teams
```

But if the parent agent needs reliable capture/control, keep a tmux session and
pipe log as the evidence layer. CMUX/Ghostty can mirror or contain the operator
view; tmux owns automation.

## Safety

- Do not silently approve permission prompts. Capture the prompt, decide if it
  is task-scoped, then send the answer.
- Do not put secrets into prompts, pane logs, or bus messages.
- Do not run multiple write-capable agents in the same checkout unless their
  allowed paths are non-overlapping.
- Stop sessions explicitly when done.

```bash
skills/interactive-agent-control/scripts/agent-tmux-control.sh stop \
  --name claude-ui
```
