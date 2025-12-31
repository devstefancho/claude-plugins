# Installation Guide

Detailed guide for plugin installation and management.

## Marketplace Management

### Register Marketplace

```bash
/plugin marketplace add devstefancho/claude-plugins
```

### Check Registered Marketplaces

```bash
/plugin
# Shows 'devstefancho-claude-plugins' marketplace
```

## Plugin Installation

### Install Single Plugin

```bash
/plugin install <plugin-name>@devstefancho-claude-plugins
```

### Recommended Plugin Sets

**Code Review Set**
```bash
/plugin install code-style-plugin@devstefancho-claude-plugins
/plugin install code-quality-plugin@devstefancho-claude-plugins
```

**Git Workflow Set**
```bash
/plugin install git-commit-plugin@devstefancho-claude-plugins
/plugin install pr-create-plugin@devstefancho-claude-plugins
/plugin install git-worktree-plugin@devstefancho-claude-plugins
```

**Development Productivity Set**
```bash
/plugin install scaffold-claude-feature@devstefancho-claude-plugins
/plugin install session-reporter-plugin@devstefancho-claude-plugins
/plugin install stop-notification-plugin@devstefancho-claude-plugins
```

## Uninstall Plugin

```bash
/plugin uninstall <plugin-name>@devstefancho-claude-plugins
```

## Post-Installation Checklist

1. ✅ Restart Claude Code (close and reopen terminal)
2. ✅ Verify installation with `/plugin` command
3. ✅ Check new commands with `/help` (for Commands plugins)
4. ✅ Skills are automatically detected and activated

## Troubleshooting

### Plugin Not Working

1. Ensure Claude Code was fully restarted
2. Verify plugin is installed with `/plugin` command
3. Check plugin version compatibility

### Marketplace Registration Failed

```bash
# Verify GitHub access
git ls-remote https://github.com/devstefancho/claude-plugins.git
```

## Team Sharing

Add marketplace to your team project's `.claude/settings.json` for automatic sharing:

```json
{
  "plugins": {
    "marketplaces": ["devstefancho/claude-plugins"]
  }
}
```
