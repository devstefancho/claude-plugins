# Claude Code Plugins Marketplace

A collection of reusable [Claude Code](https://claude.ai/code) plugins — slash commands, agent skills, subagents, hooks, and MCP server integrations.

## Quick Start

```bash
# 1. Add this marketplace
/plugin marketplace add devstefancho/claude-plugins

# 2. Install a plugin
/plugin install <plugin-name>@devstefancho-claude-plugins

# 3. Restart Claude Code to activate
```

## Available Plugins

### Code Quality

| Plugin | Description |
|--------|-------------|
| [code-style-plugin](./code-style-plugin) | Code review based on SRP, DRY, Simplicity First, YAGNI, and Type Safety |
| [code-quality-plugin](./code-quality-plugin) | Code quality review focusing on DRY, KISS, and Clean Code principles |
| [frontend-plugin](./frontend-plugin) | React/Next.js component design review |

### Spec-Driven Development

| Plugin | Description |
|--------|-------------|
| [writing-specs-plugin](./writing-specs-plugin) | Spec writing with conflict detection and reporting |
| [simple-sdd-plugin](./simple-sdd-plugin) | SDD workflow: spec → plan → tasks → implement |
| [implement-with-test-plugin](./implement-with-test-plugin) | Implement code with tests from specs or direct requests |
| [brain-storm-plugin](./brain-storm-plugin) | Brainstorm features and improvements with wireframes |

### Git & Workflow

| Plugin | Description |
|--------|-------------|
| [git-worktree-plugin](./git-worktree-plugin) | Manage git worktrees for parallel branch work |
| [git-commit-plugin](./git-commit-plugin) | Auto-generate conventional commit messages |
| [smart-commit-plugin](./smart-commit-plugin) | Split uncommitted changes into logical commits |
| [pr-create-plugin](./pr-create-plugin) | Create GitHub PRs with auto-generated descriptions |
| [test-commit-push-pr-clean-plugin](./test-commit-push-pr-clean-plugin) | Automate lint, test, commit, push, PR, and worktree cleanup |

### Testing & Reporting

| Plugin | Description |
|--------|-------------|
| [computer-use-plugin](./computer-use-plugin) | App testing via Computer Use MCP with feedback reports |
| [session-reporter-plugin](./session-reporter-plugin) | Generate HTML reports for work sessions |
| [worktrace-plugin](./worktrace-plugin) | Extract work history and generate daily summaries |

### Agent & Automation

| Plugin | Description |
|--------|-------------|
| [agent-team-plugin](./agent-team-plugin) | Create and manage agent teams for worktree sessions |
| [hermes-gateway-plugin](./hermes-gateway-plugin) | Interact with Hermes Agent via local or SSH connection |
| [stop-notification-plugin](./stop-notification-plugin) | macOS TTS notification when Claude stops or needs attention |

### Tooling

| Plugin | Description |
|--------|-------------|
| [scaffold-claude-feature](./scaffold-claude-feature) | Generate Claude Code features with proper structure |
| [common-mcp-plugin](./common-mcp-plugin) | Common MCP servers for shared tools and integrations |
| [local-test-plugin](./local-test-plugin) | Symlink-based local plugin testing |

### Deprecated

| Plugin | Description |
|--------|-------------|
| [spec-manager-plugin](./spec-manager-plugin) | Replaced by `writing-specs-plugin` |

## Plugin Structure

Each plugin follows this layout:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json         # Plugin metadata (required)
├── commands/               # Slash commands
├── skills/                 # Agent skills
├── agents/                 # Subagents
├── hooks/                  # Event handlers
├── .mcp.json               # MCP servers
└── README.md
```

## Local Development

```bash
# Clone and add as local marketplace
git clone https://github.com/devstefancho/claude-plugins.git
cd claude-plugins
claude

# Inside Claude Code
/plugin marketplace add .
/plugin install <plugin-name>@devstefancho-claude-plugins
```

## License

MIT
