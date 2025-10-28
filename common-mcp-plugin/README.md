# Common MCP Plugin

A plugin providing commonly-used MCP servers for Claude Code integration with external tools and services.

## Overview

This plugin provides centralized management of shared MCP (Model Context Protocol) servers that can be reused across multiple projects and plugins. It enables teams to maintain consistent tool integrations without duplicating server configurations.

## Installation

```bash
/plugin install common-mcp-plugin@devstefancho-claude-plugins
```

## Included MCP Servers

### Chrome DevTools
Provides integration with Chrome DevTools for browser automation and inspection.

**Configuration:**
```json
{
  "command": "npx",
  "args": ["chrome-devtools-mcp@latest"]
}
```

**Usage:**
The chrome-devtools MCP server is automatically available when this plugin is installed. You can use it for:
- Browser automation
- Page inspection
- Network debugging
- Performance analysis

## Using MCP Servers from Plugins

### Adding to Your Project

When you install this plugin, the included MCP servers are configured in your Claude Code environment. They are available automatically for Claude to use during code sessions.

### Extending the Plugin

To add more MCP servers to this plugin:

1. Edit `.mcp.json` in the plugin root
2. Add new server definitions to the `mcpServers` object:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest"]
    },
    "your-new-server": {
      "command": "npx",
      "args": ["your-server-mcp@latest"]
    }
  }
}
```

### Plugin Isolation

Each plugin manages its own `.mcp.json` configuration, allowing for:
- **Isolated dependencies**: Each plugin's MCP servers are independent
- **Clean removal**: Uninstalling the plugin removes all its MCP server configurations
- **Team coordination**: Share common server setups through the marketplace

## Plugin Structure

```
common-mcp-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── .mcp.json                # MCP server definitions
└── README.md                # This file
```

## Integration with Other Plugins

While MCP servers are isolated per plugin, they can be used together when multiple plugins are installed. For example:
- Install `common-mcp-plugin` for shared tools
- Install `code-style-plugin` for code review skills
- Both work together seamlessly

## Documentation

For more information about MCP (Model Context Protocol):
- [Claude Code MCP Documentation](https://docs.claude.com/en/docs/claude-code/mcp)

For more information about Claude Code plugins:
- [Claude Code Plugins Documentation](https://docs.claude.com/en/docs/claude-code/plugins)

## Version History

- **1.0.0** (2025-10-28) - Initial release with Chrome DevTools MCP server
