---
description: Analyze changes and auto-commit with conventional commit format
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git log:*)
---

# Automatic Git Commit Generation

Analyzes modified files and content to automatically generate appropriate conventional commit messages and commit changes.

<context>
Check current git status:

!`git status`: Check current changes and staging status
!`git diff --cached`: Check staged changes in detail (if no staged files, also check unstaged files)
!`git log -5 --oneline --no-decorate`: Reference recent commit message style
</context>

<instruction>
Follow these steps:

1. **Analyze Changes**
   - If no files are staged, notify the user and suggest which files to stage
   - Analyze paths and content of modified files
   - Determine appropriate scope considering project structure

2. **Automatically Determine Commit Scope**
   Select scope based on these rules:
   - `feat`: New features, components, API endpoints, UI additions
   - `fix`: Bug fixes, error handling, error corrections
   - `chore`: Dependency updates, config file changes, build settings
   - `docs`: README, documentation files (*.md), comment changes
   - `style`: Code formatting, CSS, style modifications (no functional changes)
   - `refactor`: Code structure improvements without functional changes, refactoring
   - `test`: Test code additions/modifications, test configuration
   - `build`: Build script, package configuration changes
   - `ci`: CI/CD configuration changes

3. **Write Commit Message** (English)
   - Format: `{scope}: {clear and concise English summary}`
   - Start summary with a verb (e.g., "Add", "Fix", "Improve", "Remove")
   - Keep within 50 characters
   - Add detailed description after blank line if needed (each line within 72 characters)

4. **Request User Confirmation**
   - Show the generated commit message
   - Summarize key changes (diff highlights)
   - Use AskUserQuestion tool to request approval or modification
   - Options: "Execute commit", "Modify message", "Cancel"

5. **Execute Commit**
   - If approved: `git commit -m "generated message"`
   - If modification requested: Rewrite message reflecting user feedback and confirm again
   - If cancelled: Abort operation
</instruction>

<important>
- If no staged changes, first suggest files to `git add`
- If changes span multiple scopes, select the most significant one or suggest separate commits
- Warn about files containing sensitive information (API keys, passwords, etc.)
- Maintain consistency by referencing the project's recent commit style
- Do not create empty commits
</important>

<examples>
Good commit message examples:
- `feat: Add user authentication feature`
- `fix: Fix boundary value error in date range search`
- `chore: Update dependency versions`
- `docs: Add API usage examples`
- `refactor: Improve service layer code structure`
- `test: Add unit tests`
</examples>
