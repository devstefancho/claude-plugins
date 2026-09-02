---
title: Tags
slug: tags
type: index
created: {date}
updated: {date}
---

# {wiki_title} — Tags (MOC)

태그별 자동 목록. **Obsidian + Dataview 플러그인**에서 렌더링된다 (플러그인이 없으면 아래는 코드블록으로 보인다). 페이지의 `tags` frontmatter만 잘 채우면 이 뷰는 자동 갱신 — 수동 편집 불필요.

## 태그별 페이지

```dataview
TABLE rows.file.link AS "페이지"
FROM "wiki/pages"
FLATTEN tags AS tag
GROUP BY tag
SORT tag ASC
```

## 최근 갱신

```dataview
TABLE type, tags, updated
FROM "wiki/pages"
SORT updated DESC
LIMIT 15
```
