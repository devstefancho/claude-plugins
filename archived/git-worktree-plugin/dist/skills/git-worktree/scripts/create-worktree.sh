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
  # PR checkout mode - optimized: fetch PR branch directly, then create worktree
  WORKTREE_PATH="$WORKTREE_ROOT/pr-$PR"

  if [ -d "$WORKTREE_PATH" ]; then
    echo "ERROR: Worktree path already exists: $WORKTREE_PATH" >&2
    exit 1
  fi

  # Try to get PR branch name and create worktree directly (avoids double file write)
  PR_BRANCH=$(gh pr view "$PR" --json headRefName --jq '.headRefName' 2>/dev/null || true)

  if [ -n "$PR_BRANCH" ]; then
    # Same-repo PR: fetch the branch and create worktree directly
    echo "Fetching PR branch '$PR_BRANCH' from origin..."
    git -C "$PROJECT_ROOT" fetch origin "$PR_BRANCH"
    FETCHED_COMMIT=$(git -C "$PROJECT_ROOT" rev-parse --short "origin/$PR_BRANCH" 2>/dev/null || echo "unknown")
    echo "Fetched: origin/$PR_BRANCH → $FETCHED_COMMIT ($(date '+%Y-%m-%d %H:%M:%S'))"

    git -C "$PROJECT_ROOT" worktree add "$WORKTREE_PATH" -b "pr-$PR" "origin/$PR_BRANCH"
  else
    # Fork PR or gh unavailable: fallback to detach + gh pr checkout
    git -C "$PROJECT_ROOT" worktree add "$WORKTREE_PATH" --detach
    cd "$WORKTREE_PATH"
    gh pr checkout "$PR"
  fi

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

  # Targeted fetch: only the base branch instead of all refs
  BASE_BRANCH=$(echo "$BASE" | sed 's|^origin/||')
  echo "Fetching latest '$BASE_BRANCH' from origin..."
  git -C "$PROJECT_ROOT" fetch origin "$BASE_BRANCH"
  FETCHED_COMMIT=$(git -C "$PROJECT_ROOT" rev-parse --short "$BASE" 2>/dev/null || echo "unknown")
  echo "Fetched: $BASE → $FETCHED_COMMIT ($(date '+%Y-%m-%d %H:%M:%S'))"

  git -C "$PROJECT_ROOT" worktree add "$WORKTREE_PATH" -b "$BRANCH" "$BASE"

  echo "Worktree created"
  echo "  Branch: $BRANCH"
  echo "  Base: $BASE"
  echo "  Path: $WORKTREE_PATH"
fi
