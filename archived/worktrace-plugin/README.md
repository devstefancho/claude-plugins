# Worktrace Plugin

Extract Claude Code work history and generate daily summaries grouped by project and ticket.

## Features

- Extract work history from `~/.claude/history.jsonl`
- Automatic grouping by ticket number and project
- Markdown or JSON output support
- Preserve other sections when updating existing daily files
- Timezone support

## Installation

```bash
/plugin install worktrace-plugin@devstefancho-claude-plugins
```

## Usage

### Slash Command

```
/trace
```

This command invokes the worktrace skill to extract today's work history and update daily notes.

### Direct Script Usage

```bash
# Basic usage (stdout output)
python scripts/worktrace.py

# Save to specific directory
python scripts/worktrace.py --output-dir ./daily

# Custom ticket patterns
python scripts/worktrace.py --ticket-pattern "AMAP-\d+" --ticket-pattern "IE-\d+"

# Specific date and timezone
python scripts/worktrace.py --date 2024-12-31 --timezone Asia/Seoul

# Use config file
python scripts/worktrace.py --config config.json

# JSON output
python scripts/worktrace.py --json
```

## Configuration

Copy `config.example.json` to `config.json` for configuration:

```json
{
  "history_file": "~/.claude/history.jsonl",
  "output_dir": "./daily",
  "ticket_patterns": ["[A-Z]+-\\d+"],
  "timezone": "Asia/Seoul",
  "section_title": "## Claude Code Work History"
}
```

**Priority**: CLI args > config.json > defaults

## Output Example

```markdown
## Claude Code Work History

### PROJ-123 (webapp)
- **Directory**: `/Users/user/projects/webapp/feat/PROJ-123`
- **Session**: `464c991b-f368-4ac4-9376-4fe6f1c9147e`
- Implement login form validation
- Fix password reset flow

### API-456 (api-service)
- **Directory**: `/Users/user/projects/api-service/bugfix/API-456`
- **Session**: `abc12345-...`
- Fix null pointer exception in user service

### Other (docs)
- **Directory**: `/Users/user/projects/docs`
- **Session**: `xyz78910-...`
- Update README documentation
```

## File Handling

When `--output-dir` is specified:
- Creates `{YYYY-MM-DD}.md` file
- If file already exists, only replaces `## Claude Code Work History` section
- Other sections are preserved

## See Also

- [SKILL.md](skills/worktrace/SKILL.md) - Skill definition
- [template.md](skills/worktrace/references/template.md) - Template reference
- [summarize.md](skills/worktrace/references/summarize.md) - Summarization guidelines
