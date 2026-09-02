# operation: ingest

새 소스를 처리하고 **같은 턴에** 원본(`raw/sources/`)과 위키 페이지를 함께 쓴다. distill을 기다리지 않는다.

<refs>PRINCIPLES.md: secret-scan, dedup, merge-and-split, frontmatter, wikilink, bidirectional, page-types, source-thickness, slug-rules.</refs>

## 1. 소스 수락

**소스가 특정되지 않으면 쓰지 않는다.** 대화 맥락이나 인자에 파일·URL·세션·본문이 없으면 파일시스템을 뒤져 추측하지 말고 사용자에게 무엇을 넣을지 묻는다 (2026-08-19 실측: 포크가 "미팅 전사"만 보고 다른 미팅을 골라 위키에 썼다).

사용자 입력으로부터:
- 파일 경로 → `Read`
- URL → `WebFetch`. 실패 시 사용자에게 본문 붙여넣기 요청
- 텍스트 → 그대로
- **과거 Claude Code 세션** (UUID·"어제 세션"·`.jsonl` 경로) → 1b
- **현재 세션** ("이 대화 정리", "지금까지 한 거 위키에") → 1c

## 1b. 과거 세션 소스 (끝난 대화)

과거 세션 대화를 지식으로 소화한다. **원본 JSONL을 복사하지 않는다** — 요약본만 raw로, 원본은 UUID/경로로 참조.

1. 대상 특정:
   - UUID/경로가 명확하면 바로 다음 단계.
   - "어제 세션"·"이 프로젝트 대화"처럼 모호하면 먼저 나열 후 확인:
     ```bash
     scripts/session_text.py --list --project <cwd-substr> --limit 20
     ```
2. 깨끗한 트랜스크립트 추출 (tool 노이즈·thinking 제거됨):
   ```bash
   scripts/session_text.py <uuid|path>
   ```
3. 출력의 헤더(session/transcript/cwd/span)를 provenance로 보관하고, 본문 대화를 요약 대상으로 삼아 **3단계**로 진행한다.
4. raw 저장 시 헤더에 `source_session`·`source_transcript`를 넣고 `type: conversation`. 날짜 prefix는 세션 날짜(span 시작일). 요약본을 `raw/sources/{YYYY-MM-DD}-{slug}.md`로 Write — 원본 JSONL은 그대로 `~/.claude/projects`에 남는다.

## 1c. 현재 세션 소스 (진행 중인 대화)

지금 맥락에서 **결정·인사이트·핵심**만 압축한 요약을 만든다 (전체 대화 복제가 아님). 요약 단계에서 시크릿(API키·토큰·비밀번호)을 옮겨 적지 않는다 — raw 확정 전 스크립트 게이트가 한 번 더 본다. 헤더는 `type: conversation`, `source_session`에 현재 세션 ID(알 수 없으면 생략), 날짜 prefix는 오늘. 이어서 2단계부터 그대로 진행한다 — 이 경로가 "이 대화 정리"의 전부이고 inbox를 거치지 않는다.

## 2. raw 저장

slug는 PRINCIPLES.md slug-rules에 따라 직접 생성 (한글/CJK는 transliterate, 충돌 시 `-2/-3`, 날짜는 slug에 넣지 않음). 날짜 prefix는 **자료의 사건일**(미팅·발행·세션일) — 모르면 오늘, 월만 알면 `YYYY-MM`.

- 텍스트/마크다운 → `{wiki_root}/raw/sources/{date}-{slug}.md`에 헤더 + 전체 본문 Write
- PDF·이미지 등 binary → `{wiki_root}/raw/sources/{date}-{slug}.{ext}`로 원본 복사 + `{wiki_root}/raw/sources/{date}-{slug}.meta.md`에 헤더만
- `raw/sources/` 아래에 폴더를 만들지 않는다(유형별 분류 폴더 금지). `raw/<tool>/`(session-history 등)에는 쓰지 않는다.

헤더:

```yaml
---
source_url: <url-if-applicable>
source_session: <uuid-if-conversation>
source_transcript: <path-if-conversation>
ingested: <today>
type: article|paper|video|code|note|research|conversation
---
```

세션 소스면 `source_url` 대신 `source_session`·`source_transcript`를 채운다. 리서치 리포트는 `research`.

