# Skills Reference

Quick reference for creating agent skills.

## Structure

```
my-skill/
├── SKILL.md (required)
├── reference.md (optional)
├── examples.md (optional)
├── scripts/
│   └── helper.py
└── templates/
    └── template.txt
```

## Location

- Project: `.claude/skills/skill-name/`
- Personal: `~/.claude/skills/skill-name/`

## SKILL.md Format

```markdown
---
name: my-skill-name
description: What it does and when to use it. Include trigger keywords.
allowed-tools: Read, Write, Bash
---

# My Skill

## Instructions

1. Clear step-by-step guidance
2. What to do and how

## Examples

Simple, minimal examples
```

## Description Tips

Include WHEN to use:
- ✅ "Extract PDF text. Use when working with PDF files."
- ❌ "Extract PDF text."

## Tool Access

- Omit `allowed-tools` → inherit all tools
- Specify tools → restrict access (e.g., read-only: `Read, Grep, Glob`)

## Progressive Disclosure

Reference other files:
```markdown
For advanced usage, see [reference.md](reference.md)
Run helper: `python scripts/helper.py`
```

Claude loads files only when needed.

## Simple Examples

**Code reviewer:**
```markdown
---
name: code-reviewer
description: Review code quality. Use after writing or modifying code.
allowed-tools: Read, Grep, Glob
---

# Code Reviewer

## Checklist
- Readable code
- Error handling
- No duplicated code
- Security issues

Review and provide specific feedback.
```

**Commit helper:**
```markdown
---
name: commit-helper
description: Generate commit messages. Use when staging commits.
allowed-tools: Bash(git diff:*), Bash(git status:*)
---

# Commit Helper

## Instructions
1. Run `git diff --staged`
2. Generate clear commit message:
   - Summary under 50 chars
   - Present tense
   - Explain what and why
```

## Tips

- One skill = one focused capability
- Clear, specific descriptions
- Simple instructions
- Test with relevant requests
