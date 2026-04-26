#!/bin/bash
set -euo pipefail

# Usage: create-and-open.sh --project-root ROOT --worktree-root WTROOT
#        [--branch BRANCH --base BASE | --pr NUMBER]
#        [--push] [--tmux-name NAME] [--context CONTEXT]
#
# Unified script: create-worktree + push + open-in-tmux in a single call.

usage() {
  echo "Usage: $0 --project-root ROOT --worktree-root WTROOT"
  echo "       [--branch BRANCH --base BASE | --pr NUMBER]"
  echo "       [--push] [--tmux-name NAME] [--context CONTEXT]"
  exit 1
}

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

PROJECT_ROOT=""
WORKTREE_ROOT=""
BRANCH=""
BASE=""
PR=""
PUSH=false
TMUX_NAME=""
CONTEXT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project-root) PROJECT_ROOT="$2"; shift 2 ;;
    --worktree-root) WORKTREE_ROOT="$2"; shift 2 ;;
    --branch) BRANCH="$2"; shift 2 ;;
    --base) BASE="$2"; shift 2 ;;
    --pr) PR="$2"; shift 2 ;;
    --push) PUSH=true; shift ;;
    --tmux-name) TMUX_NAME="$2"; shift 2 ;;
    --context) CONTEXT="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; usage ;;
  esac
done

if [ -z "$PROJECT_ROOT" ] || [ -z "$WORKTREE_ROOT" ]; then
  echo "ERROR: --project-root and --worktree-root are required" >&2
  usage
fi

# 1. Create worktree
if [ -n "$PR" ]; then
  bash "$SCRIPT_DIR/create-worktree.sh" \
    --project-root "$PROJECT_ROOT" \
    --worktree-root "$WORKTREE_ROOT" \
    --pr "$PR"

  WORKTREE_PATH="$WORKTREE_ROOT/pr-$PR"
  [ -z "$TMUX_NAME" ] && TMUX_NAME="pr-$PR"
else
  if [ -z "$BRANCH" ] || [ -z "$BASE" ]; then
    echo "ERROR: --branch and --base are required for new branch mode" >&2
    usage
  fi

  bash "$SCRIPT_DIR/create-worktree.sh" \
    --project-root "$PROJECT_ROOT" \
    --worktree-root "$WORKTREE_ROOT" \
    --branch "$BRANCH" \
    --base "$BASE"

  DIR_NAME=$(echo "$BRANCH" | tr '/' '-')
  WORKTREE_PATH="$WORKTREE_ROOT/$DIR_NAME"
  [ -z "$TMUX_NAME" ] && TMUX_NAME="$DIR_NAME"
fi

# 2. Push to remote (new branch only)
if [ "$PUSH" = true ] && [ -n "$BRANCH" ]; then
  cd "$WORKTREE_PATH"
  git push -u origin "$BRANCH" 2>&1 || echo "WARNING: push failed, continuing..." >&2
fi

# 3. Open in tmux
if [ -z "$CONTEXT" ]; then
  CONTEXT="Branch: $BRANCH"
fi

bash "$SCRIPT_DIR/open-in-tmux.sh" \
  --path "$WORKTREE_PATH" \
  --name "$TMUX_NAME" \
  --context "$CONTEXT"
