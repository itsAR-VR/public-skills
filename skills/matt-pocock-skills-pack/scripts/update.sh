#!/usr/bin/env bash
# matt-pocock-skills-pack/scripts/update.sh
# Refresh the Matt Pocock Skills marketplace pack to the latest version.
# Called by sync-skills Step 1.5. Non-fatal on offline / registry errors.

set -uo pipefail

PACKAGE="mattpocock/skills"

if ! command -v npx >/dev/null 2>&1; then
  echo "[matt-pocock-skills-pack] WARN: npx not available — skipping refresh."
  exit 1
fi

if ! curl -fsS -m 3 -o /dev/null https://registry.npmjs.org/skills 2>/dev/null; then
  echo "[matt-pocock-skills-pack] INFO: npm registry unreachable — skipping refresh."
  exit 0
fi

echo "[matt-pocock-skills-pack] Refreshing $PACKAGE..."

if npx -y skills@latest update "$PACKAGE" -g -y 2>/tmp/matt-pocock-update.log; then
  echo "[matt-pocock-skills-pack] Update OK."
else
  echo "[matt-pocock-skills-pack] update failed; falling back to add (with --copy)..."
  if npx -y skills@latest add "$PACKAGE" -g -y --copy; then
    echo "[matt-pocock-skills-pack] Refresh via add OK."
  else
    echo "[matt-pocock-skills-pack] WARN: refresh failed — pack remains at last installed version."
    cat /tmp/matt-pocock-update.log 2>/dev/null || true
    exit 0
  fi
fi
