# Git Worktree Plugin v2.0

셸 스크립트 자동화를 통한 git worktree 관리 플러그인입니다.

## 기능

- **사전 제안** - PR이나 새 기능 작업 시 자동으로 worktree 생성 제안
- **Bare Repository 지원** - bare clone 또는 기존 저장소 변환으로 최적의 worktree 워크플로우 구성
- **백업 & 롤백** - bare 변환 시 자동 백업 및 실패 시 롤백
- **셸 스크립트 기반** - 인라인 명령어 대신 테스트된 셸 스크립트로 안정적 실행
- **정리 관리** - worktree 및 관련 브랜치 안전하게 제거

## 설치

```bash
/plugin install git-worktree-plugin@devstefancho-claude-plugins
```

또는 npx로 설치:
```bash
npx @anthropic-ai/claude-code@latest /plugin install git-worktree-plugin@devstefancho-claude-plugins
```

## 워크플로우

### A. Worktree 생성

다음과 같은 상황에서 스킬이 자동으로 호출됩니다:
- PR 작업 시 (예: "PR #9 작업하자")
- 새 기능/작업 시작 시
- main 브랜치에서 새로운 기능 구현 시

**PR 체크아웃**과 **새 브랜치** 모드를 모두 지원합니다.

### B-1. Bare Clone (새 프로젝트)

bare 저장소 구조로 새 프로젝트를 설정합니다:

```
project-name/
├── .bare/              # Bare git 저장소
├── .git                # .bare를 가리키는 파일
└── trees/
    └── main/           # 초기 worktree
```

### B-2. Bare 전환 (기존 프로젝트)

기존 clone을 bare 구조로 변환합니다:
- 변환 전 `.git`을 `.git-backup/`으로 백업
- 실패 시 자동 롤백
- 모든 커밋 기록과 브랜치 보존

### C. 정리

worktree를 개별 또는 전체 삭제하며, 관련 브랜치도 함께 정리합니다.

## Worktree 구조

```
./trees/{branch-name}/
```

브랜치 명명:
- PR: `pr-{number}` (예: `pr-123`)
- 기능: `{prefix}/{feature-name}` (예: `feat/user-authentication`)

프리픽스: feat, fix, chore, refactor, docs, test

## 스크립트

모든 작업은 `scripts/`의 셸 스크립트로 구현되어 있습니다:

| 스크립트 | 용도 |
|---------|------|
| `detect.sh` | 저장소 타입 감지 (bare/normal/none) |
| `create-worktree.sh` | 브랜치 또는 PR로 worktree 생성 |
| `bare-clone.sh` | bare 저장소로 clone하여 worktree 구조 생성 |
| `convert-to-bare.sh` | 기존 clone을 bare로 변환 (백업/롤백 포함) |
| `cleanup-worktree.sh` | worktree 및 브랜치 제거 |

## 테스트

```bash
bash tests/run-all.sh
```

개별 테스트:
```bash
bash tests/test-detect.sh
bash tests/test-create-worktree.sh
bash tests/test-bare-clone.sh
bash tests/test-convert-to-bare.sh
bash tests/test-cleanup.sh
```
