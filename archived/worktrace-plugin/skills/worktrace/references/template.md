# Daily File Template Reference

This document defines templates and customization options for daily work history files.

## Frontmatter Template

When creating a new daily file, use this YAML frontmatter:

```yaml
---
published: false
id: {YYYY-MM-DD}
slug: {YYYY-MM-DD}
title: {YYYY-MM-DD}
summary: Daily work notes for {YYYY-MM-DD}
toc: false
tags: ["daily"]
categories: ["daily"]
createdDate: {YYYY-MM-DD}
updatedDate: {YYYY-MM-DD}
---
```

## Output Section Format

The work history section follows this structure:

```markdown
## Claude Code Work History

### {TICKET} ({project})
- **Directory**: `{full project path}`
- **Session**: `{session-id}`
- {activity 1}
- {activity 2}

### Other ({project})
- **Directory**: `{full project path}`
- **Sessions**: `{id1}`, `{id2}` (if multiple sessions)
- {activities without ticket}
```

## Ticket Pattern Configuration

Configure ticket patterns using regex. Common patterns:

| Pattern | Description | Example Match |
|---------|-------------|---------------|
| `[A-Z]+-\d+` | Standard JIRA | PROJ-123, API-456 |
| `AMAP-\d+` | Specific prefix | AMAP-1234 |
| `#\d+` | GitHub issue | #123 |
| `[A-Z]{2,5}-\d{1,6}` | Flexible JIRA | AB-1, ABCDE-123456 |

Multiple patterns can be specified. First match wins.

## Activity Summarization

Activities are extracted from the `display` field in history.jsonl:

- Commands are preserved: `/commit`, `/context`, `/mcp`
- Long text is truncated to 60 characters
- Duplicate activities are deduplicated per group
- Empty activities are skipped

## Timezone Handling

Specify timezone for accurate "today" calculation:

| Timezone | Example |
|----------|---------|
| `UTC` | Universal Time |
| `Asia/Seoul` | Korea Standard Time (KST) |
| `America/New_York` | Eastern Time |
| `Europe/London` | British Time |

If not specified, system timezone is used.

## CLI Usage Examples

```bash
# Basic usage - output to stdout
python worktrace.py

# Save to specific directory
python worktrace.py --output-dir ./daily

# Custom ticket patterns
python worktrace.py --ticket-pattern "AMAP-\d+" --ticket-pattern "IE-\d+"

# Specific date and timezone
python worktrace.py --date 2024-12-31 --timezone Asia/Seoul

# Use config file
python worktrace.py --config config.json

# Output as JSON
python worktrace.py --json
```

## Config File Structure

```json
{
  "history_file": "~/.claude/history.jsonl",
  "output_dir": "./daily",
  "ticket_patterns": ["[A-Z]+-\\d+"],
  "timezone": "UTC",
  "section_title": "## Claude Code Work History",
  "frontmatter": {
    "published": false,
    "tags": ["daily"]
  }
}
```

CLI arguments override config file values.

## File Saving Logic

When `output_dir` is specified, the script handles file creation and updates:

### New File
If `{YYYY-MM-DD}.md` doesn't exist:
- Creates new file with the generated content

### Existing File
If file already exists:
1. Reads current content
2. Looks for `## Claude Code Work History` section
3. **Section found**: Replaces only that section (preserves other content)
4. **Section not found**: Appends after first `# heading`

```
+-----------------------------+
| # 2024-12-31               |  <- Preserved
|                             |
| ## My Notes                 |  <- Preserved
| - Some notes...             |
|                             |
| ## Claude Code Work History |  <- Replaced
| ### PROJ-123 (webapp)       |
| - Updated content           |
|                             |
| ## Other Section            |  <- Preserved
+-----------------------------+
```

This allows you to add custom notes to the daily file without losing them on updates.
