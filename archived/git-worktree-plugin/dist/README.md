# Git Worktree Plugin v2.0

Manage git worktrees for parallel branch work with shell script automation.

## Features

- **Proactive Suggestions** - Automatically suggests creating worktrees when working on PRs or new features
- **Bare Repository Support** - Clone as bare or convert existing repos for optimal worktree workflow
- **Backup & Rollback** - Safe bare conversion with automatic backup and rollback on failure
- **Shell Script Based** - Reliable execution via tested shell scripts instead of inline commands
- **Cleanup Management** - Remove worktrees and associated branches safely

## Installation

```bash
/plugin install git-worktree-plugin@devstefancho-claude-plugins
```

Or install via npx:
```bash
npx @anthropic-ai/claude-code@latest /plugin install git-worktree-plugin@devstefancho-claude-plugins
```

## Workflows

### A. Create Worktree

The skill is proactively invoked when you mention:
- Working on a PR (e.g., "Let's work on PR #9")
- Starting a new feature/task
- Implementing something while on main branch

Supports both **PR checkout** and **new branch** modes.

### B-1. Bare Clone (New Project)

Set up a new project with bare repository structure:

```
project-name/
├── .bare/              # Bare git repository
├── .git                # File pointing to .bare
└── trees/
    └── main/           # Initial worktree
```

### B-2. Convert to Bare (Existing Project)

Convert an existing clone to bare structure:
- Backs up `.git` to `.git-backup/` before conversion
- Automatic rollback on any failure
- Preserves all commit history and branches

### C. Cleanup

Remove worktrees individually or all at once, with associated branch cleanup.

## Worktree Structure

```
./trees/{branch-name}/
```

Branch naming:
- PR: `pr-{number}` (e.g., `pr-123`)
- Features: `{prefix}/{feature-name}` (e.g., `feat/user-authentication`)

Prefixes: feat, fix, chore, refactor, docs, test

## Scripts

All operations are implemented as shell scripts in `scripts/`:

| Script | Purpose |
|--------|---------|
| `detect.sh` | Detect repo type (bare/normal/none) |
| `create-worktree.sh` | Create worktree with branch or PR |
| `bare-clone.sh` | Clone repo as bare with worktree structure |
| `convert-to-bare.sh` | Convert existing clone to bare (with backup/rollback) |
| `cleanup-worktree.sh` | Remove worktree(s) and branches |

## Testing

```bash
bash tests/run-all.sh
```

Individual tests:
```bash
bash tests/test-detect.sh
bash tests/test-create-worktree.sh
bash tests/test-bare-clone.sh
bash tests/test-convert-to-bare.sh
bash tests/test-cleanup.sh
```
