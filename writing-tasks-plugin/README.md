# writing-tasks-plugin

Persistent task files from specs, with dependency graph and dynamic progress.

Natural pair of [`writing-specs-plugin`](../writing-specs-plugin): specs go in, tasks come out.

## What it does

- Decomposes `specs/phase-N/NN-name.md` into `tasks/phase-N-slug/NN-name.md`
- Enforces explicit dependencies on every task (no orphans)
- Derives progress, "ready to start" list, and parallel lane suggestions dynamically from task files
- Zero shared files under `tasks/` — each task is its own file so parallel worktrees never collide

## Commands

Two commands. Everything else is computed.

```
/writing-tasks              # smart dispatch: decompose new specs OR show status
/writing-tasks new <desc>   # manual task (ad-hoc hotfix/refactor)
```

## Layout

```
specs/
  phase-1/01-monorepo-setup.md
  phase-3/02-profile-api-delete.md
tasks/
  phase-1-foundation/
    01-monorepo-setup.md        # id: 1.01
  phase-3-profile/
    02-profile-api-delete.md    # id: 3.02
```

- Phase number cumulates across sprints (never resets)
- Local task number resets per phase (`01`, `02`, ...)
- Task id = `{phase}.{local}` — unambiguous cross-phase reference

## Frontmatter

```yaml
---
id: "3.02"
phase: 3
title: "DELETE /api/users/me"
spec: "specs/phase-3/02-profile-api-delete.md"
depends_on: ["3.01", "2.04", "5.03"]
blocks: []
estimate: "M"
status: "todo"
owner: ""
sprint: ""
---
```

## Why persistent files instead of a single TODO.md

- Every worktree touches at most one task file → zero merge collisions for parallel work
- History of what was planned, what changed, what landed is self-contained per task
- `grep`/`glob` over task files gives any query you need (no separate DB)

## Why no `README.md` or `DEPENDENCIES.md` under `tasks/`

Shared files under `tasks/` create merge conflicts when multiple worktrees run in parallel. Progress, lanes, and the dependency graph are derived at query time from task frontmatter — no stored state to go stale.

## Install

```bash
/plugin marketplace add .
/plugin install writing-tasks-plugin@devstefancho-claude-plugins
```

## Related

- [`writing-specs-plugin`](../writing-specs-plugin) — writes the specs this plugin decomposes
- [`git-worktree-plugin`](../git-worktree-plugin) — create worktrees named `task-N.NN-*` for parallel work
- [`implement-with-test-plugin`](../implement-with-test-plugin) — implement a task's spec with tests
