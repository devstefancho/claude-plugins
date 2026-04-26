---
name: git-worktree
description: Manage git worktrees for parallel branch work. PROACTIVELY USE when user mentions working on a PR, new feature, or new task - ask if they want to create a worktree BEFORE starting implementation.
allowed-tools: Bash, AskUserQuestion
context: fork
agent: general-purpose
---

# Git Worktree Manager

## Overview

| Workflow | Trigger | Scripts |
|----------|---------|---------|
| A. Create Worktree | PR/새 기능 작업 언급 | create-and-open.sh |
| B-1. Bare Clone | 새 프로젝트 세팅 요청 | bare-clone.sh |
| B-2. Convert to Bare | bare 전환 요청 | detect.sh → convert-to-bare.sh |
| C. Cleanup | worktree 정리 요청 | cleanup-worktree.sh |

## CRITICAL: Script-Only Execution

**절대 git worktree/tmux 명령어를 직접 실행하지 마세요.**
모든 워크플로우는 반드시 `$PLUGIN_DIR/scripts/` 의 스크립트를 통해 실행해야 합니다.
스크립트가 worktree 생성, push, CLAUDE.local.md 생성, tmux 윈도우 열기를 모두 처리합니다.

금지 명령어: `git worktree add`, `tmux new-window`, `tmux split-window` 등을 직접 호출하지 마세요.
반드시 아래 Bash 코드블록을 그대로 복사하여 플레이스홀더(`{...}`)만 치환 후 실행하세요.

## Smart Detection (Proactive Trigger)

When the user mentions any of these, **skip the Workflow/Type selection** and proceed directly:

| User says | Action |
|-----------|--------|
| PR number (e.g., "PR #9", "work on PR 123") | → Workflow A: PR Checkout (0 questions) |
| New feature/task (e.g., "implement auth", "add dark mode") | → Workflow A: New Branch (3-4 questions) |
| `/git-worktree` manual trigger | → Workflow Selection (show menu) |

**Ask BEFORE proceeding with implementation work.**

## Workflow Selection (Manual Trigger Only)

Only show when `/git-worktree` is explicitly invoked. First run the Inline Detection block below to determine `WORKTREE_STYLE`, then filter options:

| WORKTREE_STYLE | Available Options |
|----------------|-------------------|
| `bare` | Create Worktree, Cleanup, Bare Clone |
| `normal` | Create Worktree, Convert to Bare, Cleanup, Bare Clone |
| `none` | Bare Clone only |

```
Question: "어떤 작업을 하시겠습니까?"
Header: "Workflow"
Options: (filtered by WORKTREE_STYLE)
- "Create Worktree" - PR 체크아웃 또는 새 브랜치로 worktree 생성
- "Convert to Bare" - 현재 repo를 bare 구조로 변환
- "Cleanup" - 불필요한 worktree 제거
- "Bare Clone" - 새 프로젝트를 bare repo로 clone
```

To detect `WORKTREE_STYLE`, run this single Bash call:

```bash
TOPLEVEL=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$TOPLEVEL" ]; then
  echo "WORKTREE_STYLE=none"
elif [ -f "$TOPLEVEL/.git" ]; then
  echo "WORKTREE_STYLE=bare"
else
  echo "WORKTREE_STYLE=normal"
fi
```

## Workflow A: Create Worktree

### Smart Path: PR Checkout (0 questions)

When user mentions a PR number, extract it and run this **complete** Bash block. Replace `{NUMBER}` with the actual PR number:

