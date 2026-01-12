---
name: git-worktree
description: Manage git worktrees for parallel branch work. PROACTIVELY USE when user mentions working on a PR, new feature, or new task - ask if they want to create a worktree BEFORE starting implementation.
allowed-tools: Bash, AskUserQuestion
---

# Git Worktree Manager

## Proactive Usage Triggers

When the user mentions any of these, IMMEDIATELY ask if they want to create a new worktree:
- Working on a PR (e.g., "Let's work on PR #9", "work on PR #123")
- Starting a new feature/task (e.g., "implement new feature", "handle issue")
- Implementing something new while on main branch

**Ask BEFORE proceeding with implementation work.**

## Create Worktree

### Step 1: Fetch and Determine Creation Type

Run `git fetch` to update remote refs, then use AskUserQuestion:

```
Question: "How would you like to create the worktree?"
Header: "Type"
Options:
- "Checkout PR" - Create worktree from existing PR
- "New branch" - Create worktree with new branch
```

### Step 2a: PR Checkout (if "Checkout PR" selected)

Ask for PR number, then:
- Run `gh pr checkout {pr-number}` in `./trees/pr-{number}/`
- Skip to Step 6 (Worktree Path)

### Step 2b: Branch Prefix (if "New branch" selected)

Use AskUserQuestion:

```
Question: "Select a branch prefix"
Header: "Prefix"
Options:
- "feat" - New feature
- "fix" - Bug fix
- "chore" - Maintenance
- "refactor" - Code refactoring
```

Note: User can select "Other" for custom prefix (e.g., docs, test, build)

### Step 3: Feature Name

Ask user to describe the feature briefly. Format the name:
- Convert to lowercase
- Replace spaces/underscores with dashes
- Final format: `{prefix}/{feature-name}` (e.g., `feat/user-authentication`)

### Step 4: Base Branch

Use AskUserQuestion:

```
Question: "Select base branch"
Header: "Base"
Options:
- "main (Recommended)" - Main branch
- "develop" - Development branch
```

Note: User can select "Other" for custom base branch

### Step 5: Worktree Path

Use AskUserQuestion:

```
Question: "Select worktree directory"
Header: "Path"
Options:
- "./trees/{branch-name} (Recommended)" - Default location in trees folder
```

Note: User can select "Other" for custom path

### Step 6: Create Worktree

1. Check if worktree path exists:
   - If exists, use AskUserQuestion:
     ```
     Question: "Worktree already exists. What would you like to do?"
     Header: "Conflict"
     Options:
     - "Remove and recreate" - Delete existing and create new
     - "Cancel" - Abort operation
     ```
   - If "Remove and recreate": run `git worktree remove {path} --force` then `git branch -D {branch-name}` (ignore errors)

2. Create worktree: `git worktree add {path} -b {branch-name} origin/{base-branch}`

### Step 7: Set Remote Tracking

Use AskUserQuestion:

```
Question: "Push branch to remote and set tracking?"
Header: "Remote"
Options:
- "Yes (Recommended)" - Push and set upstream to origin/{branch-name}
- "No" - Keep local only for now
```

If "Yes":
1. Change to worktree: `cd {path}`
2. Push with upstream: `git push -u origin {branch-name}`

This ensures proper tracking: `{branch-name}` → `origin/{branch-name}` (instead of tracking the base branch)

## Cleanup Worktree

1. List worktrees: `git worktree list`
2. Use AskUserQuestion to ask which to remove:
   ```
   Question: "Which worktree would you like to remove?"
   Header: "Remove"
   Options:
   - List each worktree in ./trees/
   - "All" - Remove all worktrees
   ```
3. For each selected worktree:
   - `git worktree remove {path} --force`
   - `git branch -D {branch-name}` (ignore errors)

## Format Rules

- Feature names: lowercase, spaces/underscores → dashes
- Branch format: `{prefix}/{feature-name}` (e.g., `feat/user-authentication`)
- PR format: `pr-{number}` (e.g., `pr-123`)
- Worktree path: `./trees/{branch-name}` (customizable)
