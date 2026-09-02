---
name: github-issue
description: "Unified GitHub issue workflow via the gh CLI — fetch an issue (body, labels, comments, image/video attachments) into the session, create a new issue from a template, or update an existing one (body, labels, state, comments). Handles the 404 that plain curl/WebFetch hits on GitHub attachment URLs by downloading with an auth token, and extracts viewable frames from video attachments. Use whenever the user mentions GitHub issues — 이슈 가져와, 이슈 조회, 이슈 등록, 이슈 생성, 이슈 만들어줘, 이슈 업데이트, 이슈 수정, 이슈 코멘트, 이슈 작업, fetch issue N, work on issue N, create an issue, update issue N, file a bug, /github-issue."
---

# GitHub Issue

Operate on GitHub issues with the `gh` CLI. One skill, three operations — dispatch on the user's words or the argument:

| User intent | Operation |
| --- | --- |
| "이슈 N 가져와 / 조회 / 작업", "fetch issue N", bare `/github-issue 94` | **Fetch** |
| "이슈 등록 / 생성 / 만들어줘", "create issue", "file a bug" | **Create** |
| "이슈 N 수정 / 업데이트 / 코멘트 / 닫아줘", "update issue N" | **Update** |

If the intent is genuinely ambiguous, ask which operation — don't guess.

## Common setup

- `gh auth status` 는 매번 돌리지 않는다. `gh` 호출이 인증 오류로 실패했을 때만 확인하고, 그때 사용자에게 `gh auth login` 을 안내한다 (12세션 실측: 사전 확인 실행 0회, 인증 실패 0건).
- Default to the current repo. If the user names another repo, pass `-R <owner>/<repo>` to every `gh` call.

## Fetch

1. If no issue number was given, run `gh issue list`, show the open issues, and let the user pick.
2. `gh issue view <N> --json number,title,state,labels,author,url,body,comments`
3. 본문이나 코멘트에 `github.com/user-attachments/` 링크가 있을 때만 [fetching.md](fetching.md) 를 읽고 그 절차대로 받는다 — **plain curl/WebFetch returns 404 on GitHub attachment URLs** (auth-token download, image Read, video → ffmpeg frames). 첨부가 없으면 이 단계는 없다.
4. Summarize in the conversation: issue number/title/labels, the problem or request in one or two lines, and what the attachments show.
5. 사용자가 첫 지시에서 구현 범위까지 준 경우(워커 칸의 발제문이 보통 그렇다)에는 조회 뒤 그대로 이어서 작업한다. 지시가 "가져와/조회"뿐이면 관련 코드 위치(grep for the symbols/strings the issue points at)와 가설 한두 문장까지만 말하고 멈춘다 — intake ends at understanding.

## Create

이 절은 사용자가 "이슈 만들어줘"라고 했을 때만이다. 작업 세션이 착수 전 스스로 만드는 이슈(work-routing 의 issue-SSOT)는 이 스킬을 거치지 않고 `gh issue create` 한 줄로 끝내고, 두 건 이상이면 `writing-tasks` 가 관계까지 건다.

1. Pick a template, in this order:
   - The repo's own `.github/ISSUE_TEMPLATE/*.md|*.yml` if present — list them and match by intent.
   - Otherwise the bundled ones: [templates/bug-report.md](templates/bug-report.md), [templates/feature-request.md](templates/feature-request.md), [templates/task.md](templates/task.md).
2. Fill the template from the conversation and any context the user gave. Write the issue in the language of the repo's existing issues (check a recent one if unsure). Ask only for fields you genuinely can't fill — don't interrogate.
3. **Show the complete draft (title, body, labels) and wait for the user's OK before creating.** Filing an issue is outward-facing and visible to others; never skip this gate.
4. Create with a body file so markdown survives quoting:

   ```bash
   gh issue create --title "<title>" --body-file <draft.md> --label "<labels>"
   ```

   Only pass labels that already exist in the repo (`gh label list`) — `gh` errors on unknown labels. Same rule for `--add-label` on update.

5. Report the created issue URL.

## Update

1. Fetch the current state first (`gh issue view <N> --json title,body,labels,state,comments`) — never edit blind. 코멘트만 달 때도 `body` 와 `comments` 를 함께 받는다. 본문을 안 읽고 단 코멘트는 이미 나온 답을 반복한다.
2. 코멘트 추가는 확인 없이 바로 올린다 (덧붙이는 것이라 되돌리기 쉽고, 5세션 실측에서 사용자가 이미 내용을 지정한 상태였다). 본문·제목·라벨·상태를 바꿀 때만 before → after 를 보이고 확인을 받는다.
3. Apply with the matching command:
   - body/title/labels: `gh issue edit <N> --title/--body-file/--add-label/--remove-label`
   - comment: `gh issue comment <N> --body-file <comment.md>`
   - state: `gh issue close <N> [--comment]` / `gh issue reopen <N>`
4. Report the issue URL and what changed.

## Anti-patterns

- **WRONG**: `curl <attachment-url>` or WebFetch on `github.com/user-attachments/assets/...` → 404. **RIGHT**: download with `Authorization: token $(gh auth token)` per [fetching.md](fetching.md).
- **WRONG**: Read a downloaded `.mp4` directly (wastes a turn, shows nothing). **RIGHT**: extract frames with ffmpeg and Read those.
- **WRONG**: `gh issue create`/`edit` (본문·제목·라벨·상태 변경) straight away with a body you never showed. **RIGHT**: full draft → user confirmation → apply. 코멘트는 예외다.
- **WRONG**: free-form issue body because the template "doesn't quite fit". **RIGHT**: pick the closest template and drop sections that are truly N/A.
