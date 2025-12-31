---
name: worktrace
description: Extract Claude Code work history and update daily notes. Use when user asks to update daily file with today's work, sync work history, record activities, or generate daily summary from Claude Code history.
---

# Worktrace

Extract today's Claude Code work history from `~/.claude/history.jsonl` and generate a structured markdown summary grouped by project and ticket.

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

## Workflow

1. **Determine target date** - Default is today, or use `--date YYYY-MM-DD`
2. **Run the script** with appropriate options
3. **Summarize output** - Analyze raw results and create meaningful summary
   - For guidelines, see [references/summarize.md](references/summarize.md)
4. **Update daily file** - Present or save the summarized content

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
