# Code Style Plugin

AI code review plugin based on code style principles. Claude directly analyzes code and provides detailed reviews focusing on 5 core principles.

## Features

This plugin reviews code based on these 5 core principles:

1. **Single Responsibility Principle (SRP)** - Functions/classes should have only one responsibility
2. **DRY** - Avoid repeated code and extract common logic
3. **Simplicity First** - Prefer easy-to-understand code over complex abstractions
4. **YAGNI** - Don't implement features not currently needed
5. **Type Safety** - Avoid `any` type and define clear types

Additionally checks:
- Naming conventions (consistency of variables, functions, classes, etc.)
- Code structure and complexity
- Comments and documentation quality

## Installation

```bash
/plugin install code-style-plugin@devstefancho-claude-plugins
```

Restart Claude Code after installation to activate the plugin.

## Usage

### Automatic Usage

Claude automatically uses this skill when you request code reviews:

```
"Can you review this code?"
"Analyze the code quality of this function"
"Suggest ways to improve the code structure"
```

### Explicit Usage

When requesting a code review for a specific file:

```
Use the code-style-reviewer skill to analyze @src/services/userService.ts
```

## Review Items

### Single Responsibility Principle (SRP)
- Does the function/method perform only one task?
- Does the class have only one responsibility?
- Is the function length appropriate? (Recommended: under 20 lines)

### DRY (Don't Repeat Yourself)
- Are there repeated code patterns?
- Can common logic be extracted?
- Are there hardcoded config values?

### Simplicity First
- Are there unnecessary abstractions?
- Is there deep nesting? (Recommended: within 3 levels)
- Is there overly clever code?

### YAGNI (You Aren't Gonna Need It)
- Is there unused code?
- Are there unnecessary features for future use?
- Is there dead code?

### Type Safety (TypeScript)
- Is `any` type used?
- Are function parameters and return types defined?
- Are interfaces used appropriately?

### Naming Conventions
- Are variable names clear and meaningful?
- Do function names start with verbs?
- Is consistent casing used?

## Review Report

Review results are provided in the following format:

```
# Code Style Review Report

## File: [filename]

### Good Points
- [Good practices]

### Critical Issues
- [Issues that must be fixed]

### Warnings
- [Issues that need improvement]

### Suggestions
- [Suggestions worth considering]

## Overall Assessment
- Overall code quality score: [X/10]
- Most important improvements: [Top 3]
```

## Detailed Documentation

Documentation included in the plugin:

- **SKILL.md** - Skill definition and review process
- **PRINCIPLES.md** - Detailed explanation and checklist for each principle
- **EXAMPLES.md** - Bad code vs good code examples

## License

MIT License

## Author

Stefan Cho
