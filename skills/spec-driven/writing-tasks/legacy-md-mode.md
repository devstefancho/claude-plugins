# Legacy `tasks/` md — read-only mode

Repos that predate issue-SSOT carry a `tasks/` directory of one-file-per-task markdown. This is how to read it and what to do with it. **The forward mode is issues only** ([SKILL.md](SKILL.md)); nothing here creates or updates md.

## Migration policy (decided — do not re-litigate per repo)

1. **Leave it in place.** No bulk move, no bulk delete, no conversion pass. Git history and cross-links stay intact, and a migration that touches every repo buys nothing.
2. **Read-only.** Never write a new task md, never edit an existing one to reflect progress. New tracked work is an issue, in the owning repo.
3. **Promote on touch.** When work described by an *open* legacy task (`status:` todo / in_progress / doing / review / blocked) actually resumes, create the issue then — and only then. Add `issue: <owner>/<repo>#N` to the md's frontmatter and set `status: legacy`. One line, no rewrite.
4. **Done stays done.** A `status: done` task is a completed record. It is never promoted, never migrated, never deleted — it's the archive.
5. **Never resurrect the directory.** If `tasks/` is absent, do not create it, not even "just for this one".

The structure detector reports legacy inventory (file count, open count) as its own bucket — informational, not a violation. Repos with a large open-legacy count are simply the ones where step 3 will fire most often.

## Reading a legacy task file

Frontmatter that older files carry:

```yaml
id: "N.NN"          # phase.local — replaced by the issue number
phase: N
title: "…"
spec: "specs/phase-N-slug/NN-name.md"
depends_on: ["N.NN", …]     # → blocked-by
blocks: ["N.NN", …]         # → blocking (derived on GitHub; ignore when promoting)
estimate: "S" | "M" | "L"
status: "todo" | "in_progress" | "review" | "done" | "blocked"
completed_at: ""
```

Body sections: `## 의존성` · `## 사전 준비` · `## 구현 체크리스트` · `## Definition of Done` · `## 리스크 / 메모`.

## Promoting one legacy task to an issue

1. Confirm it's genuinely open (status + does the code already do it?). Stale "todo" that is actually implemented → mark `status: done` in the md instead, and stop.
2. Map the fields: title → title, body sections → the sub-issue skeleton in [templates/issue-body.md](templates/issue-body.md), `depends_on` → `--blocked-by` **for prerequisites that are themselves issues** (a prerequisite still living as a done md needs no relation).
3. Create the issue, then append `issue: <owner>/<repo>#N` and flip `status: legacy` in the md. Don't restructure the file.
4. Report the promotion — one line per task, with both the md path and the issue URL.

Promote one at a time, on demand. A bulk promotion of an old backlog just moves stale items into a tracker where they are harder to ignore.
