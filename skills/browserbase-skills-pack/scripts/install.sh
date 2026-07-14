#!/usr/bin/env bash
# browserbase-skills-pack/scripts/install.sh
# Cherry-pick install of github.com/browserbase/skills into ~/.claude/skills/
# with `browserbase-` prefix on each skill (avoids name collisions with
# browser-harness and existing browser-related skills).
#
# Idempotent — safe to re-run. On replacement, writes a diff snapshot under
# $HOME/.codex/skill-sync-diffs/<timestamp>/ first (matching sync-skills
# convention).
#
# Exit codes:
#   0  installed (or already current)
#   1  git unavailable
#   2  clone/pull failed AND cache is empty
#   3  cherry-pick failed for one or more skills

set -uo pipefail

PACK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="$PACK_DIR/manifest.txt"
CACHE_DIR="${BROWSERBASE_SKILLS_CACHE:-$HOME/.cache/browserbase-skills}"
SKILLS_DIR="${SKILLS_DIR:-$HOME/.claude/skills}"
DIFF_ROOT="${SKILL_SYNC_DIFFS:-$HOME/.codex/skill-sync-diffs}"
UPSTREAM_URL="${BROWSERBASE_SKILLS_URL:-https://github.com/browserbase/skills.git}"
UPSTREAM_BRANCH="${BROWSERBASE_SKILLS_BRANCH:-main}"

if ! command -v git >/dev/null 2>&1; then
  echo "[browserbase-skills-pack] ERROR: git is not installed."
  echo "  macOS: xcode-select --install"
  echo "  Linux: sudo apt install git"
  exit 1
fi

mkdir -p "$SKILLS_DIR"

# 1. Clone or update the cache
if [ -d "$CACHE_DIR/.git" ]; then
  echo "[browserbase-skills-pack] Updating cache at $CACHE_DIR"
  if ! git -C "$CACHE_DIR" fetch --depth 1 origin "$UPSTREAM_BRANCH" 2>/tmp/bb-pack-fetch.log; then
    echo "[browserbase-skills-pack] WARN: fetch failed — using whatever's in the cache."
    cat /tmp/bb-pack-fetch.log 2>/dev/null || true
  else
    git -C "$CACHE_DIR" reset --hard "origin/$UPSTREAM_BRANCH" >/dev/null 2>&1 || true
  fi
else
  echo "[browserbase-skills-pack] Cloning $UPSTREAM_URL to $CACHE_DIR"
  if ! git clone --depth 1 --branch "$UPSTREAM_BRANCH" "$UPSTREAM_URL" "$CACHE_DIR" 2>/tmp/bb-pack-clone.log; then
    echo "[browserbase-skills-pack] ERROR: clone failed."
    cat /tmp/bb-pack-clone.log 2>/dev/null || true
    [ -d "$CACHE_DIR/skills" ] || exit 2
    echo "[browserbase-skills-pack] WARN: continuing with stale cache."
  fi
fi

if [ ! -d "$CACHE_DIR/skills" ]; then
  echo "[browserbase-skills-pack] ERROR: $CACHE_DIR/skills missing — upstream layout changed?"
  exit 2
fi

# 2. Read manifest (strip comments and blanks)
SKILLS=()
while IFS= read -r line; do
  trimmed="${line%%#*}"
  trimmed="$(echo "$trimmed" | xargs)"
  [ -n "$trimmed" ] && SKILLS+=("$trimmed")
done < "$MANIFEST"

if [ "${#SKILLS[@]}" -eq 0 ]; then
  echo "[browserbase-skills-pack] ERROR: manifest is empty."
  exit 3
fi

# 3. For each manifested skill, copy from cache to ~/.claude/skills/<prefixed>
TS="$(date +%Y%m%dT%H%M%S)"
DIFF_DIR="$DIFF_ROOT/$TS-browserbase-skills-pack"
FAIL_COUNT=0

STAGE_ROOT="$(mktemp -d -t browserbase-skills-pack-XXXXXX)"
trap 'rm -rf "$STAGE_ROOT"' EXIT

