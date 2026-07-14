#!/usr/bin/env bash
# higgsfield-skills-pack/scripts/update.sh
# Refresh the Higgsfield AI Skills marketplace pack to the latest version.
#
# Called by sync-skills on every sync so the pack stays current.
#
# Exit codes:
#   0  updated (or already current, or no internet — non-fatal)
#   1  npx not available (caller should treat as soft failure)

set -uo pipefail

PACKAGE="higgsfield-ai/skills"

if ! command -v npx >/dev/null 2>&1; then
  echo "[higgsfield-skills-pack] WARN: npx not available — skipping marketplace refresh."
  exit 1
fi

# Probe network with a 3-second budget. If the registry is unreachable, skip
# silently — sync-skills should not fail just because we're offline.
if ! curl -fsS -m 3 -o /dev/null https://registry.npmjs.org/skills 2>/dev/null; then
  echo "[higgsfield-skills-pack] INFO: npm registry unreachable — skipping refresh."
  exit 0
fi

echo "[higgsfield-skills-pack] Refreshing $PACKAGE..."

# Try update first (faster path when already installed). Fall back to add (which
# is install-or-refresh) if update reports the package is missing or the CLI
# version doesn't support `update` for this package shape.
if npx -y skills@latest update "$PACKAGE" -g -y 2>/tmp/higgsfield-skills-update.log; then
  echo "[higgsfield-skills-pack] Update OK."
else
  echo "[higgsfield-skills-pack] update failed; falling back to add (with --copy)..."
  if npx -y skills@latest add "$PACKAGE" -g -y --copy; then
    echo "[higgsfield-skills-pack] Refresh via add OK."
  else
    echo "[higgsfield-skills-pack] WARN: refresh failed — pack remains at last installed version."
    cat /tmp/higgsfield-skills-update.log 2>/dev/null || true
    exit 0   # non-fatal for sync-skills
  fi
fi
