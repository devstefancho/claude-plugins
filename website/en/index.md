---
layout: home
hero:
  name: Claude Plugins
  text: Claude Code Plugin Marketplace
  tagline: Extend Claude Code with Skills, Commands, Hooks, and MCP Servers
  actions:
    - theme: brand
      text: Browse Plugins
      link: /en/plugins/
    - theme: alt
      text: Get Started
      link: /en/guide/getting-started
---

<HomeFeatures lang="en" />

<div class="quick-start-section">

## Quick Start

<div class="quick-start-steps">
  <div class="step">
    <span class="step-number">1</span>
    <span class="step-text">Register marketplace</span>
  </div>
  <div class="step">
    <span class="step-number">2</span>
    <span class="step-text">Install plugin</span>
  </div>
  <div class="step">
    <span class="step-number">3</span>
    <span class="step-text">Restart Claude Code</span>
  </div>
</div>

```bash
# Using Claude Code CLI
/plugin marketplace add devstefancho/claude-plugins
/plugin install code-style-plugin@devstefancho-claude-plugins
```

```bash
# Or using npx (from any terminal)
npx skills add devstefancho/claude-plugins
```

[View All Plugins →](/en/plugins/)

</div>
