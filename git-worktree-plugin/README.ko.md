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

## 명령어

### /bare-setup

git worktree 워크플로우를 위한 bare clone 구조로 새 저장소를 설정합니다.

```bash
# URL 인자와 함께
/bare-setup git@github.com:org/repo.git

# 대화형 모드 (URL 입력 프롬프트)
/bare-setup
```

**수행 작업:**
1. 저장소를 bare로 clone (`.bare/`)
2. gitdir 포인터 생성 (`.git` 파일)
3. 원격 추적을 위한 fetch refspec 설정 (git pull/push 가능)
4. `trees/` 디렉토리에 초기 worktree 생성

**결과 구조:**
```
project-name/
├── .bare/              # Bare git 저장소
├── .git                # .bare를 가리키는 파일
└── trees/
    └── main/           # 초기 worktree (작업 디렉토리)
```

**장점:**
- 여러 브랜치를 동시에 체크아웃 가능
- 각 worktree는 별도의 작업 디렉토리
- 여러 기능 작업 시 stash/switch 불필요
- 단일 공유 git 객체 저장소로 디스크 사용량 감소
