#!/usr/bin/env bash
# harness-autobrowse/scripts/finish-run.sh
# Mark the latest (or a specified) run as pass/fail/partial. Records the
# hypothesis tested and appends to history.jsonl.
#
# Usage:
#   bash finish-run.sh <task-name> <pass|fail|partial> "<one-line hypothesis>" [run-NNN]
#
# Exit codes:
#   0  recorded; prints "graduate-ready" if 2-of-last-3 met
#   1  bad arguments
#   2  task or run not found

set -uo pipefail

if [ $# -lt 3 ]; then
  echo "Usage: bash finish-run.sh <task-name> <pass|fail|partial> \"<hypothesis>\" [run-NNN]" >&2
  exit 1
fi

TASK_NAME="$1"
STATUS="$2"
HYPOTHESIS="$3"
RUN_NAME="${4:-latest}"

case "$STATUS" in
  pass|fail|partial) ;;
  *)
    echo "[harness-autobrowse] ERROR: status must be pass|fail|partial. Got: '$STATUS'" >&2
    exit 1
    ;;
esac

WORKSPACE="${HARNESS_AUTOBROWSE_WORKSPACE:-$PWD/harness-autobrowse}"
RUNS_DIR="$WORKSPACE/runs/$TASK_NAME"

if [ ! -d "$RUNS_DIR" ]; then
  echo "[harness-autobrowse] ERROR: no runs dir for task '$TASK_NAME' at $RUNS_DIR" >&2
  exit 2
fi

# Resolve run dir (latest is a symlink)
if [ "$RUN_NAME" = "latest" ]; then
  if [ ! -L "$RUNS_DIR/latest" ]; then
    echo "[harness-autobrowse] ERROR: no latest run — start one with start-run.sh" >&2
    exit 2
  fi
  RUN_NAME="$(readlink "$RUNS_DIR/latest")"
fi

RUN_DIR="$RUNS_DIR/$RUN_NAME"
if [ ! -d "$RUN_DIR" ]; then
  echo "[harness-autobrowse] ERROR: run '$RUN_NAME' not found at $RUN_DIR" >&2
  exit 2
fi

RUN_NUM="$(echo "$RUN_NAME" | sed -E 's/^run-0*//')"
ISO_TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

json_escape() {
  local value="$1"
  value=${value//\\/\\\\}
  value=${value//\"/\\\"}
  value=${value//$'\b'/\\b}
  value=${value//$'\f'/\\f}
  value=${value//$'\n'/\\n}
  value=${value//$'\r'/\\r}
  value=${value//$'\t'/\\t}
  printf '%s' "$value"
}

json_string() {
  printf '"%s"' "$(json_escape "$1")"
}

# Read the original started_at BEFORE we rewrite meta.json so the original
# run start time survives the status update.
ORIG_STARTED_AT=""
if [ -f "$RUN_DIR/meta.json" ]; then
  ORIG_STARTED_AT="$(grep '"started_at"' "$RUN_DIR/meta.json" 2>/dev/null \
    | sed -E 's/.*"started_at":[[:space:]]*"([^"]+)".*/\1/' \
    | head -1)"
fi
[ -z "$ORIG_STARTED_AT" ] && ORIG_STARTED_AT="$ISO_TS"

# Write status + hypothesis as plain files (cheap to grep)
printf '%s\n' "$STATUS" > "$RUN_DIR/status.txt"
printf '%s\n' "$HYPOTHESIS" > "$RUN_DIR/hypothesis.txt"

# Build meta.json with explicit JSON string escaping so this stays portable
# even when python3 is unavailable.
{
  printf '{\n'
  printf '  "task": %s,\n' "$(json_string "$TASK_NAME")"
  printf '  "run": %s,\n' "$RUN_NUM"
  printf '  "started_at": %s,\n' "$(json_string "$ORIG_STARTED_AT")"
  printf '  "finished_at": %s,\n' "$(json_string "$ISO_TS")"
  printf '  "status": %s,\n' "$(json_string "$STATUS")"
  printf '  "hypothesis": %s\n' "$(json_string "$HYPOTHESIS")"
  printf '}\n'
} > "$RUN_DIR/meta.json"

HIST="$RUNS_DIR/history.jsonl"
printf '{"ts":%s,"run":%s,"status":%s,"hypothesis":%s}\n' \
  "$(json_string "$ISO_TS")" \
  "$RUN_NUM" \
  "$(json_string "$STATUS")" \
  "$(json_string "$HYPOTHESIS")" >> "$HIST"

printf '%s\n' "[harness-autobrowse] Recorded $RUN_NAME: $STATUS — $HYPOTHESIS"

# Append iteration log line to strategy.md (so it accumulates as a record)
TASK_DIR="$WORKSPACE/tasks/$TASK_NAME"
if [ -f "$TASK_DIR/strategy.md" ] && grep -q '<!-- runs appended here -->' "$TASK_DIR/strategy.md"; then
  TMP="$TASK_DIR/strategy.md.tmp"
  awk -v line="- run $RUN_NUM ($ISO_TS): **$STATUS** — $HYPOTHESIS" '
    /<!-- runs appended here -->/ { print line; print; next }
    { print }
  ' "$TASK_DIR/strategy.md" > "$TMP" && mv "$TMP" "$TASK_DIR/strategy.md"
fi

# Check 2-of-last-3 graduation rule by parsing the last three JSONL rows with
# a whitespace-tolerant JSON field match.
PASS_COUNT=0
if [ -f "$HIST" ]; then
  PASS_COUNT="$(tail -n 3 "$HIST" | awk '
    /^[[:space:]]*\{.*"status"[[:space:]]*:[[:space:]]*"pass"/ { count++ }
    END { print count + 0 }
  ')"
fi

if [ "$PASS_COUNT" -ge 2 ]; then
  echo "[harness-autobrowse] GRADUATE-READY: $PASS_COUNT of last 3 passed."
  echo "  Run: bash scripts/graduate.sh $TASK_NAME"
else
  TOTAL_RUNS=$(wc -l < "$HIST" | xargs)
  echo "[harness-autobrowse] $PASS_COUNT/3 recent passes — keep iterating ($TOTAL_RUNS run(s) so far)."
fi
