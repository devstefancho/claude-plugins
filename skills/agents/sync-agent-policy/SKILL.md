---
name: sync-agent-policy
description: "Projects one local policy file onto Claude Code, Grok, and Cursor Agent — deny rules, guideline files, and an optional read-deny hook. Use when the user says 에이전트 권한 맞춰, 권한 동기화, grok이랑 cursor 권한, 같은 보안 설정, deny 규칙 맞춰줘, agent policy sync, sync permissions across agents, 에이전트 설정 통일."
---

# Sync Agent Policy

One local policy file is the source of truth. This skill maps it onto each harness — it does not copy one agent's config onto another.

## Hard Rules

- **Policy file is SSOT.** User paths live in `~/.config/agent-policy/policy.toml`, never in this skill. Why: the skill is public; the deny list is personal.
- **Status first; write only on explicit apply.** `apply` is dry-run unless `--write`. Why: these files also hold allow-lists and unrelated hooks.
- **Merge deny, keep everything else.** Union missing tokens into `deny`. Do not replace `allow`, `ask`, MCP, or `permission_mode`.
- **Emit native tokens.** `~/` and `//` are not portable. Mapping is in [references/adapters.md](references/adapters.md).
- **Do not replace an existing regular guideline file.** Only create missing files or retarget our own symlinks.

## Dispatch

| User says | Run |
| --- | --- |
| 맞춰 / 동기화 / 체크 / status | `status` |
| 처음 / init / policy 만들어 | `init` (add `--from-claude` if Claude already has denys) |
| 적용 / apply / 써줘 | `status` → show the table → `apply --write` after they confirm |
| 훅도 | `apply --write --hooks` |
| 토큰이 어떻게 되나 | `map` |

```bash
SCRIPT="$HOME/.claude/skills/sync-agent-policy/scripts/sync.py"
# fallback: $HOME/.agents/skills/sync-agent-policy/scripts/sync.py
python3 "$SCRIPT" status
```

`-h` documents `init`, `status`, `map`, `apply`.

## Phases

1. **Policy**
   - [ ] `~/.config/agent-policy/policy.toml` exists; else `init` (or `init --from-claude`)
   - [ ] Edit the file with the user if the starter deny list is wrong. `guidelines` lists markdown to project.

2. **Diff**
   - [ ] `status` (exit 1 = gaps). Show the table as-is.
   - [ ] `map` only when they ask how a path is spelled per agent.

3. **Apply** (only if they asked to apply, after they saw the table)
   - [ ] `apply --write` (add `--hooks` only when asked)
   - [ ] `status` again — remaining gaps are the report

Installed-but-disabled agents (`[agents] grok = false`) are skipped. Not-installed agents are reported, not created from scratch except for the specific config file `apply` must write.

## Anti-patterns

- **WRONG**: copy `~/.claude/settings.json` into Grok or Cursor. **RIGHT**: render tokens per [adapters.md](references/adapters.md).
- **WRONG**: overwrite `permissions` / `[permission]`. **RIGHT**: union `deny` only.

## Boundaries

Occasional check/apply, not a daemon. Codex and Windsurf are out of v1. Allow-lists, MCP, always-approve, sandbox.toml, and Orca/Herdr hooks stay untouched.
