---
name: session-reporter
description: Generate HTML file to view work session. Use when user asks to view content as HTML (e.g., 'view as HTML', 'export to HTML', 'create HTML file', 'save as HTML').
allowed-tools: Write, Bash, AskUserQuestion
---

# Session Reporter

Generate an HTML file that visualizes your current work session, including conversation history, code changes, and execution results. The HTML file is automatically opened in your default browser.

## Instructions

Follow these steps to generate a session report:

### 1. Ask User for Report Scope

Use the AskUserQuestion tool to determine what content to include:

```
Question: "What scope of session content should be included in the HTML?"
Options:
- "Last activity only" (most recent task/conversation)
- "Full session" (entire conversation from start)
- "Custom" (ask user to specify what to include)
```

### 2. Collect Session Information

Based on the user's choice, gather the following information:

- **Work Summary**:
  - Files modified
  - Key decisions made
  - Major changes implemented

- **Conversation**:
  - User questions and requests
  - Claude's responses
  - Important clarifications

- **Code Changes**:
  - Modified files with diffs or before/after comparisons
  - New files created
  - Files deleted

- **Execution Results**:
  - Test results
  - Build output
  - Error messages
  - Command outputs

### 3. Generate HTML File

Use the template at `templates/report.html` to create the HTML file:

1. Read the template file
2. Replace placeholders with actual session data:
   - `{{TITLE}}` - Report title (e.g., "Session Report - 2025-11-15")
   - `{{TIMESTAMP}}` - Generation timestamp
   - `{{SUMMARY}}` - Work summary section
   - `{{CONVERSATION}}` - Conversation content
   - `{{CHANGES}}` - Code changes section
   - `{{RESULTS}}` - Execution results section
3. Save to `/tmp/session-report-{timestamp}.html`
   - Use format: `session-report-YYYYMMDD-HHMMSS.html`
   - Example: `session-report-20251115-143022.html`

### 4. Open in Browser

After generating the HTML file:

1. Use Bash tool to open the file:
   ```bash
   open /tmp/session-report-{timestamp}.html
   ```
2. Provide the file:// path to the user:
   ```
   file:///tmp/session-report-{timestamp}.html
   ```

### 5. Inform User

Tell the user:
- The HTML file has been generated and opened in the browser
- The file path for future reference
- The file is temporary and will be cleaned up on system restart

## Examples

### Example 1: Last Activity Only

```
User: View as HTML
Claude: [Uses AskUserQuestion to confirm scope]
User: Last activity only
Claude: [Generates HTML with recent changes only, opens in browser]
```

### Example 2: Full Session

```
User: Create an HTML file with the full session
Claude: [Uses AskUserQuestion to confirm]
User: Full session
Claude: [Generates comprehensive HTML with all conversation and changes]
```

## Tips

- Keep HTML styling simple and clean for easy reading
- Include proper syntax highlighting for code blocks using `<pre><code>` tags
- Add section navigation for longer reports
- Make the HTML print-friendly for documentation purposes
- Use semantic HTML elements for better accessibility
