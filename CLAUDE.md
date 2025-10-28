# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository serves as a **Claude Code plugins marketplace** containing reusable extensions that can be shared across projects and teams. Plugins provide custom slash commands, Agent Skills, subagents, hooks, and MCP server integrations.

## Plugin Development Workflow

### Adding New Plugins

Each plugin follows this standard structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json              # Plugin metadata (required)
├── commands/                     # Slash commands (optional)
│   └── example.md
├── agents/                       # Subagents (optional)
│   └── helper.md
├── skills/                       # Agent Skills (optional)
│   └── my-skill/
│       ├── SKILL.md
│       ├── PRINCIPLES.md         # Reference docs
│       └── EXAMPLES.md
├── hooks/                        # Event handlers (optional)
│   └── hooks.json
├── .mcp.json                     # MCP servers (optional)
└── README.md                     # Usage documentation
```

The only required file is `.claude-plugin/plugin.json`. Add other components as needed.

### Testing Plugins Locally

```bash
# From repository root
claude

# Within Claude Code
/plugin marketplace add .
/plugin install plugin-name@devstefancho-claude-plugins
```

After installation, restart Claude Code to activate the plugin.

### Iterating on Plugin Components

When developing or updating plugin components (skills, commands, hooks):

1. Modify files within the plugin directory
2. Uninstall the plugin: `/plugin uninstall plugin-name@devstefancho-claude-plugins`
3. Reinstall to test changes: `/plugin install plugin-name@devstefancho-claude-plugins`
4. Restart Claude Code if needed

## Plugin Architecture

### Marketplace Configuration

`.claude-plugin/marketplace.json` defines all available plugins:
- Lists plugin names and their source directories
- Metadata for discovery and installation
- Used by `/plugin install` commands

### Plugin Metadata

Each plugin requires `.claude-plugin/plugin.json`:
- `name`: Plugin identifier (kebab-case)
- `description`: Human-readable summary
- `version`: Semantic versioning (e.g., 1.0.0)
- `author`: Author information

### Plugin Components

**Slash Commands** (`commands/`)
- Markdown files with frontmatter metadata
- One file per command (e.g., `spec.md` defines `/spec`)
- Include `description` and `argument-hint` in frontmatter

**Agent Skills** (`skills/`)
- Directory structure: `skills/skill-name/SKILL.md`
- Main skill definition in `SKILL.md` with metadata and instructions
- Supporting documentation in `PRINCIPLES.md` and `EXAMPLES.md`
- Skills are automatically available when plugin is installed

**Subagents** (`agents/`)
- Custom agent definitions
- Extend Claude Code's agent capabilities

**Event Hooks** (`hooks/`)
- Automation based on IDE events
- Defined in `hooks.json`

**MCP Servers** (`.mcp.json`)
- External tool integration
- Provides LLM-compatible tool definitions

## Key Directories

- **`.claude-plugin/`** - Marketplace and plugin metadata
  - `marketplace.json` - Marketplace catalog
  - Plugin directories contain `.claude-plugin/plugin.json`

- **`docs/`** - Reference documentation for Claude Code features
  - Not part of plugins; useful for understanding plugin development patterns

- **Plugin directories** (e.g., `code-style-plugin/`, `simple-sdd-plugin/`)
  - Each plugin is self-contained and independently installable
  - Include README.md with installation and usage instructions

## Adding New Content to Plugins

When extending existing plugins or creating new ones:

1. **For new slash commands**: Add markdown file to `plugin-name/commands/`
2. **For new skills**: Create directory under `plugin-name/skills/`
3. **For new subagents**: Add markdown file to `plugin-name/agents/`
4. **For MCP servers**: Add or update `.mcp.json` in plugin root
5. **For hooks**: Add to or update `plugin-name/hooks/hooks.json`

After adding components, update the plugin's `.claude-plugin/plugin.json` version number.

## Managing MCP Servers through Plugins

### Plugin-based MCP Server Configuration

Each plugin can include its own `.mcp.json` file at the plugin root to define MCP (Model Context Protocol) servers. This enables:

- **Server Isolation**: Each plugin manages its own MCP servers independently
- **Dependency Management**: MCP servers are installed/removed with the plugin
- **Team Sharing**: Common MCP configurations can be distributed via plugins
- **Clean Separation**: No conflicts when multiple plugins define MCP servers

### Creating a Plugin with MCP Servers

When adding MCP servers to a plugin:

1. Create `.mcp.json` in the plugin root directory
2. Define your MCP server configurations in the standard format:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["server-package@latest"]
    }
  }
}
```

3. Document the MCP servers in the plugin's `README.md`
4. Update the plugin's `.claude-plugin/plugin.json` version number

### Example: common-mcp-plugin

The `common-mcp-plugin` provides shared MCP servers for the marketplace:

```
common-mcp-plugin/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json                # Defines chrome-devtools, etc
└── README.md
```

When installed, all MCP servers defined in `common-mcp-plugin/.mcp.json` become available for use across Claude Code sessions.

### Best Practices

1. **Centralize common servers**: Use a dedicated plugin like `common-mcp-plugin` for widely-used MCP servers
2. **Plugin-specific servers**: Include specialized MCP servers directly in feature plugins
3. **Documentation**: Always document which MCP servers a plugin provides
4. **Version management**: Use semantic versioning and track MCP server updates in the plugin version

## Distribution

Plugins can be shared through:

1. **Git Repository**: Commit to version control
   ```bash
   /plugin install plugin-name@your-org/claude-plugins
   ```

2. **Local Development**: Reference repository path
   ```bash
   /plugin marketplace add ./path/to/repo
   /plugin install plugin-name@your-local-marketplace
   ```

3. **Team Repository Configuration**: Add to `.claude/settings.json` for automatic plugin installation across team projects

## Common Commands

```bash
# View all available plugins
/plugin

# Add marketplace to local development
/plugin marketplace add .

# Install a plugin
/plugin install plugin-name@devstefancho-claude-plugins

# List installed plugins
/plugin

# Uninstall a plugin
/plugin uninstall plugin-name@devstefancho-claude-plugins

# View installed commands
/help
```

## See Also

- Claude Code Plugins Documentation: Check `docs/` directory for feature references
- Individual plugin READMEs: Each plugin contains usage documentation
- Plugin Structure: Refer to existing plugins as examples (e.g., `code-style-plugin/`)
