#!/usr/bin/env bash
# verify.sh — check that MiniMax wrappers, key, and endpoint are all working.
#
# Usage: bash verify.sh [--no-network]   (--no-network skips the curl probe)
#
# Exit codes:
#   0  = fully working (wrappers on PATH, key present, endpoint reachable)
#   10 = wrappers missing or not on PATH
#   11 = key file missing or empty
#   12 = endpoint probe failed (network / auth / rate limit)

set -euo pipefail

SKIP_NET=0
for arg in "$@"; do
  case "$arg" in
    --no-network) SKIP_NET=1 ;;
  esac
done

KEY_FILE="$HOME/.config/minimax/token-plan.key"
WRAPPERS=(claude-mm ct-mm claw-mm claude-mm-sync)

pass()  { printf "  \033[32m✓\033[0m  %s\n" "$1"; }
fail()  { printf "  \033[31m✗\033[0m  %s\n" "$1" >&2; }
warn()  { printf "  \033[33m!\033[0m  %s\n" "$1" >&2; }

echo "minimax-setup: verifying installation"
echo ""

# 1. Wrapper presence
echo "Wrappers on PATH:"
missing=0
for w in "${WRAPPERS[@]}"; do
  if command -v "$w" >/dev/null 2>&1; then
    pass "$w -> $(command -v "$w")"
  else
    fail "$w not found on PATH"
    missing=1
  fi
done
(( missing )) && { echo ""; fail "Wrappers missing — run scripts/install.sh first"; exit 10; }

# 2. Key file
echo ""
echo "API key:"
if [[ ! -r "$KEY_FILE" ]]; then
  fail "$KEY_FILE not readable"
  exit 11
fi
if [[ ! -s "$KEY_FILE" ]]; then
  fail "$KEY_FILE is empty"
  exit 11
fi
size=$(wc -c < "$KEY_FILE" | tr -d ' ')
pass "$KEY_FILE present ($size bytes)"
if (( size < 60 || size > 400 )); then
  warn "size unusual (expected ~120-160 bytes) — if auth fails, re-save the key"
fi
# Check for trailing newline
last_byte=$(tail -c 1 "$KEY_FILE" | od -An -c | tr -d ' ')
if [[ "$last_byte" == "\n" ]]; then
  warn "key has trailing newline — this sometimes causes 401s (re-save with printf, not echo)"
fi

# 3. Endpoint probe
if (( SKIP_NET )); then
  echo ""
  pass "Network probe skipped"
  exit 0
fi

echo ""
echo "Endpoint probe (api.minimax.io/anthropic):"
KEY="$(tr -d '\n\r' < "$KEY_FILE")"
PAYLOAD='{"model":"MiniMax-M2.7","max_tokens":16,"messages":[{"role":"user","content":"ping"}]}'

HTTP_CODE=$(curl -sS -o /tmp/minimax-verify-$$.json -w "%{http_code}" \
  -X POST https://api.minimax.io/anthropic/v1/messages \
  -H "content-type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -H "Authorization: Bearer $KEY" \
  -d "$PAYLOAD" \
  --max-time 30 \
  2>/dev/null || echo "000")

case "$HTTP_CODE" in
  200)
    pass "HTTP 200 — endpoint reachable, key valid"
    rm -f /tmp/minimax-verify-$$.json
    ;;
  401|403)
    fail "HTTP $HTTP_CODE — key rejected (stale, rotated, or malformed)"
    echo "     Rotate at https://platform.minimax.io/subscribe/coding-plan"
    rm -f /tmp/minimax-verify-$$.json
    exit 12
    ;;
  429)
    warn "HTTP 429 — concurrent request cap hit (retry in 5s)"
    rm -f /tmp/minimax-verify-$$.json
    exit 0
    ;;
  000)
    fail "no HTTP response — network blocked or DNS failed"
    exit 12
    ;;
  *)
    fail "HTTP $HTTP_CODE — unexpected response"
    cat /tmp/minimax-verify-$$.json 2>/dev/null | head -5 >&2
    rm -f /tmp/minimax-verify-$$.json
    exit 12
    ;;
esac

echo ""
pass "minimax-setup verified end-to-end"
