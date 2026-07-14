#!/usr/bin/env bash
# caveman-skills-pack update — same flow as install.sh, called automatically
# by sync-skills Step 1.5. Non-fatal on network failure (uses cached copy).
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash "$SCRIPT_DIR/install.sh"
