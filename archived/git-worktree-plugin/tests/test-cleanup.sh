#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
SCRIPTS_DIR="$SCRIPT_DIR/../dist/skills/git-worktree/scripts"
TMPDIR_BASE=$(mktemp -d)
ERRORS=0

cleanup() {
  rm -rf "$TMPDIR_BASE"
}
trap cleanup EXIT

assert_eq() {
  local label="$1" expected="$2" actual="$3"
  if [ "$expected" != "$actual" ]; then
    echo "  FAIL: $label - expected '$expected', got '$actual'"
    ((ERRORS++))
  else
    echo "  OK: $label"
  fi
}

# Setup: create source and clone
SOURCE_REPO="$TMPDIR_BASE/source"
mkdir -p "$SOURCE_REPO"
git -C "$SOURCE_REPO" init -b main --quiet
git -C "$SOURCE_REPO" commit --allow-empty -m "init" --quiet

REPO="$TMPDIR_BASE/repo"
git clone "$SOURCE_REPO" "$REPO" --quiet

# Create a worktree to test cleanup
mkdir -p "$REPO/trees"
git -C "$REPO" worktree add "$REPO/trees/feat-test" -b feat/test origin/main --quiet

# ── Test 1: Remove single worktree ──
echo "Test 1: Remove single worktree"

# Verify worktree exists first
WT_COUNT_BEFORE=$(git -C "$REPO" worktree list | wc -l | tr -d ' ')

bash "$SCRIPTS_DIR/cleanup-worktree.sh" \
  --project-root "$REPO" \
  --path "$REPO/trees/feat-test"

WT_COUNT_AFTER=$(git -C "$REPO" worktree list | wc -l | tr -d ' ')

if [ "$WT_COUNT_AFTER" -lt "$WT_COUNT_BEFORE" ]; then
  echo "  OK: worktree removed"
else
  echo "  FAIL: worktree count didn't decrease"
  ((ERRORS++))
fi

# Verify directory removed
if [ ! -d "$REPO/trees/feat-test" ]; then
  echo "  OK: directory removed"
else
  echo "  FAIL: worktree directory still exists"
  ((ERRORS++))
fi

# ── Test 2: Non-existent worktree → warning ──
echo "Test 2: Non-existent worktree"
OUTPUT=$(bash "$SCRIPTS_DIR/cleanup-worktree.sh" \
  --project-root "$REPO" \
  --path "$REPO/trees/does-not-exist" 2>&1 || true)

if echo "$OUTPUT" | grep -qi "warning\|not exist\|error"; then
  echo "  OK: proper error/warning for non-existent path"
else
  echo "  FAIL: should warn about non-existent path"
  ((ERRORS++))
fi

# ── Test 3: --all removes all worktrees ──
echo "Test 3: --all removes all worktrees"

# Create multiple worktrees
git -C "$REPO" worktree add "$REPO/trees/feat-a" -b feat/a origin/main --quiet
git -C "$REPO" worktree add "$REPO/trees/feat-b" -b feat/b origin/main --quiet

bash "$SCRIPTS_DIR/cleanup-worktree.sh" \
  --project-root "$REPO" \
  --all

# Check trees/ is empty
REMAINING=$(ls -A "$REPO/trees" 2>/dev/null | wc -l | tr -d ' ')
assert_eq "no worktrees remaining" "0" "$REMAINING"

# ── Summary ──
if [ "$ERRORS" -gt 0 ]; then
  echo "test-cleanup: $ERRORS error(s)"
  exit 1
fi
echo "test-cleanup: all passed"
