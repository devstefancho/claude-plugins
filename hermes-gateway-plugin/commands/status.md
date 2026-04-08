---
description: Check Hermes connection status, tunnel status, and recent jobs
argument-hint: "[job-id] [--json]"
allowed-tools: Bash(node:*)
---

Check Hermes connection health, tunnel status, and recent job history.

Execute:
```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/hermes-companion.mjs" status $ARGUMENTS
```

Return the output verbatim.
