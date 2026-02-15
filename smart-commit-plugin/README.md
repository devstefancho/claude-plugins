# Smart Commit Plugin

Analyze Claude Code session history to split uncommitted changes into logical commits.

## Features

- Parse current session's conversation to understand what was built
- Automatically group file changes by user intent and topic boundaries
- Merge overlapping file groups for safe, conflict-free commits
- Present commit plan for user review before execution
- Execute commits sequentially via TaskCreate workflow

## Installation

```bash
/plugin install smart-commit-plugin@devstefancho-claude-plugins
```

## Usage

Trigger the skill with natural language:

```
커밋 나눠줘
커밋 분리해줘
세션 기반으로 커밋 정리해줘
Split my commits by feature
Organize my uncommitted changes into commits
```

## How It Works

1. **Pre-flight**: Checks for uncommitted changes via `git status`
2. **Session Parsing**: Reads the current session's JSONL to extract file operations and user messages
3. **Commit Analysis**: Groups changes by user intent boundaries, time gaps, and topic changes. Automatically merges groups with overlapping files
4. **Plan Review**: Presents a formatted commit plan for user approval
5. **Execution**: Creates Tasks for each commit, executes sequentially with user confirmation
6. **Report**: Shows git log of created commits

## Commit Plan Example

```
Commit Plan (3 commits):

1. feat: Add user authentication
   Files: src/auth.ts (new), src/middleware.ts (modified)

2. fix: Fix validation error handling
   Files: src/validator.ts (modified)

3. chore: Update configuration
   Files: config.json (modified), .env.example (new)
```

## Script CLI

### parse-session.py

```bash
# Auto-detect latest session for current project
python scripts/parse-session.py --project "$(pwd)"

# Specific session
python scripts/parse-session.py --session abc12345-...

# Verbose logging
python scripts/parse-session.py --project "$(pwd)" --verbose
```

### analyze-commits.py

```bash
# From file
python scripts/analyze-commits.py --session-data /tmp/session.json

# Via pipe
python parse-session.py --project "$(pwd)" | python analyze-commits.py

# Verbose
python scripts/analyze-commits.py --session-data /tmp/session.json --verbose
```

## Limitations

- Requires an active Claude Code session with file edit history
- Only analyzes the current (most recent) session by default
- File operations outside the project directory are excluded
- Overlapping file groups are merged (cannot split changes within a single file across commits)

## See Also

- [SKILL.md](skills/smart-commit/SKILL.md) - Skill definition
- [commit-execution.md](skills/smart-commit/references/commit-execution.md) - Commit execution workflow
