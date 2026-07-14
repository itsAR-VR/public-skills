#!/usr/bin/env bash
set -euo pipefail

ROOT="${AGENT_TMUX_LOG_ROOT:-/tmp/agent-terminal-control}"
DEFAULT_HISTORY="${AGENT_TMUX_HISTORY_LIMIT:-200000}"
DEFAULT_WIDTH="${AGENT_TMUX_WIDTH:-140}"
DEFAULT_HEIGHT="${AGENT_TMUX_HEIGHT:-45}"

usage() {
  cat <<'USAGE'
agent-tmux-control.sh - control interactive agents through tmux

Commands:
  start --name NAME --cwd DIR [--log PATH] [--width N] [--height N] -- CMD...
  start-claude --name NAME --cwd DIR [--log PATH] -- [claude args...]
  start-codex --name NAME --cwd DIR [--log PATH] -- [codex args...]
  send --name NAME --text TEXT
  send-file --name NAME --file PATH
  capture --name NAME [--tail N]
  log --name NAME [--tail N] [--plain]
  wait --name NAME --pattern REGEX [--timeout SEC]
  wait-log --name NAME --pattern REGEX [--timeout SEC] [--fresh]
  list
  status --name NAME
  stop --name NAME

Notes:
  - start-claude launches interactive `claude`, never `claude -p`.
  - pipe-pane logs are written immediately and are the durable proof surface.
USAGE
}

die() {
  echo "agent-tmux-control: $*" >&2
  exit 1
}

require_tmux() {
  command -v tmux >/dev/null 2>&1 || die "tmux not found"
}

require_name() {
  [[ -n "${name:-}" ]] || die "--name is required"
}

default_log_path() {
  mkdir -p "$ROOT"
  printf '%s/%s.log\n' "$ROOT" "$1"
}

state_path() {
  mkdir -p "$ROOT"
  printf '%s/%s.state\n' "$ROOT" "$1"
}

remember_session() {
  local name="$1" log="$2" cwd="$3" pane="$4"
  local state
  state="$(state_path "$name")"
  {
    printf 'log=%s\n' "$log"
    printf 'cwd=%s\n' "$cwd"
    printf 'pane=%s\n' "$pane"
  } > "$state"
}

remembered_value() {
  local name="$1" key="$2" state line
  state="$(state_path "$name")"
  if [[ -f "$state" ]]; then
    while IFS= read -r line; do
      case "$line" in
        "$key"=*) printf '%s\n' "${line#*=}"; return 0 ;;
      esac
    done < "$state"
  fi
  return 1
}

remembered_log_path() {
  local name="$1"
  if remembered_value "$name" log; then
    return 0
  fi
  default_log_path "$name"
}

target_for_name() {
  local name="$1"
  remembered_value "$name" pane || printf '%s\n' "$name"
}

strip_control_sequences() {
  perl -pe 's/\e\][^\a]*(\a|\e\\)//g; s/\e\[[0-9;?]*[ -\/]*[@-~]//g; s/\r/\n/g'
}

shell_quote() {
  local out="" item
  for item in "$@"; do
    printf -v item "%q" "$item"
    out+="${item} "
  done
  printf '%s' "$out"
}

