# LLM Wiki Plugin

Andrej Karpathy의 LLM Wiki 패턴을 Claude Code 스킬로 구현. LLM이 raw 소스를 읽고 마크다운 위키로 컴파일하여 지식을 축적하는 개인 위키 시스템.

## Installation

```bash
/plugin marketplace add .
/plugin install llm-wiki-plugin@devstefancho-claude-plugins
```

## Trigger Keywords

`wiki init`, `wiki ingest`, `wiki query`, `wiki lint`, `wiki update`, `위키 초기화`, `위키 추가`, `위키 질문`, `위키 검사`, `위키 수정`

## Operations

### `wiki init` — 새 위키 도메인 생성
도메인명, 설명, 소스 유형을 입력받아 위키 구조를 초기화합니다.

### `wiki ingest <source>` — 소스 추가
파일, URL, 텍스트를 읽어 위키 페이지로 컴파일합니다. 관련 페이지를 자동 업데이트하고 양방향 백링크를 생성합니다.

### `wiki query <question>` — 위키 검색
위키를 기반으로 질문에 답변하며 `[[slug]]` 인용을 포함합니다. 답변을 위키 페이지로 저장할 수 있습니다.

### `wiki lint` — 위키 건강 검사
broken links, orphan pages, missing backlinks, stale pages 등을 검출하고 자동 수정을 제안합니다.

### `wiki update <page>` — 페이지 수정
특정 페이지를 수정하고 연관 페이지의 모순을 체크합니다.

## Directory Structure

```
{wiki_root}/
└── {domain}/
    ├── SCHEMA.md          # 위키 규약
    ├── raw/               # 원본 소스 (불변)
    └── wiki/
        ├── index.md       # 페이지 카탈로그
        ├── overview.md    # 도메인 요약
        ├── log.md         # 작업 이력 (append-only)
        └── pages/         # 위키 페이지 (flat)
            └── {slug}.md
```

## Configuration

최초 실행 시 위키 루트 경로를 설정합니다. 설정은 `config.json`에 저장됩니다.

```json
{ "wiki_root": "~/wiki" }
```

## Design

Based on [Andrej Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — 3-layer architecture with compiled knowledge that accumulates over time.