**시크릿 게이트 (PRINCIPLES.md secret-scan).** raw는 불변이므로 **raw에 먼저 쓰지 않는다** — 본문을 스크래치 파일에 쓰고 `scripts/secret_scan.py {staging_path}`를 통과한 뒤 `raw/sources/`로 옮긴다. exit 3이면 거기서 멈추고 사용자에게 묻는다(마스킹/폐기/오탐 진행). 세션 소스(1b·1c)는 시크릿 유입 위험이 가장 크므로 반드시 통과시킨다.

## 2c. 중복 확인 (PRINCIPLES.md dedup)

source 페이지를 만들기 전에 `Grep {wiki_root}/wiki/pages/`로 같은 소스(URL·세션 UUID)·유사 제목을 검색한다. 기존 페이지가 이미 이 소스를 다루면 **신규 생성 대신** update op(또는 merge-and-split 병합)로 전환하고, 애매하면 병합 vs 신규를 사용자에게 확인한다.

## 2d. 갈래 파악 (어디에 속하는 문서인가)

**페이지를 쓰기 전에 이 소스가 어느 갈래에 속하는지 정한다.** 새 카테고리를 세우는 것보다 이미 있는 갈래에 붙이는 것이 먼저다.

- `Grep {wiki_root}/wiki/pages/concept/ -l 'slug: hub-'`로 허브 목록을 훑는다 (사업·제품·공장·관제·개인)
- 후보 허브를 하나 고르고 그 본문을 읽어 어느 절에 들어갈지까지 정한다. 절 이름이 곧 이 문서의 이웃이 무엇인지다
- 어느 갈래에도 안 맞으면 허브를 새로 만들지 말고 3단계 확인에 그 사실을 적어 사용자에게 묻는다

여기서 정한 갈래는 3단계 확인 문구에 실어 사용자가 그 자리에서 고칠 수 있게 한다. 실제로 매다는 것은 5b.

허브에 매달지 않으면 페이지는 태그로만 닿는다. 2026-09-01에 사업 페이지 넷(Agora 계약·Higgsfield 제안·한국전자인증·패스트캠퍼스 미팅)이 `[[hub-business]]`에서 닿지 않는 채로 남아 있었다.

## 3. 핵심 시사점 합성

소스를 분석해 핵심 포인트 3개와 관련 엔티티/개념 후보, 갈래(허브 > 절)를 정한다. **멈춰서 묻지 않는다** — 이 요약은 10단계 보고에 그대로 실어 사용자가 사후에 고치게 한다(21회 실측에서 확인 단계가 한 번도 실행되지 않았고, 교정은 늘 회차가 끝난 뒤 왔다). 갈래를 정할 수 없을 때만 한 줄로 묻는다.

## 4. source 페이지 작성 (원본이 외부 문서일 때)

원본이 외부 문서(글·논문·영상·리서치)면 얇은 지도 페이지를 만든다. 세션 실측·대화 요약처럼 raw 자체가 원본이면 source 페이지를 만들지 않고 5단계 concept/entity 로 바로 간다 (ingest 58건 중 source 페이지 40장, 건너뛴 이유가 적힌 것은 2건뿐이라 규칙으로 올림). 건너뛰면 9단계 로그에 "source 페이지 없음 — 사유"를 적는다.

`templates/page-template.md`를 참고해 `{wiki_root}/wiki/pages/source/{today}-{slug}.md`로 Write (폴더 = type, 파일명 날짜 = `created` = 오늘, 페이지 slug는 raw 이름과 독립):

- frontmatter: `type: source`, `aliases: [{slug}]`, `sources: [{raw basename}]`(raw 파일명에서 확장자만 뺀 것, 날짜 포함), tags
- 소스 메타 (raw 경로·URL·수집일)
- 2-3 문단 합성 요약
- 핵심 시사점 (사용자 피드백 반영)
- Related 섹션에 엔티티/개념 wikilink

**두께 (PRINCIPLES.md source-thickness).** 요약·시사점·링크까지만. 원문 섹션을 순서대로 재서술하거나 표·수치를 전량 옮기지 않는다 — 원문은 raw에 있다. lint `oversized_source`(본문 8,000자)가 백스톱.

