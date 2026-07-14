#!/usr/bin/env bash
# ponytail-skills-pack/scripts/install.sh
# Install Dietrich Gebert's Ponytail skill pack at user-global scope.

set -euo pipefail

PACKAGE="DietrichGebert/ponytail"

if ! command -v npx >/dev/null 2>&1; then
  echo "ERROR: npx is not available. Install Node.js 20+ first."
  exit 1
fi

echo "[ponytail-skills-pack] Installing $PACKAGE at user-global scope..."

if npx -y skills@latest add "$PACKAGE" -g -y --copy --full-depth --skill '*'; then
  echo "[ponytail-skills-pack] Install OK."
else
  echo "[ponytail-skills-pack] ERROR: install failed (exit $?)."
  echo "  Re-run manually:"
  echo "    npx -y skills@latest add $PACKAGE -g -y --copy --full-depth --skill '*'"
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "$SCRIPT_DIR/verify.sh" || true
