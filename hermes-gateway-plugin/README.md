# Hermes Gateway Plugin

Interact with Hermes Agent via local or SSH-tunneled connection. Provides commands for messaging, async task execution, health checks, and cron job management.

https://github.com/user-attachments/assets/aeecb2de-813f-484a-9de6-d266316f0fcd

## Installation

```bash
/plugin marketplace add .
/plugin install hermes-gateway-plugin@devstefancho-claude-plugins
```

## Commands

| Command | Description |
|---------|-------------|
| `/hermes:setup` | Check connectivity and configure connection mode |
| `/hermes:chat` | Send a message to Hermes Agent |
| `/hermes:run` | Start an async task with event streaming |
| `/hermes:status` | Check connection health, tunnel status, and recent jobs |
| `/hermes:jobs` | Manage cron jobs (list, create, delete) |

## Connection Modes

- **auto** (default) - Tries localhost first, falls back to SSH tunnel
- **local** - Direct connection to `localhost:8642`
- **ssh** - SSH tunnel to remote Hermes server

## Configuration

Config file: `~/.claude/hermes/config.json`

Supported flags for `/hermes:setup`:
- `--mode` - Connection mode (auto, local, ssh)
- `--remote-host` - SSH remote host
- `--remote-port` - Remote port
- `--local-port` - Local port
- `--api-key` - API key

## Usage Examples

```
/hermes:setup --mode ssh --remote-host arch-server
/hermes:chat What's the current system load?
/hermes:run --background Analyze disk usage and report
/hermes:jobs
```
