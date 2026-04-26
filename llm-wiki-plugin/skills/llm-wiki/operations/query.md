# Operation: query

위키를 검색하고 인용 포함 답변을 합성한다.

## Prerequisites
- Phase 0 완료, `{wiki_root}/SCHEMA.md` 존재

## References
질문에 답하면서 `[[slug]]` 인용을 쓰려면 PRINCIPLES.md "Wikilink Format"이 필요. 답변을 위키 페이지로 저장(아카이브)하기로 결정한 경우에는 PRINCIPLES.md "Page Frontmatter", "Slug Rules", "Bidirectional Linking Policy"도 추가로 필요. 처음에는 Read하지 말고, 4단계에서 사용자가 "Yes"한 경우에만 Read한다.

## Steps

1. **인덱스 스캔**:
   - `{wiki_root}/wiki/index.md`를 전체 읽기
   - 사용자 질문에서 관련 페이지 식별
   - 일반 지식보다 위키 내용을 우선시

2. **페이지 회수**:
   - 식별된 페이지의 전체 내용 읽기
   - 관련 있는 경우 `[[cross-references]]`를 최대 2 hop까지 따라가기
   - 포괄적인 컨텍스트 구축

3. **답변 합성**:
   - 모든 주장을 인라인 `[[slug]]` 인용으로 위키 소스에 근거시키기
   - 페이지 간 동의/불일치를 명시
   - 공백을 명시적으로 표시: "위키에 {topic}에 대한 내용이 없습니다"
   - 적절한 형식: 사실은 산문, 비교는 표, 절차는 번호 단계

4. **아카이빙 제안** — `AskUserQuestion`:
   > 이 답변을 위키 페이지로 저장할까요?
   > 제안 slug: `{suggested-slug}`

   - **Yes**:
     - PRINCIPLES.md를 Read (frontmatter, slug rules, bidirectional 필요)
     - `type: concept`, tags `[query, analysis]`로 페이지 생성
     - mini-ingest 수행: index.md 갱신, log.md 추가, 백링크 감사
   - **No**: log.md에만 다음 항목 추가 (PRINCIPLES.md "Log Entry Format"):
     ```markdown
     ## [{today}] query | {question_summary} (not filed)
     ```
