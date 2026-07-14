#!/usr/bin/env bash
# higgsfield-skills-pack/scripts/verify.sh
# Verify that the Higgsfield AI Skills marketplace pack is installed
# and all four bundled skills (higgsfield-generate, higgsfield-soul-id,
# higgsfield-product-photoshoot, higgsfield-marketplace-cards) are
# resolvable under the user-global skills directory.
#
# Exit codes:
#   0  verified — pack present, all marquee skills resolvable
#   1  not installed
#   2  partially installed (CLI says present but marquee skills missing)

set -uo pipefail

PACKAGE="higgsfield-ai/skills"
SKILLS_DIR="${SKILLS_DIR:-$HOME/.claude/skills}"

if ! command -v npx >/dev/null 2>&1; then
  echo "[higgsfield-skills-pack] verify: npx unavailable — cannot query CLI."
  exit 1
fi

echo "[higgsfield-skills-pack] Listing global skills..."
LIST_OUT="$(npx -y skills@latest list -g 2>/dev/null || true)"

if echo "$LIST_OUT" | grep -qiE "higgsfield-ai/skills|higgsfield-generate|higgsfield-soul-id"; then
  echo "[higgsfield-skills-pack] CLI reports pack installed."
else
  echo "[higgsfield-skills-pack] CLI does NOT report pack installed."
  echo "  Run: bash $HOME/.claude/skills/higgsfield-skills-pack/scripts/install.sh"
  exit 1
fi

# Check that all four bundled skills resolve on disk.
MARQUEE=(higgsfield-generate higgsfield-soul-id higgsfield-product-photoshoot higgsfield-marketplace-cards)
MISSING=()
for s in "${MARQUEE[@]}"; do
  if [ ! -e "$SKILLS_DIR/$s/SKILL.md" ]; then
    MISSING+=("$s")
  fi
done

if [ "${#MISSING[@]}" -eq 0 ]; then
  echo "[higgsfield-skills-pack] All marquee skills present: ${MARQUEE[*]}"
  echo "[higgsfield-skills-pack] Verify OK."
  exit 0
else
  echo "[higgsfield-skills-pack] WARN: marquee skills missing under $SKILLS_DIR: ${MISSING[*]}"
  echo "  The CLI may have installed them under a different agent dir."
  echo "  Inspect: npx skills list -g"
  exit 2
fi
