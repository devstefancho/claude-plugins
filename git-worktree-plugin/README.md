# Git Worktree Plugin

Manage git worktrees for parallel branch work.

## Features

- **Proactive Suggestions** - Automatically suggests creating worktrees when working on PRs or new features
- **Easy Creation** - Creates worktrees with proper branch naming conventions
- **Cleanup Management** - Lists and removes worktrees safely

## Installation

```bash
/plugin install git-worktree-plugin@devstefancho-claude-plugins
```

## Usage

The skill is proactively invoked when you mention:
- Working on a PR (e.g., "Let's work on PR #9", "work on PR #123")
- Starting a new feature/task
- Implementing something while on main branch

## Worktree Structure

```
./trees/{branch-name}/
```

Branch naming:
- PR: `pr-{number}` (e.g., `pr-123`)
- Features: `{prefix}/{feature-name}` (e.g., `feat/user-authentication`)

Prefixes: feat, fix, bug, chore, docs, test
