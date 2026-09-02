# operation: lint

위키 건강 감사. 검사는 결정론적 — `scripts/lint_wiki.py`가 전담한다.

lint가 예상 경로(`wiki/pages/{type}/{created}-{slug}.md`, `raw/sources/{date}-{slug}.{ext}`)에서 페이지·raw 파일을 못 찾으면, 구 레이아웃 흔적일 수 있다 — vault 루트 `MIGRATION.md`(옛→새 경로 표)를 먼저 확인한다.

<refs>스크립트 출력 자체에는 PRINCIPLES.md 필요 없다. 자동 수정 수락 시 frontmatter, bidirectional, wikilink 추가 Read.</refs>

## 1. lint 실행

```bash
scripts/lint_wiki.py {wiki_root} --json
```

JSON: `{ scanned, errors[], warnings[], info[] }`. 각 항목은 `{ check, page?, target?, fields?, ... }`.

검사 항목 (스크립트가 코드화):
- errors: `broken_link`, `missing_frontmatter`, `invalid_slug`, `duplicate_slug`, `bad_path`(`pages/{type}/{YYYY-MM-DD}-{slug}.md` 형태 아님), `type_dir_mismatch`(폴더 ≠ frontmatter type), `missing_source`(`sources:` 항목이 `raw/sources/`에 없음), `raw_misplaced`(`raw/` 바로 아래 파일·`raw/sources/` 하위 폴더), `raw_bad_name`(날짜 prefix 없음)
- warnings: `orphan`, `unhubbed`(어느 허브에서도 안 닿음), `missing_backlink`, `stale`, `duplicate_title`, `date_mismatch`(파일명 날짜 ≠ created), `oversized_source`(source 본문 8,000자 초과)
- info: `unindexed`, `far_from_hub`(허브에서 3홉 이상), `raw_tool_dir`(`raw/<tool>/` — 도구 소유, 검사 면제 알림)

wikilink는 frontmatter `slug`로 해석하고 코드 블록·인라인 코드 안의 `[[…]]`는 링크로 보지 않는다.

## 2. 리포트 출력

> 📋 **Wiki Lint Report** ({today})
> Pages scanned: {scanned}
>
> 🔴 Errors (n) — broken_link / missing_frontmatter / invalid_slug / duplicate_slug / bad_path / type_dir_mismatch / missing_source / raw_misplaced / raw_bad_name
> 🟡 Warnings (n) — orphan / unhubbed / missing_backlink / stale / duplicate_title / date_mismatch / oversized_source
> 🔵 Info (n) — unindexed / far_from_hub / raw_tool_dir
>
> 각 항목 한 줄: `{check} {page} {detail}`

## 3. 자동 수정 제안

수정 가능한 카테고리가 있으면 사용자에게 묻는다:

> 자동 수정 가능 항목 n개. 수정할까요?
> - broken_link 제거/올바른 slug로 교체
> - missing_backlink 추가
> - unindexed 항목 index.md에 추가
> - missing_frontmatter 채우기
> - missing_source를 실재하는 raw basename으로 교정
> - bad_path / type_dir_mismatch 페이지를 `{type}/{created}-{slug}.md`로 이동

`duplicate_title`은 자동수정하지 않는다 — 병합 판단이 필요하므로 **update/distill의 merge-and-split 병합**으로 안내한다. `oversized_source`도 자동으로 자르지 않는다 — update op에서 요약·시사점·링크로 줄이도록 안내. `raw_misplaced`·`raw_bad_name`은 raw 불변 규칙상 **이름·위치만** 바꾸는 일이라 대상 목록을 보여 주고 사용자 확인 후 이동한다(본문 무수정).

<onaccept>
PRINCIPLES.md frontmatter, bidirectional, wikilink Read. 그 다음:

- broken_link → 해당 페이지에서 wikilink 제거 또는 올바른 slug로 Edit
- missing_backlink → 대상 페이지 Related 섹션에 `[[from]]` 추가
- unindexed → index.md 적절한 카테고리에 `- [[{slug}]] — {one-line}` 추가
- unhubbed → SCHEMA.md 허브 규칙대로 맞는 허브의 절에 매달고 갈래 대표 태그 추가. 맞는 갈래가 없으면 사용자에게 묻는다 (허브 신설은 사용자 결정)
- missing_frontmatter → 누락 필드 채움 (`created`/`updated`는 파일 mtime 사용, mtime을 못 얻으면 today)
- missing_source → `raw/sources/`에서 같은 slug를 가진 파일을 찾아 basename으로 교정, 없으면 항목 제거 후 보고
- bad_path / type_dir_mismatch → 페이지 내용은 그대로 두고 `wiki/pages/{type}/{created}-{slug}.md`로 이동

적용 후 lint를 재실행해 잔여 항목을 보고한다.
</onaccept>

## 4. 로그

```bash
scripts/append_log.py {wiki_root} lint "{e} errors, {w} warnings, {i} info"
```

자동 수정을 적용했으면 stdin으로 `Fixed: <one-line summary>` 전달.
