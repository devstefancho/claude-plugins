# Git Commit Plugin

Auto-generate conventional commit messages in Korean by analyzing git changes.

## Features

- **Smart Analysis** - Analyzes staged/unstaged changes automatically
- **Scope Detection** - Determines appropriate commit type (feat, fix, chore, etc.)
- **Korean Messages** - Generates commit messages in Korean
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
feat: 사용자 인증 기능 추가
fix: 날짜 범위 검색 시 경계값 오류 수정
chore: 의존성 버전 업데이트
```
