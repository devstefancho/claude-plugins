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

# Setup: create a source repo with remote
SOURCE_REPO="$TMPDIR_BASE/source"
mkdir -p "$SOURCE_REPO"
git -C "$SOURCE_REPO" init -b main --quiet
git -C "$SOURCE_REPO" commit --allow-empty -m "init" --quiet

# ── Test 1: Normal clone - create branch worktree ──
echo "Test 1: Normal clone - create branch worktree"
NORMAL_REPO="$TMPDIR_BASE/normal-clone"
git clone "$SOURCE_REPO" "$NORMAL_REPO" --quiet

bash "$SCRIPTS_DIR/create-worktree.sh" \
  --project-root "$NORMAL_REPO" \
  --worktree-root "$NORMAL_REPO/trees" \
  --branch "feat/auth" \
  --base "origin/main"

assert_dir_exists "worktree directory created" "$NORMAL_REPO/trees/feat-auth"

# Verify branch exists (+ prefix means checked out in a worktree)
BRANCH_EXISTS=$(git -C "$NORMAL_REPO" branch --list "feat/auth" | sed 's/^[* +]*//')
assert_eq "branch feat/auth exists" "feat/auth" "$BRANCH_EXISTS"

# ── Test 2: Bare repo - create branch worktree ──
echo "Test 2: Bare repo - create branch worktree"
BARE_PROJECT="$TMPDIR_BASE/bare-project"
mkdir -p "$BARE_PROJECT"
git clone --bare "$SOURCE_REPO" "$BARE_PROJECT/.bare" --quiet
echo "gitdir: ./.bare" > "$BARE_PROJECT/.git"
git -C "$BARE_PROJECT" config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git -C "$BARE_PROJECT" fetch origin --quiet
mkdir -p "$BARE_PROJECT/trees"
git -C "$BARE_PROJECT" worktree add "./trees/main" main --quiet

bash "$SCRIPTS_DIR/create-worktree.sh" \
  --project-root "$BARE_PROJECT" \
  --worktree-root "$BARE_PROJECT/trees" \
  --branch "fix/bug-123" \
  --base "origin/main"

assert_dir_exists "bare repo worktree created" "$BARE_PROJECT/trees/fix-bug-123"

# ── Test 3: Duplicate path → error ──
echo "Test 3: Duplicate path raises error"
OUTPUT=$(bash "$SCRIPTS_DIR/create-worktree.sh" \
  --project-root "$NORMAL_REPO" \
  --worktree-root "$NORMAL_REPO/trees" \
  --branch "feat/auth-dup" \
  --base "origin/main" 2>&1 || true)

# First creation should succeed, try same dir name
bash "$SCRIPTS_DIR/create-worktree.sh" \
  --project-root "$NORMAL_REPO" \
  --worktree-root "$NORMAL_REPO/trees" \
  --branch "feat/auth2" \
  --base "origin/main" 2>&1 >/dev/null

# Now try to create again at same path by using same branch dir name
OUTPUT=$(bash "$SCRIPTS_DIR/create-worktree.sh" \
  --project-root "$NORMAL_REPO" \
  --worktree-root "$NORMAL_REPO/trees" \
  --branch "feat/auth-dup2" \
  --base "origin/main" 2>&1 || true)

# Create a conflicting directory manually
mkdir -p "$NORMAL_REPO/trees/feat-conflict"
OUTPUT=$(bash "$SCRIPTS_DIR/create-worktree.sh" \
  --project-root "$NORMAL_REPO" \
  --worktree-root "$NORMAL_REPO/trees" \
  --branch "feat/conflict" \
  --base "origin/main" 2>&1 || true)

if echo "$OUTPUT" | grep -q "ERROR.*already exists"; then
  echo "  OK: error on duplicate path"
else
  echo "  FAIL: expected error for duplicate path"
  ((ERRORS++))
fi

# ── Summary ──
if [ "$ERRORS" -gt 0 ]; then
  echo "test-create-worktree: $ERRORS error(s)"
  exit 1
fi
echo "test-create-worktree: all passed"
