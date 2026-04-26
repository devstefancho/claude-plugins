# Operation: ingest

새 소스를 처리하고 위키에 통합한다.

## Prerequisites
- Phase 0 완료
- `{wiki_root}/SCHEMA.md` 존재 (없으면 init 안내 후 종료 — Phase 0이 처리)

## References
이 operation을 시작하기 전에 `PRINCIPLES.md`를 Read한다 — slug 규칙, frontmatter 형식, 양방향 링킹 정책이 모든 단계에서 필요.

## Steps

1. **소스 수락** — 사용자 입력으로부터 소스 유형 판별:
   - 파일 경로 → `Read`로 파일 읽기
   - URL → `WebFetch`로 가져오기. 사용 불가 시 사용자에게 내용 붙여넣기 요청
   - 붙여넣은 텍스트 → 그대로 사용

2. **원본 소스 저장** (slug는 PRINCIPLES.md "Slug Rules"를 따라 생성):
   - **텍스트/마크다운** → `{wiki_root}/raw/{slug}.md`에 메타데이터 헤더와 함께 저장:
     ```markdown
     ---
     source_url: {url_if_applicable}
     ingested: {today}
     type: {article|paper|video|code|note}
     ---

     {full_source_content}
     ```
   - **바이너리 (PDF, 이미지)** → `{wiki_root}/raw/{slug}.{ext}`로 원본 형식 보존하여 복사. 동반 파일 `{wiki_root}/raw/{slug}.meta.md`에 위 메타데이터 헤더 작성 (content 필드 = 파일 경로 참조)

3. **주요 시사점 제시** — `AskUserQuestion`:
   > 📖 **{source_title}** 분석 완료
   >
   > **핵심 포인트:**
   > 1. {takeaway_1}
   > 2. {takeaway_2}
   > 3. {takeaway_3}
   >
   > **관련 엔티티/개념:** {entity_list}
   >
   > 강조하거나 제외할 내용이 있나요? (없으면 Enter)

4. **소스 요약 페이지 작성** — `templates/page-template.md` 사용:
   - `type: source` (PRINCIPLES.md "Page Types" 참조)
   - 포함: URL/경로, 수집일, 2-3 문단 합성, 핵심 시사점, 엔티티/개념 링크
   - frontmatter는 PRINCIPLES.md "Page Frontmatter" 형식 준수

5. **엔티티/개념 페이지 갱신** — 소스에 언급된 각 엔티티/개념마다:
   - `{wiki_root}/wiki/pages/`에서 기존 페이지를 `Grep`
   - **존재**: 페이지를 읽고 `sources` frontmatter에 추가, 본문에 새 정보 추가, `updated` 날짜 갱신
   - **없음**: `type: entity` 또는 `type: concept`로 새 페이지 생성

6. **양방향 백링크 감사** (CRITICAL — PRINCIPLES.md "Bidirectional Linking Policy" 참조):
   - 새/갱신 페이지의 모든 `[[slug]]`에 대해, 대상 페이지가 역으로 링크하지 않으면 대상 Related 섹션에 `[[new-slug]]` 추가
   - `{wiki_root}/wiki/pages/`의 모든 파일을 `Grep`하여 새 소스의 엔티티/개념이 `[[links]]` 없이 언급된 곳을 찾아 wikilink 추가

7. **`{wiki_root}/wiki/index.md` 갱신**:
   - 적절한 카테고리(Sources/Entities/Concepts) 아래 항목 추가:
     `- [[{slug}]] — {one-line summary} _(ingested {today})_`
   - Recent 섹션을 최근 5개 항목으로 갱신

8. **`{wiki_root}/wiki/overview.md` 갱신**:
   - 새 소스가 이해를 바꾼다면 Key Themes 갱신, Open Questions 추가
   - Statistics 카운트 갱신
   - `updated` frontmatter 날짜 갱신

9. **`{wiki_root}/wiki/log.md`에 추가** (사용자 확인 불필요 — PRINCIPLES.md "Log Entry Format" 참조):
   ```markdown
   ## [{today}] ingest | {source_title}
   - Pages created: [[{slug1}]], [[{slug2}]]
   - Pages updated: [[{slug3}]], [[{slug4}]]
   - Backlinks added: {count}
   ```

10. **보고**:
    > ✅ **{source_title}** ingest 완료
    > - 소스 페이지: `[[{slug}]]`
    > - 생성된 페이지: {count}개
    > - 업데이트된 페이지: {count}개
    > - 추가된 백링크: {count}개
