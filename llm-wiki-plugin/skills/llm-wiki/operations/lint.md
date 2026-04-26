# Operation: lint

위키 건강도를 감사하고 수정안을 제시한다.

## Prerequisites
- Phase 0 완료, `{wiki_root}/SCHEMA.md` 존재

## References
이 operation은 PRINCIPLES.md의 모든 규칙을 위반 검사 기준으로 사용한다. 시작 전에 PRINCIPLES.md를 Read한다 — 특히 "Page Frontmatter"(필수 필드), "Slug Rules", "Bidirectional Linking Policy", "Immutability Rules"가 검사 항목의 근거다.

## Steps

1. **인벤토리 구축**:
   - `Glob {wiki_root}/wiki/pages/*.md`로 모든 페이지 수집
   - `{wiki_root}/wiki/index.md`, `{wiki_root}/wiki/overview.md` 읽기
   - 수집: 모든 slug, 모든 `[[slug]]` 참조, 모든 frontmatter 필드

2. **점검 실행**:

   **🔴 Errors** (반드시 수정):
   - **깨진 링크**: 대응 파일이 없는 `[[slug]]`
   - **누락된 frontmatter**: PRINCIPLES.md "Page Frontmatter" 필수 필드(`title`, `slug`, `type`, `created`, `updated`) 중 하나라도 없음
   - **잘못된 slug**: PRINCIPLES.md "Slug Rules" 위반 (lowercase-with-hyphens 아님 등)

   **🟡 Warnings** (수정 권장):
   - **고아 페이지**: 인바운드 링크 0 (index, overview 제외)
   - **누락된 백링크**: A→B는 있으나 B→A가 없음 (PRINCIPLES.md "Bidirectional Linking Policy" 위반)
   - **오래된 페이지**: `updated`가 90일 이상 지났고 시간 표현("current", "latest", "recent")을 포함

   **🔵 Info**:
   - **누락된 개념 페이지**: 엔티티/개념이 3회 이상 언급되지만 전용 페이지 없음
   - **인덱스 누락**: 페이지는 존재하지만 `index.md`에 등록되지 않음

3. **리포트 출력**:
   > 📋 **Wiki Lint Report** ({today})
   >
   > **Pages scanned:** {count}
   >
   > 🔴 **Errors ({count})**
   > {error_list}
   >
   > 🟡 **Warnings ({count})**
   > {warning_list}
   >
   > 🔵 **Info ({count})**
   > {info_list}

4. **수정 제안** — `AskUserQuestion`:
   > 자동 수정 가능한 항목이 {count}개 있습니다. 수정할까요?
   > - Broken links 제거/수정
   > - Missing backlinks 추가
   > - Index 누락 항목 추가
   > - Missing frontmatter 채우기

   - 수락: 수정 적용, 변경 사항 보고
   - 거부: 건너뜀

5. **`{wiki_root}/wiki/log.md`에 추가** (PRINCIPLES.md "Log Entry Format"):
   ```markdown
   ## [{today}] lint | {error_count} errors, {warning_count} warnings, {info_count} info
   Fixed: {list_of_fixes_or_none}
   ```
