#!/usr/bin/env python3
"""Extract human-readable text from a Claude Code session transcript.

Sessions live at ~/.claude/projects/<project-slug>/<uuid>.jsonl, one JSON
event per line. This strips tool noise (tool_use / tool_result / thinking)
and sidechains, leaving just user prompts and assistant prose — so an LLM
can summarize a conversation without loading megabytes of context.

Usage:
  session_text.py <uuid|path>            # emit clean transcript
  session_text.py --list [--limit N] [--project SUBSTR]

--list ranks sessions by recency (mtime) across all projects; --project
filters by substring of the project dir name or the session's cwd.
"""
import datetime
import json
import sys
from pathlib import Path

PROJECTS = Path("~/.claude/projects").expanduser()
LIST_SCAN_LINES = 300  # cap per-file read when listing (title/cwd appear early)


def iter_events(path: Path):
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def _text_from_content(content):
    """User content is str (a prompt) or a list of blocks (tool_result → skip).
    Assistant content is a list of blocks; keep only type==text."""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = [b.get("text", "") for b in content
                 if isinstance(b, dict) and b.get("type") == "text"]
        return "\n".join(p for p in parts if p).strip()
    return ""


def resolve(arg: str) -> Path:
    p = Path(arg).expanduser()
    if p.suffix == ".jsonl" and p.exists():
        return p
    matches = sorted(PROJECTS.glob(f"*/{arg}.jsonl"))
    if matches:
        return matches[0]
    matches = sorted(PROJECTS.glob(f"*/{arg}*.jsonl"))
    if matches:
        return matches[0]
    sys.exit(f"session not found: {arg}")


def emit(path: Path) -> int:
    title, cwd, branch, sid = None, None, None, None
    first_ts = last_ts = None
    turns = []  # (role, ts, text)
    for o in iter_events(path):
        t = o.get("type")
        if t == "ai-title":
            title = o.get("aiTitle") or title
            continue
        if o.get("isSidechain") or o.get("isMeta"):
            continue
        msg = o.get("message")
        if not isinstance(msg, dict) or t not in ("user", "assistant"):
            continue
        cwd = cwd or o.get("cwd")
        branch = branch or o.get("gitBranch")
        sid = sid or o.get("sessionId")
        ts = o.get("timestamp")
        text = _text_from_content(msg.get("content"))
        if not text:  # tool_result-only user turn, or tool_use-only assistant turn
            continue
        if ts:
            first_ts = first_ts or ts
            last_ts = ts
        turns.append((msg.get("role"), ts, text))

    u = sum(1 for r, _, _ in turns if r == "user")
    a = sum(1 for r, _, _ in turns if r == "assistant")
    print(f"# Session: {title or path.stem}")
    print(f"- session: {sid or path.stem}")
    print(f"- transcript: {path}")
    print(f"- cwd: {cwd or '?'}")
    print(f"- branch: {branch or '?'}")
    print(f"- span: {first_ts or '?'} → {last_ts or '?'}")
    print(f"- turns: user {u}, assistant {a}\n\n---\n")
    for role, ts, text in turns:
        who = "🧑 User" if role == "user" else "🤖 Assistant"
        stamp = f" [{ts}]" if ts else ""
        print(f"## {who}{stamp}\n\n{text}\n")
    return 0


def scan_meta(path: Path):
    title, cwd, first_user = None, None, None
    for i, o in enumerate(iter_events(path)):
        if i >= LIST_SCAN_LINES:
            break
        if o.get("aiTitle"):
            title = o["aiTitle"]
        cwd = cwd or o.get("cwd")
        if first_user is None and o.get("type") == "user":
            msg = o.get("message")
            if isinstance(msg, dict) and isinstance(msg.get("content"), str):
                first_user = msg["content"].strip().replace("\n", " ")[:80]
    return title, cwd, first_user


def do_list(limit: int, project: str | None) -> int:
    files = sorted(PROJECTS.glob("*/*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    shown = 0
    for p in files:
        if shown >= limit:
            break
        if project and project not in p.parent.name:
            title, cwd, first_user = scan_meta(p)
            if not (cwd and project in cwd):
                continue
        else:
            title, cwd, first_user = scan_meta(p)
        date = datetime.date.fromtimestamp(p.stat().st_mtime).isoformat()
        print(f"{date}  {p.stem}")
        print(f"    title: {title or '(untitled)'}")
        print(f"    cwd:   {cwd or '?'}")
        if first_user:
            print(f"    first: {first_user}")
        shown += 1
    if shown == 0:
        print("(no sessions found)")
    return 0


def main() -> int:
    argv = sys.argv[1:]
    if not argv:
        print(__doc__.strip().split("\n\n")[0], file=sys.stderr)
        return 2
    if argv[0] == "--list":
        limit, project = 20, None
        rest = argv[1:]
        i = 0
        while i < len(rest):
            if rest[i] == "--limit" and i + 1 < len(rest):
                limit = int(rest[i + 1]); i += 2
            elif rest[i] == "--project" and i + 1 < len(rest):
                project = rest[i + 1]; i += 2
            else:
                i += 1
        return do_list(limit, project)
    return emit(resolve(argv[0]))


if __name__ == "__main__":
    sys.exit(main())
