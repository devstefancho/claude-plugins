# Git Commit Plugin

Auto-generate conventional commit messages by analyzing git changes.

## Features

- **Smart Analysis** - Analyzes staged/unstaged changes automatically
- **Scope Detection** - Determines appropriate commit type (feat, fix, chore, etc.)
- **User Confirmation** - Asks for approval before committing
- **Security Checks** - Warns about sensitive information in commits

## Installation

```bash
/plugin install git-commit-plugin@devstefancho-claude-plugins
```

## Usage

```bash
/commit
```

The command will:
1. Check git status and staged changes
2. Analyze the changes
3. Generate a conventional commit message
4. Ask for your approval
5. Execute the commit

## Commit Types

- `feat`: New features
- `fix`: Bug fixes
- `chore`: Maintenance tasks
- `docs`: Documentation changes
- `style`: Code formatting
- `refactor`: Code refactoring
- `test`: Test additions/updates
- `build`: Build configuration
- `ci`: CI/CD changes

## Example Output

```
feat: Add user authentication feature
fix: Fix boundary value error in date range search
chore: Update dependency versions
```
