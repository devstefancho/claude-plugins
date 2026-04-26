---
description: 플러그인 개발을 위한 프로젝트 구조와 규칙을 세션에 주입합니다
---

# Prime - 플러그인 개발 지식 주입

새 세션에서 플러그인/스킬/커맨드를 만들기 위한 프로젝트 지식을 빠르게 로드합니다.

<context>
현재 마켓플레이스 상태를 확인합니다:
!`cat .claude-plugin/marketplace.json`: 등록된 플러그인 목록 확인
</context>

---

## 1. 레포지토리 구조

플러그인은 카테고리별로 분류됩니다:

| 카테고리 | 플러그인 |
|----------|----------|
| **코드 리뷰** | `code-style-plugin`, `code-quality-plugin`, `frontend-plugin` |
| **워크플로우** | `simple-sdd-plugin`, `spec-manager-plugin` |
| **Git** | `git-commit-plugin`, `pr-create-plugin`, `git-worktree-plugin` |
| **유틸리티** | `session-reporter-plugin`, `stop-notification-plugin`, `common-mcp-plugin` |
| **메타** | `scaffold-claude-feature` |

---

## 2. 플러그인 구성요소

### 표준 디렉토리 구조

```
plugin-name/
  .claude-plugin/plugin.json   (필수)
  commands/                     (선택)
  skills/                       (선택)
  agents/                       (선택)
  hooks/                        (선택)
  .mcp.json                     (선택)
  README.md                     (권장)
```

### plugin.json 스키마

```json
{
  "name": "kebab-case-name",
  "description": "설명",
  "version": "X.Y.Z",
  "author": { "name": "Author Name" }
}
```

### marketplace.json 등록 형식

```json
{
  "name": "plugin-name",
  "source": "./plugin-name",
  "description": "설명"
}
```

---

## 3. Slash Command 작성법

### Frontmatter 필드

- `description` (필수): 커맨드 설명
- `argument-hint` (선택): UI에 표시되는 인자 힌트 (예: `"[requirements]"`)
- `allowed-tools` (선택): 사전 승인 도구 목록 (예: `Bash(git status:*), Bash(git diff:*)`)

### XML 태그 패턴

| 태그 | 역할 |
|------|------|
| `<context>` | 동적 정보 수집. `!`command`` 로 bash 실행, `@filepath`로 파일 참조 |
| `<instruction>` | 수행할 단계별 절차 |
| `<important>` | 반드시 지켜야 할 제약/규칙 |
| `<examples>` | 출력 형식 예시 |

### 인자 변수

- `$ARGUMENTS`: 전체 인자를 단일 문자열로
- `$1`, `$2`, `$3`: 개별 위치 인자

### 파일 참조와 bash 실행

- `@src/app.js`: 파일 내용 참조
- `` !`git status` ``: bash 명령 실행 (allowed-tools에 해당 도구 필요)

---

## 4. Skill 작성법

**핵심 원칙: Progressive Disclosure를 항상 적용할 것.**

### Frontmatter 필드

- `name` (필수): kebab-case, 디렉토리명과 일치
- `description` (필수): **트리거 메커니즘** - "Use when..." 패턴으로 활성화 조건 명시
- `allowed-tools` (선택): 도구 제한 (생략 시 모든 도구 상속)

### Progressive Disclosure 3단계 구조

| 단계 | 파일 | 역할 | 로딩 시점 |
|------|------|------|----------|
| Tier 1 | `SKILL.md` | 핵심 정의, 지시사항, 체크리스트 | 스킬 활성화 시 |
| Tier 2 | `EXAMPLES.md` | 좋은 예 vs 나쁜 예 비교 | 예시 필요 시 |
| Tier 3 | `PRINCIPLES.md` | 원칙 상세 설명, 위반 패턴 | 심층 참조 시 |

### 구현 메커니즘

```markdown
## 참고 문서
자세한 예시는 [EXAMPLES.md](EXAMPLES.md) 참고
상세 원칙은 [PRINCIPLES.md](PRINCIPLES.md) 참고
```

- 마크다운 링크로 참조 → Claude가 필요할 때만 파일 로드
- SKILL.md만으로 독립 동작 가능하게 설계
- 지원 문서는 선택적 심화 자료

### description 작성 팁

- ✅ `"코드 리뷰 및 품질 분석. 코드 리뷰가 필요할 때 사용"`
- ❌ `"코드 리뷰 도구"`

---

## 5. Subagent 작성법

- 단일 마크다운 파일: `agents/agent-name.md`
- frontmatter: `name`, `description`, `tools` (skills의 allowed-tools와 다름!), `model` (sonnet/opus/haiku/inherit)
- `"use proactively"` 키워드를 description에 포함하면 자동 호출 활성화

---

## 6. 기타 컴포넌트

### Hooks

- `hooks/hooks.json` 형식
- 주요 이벤트: `PreToolUse`, `PostToolUse`, `Stop` 등
- `${CLAUDE_PLUGIN_ROOT}` 변수로 플러그인 루트 경로 참조

### MCP 서버

- 플러그인 루트에 `.mcp.json` 배치
- `mcpServers` 키로 서버 정의

### Output Styles

- `.claude/output-styles/style-name.md` 위치
- `keep-coding-instructions` frontmatter로 코딩 지시 유지 가능

---

## 7. 개발 워크플로우

```
1. /prime 실행 → 프로젝트 지식 로드
2. 만들고 싶은 것 설명 → scaffold-claude-feature 스킬이 구조 생성
3. 생성 완료 후 → Claude Code agent로 검토
4. 테스트: /plugin uninstall → 수정 → /plugin install → 재시작
```

---

<instruction>
위 컨텍스트와 지식을 확인한 후:
1. 현재 등록된 플러그인 수와 카테고리 요약을 출력
2. "세션이 프라이밍되었습니다" 확인 메시지 출력
3. 다음 단계 안내: 새 기능이 필요하면 scaffold-claude-feature 스킬 활용
</instruction>

<important>
- 이 명령은 지식 주입 전용입니다. 파일을 생성하거나 수정하지 않습니다.
- 새 기능 생성이 필요하면 scaffold-claude-feature 스킬을 활용하세요.
- 신규 스킬 생성 시 항상 Progressive Disclosure 방식을 권장합니다:
  SKILL.md (핵심) → EXAMPLES.md (예시) → PRINCIPLES.md (원칙)
- 신규 컴포넌트(스킬, 커맨드, 플러그인) 생성 후에는 반드시 Claude Code agent를 사용하여 검토하세요:
  - 구조가 올바른지 (frontmatter 필드, 디렉토리 구조)
  - 기존 패턴과 일관성이 있는지
  - progressive disclosure가 적절히 적용되었는지
  - description 필드에 트리거 키워드가 포함되어 있는지
- 참고 자료: scaffold-claude-feature/skills/scaffold-claude-feature/references/ 디렉토리에 각 기능 타입별 상세 레퍼런스 존재
- 플러그인 설치 후 반드시 Claude Code를 재시작해야 적용됩니다
</important>
