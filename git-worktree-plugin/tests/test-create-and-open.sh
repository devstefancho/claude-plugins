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

assert_file_contains() {
  local label="$1" path="$2" expected="$3"
  if grep -qF "$expected" "$path" 2>/dev/null; then
    echo "  OK: $label"
  else
    echo "  FAIL: $label - '$expected' not found in $path"
    ((ERRORS++))
  fi
}

# Setup: create a source repo with remote
SOURCE_REPO="$TMPDIR_BASE/source"
mkdir -p "$SOURCE_REPO"
git -C "$SOURCE_REPO" init -b main --quiet
echo "hello" > "$SOURCE_REPO/README.md"
git -C "$SOURCE_REPO" add README.md
git -C "$SOURCE_REPO" commit -m "init" --quiet

# Unset TMUX to avoid opening tmux windows during tests
unset TMUX 2>/dev/null || true

# ── Test 1: New branch - creates worktree, CLAUDE.local.md, outputs path ──
echo "Test 1: New branch - full pipeline"
REPO1="$TMPDIR_BASE/repo1"
git clone "$SOURCE_REPO" "$REPO1" --quiet

OUTPUT=$(bash "$SCRIPTS_DIR/create-and-open.sh" \
  --project-root "$REPO1" \
  --worktree-root "$REPO1/trees" \
  --branch "feat/auth" \
  --base "origin/main" \
  --context "Branch: feat/auth, Base: origin/main
Feature: User authentication system" 2>&1)

assert_dir_exists "worktree created" "$REPO1/trees/feat-auth"
assert_file_exists "CLAUDE.local.md created" "$REPO1/trees/feat-auth/CLAUDE.local.md"
assert_file_contains "CLAUDE.local.md has context" "$REPO1/trees/feat-auth/CLAUDE.local.md" "User authentication system"

# Verify branch exists
BRANCH_EXISTS=$(git -C "$REPO1" branch --list "feat/auth" | sed 's/^[* +]*//')
assert_eq "branch feat/auth exists" "feat/auth" "$BRANCH_EXISTS"

# ── Test 2: Custom tmux-name ──
echo "Test 2: Custom tmux-name parameter"
REPO2="$TMPDIR_BASE/repo2"
git clone "$SOURCE_REPO" "$REPO2" --quiet

OUTPUT=$(bash "$SCRIPTS_DIR/create-and-open.sh" \
  --project-root "$REPO2" \
  --worktree-root "$REPO2/trees" \
  --branch "fix/bug-42" \
  --base "origin/main" \
  --tmux-name "custom-name" \
  --context "Fix bug #42" 2>&1)

assert_dir_exists "worktree created" "$REPO2/trees/fix-bug-42"
assert_file_exists "CLAUDE.local.md created" "$REPO2/trees/fix-bug-42/CLAUDE.local.md"

# ── Test 3: Missing required args → error ──
echo "Test 3: Missing required arguments"
OUTPUT=$(bash "$SCRIPTS_DIR/create-and-open.sh" \
  --project-root "$REPO2" 2>&1 || true)

if echo "$OUTPUT" | grep -q "ERROR"; then
  echo "  OK: error on missing args"
else
  echo "  FAIL: expected error for missing args"
  ((ERRORS++))
fi

# ── Test 4: Default context when none provided ──
echo "Test 4: Default context fallback"
REPO4="$TMPDIR_BASE/repo4"
git clone "$SOURCE_REPO" "$REPO4" --quiet

OUTPUT=$(bash "$SCRIPTS_DIR/create-and-open.sh" \
  --project-root "$REPO4" \
  --worktree-root "$REPO4/trees" \
  --branch "chore/cleanup" \
  --base "origin/main" 2>&1)

assert_file_exists "CLAUDE.local.md created" "$REPO4/trees/chore-cleanup/CLAUDE.local.md"
assert_file_contains "default context has branch" "$REPO4/trees/chore-cleanup/CLAUDE.local.md" "Branch: chore/cleanup"

# ── Summary ──
if [ "$ERRORS" -gt 0 ]; then
  echo "test-create-and-open: $ERRORS error(s)"
  exit 1
fi
echo "test-create-and-open: all passed"
