---
name: llm-wiki
description: Maintain an LLM-powered personal wiki from raw sources. Use when user mentions wiki init, wiki ingest, wiki query, wiki lint, wiki update, 위키 초기화, 위키 추가, 위키 질문, 위키 검사, 위키 업데이트, or wants to build a knowledge base from sources.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, AskUserQuestion
context: fork
agent: general-purpose
---

# LLM Wiki

Manages an LLM-maintained personal wiki using the 3-layer architecture (raw sources → wiki pages → schema). The wiki compiles knowledge from raw sources into interconnected markdown pages that accumulate over time.

Read [PRINCIPLES.md](PRINCIPLES.md) for linking rules, frontmatter conventions, and immutability rules.

## Phase 0: Config Discovery

Every operation starts here. Find the wiki root path.

1. Determine the plugin install directory (where this SKILL.md lives)
2. Check if `config.json` exists in the plugin root (2 levels up from SKILL.md):
   - **Exists**: Read `wiki_root` value
   - **Not exists**: Ask user with `AskUserQuestion`:
     > 위키 루트 경로를 설정해주세요. 모든 위키 도메인이 이 경로 하위에 생성됩니다.
     > 기본값: `~/wiki`
   - Create `config.json` with the user's answer: `{ "wiki_root": "<path>" }`
3. Expand `~` to absolute path

```json
// config.json
{ "wiki_root": "~/wiki" }
```

## Phase 1: Domain Discovery

After config is loaded, find the target wiki domain.

1. Run `Glob {wiki_root}/*/SCHEMA.md` to find all domains
2. **No domains found**:
   - If operation is `init` → proceed to init
   - Otherwise → inform user: "위키가 없습니다. 먼저 `wiki init`을 실행해주세요."
3. **One domain found**: Use it automatically
4. **Multiple domains found**: Ask user to select with `AskUserQuestion`:
   > 여러 위키 도메인이 있습니다. 어떤 도메인에서 작업할까요?
   > 1. {domain_1}
   > 2. {domain_2}
5. Read `SCHEMA.md` of selected domain for conventions
6. Set `{domain_path}` = `{wiki_root}/{domain}` — all subsequent paths in operations are relative to this absolute path

## Operation: init

Creates a new wiki domain under the wiki root.

### Steps

1. Ensure Phase 0 is complete (config.json exists)
2. Ask user with `AskUserQuestion`:
   > 새 위키 도메인을 생성합니다.
   > - **도메인명** (디렉토리명으로 사용, lowercase-with-hyphens): 
   > - **도메인 설명** (한 줄):
   > - **소스 유형** (예: papers, articles, videos, code):
3. Create directory structure:
   ```
   {wiki_root}/{domain}/
   ├── SCHEMA.md
   ├── raw/
   └── wiki/
       ├── index.md
       ├── overview.md
       ├── log.md
       └── pages/
   ```
