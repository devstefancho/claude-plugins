# Decomposition Rules

Detail for the decomposition flow in SKILL.md (Scan → Propose → Gate → Create → Report).

## Sizing — how many issues per spec

Read each unmapped spec and decide:

- **S (< 200 lines, one concern)** → a single issue, no parent/child. Don't build a hierarchy for one piece of work.
- **M / L (multiple sections, many files)** → parent issue + N sub-issues (one per major section / milestone). If ambiguous, ask.
- A step that is not independently verifiable → **checklist line in the parent body**, not a sub-issue.

### Cut vertically, not by layer

Each issue is a **tracer bullet**: a thin slice through every layer it touches (schema → API → UI), demoable on its own, sized to one agent context. Layer-shaped issues can't be verified alone and force a big-bang integration at the end.

**WRONG:** `add DB columns` · `add API endpoints` · `wire the UI`
**RIGHT:** `profile name editable end-to-end` · `avatar upload end-to-end`

### Wide refactors are the exception

A change that touches many call sites has no meaningful vertical slice. Decompose it as **expand → migrate → contract**:

1. **expand** — add the new API alongside the old one; nothing breaks yet.
2. **migrate** — move call sites over in batches, one issue per batch, each `--blocked-by <expand>`. Batches are independent, so they form parallel lanes.
3. **contract** — delete the old API; blocked by every migrate issue.

## Dependency inference — the four signals

For each proposed issue, infer prerequisites from:

1. **Phase order** — work in earlier spec phases defaults as a candidate prerequisite.
2. **Spec body parsing** — grep the spec for references to other specs, and for "requires", "선행", "depends on", "…한 뒤".
3. **Spec frontmatter inheritance** — if the spec declares `depends_on`, carry it over to the parent issue.
4. **Shared module heuristic (flag only)** — two pieces touching the same module path → flag as "potential sequential" and require confirmation. **Never auto-decide from this signal.**

Existing open issues in the target repo are also candidate prerequisites — search before proposing, and wire to a real issue instead of inventing a duplicate.

## Preview table format

Show the graph and the lanes before touching anything:

```
Spec: specs/phase-3-profile/01-profile-editing.md  → owner/repo (parent: new)
  P   profile editing 전체                        parent
  1   프로필 이름 인라인 편집 end-to-end            blocked-by: —
  2   아바타 업로드 end-to-end                     blocked-by: 1        [signal: spec body "이름 편집 후"]
  3   프로필 삭제 + 정리 잡                        blocked-by: 1, #248  [cross-repo: 이벤트 테이블 선행]
  ⚠ 5·6은 sub-issue 아님 → 부모 본문 체크리스트

Lanes: A=[1→2]  B=[3 (after 1)]   ← 1 완료 후 2·3 병렬
```

Then ask `proceed / edit / cancel`. On `edit`, adjust the graph interactively and re-print.

## Create step detail

- Topological order: an issue is created only after every prerequisite has a number.
- Parent first (`gh issue create … `), then each sub-issue with `--parent <n> --blocked-by <…>`.
- Labels: reuse the repo's existing labels (`gh label list`). If a global routing rule requires an app/area label, apply it. Never invent a new label taxonomy as a side effect of decomposition.
- After creation: write `issue: <owner>/<repo>#<parent>` into the spec frontmatter, and verify the graph once with `gh issue view <parent> --json blockedBy,blocking,subIssues`.

## Parallel lanes

Lanes are derived from the graph, not stored: repeatedly take the set of issues whose prerequisites are all closed; split that ready-set by the module paths their checklists touch (same module → same lane, different modules → parallel lanes). Report lanes as a suggestion; never assign them.

## Report format

```
✅ Decomposition complete
   Spec:      specs/phase-3-profile/01-profile-editing.md  (backlink written)
   Parent:    owner/repo#312  https://github.com/owner/repo/issues/312
   Sub-issues: #313 #314 #315   (checklist-only items: 2)
   Graph:     314←313, 315←313  (verified)
   Lanes:     A=[313→314]  B=[315]
   Reused:    #248 (existing, wired as prerequisite)
```

## Non-interactive defaults

If interactive questions are unavailable (auto mode, headless, scheduled run), use these defaults and echo every defaulted decision in the report.

| Decision point | Default | Rationale |
|---|---|---|
| Decomposition proposal (`proceed/edit/cancel`) | **Stop and report the plan — do not create.** | Issue creation is outward-facing; a wrong graph costs cleanup in a shared tracker. |
| Target repo when routing is ambiguous | The repo the spec's doc-root maps to; if none, stop. | Wrong-repo issues are worse than none. |
| Prerequisite unclear between two pieces | Declare them independent and note the risk. | An over-serialized graph silently kills parallelism. |
| Manual `/writing-tasks new` | **Refuse**: "manual issue creation requires interactive input." | Intent-heavy; defaulting produces wrong graphs. |
