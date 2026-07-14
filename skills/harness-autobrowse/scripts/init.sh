#!/usr/bin/env bash
# harness-autobrowse/scripts/init.sh
# Bootstrap a new harness-autobrowse task workspace.
#
# Usage:
#   bash init.sh <task-name> <url> "<one-sentence-goal>"
#
# Creates:
#   ./harness-autobrowse/tasks/<task-name>/task.md       (read-only spec)
#   ./harness-autobrowse/tasks/<task-name>/strategy.md   (mutable working file)
#   ./harness-autobrowse/runs/<task-name>/                (empty — populated by start-run.sh)
#
# Idempotent: if task.md exists, refuses to overwrite (use a different name
# or `rm -rf ./harness-autobrowse/tasks/<task-name>` to start over).
#
# Exit codes:
#   0  task initialized
#   1  bad arguments
#   2  task already exists
#   3  template missing

set -uo pipefail

if [ $# -lt 3 ]; then
  cat <<EOF
Usage: bash init.sh <task-name> <url> "<one-sentence-goal>"

Example:
  bash init.sh github-star-repo \\
       https://github.com/browser-use/browser-harness \\
       "Click the Star button and verify the count increments by 1"
EOF
  exit 1
fi

TASK_NAME="$1"
URL="$2"
GOAL="$3"

# Validate task name (kebab-case, alphanumeric and hyphens only)
if ! echo "$TASK_NAME" | grep -qE '^[a-z0-9][a-z0-9-]*$'; then
  echo "[harness-autobrowse] ERROR: task name must be lowercase kebab-case (a-z, 0-9, hyphens). Got: '$TASK_NAME'"
  exit 1
fi

# Resolve the skill root (this script lives in scripts/)
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TASK_TEMPLATE="$SKILL_DIR/references/example-task.md"
STRATEGY_TEMPLATE="$SKILL_DIR/references/example-strategy.md"

if [ ! -f "$TASK_TEMPLATE" ] || [ ! -f "$STRATEGY_TEMPLATE" ]; then
  echo "[harness-autobrowse] ERROR: templates missing under $SKILL_DIR/references/"
  exit 3
fi

WORKSPACE="${HARNESS_AUTOBROWSE_WORKSPACE:-$PWD/harness-autobrowse}"
TASK_DIR="$WORKSPACE/tasks/$TASK_NAME"
RUNS_DIR="$WORKSPACE/runs/$TASK_NAME"

if [ -e "$TASK_DIR/task.md" ]; then
  echo "[harness-autobrowse] ERROR: $TASK_DIR/task.md already exists."
  echo "  Use a different name, or remove the existing task: rm -rf $TASK_DIR $RUNS_DIR"
  exit 2
fi

mkdir -p "$TASK_DIR" "$RUNS_DIR"

# Extract host for SITE_HOST placeholder
SITE_HOST="$(printf '%s' "$URL" | sed -E 's|^https?://([^/]+).*|\1|; s|^www\.||')"
ISO_DATE="$(date -u +%Y-%m-%d)"

# Escape user-supplied values for sed replacement strings.
# sed replacement metachars are `\`, `&`, and the delimiter (we use `|`).
# Without escaping, URLs containing `&` (like `?a=1&b=2`) get corrupted
# because `&` in a sed replacement means "the entire match".
sed_escape() {
  local value="$1"
  value="${value//\\/\\\\}"
  value="${value//&/\\&}"
  value="${value//|/\\|}"
  printf '%s' "$value"
}

ESC_TASK_NAME="$(sed_escape "$TASK_NAME")"
ESC_URL="$(sed_escape "$URL")"
ESC_SITE_HOST="$(sed_escape "$SITE_HOST")"
ESC_ISO_DATE="$(sed_escape "$ISO_DATE")"
ESC_GOAL="$(sed_escape "$GOAL")"

# Render task.md from template
sed \
  -e "s|<TASK_TITLE>|$ESC_TASK_NAME|g" \
  -e "s|<TASK_URL>|$ESC_URL|g" \
  -e "s|<SITE_HOST>|$ESC_SITE_HOST|g" \
  -e "s|<ISO_DATE>|$ESC_ISO_DATE|g" \
  -e "s|<ONE_SENTENCE_GOAL>|$ESC_GOAL|g" \
  "$TASK_TEMPLATE" > "$TASK_DIR/task.md"

# Render strategy.md from template
sed \
  -e "s|<TASK_TITLE>|$ESC_TASK_NAME|g" \
  -e "s|<TASK_URL>|$ESC_URL|g" \
  -e "s|<ISO_DATE>|$ESC_ISO_DATE|g" \
  "$STRATEGY_TEMPLATE" > "$TASK_DIR/strategy.md"

# Initialize empty history.jsonl
: > "$RUNS_DIR/history.jsonl"

cat <<EOF
[harness-autobrowse] Task initialized.

  Task dir:     $TASK_DIR
  Runs dir:     $RUNS_DIR
  Spec:         $TASK_DIR/task.md   (read-only — edit only to add expected output schema)
  Strategy:     $TASK_DIR/strategy.md   (mutable — outer agent edits this between iterations)

Next steps:
  1. Open $TASK_DIR/task.md and fill in the expected output schema and any constraints.
  2. Run an iteration:
       RUN_DIR=\$(bash $SKILL_DIR/scripts/start-run.sh $TASK_NAME)
  3. Run browser-harness against the goal, capturing screenshots into \$RUN_DIR/screenshots/.
  4. Write \$RUN_DIR/summary.md with what happened.
  5. Mark the result:
       bash $SKILL_DIR/scripts/finish-run.sh $TASK_NAME pass|fail|partial "<one-line hypothesis>"
EOF
