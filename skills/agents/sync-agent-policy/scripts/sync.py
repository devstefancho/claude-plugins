#!/usr/bin/env python3
"""Project a local policy file onto Claude Code, Grok, and Cursor Agent configs."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

PROG = "sync-agent-policy"
POLICY_REL = Path("agent-policy") / "policy.toml"
HOOK_NAME = "deny_read_hook.py"
AGENTS = ("claude", "grok", "cursor")


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def home() -> Path:
    return Path(os.environ.get("HOME", "")).expanduser()


def config_root() -> Path:
    xdg = os.environ.get("XDG_CONFIG_HOME")
    return Path(xdg) if xdg else home() / ".config"


def default_policy_path() -> Path:
    override = os.environ.get("AGENT_POLICY_FILE")
    return Path(override).expanduser() if override else config_root() / POLICY_REL


def skill_dir() -> Path:
    return Path(__file__).resolve().parent.parent


def fmt_array(values: list[str]) -> str:
    if not values:
        return "[]"
    inner = ",\n".join(f'  "{v}"' for v in values)
    return "[\n" + inner + ",\n]"


def parse_quoted_strings(blob: str) -> list[str]:
    return re.findall(r'"((?:\\.|[^"\\])*)"', blob)


def find_matching_bracket(text: str, start: int) -> int:
    depth = 0
    in_str = False
    esc = False
    for i, ch in enumerate(text[start:], start):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return i
    raise ValueError("unbalanced [")


def upsert_toml_string_array(text: str, table: str, key: str, add: list[str]) -> str:
    """Union `add` into [table] key = […] without dropping existing values."""
    if not add:
        return text
    table_re = re.compile(rf"^\[{re.escape(table)}\]\s*$", re.M)
    m = table_re.search(text)
    if not m:
        block = f"[{table}]\n{key} = {fmt_array(add)}\n"
        if text and not text.endswith("\n"):
            text += "\n"
        sep = "" if text.endswith("\n\n") or text == "" else "\n"
        return text + sep + block

    rest = text[m.end() :]
    nxt = re.search(r"^\[", rest, re.M)
    section = rest if not nxt else rest[: nxt.start()]
    after = "" if not nxt else rest[nxt.start() :]
    before = text[: m.end()]

    key_re = re.compile(rf"^{re.escape(key)}\s*=\s*\[", re.M)
    km = key_re.search(section)
    if not km:
        insert = f"\n{key} = {fmt_array(add)}\n"
        return before + insert + section + after

    arr_start = section.find("[", km.start())
    arr_end = find_matching_bracket(section, arr_start)
    existing = parse_quoted_strings(section[arr_start : arr_end + 1])
    merged = list(dict.fromkeys(existing + add))
    new_section = section[:arr_start] + fmt_array(merged) + section[arr_end + 1 :]
    return before + new_section + after


@dataclass
class Policy:
    path: Path
    deny_reads: list[str] = field(default_factory=list)
    deny_writes: list[str] = field(default_factory=list)
    deny_commands: list[str] = field(default_factory=list)
    guidelines: list[str] = field(default_factory=list)
    agents: dict[str, bool] = field(default_factory=lambda: {a: True for a in AGENTS})

    def enabled(self, name: str) -> bool:
        return bool(self.agents.get(name, True))


def load_policy(path: Path) -> Policy:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    agents = {a: True for a in AGENTS}
    raw = data.get("agents") or {}
    for a in AGENTS:
        if a in raw:
            agents[a] = bool(raw[a])
    return Policy(
        path=path,
        deny_reads=list(data.get("deny_reads") or []),
        deny_writes=list(data.get("deny_writes") or []),
        deny_commands=list(data.get("deny_commands") or []),
        guidelines=list(data.get("guidelines") or []),
        agents=agents,
    )


def resolve_path(p: str, base: Path) -> Path:
    if p.startswith("~/") or p == "~":
        return Path(p).expanduser()
    path = Path(p)
    return path if path.is_absolute() else (base / path)


def claude_path_token(pattern: str) -> str:
    if pattern.startswith("~/") or pattern == "~" or not pattern.startswith(("/", "*")):
        return pattern
    if pattern.startswith("**"):
        return "//" + pattern
    return "//" + pattern.lstrip("/")


def grok_path_token(pattern: str, h: Path) -> str:
    if pattern.startswith("~/"):
        return str(h / pattern[2:])
    if pattern == "~":
        return str(h)
    return pattern


def cursor_path_token(pattern: str, h: Path) -> str:
    return grok_path_token(pattern, h)


def first_token(command: str) -> str:
    return command.strip().split()[0] if command.strip() else command


def tokens_for(agent: str, policy: Policy, h: Path) -> list[str]:
    out: list[str] = []
    if agent == "claude":
        for p in policy.deny_reads:
            out.append(f"Read({claude_path_token(p)})")
        for p in policy.deny_writes:
            inner = claude_path_token(p)
            out.append(f"Edit({inner})")
            out.append(f"Write({inner})")
        for c in policy.deny_commands:
            out.append(f"Bash({c})")
    elif agent == "grok":
        for p in policy.deny_reads:
            out.append(f"Read({grok_path_token(p, h)})")
        for p in policy.deny_writes:
            out.append(f"Edit({grok_path_token(p, h)})")
        for c in policy.deny_commands:
            out.append(f"Bash({c})")
    elif agent == "cursor":
        for p in policy.deny_reads:
            out.append(f"Read({cursor_path_token(p, h)})")
        for p in policy.deny_writes:
            out.append(f"Write({cursor_path_token(p, h)})")
        for c in policy.deny_commands:
            out.append(f"Shell({first_token(c)})")
    return list(dict.fromkeys(out))


def which(name: str) -> bool:
    return shutil.which(name) is not None


def installed(agent: str, h: Path) -> bool:
    if agent == "claude":
        return (h / ".claude" / "settings.json").exists() or which("claude")
    if agent == "grok":
        return (h / ".grok" / "config.toml").exists() or which("grok")
    if agent == "cursor":
        return (h / ".cursor").is_dir() or which("cursor-agent") or which("cursor")
    return False


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def current_denies(agent: str, h: Path) -> list[str]:
    if agent == "claude":
        data = read_json(h / ".claude" / "settings.json")
        return list((data.get("permissions") or {}).get("deny") or [])
    if agent == "cursor":
        data = read_json(h / ".cursor" / "cli-config.json")
        return list((data.get("permissions") or {}).get("deny") or [])
    if agent == "grok":
        path = h / ".grok" / "config.toml"
        if not path.exists():
            return []
        perm = (tomllib.loads(path.read_text(encoding="utf-8"))).get("permission") or {}
        return list(perm.get("deny") or [])
    return []


def merge_json_denies(path: Path, add: list[str]) -> None:
    data = read_json(path)
    perms = data.setdefault("permissions", {})
    deny = list(perms.get("deny") or [])
    perms["deny"] = list(dict.fromkeys(deny + add))
    if "allow" not in perms:
        perms["allow"] = list(perms.get("allow") or [])
    write_json(path, data)


def apply_permissions(agent: str, add: list[str], h: Path) -> Path:
    if agent == "claude":
        path = h / ".claude" / "settings.json"
        merge_json_denies(path, add)
        return path
    if agent == "cursor":
        path = h / ".cursor" / "cli-config.json"
        merge_json_denies(path, add)
        return path
    path = h / ".grok" / "config.toml"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(upsert_toml_string_array(text, "permission", "deny", add), encoding="utf-8")
    return path


def guideline_targets(src: Path, h: Path) -> dict[str, Path]:
    name = src.name
    stem = src.stem
    return {
        "claude": h / ".claude" / "rules" / name,
        "grok": h / ".grok" / "rules" / name,
        "cursor": h / ".cursor" / "rules" / f"{stem}.mdc",
    }


def write_cursor_mdc(dest: Path, src: Path) -> None:
    body = src.read_text(encoding="utf-8")
    if body.startswith("---"):
        content = body
    else:
        desc = stem_description(src)
        content = f"---\ndescription: {desc}\nalwaysApply: true\n---\n\n{body}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")


def stem_description(src: Path) -> str:
    for line in src.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return src.stem.replace("-", " ")


def apply_guideline(agent: str, src: Path, dest: Path) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        if dest.resolve() == src.resolve():
            return "same"
    except OSError:
        pass
    if dest.is_symlink():
        dest.unlink()
        dest.symlink_to(src)
        return "relinked"
    if dest.exists():
        return "skipped-exists"
    if agent == "cursor":
        write_cursor_mdc(dest, src)
        return "wrote"
    dest.symlink_to(src)
    return "linked"


def guideline_status(agent: str, src: Path, dest: Path) -> str:
    if not dest.exists() and not dest.is_symlink():
        return "missing"
    try:
        if dest.resolve() == src.resolve():
            return "ok"
    except OSError:
        return "broken"
    if dest.is_symlink():
        return "different"
    return "exists"


def hook_script_src() -> Path:
    return Path(__file__).resolve().parent / HOOK_NAME


def hook_script_dst(policy: Policy) -> Path:
    return policy.path.parent / HOOK_NAME


def install_hooks(policy: Policy, agents: list[str], h: Path) -> list[str]:
    src = hook_script_src()
    dst = hook_script_dst(policy)
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    dst.chmod(0o755)
    cmd = f"{sys.executable} {dst}"
    notes = [f"hook script → {dst}"]
    if "claude" in agents:
        path = h / ".claude" / "settings.json"
        data = read_json(path)
        hooks = data.setdefault("hooks", {})
        groups = hooks.setdefault("PreToolUse", [])
        if not any(HOOK_NAME in json.dumps(g) for g in groups):
            groups.append(
                {
                    "matcher": "Read|Bash|Edit|Write",
                    "hooks": [{"type": "command", "command": cmd, "timeout": 5}],
                }
            )
            write_json(path, data)
            notes.append(f"claude PreToolUse → {path}")
        else:
            notes.append("claude hook already registered")
    if "grok" in agents:
        path = h / ".grok" / "hooks" / "agent-policy.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "hooks": {
                        "PreToolUse": [
                            {
                                "matcher": "Read|Bash|Edit|Write",
                                "hooks": [{"type": "command", "command": cmd, "timeout": 5}],
                            }
                        ]
                    }
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        notes.append(f"grok hook → {path}")
    if "cursor" in agents:
        path = h / ".cursor" / "hooks.json"
        data = read_json(path)
        if not data.get("version"):
            data["version"] = 1
        hooks = data.setdefault("hooks", {})
        arr = hooks.setdefault("beforeReadFile", [])
        if not any(HOOK_NAME in json.dumps(x) for x in arr):
            arr.append({"command": cmd, "failClosed": True, "timeout": 5})
            write_json(path, data)
            notes.append(f"cursor beforeReadFile → {path}")
        else:
            notes.append("cursor hook already registered")
    return notes


def unwrap_claude_inner(inner: str) -> str:
    if inner.startswith("//"):
        rest = inner[2:]
        return rest if rest.startswith("**") else "/" + rest.lstrip("/")
    return inner


def seed_from_claude(h: Path) -> dict[str, list[str]]:
    deny = current_denies("claude", h)
    reads, writes, commands = [], [], []
    for tok in deny:
        m = re.match(r"(Read|Edit|Write|Bash)\((.*)\)\s*$", tok)
        if not m:
            continue
        kind, inner = m.group(1), m.group(2)
        if kind == "Read":
            reads.append(unwrap_claude_inner(inner))
        elif kind in ("Edit", "Write"):
            writes.append(unwrap_claude_inner(inner))
        else:
            commands.append(inner)
    rules_dir = h / ".claude" / "rules"
    guidelines: list[str] = []
    if rules_dir.is_dir():
        guidelines = [f"~/.claude/rules/{p.name}" for p in sorted(rules_dir.glob("*.md"))]
    return {
        "deny_reads": list(dict.fromkeys(reads)),
        "deny_writes": list(dict.fromkeys(writes)),
        "deny_commands": list(dict.fromkeys(commands)),
        "guidelines": guidelines,
    }


def render_policy_toml(
    reads: list[str], writes: list[str], commands: list[str], guidelines: list[str]
) -> str:
    return (
        "# Local source of truth for cross-agent permissions.\n"
        "# Paths: ~ is $HOME. ** matches across directories.\n\n"
        "version = 1\n\n"
        f"deny_reads = {fmt_array(reads)}\n\n"
        f"deny_writes = {fmt_array(writes)}\n\n"
        f"deny_commands = {fmt_array(commands)}\n\n"
        f"guidelines = {fmt_array(guidelines)}\n\n"
        "[agents]\nclaude = true\ngrok = true\ncursor = true\n"
    )


def cmd_init(args: argparse.Namespace) -> int:
    dest = Path(args.policy)
    if dest.exists() and not args.force:
        eprint(f"already exists: {dest} (pass --force to overwrite)")
        return 1
    dest.parent.mkdir(parents=True, exist_ok=True)
    rules_dest = dest.parent / "rules"
    rules_dest.mkdir(parents=True, exist_ok=True)
    tmpl = skill_dir() / "templates"
    src_rule = tmpl / "rules" / "secrets.md"
    if src_rule.exists() and (args.force or not (rules_dest / "secrets.md").exists()):
        shutil.copy2(src_rule, rules_dest / "secrets.md")

    if args.from_claude:
        seeded = seed_from_claude(home())
        fallback = tomllib.loads((tmpl / "policy.toml").read_text(encoding="utf-8"))
        reads = seeded["deny_reads"] or list(fallback.get("deny_reads") or [])
        writes = seeded["deny_writes"]
        commands = seeded["deny_commands"]
        guidelines = seeded["guidelines"] or ["rules/secrets.md"]
        dest.write_text(
            render_policy_toml(reads, writes, commands, guidelines),
            encoding="utf-8",
        )
    else:
        shutil.copy2(tmpl / "policy.toml", dest)
    print(dest)
    return 0


def selected_agents(policy: Policy, only: str | None) -> list[str]:
    wanted = [a.strip() for a in only.split(",")] if only else list(AGENTS)
    bad = [a for a in wanted if a not in AGENTS]
    if bad:
        raise SystemExit(f"unknown agent: {', '.join(bad)}")
    return [a for a in wanted if policy.enabled(a)]


def collect_status(policy: Policy, agents: list[str], h: Path) -> list[dict]:
    rows = []
    for agent in agents:
        expected = tokens_for(agent, policy, h)
        present = installed(agent, h)
        have = current_denies(agent, h) if present else []
        missing = [t for t in expected if t not in have]
        extra_note = ""
        if agent == "cursor":
            coarse = [
                c
                for c in policy.deny_commands
                if c.strip() and first_token(c) != c.strip()
            ]
            if coarse:
                extra_note = "Shell(first-token) coarsens: " + ", ".join(coarse)
        g_missing = []
        for g in policy.guidelines:
            src = resolve_path(g, policy.path.parent)
            dest = guideline_targets(src, h)[agent]
            st = guideline_status(agent, src, dest) if present else "n/a"
            if st not in ("ok", "exists"):
                g_missing.append(f"{src.name}:{st}")
        rows.append(
            {
                "agent": agent,
                "installed": present,
                "missing": missing,
                "guidelines": g_missing,
                "note": extra_note,
                "have": have,
                "expected": expected,
            }
        )
    return rows


def print_status(rows: list[dict]) -> None:
    print(f"{'agent':<8} {'state':<14} missing")
    print("-" * 72)
    for row in rows:
        if not row["installed"]:
            print(f"{row['agent']:<8} {'not installed':<14} —")
            continue
        n = len(row["missing"])
        g = f" guidelines={','.join(row['guidelines'])}" if row["guidelines"] else ""
        state = "ok" if n == 0 and not row["guidelines"] else f"{n} missing"
        preview = ", ".join(row["missing"][:3])
        if n > 3:
            preview += f" … +{n - 3}"
        print(f"{row['agent']:<8} {state:<14} {preview or '—'}{g}")
        if row["note"]:
            print(f"{'':8} note: {row['note']}")


def cmd_status(args: argparse.Namespace) -> int:
    path = Path(args.policy)
    if not path.exists():
        eprint(f"no policy at {path} — run `{PROG} init` first")
        return 1
    policy = load_policy(path)
    rows = collect_status(policy, selected_agents(policy, args.agent), home())
    print_status(rows)
    return 0 if all((not r["installed"]) or (not r["missing"] and not r["guidelines"]) for r in rows) else 1


def cmd_map(args: argparse.Namespace) -> int:
    path = Path(args.policy)
    if not path.exists():
        eprint(f"no policy at {path} — run `{PROG} init` first")
        return 1
    policy = load_policy(path)
    h = home()
    for agent in selected_agents(policy, args.agent):
        print(f"# {agent}")
        for tok in tokens_for(agent, policy, h):
            print(tok)
        print()
    return 0


def cmd_apply(args: argparse.Namespace) -> int:
    path = Path(args.policy)
    if not path.exists():
        eprint(f"no policy at {path} — run `{PROG} init` first")
        return 1
    policy = load_policy(path)
    h = home()
    agents = selected_agents(policy, args.agent)
    rows = collect_status(policy, agents, h)
    print_status(rows)
    todo = [r for r in rows if r["installed"] and (r["missing"] or r["guidelines"] or args.hooks)]
    if not todo and not args.hooks:
        print("nothing to apply")
        return 0
    if not args.write:
        eprint("dry-run (pass --write to apply)")
        return 0
    for row in rows:
        if not row["installed"]:
            continue
        agent = row["agent"]
        if row["missing"]:
            dest = apply_permissions(agent, row["missing"], h)
            print(f"wrote permissions {agent}: {dest} (+{len(row['missing'])})")
        for g in policy.guidelines:
            src = resolve_path(g, policy.path.parent)
            if not src.exists():
                eprint(f"guideline missing: {src}")
                continue
            dest = guideline_targets(src, h)[agent]
            if guideline_status(agent, src, dest) != "ok":
                how = apply_guideline(agent, src, dest)
                print(f"guideline {agent}: {dest} ({how})")
    if args.hooks:
        present = [r["agent"] for r in rows if r["installed"]]
        for note in install_hooks(policy, present, h):
            print(note)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog=PROG, description=__doc__)
    p.add_argument("--policy", default=str(default_policy_path()), help="policy.toml path")
    sub = p.add_subparsers(dest="cmd", required=True)

    st = sub.add_parser("status", help="diff policy against installed agents")
    st.add_argument("--agent", help="comma list: claude,grok,cursor")
    st.set_defaults(func=cmd_status)

    mp = sub.add_parser("map", help="print rendered deny tokens")
    mp.add_argument("--agent", help="comma list: claude,grok,cursor")
    mp.set_defaults(func=cmd_map)

    ini = sub.add_parser("init", help="write ~/.config/agent-policy/policy.toml")
    ini.add_argument("--force", action="store_true")
    ini.add_argument("--from-claude", action="store_true", help="seed deny lists from Claude settings")
    ini.set_defaults(func=cmd_init)

    ap = sub.add_parser("apply", help="merge missing deny tokens (default: dry-run)")
    ap.add_argument("--agent", help="comma list: claude,grok,cursor")
    ap.add_argument("--write", action="store_true", help="actually write files")
    ap.add_argument("--hooks", action="store_true", help="also install the read-deny hook")
    ap.set_defaults(func=cmd_apply)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except (OSError, ValueError, tomllib.TOMLDecodeError, json.JSONDecodeError) as exc:
        eprint(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
