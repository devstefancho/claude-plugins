# Brain Storm Plugin

Brainstorm future features and improvements based on the current codebase. Includes ASCII wireframes for UI ideas and auto-detects already-implemented ideas for cleanup.

## Installation

```bash
/plugin marketplace add .
/plugin install brain-storm-plugin@devstefancho-claude-plugins
```

## Trigger Keywords

- "brainstorm", "feature ideas", "what could we build", "improvement ideas"

## How It Works

1. **Codebase Scan** - Analyze project structure and existing ideas
2. **Ideation** - Generate 3-5 ideas with complexity ratings and UI tags
3. **Deduplication** - Check against existing ideas to avoid duplicates
4. **Write** - Save selected ideas using templates (with wireframes for UI ideas)
5. **Implementation Check** - Detect already-implemented ideas and remove with user confirmation
6. **Report** - Output a summary of results

## Directory Structure

```
brain-storm/
├── dashboard-analytics.md
├── auth/
│   └── sso-login.md
└── ui/
    └── dark-mode-toggle.md
```

- Files are stored in `brain-storm/` with optional 1-depth subdirectories
- Filenames use lowercase-with-hyphens format

## Differences from writing-specs-plugin

| writing-specs | brain-storm |
|---------------|-------------|
| Specifies what **will** be built | Explores what **could** be built |
| Structured requirements | Exploratory ideas |
| No wireframes | ASCII wireframes for UI ideas |
| Outdated content detection | Implementation completion detection |
