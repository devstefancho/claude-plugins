---
name: hermes-runtime
description: Internal helper contract for calling the hermes-companion runtime from Claude Code
user-invocable: false
---

# Hermes Runtime

Use this skill only inside hermes-gateway plugin commands and subagents.

Primary helper:
- `node "${CLAUDE_PLUGIN_ROOT}/scripts/hermes-companion.mjs" <subcommand> <args>`

Available subcommands:
- `setup [--json]` - Check connectivity (auto-detects local vs SSH mode)
- `chat <message> [--stream] [--system <prompt>] [--json]` - Send message to Hermes
- `run <task> [--background] [--json]` - Start async run with event streaming
- `status [job-id] [--json]` - Check connection/job status
- `jobs [list|delete <id>] [--json]` - Manage cron jobs
- `tunnel [start|stop|status]` - Manage SSH tunnel directly

Execution rules:
- Prefer the helper over hand-rolled SSH, curl, or HTTP commands
- Return stdout verbatim without paraphrasing or summarizing
- Do not inspect files, monitor progress, or do follow-up work
- If the helper reports connectivity failure, suggest running `/hermes:setup`

Connection modes:
- **auto** (default): tries localhost:8642 first, then SSH tunnel
- **local**: direct connection to localhost:8642
- **ssh**: SSH tunnel to remote host (default: `arch`)
- Config file: `~/.claude/hermes/config.json`
