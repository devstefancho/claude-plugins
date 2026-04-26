# Skills/Plugins 정리 작업 (2026-04-26)

> 작업 목적: 최근 1개월(2026-03-26 ~ 2026-04-26) 실제 사용 데이터를 근거로 필수 스킬만 플러그인화하고, 사용 흐름(워크플로) 기반으로 카테고리를 재구성한다.

## 1. 최근 1개월 사용 빈도

### 1.1 데이터 출처
- `~/wiki/raw/obsidian-notes/daily/2026-03-26 ~ 2026-04-26.md` (25개 파일)
- 추출 방식
  - **slash 호출 수**: 세션 종료 노트의 "최근 작업" 항목 안에 인용된 `"/<name>"` 토큰 카운트
  - **이름 멘션 수**: 본문 내 스킬/플러그인 이름이 등장한 건수 (작업 디렉토리 worktree명에 포함된 것 포함 — 노이즈 있음)

### 1.2 슬래시 커맨드 호출 횟수 (Top, Claude built-in 제외)

| 커맨드 | 호출 수 | 출처 |
|---|---|---|
| `/tmux-open` | 32 | user skill (~/.claude/skills) |
| `/devstefancho:test-commit-push-pr-clean` | 25 | test-commit-push-pr-clean-plugin |
| `/implement` | 13 | simple-sdd-plugin |
| `/agent-team-plugin:create-team` | 12 | agent-team-plugin |
| `/hermes:chat` | 11 | hermes |
| `/writing-specs` | 9 | writing-specs-plugin |
| `/agent-team-plugin:cleanup-team` | 9 | agent-team-plugin |
| `/loop` | 8 | (built-in skill) |
| `/commit-commands:commit` | 8 | commit-commands (official) |
| `/hermes:setup` | 5 | hermes |
| `/create-team` | 4 | agent-team-plugin (alias) |
| `/skill-creator:skill-creator` | 3 | skill-creator (official) |
| `/simplify` | 3 | (built-in skill) |
| `/implement-with-test` | 3 | implement-with-test-plugin |
| `/impeccable:shape` | 3 | impeccable |
| `/wrap-up` | 2 | user skill |
| `/playwright-cli` | 2 | user skill |
| `/impeccable:impeccable` | 2 | impeccable |
| `/impeccable:critique` | 2 | impeccable |
| `/codex:review` | 2 | codex |
| `/advisor` | 2 | (built-in) |
| `/llm-wiki-plugin:llm-wiki` | 1 | llm-wiki-plugin |
| `/impeccable:{quieter,polish,harden,distill,clarify,adapt}` | 각 1 | impeccable |
| `/brain-storm` | 1 | brain-storm-plugin |
| `/agent-team-plugin:expand-team` | 1 | agent-team-plugin |
| `/pick-up` | 1 | user command |
| `/vault-sync` | 1 | (deprecated user skill) |
| `/schedule` | 1 | (built-in) |

### 1.3 이름 멘션 (대화 본문 — 슬래시 호출이 아닌 자연어 트리거)

| 이름 | 멘션 수 | 비고 |
|---|---|---|
| agent-team | 84 | worktree 경로 포함, 실제 사용 12+9+1=22 |
| hermes | 52 | 프로젝트명 포함 — 실제 사용 11+5+1=17 |
| computer-use | 41 | 컴퓨터 유즈 작업 빈번 |
| tmux-open | 40 | slash 32 + 자연어 트리거 |
| test-commit-push-pr-clean | 27 | slash 25 + α |
| impeccable | 20 | slash 13건 + 멘션 |
| llm-wiki | 16 | 개발 중 (활발) |
| writing-specs | 12 | slash 9 + α |
| playbook | 10 | user skill |
| skill-creator | 9 | |
| playwright-cli | 9 | |
| brain-storm | 10 | (brain-storm 1 + brain-storm-plugin 8 + brain-storm 1) |
| task-manager | 6 | `/td` |
| simplify | 3 | |
| codex | 3+ | |

## 2. 필수/비필수 분류

