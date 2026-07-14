---
name: minimax-setup
description: >
  Install and verify the MiniMax Token Plan backend currently pinned by these
  wrappers to MiniMax-M2.7 (checked 2026-06-10) — Token Plan key,
  Anthropic-compatible endpoint, and the four wrapper scripts (claude-mm,
  ct-mm, claw-mm, claude-mm-sync) that route Claude Code / claw-code at
  MiniMax. Idempotent; safe to re-run. Use when: setting up a fresh machine,
  `ct-mm` / `claude-mm` not on PATH, `llm-council` skill failing at MiniMax
  step, or user asks to "set up minimax", "install minimax wrappers",
  "add minimax backend".
argument-hint: "[install|verify|key]"
allowed-tools: Bash, Read, Write
related_skills: [llm-council, setup-skill-packs]
---

# minimax-setup

Installs the MiniMax Token Plan backend for Claude Code and claw-code.

## What this provides

| Component | Destination | Purpose |
|---|---|---|
| `claude-mm` | `~/.local/bin/claude-mm` | Claude Code TUI → MiniMax backend |
| `ct-mm` | `~/.local/bin/ct-mm` | `cmux claude-teams` → MiniMax backend |
| `claw-mm` | `~/.local/bin/claw-mm` | `claw-code` Rust CLI → MiniMax backend |
| `claude-mm-sync` | `~/.local/bin/claude-mm-sync` | Symlink shared resources into MiniMax profiles |
| API key | `~/.config/minimax/token-plan.key` (chmod 600) | Token Plan secret (not in repo) |

All wrappers read the key from `~/.config/minimax/token-plan.key` and point
Claude Code / claw at `https://api.minimax.io/anthropic` (Anthropic-compatible,
NOT `/v1` — Token Plan keys only work against `/anthropic`).

Model/source check (2026-06-10): these wrappers still pin `MiniMax-M2.7` in
`bin/`, while MiniMax's official docs now recommend `MiniMax-M3` for coding
tools and list the Anthropic-compatible endpoint at
`https://api.minimax.io/anthropic/v1/messages`. Before changing model IDs,
re-check the MiniMax Token Plan and Anthropic-compatible API docs, then update
the wrapper scripts and this skill together.

## When to use

- Fresh-machine bootstrap after `setup-skill-packs` skips or fails the MiniMax phase
- `llm-council` skill fails at Step 4b (MiniMax curl) because the key is missing
- `ct-mm` / `claude-mm` not on PATH
- User says: "set up minimax", "install minimax wrappers", "add minimax backend"

## Prerequisites

- `bash` (already installed on macOS/Linux)
- A MiniMax Token Plan key starting with `sk-cp-` from
  https://platform.minimax.io/subscribe/coding-plan
- `~/.local/bin` on PATH (most shells; setup-skill-packs Phase 2 ensures this)
- `cmux` (optional, required for `ct-mm`) — installed as `/Applications/cmux.app/...`
- claw-code binary (optional, required for `claw-mm`) — built separately

## Execution flow

### Step 1 — Install the wrappers

```bash
bash "$(dirname "$(realpath "${BASH_SOURCE[0]:-$0}")")/scripts/install.sh"
```

Or from an installed skill dir:

```bash
bash ~/.claude/skills/minimax-setup/scripts/install.sh
```

This symlinks the four scripts from `bin/` into `~/.local/bin/`. Idempotent:
existing correct symlinks are left alone, stale symlinks get updated, real
files get preserved (with a warning — use `--force` to back them up).

### Step 2 — Register the API key

If `~/.config/minimax/token-plan.key` is missing or empty, prompt the user:

```bash
umask 077 && mkdir -p ~/.config/minimax && read -rs "K?Paste MiniMax Token Plan key: " && \
  printf '%s' "$K" > ~/.config/minimax/token-plan.key && unset K && \
  chmod 600 ~/.config/minimax/token-plan.key
```

