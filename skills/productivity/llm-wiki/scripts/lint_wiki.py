#!/usr/bin/env python3
"""Audit wiki health.

Usage:
  lint_wiki.py <wiki_root> [--json]

Layout this script enforces (PRINCIPLES.md architecture):
  wiki/pages/{type}/{YYYY-MM-DD}-{slug}.md   type dir == frontmatter type, date == created
  raw/sources/{YYYY-MM-DD|YYYY-MM}-{slug}.{ext}   human/ingest area
  raw/<other>/                                tool-owned, own convention, exempt (reported as info)

Wikilinks [[slug]] resolve through frontmatter `slug:` (file names are independent).

Checks:
  errors:   broken_link, missing_frontmatter, invalid_slug, duplicate_slug, bad_path,
            type_dir_mismatch, missing_source, raw_misplaced, raw_bad_name
  warnings: orphan, missing_backlink, stale, duplicate_title, date_mismatch, oversized_source
  info:     unindexed, raw_tool_dir

Frontmatter parsing is intentionally permissive — the 5 required scalar fields
(title, slug, type, created, updated) plus the `sources` list are read.
"""
import collections
import datetime
import json
import re
import sys
from pathlib import Path

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,49}$")
PAGE_FILE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-([a-z0-9][a-z0-9-]{0,49})\.md$")
RAW_FILE_RE = re.compile(r"^\d{4}-\d{2}(-\d{2})?-[a-z0-9][a-z0-9-]*(\.[A-Za-z0-9]+)+$")
# wikilink target may include #anchor; strip anchor before resolving as slug
WIKILINK_RE = re.compile(r"\[\[([^\]\|#]+)(?:#[^\]\|]+)?(?:\|[^\]]+)?\]\]")
FENCE_RE = re.compile(r"```.*?```", re.S)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
REQUIRED_FM = ("title", "slug", "type", "created", "updated")
HUB_MAX_DEPTH = 3
STALE_DAYS = 90
SOURCE_MAX_CHARS = 8000  # source page = summary + implications + links; the full text lives in raw
TIME_WORDS = re.compile(r"current|latest|recent|now|today|최신|최근", re.I)


def split_frontmatter(text: str):
    """Return (fm_text or None, body). Tolerates EOF without trailing newline."""
    if not text.startswith("---\n"):
        return None, text
    for marker in ("\n---\n", "\n---"):
        idx = text.find(marker, 4)
        if idx >= 0:
            return text[4:idx], text[idx + len(marker):]
    return None, text


def parse_frontmatter(text: str):
    """Return (fm_dict, body). Scalars only; `sources` list parsed separately."""
    fm_text, body = split_frontmatter(text)
    if fm_text is None:
        return {}, body
    fm = {}
    for line in fm_text.split("\n"):
        if line.startswith((" ", "\t", "-")) or ":" not in line:
            continue
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip()
    fm["_sources"] = parse_list_field(fm_text, "sources")
    fm["_tags"] = parse_list_field(fm_text, "tags")
    return fm, body


def parse_list_field(fm_text: str, key: str):
    """Parse `key: [a, b]` or a `key:` block list. Returns list of strings."""
    lines = fm_text.split("\n")
    for i, line in enumerate(lines):
        if not line.startswith(key + ":"):
            continue
        v = line.partition(":")[2].strip()
        if v.startswith("[") and v.endswith("]"):
            return [x.strip().strip("'\"") for x in v[1:-1].split(",") if x.strip()]
        if v:
            return [v.strip("'\"")]
        out = []
        for cont in lines[i + 1:]:
            if re.match(r"^\s*-\s+", cont):
                out.append(re.sub(r"^\s*-\s+", "", cont).split("#")[0].strip().strip("'\""))
            elif cont.strip() == "" or cont.startswith((" ", "\t")):
                continue
            else:
                break
        return out
    return []


