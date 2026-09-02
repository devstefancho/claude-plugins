# Issue Schema & Validation

What a decomposed issue looks like, how the graph is expressed, and what is checked before creation.

## Field mapping (the old task frontmatter → issue fields)

| Concept | Issue field | How |
|---|---|---|
| id | issue number | assigned by GitHub; cross-repo = `owner/repo#N` |
| title | issue title | one line, imperative, no `[phase-N]` prefixes |
| spec backlink | first body line | `spec: <specs-root>/phase-N-slug/NN-slug.md` + the spec's `issue:` frontmatter (both directions) |
| parent / phase | sub-issue relation | `gh issue create --parent <parent#>` |
| depends_on | `blocked-by` | `--blocked-by 124,125` (create) / `gh issue edit N --add-blocked-by 124` |
| blocks | `blocking` | **derived** — GitHub sets the inverse automatically; never maintain by hand |
| estimate | label | the repo's existing size labels if any; otherwise omit — don't invent a label taxonomy |
| status | open/closed + repo's own labels | never a body field |
| owner | assignee | |
| completed_at | closedAt | queried, never written |

## Body skeleton

Parent and sub-issue bodies come from [templates/issue-body.md](templates/issue-body.md). The parent carries the spec link, the sub-issue index, and any checklist items too small to be issues; each sub-issue carries its own dependency reasoning, checklist, and definition of done.

## Validation (before creating anything)

Reject the proposal and re-plan if any fail:

- **Cycle** — the proposed `blocked-by` graph must be acyclic (topological sort must succeed; it's also the creation order).
- **Phantom spec** — the `spec:` path must exist.
- **Phantom dependency** — every prerequisite must be either an already-existing issue number or another issue in this same proposal.
- **Duplicate** — `gh issue list --search "<title>" --state all` returns an equivalent open issue → reuse it (wire the relation) instead of creating.
- **Missing dependency declaration** — a piece with no prerequisites must be *declared* independent, not silently defaulted.

Warn (non-blocking):

- Parent issue closed while its spec's `status:` is not `done` (or the reverse) — surface, never auto-fix.
- Sub-issue with no checklist and no definition of done — it's probably a checklist line, not an issue.
- More than ~8 sub-issues under one parent — the spec is likely two specs.

## gh command shapes

```bash
# parent
gh issue create -R <owner>/<repo> --title "<spec title>" --body-file <parent.md> --label <labels>

# sub-issue with prerequisites (topological order — prerequisites exist first)
gh issue create -R <owner>/<repo> --title "<piece>" --body-file <sub.md> \
    --parent <parent#> --blocked-by <n1>,<n2>

# wire a relation after the fact
gh issue edit <n> -R <owner>/<repo> --add-blocked-by <m>
# 크로스 repo 의존은 owner/repo#N 이 아니라 전체 URL 로만 받는다
gh issue edit <n> -R <owner>/<repo> --add-blocked-by "https://github.com/<owner>/<other>/issues/<m>"

# verify the graph
gh issue view <parent#> -R <owner>/<repo> --json subIssues,blockedBy \
    --jq '{sub: [.subIssues.nodes[].number], blocked: [.blockedBy.nodes[].number]}'   # subIssues·blockedBy 는 {nodes,totalCount} 객체
```

`--parent`, `--blocked-by`, `--blocking`, and `--add-sub-issue` require a recent `gh` (≥ 2.90). If they're unavailable, fall back to a parent-body checklist with `- [ ] #124` lines and state the degradation in the report — never silently drop the graph.
