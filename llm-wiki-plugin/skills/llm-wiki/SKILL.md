---
name: llm-wiki
description: Maintain an LLM-powered personal wiki from raw sources. Use when user mentions wiki init, wiki ingest, wiki query, wiki lint, wiki update, 위키 초기화, 위키 추가, 위키 질문, 위키 검사, 위키 업데이트, or wants to build a knowledge base from sources.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, AskUserQuestion
context: fork
agent: general-purpose
---

# LLM Wiki

3-layer 아키텍처(원본 소스 → 위키 페이지 → 스키마)로 LLM이 유지보수하는 개인 위키. 위키는 `wiki_root` 하나에 뿌리내린 단일 지식 그래프 — `[[slug]]` 교차 참조가 한 그래프 안에서만 유효하므로 위키를 여러 개로 쪼개지 않는다.

## 이 SKILL의 역할 — 라우터

이 파일은 **라우터**다. 모든 operation의 본문은 별도 파일에 있고, 의도가 정해진 뒤에야 해당 파일을 읽는다. 처음부터 5개 operation을 전부 컨텍스트에 올리지 않는다 (progressive disclosure).

흐름:
1. **Phase 0** — 설정과 위키 위치를 확정
2. **Operation Detection** — 사용자 의도를 5개 중 하나로 분류
3. **Dispatch** — `operations/{op}.md`를 Read 하고 그 절차를 따름
4. 공통 규칙이 필요할 때만 [PRINCIPLES.md](PRINCIPLES.md)를 Read

## Phase 0: Config & Wiki Discovery

모든 operation 시작 전 1회 수행.

1. 플러그인 설치 디렉토리(이 SKILL.md가 있는 곳)를 식별
2. 플러그인 루트(SKILL.md로부터 두 단계 위)의 `config.json` 확인:
   - **존재**: `wiki_root` 값 읽기
   - **없음**: `AskUserQuestion`으로
     > 위키 루트 경로를 설정해주세요. 위키가 이 경로에 생성됩니다.
     > 기본값: `~/wiki`

     답을 받아 `config.json`을 `{ "wiki_root": "<path>" }`로 생성
3. `wiki_root`의 `~`를 절대 경로로 확장
4. `{wiki_root}/SCHEMA.md` 확인:
   - **존재**: 위키 준비 완료. 이후 모든 경로는 `{wiki_root}` 기준
   - **없음**:
     - operation이 `init`이면 → init 진행
     - 그 외 → "위키가 없습니다. 먼저 `wiki init`을 실행해주세요." 안내 후 종료

```json
// config.json
{ "wiki_root": "~/wiki" }
```

## Operation Detection

| 사용자 발화 | Operation | 본문 파일 |
|---|---|---|
| "wiki init", "위키 초기화", "위키 만들어" | init | [operations/init.md](operations/init.md) |
| URL, 파일 경로, "ingest", "위키 추가", "이거 읽어줘" | ingest | [operations/ingest.md](operations/ingest.md) |
| 위키 내용에 대한 질문, "wiki query", "위키에서 찾아줘" | query | [operations/query.md](operations/query.md) |
| "wiki lint", "위키 검사", "위키 건강 체크" | lint | [operations/lint.md](operations/lint.md) |
| "wiki update", "위키 수정", 특정 페이지 + 변경 의도 | update | [operations/update.md](operations/update.md) |

모호하면 `AskUserQuestion`:
> 어떤 작업을 할까요?
> 1. ingest — 새 소스 추가
> 2. query — 위키에서 검색
> 3. lint — 위키 건강 검사
> 4. update — 페이지 수정

## Dispatch

operation이 결정되면:

1. 해당 `operations/{op}.md`를 `Read`
2. 그 파일의 "Steps"를 그대로 수행
3. 그 파일이 PRINCIPLES.md의 특정 섹션을 참조하라고 지시하면 그때 Read

PRINCIPLES.md를 미리 Read하지 말 것 — 필요한 operation이 명시할 때만 읽는다.
