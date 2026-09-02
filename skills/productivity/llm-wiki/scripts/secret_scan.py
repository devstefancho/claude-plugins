#!/usr/bin/env python3
"""Scan text for likely secrets/credentials before it lands in the wiki.

Usage:
  secret_scan.py <file>        # scan a file
  secret_scan.py -             # scan stdin
  secret_scan.py <file> --json # machine-readable

Deterministic regex gate — high-signal credential patterns only (no PII/IP
heuristics, which are noisy). Exit code: 0 = clean, 3 = secrets found,
2 = usage error. Ops run this before finalizing any raw/inbox write and, on
a hit, ask the user to mask or abort (see PRINCIPLES.md secret-scan).
"""
import json
import re
import sys

# (kind, compiled regex). Ordered most-specific → generic.
PATTERNS = [
    ("private_key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |PGP |DSA )?PRIVATE KEY-----")),
    ("anthropic_key", re.compile(r"sk-ant-[A-Za-z0-9\-_]{20,}")),
    ("openai_key", re.compile(r"sk-(?:proj-)?[A-Za-z0-9]{20,}")),
    ("github_token", re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}")),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("google_api_key", re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b")),
    ("slack_token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}")),
    ("bearer_token", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9_\-\.]{20,}")),
    # keyword may sit inside a compound identifier (DATABASE_PASSWORD, MY_API_KEY),
    # so allow identifier chars on both sides — `_` is a word char, so \b fails here.
    ("assigned_secret", re.compile(
        r"(?i)[A-Za-z0-9_.\-]*"
        r"(?:passwd|password|secret|api[_-]?key|apikey|access[_-]?token|"
        r"auth[_-]?token|client[_-]?secret|credential|token|pwd)"
        r"[A-Za-z0-9_.\-]*\s*[:=]\s*['\"]?[A-Za-z0-9/+_.\-]{8,}")),
]


def mask(s: str) -> str:
    s = s.strip()
    if len(s) <= 8:
        return s[:2] + "***"
    return s[:4] + "***" + s[-2:]


def scan(text: str):
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        for kind, rx in PATTERNS:
            m = rx.search(line)
            if m:
                hits.append({"line": i, "kind": kind, "preview": mask(m.group(0))})
                break  # one hit per line is enough to flag it
    return hits


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    json_out = "--json" in sys.argv[1:]
    if not args:
        print("usage: secret_scan.py <file|-> [--json]", file=sys.stderr)
        return 2

    src = args[0]
    text = sys.stdin.read() if src == "-" else open(src, encoding="utf-8", errors="replace").read()
    hits = scan(text)

    if json_out:
        print(json.dumps({"hits": hits, "count": len(hits)}, ensure_ascii=False, indent=2))
    elif not hits:
        print("clean — no secrets detected")
    else:
        print(f"⚠️  {len(hits)} likely secret(s):")
        for h in hits:
            print(f"  L{h['line']} [{h['kind']}] {h['preview']}")
    return 3 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
