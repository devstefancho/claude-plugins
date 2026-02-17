#!/bin/bash
set -euo pipefail

# Usage:
#   open-in-tmux.sh --path WORKTREE_PATH --name WINDOW_NAME --context "context text"
#
# Actions:
# 1. Creates CLAUDE.local.md in WORKTREE_PATH with --context content
# 2. If $TMUX is set: opens a new tmux window and runs `claude`
# 3. If $TMUX is not set: prints the path only

usage() {
  echo "Usage: $0 --path PATH --name NAME --context CONTEXT"
  exit 1
}

WORKTREE_PATH=""
WINDOW_NAME=""
CONTEXT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --path) WORKTREE_PATH="$2"; shift 2 ;;
    --name) WINDOW_NAME="$2"; shift 2 ;;
    --context) CONTEXT="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; usage ;;
  esac
done

if [ -z "$WORKTREE_PATH" ] || [ -z "$WINDOW_NAME" ] || [ -z "$CONTEXT" ]; then
  echo "ERROR: --path, --name, and --context are required" >&2
  usage
fi

if [ ! -d "$WORKTREE_PATH" ]; then
  echo "ERROR: Worktree path does not exist: $WORKTREE_PATH" >&2
  exit 1
fi

# Create CLAUDE.local.md
cat > "$WORKTREE_PATH/CLAUDE.local.md" <<EOF
# Task Context

$CONTEXT
EOF

echo "Created CLAUDE.local.md in $WORKTREE_PATH"

# Open in tmux if available
if [ -n "${TMUX:-}" ]; then
  tmux new-window -n "$WINDOW_NAME" -c "$WORKTREE_PATH"
  tmux send-keys "claude" Enter
  echo "Opened tmux window '$WINDOW_NAME' with claude"
else
  echo "Not in tmux session. Worktree ready at:"
  echo "  $WORKTREE_PATH"
fi
