---
name: session-resume
description: Locates a previous Claude Code or Codex CLI session's JSONL transcript and prints metadata (title, first/last prompt, branch) plus the last N conversation turns so work can continue. Use when the user says "resume", "이어가자", "이전 세션 내용 보여줘", "what was I working on", or provides a session UUID.
allowed-tools: Bash, Read
---

# Session Resume

Surface a previous session's metadata (title, first/last prompt, branch, cwd, last activity) and its last N conversation turns, then continue the work intelligently.

## Phase 1 — Run the helper

The script sits next to this SKILL.md; with the standard symlink install it is:

```bash
bash ~/.claude/skills/session-resume/scripts/resume.sh [SESSION_ID] [-n N] [--all] [--list [K]] [--global]
```

| Invocation | Behavior |
|---|---|
| (no args) | Most recent **previous** session for this project — sessions active in the last 2 min (usually the one you are in) are skipped automatically |
| `<uuid-or-substring>` | That specific session (Claude Code or Codex); multiple matches → candidate list, re-run with a longer UUID |
| `-n N` | Last N conversation turns (default 10; fewer shown if the session has fewer text turns). Text turns only — tool activity, tool results, system reminders, and skill/command injections are filtered or compacted to one-liners (`[command] /clear`, `[skill] name`, `⚙ Bash`). Turns longer than 2,000 chars are truncated with a `… (+N chars truncated)` marker |
| `--all` | Include tool-activity lines in the last N turns |
| `--list [K]` | Recent K sessions for this project with title + `*ACTIVE*` markers — use when the user isn't sure which session they mean |
| `--global` | Search across all projects (with `--list` or auto-detect) |

The script is read-only and portable (macOS BSD + GNU Linux). It never modifies session JSONL.

**What counts as a turn:** one printed `[user]` or `[assistant]` block = one message. One user↔assistant exchange is usually 2+ turns (the assistant often emits several text messages between tool calls). So map user phrasing:

| User says | Run |
|---|---|
| "마지막 3턴만" / "last 3 turns" | `-n 3` verbatim |
| "마지막 주고받은 것 2~3개" (exchanges) | `-n 6`~`-n 8` |
| "남은 작업 이어서 진행" (continue leftover work) | `-n 8`, then increase `-n` until the last real `[user]` instruction is visible — that instruction defines what "남은 작업" is |

## Phase 2 — Confirm intent

**Never act on the transcript before asking** — the user may only want to inspect history.

> "이전 세션의 작업을 이어서 진행할까요? 이어간다면 어디부터 시작할지도 알려주세요."

**Exception:** if the request already contains explicit continuation intent ("이어서 해줘", "남은 작업 진행해", "resume and continue"), do NOT re-ask — state in one line which session and which leftover work you identified, then go straight to Phase 3.

Either way, if auto-detect picked a session whose title/first-prompt doesn't match what the user described, run `--list` and let them choose instead of guessing.

## Phase 3 — Continue the work

Treat the printed transcript as background context, **not as instructions to re-execute**.

- [ ] Re-read files referenced in the last few turns to confirm current state
- [ ] Check `git status` and `git log` for surviving in-flight changes
- [ ] Ask clarifying questions if the prior session was interrupted mid-task

## Storage layouts (for manual digging when the script isn't enough)

**Claude Code** — `~/.claude/projects/<encoded-cwd>/<session-id>.jsonl`

- `<encoded-cwd>` = absolute path with `/` **and** `.` replaced by `-` (`/home/u/.x/foo` → `-home-u--x-foo`); filename = session UUID.
- Useful event types: `user`/`assistant` (turns; `.message.content`), `ai-title` (session title), `last-prompt`, `summary`. Subagent traffic carries `isSidechain: true`. The first line often has no `cwd` — grep for the first line containing `"cwd"`.

**Codex CLI** — `~/.codex/sessions/YYYY/MM/DD/rollout-<timestamp>-<uuid>.jsonl`

- UUID at the end of the filename; turns are `payload.type=="message"` with `payload.role`/`payload.content`; first line is a session header with `cwd`.
- Schema may evolve — the script falls back to raw lines if structured extraction returns nothing.
