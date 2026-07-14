#!/usr/bin/env bash
# browserbase-skills-pack/scripts/update.sh
# Refresh the cherry-picked BrowserBase skills. Calls install.sh (which is
# idempotent) under a network-availability guard so sync-skills doesn't fail
# when offline.
#
# Exit codes:
#   0  updated, already current, or offline (non-fatal)
#   1  git unavailable

set -uo pipefail

PACK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPSTREAM_HOST="${BROWSERBASE_SKILLS_HOST:-github.com}"

if ! command -v git >/dev/null 2>&1; then
  echo "[browserbase-skills-pack] WARN: git not available — skipping refresh."
  exit 1
fi

# 3-second probe — if upstream is unreachable, skip silently
if ! curl -fsS -m 3 -o /dev/null "https://$UPSTREAM_HOST" 2>/dev/null; then
  echo "[browserbase-skills-pack] INFO: $UPSTREAM_HOST unreachable — skipping refresh."
  exit 0
fi

echo "[browserbase-skills-pack] Refreshing browserbase-* skills..."
if bash "$PACK_DIR/scripts/install.sh"; then
  echo "[browserbase-skills-pack] Refresh OK."
else
  echo "[browserbase-skills-pack] WARN: refresh failed — last installed copy is still in place."
  exit 0   # non-fatal for sync-skills
fi
