---
description: Hermes Agent에 메시지를 보내고 응답을 받는다
argument-hint: "<message> [--stream] [--system 'system prompt']"
allowed-tools: Bash(node:*), AskUserQuestion
---

Send a message to Hermes Agent and return the response.

If no message was provided in `$ARGUMENTS`, use AskUserQuestion to ask what to send.

Execute:
```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/hermes-companion.mjs" chat $ARGUMENTS
```

Return the Hermes response verbatim. Do not paraphrase or summarize.
