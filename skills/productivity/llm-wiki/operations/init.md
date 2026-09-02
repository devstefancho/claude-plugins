# operation: init

`wiki_root`에 새 위키를 생성한다.

<refs>없음. (시스템 페이지만 만들고, 사용자 페이지는 만들지 않는다. log.md 첫 항목은 init이 직접 작성하는 bootstrap 예외 — `append_log.py`를 쓰려면 log.md가 먼저 있어야 한다.)</refs>

## 1. 사용자에게 위키 정체성을 묻는다

사용자에게 묻는다:

> 위키를 생성합니다.
> - **위키 이름** (예: "Stefan's Knowledge Wiki")
> - **위키 설명** (한 줄)
> - **소스 유형** (예: papers, articles, videos, code)

세 항목 모두 필수. 빈 응답이면 한 번 더 묻는다.

## 2. 디렉토리 생성

```bash
mkdir -p {wiki_root}/raw/sources {wiki_root}/wiki/pages/source {wiki_root}/wiki/pages/entity {wiki_root}/wiki/pages/concept {wiki_root}/journal {wiki_root}/inbox
```

- `raw/sources/` — 원본(불변). `{YYYY-MM-DD}-{slug}.{ext}`, 날짜 = 자료 사건일
- `wiki/pages/{type}/` — 페이지. `{created}-{slug}.md`, wikilink는 frontmatter slug로 해석
- `journal/` — 날짜별 데일리 메모 (사용자 편집·capture)
- `inbox/` — 링크·처리 대기 자료 park (capture·Web Clipper → "위키 정리" 때 distill이 소비)

## 3. 시스템 페이지 작성

`{today}` = 시스템 오늘 날짜 (`YYYY-MM-DD`).

각 템플릿을 Read하고 `{wiki_title}`, `{description}`, `{source_types}`, `{date}` 변수를 치환해서 Write:

- `templates/schema-template.md` → `{wiki_root}/SCHEMA.md`
- `templates/index-template.md` → `{wiki_root}/wiki/index.md`
- `templates/overview-template.md` → `{wiki_root}/wiki/overview.md`
- `templates/tags-template.md` → `{wiki_root}/wiki/tags.md`

치환은 **단순 문자열 치환**이 아니라 의미를 이해하고 처리한다 — 사용자 입력에 `{date}` 같은 글자가 들어있으면 그대로 두고 템플릿 placeholder만 바꾼다.

## 4. log.md 초기화 (bootstrap)

`{wiki_root}/wiki/log.md`에 다음을 직접 Write:

```markdown
# Wiki Log

Append-only operation record.

---

## [{today}] init | {wiki_title}
- Wiki created at `{wiki_root}/`
```

이후 모든 로그 추가는 `scripts/append_log.py`로만.

## 5. 사용자 보고

> ✅ 위키 `{wiki_title}` 생성 완료
> - 경로: `{wiki_root}/` (raw/sources · wiki/pages/{type} · journal · inbox)
> - **Obsidian**: `{wiki_root}`를 vault로 열고 **Dataview**(tags.md MOC용)·**Web Clipper**(리서치 캡처용) 플러그인 설치 권장
> - 다음: 메모·링크는 `capture`, 외부 자료와 "이 대화 정리"는 `wiki ingest`(같은 턴에 raw+pages), inbox가 쌓이면 "위키 정리"(`distill`, 스케줄 없음)
