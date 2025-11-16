# PR Create Plugin

Create GitHub pull requests with auto-generated title and description.

## Features

- **Smart Analysis** - Analyzes all commits since branching from main
- **Auto Title** - Generates concise PR title from changes
- **Structured Body** - Creates summary and test plan sections
- **Push & Create** - Pushes branch and creates PR in one command

## Installation

```bash
/plugin install pr-create-plugin@devstefancho-claude-plugins
```

## Usage

```bash
/pr-create
```

The command will:
1. Check current branch status and commits
2. Analyze all changes from main branch
3. Generate PR title and description
4. Push branch to origin (if needed)
5. Create PR using GitHub CLI

## PR Format

```markdown
## Summary
- Bullet point 1
- Bullet point 2

## Test plan
- [ ] Test step 1
- [ ] Test step 2

🤖 Generated with Claude Code
```

## Requirements

- GitHub CLI (`gh`) installed and authenticated
- Git repository with remote configured