```bash
# === PLUGIN_DIR Resolution ===
PLUGIN_DIR=$(find ~/.claude/plugins/cache -maxdepth 6 -path "*/git-worktree-plugin/*/scripts/create-and-open.sh" 2>/dev/null \
  | sed 's|/scripts/create-and-open.sh||' \
  | sort -V \
  | tail -1)
if [ -z "$PLUGIN_DIR" ]; then
  _SKILL_SCRIPTS=$(find ~/.agents/skills -maxdepth 4 -path "*/git-worktree/scripts/create-and-open.sh" 2>/dev/null | head -1)
  [ -n "$_SKILL_SCRIPTS" ] && PLUGIN_DIR=$(dirname "$_SKILL_SCRIPTS")/..
fi
if [ -z "$PLUGIN_DIR" ]; then echo "ERROR: Plugin scripts not found" >&2; exit 1; fi

# === Inline Detection ===
TOPLEVEL=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$TOPLEVEL" ]; then
  echo "ERROR: Not in a git repository" >&2; exit 1
elif [ -f "$TOPLEVEL/.git" ]; then
  GIT_COMMON=$(cd "$TOPLEVEL" && git rev-parse --git-common-dir)
  BARE_DIR=$(cd "$TOPLEVEL" && cd "$GIT_COMMON" && pwd)
  PROJECT_ROOT=$(dirname "$BARE_DIR")
  WORKTREE_ROOT="$PROJECT_ROOT/trees"
else
  PROJECT_ROOT="$TOPLEVEL"
  WORKTREE_ROOT="$TOPLEVEL/trees"
fi

# === Execute ===
PR_INFO=$(gh pr view {NUMBER} --json title,body --jq '"PR #\(.number): \(.title)\n\n\(.body)"' 2>/dev/null || echo "PR #{NUMBER}")
bash "$PLUGIN_DIR/scripts/create-and-open.sh" \
  --project-root "$PROJECT_ROOT" \
  --worktree-root "$WORKTREE_ROOT" \
  --pr {NUMBER} \
  --tmux-name "pr-{NUMBER}" \
  --context "$PR_INFO"
```

### Smart Path: New Branch (3-4 questions)

When user mentions a new feature/task, ask 3-4 questions:

**Question 1: Branch type**
```
Question: "브랜치 타입을 선택하세요"
Header: "Branch"
Options:
- "feat/ (Recommended)" - 새 기능 개발
- "fix/" - 버그 수정
- "chore/" - 유지보수 작업
- "refactor/" - 코드 리팩토링
```

Parse the selection: prefix = first word before `/`.
If user selects "Other", ask for custom prefix.

**Question 2: Base branch**
```
Question: "어느 브랜치에서 분기하시겠습니까?"
Header: "Base"
Options:
- "main (Recommended)" - main 브랜치의 최신 remote 상태에서 분기
- "develop" - develop 브랜치의 최신 remote 상태에서 분기
```

Parse the selection: base = `origin/{selection}`.
If user selects "Other", ask for custom base (e.g., `origin/release/v2`).

**Question 3: Feature name**
```
Ask user to briefly describe the feature. Format: lowercase, spaces/underscores → dashes.
```

**Question 4: Context interview (optional)**
```
Question: "Worktree에서 작업할 내용을 상세히 입력하시겠습니까?"
Header: "Context"
Options:
- "입력하기" - 해결할 문제, 할 일, 참고사항을 입력
- "건너뛰기" - 기본 컨텍스트만 사용
```

If user selects "입력하기", ask a follow-up free-text question:
```
"작업 컨텍스트를 자유롭게 입력해주세요. 예시:
- 해결할 문제: 로그인 세션 만료 시 자동 갱신이 안 됨
- 할 일: 토큰 갱신 로직 추가, 미들웨어 수정, 테스트 작성
- 참고: src/auth/ 디렉토리, v2 API 호환 필요"
```

Organize the user's response into `## Problem`, `## Tasks`, `## Notes` sections and append to the `--context` parameter.

**`--context` format when interview is completed:**
```
Branch: {prefix}/{feature-name}, Base: origin/{base-branch}
Feature: {description}

## Problem
{organized problem description}

## Tasks
{organized task list}

## Notes
{organized notes}
```

**`--context` format when skipped:** same as before (Branch + Feature only).

Then run this **complete** Bash block. Replace `{prefix}`, `{feature-name}`, `{base-branch}`, `{dir-name}`, and `{description}`:

