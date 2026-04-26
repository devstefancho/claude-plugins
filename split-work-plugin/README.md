# split-work-plugin

현재 프로젝트의 작업을 충돌 없는 병렬 묶음으로 쪼개고, 각 묶음을 별도 worktree에서 시작할 수 있도록 CLI 명령 + 시작 프롬프트를 생성한다. 시니어가 주니어들에게 업무를 분담하듯 의존성·파일 충돌을 분석해 안전한 lane을 제안한다.

## 사용법

```
/split-work
```

또는 자연어로 "작업 쪼개줘", "병렬로 진행할 수 있게 분리해줘".

## 동작

1. `tasks/`, `specs/`, `git worktree list`, 최근 커밋 기반으로 현황 수집
2. `depends_on` 충족 + 파일/패턴 충돌 여부로 그룹화
3. 브랜치명 추천 (`worktree-task-{번호}` 패턴)
4. 각 task에 시작 프롬프트(XML) 생성
5. `~/.claude/split-work/{project-slug}/{YYYY-MM-DD-HHmm}.md` 에 저장

## Pair

- `writing-tasks-plugin` — task 분해 (split-work의 입력)
- `agent-team-plugin` — split-work 결과를 받아 worktree+팀 자동 구성

## Install

```bash
/plugin marketplace add devstefancho/claude-plugins
/plugin install split-work-plugin@devstefancho-claude-plugins
```
