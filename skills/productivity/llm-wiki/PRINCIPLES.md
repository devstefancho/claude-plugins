# LLM Wiki Principles

각 operation은 `<refs>`로 필요한 섹션만 명시한다. 미리 다 읽지 않는다.

## architecture

위키는 단일 그래프다. `[[slug]]` 교차 참조가 한 그래프 안에서만 유효하므로 위키를 쪼개지 않는다. 입력 스트림(리서치·대화·메모)은 위키를 나누지 않고 `type`/`tags`로만 구분한다.

계층은 **캡처(가변) → 원본(불변) → 위키(컴파일)** 로 흐른다. 지식(대화 정리·리서치)은 ingest가 **같은 턴에 원본과 위키를 함께 쓴다** — 캡처 계층에 쌓아 두고 나중 정리를 기다리지 않는다.

- **`journal/`** — 날짜별 데일리 메모. `journal/YYYY-MM-DD.md`, 하루 파일에 자유롭게 append. 사용자 편집 영역(옵시디언 직접 작성 OK). ops는 **지우거나 고치지 않는다**(영구 다이어리).
- **`inbox/`** — 나중에 볼 링크·처리 대기 자료를 던져 두는 마찰0 트레이. `inbox/{YYYY-MM-DD}-{slug}.md` 항목별 파일. 사용자 편집 영역. 승격 경로의 하나일 뿐 유일한 경로가 아니다 — distill이 소비하면 원본을 `raw/`로 확정하고 **inbox 파일은 제거**한다.
- **`raw/`** — 원본 자료. 추가만 가능, 수정/삭제 금지.
  - `raw/sources/{YYYY-MM-DD}-{slug}.md` — 사람·ingest 영역. binary(PDF·이미지)는 같은 이름 규칙 + 동반 `…-{slug}.meta.md`에 메타 헤더. **날짜 = 자료의 사건일**(미팅·발행·세션일). 모르면 ingest일, 월만 알면 `YYYY-MM` 허용. 목적은 `ls` 한 화면이 날짜순으로 읽히는 것이므로 **유형별 분류 폴더(research/, meeting/)를 만들지 않는다**.
  - `raw/<tool>/` (예: `session-history/`, `tool-updates/`) — 다른 스킬이 소유하는 기계 영역. 자체 규약을 따르고 lint의 이름 검사에서 면제. ingest는 여기에 쓰지 않는다.
- **`wiki/`** — LLM이 컴파일·유지보수.
  - `wiki/index.md` — 페이지 카탈로그
  - `wiki/overview.md` — 위키 요약
  - `wiki/tags.md` — 태그별 MOC (Obsidian Dataview 뷰, 찾기 보조 진입점)
  - `wiki/log.md` — append-only 작업 이력
  - `wiki/pages/{type}/{created}-{slug}.md` — type 폴더 한 층(`source/`·`entity/`·`concept/`, 위키별 추가 type은 SCHEMA.md에). 폴더명 = frontmatter `type`, 파일명 날짜 = `created`. 그 아래 폴더 금지.
- **`SCHEMA.md`** — 위키 정체성. Phase 0의 발견 진입점.

## capture-layers

`journal/`·`inbox/`는 **마찰0 입력 트레이**다 — 옵시디언 직접 작성, Web Clipper, `capture` op이 모두 여기로 쓴다.

- **capture는 메모와 링크만.** 짧은 생각은 journal에, 나중에 볼 URL·자료는 inbox에 받아 적는다. 분류·페이지화는 하지 않는다.
- **대화 정리·리서치는 capture가 아니라 ingest.** "이 대화 정리"는 현재 세션을 요약해 `raw/sources/`에 확정하고 같은 턴에 페이지까지 쓴다(ingest 1c). inbox에 넣고 기다리지 않는다.
- **distill은 선택 작업이고 스케줄이 없다.** 사용자가 "위키 정리"라고 시킬 때만 inbox/journal에 남은 것을 주제별로 묶어 승격한다. 자동 실행·cron/launchd/loop 스케줄·"끝나면 알려줄게" 모니터를 만들지 않는다 — 토큰 사용량을 예측할 수 없어서다. 메인 경로는 distill 없이도 완결돼야 한다.
- **워터마크.** distill은 `log.md`의 마지막 `distill` 항목 날짜 이후의 journal 파일만 읽는다 (없으면 전부). 사용자가 "전체 다시"라고 하면 무시. inbox는 큐라 매번 전량 처리.
- **provenance.** inbox 항목이 페이지로 승격되면 그 내용을 `raw/sources/{captured}-{slug}.md`로 확정(불변)한 뒤 inbox 파일 삭제. journal에서 승격된 페이지는 원본 journal이 영구 기록이므로 raw 복사 없이 `journal/YYYY-MM-DD.md` 날짜만 페이지에 남긴다.
- **경계.** ops는 `journal/`을 절대 수정/삭제하지 않는다(사용자 다이어리). `inbox/`는 distill의 소비 삭제만 허용, 내용 개정은 금지.

