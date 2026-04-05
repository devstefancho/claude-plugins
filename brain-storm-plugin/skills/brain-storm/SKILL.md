---
name: brain-storm
description: Brainstorm future features and improvements based on the current codebase. This is the ideation step BEFORE writing specs (/writing-specs). Use when user asks to brainstorm ideas, generate feature ideas, explore improvements, or mentions 브레인스톰, 아이디어, 기능 제안, 개선 아이디어, 뭐 만들까, 앞으로 뭐 하지. Also trigger for cleanup requests like 브레인스톰 정리, 구현된 아이디어 정리. Proactively trigger when the user wants creative exploration of what COULD be built.
allowed-tools: Read, Write, Glob, Grep, Bash, AskUserQuestion
context: fork
agent: general-purpose
---

# Brain Storm

`/writing-specs`로 스펙을 작성하기 전 단계. 사용자가 전달한 아이디어를 바탕으로 추가적이고 구체적인 아이디어를 도출한다. 아이디어마다 대략적인 wireframe을 포함하여 구현 방향을 시각화하고, 선정된 아이디어를 `brain-storm/` 디렉토리에 마크다운으로 저장한다.

## Two Modes

이 스킬은 두 가지 모드로 동작한다. 사용자 요청에 따라 적절한 모드를 선택한다.

- **Brainstorm Mode** (기본): 아이디어 생성 & 저장. "브레인스톰 해줘", "아이디어 내줘" 등
- **Cleanup Mode**: 이미 구현된 아이디어 감지 & 삭제. "브레인스톰 정리", "구현된 거 삭제" 등

## Principles

1. **Explore before proposing** - 코드베이스를 먼저 파악한 뒤 아이디어를 제안한다. 실제 코드에 기반한 아이디어가 훨씬 유용하다.
2. **Diverge then converge** - 먼저 여러 아이디어를 자유롭게 생성(최소 3개)한 뒤, 사용자가 선택한다.
3. **One idea = one file** - 각 아이디어는 별도 파일로 관리한다. 내용이 매우 적은 경우(bullet 3개 이하)에만 합칠 수 있다.
4. **Always wireframe** - 모든 아이디어에 대략적인 wireframe을 포함한다. 화면 관련 아이디어는 상세한 UI wireframe을, 백엔드/인프라 아이디어는 아키텍처 다이어그램이나 데이터 플로우를 ASCII로 그린다.
5. **Prune the implemented** - Cleanup Mode에서 기존 아이디어가 이미 구현되었는지 확인하고 정리한다.

## Directory Rules

- Ideas live in `brain-storm/` at the project root
- File format: `brain-storm/{name}.md` or `brain-storm/{subdir}/{name}.md`
- Only 1-depth subdirectories allowed (e.g., `brain-storm/auth/sso-login.md` OK, `brain-storm/auth/v2/sso.md` NOT OK)
- Filenames: lowercase-with-hyphens (e.g., `dark-mode-toggle.md`)
- Create subdirectories only when user requests grouping or 5+ ideas share a domain

---

## Brainstorm Mode

### Step 1: Scan & Ideate

First understand the codebase, then generate ideas:

1. Run `Glob` on key directories (`src/**`, `app/**`, `pages/**`, `components/**`, `lib/**`, etc.) to map project structure
2. Run `Glob brain-storm/**/*.md` to list existing brainstorm ideas
3. Read `package.json`, `README.md`, or equivalent to understand tech stack
4. Generate 3-5 ideas based on the scan. For each, present:
   - **Title** (as H3)
   - **Description**: 1-2 sentences
   - **Complexity**: Low / Medium / High
   - **Quick wireframe sketch**: 3-5 lines of ASCII to give a visual sense of the idea
5. Ask the user: "어떤 아이디어를 저장할까요? 번호로 선택하세요 (여러 개 가능). 수정하거나 새로운 아이디어를 추가할 수도 있습니다."

Ideas should be grounded in the actual codebase (reference specific files/patterns), actionable, and varied in scope.

### Step 2: Deduplicate & Write

For each selected idea:

1. Extract 3-5 key nouns from the title/description
2. Run `Grep` across `brain-storm/**/*.md` for those keywords
3. If duplicate found, ask: "이미 유사한 아이디어가 존재합니다: `{path}`. 업데이트할까요, 새로 생성할까요, 건너뛸까요?"
4. Read the idea template: [templates/idea-template.md](templates/idea-template.md)
5. Read the wireframe guide: [templates/wireframe-guide.md](templates/wireframe-guide.md)
6. Fill in all sections:
   - **Summary**: 1-2 sentences
   - **Motivation**: 2-4 sentences referencing specific codebase parts
   - **Proposed Approach**: 3-7 bullet points (no code snippets)
   - **Wireframe**: ASCII art in fenced code block, minimum 10 lines. For UI ideas: screen layout with interactive elements. For non-UI ideas: architecture diagram, data flow, or system interaction diagram.
   - **Complexity**: Low/Medium/High with 1-sentence justification
   - **Open Questions**: 1-3 bullets
7. Write to the appropriate path under `brain-storm/`

### Step 3: Report

After writing all idea files, output a summary report directly (no separate file needed):

```
## Brain Storm Report

| Field | Value |
|-------|-------|
| Action | Created / Updated |
| Ideas Proposed | {count} |
| Ideas Saved | {count} |

### Saved Ideas
| File | Title | Complexity |
|------|-------|-----------|
| `{path}` | {title} | {complexity} |

### Next Steps
- 스펙으로 발전시키려면: /writing-specs {idea title}
```

The report is part of the final response message, not a separate file. This ensures it always gets delivered.

---

## Cleanup Mode

Triggered by: "브레인스톰 정리", "구현된 아이디어 정리", "clean up brainstorm"

### Step 1: Detect Implemented Ideas

1. Run `Glob brain-storm/**/*.md` to list all idea files
2. For each idea:
   a. Read the file, extract title + summary
   b. Extract 3-5 implementation-indicator keywords (component names, function names, route paths, API endpoints)
   c. Run `Grep` for those keywords in source code (exclude `brain-storm/`, `specs/`, `node_modules/`, `.git/`)
   d. Mark as **implemented** if 3+ keywords match in source code AND the code actually implements the described functionality (not just naming coincidence or TODOs)

### Step 2: Confirm & Delete

1. Present findings to user: "다음 아이디어가 이미 구현된 것으로 보입니다:"
   - For each implemented idea: show file path, matched evidence (which files/functions matched)
2. Ask: "삭제할까요? (전체/선택적/취소)"
3. Delete only after user confirmation
4. Report results:

```
## Cleanup Report

| Idea | Status | Evidence |
|------|--------|----------|
| `{path}` | Implemented (deleted) | {matched files} |
| `{path}` | Not implemented (kept) | - |
```
