---
name: worktrace
description: Extract Claude Code work history and update daily notes. Use when user asks to update daily file with today's work, sync work history, record activities, or generate daily summary from Claude Code history.
---

# Worktrace

Extract today's Claude Code work history from `~/.claude/history.jsonl` and generate a structured markdown summary grouped by project and ticket.

## CRITICAL: Execution Rules

**MUST DO:**
- Run `python scripts/worktrace.py --config config.json`
- Wait for complete script output before summarizing
- Use the Python script for ALL data extraction

**NEVER DO:**
- Parse `~/.claude/history.jsonl` directly with Bash/jq
- Use `find`, `grep`, `cat` to read session files manually
- Proceed without running the Python script first

**WHY:** The script handles complex logic (date filtering, ticket extraction, session lookup) that is error-prone and inefficient when done manually with shell commands. The script is optimized for this task.

## First-time Setup

When `config.json` doesn't exist in the plugin directory:

1. **Ask user for output directory** (use user's preferred language)
   - English: "Please provide the directory path for daily files (e.g., ~/.wiki/work-wiki/daily)"
   - Korean: "daily 파일을 저장할 디렉토리 경로를 알려주세요 (예: ~/.wiki/work-wiki/daily)"

2. **Ask user for ticket patterns** (optional)
   - Default pattern: `[A-Z]+-\d+` (matches PROJ-123 style)
   - Ask if they have custom patterns

3. **Create config.json** with user's answers:
   ```json
   {
     "output_dir": "<user-provided-path>",
     "ticket_patterns": ["[A-Z]+-\\d+"],
     "timezone": "Asia/Seoul"
   }
   ```

## Quick Start

1. Set up config (optional but recommended):
   ```bash
   cp config.example.json config.json
   # Edit config.json to set output_dir
   ```

2. Run with config:
   ```bash
   python scripts/worktrace.py --config config.json
   ```

3. Or run directly with CLI args (overrides config):
   ```bash
   python scripts/worktrace.py --output-dir /path/to/daily
   ```

**Priority**: CLI args > config.json > defaults

## Workflow (Phase-based)

### Phase 0: Configuration Check (First-time only)

```
IF config.json does not exist:
  1. Ask user for output directory path (in user's language)
  2. Ask user for ticket patterns (optional, default: [A-Z]+-\d+)
  3. Create config.json with user's answers
  4. Continue to Phase 1
```

### Phase 1: Data Extraction (MUST use Python script)

```bash
# REQUIRED: Run the Python script
python scripts/worktrace.py --config config.json

# Or with CLI overrides
python scripts/worktrace.py --output-dir /path/to/daily --date 2024-01-15
```

**Important:**
- MUST wait for complete script output before proceeding
- NEVER attempt to parse files manually with Bash

### Phase 2: Summarization

1. Read script output (markdown or JSON)
2. Refer to [references/summarize.md](references/summarize.md) for summarization rules
3. Transform raw output into meaningful summary:
   - Group similar activities
   - Remove noise and duplicates
   - Infer context from activity patterns

### Phase 3: Output

1. If `output_dir` is configured: Script saves directly to daily file
2. If not configured: Present summarized content to user
3. Verify the output file was updated correctly

## Common Options

| Option | Description |
|--------|-------------|
| `--output-dir PATH` | Save to daily file in directory |
| `--ticket-pattern REGEX` | Custom ticket pattern (repeatable) |
| `--timezone TZ` | Timezone for "today" calculation |
| `--config FILE` | Load settings from JSON config |
| `--json` | Output as JSON instead of markdown |

## Examples

Extract with custom ticket patterns:

```bash
python scripts/worktrace.py \
  --ticket-pattern "AMAP-\d+" \
  --ticket-pattern "IE-\d+"
```

Use config file:

```bash
python scripts/worktrace.py --config config.json
```

## Output Format

```markdown
## Claude Code Work History

### PROJ-123 (webapp)
- Implement login form validation
- Fix password reset flow

### API-456 (api-service)
- Fix null pointer exception in user service

### Other (docs)
- Update README documentation
```

## File Handling

When `output_dir` is specified:
- Creates `{YYYY-MM-DD}.md` in the directory
- **If file exists**: replaces `## Claude Code Work History` section only
- Other sections in the file are preserved

## Configuration

For detailed configuration options including:
- Frontmatter template
- Ticket pattern examples
- Timezone settings
- CLI usage examples

See [references/template.md](references/template.md)

## Error Handling

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "No entries found" | No activity for the target date | Check `--date` option or verify Claude Code was used |
| Script not found | Wrong working directory | Run from plugin root directory |
| Permission denied | File access issue | Check file permissions for `~/.claude/` |
| Config not found | Missing config.json | Run First-time Setup (Phase 0) |

### Debug Mode

If issues persist, use JSON output for debugging:

```bash
python scripts/worktrace.py --config config.json --json
```

This outputs raw data structure for inspection.

### Fallback Behavior

If the Python script fails:
1. Check that `~/.claude/history.jsonl` exists
2. Verify Python 3 is available (`python --version`)
3. Check config.json is valid JSON
4. Try running without config: `python scripts/worktrace.py --output-dir /path/to/daily`
