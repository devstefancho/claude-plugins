# Getting Started

Welcome to the Claude Plugins marketplace!

## What are Claude Plugins?

Claude Plugins are reusable components that extend Claude Code CLI:

- **Skills**: Specialized knowledge and behaviors automatically activated by Claude Code
- **Commands**: Custom slash commands starting with `/`
- **Hooks**: Automation scripts that respond to specific events
- **MCP Servers**: Integration with external tools

## Prerequisites

- Claude Code CLI must be installed
- Git access is required

## Quick Start

### 1. Register Marketplace

```bash
/plugin marketplace add devstefancho/claude-plugins
```

### 2. Install Plugins

```bash
# Example: Code style review plugin
/plugin install code-style-plugin@devstefancho-claude-plugins

# Example: Git commit automation plugin
/plugin install git-commit-plugin@devstefancho-claude-plugins
```

### 3. Restart Claude Code

After installing plugins, restart Claude Code to apply changes.

```bash
# Close and reopen terminal, or
# Start a new Claude Code session
claude
```

### 4. Verify Installation

```bash
/plugin
# Check installed plugins list
```

## Alternative: npx skills

You can also install skills using the `npx skills` CLI from any terminal:

```bash
# List available skills
npx skills add devstefancho/claude-plugins --list

# Install all skills
npx skills add devstefancho/claude-plugins

# Install a specific skill
npx skills add devstefancho/claude-plugins --skill code-style-reviewer
```

> Note: `npx skills` installs Agent Skills only. For commands, hooks, and MCP servers, use the `/plugin` method above.

## Next Steps

- [Installation Guide](/guide/installation) - Detailed installation instructions
- [Plugin List](/plugins/) - Browse all available plugins