```bash
# === PLUGIN_DIR Resolution ===
PLUGIN_DIR=$(find ~/.claude/plugins/cache -maxdepth 6 -path "*/git-worktree-plugin/*/scripts/create-and-open.sh" 2>/dev/null \
  | sed 's|/scripts/create-and-open.sh||' \
  | sort -V \
  | tail -1)
if [ -z "$PLUGIN_DIR" ]; then
  _SKILL_SCRIPTS=$(find ~/.agents/skills -maxdepth 4 -path "*/git-worktree/scripts/create-and-open.sh" 2>/dev/null | head -1)
  [ -n "$_SKILL_SCRIPTS" ] && PLUGIN_DIR=$(dirname "$_SKILL_SCRIPTS")/..
fi
if [ -z "$PLUGIN_DIR" ]; then echo "ERROR: Plugin scripts not found" >&2; exit 1; fi

# === Inline Detection ===
TOPLEVEL=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$TOPLEVEL" ]; then
  echo "ERROR: Not in a git repository" >&2; exit 1
elif [ -f "$TOPLEVEL/.git" ]; then
  GIT_COMMON=$(cd "$TOPLEVEL" && git rev-parse --git-common-dir)
  BARE_DIR=$(cd "$TOPLEVEL" && cd "$GIT_COMMON" && pwd)
  PROJECT_ROOT=$(dirname "$BARE_DIR")
  WORKTREE_ROOT="$PROJECT_ROOT/trees"
else
  PROJECT_ROOT="$TOPLEVEL"
  WORKTREE_ROOT="$TOPLEVEL/trees"
fi

# === Execute ===
bash "$PLUGIN_DIR/scripts/create-and-open.sh" \
  --project-root "$PROJECT_ROOT" \
  --worktree-root "$WORKTREE_ROOT" \
  --branch "{prefix}/{feature-name}" \
  --base "origin/{base-branch}" \
  --push \
  --tmux-name "{dir-name}" \
  --context "Branch: {prefix}/{feature-name}, Base: origin/{base-branch}
Feature: {description}"
```

### Manual Path: Create Worktree

If reached via Workflow Selection, first ask Type (PR or New Branch), then follow the appropriate Smart Path above.

## Workflow B-1: Bare Clone

Use AskUserQuestion to collect URL and path, then run this **complete** Bash block. Replace `{URL}` and `{PATH}`:

```bash
# === PLUGIN_DIR Resolution ===
PLUGIN_DIR=$(find ~/.claude/plugins/cache -maxdepth 6 -path "*/git-worktree-plugin/*/scripts/create-and-open.sh" 2>/dev/null \
  | sed 's|/scripts/create-and-open.sh||' \
  | sort -V \
  | tail -1)
if [ -z "$PLUGIN_DIR" ]; then
  _SKILL_SCRIPTS=$(find ~/.agents/skills -maxdepth 4 -path "*/git-worktree/scripts/create-and-open.sh" 2>/dev/null | head -1)
  [ -n "$_SKILL_SCRIPTS" ] && PLUGIN_DIR=$(dirname "$_SKILL_SCRIPTS")/..
fi
if [ -z "$PLUGIN_DIR" ]; then echo "ERROR: Plugin scripts not found" >&2; exit 1; fi

# === Execute ===
bash "$PLUGIN_DIR/scripts/bare-clone.sh" \
  --url "{URL}" \
  --path "{PATH}" \
  --branch "main"
```

## Workflow B-2: Convert to Bare

### Step 1: Detect and confirm
Run inline detection. If WORKTREE_STYLE is already "bare", inform user it's already a bare repo.

Use AskUserQuestion:
```
Question: "Convert this repository to bare structure? A backup will be created at .git-backup/"
Header: "Convert"
Options:
- "Proceed" - Convert to bare (backup included)
- "Cancel" - Abort
```

### Step 2: Execute

Run this **complete** Bash block:

