---
name: claude-code-generator
description: Generate Claude Code features (slash commands, skills, subagents, hooks, output styles). Use when user asks to create Claude Code build tools or mentions these feature types explicitly.
---

# Claude Code Feature Generator

Quick generator for Claude Code features with proper structure and best practices.

## Feature Types

1. **Slash Commands** - Reusable prompts (`.claude/commands/`)
2. **Skills** - Model-invoked capabilities (`.claude/skills/`)
3. **Subagents** - Specialized AI agents (`.claude/agents/`)
4. **Hooks** - Event handlers (settings.json)
5. **Output Styles** - Custom system prompts (`.claude/output-styles/`)

## Workflow

1. **Detect feature type** from user request
2. **Ask location**: project (`.claude/`) or personal (`~/.claude/`)
3. **Load reference**: See appropriate file in [references/](references/)
4. **Generate feature** using [templates/](templates/)
5. **Validate** naming and structure
6. **Provide** testing guidance

## Feature Detection

- Keywords: "create", "generate", "add", "new"
- Feature names: "slash command", "skill", "subagent", "agent", "hook", "output style"
- Context: "Claude Code tool", "build tool", "custom feature"

## Progressive Disclosure

Load details only when needed:
- Slash commands → [references/slash-commands.md](references/slash-commands.md)
- Skills → [references/skills.md](references/skills.md)
- Subagents → [references/subagents.md](references/subagents.md)
- Hooks → [references/hooks.md](references/hooks.md)
- Output styles → [references/output-styles.md](references/output-styles.md)

## Quick Rules

- Use lowercase with hyphens for names
- Project features for teams, personal for individual use
- Keep examples simple and minimal
- Test after creation