template은 placeholder의 의미를 보고 의미 있게 채운다 — 비워둔 키 포인트가 있으면 항목을 줄인다.

## 5. 엔티티/개념 페이지 갱신

언급된 엔티티/개념마다 `Grep {wiki_root}/wiki/pages/`로 기존 페이지 검색:

- 존재: merge-and-split 병합 규칙으로 **차이나는 정보만** 본문에 녹이고(그대로 이어붙이지 않음), `sources`에 raw basename 추가, `updated` 갱신. **파일명은 그대로** (날짜·slug 고정)
- 없음: `{wiki_root}/wiki/pages/entity/{today}-{slug}.md` 또는 `concept/{today}-{slug}.md`로 신규 생성 (frontmatter `aliases` 포함, slug는 같은 규칙)
- 페이지가 여러 독립 개념을 담아 응집도가 떨어지면 merge-and-split 분할 규칙 적용

## 5b. 갈래에 매달기

2d에서 정한 갈래대로 실행한다.

- 허브 본문의 맞는 절에 `- [[slug]] — 한 줄` 추가. 맞는 절이 없으면 절을 하나 늘린다
- 갈래의 대표 태그를 새 페이지 `tags`에 넣는다. **허브 링크와 태그 둘 다** 있어야 그래프와 Dataview 양쪽에서 닿는다
- 검증: lint의 `unhubbed`(어느 허브에서도 안 닿음)·`far_from_hub`(3홉 이상)에 이번에 만든 페이지가 없어야 한다. 규칙은 SCHEMA.md 허브 절

## 6. 양방향 백링크 보강

PRINCIPLES.md bidirectional에 따라:

- 새/갱신 페이지의 모든 `[[slug]]`에 대해 대상 페이지 Related에 역링크가 있는지 확인하고, 없으면 추가
- 기존 페이지에서 새 엔티티/개념이 plain text로 언급된 곳이 있으면 wikilink로 변환
- 검증: `Bash: scripts/lint_wiki.py {wiki_root} --json`에서 **이번 ingest가 만들거나 건드린 페이지**의 `missing_backlink`·`missing_source`·`bad_path`가 0이 될 때까지 보강 (기존 백로그는 lint op의 일)

## 7. index.md 갱신

`{wiki_root}/wiki/index.md` 를 **먼저 Read 한 뒤** Edit 한다 (21회 중 13회가 "File has not been read yet" 오류로 한 턴을 버렸고, 회피하려고 heredoc 덮어쓰기로 갈아타면서 raw 불변·log append-only 가 도구로 막히지 않게 됐다). overview.md 의 `updated:` 도 같은 규칙이고, frontmatter 값은 본문에도 같은 글자가 있을 수 있으니 `---\n...updated:` 처럼 앞뒤 문맥을 포함해 치환한다.

- 적절한 카테고리(Sources/Entities/Concepts, SCHEMA.md에 추가 type이 있으면 그 섹션)에 `- [[{slug}]] — {one-line} _(ingested {today})_` 추가
- Recent 섹션은 최근 5개 항목만 유지. 밀려나는 항목이 카테고리 섹션에 없으면 먼저 등재한다(Recent에만 있던 페이지가 unindexed가 되지 않게)

## 8. overview.md 갱신

새 소스가 위키 전체 이해를 바꾸는 경우에만 Key Themes / Open Questions를 갱신한다. Statistics 카운트(lint `scanned`와 type 폴더별 파일 수 기준)와 frontmatter `updated`는 항상 갱신.

## 9. 로그

```bash
cat <<EOF | scripts/append_log.py {wiki_root} ingest "{source_title}"
- Raw: raw/sources/{date}-{slug}.md
- Pages created: [[slug1]], [[slug2]]
- Pages updated: [[slug3]], [[slug4]]
- Backlinks added: <count>
EOF
```

## 10. 보고

> ✅ **{source_title}** ingest 완료
> - raw: `raw/sources/{date}-{slug}.md` · 페이지: `[[{slug}]]` · 갈래: {hub} > {절}
> - 핵심 포인트: 1) … 2) … 3) …  (틀렸으면 지금 고쳐 달라)
> - 생성/업데이트/백링크: c1/c2/c3 · lint 백로그: unhubbed n · far_from_hub n · missing_backlink n (이번 회차 페이지는 0)