```bash
# === PLUGIN_DIR Resolution ===
PLUGIN_DIR=$(find ~/.claude/plugins/cache -maxdepth 6 -path "*/git-worktree-plugin/*/scripts/create-and-open.sh" 2>/dev/null \
  | sed 's|/scripts/create-and-open.sh||' \
  | sort -V \
  | tail -1)
if [ -z "$PLUGIN_DIR" ]; then
  _SKILL_SCRIPTS=$(find ~/.agents/skills -maxdepth 4 -path "*/git-worktree/scripts/create-and-open.sh" 2>/dev/null | head -1)
  [ -n "$_SKILL_SCRIPTS" ] && PLUGIN_DIR=$(dirname "$_SKILL_SCRIPTS")/..
fi
if [ -z "$PLUGIN_DIR" ]; then echo "ERROR: Plugin scripts not found" >&2; exit 1; fi

# === Inline Detection ===
TOPLEVEL=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$TOPLEVEL" ]; then
  echo "ERROR: Not in a git repository" >&2; exit 1
elif [ -f "$TOPLEVEL/.git" ]; then
  GIT_COMMON=$(cd "$TOPLEVEL" && git rev-parse --git-common-dir)
  BARE_DIR=$(cd "$TOPLEVEL" && cd "$GIT_COMMON" && pwd)
  PROJECT_ROOT=$(dirname "$BARE_DIR")
else
  PROJECT_ROOT="$TOPLEVEL"
fi

# === Execute ===
bash "$PLUGIN_DIR/scripts/convert-to-bare.sh" --project-root "$PROJECT_ROOT"
```

※ Failure triggers automatic rollback. Backup is kept at `.git-backup/`.

## Workflow C: Cleanup

### Step 1: List worktrees

Run this **complete** Bash block to detect and list:

```bash
# === Inline Detection ===
TOPLEVEL=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$TOPLEVEL" ]; then
  echo "ERROR: Not in a git repository" >&2; exit 1
elif [ -f "$TOPLEVEL/.git" ]; then
  GIT_COMMON=$(cd "$TOPLEVEL" && git rev-parse --git-common-dir)
  BARE_DIR=$(cd "$TOPLEVEL" && cd "$GIT_COMMON" && pwd)
  PROJECT_ROOT=$(dirname "$BARE_DIR")
else
  PROJECT_ROOT="$TOPLEVEL"
fi

# === List ===
git -C "$PROJECT_ROOT" worktree list
```

### Step 2: Select target
Use AskUserQuestion to ask which worktree(s) to remove.

### Step 3: Execute

Run this **complete** Bash block. Replace `{WORKTREE_PATH}` with the selected path, or use `--all`:

```bash
# === PLUGIN_DIR Resolution ===
PLUGIN_DIR=$(find ~/.claude/plugins/cache -maxdepth 6 -path "*/git-worktree-plugin/*/scripts/create-and-open.sh" 2>/dev/null \
  | sed 's|/scripts/create-and-open.sh||' \
  | sort -V \
  | tail -1)
if [ -z "$PLUGIN_DIR" ]; then
  _SKILL_SCRIPTS=$(find ~/.agents/skills -maxdepth 4 -path "*/git-worktree/scripts/create-and-open.sh" 2>/dev/null | head -1)
  [ -n "$_SKILL_SCRIPTS" ] && PLUGIN_DIR=$(dirname "$_SKILL_SCRIPTS")/..
fi
if [ -z "$PLUGIN_DIR" ]; then echo "ERROR: Plugin scripts not found" >&2; exit 1; fi

# === Inline Detection ===
TOPLEVEL=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$TOPLEVEL" ]; then
  echo "ERROR: Not in a git repository" >&2; exit 1
elif [ -f "$TOPLEVEL/.git" ]; then
  GIT_COMMON=$(cd "$TOPLEVEL" && git rev-parse --git-common-dir)
  BARE_DIR=$(cd "$TOPLEVEL" && cd "$GIT_COMMON" && pwd)
  PROJECT_ROOT=$(dirname "$BARE_DIR")
else
  PROJECT_ROOT="$TOPLEVEL"
fi

# === Execute (choose one) ===
# Single worktree:
bash "$PLUGIN_DIR/scripts/cleanup-worktree.sh" \
  --project-root "$PROJECT_ROOT" \
  --path "{WORKTREE_PATH}"

# All worktrees:
# bash "$PLUGIN_DIR/scripts/cleanup-worktree.sh" \
#   --project-root "$PROJECT_ROOT" \
#   --all
```

## Format Rules

- Feature names: lowercase, spaces/underscores → dashes
- Branch format: `{prefix}/{feature-name}` (e.g., `feat/user-authentication`)
- PR format: `pr-{number}` (e.g., `pr-123`)
- Worktree path: `./trees/{branch-name}` (customizable)
