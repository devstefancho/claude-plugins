---
name: writing-tasks
description: Decomposes specs into GitHub issues — one parent issue per spec plus sub-issues, with the dependency graph expressed as blocked-by/blocking relations and parallel lanes derived from that graph. Use when user mentions task 분리, task 생성, task 쪼개기, spec을 task로, 이슈로 분해, decompose, writing-tasks, 병렬 작업 편성, 의존성 그래프. 그리고 이 세션에서 `gh issue create` 를 두 건 이상 만들려 할 때는 손으로 만들지 말고 반드시 이 스킬을 먼저 부른다 — 부모 자식 관계와 blocked-by 가 붙지 않은 이슈 묶음은 나중에 순서를 복원할 수 없다 (30일간 이슈 72건 중 53건이 관계 없이 손으로 생성된 실측). Also trigger when a specs/ directory has specs with no tracking issue.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Writing Tasks

Decompose specs into **GitHub issues**: one parent issue per spec, sub-issues for the pieces, dependencies as issue relations. Progress, lanes, and graphs are queried from `gh` — never stored in a file.

## Hard Rules

- **Issues are the only SSOT.** Never create `tasks/` files, `tasks/README.md`, or status scripts in the repo. A tracked work item that isn't an issue doesn't exist. (Reading a repo's pre-existing `tasks/` md: [legacy-md-mode.md](legacy-md-mode.md).)
- **Preview, then create.** 첫 `gh issue create` 앞에 분해 전체(부모, sub-issue, 의존 그래프, 병렬 레인)를 한 번 출력한다. 사용자가 이미 착수를 승인한 흐름이면 출력 직후 바로 만들고 결과를 사후 보고한다(전역 규칙: 가역 판단은 실행 후 보고). 사용자가 아직 방향을 정하지 않았거나 기존 이슈를 닫거나 다시 쓰는 작업이 섞여 있으면 그때만 멈추고 답을 기다린다. 탐색 중에는 절대 만들지 않는다.
- **Search before create.** `gh issue list --search` on the spec title and each proposed piece; an existing open issue is reused (link it), never duplicated.
- **Dependencies are mandatory and explicit.** Every sub-issue declares its prerequisites via `--blocked-by`, or is consciously declared independent. Never leave it unstated. GitHub maintains the inverse (`blocking`) automatically — no write-through bookkeeping, but verify once after creation.
- **Route to the owning repo.** Issues live in the repo the work belongs to. If the work spans repos or has no obvious home, follow the user's global routing rule (many setups designate a meta tracker repo for cross-cutting work). Ask only when routing is genuinely ambiguous.
- **One issue : one spec.** The parent issue links exactly one spec. Work that would span two specs is a boundary error — re-scope the specs, never list two. See [examples.md](examples.md).
- **Write the backlink.** After creating the parent, set `issue: <owner>/<repo>#N` in the spec's frontmatter. This is the only place the spec↔issue link is recorded. `issue:` 에는 이슈를 정확히 하나만 적는다. 스펙 하나가 이슈 둘을 필요로 하면 스펙 경계가 잘못 그어진 것이니 스펙을 쪼갠다. 관련 이슈는 스펙 본문에서 참조한다.

## Layout

```
<doc-root>/<repo>/specs/phase-N-slug/NN-slug.md   ← input (writing-specs; repo 밖 2급 문서)
        │  frontmatter: issue: owner/repo#123
        ▼
owner/repo#123   parent issue   "<spec title>"       labels: spec
        ├── #124 sub-issue  "…"   blocked-by: —
        ├── #125 sub-issue  "…"   blocked-by: #124
        └── #126 sub-issue  "…"   blocked-by: #124
```

- **Specs are external.** Resolve the specs root the same way `writing-specs` does: an external doc-root (`<doc-root>/<repo-name>/specs/`) when the user's global rules map 2nd-class docs there, else repo-local `specs/`.
- **Sub-issue vs checklist item.** A piece that is independently verifiable and worth its own branch/session → sub-issue. Anything smaller → a `- [ ]` checklist line in the parent body. Don't mint issues for one-line steps.
- **Ids are issue numbers.** No `N.NN` scheme; cross-repo references use `owner/repo#N` (문서 표기용. gh 인자로는 같은 repo 면 번호, 다른 repo 면 전체 URL 만 받는다 — `owner/repo#N` 을 `--add-blocked-by` 에 주면 "invalid issue format" 으로 실패한다, 2026-08-18 실측).
- Issue field mapping, body skeletons, and validation: [issue-schema.md](issue-schema.md).

## Commands

Only two user-facing commands. Everything else is derived.

### `/writing-tasks` (no args) — smart dispatch

| State | Action |
|---|---|
| Specs with no `issue:` backlink | Propose decomposition, await approval, create issues |
| All specs mapped, work in progress | Print the status dashboard ([dashboard.md](dashboard.md)) |
| Mapped but the parent issue is closed while the spec is `wip` | Report the mismatch; ask which side is right |
| All issues closed | Print `All done.` + one-line suggestion (next phase, or flip spec status to `done`) |

### `/writing-tasks new <description>` — manual issue

For ad-hoc work without a spec (hotfixes, refactors):

1. Confirm the target repo (routing rule above).
2. `gh issue list` the open issues; ask which are prerequisites (multi-select) → `--blocked-by`.
3. None selected → re-confirm "Is this truly independent (no prerequisites)?" — explicit opt-in required.
4. Create with labels; report the URL. No spec backlink (that's what makes it ad-hoc).

## Decomposition (primary path)

Sizing rules, the four dependency-inference signals, preview format, and `gh` command shapes: [decomposition.md](decomposition.md).

1. **Scan** — glob the specs root; read each spec's frontmatter; a spec with no `issue:` is unmapped. Cross-check with `gh issue list --json number,title,body` in case a backlink was never written.
2. **Propose** — split each unmapped spec into pieces, infer prerequisites from the four signals, print the preview table with the inference trail (which signal → which dependency) and the suggested parallel lanes.
3. **Gate** — ask `proceed / edit / cancel`. On `edit`, adjust the graph interactively. **Never call `gh issue create` before this gate.**
4. **Create** — parent first, then sub-issues with `--parent` and `--blocked-by` (dependency-topological order so prerequisites already have numbers). Then write `issue:` into the spec frontmatter.
5. **Report** — parent + sub-issue URLs, the dependency graph, suggested lanes, and any reused-existing-issue notes.

- [ ] Preview approved (or non-interactive default applied and echoed in the report)
- [ ] 생성 후 그래프 확인: `gh issue view <parent> -R <owner>/<repo> --json subIssues,blockedBy --jq '{sub: [.subIssues.nodes[].number], blocked: [.blockedBy.nodes[].number]}'` (`subIssues`·`blockedBy` 는 배열이 아니라 `{nodes, totalCount}` 객체다 — 두 세션이 여기서 두 턴씩 잃었다)

## Incremental updates (re-runs)

- New spec → new parent + sub-issues; never touch existing issues.
- Modified spec → **never silently rewrite issue bodies.** Ask: "Spec `X` changed. Add follow-up sub-issues / update the parent body?" showing the diff.
- Deleted spec → report its parent issue as orphaned; never auto-close.
- Closed issue → never reopen or rewrite on resync unless the user asks.

## Worktree integration

Inside a worktree branched for an issue (`issue-123-*`, `123-slug`, …): parse the number, print that issue's checklist as "Next up", and offer to move it to in-progress (assign `@me` / apply the in-progress label the repo uses). The in-session working set is the session's own job (the retired `live-tasks` skill used the built-in TaskList, removed in Claude Code 2.1.233).

## Anti-patterns

**WRONG:** write `tasks/*.md` or a progress dashboard file to track work "because it's easier to read".
**RIGHT:** query `gh` on demand ([dashboard.md](dashboard.md)) — one state, no drift.

**WRONG:** create issues while still exploring the spec, then close the wrong ones.
**RIGHT:** preview the whole graph, get approval once, create in one pass.

## Boundaries

This skill only decomposes and wires issues. Specs come from `writing-specs` (the natural pair). 구현과 spec status 갱신은 이 스킬 밖이고, 머지 뒤 문서 정합은 `reconcile-docs` 가 맡는다. Non-development or non-tracked personal todos are out of scope — they belong wherever the user's routing rule puts them. Keep outputs tight: the dashboard fits on one screen.
