#!/usr/bin/env bash
# install.sh — install MiniMax wrappers into ~/.local/bin as symlinks to the
# skill's bin/ directory. Idempotent; safe to re-run.
#
# Usage:
#   bash install.sh                   # link wrappers, prompt for key if missing (interactive only)
#   bash install.sh --no-prompt       # skip the key prompt (CI / non-interactive)
#   bash install.sh --force           # back up real files to *.pre-install-<ts> before linking
#   bash install.sh --dry-run         # show what would change
#
# Exit codes: 0 = fully configured, 10 = wrappers installed but key missing,
#             20 = wrappers installed but claude-mm can't reach MiniMax,
#             other = hard failure.

set -euo pipefail

# Resolve script and skill directories (handles symlinked invocation).
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}")"
SKILL_DIR="$(cd "$(dirname "$SCRIPT_PATH")/.." && pwd)"
BIN_SRC="$SKILL_DIR/bin"
BIN_DST="$HOME/.local/bin"
KEY_FILE="$HOME/.config/minimax/token-plan.key"

DRY_RUN=0
FORCE=0
PROMPT_FOR_KEY=1
STAMP="$(date +%Y%m%d-%H%M%S)"

for arg in "$@"; do
  case "$arg" in
    --dry-run|-n)   DRY_RUN=1 ;;
    --force|-f)     FORCE=1 ;;
    --no-prompt)    PROMPT_FOR_KEY=0 ;;
    -h|--help)
      sed -n '2,14p' "$SCRIPT_PATH"
      exit 0 ;;
  esac
done

# Non-interactive shells (no tty) auto-disable the prompt.
[[ ! -t 0 ]] && PROMPT_FOR_KEY=0

echo "minimax-setup: installing wrappers from $BIN_SRC -> $BIN_DST"

mkdir -p "$BIN_DST"

WRAPPERS=(claude-mm ct-mm claw-mm claude-mm-sync)

for name in "${WRAPPERS[@]}"; do
  src="$BIN_SRC/$name"
  dst="$BIN_DST/$name"
  [[ -x "$src" ]] || { echo "  [error] $src is not executable — skill is broken" >&2; exit 2; }

  if [[ -L "$dst" ]]; then
    current="$(readlink "$dst")"
    if [[ "$current" == "$src" ]]; then
      echo "  [ok]     $dst (already linked)"
      continue
    fi
    if (( DRY_RUN )); then
      echo "  [update] $dst -> $src (was $current)"
    else
      ln -sfn "$src" "$dst"
      echo "  [update] $dst -> $src"
    fi
  elif [[ -e "$dst" ]]; then
    if (( FORCE )); then
      backup="$dst.pre-install-$STAMP"
      if (( DRY_RUN )); then
        echo "  [backup] $dst -> $backup; then -> $src"
      else
        mv "$dst" "$backup"
        ln -sfn "$src" "$dst"
        echo "  [backup] $dst -> $backup; linked -> $src"
      fi
    else
      echo "  [skip]   $dst exists as a real file (use --force to back up and replace)" >&2
    fi
  else
    if (( DRY_RUN )); then
      echo "  [new]    $dst -> $src"
    else
      ln -sfn "$src" "$dst"
      echo "  [new]    $dst -> $src"
    fi
  fi
done

# Warn if ~/.local/bin isn't on PATH.
case ":$PATH:" in
  *":$BIN_DST:"*) ;;
  *)
    echo ""
    echo "  WARNING: $BIN_DST is not on PATH."
    echo "  Add to your shell rc:"
    echo '    export PATH="$HOME/.local/bin:$PATH"'
    ;;
esac

# Key handling
echo ""
if [[ -r "$KEY_FILE" && -s "$KEY_FILE" ]]; then
  size=$(wc -c < "$KEY_FILE" | tr -d ' ')
  echo "  [ok]     $KEY_FILE present ($size bytes)"
  if (( size < 60 || size > 400 )); then
    echo "  WARNING: key size looks unusual (expected ~120-160 bytes, got $size)"
  fi
  exit 0
fi

echo "  [miss]   $KEY_FILE not found or empty"
if (( PROMPT_FOR_KEY )) && (( ! DRY_RUN )); then
  echo ""
  echo "  Get a key at https://platform.minimax.io/subscribe/coding-plan"
  echo "  (Token Plan keys start with sk-cp-)"
  echo ""
  mkdir -p "$(dirname "$KEY_FILE")"
  chmod 700 "$(dirname "$KEY_FILE")"
  umask 077
  printf "  Paste MiniMax Token Plan key (input hidden): "
  IFS= read -rs K
  echo ""
  if [[ -z "$K" ]]; then
    echo "  [skip]   empty input — key not saved"
    exit 10
  fi
  printf '%s' "$K" > "$KEY_FILE"
  unset K
  chmod 600 "$KEY_FILE"
  echo "  [ok]     $KEY_FILE saved"
else
  echo ""
  echo "  To add the key non-interactively:"
  echo "    umask 077 && mkdir -p ~/.config/minimax && \\"
  echo "      read -rs 'K?Paste MiniMax key: ' && \\"
  echo "      printf '%s' \"\$K\" > $KEY_FILE && unset K && \\"
  echo "      chmod 600 $KEY_FILE"
  exit 10
fi

exit 0
