# Commit Execution Workflow

Detailed guide for Phase 5 of the Smart Commit skill — executing commits via TaskCreate.

## Task Creation

For each `commit_group` from analyze-commits.py output, create a Task:

```
TaskCreate:
  subject: "Commit {index}: {type}: {message}"
  description: |
    Files: {file list with change types}
    User context: {user_context}
    Type: {type}
    Message: {message}
  activeForm: "Committing: {type}: {message}"
```

After creating all Tasks, set up sequential dependencies:

```
TaskUpdate(task_2, addBlockedBy: [task_1])
TaskUpdate(task_3, addBlockedBy: [task_2])
...
```

This ensures commits execute in chronological order.

## Per-Task Execution

For each Task (in order):

### 1. Mark In Progress

```
TaskUpdate(taskId, status: "in_progress")
```

### 2. Confirm with User

If user chose "review each commit individually" in Phase 4, use AskUserQuestion:

```
Commit {index}/{total}: {type}: {message}
Files: {file list}

Options:
- "Execute" (Recommended)
- "Skip this commit"
- "Edit commit message"
```

If user chose "Execute all" in Phase 4, skip individual confirmation.

### 3. Execute Commit

On **Execute**:

```bash
git add file1.ts file2.ts file3.ts
git commit -m "{type}: {message}"
```

On **Skip**:
- Mark Task as completed with note "skipped"
- The files from this group remain unstaged
- They will be picked up by the next commit or remain uncommitted

On **Edit message**:
- Ask user for new message
- Execute with updated message

### 4. Mark Complete

```
TaskUpdate(taskId, status: "completed")
```

## Last Commit Handling

For the final commit group, after staging its own files, also check for any remaining changes:

```bash
git status --porcelain
```

If there are remaining unstaged changes (from skipped commits or untracked operations):
- Ask user: "There are N remaining changed files. Include them in this last commit?"
- If yes: `git add` those files too before committing
- If no: Leave them uncommitted

## Commit Message Format

Follow Conventional Commits:

```
{type}: {message}
```

Types determined by analyze-commits.py:
- `feat`: New feature/functionality
- `fix`: Bug fix
- `refactor`: Code restructuring
- `style`: Formatting, whitespace
- `docs`: Documentation changes
- `test`: Test additions/modifications
- `chore`: Build, config, tooling changes

## Edge Cases

### All Commits Skipped
If user skips every commit, show:
```
All commits were skipped. Your changes remain uncommitted.
```

### Single Commit Group
If analysis produces only one group, skip TaskCreate overhead:
- Show the plan directly
- Confirm and execute as a single commit

### Empty File List After Staging
If `git add` results in nothing staged (files already committed or reverted):
```bash
git diff --cached --stat
```
If empty, skip this commit and inform user.

### Git Add Failure
If `git add` fails for any file:
1. Show the error to user
2. Ask whether to continue without that file or abort
3. Never force-add or ignore errors silently
