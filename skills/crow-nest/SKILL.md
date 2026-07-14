---
name: crow-nest
description: >
  Multi-agent situational awareness dashboard. Renders the agent message
  bus and (optionally) live Codex `codex app-server` JSON-RPC notifications
  in a multi-pane TUI so a human operator can scan progress, blockers,
  questions, and corrections across many parallel agents without spawning
  or controlling them. Use when the user wants a "crow's nest", "control
  tower", "mission control", "multi-Codex monitor", "agent dashboard", or
  "watch many agents at once". Read-only by design — never writes to the
  bus or sends RPC commands. Pairs with codex (/goal mode), agent-message-bus,
  and claude-heartbeat-loop.
metadata:
  author: public-skills
  version: 1.0.0
related_skills:
  - agent-message-bus
  - codex
  - claude-heartbeat-loop
  - orchestrate
  - terminus-maximus
  - coding-agent
compatibility: [claude-code, codex, openclaw]
---

# Crow's Nest

Read-only dashboard for the **Codex `/goal` + Claude heartbeat + Crow's
Nest** topology. Renders:

- The shared `agent-message-bus` `.bus/` directory live (every author
  every kind, color-coded by kind).
- *(Optional)* `codex app-server` JSON-RPC notifications from each
  active Codex thread (`turn/started`, `turn/plan/updated`,
  `item/agentMessage/delta`, and goal-state notifications when emitted).

Read-only is the entire safety model. Lite mode is the default and never
touches `codex app-server`. Full mode is opt-in and sends only the
initial app-server `initialize` handshake; it does not resume, start,
interrupt, approve, decline, or otherwise steer threads. Crow's Nest
never writes to the bus.

## When to Use

Use this skill when:

- Multiple agents (Codex `/goal`, Claude heartbeat, human, other doers)
  are running concurrently and you want **one screen** that shows all
  of them.
- You want to **scan from across the room** for red badges (blockers,
  priority-1 questions) instead of reading every message.
- You want **live RPC stream** of one or more Codex threads (full mode).

Don't use this skill when:

- You only have one agent. Just `tail -f .bus/*.md` is enough.
- You need the dashboard to **act** on what it sees. That's the
  `claude-heartbeat-loop`'s job; Crow's Nest is the watcher's watcher.
