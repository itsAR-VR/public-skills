#!/usr/bin/env bash
# matt-pocock-skills-pack/scripts/verify.sh
# Verify the Matt Pocock Skills pack is installed and marquee skills resolve.

set -uo pipefail

PACKAGE="mattpocock/skills"
SKILLS_DIR="${SKILLS_DIR:-$HOME/.claude/skills}"

if ! command -v npx >/dev/null 2>&1; then
  echo "[matt-pocock-skills-pack] verify: npx unavailable."
  exit 1
fi

LIST_OUT="$(npx -y skills@latest list -g 2>/dev/null || true)"
if echo "$LIST_OUT" | grep -qi "mattpocock"; then
  echo "[matt-pocock-skills-pack] CLI reports pack installed."
else
  echo "[matt-pocock-skills-pack] CLI does NOT report pack installed."
  echo "  Run: bash $HOME/.claude/skills/matt-pocock-skills-pack/scripts/install.sh"
  exit 1
fi

MARQUEE=(tdd grill-with-docs write-a-skill triage diagnose)
MISSING=()
for s in "${MARQUEE[@]}"; do
  [ -d "$SKILLS_DIR/$s" ] || MISSING+=("$s")
done

if [ "${#MISSING[@]}" -eq 0 ]; then
  echo "[matt-pocock-skills-pack] Marquee skills present: ${MARQUEE[*]}"
  echo "[matt-pocock-skills-pack] Verify OK."
  exit 0
else
  echo "[matt-pocock-skills-pack] WARN: marquee skills missing under $SKILLS_DIR: ${MISSING[*]}"
  exit 2
fi