4. Generate files from templates:
   - `SCHEMA.md` ← [templates/schema-template.md](templates/schema-template.md) (fill domain, description, source types, today's date)
   - `wiki/index.md` ← [templates/index-template.md](templates/index-template.md) (fill domain, today's date)
   - `wiki/overview.md` ← [templates/overview-template.md](templates/overview-template.md) (fill domain, description, today's date)
   - `wiki/log.md` ← initial content:
     ```markdown
     # Wiki Log
     
     Append-only operation record.
     
     ---
     
     ## [{today}] init | {domain}
     - Wiki created at `{wiki_root}/{domain}/`
     ```
5. Report to user:
   > ✅ 위키 도메인 `{domain}` 생성 완료
   > - 경로: `{wiki_root}/{domain}/`
   > - 다음 단계: `wiki ingest <source>` 로 소스를 추가하세요

## Operation: ingest

Processes a new source and integrates it into the wiki.

### Steps

1. **Accept source** — determine source type from user input:
   - File path → `Read` the file
   - URL → `WebFetch` the content. If WebFetch unavailable, ask user to paste content
   - Pasted text → use directly
2. **Save raw source**:
   - Generate slug from source title (see PRINCIPLES.md slug rules)
   - **Text/markdown content** → save to `{domain_path}/raw/{slug}.md` with metadata header:
     ```markdown
     ---
     source_url: {url_if_applicable}
     ingested: {today}
     type: {article|paper|video|code|note}
     ---
     
     {full_source_content}
     ```
   - **Binary files (PDF, images)** → copy original to `{domain_path}/raw/{slug}.{ext}` preserving format, then create a companion `{domain_path}/raw/{slug}.meta.md` with the metadata header above (content field = file path reference)
3. **Surface takeaways** — present to user with `AskUserQuestion`:
   > 📖 **{source_title}** 분석 완료
   >
   > **핵심 포인트:**
   > 1. {takeaway_1}
   > 2. {takeaway_2}
   > 3. {takeaway_3}
   >
   > **관련 엔티티/개념:** {entity_list}
   >
   > 강조하거나 제외할 내용이 있나요? (없으면 Enter)
4. **Write source summary page**:
   - Use [templates/page-template.md](templates/page-template.md)
   - `type: source`
   - Include: URL/path, ingest date, 2-3 paragraph synthesis, key takeaways, entity/concept links
5. **Update entity/concept pages**:
   - For each entity/concept mentioned in the source:
     - `Grep` for existing page in `{domain_path}/wiki/pages/`
     - **Exists**: Read page, append source to `sources` frontmatter, add new information to content, update `updated` date
     - **Not exists**: Create new page with `type: entity` or `type: concept`
6. **Bidirectional backlink audit** (CRITICAL):
   - For every `[[slug]]` in newly created/updated pages:
     - Read target page
     - If target doesn't link back → add `[[new-slug]]` to target's Related section
   - `Grep` all files in `{domain_path}/wiki/pages/` for mentions of entities/concepts from the new source that lack `[[links]]`
   - Add missing wikilinks
7. **Update index.md**:
   - Read current `{domain_path}/wiki/index.md`
   - Add entry under appropriate category (Sources/Entities/Concepts):
     `- [[{slug}]] — {one-line summary} _(ingested {today})_`
   - Update Recent section with latest 5 entries
8. **Update overview.md**:
   - Read current `{domain_path}/wiki/overview.md`
   - If new source shifts understanding: update Key Themes, add Open Questions
   - Update Statistics counts
   - Update `updated` frontmatter date
9. **Append to log.md** (no user confirmation needed):
   ```markdown
   ## [{today}] ingest | {source_title}
   - Pages created: [[{slug1}]], [[{slug2}]]
   - Pages updated: [[{slug3}]], [[{slug4}]]
   - Backlinks added: {count}
   ```
10. **Report**:
    > ✅ **{source_title}** ingest 완료
    > - 소스 페이지: `[[{slug}]]`
    > - 생성된 페이지: {count}개
    > - 업데이트된 페이지: {count}개
    > - 추가된 백링크: {count}개

## Operation: query

Searches the wiki and synthesizes an answer with citations.

### Steps

1. **Index scan**:
   - Read `{domain_path}/wiki/index.md` completely
   - Identify relevant pages from the user's question
   - Prioritize wiki content over general knowledge
2. **Page retrieval**:
   - Read full content of identified pages
   - Follow `[[cross-references]]` up to 2 hops where relevant
   - Build comprehensive context
3. **Synthesize answer**:
   - Ground all claims in wiki sources using inline `[[slug]]` citations
   - Note agreements/disagreements between pages
   - Explicitly flag gaps: "위키에 {topic}에 대한 내용이 없습니다"
   - Format appropriately: prose for facts, tables for comparisons, numbered steps for procedures
4. **Offer archival** with `AskUserQuestion`:
   > 이 답변을 위키 페이지로 저장할까요?
   > 제안 slug: `{suggested-slug}`
   - **Yes**: Create page with `type: concept`, tags `[query, analysis]`, run mini-ingest (update index, log, backlinks)
   - **No**: Log only:
     ```
     ## [{today}] query | {question_summary} (not filed)
     ```

## Operation: lint

Audits wiki health and offers fixes.

### Steps

1. **Build inventory**:
   - `Glob {domain_path}/wiki/pages/*.md` for all pages
   - Read `{domain_path}/wiki/index.md` and `{domain_path}/wiki/overview.md`
   - Collect: all slugs, all `[[slug]]` references, all frontmatter fields
2. **Run checks**:

   **🔴 Errors** (must fix):
   - Broken links: `[[slug]]` with no corresponding file
   - Missing frontmatter: absent `title`, `slug`, `type`, `created`, or `updated`
   - Invalid slug: not lowercase-with-hyphens

   **🟡 Warnings** (should fix):
   - Orphan pages: zero inbound links (exclude index, overview)
   - Missing backlinks: A→B exists but B→A doesn't
   - Stale pages: `updated` older than 90 days with temporal language ("current", "latest", "recent")

   **🔵 Info**:
   - Missing concept pages: entity/concept mentioned 3+ times without dedicated page
   - Index gaps: pages exist but not listed in index.md

3. **Output report**:
   > 📋 **Wiki Lint Report** ({today})
   >
   > **Pages scanned:** {count}
   >
   > 🔴 **Errors ({count})**
   > {error_list}
   >
   > 🟡 **Warnings ({count})**
   > {warning_list}
   >
   > 🔵 **Info ({count})**
   > {info_list}

4. **Offer fixes** with `AskUserQuestion`:
   > 자동 수정 가능한 항목이 {count}개 있습니다. 수정할까요?
   > - Broken links 제거/수정
   > - Missing backlinks 추가
   > - Index 누락 항목 추가
   > - Missing frontmatter 채우기
   - If accepted: apply fixes, report what changed
   - If declined: skip

5. **Append to log.md**:
   ```
   ## [{today}] lint | {error_count} errors, {warning_count} warnings, {info_count} info
   Fixed: {list_of_fixes_or_none}
   ```

## Operation: update

Revises wiki pages when knowledge changes or contradictions arise.

### Steps

1. **Identify targets**:
   - From user's request: specific page names, topics, or from lint recommendations
   - `Grep` to locate relevant pages in `{domain_path}/wiki/pages/`
2. **Propose changes**:
   - For each target page, show:
     > **{page_title}** (`[[{slug}]]`)
     > - 현재: `{current_text}`
     > - 변경: `{proposed_text}`
     > - 이유: {reason}
   - Wait for user confirmation via `AskUserQuestion`
3. **Apply edits**:
   - Use `Edit` to modify pages
   - Update `updated` frontmatter date to today
4. **Contradiction check**:
   - `Grep` all pages for claims related to the updated content
   - Flag conflicting assertions
   - Offer to update those pages too
5. **Update metadata**:
   - Revise index.md summary if the page's purpose changed
   - Update overview.md if the update shifts overall understanding
6. **Append to log.md**:
   ```
   ## [{today}] update | [[{slug1}]], [[{slug2}]]
   Reason: {explanation}
   Changes: {brief_summary}
   ```

## Operation Detection

Parse user intent into an operation:

| User says | Operation |
|-----------|-----------|
| "wiki init", "위키 초기화", "위키 만들어" | init |
| URL, file path, "ingest", "위키 추가", "이거 읽어줘" | ingest |
| Question about wiki content, "wiki query", "위키에서 찾아줘" | query |
| "wiki lint", "위키 검사", "위키 건강 체크" | lint |
| "wiki update", "위키 수정", specific page + change intent | update |

If ambiguous, ask with `AskUserQuestion`:
> 어떤 작업을 할까요?
> 1. ingest — 새 소스 추가
> 2. query — 위키에서 검색
> 3. lint — 위키 건강 검사
> 4. update — 페이지 수정
