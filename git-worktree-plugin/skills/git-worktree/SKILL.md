---
name: git-worktree
description: Manage git worktrees for parallel branch work. PROACTIVELY USE when user mentions working on a PR, new feature, or new task - ask if they want to create a worktree BEFORE starting implementation.
---

# Git Worktree Manager

## Proactive Usage Triggers

When the user mentions any of these, IMMEDIATELY ask if they want to create a new worktree:
- Working on a PR (e.g., "PR #9 작업하자", "work on PR #123")
- Starting a new feature/task (e.g., "새 기능 구현", "이슈 처리")
- Implementing something new while on main branch

**Ask BEFORE proceeding with implementation work.**

## Create Worktree

1. Run `git fetch` to update remote refs
2. Determine branch name:
   - If PR number provided: use `gh pr checkout {pr-number}` in `./trees/pr-{number}/`
   - If feature name provided: ask for prefix (feat/fix/bug/chore/docs/test), format as `{prefix}/{lowercase-with-dashes}`
   - If no name: ask user for feature description, then ask for prefix
3. Ask for base branch (default: `main`)
4. Check if `./trees/{branch-name}` exists:
   - If exists: ask user "Worktree exists. Remove and recreate? (yes/no)"
   - If yes: run `git worktree remove ./trees/{branch-name} --force` then `git branch -D {branch-name}` (ignore errors)
5. Create worktree: `git worktree add ./trees/{branch-name} -b {branch-name} origin/{base-branch}`

## Cleanup Worktree

1. List worktrees: `git worktree list`
2. Ask user which to remove (or "all")
3. For each worktree in `./trees/`:
   - `git worktree remove {path} --force`
   - `git branch -D {branch-name}` (ignore errors)

## Format Rules

- Feature names: lowercase, spaces/underscores → dashes
- Branch format: `{prefix}/{feature-name}` (e.g., `feat/user-authentication`)
- PR format: `pr-{number}` (e.g., `pr-123`)
- Worktree path: `./trees/{branch-name}`
