#!/bin/bash
set -euo pipefail

# Usage: cleanup-worktree.sh --project-root ROOT --path WORKTREE_PATH
#        cleanup-worktree.sh --project-root ROOT --all

usage() {
  echo "Usage: $0 --project-root ROOT --path WORKTREE_PATH"
  echo "       $0 --project-root ROOT --all"
  exit 1
}

PROJECT_ROOT=""
WORKTREE_PATH=""
ALL=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project-root) PROJECT_ROOT="$2"; shift 2 ;;
    --path) WORKTREE_PATH="$2"; shift 2 ;;
    --all) ALL=true; shift ;;
    *) echo "Unknown option: $1" >&2; usage ;;
  esac
done

if [ -z "$PROJECT_ROOT" ]; then
  echo "ERROR: --project-root is required" >&2
  usage
fi

if [ "$ALL" = false ] && [ -z "$WORKTREE_PATH" ]; then
  echo "ERROR: --path or --all is required" >&2
  usage
fi

remove_worktree() {
  local wt_path="$1"

  if [ ! -d "$wt_path" ]; then
    echo "WARNING: Path does not exist: $wt_path" >&2
    return 1
  fi

  # Extract branch name from worktree
  local branch
  branch=$(git -C "$PROJECT_ROOT" worktree list --porcelain | \
    awk -v path="$(cd "$wt_path" && pwd)" '$1=="worktree" && $2==path {found=1} found && $1=="branch" {print $2; exit}' | \
    sed 's|refs/heads/||')

  git -C "$PROJECT_ROOT" worktree remove "$wt_path" --force
  echo "Removed worktree: $wt_path"

  if [ -n "$branch" ]; then
    git -C "$PROJECT_ROOT" branch -D "$branch" 2>/dev/null && \
      echo "Deleted branch: $branch" || true
  fi
}

if [ "$ALL" = true ]; then
  TREES_DIR="$PROJECT_ROOT/trees"
  if [ ! -d "$TREES_DIR" ]; then
    echo "No trees/ directory found"
    exit 0
  fi

  REMOVED=0
  for dir in "$TREES_DIR"/*/; do
    [ -d "$dir" ] || continue
    remove_worktree "$dir" && ((REMOVED++)) || true
  done

  echo ""
  echo "Removed $REMOVED worktree(s)"
else
  remove_worktree "$WORKTREE_PATH"
fi
