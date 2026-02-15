#!/bin/bash
# Usage: source detect.sh
# Sets environment variables: WORKTREE_STYLE, WORKTREE_ROOT, PROJECT_ROOT
#
# WORKTREE_STYLE values:
#   "bare"   - inside a bare repo worktree structure
#   "normal" - inside a regular git clone
#   "none"   - not inside a git repository

TOPLEVEL=$(git rev-parse --show-toplevel 2>/dev/null)

if [ -z "$TOPLEVEL" ]; then
  WORKTREE_STYLE="none"
  WORKTREE_ROOT=""
  PROJECT_ROOT=""
  export WORKTREE_STYLE WORKTREE_ROOT PROJECT_ROOT
  return 0 2>/dev/null || exit 0
fi

if [ -f "$TOPLEVEL/.git" ]; then
  # .git is a file → this is a worktree or bare setup
  GIT_COMMON=$(cd "$TOPLEVEL" && git rev-parse --git-common-dir)
  BARE_DIR=$(cd "$TOPLEVEL" && cd "$GIT_COMMON" && pwd)
  PROJECT_ROOT=$(dirname "$BARE_DIR")
  WORKTREE_ROOT="$PROJECT_ROOT/trees"
  WORKTREE_STYLE="bare"
else
  PROJECT_ROOT="$TOPLEVEL"
  WORKTREE_ROOT="$TOPLEVEL/trees"
  WORKTREE_STYLE="normal"
fi

export WORKTREE_STYLE WORKTREE_ROOT PROJECT_ROOT
