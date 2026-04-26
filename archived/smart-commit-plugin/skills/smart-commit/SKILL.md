---
name: smart-commit
description: >
  Split uncommitted working tree changes into logical, ordered commits
  by analyzing Claude Code session history. Use when user asks to split commits,
  organize commits from session, auto-commit by feature, or says
  "커밋 나눠줘", "커밋 분리", "세션 기반 커밋".
---

# Smart Commit

Analyze the current Claude Code session history and split uncommitted changes into logical commit groups.

## CRITICAL: Execution Rules

**MUST DO:**
- Run `python scripts/parse-session.py` for session data extraction
- Run `python scripts/analyze-commits.py` for commit group analysis
- Wait for complete script output before proceeding
- Use AskUserQuestion before executing each commit
- Use TaskCreate for commit execution workflow

**NEVER DO:**
- Parse `~/.claude/projects/` JSONL files directly with Bash/jq/Read
- Commit without user confirmation
- Modify or checkout files to split commits (only use `git add` for staging)
- Reorder file history or manipulate working tree state

**WHY:** Session JSONL files have complex nested structures with tool calls, snapshots, and message threading. The Python scripts handle this reliably. Overlapping files are auto-merged by the analysis script, so no file manipulation is needed.

## Workflow

### Phase 1: Pre-flight Check

```bash
git status --porcelain
```

- If output is empty → tell user "No uncommitted changes found" and stop
- If changes exist → proceed to Phase 2
- Also run `git diff --stat` to show a summary of changes

### Phase 2: Session Data Extraction

Run the parse-session script from the plugin's skill directory:

```bash
python <plugin-skill-dir>/scripts/parse-session.py --project "$(pwd)"
```

The script outputs JSON to stdout with:
- `session_id`: Current session identifier
- `project_path`: Working project path
- `user_messages`: List of user messages with timestamps
- `file_ops`: List of file edit/write operations with timestamps and paths
- `snapshots`: File history snapshot mappings

**On error:** Script prints `[ERROR]` and `[HINT]` to stderr. Show these to user.

### Phase 3: Commit Group Analysis

Pipe or pass the session data to the analysis script:

```bash
python <plugin-skill-dir>/scripts/analyze-commits.py --session-data <temp-json-path>
```

Or via stdin:

```bash
python <plugin-skill-dir>/scripts/parse-session.py --project "$(pwd)" | \
  python <plugin-skill-dir>/scripts/analyze-commits.py
```

The script outputs JSON with:
- `commit_groups`: Ordered list of commit groups, each with index, type, message, files, user_context
- `merged_groups`: Info about groups that were merged due to overlapping files
- `summary`: Total groups count and merge statistics

**Important:** Overlapping files (same file in multiple groups) are automatically merged into a single group by the script. This means every file appears in exactly one group → simple `git add` per group is safe.

### Phase 4: Present Commit Plan

Show the user a formatted commit plan:

```
Commit Plan (N commits):

1. feat: Add user authentication
   Files: src/auth.ts (new), src/middleware.ts (modified)
   Context: "사용자 인증 기능 추가해줘"

2. fix: Fix validation error handling
   Files: src/validator.ts (modified)
   Context: "에러 처리 고쳐줘"

[Merged: Groups 2,3 combined due to shared file src/middleware.ts]
```

Then use AskUserQuestion:
- "Execute all commits as planned" (Recommended)
- "Let me review each commit individually"
- "Cancel"

If cancelled → stop. Otherwise proceed to Phase 5.

### Phase 5: Execute Commits via TaskCreate

Create a Task for each commit group and execute sequentially.

For detailed TaskCreate workflow, blocking dependencies, and per-commit confirmation logic, see:
[commit-execution.md](references/commit-execution.md)

**Quick summary:**
1. Create all Tasks with blockedBy dependencies for ordering
2. For each Task: confirm with user → `git add <files>` → `git commit`
3. Last commit includes any remaining unstaged changes
4. Skipped commits' files roll into the next commit

### Phase 6: Result Report

After all commits are done:

```bash
git log --oneline -N  # N = number of commits created
git status
```

Show:
- List of commits created with their hashes
- Any remaining uncommitted changes
- Total commits: X created, Y skipped

## Error Handling

| Issue | Cause | Solution |
|-------|-------|----------|
| "No session found" | No recent session for project | Use `--session <id>` to specify manually |
| "No file operations" | Session has no edits | Nothing to commit, inform user |
| Script not found | Wrong working directory | Ensure plugin is installed correctly |
| Git conflicts | Staging issues | Run `git status` and show user |
| Empty commit group | All files in group already committed | Skip and continue |

If a Python script fails:
1. Show the stderr output to the user
2. Verify `~/.claude/` directory exists and has session data
3. Check Python 3 is available
4. Suggest `--verbose` flag for detailed diagnostics

## Script CLI Reference

### parse-session.py

| Option | Description |
|--------|-------------|
| `--project <path>` | Project directory path (auto-detects latest session) |
| `--session <id>` | Specific session ID to parse |
| `--verbose` | Print detailed parsing log to stderr |

### analyze-commits.py

| Option | Description |
|--------|-------------|
| `--session-data <path>` | Path to JSON from parse-session.py (or use stdin) |
| `--verbose` | Print boundary decision reasoning to stderr |