def wikilinks(body: str):
    """Wikilinks outside fenced blocks and inline code (Swift `[[String: Any]]` is not a link)."""
    cleaned = INLINE_CODE_RE.sub("", FENCE_RE.sub("", body))
    return set(t.strip() for t in WIKILINK_RE.findall(cleaned))


def raw_exists(root: Path, entry: str) -> bool:
    """`sources:` entry = raw basename without extension. `a/b` resolves under raw/, else raw/sources/."""
    base = root / "raw" / entry if "/" in entry else root / "raw" / "sources" / entry
    return any(base.parent.glob(base.name + ".*")) if base.parent.exists() else False


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    json_out = "--json" in sys.argv[1:]
    if not args:
        print("usage: lint_wiki.py <wiki_root> [--json]", file=sys.stderr)
        return 2

    root = Path(args[0]).expanduser().resolve()
    pages_dir = root / "wiki" / "pages"
    index_path = root / "wiki" / "index.md"
    if not pages_dir.exists():
        print(f"refuse: {pages_dir} does not exist", file=sys.stderr)
        return 1

    errors, warnings, info = [], [], []
    today = datetime.date.today()

    pages = {}  # slug -> info
    inbound: dict = {}
    for p in sorted(pages_dir.rglob("*.md")):
        rel = p.relative_to(pages_dir)
        text = p.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        m = PAGE_FILE_RE.match(p.name)
        file_date, file_slug = (m.group(1), m.group(2)) if m else (None, p.stem)
        slug = fm.get("slug") or file_slug
        ref = str(rel)
        if len(rel.parts) != 2 or not m:
            errors.append({"check": "bad_path", "page": ref,
                           "expected": "wiki/pages/{type}/{YYYY-MM-DD}-{slug}.md"})
        elif fm.get("type") and fm["type"] != rel.parts[0]:
            errors.append({"check": "type_dir_mismatch", "page": ref, "type": fm["type"], "dir": rel.parts[0]})
        if file_date and fm.get("created") and fm["created"][:10] != file_date:
            warnings.append({"check": "date_mismatch", "page": ref, "created": fm["created"], "file": file_date})
        if slug in pages:
            errors.append({"check": "duplicate_slug", "slug": slug, "pages": [pages[slug]["ref"], ref]})
            continue
        links = wikilinks(body)
        pages[slug] = {"ref": ref, "fm": fm, "body": body, "links": links}
        for tgt in links:
            inbound.setdefault(tgt, set()).add(slug)

    # also count inbound from index/overview so they're not flagged orphan
    for sys_page in (index_path, root / "wiki" / "overview.md"):
        if sys_page.exists():
            for tgt in wikilinks(sys_page.read_text(encoding="utf-8")):
                inbound.setdefault(tgt, set()).add(sys_page.stem)

    for slug, p in pages.items():
        if not SLUG_RE.match(slug):
            errors.append({"check": "invalid_slug", "page": p["ref"], "slug": slug})
        missing = [k for k in REQUIRED_FM if k not in p["fm"]]
        if missing:
            errors.append({"check": "missing_frontmatter", "page": slug, "fields": missing})
        for tgt in sorted(p["links"]):
            if tgt not in pages:
                errors.append({"check": "broken_link", "page": slug, "target": tgt})
        for src in p["fm"].get("_sources", []):
            if not raw_exists(root, src):
                errors.append({"check": "missing_source", "page": slug, "source": src})
        if slug not in inbound and slug not in ("index", "overview"):
            warnings.append({"check": "orphan", "page": slug})
        for tgt in sorted(p["links"]):
            if tgt in pages and slug not in pages[tgt]["links"]:
                warnings.append({"check": "missing_backlink", "from": slug, "to": tgt})
        u = p["fm"].get("updated", "")
        try:
            ud = datetime.date.fromisoformat(u[:10])
            if (today - ud).days > STALE_DAYS and TIME_WORDS.search(p["body"]):
                warnings.append({"check": "stale", "page": slug, "updated": u})
        except ValueError:
            pass
        if p["fm"].get("type") == "source" and len(p["body"]) > SOURCE_MAX_CHARS:
            warnings.append({"check": "oversized_source", "page": slug, "chars": len(p["body"]),
                             "limit": SOURCE_MAX_CHARS})

    # unhubbed / far_from_hub — topic grouping. A page should sit under a hub, not just
    # be linked from somewhere. Depth: hub(0) -> 갈래(1) -> page(2) is the intended shape.
    hub_roots = {slug for slug, p in pages.items()
                 if "hub" in (p["fm"].get("_tags") or []) or slug == "operating-guidelines"}
    if hub_roots:
        depth = {r: 0 for r in hub_roots}
        frontier = collections.deque(hub_roots)
        while frontier:
            cur = frontier.popleft()
            for tgt in sorted(pages.get(cur, {}).get("links", ())):
                if tgt in pages and tgt not in depth:
                    depth[tgt] = depth[cur] + 1
                    frontier.append(tgt)
        for slug in pages:
            if slug in ("index", "overview"):
                continue
            if slug not in depth:
                warnings.append({"check": "unhubbed", "page": slug})
            elif depth[slug] >= HUB_MAX_DEPTH:
                info.append({"check": "far_from_hub", "page": slug, "depth": depth[slug]})

    # duplicate_title — pages sharing an identical title are merge candidates
    by_title: dict = {}
    for slug, p in pages.items():
        t = p["fm"].get("title", "").strip().lower()
        if t:
            by_title.setdefault(t, []).append(slug)
    for t, slugs in by_title.items():
        if len(slugs) > 1:
            warnings.append({"check": "duplicate_title", "pages": sorted(slugs)})

    if index_path.exists():
        index_text = index_path.read_text(encoding="utf-8")
        for slug in pages:
            if slug in ("index", "overview"):
                continue
            if f"[[{slug}]]" not in index_text and f"[[{slug}|" not in index_text:
                info.append({"check": "unindexed", "page": slug})

    # raw layout — human/ingest area is raw/sources/ only; other dirs are tool-owned
    raw_dir = root / "raw"
    raw_sources = 0
    if raw_dir.exists():
        for entry in sorted(raw_dir.iterdir()):
            if entry.name.startswith("."):
                continue
            if entry.is_file():
                errors.append({"check": "raw_misplaced", "path": f"raw/{entry.name}",
                               "expected": "raw/sources/{YYYY-MM-DD}-{slug}.{ext}"})
            elif entry.name != "sources":
                info.append({"check": "raw_tool_dir", "path": f"raw/{entry.name}/"})
        src_dir = raw_dir / "sources"
        if src_dir.exists():
            for f in sorted(src_dir.iterdir()):
                if f.name.startswith("."):
                    continue
                if f.is_dir():
                    errors.append({"check": "raw_misplaced", "path": f"raw/sources/{f.name}/",
                                   "expected": "no sub-directories under raw/sources/"})
                    continue
                raw_sources += 1
                if not RAW_FILE_RE.match(f.name):
                    errors.append({"check": "raw_bad_name", "path": f"raw/sources/{f.name}",
                                   "expected": "{YYYY-MM-DD|YYYY-MM}-{slug}.{ext}"})

    summary = {"scanned": len(pages), "raw_sources": raw_sources,
               "errors": errors, "warnings": warnings, "info": info}

    if json_out:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    print(f"# Wiki Lint Report ({today})")
    print(f"Pages scanned: {len(pages)} · raw/sources: {raw_sources}\n")
    print(f"## Errors ({len(errors)})")
    for e in errors or [{"check": "(none)"}]:
        print(f"- {e}")
    print(f"\n## Warnings ({len(warnings)})")
    for w in warnings or [{"check": "(none)"}]:
        print(f"- {w}")
    print(f"\n## Info ({len(info)})")
    for i in info or [{"check": "(none)"}]:
        print(f"- {i}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
