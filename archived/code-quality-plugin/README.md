# Code Quality Plugin

Comprehensive code quality review skill for Claude Code. Provides systematic review of code based on DRY (Don't Repeat Yourself), KISS (Keep It Simple, Stupid), and CLEAN CODE (Easy to Read) principles.

## Installation

```bash
/plugin install code-quality-plugin@devstefancho-claude-plugins
```

## Features

The Code Quality Reviewer skill automatically activates when you:

- Request code review or quality assessment
- Ask for feedback on code changes
- Question code complexity or readability
- Review pull requests or commits
- Request refactoring suggestions
- Ask about code maintainability

## Quick Start

Ask Claude for a code quality review:

```
"Can you review this code for quality issues?"
"Is there any unnecessary duplication in this function?"
"How can I simplify this complex logic?"
"Review my changes for code quality."
```

## What Gets Reviewed

The skill provides systematic review across three core principles:

### DRY (Don't Repeat Yourself)
- Identifies duplicated code that should be consolidated
- Detects repeated patterns and suggests extraction
- Finds opportunities to reuse existing functions
- Checks for consistent error handling

### KISS (Keep It Simple, Stupid)
- Detects overly complex logic
- Identifies unnecessary abstractions
- Suggests simplifications
- Flags functions with too many parameters

### CLEAN CODE (Easy to Read)
- Evaluates variable and function naming clarity
- Checks for self-documenting code
- Identifies magic values needing explanation
- Verifies logical code organization

## Review Output Format

The skill provides structured feedback including:

- **Critical Issues** (🔴) - Must be addressed
- **Moderate Issues** (🟡) - Should be addressed
- **Minor Issues** (🟢) - Optional improvements
- **Positive Observations** (✅) - What was done well
- **Summary** - Overall assessment and key recommendations

Each finding includes:
- Specific file paths and line numbers
- Clear explanation of the issue
- Example of the problematic code pattern
- Suggested improvement

## Examples

### Example: Code Review Request

**Your request:**
```
"Review this authentication module for code quality."
```

**Response includes:**
- Duplicate validation logic (DRY)
- Overly nested conditions (KISS)
- Unclear variable names (CLEAN CODE)
- Recommendations for improvement
- Refactored code examples

### Example: Refactoring Validation

**Your request:**
```
"Is this refactoring approach sound?"
```

**Response includes:**
- Assessment of changes against quality principles
- Confirmation if simplification improves maintainability
- Additional optimization suggestions if applicable

## Documentation

### SKILL.md
Main skill definition with:
- Overview of quality principles
- Review process and checklist
- Output format specification
- Usage scenarios

### PRINCIPLES.md
Detailed reference covering:
- **DRY Principle** - Why it matters, violation patterns, how to fix
- **KISS Principle** - Why it matters, violation patterns, how to fix
- **CLEAN CODE Principle** - Why it matters, violation patterns, how to fix
- Assessment guidelines for prioritizing issues

### EXAMPLES.md
Real-world code examples:
- User Authentication Module
- E-commerce Order Processing
- Data Validation Utilities
- API Response Handling

Each example shows:
- ❌ Before (with quality issues)
- ✅ After (improved version)
- Specific improvements made

## Skill Permissions

This skill uses read-only tools:
- **Read** - View file contents
- **Grep** - Search within files
- **Glob** - Find files by pattern

The skill cannot modify files or make changes to your code.

## Best Practices for Code Review

1. **Ask for specific focus** - "Review for DRY violations" or "Check complexity"
2. **Provide context** - Share related files if cross-file patterns matter
3. **Use for PRs** - Request review before merging changes
4. **Learn from feedback** - Use examples to improve coding style
5. **Apply gradually** - Don't feel obligated to fix every suggestion

## Related Commands

- **Use with style review** - Combine with code-style-reviewer for comprehensive review
- **Use with refactoring** - Request refactoring then review the result
- **Use in PR process** - Review code quality before merging

## Tips

- The skill focuses on maintainability and readability, not formatting
- It applies to all code: features, bug fixes, refactoring, and chores
- Complex logic suggestions aim to improve understanding, not reduce functionality
- Duplication detection considers both exact and semantic duplication

## Feedback

To report issues or suggest improvements to this skill:

1. Check the [PRINCIPLES.md](skills/code-quality-reviewer/PRINCIPLES.md) for detailed guidelines
2. Review [EXAMPLES.md](skills/code-quality-reviewer/EXAMPLES.md) for common patterns
3. Report issues at https://github.com/anthropics/claude-code/issues

## Version

Current version: 1.0.0

## See Also

- **Claude Code Skills Documentation** - https://docs.claude.com/en/docs/claude-code/agent-skills
- **Code Style Plugin** - For code style and naming convention reviews
- **SKILL.md** - Complete skill reference in the plugin directory