Never echo the key or write it into the repo, shell history, or a log file.

### Step 3 — Verify

```bash
bash ~/.claude/skills/minimax-setup/scripts/verify.sh
```

This checks:
1. All 4 wrappers are on PATH and executable
2. Key file exists, is readable, is ~120-160 bytes, has no newline
3. A minimal curl against `https://api.minimax.io/anthropic/v1/messages`
   returns HTTP 200 with a valid response

On failure, the script prints which step broke and how to fix it.

## Wrapper behavior

### `claude-mm`
Launches Claude Code TUI pointed at MiniMax. Profile: `~/.claude-minimax`.
Auto-runs `claude-mm-sync solo` pre-exec so new skills/memories from the
main `~/.claude` profile propagate automatically.

### `ct-mm`
Launches `cmux claude-teams --dangerously-skip-permissions` pointed at
MiniMax. Profile: `~/.claude-minimax-teams`. Same auto-sync on launch.
Token Plan concurrent-request cap is ~5-10; teams of 3-5 panes safe.

### `claw-mm`
Launches the claw-code Rust binary pointed at MiniMax. Reads
`CLAW_BIN` env var (default: `~/Desktop/Codespace/claw-code/rust/target/debug/claw`).
Override with `CLAW_BIN=/path/to/claw claw-mm`. Rarely needed — use
`claude-mm` for the full TUI.

### `claude-mm-sync`
Idempotently symlinks shared resources from `~/.claude` into the MiniMax
profile dirs: skills, agents, commands, rules, contexts, hooks, plugins,
plans, chrome, ide, CLAUDE.md, `.claude.json`, settings. Sessions stay
isolated (each profile keeps its own `projects/<workspace>/sessions/`).

Flags: `--dry-run`, `--force`, `solo`, `teams`.

Also audits agent files for hardcoded `model: claude-sonnet-4-6` style
literals that would leak requests to Anthropic under claude-mm/ct-mm.

## Integration with other skills

- **llm-council** — Step 4b (MiniMax curl) requires the key file. If the key
  is missing, council fails. This skill is the prerequisite.
- **setup-skill-packs** — Phase 12.5 detects missing wrappers and invokes
  `scripts/install.sh` from this skill. Interactive key prompt is gated on
  `CLAW_SETUP_INTERACTIVE=1` (defaults on for macOS terminals; opt-in for CI).

## Troubleshooting

### `claude-mm: token-plan.key is empty`
The key file was created but has no content. Re-run Step 2 above and
double-check you pasted the key before hitting Enter.

### Wrappers installed but `claude-mm: command not found`
`~/.local/bin` is not on PATH. Add to your shell rc:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
```

### MiniMax returns 401
Key is stale, has a trailing newline, or was rotated. Check:
```bash
wc -c < ~/.config/minimax/token-plan.key   # expect ~120-160, no trailing \n
```
Rotate at https://platform.minimax.io/subscribe/coding-plan and re-save.

### MiniMax returns 429
Token Plan concurrent-request ceiling (~5-10). Wait 5s, retry. If you're
running `ct-mm` with many panes and the council at the same time, pause
one before running the other.

### `claw-mm: claw not found`
claw-code isn't built. Either build it:
```bash
cd ~/Desktop/Codespace/claw-code/rust && cargo build --workspace
```
Or skip — `claude-mm` covers the same use case with the full TUI.

## Design notes

- **Key file outside the repo**: `~/.config/minimax/token-plan.key` is the
  single source of truth. All four wrappers read from the same file, so
  rotation is one edit.
- **No env-var-only config**: storing the key in shell rc as
  `export ANTHROPIC_AUTH_TOKEN=...` would leak to every subshell and every
  process inheriting the environment. File-gated reads are safer.
- **Idempotent install**: re-running this skill on an already-configured
  machine is a no-op. Safe to invoke from setup-skill-packs every bootstrap.
