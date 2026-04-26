# LLM Wiki Principles

위키 전반의 공통 규칙. 각 operation 파일은 필요한 섹션만 참조한다.

## 3-Layer Architecture

### Layer 1: Raw Sources (`raw/`)
- **Immutable** — 한 번 저장된 소스는 절대 수정하지 않는다
- 논문, 기사, URL 스냅샷, 트랜스크립트, 노트 등 원본 자료
- 형식: `raw/{slug}.md` 또는 `raw/{slug}.{ext}` (binary)
- LLM은 읽기만 가능, 쓰기 불가

### Layer 2: Wiki (`wiki/`)
- LLM이 생성하고 유지보수하는 컴파일된 지식
- 구조:
  - `wiki/index.md` — 전체 페이지 카탈로그 (페이지 추가/변경마다 갱신)
  - `wiki/overview.md` — 위키 전체 요약 (이해가 바뀔 때 갱신)
  - `wiki/log.md` — append-only 작업 이력
  - `wiki/pages/{slug}.md` — 개별 위키 페이지 (flat 구조, 하위 디렉토리 없음)

### Layer 3: Schema (`SCHEMA.md`)
- 위키의 정체성 (이름, 설명, 소스 유형, 생성일)
- 스킬이 위키를 발견하는 진입점 (Phase 0에서 존재 여부로 판단)
- 위키는 단일 그래프로 운영. `[[slug]]` cross-reference가 한 그래프 안에서만 유효하므로 위키를 여러 개로 쪼개지 않는다

## Page Types

위키 페이지의 `type` 필드는 다음 중 하나:

- **source**: 원본 자료 요약 (논문, 기사, 영상, 코드 등)
- **entity**: 사람, 조직, 도구, 기술
- **concept**: 아이디어, 패턴, 원칙

`index`, `overview`는 시스템 페이지 type으로, index/overview 템플릿에서만 사용한다.

## Page Frontmatter

모든 위키 페이지는 YAML frontmatter로 시작한다:

```yaml
---
title: Page Title
slug: page-title
type: source | entity | concept
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [slug1, slug2]
tags: [tag1, tag2]
---
```

### 필수 필드
- `title`: 페이지 제목
- `slug`: 파일명과 동일 (확장자 제외)
- `type`: 위 Page Types 중 하나
- `created`: 생성일
- `updated`: 최종 수정일

### 선택 필드
- `sources`: 이 페이지가 참조하는 소스 slug 목록
- `tags`: 분류 태그

## Wikilink Format

- 기본: `[[slug]]` → `wiki/pages/{slug}.md`로 연결
- 커스텀 표시: `[[slug|표시 텍스트]]`
- 위키 내부 링크에만 사용. 외부 URL은 일반 마크다운 링크 사용
- `slug` = 확장자 `.md`를 뺀 파일명

## Bidirectional Linking Policy

- A 페이지가 B를 `[[B]]`로 참조하면, B 페이지의 Related 섹션에도 `[[A]]`가 있어야 함
- ingest/update 시 새/변경된 페이지에 대해 반드시 **백링크 감사** 수행
- Grep으로 전체 `wiki/pages/`를 스캔하여 누락된 역방향 링크 추가

## Slug Rules

- lowercase-with-hyphens만 허용
- 최대 50자
- 특수문자 불가 (알파벳, 숫자, 하이픈만)
- 예: "Attention Is All You Need" → `attention-is-all-you-need`
- 충돌 시 숫자 접미사: `concept-2`

## Immutability Rules

1. **`raw/` 불변**: 소스 파일은 추가만 가능, 수정/삭제 불가
2. **`log.md` append-only**: 기존 로그 항목을 수정하거나 삭제하지 않음. 항상 맨 아래에 추가
3. **SCHEMA.md 보존**: 사용자 확인 없이 SCHEMA.md를 수정하지 않음
4. **`wiki/pages/` flat**: 모든 페이지는 `{slug}.md` 형태이며 하위 디렉토리 없음

## Log Entry Format

`wiki/log.md`에 추가하는 항목 형식:

```markdown
## [YYYY-MM-DD] <operation> | <description>
- Pages created: [[slug1]], [[slug2]]
- Pages updated: [[slug3]], [[slug4]]
- Backlinks added: <count>
```

Operations: `init`, `ingest`, `query`, `lint`, `update`
