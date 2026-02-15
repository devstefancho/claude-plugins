#!/bin/bash
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PASS=0
FAIL=0

for test in "$SCRIPT_DIR"/test-*.sh; do
  echo "=== Running $(basename "$test") ==="
  if bash "$test"; then
    echo "--- PASS ---"
    ((PASS++))
  else
    echo "--- FAIL ---"
    ((FAIL++))
  fi
  echo ""
done

echo "================================"
echo "Results: $PASS passed, $FAIL failed"
echo "================================"
[ "$FAIL" -eq 0 ]
