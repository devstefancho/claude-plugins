# Session Reporter Plugin

Generate HTML reports to visualize your Claude Code work sessions.

## Features

- **Session Visualization** - View conversation history, code changes, and execution results
- **Flexible Scope** - Export last activity only or entire session
- **Auto-open** - HTML file opens automatically in your browser
- **Clean Formatting** - Syntax highlighting and section navigation

## Installation

```bash
/plugin install session-reporter-plugin@devstefancho-claude-plugins
```

## Usage

The skill is invoked when you ask to view content as HTML:

- "HTML로 보여줘"
- "HTML 파일로 만들어줘"
- "view as HTML"
- "export to HTML"

## Report Contents

- **Work Summary** - Files modified, key decisions, major changes
- **Conversation** - User questions and Claude's responses
- **Code Changes** - Diffs and before/after comparisons
- **Execution Results** - Test results, build output, errors

## Output

Reports are saved to `/tmp/session-report-{timestamp}.html`
