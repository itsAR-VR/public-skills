#!/usr/bin/env bash
# caveman-skills-pack verify — confirm all 5 caveman skills exist with valid
# frontmatter (name + description). Exits non-zero on any missing skill.
set -euo pipefail

DEST_DIR="${CAVEMAN_DEST_DIR:-$HOME/.claude/skills}"
EXPECTED=(caveman caveman-commit caveman-help caveman-review caveman-compress)

MISSING=0
for s in "${EXPECTED[@]}"; do
  if [ ! -f "$DEST_DIR/$s/SKILL.md" ]; then
    echo "[caveman-skills-pack] MISSING: $s"
    MISSING=$((MISSING + 1))
    continue
  fi
  if ! grep -q "^name: $s\$" "$DEST_DIR/$s/SKILL.md"; then
    echo "[caveman-skills-pack] FRONTMATTER MISMATCH: $s/SKILL.md does not declare name: $s"
    MISSING=$((MISSING + 1))
    continue
  fi
  if ! grep -q "^description:" "$DEST_DIR/$s/SKILL.md"; then
    echo "[caveman-skills-pack] FRONTMATTER MISSING: $s/SKILL.md has no description:"
    MISSING=$((MISSING + 1))
    continue
  fi
  echo "[caveman-skills-pack] OK: $s"
done

if [ "$MISSING" -gt 0 ]; then
  echo "[caveman-skills-pack] FAIL: $MISSING issue(s). Run scripts/install.sh to repair."
  exit 1
fi
echo "[caveman-skills-pack] All 5 skills present and valid."
