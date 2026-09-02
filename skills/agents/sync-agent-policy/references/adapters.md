# Adapters

Policy paths stay portable (`~/…`, `**/.env`). Each harness gets the token shape it actually matches.

## Files

| Agent | Permissions | Guidelines | Hooks (optional `--hooks`) |
| --- | --- | --- | --- |
| Claude Code | `~/.claude/settings.json` → `permissions.deny` | `~/.claude/rules/*.md` | `hooks.PreToolUse` |
| Grok | `~/.grok/config.toml` → `[permission] deny` | `~/.grok/rules/*.md` | `~/.grok/hooks/agent-policy.json` |
| Cursor Agent | `~/.cursor/cli-config.json` → `permissions.deny` | `~/.cursor/rules/*.mdc` | `~/.cursor/hooks.json` `beforeReadFile` |

Grok also *reads* Claude `settings.json` when `compat.claude` is on (default). Still write Grok native tokens: Grok treats `~/` and `//` in a pattern as literal glob text, so Claude's `Read(~/.secrets/**)` / `Read(//**/.env)` can miss.

## Token mapping

| Policy | Claude | Grok | Cursor |
| --- | --- | --- | --- |
| `~/.secrets/**` (read) | `Read(~/.secrets/**)` | `Read($HOME/.secrets/**)` | `Read($HOME/.secrets/**)` |
| `**/.env` (read) | `Read(//**/.env)` | `Read(**/.env)` | `Read(**/.env)` |
| `/abs/path` (read) | `Read(//abs/path)` | `Read(/abs/path)` | `Read(/abs/path)` |
| write | `Edit(…)` and `Write(…)` | `Edit(…)` | `Write(…)` |
| `rm -rf *` | `Bash(rm -rf *)` | `Bash(rm -rf *)` | `Shell(rm)` (first token) |

Cursor `Shell(cmd)` matches the first token. A deny of `git push --force *` becomes `Shell(git)` — broader than Claude/Grok. That is expected.

## Merge rules

- Union into `deny` / `[permission] deny`. Never delete extra entries the user already has.
- Do not touch `allow`, `ask`, MCP servers, `permission_mode`, or always-approve.
- Grok: if `[permission]` is missing, append a compact `deny` table. Existing `rules = [{action=…}]` rows are left alone.

## Guidelines

Sources listed in `guidelines` (relative to the policy file, or `~/…`):

- Claude: symlink `~/.claude/rules/<name>.md` → source when missing
- Grok: symlink `~/.grok/rules/<name>.md` → source when missing
- Cursor: write `~/.cursor/rules/<stem>.mdc` with `alwaysApply: true` when missing

An existing regular file is left in place (`skipped-exists`). Only our own dangling/wrong symlink is retargeted.

## Hooks

`apply --hooks` copies `deny_read_hook.py` next to the policy file and registers it. The hook blocks matching **file reads**; it is fail-open on Grok, so set Cursor `failClosed: true`. Permission tokens remain the primary gate. Hooks do not replace a sandbox.

## Not in v1

Codex, Windsurf, project-local `.claude/settings.local.json`, Grok `sandbox.toml`, allow-lists, MCP, notification hooks, Orca/Herdr hooks.
