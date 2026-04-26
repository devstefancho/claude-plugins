# Slash Commands Reference

Quick reference for creating custom slash commands.

## Structure

```markdown
---
description: Brief description
argument-hint: [arg1] [arg2]
allowed-tools: Tool1, Tool2
---

Your command prompt here with $ARGUMENTS or $1, $2, etc.
```

## Location

- Project: `.claude/commands/filename.md` → `/filename`
- Personal: `~/.claude/commands/filename.md` → `/filename`
- Subdirectories: `.claude/commands/subdir/filename.md` → `/filename` (subdir shown in description)

## Arguments

- `$ARGUMENTS` - All arguments as single string
- `$1, $2, $3` - Individual arguments

## File References

Use `@` prefix to reference files:
```
Review @src/app.js for bugs
Compare @old.js with @new.js
```

## Bash Execution

Prefix with `!` to execute bash:
```markdown
---
allowed-tools: Bash(git status:*), Bash(git diff:*)
---

Current status: !`git status`
Recent changes: !`git diff HEAD`
```

## Simple Examples

**Commit helper:**
```markdown
---
description: Create git commit
allowed-tools: Bash(git add:*), Bash(git commit:*)
---

Create a commit for these changes: !`git diff`
```

**Review PR:**
```markdown
---
description: Review pull request
argument-hint: [pr-number]
---

Review PR #$1 focusing on code quality and security.
```

**Fix issue:**
```markdown
---
description: Fix GitHub issue
argument-hint: [issue-number]
---

Fix issue #$ARGUMENTS following our coding standards.
```

## Tips

- Keep descriptions short and clear
- Use `allowed-tools` to pre-approve tools
- Simple prompts work best
- Test with different arguments
