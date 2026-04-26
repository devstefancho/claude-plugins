# Simple SDD Plugin

Simple SDD (Software Specification & Design) workflow commands for generating specifications, plans, tasks, and implementations through a 4-step process.

## Installation

```bash
/plugin marketplace add .
/plugin install simple-sdd-plugin@devstefancho-claude-plugins
```

## Commands

| Command | Description |
|---------|-------------|
| `/simple-sdd/spec [requirements]` | Generate a specification document |
| `/simple-sdd/plan [tech-stack]` | Generate a technical implementation plan |
| `/simple-sdd/tasks [context]` | Generate atomic implementation tasks |
| `/simple-sdd/implement [--all]` | Execute tasks (batch or incremental) |

## How It Works

1. **Spec** - Create a comprehensive specification with user stories, requirements, and success criteria
2. **Plan** - Generate a technical plan with architecture, data models, API design, and testing strategy
3. **Tasks** - Break the plan into atomic tasks (ID: T-001, T-002...) with dependencies
4. **Implement** - Execute tasks incrementally (with user approval per group) or all at once with `--all`

## Output Structure

```
docs/
├── spec-init.md      # Specification document
├── plan-init.md      # Technical implementation plan
└── tasks-init.md     # Atomic implementation tasks
```

## Usage Example

```
/simple-sdd/spec Build a user authentication system with OAuth support
/simple-sdd/plan React + Node.js + PostgreSQL
/simple-sdd/tasks
/simple-sdd/implement --all
```
