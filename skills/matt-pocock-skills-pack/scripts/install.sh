#!/usr/bin/env bash
# matt-pocock-skills-pack/scripts/install.sh
# Install the Matt Pocock Skills marketplace pack at user-global scope.

set -euo pipefail

PACKAGE="mattpocock/skills"

if ! command -v npx >/dev/null 2>&1; then
  echo "ERROR: npx is not available. Install Node.js 20+ first."
  exit 1
fi

echo "[matt-pocock-skills-pack] Installing $PACKAGE at user-global scope..."

if npx -y skills@latest add "$PACKAGE" -g -y --copy; then
  echo "[matt-pocock-skills-pack] Install OK."
else
  echo "[matt-pocock-skills-pack] ERROR: install failed (exit $?)."
  echo "  Re-run manually:"
  echo "    npx -y skills@latest add $PACKAGE -g -y --copy"
  exit 2
fi
