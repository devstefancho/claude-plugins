---
name: llm-wiki
description: Maintains an LLM-powered personal wiki (capture → raw → wiki → schema) that self-organizes from memos, AI conversations, and research. Use when user mentions wiki init, wiki capture, wiki ingest, wiki distill, wiki query, wiki lint, wiki update, 위키 초기화, 위키에 적어줘/메모, 이 대화 위키에 정리, 위키 추가, 위키 정리, 위키 질문, 위키 검사, 위키 업데이트, or wants to build/maintain a knowledge base.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, AskUserQuestion
---

# LLM Wiki

개인 지식 베이스. 캡처(`journal`·`inbox`) → `raw/sources`(불변) → `wiki/pages`(LLM 컴파일) → `SCHEMA` 흐름. **이 파일은 라우터다** — operation 본문은 `operations/{op}.md`에 있고, 의도 분류 후 그 파일만 Read한다. **이 스킬은 부른 세션 안에서 인라인으로 실행한다** (fork 아님 — 2026-08 실측 21회 중 포크가 소스를 잘못 고른 사고 1회, 확인 단계 0회 실행이라 2026-09-02 에 인라인으로 전환, skills-internal#25). 대화 맥락이 곧 소스이므로 별도 에이전트에 넘기지 않는다.

입력: (1) 리서치·외부 자료 → ingest (2) AI 대화 → ingest (현재 세션 요약도, 과거 세션 트랜스크립트도) (3) 짧은 메모·링크 → capture. **지식은 ingest가 같은 턴에 raw와 pages를 함께 쓴다.** distill은 "위키 정리"라고 시킬 때만 inbox/journal 잔여를 묶는 선택 op이고 스케줄이 없다.

## Phase 0 — Config & Wiki Discovery

모든 op 시작 전 1회 수행. 결과로 `wiki_root`(절대 경로)와 `wiki_exists`(SCHEMA.md 존재 여부)를 갖춘다.

Bash 한 번으로 끝낸다 (21회 실측에서 매 회차 3~6 호출을 쓰던 단계다):
```bash
SKILL_DIR="$(cd "$(dirname "$(readlink -f ~/.claude/skills/llm-wiki/SKILL.md)")" && pwd)"; WIKI_ROOT="$(python3 -c "import json,os;print(os.path.expanduser(json.load(open('$SKILL_DIR/config.json'))['wiki_root']))" 2>/dev/null || echo ~/wiki)"; test -f "$WIKI_ROOT/SCHEMA.md" && echo "wiki_root=$WIKI_ROOT exists=true" || echo "wiki_root=$WIKI_ROOT exists=false"
```
`config.json`이 없으면 사용자에게 위키 루트를 묻고(빈 응답이면 `~/wiki`) `{ "wiki_root": "<path>" }`로 만든다. operation 문서의 `scripts/…`는 전부 `$SKILL_DIR/scripts/…`로 읽고 cwd에 의존하지 않는다.

## Routes

| 발화 | op |
|---|---|
| "wiki init", "위키 초기화", "위키 만들어" | init |
| 짧은 메모·"적어둬"·URL을 나중에 볼 것으로 park("적어둬", "나중에") | capture |
| URL·파일 경로를 지금 읽어서 소화("읽어줘", "위키 추가", "ingest")/**"이 대화 위키에 정리"(현재 세션)**/과거 Claude Code 세션(UUID·"어제 세션") — 단 wiki_root 안의 기존 파일 경로면 update 우선 | ingest |
| "위키 정리"/"distill"/"inbox 정리"/쌓인 캡처 일괄 승격 | distill |
| 위키 내용 질문/"wiki query"/"위키에서 찾아줘" | query |
| "wiki lint"/"위키 검사"/"위키 건강 체크" | lint |
| "wiki update"/"위키 수정"/특정 페이지 + 변경 의도 | update |

라우팅 힌트: 30일 실측은 ingest 19회 · update 2회 · 나머지 0회다. 거의 모든 요청은 ingest("이 대화 정리"도 ingest, inbox를 거치지 않는다)이고, 기존 페이지 경로를 가리키면 update다. distill은 inbox/journal 잔여를 묶을 때만이며 자동 실행·스케줄·모니터를 만들지 않는다. "이건 위키 감이 아니다"도 판정이다 — 특정 시점의 단건 분석(마케팅 분석 등)은 위키가 아니라 그 repo 문서로 보낸다 (2026-08-25 사용자 결정, SCHEMA `type: analysis` 참고). 모호하면 한 줄로 묻는다.

## Dispatch

1. **op이 `init`이 아닌데 `wiki_exists=false`면 진행하지 않는다.** "위키가 없습니다. `wiki init`을 먼저 실행해주세요." 안내 후 종료.
2. `operations/{op}.md`를 Read하고 파일의 절차를 그대로 따른다 (모든 op는 Phase 0 결과와 `wiki_exists=true`를 prereq로 가정 — init만 false에서 시작).
3. op 파일의 `<refs>`가 명시한 PRINCIPLES.md 섹션만, 그 시점에 Read. "섹션"은 `## <name>` 헤딩 한 블록 (다음 `## ...` 직전까지).
