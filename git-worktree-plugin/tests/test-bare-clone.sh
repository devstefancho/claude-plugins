#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
SCRIPTS_DIR="$SCRIPT_DIR/../skills/git-worktree/scripts"
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

assert_dir_exists() {
  local label="$1" path="$2"
  if [ -d "$path" ]; then
    echo "  OK: $label"
  else
    echo "  FAIL: $label - directory does not exist: $path"
    ((ERRORS++))
  fi
}

assert_file_exists() {
  local label="$1" path="$2"
  if [ -f "$path" ]; then
    echo "  OK: $label"
  else
    echo "  FAIL: $label - file does not exist: $path"
    ((ERRORS++))
  fi
}

# Setup: create a source repo
SOURCE_REPO="$TMPDIR_BASE/source"
mkdir -p "$SOURCE_REPO"
git -C "$SOURCE_REPO" init -b main --quiet
echo "hello" > "$SOURCE_REPO/README.md"
git -C "$SOURCE_REPO" add README.md
git -C "$SOURCE_REPO" commit -m "init" --quiet

# ── Test 1: Bare clone structure ──
echo "Test 1: Bare clone creates correct structure"
TARGET="$TMPDIR_BASE/my-project"

bash "$SCRIPTS_DIR/bare-clone.sh" \
  --url "$SOURCE_REPO" \
  --path "$TARGET" \
  --branch "main"

assert_dir_exists ".bare/ directory" "$TARGET/.bare"
assert_file_exists ".git file" "$TARGET/.git"
assert_dir_exists "trees/ directory" "$TARGET/trees"
assert_dir_exists "trees/main/ worktree" "$TARGET/trees/main"

# Verify .git is a file (not directory)
if [ -f "$TARGET/.git" ] && [ ! -d "$TARGET/.git" ]; then
  echo "  OK: .git is a file"
else
  echo "  FAIL: .git should be a file, not a directory"
  ((ERRORS++))
fi

# ── Test 2: Fetch refspec configuration ──
echo "Test 2: Fetch refspec configured correctly"
REFSPEC=$(git -C "$TARGET" config remote.origin.fetch)
assert_eq "fetch refspec" "+refs/heads/*:refs/remotes/origin/*" "$REFSPEC"

# ── Test 3: Git log works in worktree ──
echo "Test 3: Git operations work in worktree"
LOG_OUTPUT=$(git -C "$TARGET/trees/main" log --oneline 2>&1)
if echo "$LOG_OUTPUT" | grep -q "init"; then
  echo "  OK: git log works in worktree"
else
  echo "  FAIL: git log failed in worktree"
  ((ERRORS++))
fi

# ── Test 4: Files are present in worktree ──
echo "Test 4: Files are present in worktree"
assert_file_exists "README.md in worktree" "$TARGET/trees/main/README.md"
CONTENT=$(cat "$TARGET/trees/main/README.md")
assert_eq "README content" "hello" "$CONTENT"

# ── Summary ──
if [ "$ERRORS" -gt 0 ]; then
  echo "test-bare-clone: $ERRORS error(s)"
  exit 1
fi
echo "test-bare-clone: all passed"
