---
description: Run an async task on Hermes Agent and stream events
argument-hint: "<task> [--background]"
allowed-tools: Bash(node:*), AskUserQuestion
---

Start an async run on Hermes Agent with event streaming.

If no task was provided in `$ARGUMENTS`, use AskUserQuestion to ask what task to run.

Execute:
```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/hermes-companion.mjs" run $ARGUMENTS
```

- Without `--background`: stream events until completion and return output verbatim
- With `--background`: return the job ID immediately so the user can check status later

Return the output verbatim. Do not paraphrase or summarize.
