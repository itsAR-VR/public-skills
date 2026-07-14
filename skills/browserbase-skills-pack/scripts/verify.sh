#!/usr/bin/env bash
# browserbase-skills-pack/scripts/verify.sh
# Verify each manifested skill landed under ~/.claude/skills/ AND the
# frontmatter `name:` matches the directory name (prefix-rewrite drift is
# the most likely silent failure mode).
#
# Exit codes:
#   0  all skills verified
#   1  one or more missing
#   2  one or more present but with mismatched frontmatter name

set -uo pipefail

PACK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="$PACK_DIR/manifest.txt"
SKILLS_DIR="${SKILLS_DIR:-$HOME/.claude/skills}"

# Read manifest (strip comments and blanks)
SKILLS=()
while IFS= read -r line; do
  trimmed="${line%%#*}"
  trimmed="$(echo "$trimmed" | xargs)"
  [ -n "$trimmed" ] && SKILLS+=("$trimmed")
done < "$MANIFEST"

MISSING=()
MISMATCHED=()
OK=()

for prefixed in "${SKILLS[@]}"; do
  skill_md="$SKILLS_DIR/$prefixed/SKILL.md"
  if [ ! -f "$skill_md" ]; then
    MISSING+=("$prefixed")
    continue
  fi
  # Extract `name:` from the first frontmatter block
  fm_name="$(awk '
    BEGIN { in_fm = 0; fm_seen = 0 }
    /^---[[:space:]]*$/ {
      if (!fm_seen) { in_fm = 1; fm_seen = 1; next }
      else if (in_fm) { exit }
    }
    in_fm && /^name:[[:space:]]/ {
      sub(/^name:[[:space:]]+/, "")
      print
      exit
    }
  ' "$skill_md")"
  fm_name="$(echo "$fm_name" | xargs)"
  if [ "$fm_name" != "$prefixed" ]; then
    MISMATCHED+=("$prefixed (frontmatter says: '$fm_name')")
  else
    OK+=("$prefixed")
  fi
done

if [ "${#OK[@]}" -gt 0 ]; then
  echo "[browserbase-skills-pack] OK: ${OK[*]}"
fi
if [ "${#MISSING[@]}" -gt 0 ]; then
  echo "[browserbase-skills-pack] MISSING: ${MISSING[*]}"
  echo "  Run: bash $PACK_DIR/scripts/install.sh"
fi
if [ "${#MISMATCHED[@]}" -gt 0 ]; then
  echo "[browserbase-skills-pack] FRONTMATTER MISMATCH:"
  for m in "${MISMATCHED[@]}"; do
    echo "    $m"
  done
  echo "  Re-run install.sh — the prefix-rewrite is idempotent."
fi

[ "${#MISSING[@]}" -eq 0 ] && [ "${#MISMATCHED[@]}" -eq 0 ] && exit 0
[ "${#MISMATCHED[@]}" -gt 0 ] && exit 2
exit 1
