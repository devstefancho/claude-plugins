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

# ── Test 1: Normal clone ──
echo "Test 1: Normal clone detection"
REPO_DIR="$TMPDIR_BASE/normal-repo"
REPO_DIR_REAL=$(mkdir -p "$REPO_DIR" && cd "$REPO_DIR" && pwd -P)
git -C "$REPO_DIR_REAL" init -b main --quiet
git -C "$REPO_DIR_REAL" commit --allow-empty -m "init" --quiet

RESULT=$(cd "$REPO_DIR_REAL" && source "$SCRIPTS_DIR/detect.sh" && echo "$WORKTREE_STYLE|$PROJECT_ROOT")
STYLE=$(echo "$RESULT" | cut -d'|' -f1)
PROJ=$(echo "$RESULT" | cut -d'|' -f2)

assert_eq "WORKTREE_STYLE=normal" "normal" "$STYLE"
assert_eq "PROJECT_ROOT matches" "$REPO_DIR_REAL" "$PROJ"

# ── Test 2: Bare repo worktree detection ──
echo "Test 2: Bare repo worktree detection"
BARE_PROJECT="$TMPDIR_BASE/bare-project"
mkdir -p "$BARE_PROJECT"
BARE_PROJECT_REAL=$(cd "$BARE_PROJECT" && pwd -P)

# Create a source repo to clone from
SOURCE_REPO="$TMPDIR_BASE/source-repo"
mkdir -p "$SOURCE_REPO"
git -C "$SOURCE_REPO" init -b main --quiet
git -C "$SOURCE_REPO" commit --allow-empty -m "init" --quiet

# Clone as bare
git clone --bare "$SOURCE_REPO" "$BARE_PROJECT_REAL/.bare" --quiet
echo "gitdir: ./.bare" > "$BARE_PROJECT_REAL/.git"
git -C "$BARE_PROJECT_REAL" config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
mkdir -p "$BARE_PROJECT_REAL/trees"
git -C "$BARE_PROJECT_REAL" worktree add "./trees/main" main --quiet

RESULT=$(cd "$BARE_PROJECT_REAL/trees/main" && source "$SCRIPTS_DIR/detect.sh" && echo "$WORKTREE_STYLE|$PROJECT_ROOT")
STYLE=$(echo "$RESULT" | cut -d'|' -f1)
PROJ=$(echo "$RESULT" | cut -d'|' -f2)

assert_eq "WORKTREE_STYLE=bare" "bare" "$STYLE"
assert_eq "PROJECT_ROOT matches bare project" "$BARE_PROJECT_REAL" "$PROJ"

# ── Test 3: Non-git directory ──
echo "Test 3: Non-git directory detection"
NON_GIT="$TMPDIR_BASE/not-git"
mkdir -p "$NON_GIT"
NON_GIT_REAL=$(cd "$NON_GIT" && pwd -P)

RESULT=$(cd "$NON_GIT_REAL" && source "$SCRIPTS_DIR/detect.sh" && echo "$WORKTREE_STYLE")

assert_eq "WORKTREE_STYLE=none" "none" "$RESULT"

# ── Test 4: WORKTREE_ROOT for bare repo ──
echo "Test 4: WORKTREE_ROOT for bare repo"
RESULT=$(cd "$BARE_PROJECT_REAL/trees/main" && source "$SCRIPTS_DIR/detect.sh" && echo "$WORKTREE_ROOT")

assert_eq "WORKTREE_ROOT" "$BARE_PROJECT_REAL/trees" "$RESULT"

# ── Summary ──
if [ "$ERRORS" -gt 0 ]; then
  echo "test-detect: $ERRORS error(s)"
  exit 1
fi
echo "test-detect: all passed"
