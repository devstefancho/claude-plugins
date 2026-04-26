# Operation: update

지식이 바뀌거나 모순이 발생했을 때 위키 페이지를 개정한다.

## Prerequisites
- Phase 0 완료, `{wiki_root}/SCHEMA.md` 존재

## References
편집 시 frontmatter 갱신, 양방향 링크 유지, 불변 영역(`raw/`, `log.md` 기존 항목, `SCHEMA.md`) 보호가 필요. 시작 전에 PRINCIPLES.md를 Read한다 — "Page Frontmatter"(특히 `updated` 필드), "Bidirectional Linking Policy", "Immutability Rules"가 핵심.

## Steps

1. **대상 식별**:
   - 사용자 요청에서: 특정 페이지 이름, 주제, lint 권고 등
   - `{wiki_root}/wiki/pages/`에서 관련 페이지를 `Grep`

2. **변경 제안** — 각 대상 페이지에 대해:
   > **{page_title}** (`[[{slug}]]`)
   > - 현재: `{current_text}`
   > - 변경: `{proposed_text}`
   > - 이유: {reason}

   `AskUserQuestion`으로 사용자 확인 대기.

3. **편집 적용**:
   - `Edit`으로 페이지 수정
   - PRINCIPLES.md "Page Frontmatter"에 따라 `updated` 필드를 오늘 날짜로 갱신
   - 변경이 wikilink 그래프에 영향을 주면 PRINCIPLES.md "Bidirectional Linking Policy"에 따라 백링크 감사

4. **모순 점검**:
   - 갱신된 내용과 관련된 주장에 대해 모든 페이지를 `Grep`
   - 충돌하는 단언을 표시
   - 그 페이지들도 갱신할지 제안 (사용자 확인 후 적용)

5. **메타데이터 갱신**:
   - 페이지 목적이 바뀌었으면 `index.md` 요약 개정
   - 전체 이해가 바뀌었으면 `overview.md` 갱신

6. **`{wiki_root}/wiki/log.md`에 추가** (PRINCIPLES.md "Log Entry Format"):
   ```markdown
   ## [{today}] update | [[{slug1}]], [[{slug2}]]
   Reason: {explanation}
   Changes: {brief_summary}
   ```

## 금지 사항
- `raw/` 파일 수정 (불변)
- `log.md`의 기존 항목 수정/삭제 (append-only)
- `SCHEMA.md` 수정 (사용자 명시 확인 없이는 금지)
