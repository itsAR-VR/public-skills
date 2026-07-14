#!/usr/bin/env bash
# Bootstrap browser-harness on any device.
# Idempotent: safe to run repeatedly. Hardcodes a stable install path so
# `uv tool install -e .` keeps pointing at it across devices.

set -euo pipefail

REPO_URL="https://github.com/browser-use/browser-harness.git"
REPO_DIR="${BROWSER_HARNESS_DIR:-$HOME/.local/share/browser-harness}"

log() { printf '[browser-harness bootstrap] %s\n' "$*" >&2; }

ensure_path() {
  case ":$PATH:" in
    *":$HOME/.local/bin:"*) :;;
    *) export PATH="$HOME/.local/bin:$PATH";;
  esac
}

ensure_path

if command -v browser-harness >/dev/null 2>&1; then
  log "already on PATH: $(command -v browser-harness)"
  log "repo: $REPO_DIR"
  exit 0
fi

if ! command -v uv >/dev/null 2>&1; then
  log "installing uv (astral.sh)"
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ensure_path
fi

if [ ! -d "$REPO_DIR/.git" ]; then
  log "cloning $REPO_URL -> $REPO_DIR"
  mkdir -p "$(dirname "$REPO_DIR")"
  git clone --depth 1 "$REPO_URL" "$REPO_DIR"
else
  log "repo exists at $REPO_DIR, fetching latest"
  git -C "$REPO_DIR" pull --ff-only || log "pull failed, continuing with existing checkout"
fi

log "installing editable tool from $REPO_DIR"
(cd "$REPO_DIR" && uv tool install -e . --force)

ensure_path

if command -v browser-harness >/dev/null 2>&1; then
  log "OK: $(command -v browser-harness)"
  log "repo: $REPO_DIR"
  log ""
  log "next steps for the agent:"
  log "  1. cat $REPO_DIR/SKILL.md"
  log "  2. cat $REPO_DIR/helpers.py"
  log "  3. for cold-start browser bootstrap also read $REPO_DIR/install.md"
  exit 0
fi

log "ERROR: browser-harness not on PATH after install"
log "check that ~/.local/bin is on \$PATH in your shell rc"
exit 1
