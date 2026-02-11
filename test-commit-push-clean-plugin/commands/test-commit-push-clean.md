---
description: 작업 정리 (브랜치 안전장치, lint, 테스트 커버리지 100%, 단일커밋, push, 워크트리 정리)
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git log:*), Bash(git push:*), Bash(git branch:*), Bash(git worktree:*), Bash(npm run:*), Bash(npx:*), Bash(pnpm:*), Bash(yarn:*)
---

# Test, Commit, Push, Clean

Automates the workflow of testing, committing, pushing, and cleaning up worktrees after completing work on a feature branch.

<context>
Gather current state:

!`git status`: Current working tree status
!`git worktree list`: List of active worktrees
!`git log --oneline -10`: Recent commits
!`git branch --show-current`: Current branch name
</context>

<instruction>
Follow these steps in order:

1. **Branch Safety Check**
   - Get the current branch name
   - If on a default branch (main, master, develop), **STOP immediately**
   - Inform the user: "You are on a default branch. Please create a feature branch or worktree first."
   - Do NOT proceed with any further steps

2. **Lint/Format Check**
   - Detect the project's lint/format configuration (package.json scripts, .eslintrc, prettier config, etc.)
   - Run the appropriate lint command (e.g., `npm run lint`, `pnpm lint`, `yarn lint`)
   - If lint errors exist, fix them automatically when possible
   - Run format check if available (e.g., `npm run format`, `prettier --check`)

3. **Test with Coverage**
   - Detect test configuration (jest.config, vitest.config, etc.)
   - If test setup exists, run tests with coverage targeting 100%
   - If tests fail, attempt to fix or report failures
   - If no test configuration exists, skip this step and inform the user

4. **Organize Commits**
   - Review all staged and unstaged changes
   - Group changes into logical units
   - Create single, well-structured conventional commits per logical unit
   - Commit message format: `{type}: {clear English summary}`
   - Types: feat, fix, chore, docs, style, refactor, test, build, ci
   - Use AskUserQuestion to confirm commit messages before executing

5. **Push to Remote**
   - Push the current branch to origin
   - If no upstream is set, use `git push -u origin {branch-name}`

6. **Clean Up Worktrees**
   - List all worktrees with `git worktree list`
   - Identify worktrees whose branches have been merged into the default branch
   - Remove merged worktrees with `git worktree remove`
   - If no merged worktrees found, skip cleanup
</instruction>

<important>
- NEVER proceed if on a default branch (main/master/develop) — this is a hard stop
- Always confirm commit messages with the user before executing
- Do not force-push unless explicitly asked
- Warn about any sensitive files (API keys, .env, credentials) before committing
- If lint or tests fail and cannot be auto-fixed, report the issue and stop
- Preserve existing commit history — do not rebase or amend unless explicitly asked
</important>
