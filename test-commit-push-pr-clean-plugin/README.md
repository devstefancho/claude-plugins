# Test Commit Push PR Clean Plugin

Automate the full workflow of testing, committing, pushing, creating PRs, and cleaning up worktrees after completing feature branch work.

## Features

- **Branch Safety** - Prevents accidental commits to default branches (main/master/develop)
- **Lint & Format** - Runs lint and format checks automatically
- **Test Coverage** - Runs tests targeting 100% coverage (if configured)
- **Smart Commits** - Organizes changes into logical conventional commits
- **Auto Push** - Pushes branch to remote with upstream tracking
- **PR Creation** - Creates PR via `gh pr create` with commit-based title/body
- **Worktree Cleanup** - Removes merged worktrees automatically
- **Skip Support** - Skip specific steps with `--skip` argument

## Installation

```bash
/plugin install test-commit-push-pr-clean-plugin@devstefancho-claude-plugins
```

## Usage

```bash
# Run all steps
/test-commit-push-pr-clean

# Skip specific steps (available keys: lint, test, push, pr, clean)
/test-commit-push-pr-clean --skip pr,clean
/test-commit-push-pr-clean --skip lint,test
```

## Workflow Steps

1. **Branch Check** - Prevents running on main/master/develop
2. **[lint] Lint/Format** - Detects and runs project-specific lint tools
3. **[test] Test Coverage** - Runs tests with coverage if test config is detected
4. **Commit** - Groups changes into logical units with conventional commit messages
5. **[push] Push** - Pushes the branch to origin
6. **[pr] PR Create** - Creates PR targeting the default branch
7. **[clean] Worktree Cleanup** - Finds and removes merged worktrees

## Requirements

- Git repository with remote configured
- `gh` CLI installed (for PR creation)
