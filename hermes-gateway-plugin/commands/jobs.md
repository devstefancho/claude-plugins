---
description: Hermes cron job 목록 조회, 생성, 삭제
argument-hint: "[list|delete <id>] [--json]"
allowed-tools: Bash(node:*), AskUserQuestion
---

Manage Hermes cron jobs (scheduled automation tasks).

Execute:
```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/hermes-companion.mjs" jobs $ARGUMENTS
```

Return the output verbatim.
