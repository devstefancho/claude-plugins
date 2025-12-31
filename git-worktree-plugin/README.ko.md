# Git Worktree Plugin

병렬 브랜치 작업을 위한 git worktree 관리 플러그인입니다.

## 기능

- **사전 제안** - PR이나 새 기능 작업 시 자동으로 worktree 생성 제안
- **간편한 생성** - 적절한 브랜치 명명 규칙으로 worktree 생성
- **정리 관리** - worktree 목록 확인 및 안전한 제거

## 설치

```bash
/plugin install git-worktree-plugin@devstefancho-claude-plugins
```

## 사용법

다음과 같은 상황에서 스킬이 자동으로 호출됩니다:
- PR 작업 시 (예: "PR #9 작업하자", "work on PR #123")
- 새 기능/작업 시작 시
- main 브랜치에서 새로운 기능 구현 시

## Worktree 구조

```
./trees/{branch-name}/
```

브랜치 명명:
- PR: `pr-{number}` (예: `pr-123`)
- 기능: `{prefix}/{feature-name}` (예: `feat/user-authentication`)

프리픽스: feat, fix, bug, chore, docs, test
