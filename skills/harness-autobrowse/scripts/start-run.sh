#!/usr/bin/env bash
# harness-autobrowse/scripts/start-run.sh
# Begin a new iteration: create runs/<task>/run-NNN/ and snapshot strategy.md.
# Prints the run directory path on stdout (so callers can capture it via $()).
#
# Usage:
#   RUN_DIR=$(bash start-run.sh <task-name>)
#
# Exit codes:
#   0  run created — directory printed to stdout
#   1  bad arguments
#   2  task not initialized

set -uo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: bash start-run.sh <task-name>" >&2
  exit 1
fi

TASK_NAME="$1"
WORKSPACE="${HARNESS_AUTOBROWSE_WORKSPACE:-$PWD/harness-autobrowse}"
TASK_DIR="$WORKSPACE/tasks/$TASK_NAME"
RUNS_DIR="$WORKSPACE/runs/$TASK_NAME"

if [ ! -f "$TASK_DIR/task.md" ] || [ ! -f "$TASK_DIR/strategy.md" ]; then
  echo "[harness-autobrowse] ERROR: task '$TASK_NAME' not initialized." >&2
  echo "  Run: bash init.sh $TASK_NAME <url> \"<goal>\"" >&2
  exit 2
fi

mkdir -p "$RUNS_DIR"

# Find next run number
NEXT_NUM=1
if ls "$RUNS_DIR" 2>/dev/null | grep -qE '^run-[0-9]+$'; then
  LAST_NUM=$(ls "$RUNS_DIR" | grep -E '^run-[0-9]+$' | sed 's/^run-//' | sort -n | tail -1)
  NEXT_NUM=$((LAST_NUM + 1))
fi

RUN_NAME="$(printf 'run-%03d' "$NEXT_NUM")"
RUN_DIR="$RUNS_DIR/$RUN_NAME"

mkdir -p "$RUN_DIR/screenshots"

# Snapshot strategy.md as it stands at the start of this run
cp "$TASK_DIR/strategy.md" "$RUN_DIR/strategy.md"

# Write run metadata stub
cat > "$RUN_DIR/meta.json" <<EOF
{
  "task": "$TASK_NAME",
  "run": $NEXT_NUM,
  "started_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "status": null,
  "hypothesis": null
}
EOF

# Maintain a `latest` symlink for convenience
ln -sfn "$RUN_NAME" "$RUNS_DIR/latest"

# Stderr informational (so RUN_DIR=$(start-run.sh ...) keeps clean stdout)
{
  echo "[harness-autobrowse] Started $RUN_NAME for task '$TASK_NAME'"
  echo "  Strategy snapshot: $RUN_DIR/strategy.md"
  echo "  Screenshot dir:    $RUN_DIR/screenshots/"
  echo
  echo "Next: outer agent runs browser-harness, captures screenshots,"
  echo "      writes $RUN_DIR/summary.md, then calls finish-run.sh."
} >&2

# Stdout: the run dir path (stable for shell capture)
echo "$RUN_DIR"
