# Hooks Reference

Quick reference for creating event hooks. For complete documentation, see @docs-claude/hooks-reference.md

## Structure

Add to settings.json:
```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command"
          }
        ]
      }
    ]
  }
}
```

## Location

- Project: `.claude/settings.json`
- Personal: `~/.claude/settings.json`
- Local: `.claude/settings.local.json` (gitignored)

## Hook Types

- `"type": "command"` - Execute bash command
- `"type": "prompt"` - LLM-based evaluation

## Common Events

- `PreToolUse` - Before tool runs (can block)
- `PostToolUse` - After tool completes
- `UserPromptSubmit` - Before processing user prompt
- `Stop` - When Claude finishes
- `SubagentStop` - When subagent finishes
- `Notification` - On notifications
- `SessionStart` - Session begins
- `SessionEnd` - Session ends

## Matchers

**For PreToolUse/PostToolUse:**
- `"Write"` - Exact match
- `"Write|Edit"` - Multiple tools
- `"Notebook.*"` - Regex pattern
- `"*"` - All tools

**For other events:** Omit matcher

## Exit Codes (Command Type)

- `0` - Success
- `2` - Block action, show stderr to Claude
- Other - Error, execution continues

## Simple Examples

**Format on write:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $file"
          }
        ]
      }
    ]
  }
}
```

**Prevent stopping:**
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/check-todos.sh"
          }
        ]
      }
    ]
  }
}
```

**Validate bash commands:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python $CLAUDE_PROJECT_DIR/.claude/hooks/validate-bash.py"
          }
        ]
      }
    ]
  }
}
```

## Hook Input

Hooks receive JSON via stdin:
```json
{
  "session_id": "abc123",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": { "file_path": "/path/to/file" }
}
```

## Environment Variables

- `$CLAUDE_PROJECT_DIR` - Project root path
- `$CLAUDE_ENV_FILE` - SessionStart only, for env vars

## Tips

- Use `$CLAUDE_PROJECT_DIR` for project scripts
- Test hooks with `claude --debug`
- Exit code 2 blocks and sends stderr to Claude
- Keep hooks fast (60s timeout default)
- For complete API, see @docs-claude/hooks-reference.md

## Prompt-Based Hooks

Use LLM for intelligent decisions:
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if all tasks complete: $ARGUMENTS"
          }
        ]
      }
    ]
  }
}
```

LLM responds with: `{"decision": "approve"|"block", "reason": "..."}`
