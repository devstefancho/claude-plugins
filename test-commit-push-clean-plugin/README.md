# Test Commit Push Clean Plugin

Automate the full workflow of testing, committing, pushing, and cleaning up worktrees after completing feature branch work.

## Features

- **Branch Safety** - Prevents accidental commits to default branches (main/master/develop)
- **Lint & Format** - Runs lint and format checks automatically
- **Test Coverage** - Runs tests targeting 100% coverage (if configured)
- **Smart Commits** - Organizes changes into logical conventional commits
- **Auto Push** - Pushes branch to remote with upstream tracking
- **Worktree Cleanup** - Removes merged worktrees automatically

## Installation

```bash
/plugin install test-commit-push-clean-plugin@devstefancho-claude-plugins
```

## Usage

```bash
/test-commit-push-clean
```

The command will:
1. Check you're NOT on a default branch (safety guard)
2. Run lint/format checks and fix issues
3. Run tests with coverage (if test config exists)
4. Organize and commit changes with conventional commit messages
5. Push to remote
6. Clean up merged worktrees

## Workflow Steps

### 1. Branch Check
Prevents running on main/master/develop. If on a default branch, stops and suggests creating a feature branch.

### 2. Lint/Format
Detects and runs project-specific lint tools (ESLint, Prettier, etc.).

### 3. Test Coverage
Runs tests with coverage if test configuration (Jest, Vitest, etc.) is detected.

### 4. Commit
Groups changes into logical units with conventional commit messages. Asks for user confirmation before committing.

### 5. Push
Pushes the branch to origin, setting upstream if needed.

### 6. Worktree Cleanup
Finds and removes worktrees whose branches have been merged into the default branch.

## Requirements

- Git repository with remote configured
- Node.js project (for lint/test detection)
