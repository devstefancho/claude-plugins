# Session Reporter - Reference

## Overview

Visualize work sessions as HTML files that can be viewed in the browser.

## Trigger Keywords

"view as HTML", "export to HTML", "show in HTML", "create HTML file", "save as HTML"

## Report Scope Options

1. **Last activity only** - Most recent work content only
2. **Full session** - All conversations/changes from the start
3. **Custom** - Select specific content to include

## File Location

```
/tmp/session-report-YYYYMMDD-HHMMSS.html
```

⚠️ Files in `/tmp` are deleted on system restart.

## Template Customization

Template location: `.claude/skills/session-reporter/templates/report.html`

### Placeholders

- `{{TITLE}}` - Report title
- `{{TIMESTAMP}}` - Generation time
- `{{SUMMARY}}` - Work summary
- `{{CONVERSATION}}` - Conversation content
- `{{CHANGES}}` - Code changes
- `{{RESULTS}}` - Execution results
- `{{FILE_PATH}}` - File path

## Tips

- **Before sharing**: Remove sensitive information (API keys, passwords)
- **Permanent storage**: Copy important reports to another location
- **PDF conversion**: Use browser's print function (Cmd+P)
