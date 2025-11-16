# Subagents Reference

Quick reference for creating specialized subagents.

## Structure

Single Markdown file:
```markdown
---
name: my-agent
description: What it does. Use proactively when [condition].
tools: Read, Write, Bash
model: sonnet
---

System prompt for this subagent.
Detailed role and approach instructions.
```

## Location

- Project: `.claude/agents/agent-name.md`
- Personal: `~/.claude/agents/agent-name.md`

## Key Fields

- `name` - lowercase-with-hyphens
- `description` - Include "use proactively" for automatic invocation
- `tools` - Optional; omit to inherit all tools
- `model` - Optional: `sonnet`, `opus`, `haiku`, or `inherit`

## Model Selection

- `sonnet` (default) - Balanced capability
- `opus` - Maximum capability
- `haiku` - Fast, cost-effective
- `inherit` - Use main conversation's model

## Invocation

**Automatic:** Claude delegates based on description
**Explicit:** User mentions agent by name

## Simple Examples

**Code reviewer:**
```markdown
---
name: code-reviewer
description: Expert code reviewer. Use proactively after writing code.
tools: Read, Grep, Glob, Bash(git diff:*)
model: inherit
---

You are a senior code reviewer.

When invoked:
1. Run git diff to see changes
2. Review for quality and security
3. Provide specific, actionable feedback

Focus on:
- Readable code
- Error handling
- Security issues
- Performance
```

**Debugger:**
```markdown
---
name: debugger
description: Debug errors and test failures. Use proactively when issues occur.
tools: Read, Edit, Bash, Grep
---

You are an expert debugger.

Process:
1. Capture error message
2. Identify cause
3. Implement minimal fix
4. Verify solution

Provide root cause and fix.
```

**Test runner:**
```markdown
---
name: test-runner
description: Run tests and fix failures. Use proactively after code changes.
---

You run tests and fix failures.

Steps:
1. Run appropriate tests
2. Analyze failures
3. Fix issues
4. Re-run tests
```

## Tips

- Single, clear responsibility per agent
- Include "use proactively" for automatic use
- Limit tools to what's needed
- Test with relevant requests
- Use `/agents` command to manage

## When to Use

- **Subagents** - Separate context, specialized tasks
- **Skills** - Extend capabilities, loaded in main context
