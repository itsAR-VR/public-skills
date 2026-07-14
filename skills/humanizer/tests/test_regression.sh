#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LINT="$ROOT/scripts/regression_lint.py"
FIXTURES="$ROOT/tests/fixtures"

# Should fail
if python3 "$LINT" --text-file "$FIXTURES/fail_stock_phrases.txt" --strict >/tmp/humanizer_test_fail1.json 2>&1; then
  echo "Expected fail_stock_phrases.txt to fail, but it passed"
  exit 1
fi

if python3 "$LINT" --text-file "$FIXTURES/fail_structural_patterns.txt" --strict >/tmp/humanizer_test_fail2.json 2>&1; then
  echo "Expected fail_structural_patterns.txt to fail, but it passed"
  exit 1
fi

if python3 "$LINT" --text-file "$FIXTURES/fail_hormozi_ai_memo.txt" --strict >/tmp/humanizer_test_fail3.json 2>&1; then
  echo "Expected fail_hormozi_ai_memo.txt to fail, but it passed"
  exit 1
fi

# Should pass
python3 "$LINT" --text-file "$FIXTURES/pass_humanized.txt" --strict >/tmp/humanizer_test_pass.json
python3 "$LINT" --text-file "$FIXTURES/pass_hormozi_humanized_memo.txt" --strict >/tmp/humanizer_test_pass2.json

echo "humanizer regression tests: PASS"