## secret-scan

**`raw/`는 불변이다. 시크릿이 한 번 들어가면 영구 기록이 된다.** 외부/pass-through 내용을 `raw/`로 확정하기 직전 반드시 게이트를 통과시킨다.

- 적용 지점: ingest의 raw 저장(세션 트랜스크립트·현재 세션 요약 포함), distill의 inbox→raw 승격. 검사는 `scripts/secret_scan.py <file>` (API키·토큰·private key·`key=value` 시크릿 탐지, 히트 시 exit 3).
- 히트가 나오면 **저장을 멈추고** 사용자에게 묻는다 — (1) 마스킹(`‹REDACTED:kind›`로 치환) 후 진행 (2) 해당 소스 폐기 (3) 사용자가 오탐이라 판단하면 그대로 진행. 사용자 확인 없이 시크릿을 raw에 남기지 않는다.
- **journal은 예외.** 사용자 다이어리(pass-through·immutability 5)라 스캔·마스킹하지 않는다. 현재 대화를 요약할 때는 LLM이 시크릿을 애초에 옮겨 적지 않는다(판단으로 처리, 스크립트 게이트는 raw 단계에서).

## page-types

- `source` — 원본 요약 (논문, 기사, 영상, 코드, 대화). 요약·시사점·링크까지만 — source-thickness 참조
- `entity` — 사람, 조직, 도구, 기술
- `concept` — 아이디어, 패턴, 원칙
- `index`, `overview` — 시스템 페이지. 각 템플릿에서만 사용
- 위키별 추가 type(예: 살아 있는 상태 페이지 `tracker`)은 SCHEMA.md에 정의하고 같은 이름의 `wiki/pages/{type}/` 폴더를 쓴다

`source` vs `entity` vs `concept`은 페이지가 "무엇을 다루는가"로 판단 — 원본 자체가 주제면 source, 인물/조직/도구가 주제면 entity, 그 외 추상 개념이면 concept.

## source-thickness

**source 페이지는 요약·시사점·링크까지다. 원문을 재구성하지 않는다** — 원문은 `raw/sources/`에 있고 페이지는 거기로 가는 지도다.

- 담는 것: 소스 메타(raw 경로·수집일·출처 URL), 2~3문단 합성 요약, 핵심 시사점 bullet, Related wikilink.
- 담지 않는 것: 원문 섹션을 순서대로 옮긴 재서술, 표·수치·문구의 전량 복사, 원문 목차 미러링. 원문에서 찾을 정보는 "어디 있다"만 적는다.
- 백스톱: `scripts/lint_wiki.py`의 `oversized_source`(본문 8,000자 초과) 경고. 기존 두꺼운 페이지를 일괄로 자르지는 않고, 새 ingest와 update가 이 규칙을 지킨다.

## dedup

새 내용을 페이지로 만들기 전에 **이미 위키에 있는지** 확인한다 — 위키는 파편화가 아니라 수렴을 지향한다.

- **감지.** `Grep {wiki_root}/wiki/pages/`(하위 폴더 포함)로 같은 소스(URL·세션 UUID)·같은 주제·유사 제목을 찾는다. 기존 페이지가 이미 그 소스/주제를 다루면 **새로 만들지 말고** merge-and-split의 병합 경로로 간다(또는 update op).
- **결정론적 백스톱.** `scripts/lint_wiki.py`의 `duplicate_title`이 제목이 겹치는 페이지를 사후 감지한다. lint에서 뜨면 병합 대상 후보다.
- 판단이 애매하면(겹치는지 신규인지) 병합 vs 신규를 사용자에게 확인한다.

## merge-and-split

페이지는 append가 아니라 **의미 단위 병합**으로 자라고, 크기가 아니라 **개념 응집도**로 쪼갠다.