normalize_skill_tree() {
  local stage_dir="$1"
  local new_name="$2"
  local stage_md="$stage_dir/SKILL.md"

  if [ ! -f "$stage_md" ]; then
    return 1
  fi

  awk -v new_name="$new_name" '
    BEGIN { in_fm = 0; fm_seen = 0 }
    /^---[[:space:]]*$/ {
      if (!fm_seen) { in_fm = 1; fm_seen = 1; print; next }
      else if (in_fm) { in_fm = 0; print; next }
    }
    in_fm && /^name:[[:space:]]/ { print "name: " new_name; next }
    { print }
  ' "$stage_md" > "$stage_md.tmp" && mv "$stage_md.tmp" "$stage_md"
}

for prefixed in "${SKILLS[@]}"; do
  upstream="${prefixed#browserbase-}"
  src="$CACHE_DIR/skills/$upstream"
  dst="$SKILLS_DIR/$prefixed"
  normalized_stage="$STAGE_ROOT/$prefixed"

  if [ ! -d "$src" ]; then
    echo "[browserbase-skills-pack] WARN: upstream skill '$upstream' not found at $src — skipping."
    FAIL_COUNT=$((FAIL_COUNT + 1))
    continue
  fi

  # Render upstream into a staging dir, then normalize the frontmatter
  # name before comparing it to the installed copy. That keeps the replace
  # decision keyed to real content drift, not the prefixed name rewrite.
  cp -R "$src" "$normalized_stage"
  if ! normalize_skill_tree "$normalized_stage" "$prefixed"; then
    echo "[browserbase-skills-pack] WARN: $upstream/SKILL.md missing in upstream — skipping."
    FAIL_COUNT=$((FAIL_COUNT + 1))
    continue
  fi

  # Compare the normalized staging tree to the installed dst.
  # If they're identical, no-op — no snapshot, no replace, no churn.
  if [ -d "$dst" ] && diff -rq "$normalized_stage" "$dst" >/dev/null 2>&1; then
    echo "[browserbase-skills-pack] Unchanged: $prefixed"
    continue
  fi

  # Snapshot only when there's real drift to capture.
  if [ -d "$dst" ]; then
    mkdir -p "$DIFF_DIR/$prefixed"
    cp -R "$dst" "$DIFF_DIR/$prefixed/old" 2>/dev/null || true
    echo "[browserbase-skills-pack] Snapshot of existing $prefixed -> $DIFF_DIR/$prefixed/old"
  fi

  install_stage="$SKILLS_DIR/.${prefixed}.tmp.$TS.$$"
  install_backup="$SKILLS_DIR/.${prefixed}.bak.$TS.$$"

  rm -rf "$install_stage" "$install_backup"
  if ! cp -R "$normalized_stage" "$install_stage"; then
    echo "[browserbase-skills-pack] ERROR: failed to stage $prefixed into $install_stage"
    FAIL_COUNT=$((FAIL_COUNT + 1))
    rm -rf "$install_stage" "$install_backup"
    continue
  fi

  if [ -d "$dst" ]; then
    if ! mv "$dst" "$install_backup"; then
      echo "[browserbase-skills-pack] ERROR: failed to move existing $prefixed aside"
      FAIL_COUNT=$((FAIL_COUNT + 1))
      rm -rf "$install_stage" "$install_backup"
      continue
    fi
  fi

  if ! mv "$install_stage" "$dst"; then
    echo "[browserbase-skills-pack] ERROR: failed to install $prefixed into $dst"
    if [ -d "$install_backup" ]; then
      mv "$install_backup" "$dst" 2>/dev/null || true
    fi
    FAIL_COUNT=$((FAIL_COUNT + 1))
    rm -rf "$install_stage" "$install_backup"
    continue
  fi

  rm -rf "$install_backup"
  echo "[browserbase-skills-pack] Installed: $prefixed"
done

if [ "$FAIL_COUNT" -gt 0 ]; then
  echo "[browserbase-skills-pack] $FAIL_COUNT skill(s) failed to install — see warnings above."
  exit 3
fi

echo "[browserbase-skills-pack] Install OK. ${#SKILLS[@]} skill(s) installed under $SKILLS_DIR/."

# Best-effort verify
if [ -x "$PACK_DIR/scripts/verify.sh" ]; then
  bash "$PACK_DIR/scripts/verify.sh" || true
fi
