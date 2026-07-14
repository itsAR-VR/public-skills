# Pane Layout

Default 3-column TUI layout. Customize via `~/.crow-nest/config.json`:

```json
{
  "layout": "3-col",
  "colors": { "progress": "green", "correction": "yellow" },
  "tail_n": 50,
  "summary_cadence_min": 100
}
```

## Layout modes

### `3-col` (default)

```
┌── Threads ──┐ ┌── Pane focus ──┐ ┌── Flow ──┐
```

- Threads (left, 30%): one row per monitored thread + heartbeat. Goal
  state badge, tokens / budget, turn count, blocker/question count.
- Pane focus (center, 40%): full content of the currently-selected
  pane. Latest progress message, recent corrections, open
  questions/blockers.
- Flow (right, 30%): chronological cross-thread bus stream. Newest at
  top by default; toggle with `t`.

### `2-col`

```
┌── Threads ──┐ ┌── Flow ──┐
```

For narrow terminals (< 120 cols).

### `flow-only`

```
┌── Flow (full width) ──┐
```

The simplest mode — just streaming the bus, no per-thread panes.
Equivalent to running `crow-nest-lite.sh` but with hot keys.

## Hot keys

Global:
| Key | Action |
|---|---|
| `q` | Quit |
| `?` | Show help overlay |
| `space` | Pause/resume live updates |
| `r` | Reconnect app-server children when full mode was explicitly enabled |
| `t` | Toggle Flow direction (newest top vs newest bottom) |

Pane navigation:
| Key | Action |
|---|---|
| `↑↓` | Scroll within current pane |
| `←→` / `1-9` | Switch to threads pane / flow pane / N-th thread |
| `tab` | Cycle panes |
| `e` | Open current message in `$EDITOR` |

Thread-specific:
| Key | Action |
|---|---|
| `g` | Show latest goal state from notifications, if available |
| `s` | Reserved for local extensions; reference client does not call `skills/list` |
| `m` | Reserved for local extensions; reference client does not call `model/list` |
| `f` | Filter Flow to this thread's author |

Approval handling:
| Key | Action |
|---|---|
| `a` | Show approval details only; approve/decline in the original Codex session |

## Color coding

Defaults (configurable):

| Kind | Color | Why |
|---|---|---|
| `progress` | green | continuous flow — easy to skim |
| `correction` | yellow | needs attention but not urgent |
| `directive` | magenta bold | high authority, rare |
| `blocker` | red bg | stop the world |
| `question` | blue | input needed |
| `ack` | gray | thread closed |
| `vision` | cyan | scope-level |
| `frame` | cyan bold | decomposition reframe |
| `decision` | white | durable record |
| `summary` | green underline | rolling roll-up |

Priority overrides color saturation:
- `priority: 1` adds bold.
- `priority: 2` adds blink (most terminals ignore; falls back to
  reverse video).

## Filters

```bash
# Only show messages from one author
crow-nest --filter-author codex-1

# Only show one kind
crow-nest --filter-kind blocker

# Combine
crow-nest --filter-author codex-1 --filter-kind correction,directive
```

In TUI: `f` opens an inline filter prompt. Filters apply only to the
Flow pane; threads pane is always full-coverage.

## Cold-start behavior

On launch:

1. Reads `.bus/cursors/crow-nest.txt`. If not found, shows last 20
   bus messages.
2. Connects to listed app-server streams only when launched with
   `--app-server`.
3. Renders.
4. Does not advance cursor or write `.bus/`; replay is bounded by
   `tail_n`.

## State file

`.crow-nest/state.json`:

```json
{
  "threads": ["tid_abc123", "tid_def456"],
  "lastSeenCursor": "2026-05-08T11-18-02Z",
  "windowSize": [80, 24],
  "filters": {}
}
```

Read to remember which threads to monitor across sessions. The reference
client does not write this file; create or edit it outside the dashboard.

## Customization beyond config.json

Edit `crow-nest.ts` directly. The reference impl is intentionally < 400
LoC so it's hackable. For a polished TUI, layer `blessed`,
`blessed-contrib`, or `ink` on top — the JSON-RPC + bus parsing
machinery is already separated from rendering.
