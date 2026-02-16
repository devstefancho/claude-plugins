---
name: git-worktree
description: Manage git worktrees for parallel branch work. PROACTIVELY USE when user mentions working on a PR, new feature, or new task - ask if they want to create a worktree BEFORE starting implementation.
allowed-tools: Bash, AskUserQuestion
context: fork
agent: general-purpose
---

# Git Worktree Manager

## Overview

| Workflow | Trigger | Scripts |
|----------|---------|---------|
| A. Create Worktree | PR/새 기능 작업 언급 | detect.sh → create-worktree.sh |
| B-1. Bare Clone | 새 프로젝트 세팅 요청 | bare-clone.sh |
| B-2. Convert to Bare | bare 전환 요청 | detect.sh → convert-to-bare.sh |
| C. Cleanup | worktree 정리 요청 | cleanup-worktree.sh |

## PLUGIN_DIR Resolution

All scripts are located in the plugin's `scripts/` directory. Resolve the path:

```bash
# Find the plugin's scripts directory
PLUGIN_DIR=$(dirname "$(find ~/.claude -path "*/git-worktree-plugin/*/scripts/detect.sh" 2>/dev/null | head -1)")/..
```

If the above fails (e.g., local development), fall back to the repository root where this SKILL.md is located.

## Proactive Usage Triggers

When the user mentions any of these, IMMEDIATELY ask if they want to create a new worktree:
- Working on a PR (e.g., "Let's work on PR #9", "work on PR #123")
- Starting a new feature/task (e.g., "implement new feature", "handle issue")
- Implementing something new while on main branch

**Ask BEFORE proceeding with implementation work.**

## Detection (Run before all workflows)

```bash
source "$PLUGIN_DIR/scripts/detect.sh"
# Sets: WORKTREE_STYLE ("bare"|"normal"|"none"), WORKTREE_ROOT, PROJECT_ROOT
```

## Workflow Selection (Manual Trigger)

After detection, use AskUserQuestion to let the user choose a workflow. Filter options based on `WORKTREE_STYLE`:

| WORKTREE_STYLE | Available Options |
|----------------|-------------------|
| `bare` | Create Worktree, Cleanup, Bare Clone |
| `normal` | Create Worktree, Convert to Bare, Cleanup, Bare Clone |
| `none` | Bare Clone only |

```
Question: "어떤 작업을 하시겠습니까?"
Header: "Workflow"
Options: (filtered by WORKTREE_STYLE)
- "Create Worktree" - PR 체크아웃 또는 새 브랜치로 worktree 생성
- "Convert to Bare" - 현재 repo를 bare 구조로 변환
- "Cleanup" - 불필요한 worktree 제거
- "Bare Clone" - 새 프로젝트를 bare repo로 clone
```

Then proceed to the selected workflow section below.

## Workflow A: Create Worktree

### Step 1: Detect repo type
Run detection (above). If WORKTREE_STYLE is "none", inform user they're not in a git repository.

### Step 2: Determine creation type
Use AskUserQuestion:
```
Question: "How would you like to create the worktree?"
Header: "Type"
Options:
- "Checkout PR" - Create worktree from existing PR
- "New branch" - Create worktree with new branch
```

### Step 3a: PR Checkout (if "Checkout PR")
Ask for PR number, then run:
```bash
bash "$PLUGIN_DIR/scripts/create-worktree.sh" \
  --project-root "$PROJECT_ROOT" \
  --worktree-root "$WORKTREE_ROOT" \
  --pr {NUMBER}
```

### Step 3b: New Branch (if "New branch")
Use AskUserQuestion for prefix, feature name, and base branch:

**Prefix:**
```
Question: "Select a branch prefix"
Header: "Prefix"
Options:
- "feat" - New feature
- "fix" - Bug fix
- "chore" - Maintenance
- "refactor" - Code refactoring
```

**Feature Name:** Ask user to describe briefly. Format: lowercase, spaces/underscores → dashes.

**Base Branch:**
```
Question: "Select base branch"
Header: "Base"
Options:
- "origin/main (Recommended)" - Main branch
- "origin/develop" - Development branch
```

Then run:
```bash
bash "$PLUGIN_DIR/scripts/create-worktree.sh" \
  --project-root "$PROJECT_ROOT" \
  --worktree-root "$WORKTREE_ROOT" \
  --branch "{prefix}/{feature-name}" \
  --base "origin/{base}"
```

### Step 4: Set Remote Tracking (optional)
Use AskUserQuestion:
```
Question: "Push branch to remote and set tracking?"
Header: "Remote"
Options:
- "Yes (Recommended)" - Push and set upstream
- "No" - Keep local only
```

If "Yes": `cd {worktree-path} && git push -u origin {branch-name}`

### Step 5: Open in tmux + Create CLAUDE.local.md

After worktree creation, open a new tmux window with claude auto-started.

**PR Checkout:**
```bash
# Get PR info for context
PR_INFO=$(gh pr view {NUMBER} --json title,body --jq '"PR #\(.number // "{NUMBER}"): \(.title)\n\n\(.body)"' 2>/dev/null || echo "PR #{NUMBER}")

bash "$PLUGIN_DIR/scripts/open-in-tmux.sh" \
  --path "{worktree-path}" \
  --name "pr-{NUMBER}" \
  --context "$PR_INFO"
```

**New Branch:**
```bash
bash "$PLUGIN_DIR/scripts/open-in-tmux.sh" \
  --path "{worktree-path}" \
  --name "{dir-name}" \
  --context "Branch: {branch}, Base: {base}
Feature: {user's feature description}"
```

The script:
- Creates `CLAUDE.local.md` with task context so Claude Code understands the work
- If inside tmux (`$TMUX` set): opens new window named after branch/PR, runs `claude`
- If not in tmux: prints the worktree path only

## Workflow B-1: Bare Clone

Use AskUserQuestion to collect URL and path, then run:
```bash
bash "$PLUGIN_DIR/scripts/bare-clone.sh" \
  --url "{URL}" \
  --path "{PATH}" \
  --branch "main"
```

## Workflow B-2: Convert to Bare

### Step 1: Detect and confirm
Run detection. If WORKTREE_STYLE is already "bare", inform user it's already a bare repo.

Use AskUserQuestion:
```
Question: "Convert this repository to bare structure? A backup will be created at .git-backup/"
Header: "Convert"
Options:
- "Proceed" - Convert to bare (backup included)
- "Cancel" - Abort
```

### Step 2: Execute
```bash
bash "$PLUGIN_DIR/scripts/convert-to-bare.sh" --project-root "$PROJECT_ROOT"
```

※ Failure triggers automatic rollback. Backup is kept at `.git-backup/`.

## Workflow C: Cleanup

### Step 1: List worktrees
```bash
git -C "$PROJECT_ROOT" worktree list
```

### Step 2: Select target
Use AskUserQuestion to ask which worktree(s) to remove.

### Step 3: Execute
```bash
# Single worktree
bash "$PLUGIN_DIR/scripts/cleanup-worktree.sh" \
  --project-root "$PROJECT_ROOT" \
  --path "{WORKTREE_PATH}"

# All worktrees
bash "$PLUGIN_DIR/scripts/cleanup-worktree.sh" \
  --project-root "$PROJECT_ROOT" \
  --all
```

## Format Rules

- Feature names: lowercase, spaces/underscores → dashes
- Branch format: `{prefix}/{feature-name}` (e.g., `feat/user-authentication`)
- PR format: `pr-{number}` (e.g., `pr-123`)
- Worktree path: `./trees/{branch-name}` (customizable)
