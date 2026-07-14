#!/usr/bin/env bash
# marketing-skills-pack/scripts/verify.sh
# Verify that the Corey Haines Marketing Skills marketplace pack is installed
# and marquee skills (/image, /video, and /social or legacy /social-content)
# are resolvable under the user-global skills directory.
#
# Exit codes:
#   0  verified — pack present, marquee skills resolvable
#   1  not installed
#   2  partially installed (CLI says present but marquee skills missing)

set -uo pipefail

PACKAGE="coreyhaines31/marketingskills"
SKILLS_DIR="${SKILLS_DIR:-$HOME/.claude/skills}"

if ! command -v npx >/dev/null 2>&1; then
  echo "[marketing-skills-pack] verify: npx unavailable — cannot query CLI."
  exit 1
fi

echo "[marketing-skills-pack] Listing global skills..."
LIST_OUT="$(npx -y skills@latest list -g 2>/dev/null || true)"

if echo "$LIST_OUT" | grep -qi "marketingskills\|coreyhaines"; then
  echo "[marketing-skills-pack] CLI reports pack installed."
else
  echo "[marketing-skills-pack] CLI does NOT report pack installed."
  echo "  Run: bash $HOME/.claude/skills/marketing-skills-pack/scripts/install.sh"
  exit 1
fi

# Check marquee skills resolve on disk. The CLI may install at any of these
# locations depending on platform / config; we check the common one first.
MARQUEE=(image video)
MISSING=()
for s in "${MARQUEE[@]}"; do
  if [ ! -e "$SKILLS_DIR/$s" ] && [ ! -e "$SKILLS_DIR/$s/SKILL.md" ]; then
    MISSING+=("$s")
  fi
done

SOCIAL_VARIANTS=(social social-content)
SOCIAL_FOUND=""
for s in "${SOCIAL_VARIANTS[@]}"; do
  if [ -e "$SKILLS_DIR/$s" ] || [ -e "$SKILLS_DIR/$s/SKILL.md" ]; then
    SOCIAL_FOUND="$s"
    break
  fi
done

if [ -z "$SOCIAL_FOUND" ]; then
  MISSING+=("social|social-content")
fi

if [ "${#MISSING[@]}" -eq 0 ]; then
  echo "[marketing-skills-pack] Marquee skills present: ${MARQUEE[*]} $SOCIAL_FOUND"
  echo "[marketing-skills-pack] Verify OK."
  exit 0
else
  echo "[marketing-skills-pack] WARN: marquee skills missing under $SKILLS_DIR: ${MISSING[*]}"
  echo "  The CLI may have installed them under a different agent dir."
  echo "  Inspect: npx skills list -g"
  exit 2
fi