- **병합(append-doc).** 기존 페이지에 새 정보를 통합할 때 원문을 그대로 이어붙이지 않는다. **차이나는 정보만** 해당 섹션에 녹이고, 중복 문장은 재작성하지 않는다. `sources` frontmatter에 raw basename 추가, `updated` 갱신. 파일명(날짜·slug)은 바꾸지 않는다. 기존 서술과 상충하면 update op의 모순 점검(§4)을 적용한다.
- **분할(divide-doc).** 한 페이지가 **여러 독립 개념**을 담아 응집도가 떨어지면(한 페이지 = 한 주제 위반) 개념별 페이지로 분리한다. 분리 페이지는 slug-rules로 신규 생성, 원본은 허브로 남겨 `[[분리slug]]`로 연결, bidirectional에 따라 백링크 보강 후 lint로 검증. 단순히 길다는 이유로 쪼개지 않는다 — 기준은 개념 경계.

## frontmatter

```yaml
---
title: ...
slug: ...
aliases: [slug]        # Obsidian이 [[slug]]를 이 파일로 해석하게 (파일명에 날짜가 붙으므로 필요)
type: source|entity|concept|index|overview
created: YYYY-MM-DD    # 파일명 날짜 prefix와 같다. 이후 바뀌지 않는다
updated: YYYY-MM-DD
sources: [raw-basename, ...]   # optional — raw/sources/ 파일명에서 확장자만 뺀 것 (날짜 포함)
tags: [tag, ...]       # optional
---
```

필수: `title`, `slug`, `type`, `created`, `updated`. lint 스크립트는 이 5개를 검증하고 `sources` 항목의 실재를 확인한다.

## wikilink

- `[[slug]]` → frontmatter `slug`가 그 값인 페이지. 파일은 `wiki/pages/{type}/{created}-{slug}.md`에 있지만 **링크는 파일명이 아니라 slug로 해석**한다 (lint도 같은 방식)
- `[[slug|표시]]` 커스텀 표시
- `[[slug#anchor]]` 섹션 앵커 (slug 부분으로만 해석)
- 외부 URL은 일반 마크다운 링크
- `slug`는 날짜가 없는 안정 식별자다. 파일명의 날짜 prefix를 링크에 쓰지 않는다

## bidirectional

A가 `[[B]]`를 쓰면 B의 Related 섹션에도 `[[A]]`가 있어야 한다. ingest/update가 페이지를 변경한 직후 `scripts/lint_wiki.py {wiki_root} --json`을 실행해 `missing_backlink`가 0이 될 때까지 보강한다.

## slug-rules

정규식 `^[a-z0-9][a-z0-9-]{0,49}$` (소문자 영숫자·하이픈, 첫 글자 영숫자, 1~50자).

LLM이 직접 생성한다 — 한글/CJK는 의미가 통하는 영어로 transliterate (예: "어텐션 메커니즘" → `attention-mechanism`, "Café" → `cafe`). 기존 페이지와 충돌하면 `-2`, `-3`을 붙인다. 50자 제한은 충돌 접미사 포함 후의 길이. 날짜는 slug에 넣지 않는다 — 파일명 prefix가 그 역할이다.

## immutability

1. `raw/` 추가만 (수정/삭제 금지). ingest는 `raw/sources/`에만 쓰고 새 폴더를 만들지 않는다(`raw/<tool>/`은 해당 스킬만)
2. `log.md` append-only — 기존 항목 수정/삭제 금지. **추가는 `scripts/append_log.py`** (단, 위키 최초 생성 시 init이 직접 작성하는 첫 항목은 예외)
3. `SCHEMA.md` 사용자 명시 확인 없이 수정 금지
4. `wiki/pages/{type}/` 한 층만 — 그 아래 폴더 금지. 페이지 파일명(`{created}-{slug}.md`)은 생성 후 바꾸지 않는다(update는 `updated`만 갱신)
5. `journal/` ops 수정/삭제 금지 (사용자 다이어리). capture의 append만 허용
6. `inbox/` distill의 소비 삭제만 허용 — 내용 개정 금지

## log-format

```
scripts/append_log.py <wiki_root> <op> "<description>"
```

- `<op>` ∈ `init|ingest|distill|query|lint|update`
- `<description>` 한 줄 (개행 금지 — 스크립트가 거부)
- 본문 bullet은 stdin으로 전달 (heredoc)
