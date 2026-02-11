---
description: 작업 정리 (브랜치 안전장치, lint, 테스트 커버리지 100%, 단일커밋, push, 워크트리 정리)
argument-hint: [--skip lint,test,push,pr,clean]
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git log:*), Bash(git push:*), Bash(git branch:*), Bash(git worktree:*), Bash(gh pr:*), Bash(npm run:*), Bash(npx:*), Bash(pnpm:*), Bash(yarn:*)
---

# Test, Commit, Push, PR, Clean

<context>
!`git status`: 작업 상태
!`git worktree list`: 워크트리 목록
!`git log --oneline -10`: 최근 커밋
!`git branch --show-current`: 현재 브랜치
</context>

<instruction>

`$ARGUMENTS`에 `--skip 단계1,단계2,...` 가 있으면 해당 단계를 스킵한다. 사용 가능한 키: lint, test, push, pr, clean (예: `--skip push,pr,clean`)

1. 브랜치 체크 — 현재 브랜치가 디폴트 브랜치(main/master/develop)이면 작업을 중단하고, 워크트리/브랜치 생성을 안내
2. [lint] lint/format 체크
3. [test] 테스트 설정이 있으면 커버리지 100%로 맞추기, 없으면 스킵
4. 변경사항을 논리적 단위의 단일 커밋들로 정리
5. [push] git push
6. [pr] `gh pr create`로 PR 생성 (디폴트 브랜치 대상, 커밋 내용 기반으로 title/body 작성)
7. [clean] `git worktree list` + `git branch --merged main`으로 머지 완료된 다른 워크트리가 있으면 `git worktree remove`로 제거 (현재 작업 워크트리는 유지)

</instruction>
