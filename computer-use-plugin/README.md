# Computer Use Plugin

Automates app testing using Computer Use MCP. Runs scenario-based tests and ad-hoc exploration to detect functionality, UI, and UX issues, then generates structured feedback reports.

## Installation

```bash
/plugin marketplace add .
/plugin install computer-use-plugin@devstefancho-claude-plugins
```

## Prerequisites

- Computer Use MCP must be active at `/mcp`

## Trigger Keywords

- "computer use test", "cu test", "app test", "UI test", "app QA"

## How It Works

1. **Setup** - Confirm target app and request Computer Use MCP permissions
2. **Scenario Preparation** - Check existing scenarios or create new ones
3. **Scenario Execution** - Execute each step via Computer Use, detecting issues along the way
4. **Ad-hoc Exploration** - Free-form exploration beyond scenarios to discover additional issues
5. **Report** - Generate a structured feedback report

## Output Structure

```
test-cases/
└── {app-name}/
    ├── scenario-basic-flow.md
    ├── scenario-error-handling.md
    └── reports/
        └── 2026-04-05-report.md
```

## Templates

- `scenario-template.md` - Test scenario (App, Preconditions, Steps)
- `feedback-template.md` - Individual issue item (Severity, Category, Description, Screenshot)
- `report-template.md` - Final report (Summary, Issues, Ad-hoc Exploration, Recommendations)
