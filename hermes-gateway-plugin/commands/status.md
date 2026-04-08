---
description: Hermes 연결 상태, tunnel 상태, 최근 작업 목록을 확인한다
argument-hint: "[job-id] [--json]"
allowed-tools: Bash(node:*)
---

Check Hermes connection health, tunnel status, and recent job history.

Execute:
```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/hermes-companion.mjs" status $ARGUMENTS
```

Return the output verbatim.
