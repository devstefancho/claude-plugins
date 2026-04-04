---
name: writing-specs
description: Write and manage spec files with search, conflict detection, and reporting. Use when user asks to create a spec, update a spec, write a spec, or mentions 스펙 생성, 스펙 업데이트, 스펙 작성, 스펙 만들어줘. Proactively trigger whenever the user's request involves specification documents, even if they don't explicitly say "spec".
allowed-tools: Read, Write, Glob, Grep, Bash, AskUserQuestion
context: fork
agent: general-purpose
---

# Writing Specs

Manages spec files in `specs/` directory with conflict detection and concise reporting.

## Principles

1. **Template-driven** - Every spec follows the exact template structure. Never add extra sections or freestyle content. This prevents specs from becoming bloated documents that nobody reads.
2. **Search first** - Always search for existing specs before creating or updating. This catches duplicates, conflicts, and outdated specs early.
3. **One spec = one task** - Each spec covers a single unit of work. If a request spans multiple concerns, split into separate specs.
4. **Concise by default** - Each section has strict limits: Purpose (1-2 sentences), Requirements (max 5 bullets), Approach (2-5 sentences, no code), Verification (max 5 bullets).
5. **Report everything** - Every operation ends with a structured report so the user knows exactly what happened.

## Directory Rules

- Specs live in `specs/` at the project root
- File format: `specs/{name}.md` or `specs/{subdir}/{name}.md`
- Only 1-depth subdirectories allowed (e.g., `specs/api/auth.md` is OK, `specs/api/v2/auth.md` is NOT)
- Filenames use lowercase-with-hyphens (e.g., `jwt-authentication.md`)
- Create subdirectories only when the user explicitly requests grouping or when there are 5+ specs that share a clear category

## Workflow

### Phase 1: Search (mandatory)

Before any create or update operation, search for existing specs:

1. Run `Glob specs/**/*.md` to list all existing spec files
2. Extract 3-5 key nouns from the user's request (skip generic words like "system", "feature", "add", "update")
3. Run `Grep` for each keyword across all found spec files
4. Classify results:
   - **Exact match**: A spec covering the same topic already exists
   - **Related**: A spec shares 2+ keywords or covers an adjacent topic
   - **Outdated**: A spec references files/paths that no longer exist (verify with `Glob`)

If no `specs/` directory exists yet, skip search and proceed to Phase 3.

### Phase 2: Decision

Based on search results:

- **No related specs found** → Proceed to create
- **Exact match found** → Ask user: "이미 동일한 스펙이 존재합니다: `{path}`. 업데이트할까요, 새로 생성할까요, 아니면 취소할까요?"
- **Related specs found** → Show list and ask: "관련 스펙이 발견되었습니다. 어떻게 진행할까요?"
- **Outdated specs found** → Inform user and offer to update: "다음 스펙이 outdated 상태입니다 (참조 파일 없음). 함께 업데이트할까요?"

Use `AskUserQuestion` for all user decisions.

### Phase 3: Write

1. Read the spec template: [templates/spec-template.md](templates/spec-template.md)
2. Fill each section based on the user's request, strictly following the template structure
3. Write to the appropriate path under `specs/`
4. If updating an existing spec, preserve any content the user didn't ask to change

Section constraints (enforced, not suggested):
- **Purpose**: Exactly 1-2 sentences. No bullet points.
- **Requirements**: 3-5 bullet points. Each bullet is one concrete requirement.
- **Approach**: 2-5 sentences in paragraph form. No code snippets.
- **Verification**: 2-5 bullet points. Each describes a testable scenario.

### Phase 4: Outdated Cleanup

If outdated specs were found in Phase 1:
- For each outdated spec, check what references are broken
- Propose specific updates (do NOT auto-modify)
- Only update after user confirmation

### Phase 5: Report

Read the report template and fill it in: [templates/report-template.md](templates/report-template.md)

Output the completed report as the final message. This is how the user sees what happened.

- **Action**: "Created" or "Updated"
- **File**: Full relative path from project root
- **Title**: The spec's H1 title
- **Search Results**: List each related/outdated spec found, or "No related specs found"
- **Changes**: For updates, summarize what changed. For new specs, say "New spec created"
- **Next Steps**: One actionable suggestion (e.g., "Run implementation" or "Review related spec at specs/auth.md")
