#!/usr/bin/env bash
# caveman-skills-pack install — clone or update upstream caveman repo, copy
# the 5 skills into ~/.claude/skills/. Idempotent. Renames upstream `compress`
# directory to `caveman-compress` for namespace clarity.
#
# Source: https://github.com/JuliusBrussee/caveman
set -euo pipefail

REPO_URL="https://github.com/JuliusBrussee/caveman.git"
CACHE_DIR="${CAVEMAN_CACHE_DIR:-$HOME/.cache/caveman-skills-pack}"
DEST_DIR="${CAVEMAN_DEST_DIR:-$HOME/.claude/skills}"

mkdir -p "$CACHE_DIR" "$DEST_DIR"

# Clone or pull
if [ -d "$CACHE_DIR/.git" ]; then
  echo "[caveman-skills-pack] Updating cache at $CACHE_DIR"
  git -C "$CACHE_DIR" fetch --depth 1 origin main >/dev/null 2>&1 || {
    echo "[caveman-skills-pack] git fetch failed (offline?). Using cached copy."
  }
  git -C "$CACHE_DIR" reset --hard origin/main >/dev/null 2>&1 || true
else
  echo "[caveman-skills-pack] Cloning $REPO_URL → $CACHE_DIR"
  git clone --depth 1 "$REPO_URL" "$CACHE_DIR" >/dev/null 2>&1 || {
    echo "[caveman-skills-pack] ERROR: clone failed"; exit 1;
  }
fi

# Copy mapping: upstream-name → repo-name
declare -a PAIRS=(
  "caveman:caveman"
  "caveman-commit:caveman-commit"
  "caveman-help:caveman-help"
  "caveman-review:caveman-review"
  "compress:caveman-compress"
)

for pair in "${PAIRS[@]}"; do
  src="${pair%%:*}"
  dst="${pair##*:}"
  if [ ! -d "$CACHE_DIR/skills/$src" ]; then
    echo "[caveman-skills-pack] WARN: upstream skill '$src' not found, skipping"
    continue
  fi
  rm -rf "$DEST_DIR/$dst"
  cp -R "$CACHE_DIR/skills/$src" "$DEST_DIR/$dst"
  # Patch frontmatter name when directory was renamed
  if [ "$src" != "$dst" ]; then
    # macOS sed needs the empty -i argument
    if [[ "$OSTYPE" == "darwin"* ]]; then
      sed -i '' "s/^name: $src\$/name: $dst/" "$DEST_DIR/$dst/SKILL.md"
    else
      sed -i "s/^name: $src\$/name: $dst/" "$DEST_DIR/$dst/SKILL.md"
    fi
  fi
  echo "[caveman-skills-pack] installed $dst"
done

# Record the upstream commit for traceability
COMMIT=$(git -C "$CACHE_DIR" rev-parse --short HEAD 2>/dev/null || echo "unknown")
echo "[caveman-skills-pack] Install OK. Upstream HEAD: $COMMIT"