### 2.1 필수 (Daily Driver — 매일 또는 주 1회 이상)
1. **agent-team-plugin** — `/create-team`, `/cleanup-team`, `/expand-team` (worktree+플래너+구현자 팀 생성)
2. **test-commit-push-pr-clean-plugin** — 작업 마무리 표준 워크플로 (lint→test→commit→push→PR→cleanup)
3. **commit-commands** (official) — `/commit`, `/commit-push-pr` (단순 커밋)
4. **simple-sdd-plugin** — `/implement`, `/plan`, `/spec`, `/tasks` — SDD 워크플로
5. **hermes** — Hermes Agent 통신 (SSH 모드, Slack 전송)
6. **writing-specs-plugin** — `/writing-specs` 스펙 문서 작성
7. **brain-storm-plugin** — 신규 아이디어 발산 + UI 프로토타입
8. **llm-wiki-plugin** — wiki ingest/query (개발 중이지만 적극 사용)
9. **impeccable** — 디자인 강화 (`shape`, `critique`, `impeccable`, `polish` 등 자주 호출)
10. **agent skills (user-level)**: `tmux-open`, `playbook`, `task-manager`, `wrap-up`, `pick-up`, `playwright-cli`, `wiki-sync`, `daily-report`
11. **skill-creator** (official) — 스킬 신규/개선 시 사용
12. **codex** — Codex 리뷰/구원 호출

### 2.2 가끔 사용 (월 1~3회)
- **implement-with-test-plugin** — 테스트 포함 구현 (필요 케이스에서만)
- **computer-use-plugin** — 앱 QA 시나리오 실행 (특정 프로젝트에서만)
- **git-worktree-plugin** — 단독 사용은 거의 없음 (agent-team이 wraps)
- **smart-commit-plugin** — 큰 변경 분리 시
- **frontend-plugin** — 컴포넌트 리뷰 (impeccable과 중첩)
- **scaffold-claude-feature** — `/prime` (신규 플러그인 시작 시)

### 2.3 미머지 / 미공개 (마켓 미등록)
- **writing-tasks-plugin** — `.claude/worktrees/great-payne-d2902f/writing-tasks-plugin/` 에 존재
  - spec→task 분해, 의존성 그래프, 병렬 lane 추천. split-work 직전 단계
  - `marketplace.json` 미등록 → 정식 설치 불가, daily 로그 1회는 워크트리 내부 테스트로 추정
  - **결정 필요**: (a) main 머지 + 마켓 등재 (b) writing-specs-plugin에 통합 (c) 폐기

### 2.4 미사용 / 사용 0회 (제거 또는 통합 후보)
- **code-style-plugin** — 0회 (impeccable/frontend-plugin과 중복)
- **code-quality-plugin** — 0회 (코드 리뷰는 impeccable/codex로 대체)
- **spec-manager-plugin** — 0회 (writing-specs-plugin과 중복)
- **session-reporter-plugin** — 0회 (worktrace-plugin과 중복)
- **worktrace-plugin** — 0회 (wiki-sync로 대체됨)
- **work-journal-plugin** — 0회 (wiki에 흡수됨)
- **pr-create-plugin** — 0회 (commit-commands:commit-push-pr로 대체)
- **git-commit-plugin** — 0회 (commit-commands로 대체)
- **stop-notification-plugin** — 직접 호출 없음 (백그라운드 hook)
- **common-mcp-plugin** — 직접 호출 없음 (MCP 제공만, 유지)
- **local-test-plugin** — 0회 (개발 도구, 유지)

## 3. 스킬 워크플로 (사용 순서)

### 3.1 신규 기능 개발 흐름 (Idea → Ship)

```
[1. 아이디어]      brain-storm
                       ↓
[2. 스펙]          writing-specs (또는 simple-sdd:spec)
                       ↓
[3. 태스크 분해]   writing-tasks (★ 미머지)  /  simple-sdd:tasks
                       ↓
[4. 병렬 분기]     split-work (user skill)
                       ↓
[5. 구현]          implement-with-test  /  agent-team:create-team (대형)
                       ↓
[6. 디자인 강화]   impeccable:shape → critique → refine (UI 작업 시)
                       ↓
[7. 리뷰]          codex:review / impeccable:critique
                       ↓
[8. 커밋·배포]     test-commit-push-pr-clean (또는 commit-commands:commit-push-pr)
                       ↓
[9. 정리]          wrap-up → pick-up (다음 세션)
```

