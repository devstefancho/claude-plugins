#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
SCRIPTS_DIR="$SCRIPT_DIR/../scripts"
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

# Setup: create a source repo to clone from
SOURCE_REPO="$TMPDIR_BASE/source"
mkdir -p "$SOURCE_REPO"
git -C "$SOURCE_REPO" init -b main --quiet
echo "hello" > "$SOURCE_REPO/README.md"
git -C "$SOURCE_REPO" add README.md
git -C "$SOURCE_REPO" commit -m "init" --quiet

# ── Test 1: Successful conversion ──
echo "Test 1: Clean clone converts to bare successfully"
CLONE1="$TMPDIR_BASE/clone1"
git clone "$SOURCE_REPO" "$CLONE1" --quiet

bash "$SCRIPTS_DIR/convert-to-bare.sh" --project-root "$CLONE1"

assert_dir_exists ".bare/ exists" "$CLONE1/.bare"
assert_file_exists ".git is a file" "$CLONE1/.git"
assert_dir_exists "trees/ exists" "$CLONE1/trees"
assert_dir_exists "trees/main/ worktree" "$CLONE1/trees/main"

# Verify .git is a file
if [ -f "$CLONE1/.git" ] && [ ! -d "$CLONE1/.git" ]; then
  echo "  OK: .git is a file"
else
  echo "  FAIL: .git should be a file"
  ((ERRORS++))
fi

# Verify files in worktree match original
CONTENT=$(cat "$CLONE1/trees/main/README.md")
assert_eq "worktree README content" "hello" "$CONTENT"

# ── Test 2: Uncommitted changes → error ──
echo "Test 2: Uncommitted changes prevent conversion"
CLONE2="$TMPDIR_BASE/clone2"
git clone "$SOURCE_REPO" "$CLONE2" --quiet
echo "dirty" > "$CLONE2/dirty.txt"

OUTPUT=$(bash "$SCRIPTS_DIR/convert-to-bare.sh" --project-root "$CLONE2" 2>&1 || true)
if echo "$OUTPUT" | grep -q "uncommitted changes"; then
  echo "  OK: rejects uncommitted changes"
else
  echo "  FAIL: should reject uncommitted changes"
  ((ERRORS++))
fi

# Verify .git is still a directory (conversion didn't happen)
if [ -d "$CLONE2/.git" ]; then
  echo "  OK: .git directory preserved"
else
  echo "  FAIL: .git should still be a directory"
  ((ERRORS++))
fi

# ── Test 3: Backup exists after conversion ──
echo "Test 3: Backup exists after successful conversion"
assert_dir_exists ".git-backup/ exists" "$CLONE1/.git-backup"

# ── Test 4: detect.sh returns bare after conversion ──
echo "Test 4: detect.sh returns bare after conversion"
RESULT=$(cd "$CLONE1/trees/main" && source "$SCRIPTS_DIR/detect.sh" && echo "$WORKTREE_STYLE")
assert_eq "WORKTREE_STYLE=bare" "bare" "$RESULT"

# ── Test 5: Already bare repo → error ──
echo "Test 5: Already bare repo returns error"
OUTPUT=$(bash "$SCRIPTS_DIR/convert-to-bare.sh" --project-root "$CLONE1" 2>&1 || true)
if echo "$OUTPUT" | grep -q "이미 bare repo"; then
  echo "  OK: rejects already bare repo"
else
  echo "  FAIL: should reject already bare repo"
  ((ERRORS++))
fi

# ── Summary ──
if [ "$ERRORS" -gt 0 ]; then
  echo "test-convert-to-bare: $ERRORS error(s)"
  exit 1
fi
echo "test-convert-to-bare: all passed"
