#!/usr/bin/env python3
"""Pre-tool / beforeReadFile hook: deny reads that match the local policy."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:  # pragma: no cover
    tomllib = None  # type: ignore


def policy_path() -> Path:
    override = os.environ.get("AGENT_POLICY_FILE")
    if override:
        return Path(override).expanduser()
    xdg = os.environ.get("XDG_CONFIG_HOME")
    root = Path(xdg) if xdg else Path.home() / ".config"
    return root / "agent-policy" / "policy.toml"


def load_patterns() -> list[str]:
    path = policy_path()
    if tomllib is None or not path.exists():
        return []
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    return list(data.get("deny_reads") or [])


def expand(pattern: str) -> str:
    if pattern.startswith("~/"):
        return str(Path.home() / pattern[2:])
    if pattern == "~":
        return str(Path.home())
    return pattern


def glob_to_re(pat: str) -> re.Pattern[str]:
    i = 0
    out: list[str] = ["^"]
    while i < len(pat):
        if pat.startswith("/**", i) and i + 3 == len(pat):
            out.append("(?:/.*)?")
            i += 3
        elif pat.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif pat.startswith("**", i):
            out.append(".*")
            i += 2
        elif pat[i] == "*":
            out.append("[^/]*")
            i += 1
        elif pat[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(pat[i]))
            i += 1
    out.append("$")
    return re.compile("".join(out))


def match(path: str, pattern: str) -> bool:
    path = os.path.abspath(os.path.expanduser(path))
    pat = expand(pattern)
    if not any(ch in pat for ch in "*?"):
        target = os.path.abspath(os.path.expanduser(pat))
        return path == target or path.startswith(target + os.sep)
    if not pat.startswith("/") and not pat.startswith("**"):
        pat = "**/" + pat
    return glob_to_re(pat).match(path) is not None


def extract_path(payload: dict) -> str:
    if payload.get("file_path"):
        return str(payload["file_path"])
    if payload.get("filePath"):
        return str(payload["filePath"])
    tool = payload.get("toolInput") or payload.get("tool_input") or {}
    if isinstance(tool, str):
        try:
            tool = json.loads(tool)
        except json.JSONDecodeError:
            tool = {}
    if isinstance(tool, dict):
        for key in ("target_file", "file_path", "filePath", "path"):
            if tool.get(key):
                return str(tool[key])
    return ""


def is_cursor(payload: dict) -> bool:
    event = (
        payload.get("hook_event_name")
        or payload.get("hookEventName")
        or os.environ.get("GROK_HOOK_EVENT")
        or ""
    )
    return "file_path" in payload or event in {"beforeReadFile", "beforeTabFileRead"}


def emit(deny: bool, cursor: bool, reason: str) -> int:
    if cursor:
        body = {"permission": "deny" if deny else "allow"}
        if deny:
            body["user_message"] = reason
            body["agent_message"] = reason
    else:
        body = {"decision": "deny" if deny else "allow"}
        if deny:
            body["reason"] = reason
    print(json.dumps(body))
    return 2 if deny else 0


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return 0
    path = extract_path(payload)
    if not path:
        return 0
    cursor = is_cursor(payload)
    for pat in load_patterns():
        try:
            if match(path, pat):
                return emit(True, cursor, f"blocked by agent-policy deny_reads: {pat}")
        except Exception:
            continue
    return emit(False, cursor, "")


if __name__ == "__main__":
    raise SystemExit(main())