- You want a desktop GUI app. Use [CodexMonitor]
  (https://github.com/Dimillian/CodexMonitor) or
  [Sonol Multi-Agent](https://github.com/volition79/sonol-multi-agent)
  — productionized Tauri/Electron clients of the same `codex
  app-server` protocol.

## Two modes

### Lite mode (`scripts/crow-nest-lite.sh`)

Pure shell, no dependencies beyond `fswatch` (macOS) or `inotifywait`
(Linux). Tails `.bus/` and renders messages with kind-coded ANSI colors.

Use this when:

- You're starting out and just want eyes on the bus.
- You don't have the experimental `codex app-server` enabled.
- You're SSH'd into a remote workspace and Bun isn't installed.

```bash
~/.claude/skills/crow-nest/scripts/crow-nest-lite.sh
# Streams new bus messages with color-coded kinds.
# Cmd: --bus-dir <path>, --filter-author <id>, --filter-kind <k>, --tail-n <n>
```

### Full mode (`scripts/crow-nest.ts --app-server`)

Bun reference client for `codex app-server`. Spawns N stdio child
processes (one per Codex thread to monitor), parses JSON-RPC
notifications, and streams bus/app-server status to stdout. The
multi-pane layout in `references/panes.md` is the target layout for TUI
extensions.

Use this when:

- You have `codex app-server` working.
- You want notification-only token usage / goal state in addition to the bus.
- You want a Bun-based scaffold for adding richer pane/hot-key behavior.

```bash
bun ~/.claude/skills/crow-nest/scripts/crow-nest.ts --app-server
# Interactive TUI. Press ? for help.
```

Setup for full mode:

```bash
cd ~/.claude/skills/crow-nest/scripts
bun install   # currently only installs dev types; runtime uses Bun/Node stdlib
```

## Architecture

```
                      .bus/ (markdown event log)
                          ▲
                          │ fs-watch (chokidar / fswatch)
                          │
                  ┌───────┴───────┐
                  │  Crow's Nest  │
                  │   read-only   │
                  └───────┬───────┘
                          │ JSON-RPC 2.0 over stdio (full mode only)
              ┌───────────┼───────────┐
              ▼           ▼           ▼
       codex app-server  codex app-server  ...
       (thread A)        (thread B)
```

The bus is the **always-on** data source. The app-server connections
are **optional augmentation** — they give per-thread token / turn /
goal-state metadata that doesn't fit in markdown messages.

## Pane layout

Default 3-column TUI:

```
┌── Threads (left, 30%) ──┐ ┌── Pane focus (center, 40%) ──┐ ┌── Flow (right, 30%) ──┐
│ ▲ codex-1   pursuing    │ │  codex-1                       │ │ 11:14 codex-1 progress│
│   tokens 412k / 1M      │ │  Latest: progress              │ │ 11:15 claude correctn │
│   turn 124              │ │  ──────                        │ │ 11:15 codex-1 ack    │
│   ⚠ 1 blocker          │ │  Hit detection 87/100. Failing │ │ 11:16 codex-2 progrss │
│                         │ │  in tests/combat/multi_hit_*.  │ │ 11:17 codex-2 progress│
│   codex-2   pursuing    │ │  Next: fix batching in         │ │ 11:18 codex-1 progress│
│   tokens 88k / 500k     │ │  src/combat/resolver.ts:142.   │ │ ...                   │
│   turn 47               │ │                                │ │ (newest at top)       │
│                         │ │ ──────                         │ │                       │
│ * claude-watcher        │ │ Recent corrections: 1          │ │                       │
│   (heartbeat, opus)     │ │ Open questions: 0              │ │                       │
└─────────────────────────┘ └────────────────────────────────┘ └──────────────────────┘
   ↑↓ select   ⇥ cycle    space pause    g goal    a details   q quit   ? help
```

Color coding (configurable):
- `progress` — green
- `correction` — yellow
- `directive` — magenta bold
- `blocker` — red bg
- `question` — blue
- `ack` — gray
- `vision` / `frame` — cyan
- `decision` — white
- `summary` — green underline
- `paused` — dim gray

## Codex app-server protocol (full mode)

The `codex app-server` subcommand exposes JSON-RPC 2.0 over stdio (and
optionally `--listen ws://127.0.0.1:4500` with capability-token auth).
Crow's Nest documents these methods, but the reference client only sends
`initialize` by default:

Protocol drift check: last checked on 2026-06-10 against local
`REAL_CODEX=1 codex-cli 0.134.0` using `codex app-server --help` and
`codex app-server generate-json-schema --experimental`. Refresh this
section and `references/protocol.md` when the local app-server help or
generated schema changes.

| Method | Purpose |
|---|---|
| `initialize` | Initial handshake only |
| `thread/list` | Documented read method; reference client does not call it by default |
| `thread/start` | Crow's Nest does NOT call this — would create a thread it doesn't own |
| `model/list` | Documented read method; reference client does not call it by default |
| `skills/list` | Documented read method; reference client does not call it by default |
| `thread/goal/get` *(experimental)* | Documented read method; reference client does not call it by default |

Notifications consumed:

| Notification | Rendered as |
|---|---|
| `turn/started` | Increment turn counter |
| `turn/completed` | Refresh tokens used |
| `turn/plan/updated` | Show in pane focus when paused on this thread |
| `item/agentMessage/delta` | Buffer into "latest" line |
| `item/completed` | Mark line as complete |
| `thread/status/changed` | Update goal state badge |
| `item/commandExecution/requestApproval` | Red badge; approve in the original Codex session |
| `item/fileChange/requestApproval` | Red badge; approve in the original Codex session |

**Approval policy.** Crow's Nest surfaces approval requests but does NOT
respond to them. The human must approve or decline in the original Codex
session. This preserves the dashboard's read-only invariant.

Full protocol: `references/protocol.md`.

## Cold start

When Crow's Nest launches:

1. Reads `.bus/cursors/crow-nest.txt` to find its last seen timestamp.
2. Renders all bus messages **since** that cursor (no advance).
3. If full mode was explicitly started with `--app-server`, connects to
   any `codex app-server` instances listed in `.crow-nest/state.json`.
4. Starts `chokidar` for live bus updates.
5. Does not advance the bus cursor or write `.bus/`; cold-start replay is
   controlled by `--tail-n` and filters.

## Threading & scale

Tested with:

- Up to **8 concurrent Codex threads** (8 panes, 8 stdio app-server
  children).
- Bus rate up to **~10 messages/minute aggregate** (above that,
  rendering is fine but you can't read it; raise summary cadence in
  `claude-heartbeat-loop`).
- Bus backlog up to **2000 files** before rendering noticeably stutters
  (rotate via `bus-archive.sh --keep 200`).

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Pane stuck on "connecting…" | `codex app-server` child crashed | Hot key `r` reconnects; if persistent, restart from outside |
| Bus pane empty, threads visible | `chokidar` not installed (full mode) or `fswatch`/`inotifywait` missing (lite mode) | `bun install` for full mode; `brew install fswatch` or `apt install inotify-tools` for lite |
| Goal state always "unknown" | Reference client does not call `thread/goal/get`; app-server metadata is notification-only unless you extend the client | Use lite mode for bus truth, or extend full mode knowingly |
| Approval requests not surfacing | Default codex sandbox is permissive; approvals only fire for `--sandbox workspace-write` and stricter | Confirm sandbox mode in the underlying Codex session |
| Crashes corrupted bus | Should be impossible — read-only by design | If you see this, file a bug — Crow's Nest never writes |

## See also

- `agent-message-bus/SKILL.md` — the bus we render.
- `agent-message-bus/references/crow-nest-integration.md` — sister doc
  describing the same wiring from the bus's perspective.
- `claude-heartbeat-loop/SKILL.md` — the watcher whose corrections
  appear in our pane focus.
- `codex/SKILL.md` — Codex `/goal` mode + app-server JSON-RPC overview.
- [`CodexMonitor`](https://github.com/Dimillian/CodexMonitor) — Tauri
  desktop app, productionized client of the same protocol.
- [`Sonol Multi-Agent`](https://github.com/volition79/sonol-multi-agent)
  — local-first SQLite-backed dashboard.
- `references/protocol.md` — full JSON-RPC method/notification spec.
- `references/panes.md` — pane layout details and customization.
