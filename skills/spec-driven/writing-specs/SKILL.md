---
name: writing-specs
description: Writes and manages spec files in specs/ with mandatory duplicate search, conflict detection, and a structured final report. Use when user asks to create a spec, update a spec, write a spec, or mentions 스펙 생성, 스펙 업데이트, 스펙 작성, 스펙 만들어줘. Proactively trigger whenever the request involves specification documents, even if the user never says spec.
allowed-tools: Read, Write, Glob, Grep, Bash, SendMessage
context: fork
agent: general-purpose
---

# Writing Specs

Manage spec files in `specs/` with conflict detection and a concise final report.

## Hard Rules

- **Template-driven.** 네 절(Purpose·Requirements·Approach·Verification)은 [templates/spec-template.md](templates/spec-template.md) 의 순서와 이름 그대로 반드시 있고 각 절의 분량 제한을 지킨다. 앱의 사용자 기능 스펙이면 `## 이벤트 맵`과 `## 판정`도 채운다(사용자 표준). 그 뒤에 번호 붙인 상세 절을 더하는 것은 다른 세션이 스펙만 보고 구현해야 할 때만 허용하고, 그 경우 Phase 5 보고에 "인계용 상세 절 N개 추가"라고 적는다.
- **Search before write.** Never create or update a spec without running Phase 1.
- **One spec = one task.** A request spanning multiple concerns becomes multiple specs.
- **Never auto-modify outdated specs.** Propose updates in the report; never apply.
- **이 스킬은 fork 로 돌아 사용자에게 직접 물을 수 없다.** Phase 2 결정은 [non-interactive.md](non-interactive.md) 기본값을 적용하고, 되돌릴 수 없는 갈림길(기존 스펙 덮어쓰기)만 부모 세션에 `SendMessage` 로 한 번 묶어 확인한 뒤 진행한다. 포크 19회 실측에서 `AskUserQuestion` 호출은 0회였다 (skills-internal#25).
- **Always end with the report.** No silent operations.

## Directory Rules

- **Resolve the specs root first.** If the user's global rules (e.g. a `work-routing` rule) map this repo's 2nd-class docs to an external docs repo, the specs root is `<external-root>/<repo-name>/specs/` — **not** repo-local `specs/`. Otherwise it is `specs/` at the project root. Every rule below (phase dirs, naming, auto-pick, search) applies relative to the resolved root. The directory-structure SSOT is `check-doc-structure/golden_manifest.py` (shared with `writing-tasks`, `scaffold-new-app`, `reconcile-docs`); filenames are lowercase-with-hyphens.
- **A leftover repo-local `specs/` is read-only legacy** once the external root is in play: include it in the Phase 1 search, write new specs only to the external root, and note the split in the report. Never bulk-move it. Decision records (`docs/adr/`, `CONTEXT.md`) always stay in-repo.
- **Default path: `specs/phase-N-slug/NN-name.md`** — one phase dir per milestone; the spec→work handoff is carried by the `issue:` backlink, not by a parallel directory.
  - `phase-N`: 1-indexed milestone number, monotonically increasing across the project, never reset.
  - `slug`: short human-readable milestone name. **Required — never bare `phase-1`.** Example: `phase-1-foundation`.
  - `NN`: 2-digit index within the phase, starting at `01`. Example: `specs/phase-1-foundation/01-jwt-authentication.md`. Never use other prefixes (e.g. `T1-`).
  - phase 디렉토리 안에는 `NN-slug.md` 스펙 파일만 둔다. 디자인 캔버스, 이미지, 데이터 같은 자산은 `<doc-root>/<repo>/assets/` 아래로 보내고 스펙 본문에서 경로로 참조한다.
- Flat alternatives (`specs/{name}.md`, `specs/{subdir}/{name}.md`) only for projects with no phase structure. Max 1-depth subdirectories; create subdirs or new phases only on explicit request, or when 5+ specs share a clear category.
- **Decision records do not live under `specs/`.** Durable trade-offs → `docs/adr/`; lightweight decisions → `docs/decisions.md`. Never create `decisions.md` (or `00-overview.md`) inside a `specs/phase-*` dir.

Worked layout example (a phase with multiple specs; one concern per spec): [examples.md](examples.md).

Auto-pick phase + NN when the user does not specify:

1. `Glob specs/phase-*/` — no phases → start `phase-1-<slug>` (derive a short slug from the spec topic).
2. Use the highest existing phase dir, unless the user signals a new milestone → create `phase-{N+1}-<slug>` (slug 가 불분명하면 부모 세션에 묻는다).
3. `Glob specs/phase-N-*/*.md` — new spec gets highest existing `NN` + 1, zero-padded.
4. Spec belongs to a clearly different milestone? 부모 세션에 phase number + slug 를 묻고, 답이 없으면 non-interactive 기본값(활성 phase 에 `NN+1`)으로 간다.

## Phase 0 — Resolve the input

| Argument shape | Resolution |
|---|---|
| `brain-storm/**.md` path | `Read` it. `Summary` / `Motivation` / `Proposed Approach` become the spec source; the idea title becomes the spec H1. |
| Any other markdown path | `Read` it; its content is the spec source. |
| Bare title or keyword | `Glob brain-storm/**/*.md`, match H1 (case-insensitive) then filename slug. One match → use it. Multiple → non-interactive 기본값(H1 정확 일치, 없으면 파일명 순 첫 번째). Zero → treat as freestyle. |
| Freestyle text, or no argument | Use conversation context (fork 는 부모 컨텍스트를 물려받는다). Empty → 부모 세션에 `SendMessage` 로 소스를 요청하고, 답이 없으면 non-interactive 기본값대로 거부 보고. |

From a brain-storm source: `Summary` seeds `Purpose`; `Proposed Approach` bullets seed `Requirements` (prune to 3-5 concrete items) and the prose `Approach`. `Wireframe` and `Open Questions` are NOT copied — list them under "Carried over" in the report.

- [ ] Input resolved to exactly one source

## Phase 1 — Search (mandatory)

1. `Glob specs/**/*.md` to list all spec files.
2. Extract 3-5 key nouns from the request (skip generic words like "system", "feature", "add", "update").
3. `Grep` each keyword across the found specs. Bash `grep` 을 대신 쓰지 않는다 — 사용자 셸의 grep 이 ugrep 이라 `--include` 가 조용히 실패한 회차가 있다.
4. Classify: **Exact match** (same topic) · **Related** (2+ shared keywords or adjacent topic) · **Outdated** (references files that no longer exist — verify with `Glob`).

No `specs/` directory yet → skip to Phase 3.

## Phase 2 — Decide

- No related specs → proceed to create.
- Exact match → ask: "이미 동일한 스펙이 존재합니다: `{path}`. 업데이트할까요, 새로 생성할까요, 아니면 취소할까요?"
- Related specs → show the list and ask: "관련 스펙이 발견되었습니다. 어떻게 진행할까요?"
- Outdated specs → "다음 스펙이 outdated 상태입니다 (참조 파일 없음). 함께 업데이트할까요?"

위 질문 문구는 부모 세션에 `SendMessage` 로 한 번에 묶어 보내고(질문 4개 이하), 답이 없으면 [non-interactive.md](non-interactive.md) 기본값으로 진행하며 Phase 5 보고에 기본값 적용 사실을 적는다.

## Phase 3 — Write

1. Read [templates/spec-template.md](templates/spec-template.md) and fill it strictly.
2. Resolve the destination with the auto-pick rules above; write under `specs/`.
3. Set the `status` frontmatter — `planned` for a new spec; on update, reflect the real implementation state (`wip` / `done` / `held` / `legacy`). This is the only field the project roadmap is derived from, so keep it honest. frontmatter 는 `status` 와 `issue` 두 필드뿐이다. `title`, `created` 같은 필드를 더하지 않고, `issue:` 는 항상 `<owner>/<repo>#N` 정식 형 하나만 쓴다. 기존 스펙 파일을 형식 표본으로 삼지 말고 항상 템플릿을 읽는다 (주석 복사 13건·추가 필드 3건·짧은 형 8건 실측).
4. Leave `issue:` empty on creation. It records the tracking issue (`<owner>/<repo>#N`) and is written by `writing-tasks` when the spec is decomposed — a spec that has left `planned` without an `issue:` is untracked work, and the structure detector flags it.
5. On update, preserve every section the user did not ask to change.

**Never write a roadmap or index file** (`specs/README.md`, `STATUS.md`, etc.). The phase roadmap is derived on demand from `status` frontmatter — so it never drifts and never collides across worktrees:

```bash
python3 "$(readlink -f ~/.claude/skills/writing-specs)/../check-doc-structure/check_doc_structure.py" <repo> --roadmap
```

Section limits (enforced, not suggested): **Purpose** 1-2 sentences, no bullets · **Requirements** 3-5 bullets, one concrete requirement each · **Approach** 2-5 sentences, no code · **Verification** 2-5 testable bullets.

## Phase 4 — Outdated cleanup

For each outdated spec found in Phase 1: identify the broken references, propose specific updates, apply only after user confirmation. **Never auto-modify.**

## Phase 5 — Report

Fill [templates/report-template.md](templates/report-template.md) and output it as the final message: Action (Created/Updated), File (relative path), Title (spec H1), Search Results (each related/outdated spec, or "No related specs found"), Changes ("New spec created" or update summary), Next Steps (one actionable suggestion).

## Non-interactive mode

이 스킬은 항상 fork 라 사용자에게 직접 묻지 못한다. 결정은 [non-interactive.md](non-interactive.md) 기본값을 적용하고, 기본값으로 처리한 결정을 전부 Phase 5 보고에 적는다. 스펙을 쓰기 전에 확정이 필요한 항목이 있으면 부모 세션에 `SendMessage` 로 한 번만 묶어 물어라(질문 4개 이하). 작성 도중 부모가 추가 결정을 보내면 이미 쓴 절을 고쳐 반영하고, 반영한 항목을 보고의 "부모 전달 반영" 줄에 적는다.

## 호출자에게

이 스킬은 fork 로 백그라운드에서 돈다. 부르고 나서 완료 알림을 기다리지 않고 같은 주제의 이슈 생성이나 구현을 진행하면, 스펙이 도착해도 쓰이지 않는다(포크 17회 중 완주하고도 보고가 묻힌 발동 4회 실측). 스펙이 뒤 작업의 입력이라면 알림을 받고 파일을 확인한 뒤에 다음 단계로 넘어간다. 부모가 이미 스펙에 필요한 맥락을 다 들고 있으면 fork 를 띄우지 말고 이 문서의 Phase 1부터 5까지를 부모 세션에서 그대로 실행한다 — 띄웠다가 중단하면 절 제한과 보고 규격이 함께 사라진다.