start_session() {
  local name="" cwd="" log="" width="$DEFAULT_WIDTH" height="$DEFAULT_HEIGHT"
  local args=()

  while (($#)); do
    case "$1" in
      --name) name="${2:-}"; shift 2 ;;
      --cwd) cwd="${2:-}"; shift 2 ;;
      --log) log="${2:-}"; shift 2 ;;
      --width) width="${2:-}"; shift 2 ;;
      --height) height="${2:-}"; shift 2 ;;
      --) shift; args=("$@"); break ;;
      *) die "unknown start option: $1" ;;
    esac
  done

  require_name
  [[ -n "$cwd" ]] || die "--cwd is required"
  [[ -d "$cwd" ]] || die "cwd does not exist: $cwd"
  ((${#args[@]} > 0)) || die "command is required after --"

  require_tmux
  log="${log:-$(default_log_path "$name")}"
  mkdir -p "$(dirname "$log")"
  : > "$log"

  if tmux has-session -t "$name" 2>/dev/null; then
    die "tmux session already exists: $name"
  fi

  local quoted_cwd quoted_cmd cmd
  printf -v quoted_cwd "%q" "$cwd"
  quoted_cmd="$(shell_quote "${args[@]}")"
  cmd="cd ${quoted_cwd} && exec ${quoted_cmd}"

  tmux new-session -d -s "$name" -x "$width" -y "$height" "$cmd"
  local pane
  pane="$(tmux list-panes -t "$name" -F '#{pane_id}' | head -n 1)"
  [[ -n "$pane" ]] || die "could not resolve pane id for session: $name"
  tmux set-option -t "$name" history-limit "$DEFAULT_HISTORY" >/dev/null
  tmux pipe-pane -o -t "$pane" "cat >> $(printf "%q" "$log")"
  remember_session "$name" "$log" "$cwd" "$pane"

  echo "started: $name"
  echo "pane: $pane"
  echo "log: $log"
}

start_agent() {
  local agent="$1"
  shift
  local control_args=() agent_args=()
  while (($#)); do
    case "$1" in
      --) shift; agent_args=("$@"); break ;;
      *) control_args+=("$1"); shift ;;
    esac
  done
  if ((${#agent_args[@]})); then
    start_session "${control_args[@]}" -- "$agent" "${agent_args[@]}"
  else
    start_session "${control_args[@]}" -- "$agent"
  fi
}

send_text() {
  local name="" text=""
  while (($#)); do
    case "$1" in
      --name) name="${2:-}"; shift 2 ;;
      --text) text="${2:-}"; shift 2 ;;
      *) die "unknown send option: $1" ;;
    esac
  done
  require_name
  local target
  target="$(target_for_name "$name")"
  tmux send-keys -t "$target" -l -- "$text"
  tmux send-keys -t "$target" Enter
}

send_file() {
  local name="" file=""
  while (($#)); do
    case "$1" in
      --name) name="${2:-}"; shift 2 ;;
      --file) file="${2:-}"; shift 2 ;;
      *) die "unknown send-file option: $1" ;;
    esac
  done
  require_name
  [[ -r "$file" ]] || die "file is not readable: $file"
  local target
  target="$(target_for_name "$name")"
  tmux load-buffer "$file"
  tmux paste-buffer -t "$target" -p
  tmux send-keys -t "$target" Enter
}

capture_pane() {
  local name="" tail_lines=""
  while (($#)); do
    case "$1" in
      --name) name="${2:-}"; shift 2 ;;
      --tail) tail_lines="${2:-}"; shift 2 ;;
      *) die "unknown capture option: $1" ;;
    esac
  done
  require_name
  local target
  target="$(target_for_name "$name")"
  if [[ -n "$tail_lines" ]]; then
    tmux capture-pane -t "$target" -p -S - | tail -n "$tail_lines"
  else
    tmux capture-pane -t "$target" -p -S -
  fi
}

show_log() {
  local name="" log="" tail_lines="" plain=0
  while (($#)); do
    case "$1" in
      --name) name="${2:-}"; shift 2 ;;
      --log) log="${2:-}"; shift 2 ;;
      --tail) tail_lines="${2:-}"; shift 2 ;;
      --plain) plain=1; shift ;;
      *) die "unknown log option: $1" ;;
    esac
  done
  require_name
  log="${log:-$(remembered_log_path "$name")}"
  [[ -f "$log" ]] || die "log not found: $log"
  if [[ "$plain" == "1" ]]; then
    if [[ -n "$tail_lines" ]]; then
      tail -n "$tail_lines" "$log" | strip_control_sequences
    else
      strip_control_sequences < "$log"
    fi
  else
    if [[ -n "$tail_lines" ]]; then
      tail -n "$tail_lines" "$log"
    else
      cat "$log"
    fi
  fi
}

