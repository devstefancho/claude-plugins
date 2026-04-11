# {domain} Wiki Schema

## Identity
- **Domain:** {domain_description}
- **Created:** {date}
- **Source types:** {source_types}

## Page Types
- **source**: 원본 자료 요약 (논문, 기사, 영상 등)
- **entity**: 사람, 조직, 도구, 기술
- **concept**: 아이디어, 패턴, 원칙

## Frontmatter Format
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

## Cross-References
- Internal links: `[[slug]]` or `[[slug|display text]]`
- slug = filename without `.md`
- All links must be bidirectional

## Index Categories
- Sources
- Entities
- Concepts

## Governance Rules (immutable)
1. `raw/` is immutable — never modify source files
2. `log.md` is append-only — never rewrite, only append
3. `index.md` updates with every operation adding/changing pages
4. `wiki/pages/` is flat — all pages as `{slug}.md`, NO subdirectories
5. `overview.md` reflects current synthesis across all sources
