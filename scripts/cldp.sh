#!/usr/bin/env bash
# cldp - Claude Dev Plugin: fzf로 worktree 플러그인 선택 후 claude --plugin-dir 실행

cldp() {
  local base=~/works/claude-plugins/.claude/worktrees
  local selected=$(
    find "$base" -name ".claude-plugin" -type d -not -path "*/dist/*" 2>/dev/null \
      | sed 's|/.claude-plugin$||' \
      | sed "s|.*worktrees/||" \
      | fzf --multi --prompt="Select plugin(s): "
  )
  [[ -z "$selected" ]] && return

  local dirs=()
  while IFS= read -r p; do
    dirs+=(--plugin-dir "$base/$p")
  done <<< "$selected"

  claude "${dirs[@]}" "$@"
}
