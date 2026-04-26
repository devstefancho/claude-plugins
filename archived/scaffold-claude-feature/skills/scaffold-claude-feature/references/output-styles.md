# Output Styles Reference

Quick reference for creating custom output styles.

## Structure

Markdown file with frontmatter:
```markdown
---
name: My Style
description: Brief description shown in UI
keep-coding-instructions: false
---

# Custom Style Instructions

Your custom system prompt additions here.
Define how Claude should behave in this style.
```

## Location

- Project: `.claude/output-styles/style-name.md`
- Personal: `~/.claude/output-styles/style-name.md`

## Key Fields

- `name` - Display name (optional, defaults to filename)
- `description` - Shown in `/output-style` menu
- `keep-coding-instructions` - Keep Claude's coding instructions (default: false)

## Activation

- `/output-style` - Open menu to select
- `/output-style style-name` - Switch directly
- Saved in `.claude/settings.local.json`

## How It Works

Output styles modify the system prompt:
- Removes efficiency instructions (concise output)
- Removes coding instructions (unless keep-coding-instructions: true)
- Adds your custom instructions

## Simple Examples

**Teacher mode:**
```markdown
---
name: Teacher
description: Educational mode with explanations
keep-coding-instructions: true
---

# Teacher Mode

You help users learn while coding.

Behavior:
- Explain your reasoning
- Share insights between tasks
- Ask questions to check understanding
- Encourage hands-on practice
```

**Formal mode:**
```markdown
---
name: Formal
description: Professional, detailed responses
---

# Formal Mode

You provide formal, professional assistance.

Style:
- Use formal language
- Provide detailed explanations
- Structure responses clearly
- Include relevant references
```

**Quick mode:**
```markdown
---
name: Quick
description: Minimal, direct responses
keep-coding-instructions: true
---

# Quick Mode

Provide minimal, direct responses.

- Short answers
- Code only when needed
- No extra explanations
```

## Tips

- Set `keep-coding-instructions: true` for coding tasks
- Clear behavior guidelines work best
- Test with different request types
- Use for non-coding tasks (research, writing, etc.)

## Built-in Styles

- **Default** - Standard software engineering
- **Explanatory** - Adds educational insights
- **Learning** - Collaborative learn-by-doing

## Comparison

- **Output Styles** - Change system prompt, affect all responses
- **CLAUDE.md** - Add context, doesn't change system prompt
- **Subagents** - Separate tasks, own context
- **Slash Commands** - Reusable prompts