### 3.2 일상 워크플로 (주 보조)

```
세션 시작:    pick-up   (이전 세션 컨텍스트 복원)
탐색:         playbook (`/pb`)
관리:         task-manager (`/td`), tmux-open
종료:         wrap-up
주기 정리:    daily-report, wiki-sync (자동)
```

### 3.3 외부 통신/위임

```
Codex 위임:   codex:rescue / codex:review
Hermes 위임:  hermes:chat / hermes:run / hermes:jobs
브라우저:     playwright-cli, browser-walkthrough
```

## 4. impeccable.style 방식 카테고리 (동사 기반 6 그룹)

impeccable은 23개 커맨드를 6 카테고리로 묶었다 (`Create / Evaluate / Refine / Simplify / Harden / System`). 동일한 동사 중심 분류를 사용자 스킬에 적용한다.

### 4.1 Create — 새로 만든다
- `brain-storm-plugin:brain-storm`
- `brain-storm-plugin:ui-prototype-preview`
- `simple-sdd-plugin:spec`, `plan`, `tasks`, `implement`
- `writing-specs-plugin:writing-specs`
- `writing-tasks-plugin:writing-tasks` (미머지)
- `agent-team-plugin:create-team` (팀 생성)
- `scaffold-claude-feature:prime` (신규 플러그인 부트스트랩)
- `skill-creator` (스킬 자체 생성)
- `youtube-episode` (콘텐츠 생성)

### 4.2 Evaluate — 평가한다
- `codex:review`
- `impeccable:critique`, `impeccable:audit`
- `frontend-plugin:component-design-reviewer`
- `code-style-plugin`, `code-quality-plugin` (퇴역 후보)

### 4.3 Refine — 개선한다 (단일 차원)
- `impeccable:{shape, polish, layout, typeset, colorize, animate, delight, bolder, quieter}`
- `simplify` (글로벌)

### 4.4 Simplify — 줄인다
- `impeccable:{distill, clarify, adapt}`
- `simplify`
- `fewer-permission-prompts`

### 4.5 Harden — 출시 준비
- `impeccable:harden`, `impeccable:optimize`
- `implement-with-test-plugin:implement-with-test`
- `test-commit-push-pr-clean-plugin:test-commit-push-pr-clean`
- `commit-commands:{commit, commit-push-pr, clean_gone}`
- `chrome-extension-testing`
- `computer-use-plugin:computer-use-test`

### 4.6 System — 시스템/운영
- `agent-team-plugin:{expand-team, cleanup-team}`
- `hermes:{setup, chat, run, jobs, status}`
- `codex:{setup, rescue}`
- `llm-wiki-plugin:llm-wiki`, `wiki-sync`
- `update-config`, `keybindings-help`
- `tmux-open`, `task-manager`, `playbook`
- `pick-up`, `wrap-up`, `daily-report`
- `git-worktree-plugin:git-worktree`
- `vault-hub-workspace`, `vault-sync-workspace`
- `loop`, `schedule`
- `claude-api`, `playwright-cli`, `browser-walkthrough`
- `find-skills`

## 5. 결론 — 플러그인 마켓 슬림화 제안

**유지(Core)**: agent-team, test-commit-push-pr-clean, simple-sdd, writing-specs, brain-storm, implement-with-test, llm-wiki, hermes, computer-use, common-mcp, scaffold-claude-feature, local-test, stop-notification(hook)

**아카이브(Deprecate)**:
- code-style-plugin, code-quality-plugin → impeccable + codex로 대체
- spec-manager-plugin → writing-specs로 통합
- session-reporter-plugin, worktrace-plugin, work-journal-plugin → wiki-sync로 통합
- pr-create-plugin, git-commit-plugin → commit-commands(official)로 대체
- frontend-plugin → impeccable로 대체

**카테고리 디렉토리 재구성 (선택)**:
```
plugins/
├── create/       brain-storm, simple-sdd, writing-specs, scaffold
├── evaluate/     (codex, impeccable는 외부)
├── harden/       implement-with-test, test-commit-push-pr-clean, computer-use
├── system/       agent-team, hermes, llm-wiki, common-mcp, stop-notification
└── _archived/    code-style, code-quality, spec-manager, session-reporter, ...
```
