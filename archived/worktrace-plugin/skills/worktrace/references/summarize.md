# Summarization Guidelines

After running the script, analyze raw output and create a meaningful summary.

## Rules

1. **Group related activities** - Combine similar tasks into coherent descriptions
2. **Infer context** - Transform commands to actions:
   - `/commit` -> "Committed changes"
   - `/context` -> "Reviewed context"
   - `/mcp` -> "Configured MCP"
   - `/skills` -> "Managed skills"
3. **Skip noise**:
   - Test commands (`&echo`, `&hi`, `&npm run dev`)
   - Help lookups (`/help`)
   - Duplicate entries
   - Incomplete or unclear entries
4. **Extract intent** - Describe what was accomplished, not what was typed
5. **Concise** - Max 3-5 bullets per project/ticket group

## Top 3 Repetitive Prompts

Analyze all session entries and identify the **top 3 most frequently used prompts or patterns**:

1. Count occurrences of similar prompts across all projects
2. Group by semantic similarity (e.g., "fix bug", "fixing bug", "bug fix" = same category)
3. Present as a summary section at the end

**Example output:**
```markdown
## Frequently Used Patterns

| Rank | Pattern | Count |
|------|---------|-------|
| 1 | Code review/refactoring | 12 |
| 2 | Bug fixes | 8 |
| 3 | Documentation updates | 5 |
```

## Example Transformation

**Raw output:**
```
### PROJ-123 (webapp)
- **Directory**: `/Users/.../webapp/feat/PROJ-123`
- **Session**: `464c991b-f368-4ac4-9376-4fe6f1c9147e`
- &hi
- /context - Review error handling
- Fix null pointer exception in user service
- /commit - Add validation
- Implement login form

### Other (docs)
- **Directory**: `/Users/.../docs`
- **Session**: `abc12345-...`
- /help
- Update README
```

**Summarized:**
```
### PROJ-123 (webapp)
- **Directory**: `/Users/.../webapp/feat/PROJ-123`
- **Session**: `464c991b-f368-4ac4-9376-4fe6f1c9147e`
- Reviewed and fixed error handling (null pointer exception)
- Added input validation
- Implemented login form

### Other (docs)
- **Directory**: `/Users/.../docs`
- **Session**: `abc12345-...`
- Updated README documentation
```

## Output Format

Present the final summary in this structure:

```markdown
## Claude Code Work History

### {TICKET} ({project})
- **Directory**: `{full path}`
- **Session**: `{session-id}` (or **Sessions**: for multiple)
- {meaningful activity 1}
- {meaningful activity 2}

### Other ({project})
- **Directory**: `{full path}`
- **Session**: `{session-id}`
- {activity without ticket}

## Frequently Used Patterns

| Rank | Pattern | Count |
|------|---------|-------|
| 1 | {pattern} | {count} |
| 2 | {pattern} | {count} |
| 3 | {pattern} | {count} |
```