wait_for_pattern() {
  local name="" pattern="" timeout=60
  while (($#)); do
    case "$1" in
      --name) name="${2:-}"; shift 2 ;;
      --pattern) pattern="${2:-}"; shift 2 ;;
      --timeout) timeout="${2:-}"; shift 2 ;;
      *) die "unknown wait option: $1" ;;
    esac
  done
  require_name
  [[ -n "$pattern" ]] || die "--pattern is required"

  local start now
  local target
  target="$(target_for_name "$name")"
  start="$(date +%s)"
  while true; do
    if tmux capture-pane -t "$target" -p -S - | grep -E "$pattern" >/dev/null; then
      echo "matched: $pattern"
      return 0
    fi
    now="$(date +%s)"
    if (( now - start >= timeout )); then
      die "timeout waiting for pattern: $pattern"
    fi
    sleep 1
  done
}

wait_for_log_pattern() {
  local name="" pattern="" timeout=60 fresh=0
  while (($#)); do
    case "$1" in
      --name) name="${2:-}"; shift 2 ;;
      --pattern) pattern="${2:-}"; shift 2 ;;
      --timeout) timeout="${2:-}"; shift 2 ;;
      --fresh) fresh=1; shift ;;
      *) die "unknown wait-log option: $1" ;;
    esac
  done
  require_name
  [[ -n "$pattern" ]] || die "--pattern is required"

  local log offset=1 start now
  log="$(remembered_log_path "$name")"
  [[ -f "$log" ]] || die "log not found: $log"
  if [[ "$fresh" == "1" ]]; then
    offset="$(( $(wc -c < "$log" | tr -d ' ') + 1 ))"
  fi

  start="$(date +%s)"
  while true; do
    if tail -c +"$offset" "$log" | strip_control_sequences | grep -E "$pattern" >/dev/null; then
      echo "matched log: $pattern"
      return 0
    fi
    now="$(date +%s)"
    if (( now - start >= timeout )); then
      die "timeout waiting for log pattern: $pattern"
    fi
    sleep 1
  done
}

list_sessions() {
  mkdir -p "$ROOT"
  local state name log cwd pane status found=0
  for state in "$ROOT"/*.state; do
    [[ -f "$state" ]] || continue
    found=1
    name="$(basename "${state%.state}")"
    log="$(remembered_value "$name" log || true)"
    cwd="$(remembered_value "$name" cwd || true)"
    pane="$(remembered_value "$name" pane || true)"
    if tmux has-session -t "$name" 2>/dev/null; then
      status="running"
    else
      status="stopped"
    fi
    printf 'name=%s status=%s pane=%s log=%s cwd=%s\n' "$name" "$status" "$pane" "$log" "$cwd"
  done
  if [[ "$found" == "0" ]]; then
    echo "no managed sessions"
  fi
}

status_session() {
  local name=""
  while (($#)); do
    case "$1" in
      --name) name="${2:-}"; shift 2 ;;
      *) die "unknown status option: $1" ;;
    esac
  done
  require_name
  if tmux has-session -t "$name" 2>/dev/null; then
    tmux list-panes -t "$name" -F 'session=#{session_name} window=#{window_index} pane=#{pane_index} pid=#{pane_pid} command=#{pane_current_command} active=#{pane_active}'
  else
    die "tmux session not found: $name"
  fi
}

stop_session() {
  local name=""
  while (($#)); do
    case "$1" in
      --name) name="${2:-}"; shift 2 ;;
      *) die "unknown stop option: $1" ;;
    esac
  done
  require_name
  local target
  target="$(target_for_name "$name")"
  tmux pipe-pane -t "$target" '' 2>/dev/null || true
  tmux kill-session -t "$name" 2>/dev/null || true
}

main() {
  (($# > 0)) || { usage; exit 1; }
  local cmd="$1"
  shift
  case "$cmd" in
    start) start_session "$@" ;;
    start-claude) start_agent claude "$@" ;;
    start-codex) start_agent codex "$@" ;;
    send) send_text "$@" ;;
    send-file) send_file "$@" ;;
    capture) capture_pane "$@" ;;
    log) show_log "$@" ;;
    wait) wait_for_pattern "$@" ;;
    wait-log) wait_for_log_pattern "$@" ;;
    list) list_sessions "$@" ;;
    status) status_session "$@" ;;
    stop) stop_session "$@" ;;
    -h|--help|help) usage ;;
    *) die "unknown command: $cmd" ;;
  esac
}

main "$@"
