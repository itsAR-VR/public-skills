#!/usr/bin/env bash
# higgsfield-skills-pack/scripts/install.sh
# Install the Higgsfield AI Skills marketplace pack at user-global scope.
#
# Idempotent: safe to re-run. If the pack is already installed, `npx skills add`
# refreshes it to the latest version on the upstream repo.
#
# Exit codes:
#   0  installed (or already present and refreshed)
#   1  npx not available
#   2  install failed (network, registry, etc.)

set -euo pipefail

PACKAGE="higgsfield-ai/skills"

if ! command -v npx >/dev/null 2>&1; then
  echo "ERROR: npx is not available. Install Node.js 20+ first."
  echo "  macOS: brew install node"
  echo "  Linux: sudo apt install nodejs npm   (or use nvm / fnm)"
  exit 1
fi

echo "[higgsfield-skills-pack] Installing $PACKAGE at user-global scope..."

if npx -y skills@latest add "$PACKAGE" -g -y --copy; then
  echo "[higgsfield-skills-pack] Install OK."
else
  echo "[higgsfield-skills-pack] ERROR: install failed (exit $?)."
  echo "  Re-run manually for full output:"
  echo "    npx -y skills@latest add $PACKAGE -g -y --copy"
  exit 2
fi

# Best-effort verify
VERIFY="$HOME/.claude/skills/higgsfield-skills-pack/scripts/verify.sh"
if [ -x "$VERIFY" ]; then
  bash "$VERIFY" || true
fi
