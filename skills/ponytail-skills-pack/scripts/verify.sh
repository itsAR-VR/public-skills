#!/usr/bin/env bash
# ponytail-skills-pack/scripts/verify.sh
# Verify the Ponytail pack skills resolve under the local skills directory.

set -uo pipefail

SKILLS_DIR="${SKILLS_DIR:-$HOME/.claude/skills}"
REQUIRED=(ponytail ponytail-audit ponytail-debt ponytail-help ponytail-review)
MISSING=()

for skill in "${REQUIRED[@]}"; do
  if [ ! -f "$SKILLS_DIR/$skill/SKILL.md" ]; then
    MISSING+=("$skill")
  fi
done

if [ "${#MISSING[@]}" -eq 0 ]; then
  echo "[ponytail-skills-pack] Skills present under $SKILLS_DIR: ${REQUIRED[*]}"
  echo "[ponytail-skills-pack] Verify OK."
  exit 0
fi

echo "[ponytail-skills-pack] WARN: missing under $SKILLS_DIR: ${MISSING[*]}"
echo "  Run: bash $HOME/.claude/skills/ponytail-skills-pack/scripts/install.sh"
exit 2
