# Status Dashboard (derived, no stored file)

Printed when `/writing-tasks` runs with every spec already mapped. Everything is queried from `gh` at runtime — nothing is persisted, so it can never drift.

## Query

```bash
gh issue list -R <owner>/<repo> --state all --limit 200 \
  --json number,title,state,assignees,labels,parent,blockedBy,blocking,updatedAt
```

Group by `parent` (issues with no parent and no sub-issues are standalone). Spec-level rollup comes from each spec's `issue:` frontmatter.

## Output format

```
📊 Progress: X / Y closed (Z%)

   phase-1-foundation  → #301   ████████░░░░  6/12
   phase-2-auth        → #340   ██░░░░░░░░░░  2/9
   (standalone)                 ███░░░░░░░░░  1/3

🔵 In progress (N):
   #314  아바타 업로드 end-to-end        @me · 2일 전 갱신

✅ Ready to start (N):          ← open, every blocked-by closed
   #315  프로필 삭제 + 정리 잡

⚡ Suggested parallel lanes (only when >= 2 ready):
   Lane A: #315            → touches lib/profile/
   Lane B: #322 #323       → touches server/api/

⚠️  Blocked (N):
   #316 waiting on #314

⚠️  Mismatches (only if any):
   spec phase-2-auth/02-token-refresh.md: status wip, parent #345 closed
```

## Computing "ready"

An issue is ready when it is **open** and every entry in `blockedBy` is **closed**. That is the whole rule — no local status file, no derived state to keep in sync.

## Computing "in progress"

Whatever the repo already uses: an assignee, or the repo's own in-progress label (`gh label list`). Don't impose a new convention on a repo that already has one.

## Computing parallel lanes

For the ready set:

1. Read each issue's checklist, extract file paths / module directories.
2. Group by shared top-level module directory.
3. Same group → same lane (sequential). Different groups → different lanes (parallel).
4. Flag when two lanes touch the same directory.
