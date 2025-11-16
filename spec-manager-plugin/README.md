# Spec Manager Plugin

Manage specification files for spec-driven development workflow.

## Features

- **Structured Specs** - Organize specs in `specs/{scope}/{work-name}.md`
- **Scope Support** - feat, fix, docs, refactor, chore
- **XML Tag Format** - Consistent structure for each scope type
- **Duplicate Detection** - Checks for similar existing specs

## Installation

```bash
/plugin install spec-manager-plugin@devstefancho-claude-plugins
```

## Usage

The skill is invoked when creating, updating, or deleting spec files:

- "Create a spec for user authentication feature"
- "Update the login fix spec"
- "List all specs"

## Directory Structure

```
specs/
├── feat/        # New features
├── fix/         # Bug fixes
├── docs/        # Documentation
├── refactor/    # Code refactoring
└── chore/       # Maintenance tasks
```

## Principles

1. **One spec = one task** (unless frontend + backend work together)
2. **No "before" sections** - Focus only on desired state
3. **XML tag format** - Varies by scope
4. **Minimal code** - Avoid code in specs

## Templates

Includes templates for each scope type with appropriate XML tags.
