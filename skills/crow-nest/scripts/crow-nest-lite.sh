#!/usr/bin/env bash
# crow-nest-lite.sh — read-only dashboard streaming the agent message bus.
#
# Lite mode: pure shell, color-coded kinds, no Bun/Node dependencies.
# Use full mode (crow-nest.ts) when you want per-thread codex app-server
# JSON-RPC integration too.
#
# Usage:
#   crow-nest-lite.sh [--bus-dir <path>] [--tail-n <n>] [--filter-author <id>]
#                     [--filter-kind <k>] [--no-header]
#
# Hot keys (when stdin is a TTY):
#   q  quit
#   p  pause/resume
#   c  clear screen
#   ?  help

set -euo pipefail

BUS_DIR="${BUS_DIR:-$PWD/.bus}"
TAIL_N=20
FILTER_AUTHOR=""
FILTER_KIND=""
SHOW_HEADER=1

while [[ $# -gt 0 ]]; do
  case "$1" in
    --bus-dir)        BUS_DIR="$2"; shift 2 ;;
    --tail-n)         TAIL_N="$2"; shift 2 ;;
    --filter-author)  FILTER_AUTHOR="$2"; shift 2 ;;
    --filter-kind)    FILTER_KIND="$2"; shift 2 ;;
    --no-header)      SHOW_HEADER=0; shift ;;
    -h|--help)        sed -n '2,15p' "$0"; exit 2 ;;
    *) echo "crow-nest-lite: unknown arg: $1" >&2; exit 2 ;;
  esac
done

[[ -d "$BUS_DIR" ]] || { echo "crow-nest-lite: bus dir not found: $BUS_DIR" >&2; exit 2; }

# ANSI color codes by kind. Use \033 (octal) for bash 3.2 portability —
# `echo -ne "\e..."` does NOT interpret \e on macOS default bash.
color_for() {
  case "$1" in
    progress)   printf '\033[32m' ;;       # green
    correction) printf '\033[33m' ;;       # yellow
    directive)  printf '\033[35;1m' ;;     # magenta bold
    blocker)    printf '\033[41;97m' ;;    # red bg, white fg
    question)   printf '\033[34m' ;;       # blue
    ack)        printf '\033[37m' ;;       # gray
    vision)     printf '\033[36m' ;;       # cyan
    frame)      printf '\033[36;1m' ;;     # cyan bold
    decision)   printf '\033[97m' ;;       # white
    summary)    printf '\033[32;4m' ;;     # green underline
    paused)     printf '\033[2;37m' ;;     # dim gray
    *)          printf '\033[0m' ;;
  esac
}
RESET=$'\033[0m'
DIM=$'\033[2m'

render_message() {
  local F="$1" BASE TS AUTHOR KIND BODY
  BASE="$(basename "$F")"

  # Skip non-message files.
  [[ "$BASE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T ]] || return

  TS="${BASE%%--*}"
  REST="${BASE#*--}"
  AUTHOR="${REST%%--*}"
  REST2="${REST#*--}"
  KIND="${REST2%%.*}"
  KIND="${KIND%.md}"

  # Apply filters.
  [[ -n "$FILTER_AUTHOR" && "$AUTHOR" != "$FILTER_AUTHOR" ]] && return
  [[ -n "$FILTER_KIND"   && "$KIND"   != "$FILTER_KIND"   ]] && return

  # Body: first non-blank line after second `---`.
  BODY="$(awk '/^---$/{c++; next} c==2 && NF>0{print; exit}' "$F" 2>/dev/null | head -c 200)"

  local color reset
  color="$(color_for "$KIND")"
  reset="$RESET"

  # Compact ISO display: drop seconds for readability.
  local TS_DISP="${TS:0:16}"
  TS_DISP="${TS_DISP/T/ }"

  printf "%s%s %s%-18s %s%-12s%s %s\n" \
    "$DIM" "$TS_DISP" "$reset" \
    "$AUTHOR" "$color" "$KIND" "$reset" "$BODY"
}

print_header() {
  [[ "$SHOW_HEADER" -eq 0 ]] && return
  printf '\033[1m%-16s %-18s %-12s %s\033[0m\n' "TIME" "AUTHOR" "KIND" "BODY"
  printf "%s\n" "$(printf '─%.0s' $(seq 1 $(tput cols 2>/dev/null || echo 80)))"
}

# Backlog.
print_header
BACKLOG=()
while IFS= read -r line; do
  BACKLOG+=("$line")
done < <(ls "$BUS_DIR"/*.md 2>/dev/null | sort | tail -"$TAIL_N" || true)

for F in "${BACKLOG[@]+"${BACKLOG[@]}"}"; do
  render_message "$F"
done

# Live tail.
if command -v fswatch >/dev/null 2>&1; then
  fswatch -0 -e ".tmp$" "$BUS_DIR" | while IFS= read -r -d '' F; do
    [[ -f "$F" ]] && render_message "$F"
  done
elif command -v inotifywait >/dev/null 2>&1; then
  inotifywait -m -e close_write -e moved_to --format '%w%f' "$BUS_DIR" 2>/dev/null | while IFS= read -r F; do
    [[ -f "$F" ]] && render_message "$F"
  done
else
  echo
  echo "${DIM}crow-nest-lite: no fswatch/inotifywait — falling back to 2s polling${RESET}" >&2
  SEEN="$(ls "$BUS_DIR"/*.md 2>/dev/null | wc -l)"
  while sleep 2; do
    NOW="$(ls "$BUS_DIR"/*.md 2>/dev/null | wc -l)"
    if [[ "$NOW" -gt "$SEEN" ]]; then
      ls -t "$BUS_DIR"/*.md | head -n "$((NOW - SEEN))" | tac 2>/dev/null | while read -r F; do
        render_message "$F"
      done
      SEEN="$NOW"
    fi
  done
fi
