#!/usr/bin/env bash
set -euo pipefail

mode="read-only"
format="text"
compact=1
cwd=""
prompt_file=""

usage() {
  cat <<'EOF'
Usage:
  run.sh [--cwd PATH] [--json] [--write] [--no-compact] [--prompt-file FILE] "prompt text"

Defaults:
  permission-mode: read-only
  output-format:   text
  compact:         on

Examples:
  run.sh "Audit this repo for flaky tests"
  run.sh --json "List risky files as JSON"
  run.sh --cwd /abs/repo --prompt-file /tmp/prompt.txt
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --cwd)
      cwd="${2:?missing path for --cwd}"
      shift 2
      ;;
    --json)
      format="json"
      compact=0
      shift
      ;;
    --write)
      mode="workspace-write"
      shift
      ;;
    --no-compact)
      compact=0
      shift
      ;;
    --prompt-file)
      prompt_file="${2:?missing path for --prompt-file}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    *)
      break
      ;;
  esac
done

if ! command -v claw-mm >/dev/null 2>&1; then
  echo "run.sh: claw-mm is not on PATH." >&2
  echo "  Repair with ~/.codex/skills/minimax-setup/scripts/install.sh" >&2
  exit 1
fi

if [[ -n "$cwd" ]]; then
  cd "$cwd"
fi

if [[ -n "$prompt_file" ]]; then
  if [[ ! -r "$prompt_file" ]]; then
    echo "run.sh: prompt file is not readable: $prompt_file" >&2
    exit 1
  fi
  prompt="$(cat "$prompt_file")"
elif [[ $# -gt 0 ]]; then
  prompt="$*"
else
  usage >&2
  exit 2
fi

cmd=(claw-mm --permission-mode "$mode" --output-format "$format")
if [[ "$format" == "text" && "$compact" -eq 1 ]]; then
  cmd+=(--compact)
fi

exec "${cmd[@]}" "$prompt"
