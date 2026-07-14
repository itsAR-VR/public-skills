#!/usr/bin/env bash
set -euo pipefail

status=0

pass() {
  printf 'ok   %s\n' "$1"
}

fail() {
  printf 'fail %s\n' "$1" >&2
  status=1
}

check() {
  local label="$1"
  shift
  if "$@"; then
    pass "$label"
  else
    fail "$label"
  fi
}

check "claw-mm on PATH" command -v claw-mm
check "local claw binary executable" test -x "$HOME/Desktop/Codespace/claw-code/rust/target/debug/claw"
check "MiniMax key file exists and is non-empty" test -s "$HOME/.config/minimax/token-plan.key"
check "helper script parses --help" bash "$(dirname "$0")/run.sh" --help
check "claw-mm wrapper responds to --help" claw-mm --help

if [[ "$status" -ne 0 ]]; then
  echo "Repair missing prerequisites with ~/.codex/skills/minimax-setup/scripts/install.sh" >&2
fi

exit "$status"
