#!/usr/bin/env bash
# marketing-skills-pack/scripts/install.sh
# Install the Corey Haines Marketing Skills marketplace pack at user-global scope.
#
# Idempotent: safe to re-run. If the pack is already installed, `npx skills add`
# refreshes it to the latest version on the upstream repo.
#
# Exit codes:
#   0  installed (or already present and refreshed)
#   1  npx not available
#   2  install failed (network, registry, etc.)

set -euo pipefail

PACKAGE="coreyhaines31/marketingskills"

if ! command -v npx >/dev/null 2>&1; then
  echo "ERROR: npx is not available. Install Node.js 20+ first."
  echo "  macOS: brew install node"
  echo "  Linux: sudo apt install nodejs npm   (or use nvm / fnm)"
  exit 1
fi

echo "[marketing-skills-pack] Installing $PACKAGE at user-global scope..."

if npx -y skills@latest add "$PACKAGE" -g -y --copy; then
  echo "[marketing-skills-pack] Install OK."
else
  echo "[marketing-skills-pack] ERROR: install failed (exit $?)."
  echo "  Re-run manually for full output:"
  echo "    npx -y skills@latest add $PACKAGE -g -y --copy"
  exit 2
fi

# Best-effort verify
if command -v "$HOME/.claude/skills/marketing-skills-pack/scripts/verify.sh" >/dev/null 2>&1; then
  bash "$HOME/.claude/skills/marketing-skills-pack/scripts/verify.sh" || true
fi
