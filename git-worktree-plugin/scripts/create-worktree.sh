#!/bin/bash
set -euo pipefail

# Usage: create-worktree.sh --project-root ROOT --worktree-root WTROOT --branch BRANCH --base BASE
#        create-worktree.sh --project-root ROOT --worktree-root WTROOT --pr NUMBER

usage() {
  echo "Usage: $0 --project-root ROOT --worktree-root WTROOT --branch BRANCH --base BASE"
  echo "       $0 --project-root ROOT --worktree-root WTROOT --pr NUMBER"
  exit 1
}

PROJECT_ROOT=""
WORKTREE_ROOT=""
BRANCH=""
BASE=""
PR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project-root) PROJECT_ROOT="$2"; shift 2 ;;
    --worktree-root) WORKTREE_ROOT="$2"; shift 2 ;;
    --branch) BRANCH="$2"; shift 2 ;;
    --base) BASE="$2"; shift 2 ;;
    --pr) PR="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; usage ;;
  esac
done

if [ -z "$PROJECT_ROOT" ] || [ -z "$WORKTREE_ROOT" ]; then
  echo "ERROR: --project-root and --worktree-root are required" >&2
  usage
fi

mkdir -p "$WORKTREE_ROOT"

if [ -n "$PR" ]; then
  # PR checkout mode
  WORKTREE_PATH="$WORKTREE_ROOT/pr-$PR"

  if [ -d "$WORKTREE_PATH" ]; then
    echo "ERROR: Worktree path already exists: $WORKTREE_PATH" >&2
    exit 1
  fi

  git -C "$PROJECT_ROOT" worktree add "$WORKTREE_PATH" --detach
  cd "$WORKTREE_PATH"
  gh pr checkout "$PR"

  echo "Worktree created for PR #$PR"
  echo "  Path: $WORKTREE_PATH"
else
  # New branch mode
  if [ -z "$BRANCH" ] || [ -z "$BASE" ]; then
    echo "ERROR: --branch and --base are required for new branch mode" >&2
    usage
  fi

  # Sanitize branch name for directory: replace / with -
  DIR_NAME=$(echo "$BRANCH" | tr '/' '-')
  WORKTREE_PATH="$WORKTREE_ROOT/$DIR_NAME"

  if [ -d "$WORKTREE_PATH" ]; then
    echo "ERROR: Worktree path already exists: $WORKTREE_PATH" >&2
    exit 1
  fi

  git -C "$PROJECT_ROOT" fetch origin

  git -C "$PROJECT_ROOT" worktree add "$WORKTREE_PATH" -b "$BRANCH" "$BASE"

  echo "Worktree created"
  echo "  Branch: $BRANCH"
  echo "  Base: $BASE"
  echo "  Path: $WORKTREE_PATH"
fi
