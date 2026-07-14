#!/usr/bin/env bash
# ponytail-skills-pack/scripts/update.sh
# Refresh Dietrich Gebert's Ponytail skill pack to the latest version.
# Called by sync-skills Step 1.5. Non-fatal on offline / registry errors.

set -uo pipefail

PACKAGE="DietrichGebert/ponytail"

if ! command -v npx >/dev/null 2>&1; then
  echo "[ponytail-skills-pack] WARN: npx not available - skipping refresh."
  exit 1
fi

if ! curl -fsS -m 3 -o /dev/null https://registry.npmjs.org/skills 2>/dev/null; then
  echo "[ponytail-skills-pack] INFO: npm registry unreachable - skipping refresh."
  exit 0
fi

echo "[ponytail-skills-pack] Refreshing $PACKAGE..."

if npx -y skills@latest update "$PACKAGE" -g -y 2>/tmp/ponytail-skills-update.log; then
  echo "[ponytail-skills-pack] Update OK."
else
  echo "[ponytail-skills-pack] update failed; falling back to add (with --copy)..."
  if npx -y skills@latest add "$PACKAGE" -g -y --copy --full-depth --skill '*'; then
    echo "[ponytail-skills-pack] Refresh via add OK."
  else
    echo "[ponytail-skills-pack] WARN: refresh failed - pack remains at last installed version."
    cat /tmp/ponytail-skills-update.log 2>/dev/null || true
    exit 0
  fi
fi
