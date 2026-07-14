#!/usr/bin/env bash
# harness-autobrowse/scripts/graduate.sh
# Promote a task's strategy.md to a browser-harness domain skill at
# ~/.local/share/browser-harness/domain-skills/<site>/<task>.md
# (or wherever BROWSER_HARNESS_DIR points).
#
# Usage:
#   bash graduate.sh <task-name> [--force]
#
# Verifies 2-of-last-3-pass rule unless --force is given.
#
# Exit codes:
#   0  graduated
#   1  bad arguments
#   2  task not found
#   3  graduation rule not met (use --force to override)
#   4  browser-harness install dir missing

set -uo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: bash graduate.sh <task-name> [--force]" >&2
  exit 1
fi

TASK_NAME="$1"
FORCE=0
[ "${2:-}" = "--force" ] && FORCE=1

WORKSPACE="${HARNESS_AUTOBROWSE_WORKSPACE:-$PWD/harness-autobrowse}"
TASK_DIR="$WORKSPACE/tasks/$TASK_NAME"
RUNS_DIR="$WORKSPACE/runs/$TASK_NAME"
HARNESS_DIR="${BROWSER_HARNESS_DIR:-$HOME/.local/share/browser-harness}"

if [ ! -f "$TASK_DIR/strategy.md" ]; then
  echo "[harness-autobrowse] ERROR: task '$TASK_NAME' not found at $TASK_DIR" >&2
  exit 2
fi

if [ ! -d "$HARNESS_DIR" ]; then
  echo "[harness-autobrowse] ERROR: browser-harness install dir missing at $HARNESS_DIR" >&2
  echo "  Run: bash $HOME/.claude/skills/browser-harness/scripts/bootstrap.sh" >&2
  exit 4
fi

# Verify 2-of-last-3 rule
HIST="$RUNS_DIR/history.jsonl"
if [ "$FORCE" -eq 0 ]; then
  if [ ! -f "$HIST" ]; then
    echo "[harness-autobrowse] ERROR: no history yet for task '$TASK_NAME'." >&2
    exit 3
  fi
  if ! command -v python3 >/dev/null 2>&1; then
    echo "[harness-autobrowse] ERROR: python3 required to parse history.jsonl." >&2
    exit 3
  fi
  # Parse history.jsonl with python3 — matches the formatting that
  # finish-run.sh writes (json.dumps with default whitespace) and is
  # robust to future format changes.
  read -r PASS_COUNT TOTAL <<< "$(HIST="$HIST" python3 -c '
import json, os
with open(os.environ["HIST"]) as f:
    lines = [l.strip() for l in f if l.strip()]
total = len(lines)
pc = 0
for line in lines[-3:]:
    try:
        if json.loads(line).get("status") == "pass":
            pc += 1
    except Exception:
        pass
print(pc, total)
')"
  LAST_3_STATUSES=$(HIST="$HIST" python3 -c '
import json, os
with open(os.environ["HIST"]) as f:
    lines = [l.strip() for l in f if l.strip()]
out = []
for line in lines[-3:]:
    try:
        out.append(json.loads(line).get("status", "?"))
    except Exception:
        out.append("?")
print(" ".join(out))
')
  if [ "$PASS_COUNT" -lt 2 ] || [ "$TOTAL" -lt 3 ]; then
    echo "[harness-autobrowse] ERROR: 2-of-last-3-pass rule not met." >&2
    echo "  Last 3 statuses: $LAST_3_STATUSES" >&2
    echo "  Pass with --force to graduate anyway." >&2
    exit 3
  fi
fi

# Extract site from task.md
SITE="$(grep -E '^\*\*Site:\*\*' "$TASK_DIR/task.md" | head -1 | sed -E 's/^\*\*Site:\*\*[[:space:]]+(.+)$/\1/' | xargs)"
if [ -z "$SITE" ]; then
  echo "[harness-autobrowse] ERROR: could not extract Site: line from $TASK_DIR/task.md" >&2
  exit 2
fi

DEST_DIR="$HARNESS_DIR/domain-skills/$SITE"
DEST_FILE="$DEST_DIR/$TASK_NAME.md"
mkdir -p "$DEST_DIR"

ISO_DATE="$(date -u +%Y-%m-%d)"
RUN_COUNT=0
if [ -f "$HIST" ]; then
  RUN_COUNT=$(wc -l < "$HIST" | xargs)
fi

# Compose the graduated skill: header + strategy.md content
{
  echo "# $SITE / $TASK_NAME — browser-harness domain skill"
  echo
  echo "**Source:** Graduated from harness-autobrowse on $ISO_DATE after passing"
  echo "2 of the last 3 iterations (across $RUN_COUNT total run(s))."
  echo "**Last verified:** $ISO_DATE"
  echo
  echo "---"
  echo
  cat "$TASK_DIR/strategy.md"
} > "$DEST_FILE"

cat <<EOF
[harness-autobrowse] Graduated.

  From:  $TASK_DIR/strategy.md
  To:    $DEST_FILE

Next steps:
  1. Review $DEST_FILE — make sure the heuristics read cleanly for the
     next agent who lands on this site.
  2. Open a PR back to browser-use/browser-harness so other agents inherit
     the map:
         cd $HARNESS_DIR
         git checkout -b domain-skills/$SITE/$TASK_NAME
         git add domain-skills/$SITE/$TASK_NAME.md
         git commit -m "domain-skills: add $SITE/$TASK_NAME"
         git push -u origin domain-skills/$SITE/$TASK_NAME
EOF
