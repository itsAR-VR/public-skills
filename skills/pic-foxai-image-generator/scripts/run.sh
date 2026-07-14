#!/bin/bash
# FoxAI Image Generator Skill Runner
#
# Resolves the FoxAI generator location from $FOXAI_WORKSPACE with a sensible
# per-user default. Previously hardcoded /root/.openclaw/workspace, which only
# worked on a single install layout.

set -eu

WORKSPACE="${FOXAI_WORKSPACE:-${HOME}/.openclaw/workspace}"
GENERATOR="${WORKSPACE}/foxai_generator.cjs"

if [ ! -f "$GENERATOR" ]; then
    echo "error: foxai_generator.cjs not found at $GENERATOR" >&2
    echo "set FOXAI_WORKSPACE to the directory containing foxai_generator.cjs" >&2
    exit 1
fi

cd "$WORKSPACE"
exec node "$GENERATOR" "$@" --count 1
