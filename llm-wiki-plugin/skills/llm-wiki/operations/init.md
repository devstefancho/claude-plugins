# Operation: init

`wiki_root`에 새 위키를 생성한다.

## Prerequisites
- Phase 0 완료 (config.json 존재, `wiki_root` 해석됨)
- `{wiki_root}/SCHEMA.md`가 **없어야** 함 (없으니 init이 호출됐을 것)

## Steps

1. **중복 init 방지** — `{wiki_root}/SCHEMA.md`가 이미 존재하면 다음 메시지로 중단:
   > "위키가 이미 `{wiki_root}`에 존재합니다. init은 한 번만 실행할 수 있습니다."

2. **사용자에게 위키 정체성 질문** — `AskUserQuestion`:
   > 위키를 생성합니다.
   > - **위키 이름** (제목용, 자유 형식 — 예: "Stefan's Knowledge Wiki"):
   > - **위키 설명** (한 줄 — 무엇을 다루는 위키인지):
   > - **소스 유형** (예: papers, articles, videos, code):

3. **디렉토리 구조 생성**:
   ```
   {wiki_root}/
   ├── SCHEMA.md
   ├── raw/
   └── wiki/
       ├── index.md
       ├── overview.md
       ├── log.md
       └── pages/
   ```

4. **템플릿으로부터 파일 생성**:
   - `SCHEMA.md` ← `templates/schema-template.md` (변수: `{wiki_title}`, `{description}`, `{source_types}`, `{date}`)
   - `wiki/index.md` ← `templates/index-template.md` (변수: `{wiki_title}`, `{date}`)
   - `wiki/overview.md` ← `templates/overview-template.md` (변수: `{wiki_title}`, `{description}`, `{date}`)
   - `wiki/log.md` ← 다음 초기 내용:
     ```markdown
     # Wiki Log

     Append-only operation record.

     ---

     ## [{today}] init | {wiki_title}
     - Wiki created at `{wiki_root}/`
     ```

5. **사용자에게 보고**:
   > ✅ 위키 `{wiki_title}` 생성 완료
   > - 경로: `{wiki_root}/`
   > - 다음 단계: `wiki ingest <source>` 로 소스를 추가하세요

## References

- 페이지 type, frontmatter, slug 등 공통 규칙: `PRINCIPLES.md` (init은 시스템 페이지만 만들므로 일반적으로 불필요)
