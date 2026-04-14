# Agent Team Plugin

Create, expand, and manage agent teams for worktree sessions. Orchestrates multi-agent collaboration with a task-driven workflow.

## Installation

```bash
/plugin marketplace add .
/plugin install agent-team-plugin@devstefancho-claude-plugins
```

## Prerequisites

- Must start with `claude -w` (worktree session)
- Run `create team` from the active team-lead session, not from a forked helper agent
- `writing-specs-plugin` recommended for planner's spec writing (optional)

## Commands

| Command | Description |
|---------|-------------|
| `create team` (skill) | Create a default team with planner + implementer |
| `/expand-team` | Add specialized roles to existing team |
| `/cleanup-team` | Terminate members and clean up team |

## Trigger Keywords

- "create team", "agent team"

## Default Team Structure

| Member | Role |
|--------|------|
| team-lead | Orchestration, task assignment |
| planner | Brainstorming, spec writing |
| implementer | Code implementation, test writing |

### Workflow

```
Goal → planner(spec) → TaskCreate → team-lead review → implementer(code) → Done
```

## Expanding the Team

```
/expand-team           # Show role catalog with recommendations
/expand-team tester    # Add a specific role directly
```

### Available Roles

| Role | Description | Best For |
|------|-------------|----------|
| **tester** | Test writing, coverage analysis | Post-implementation quality checks |
| **reviewer** | Code review, security/performance | Pre-PR quality gate |
| **researcher** | Codebase exploration, tech research | New tech adoption, legacy analysis |
| **architect** | System design, API design | Large features, refactoring |
| **devops** | CI/CD, Docker, IaC | Infrastructure, pipelines |
| **ui-designer** | UI components, design systems | Frontend-focused work |
| **security-auditor** | Security vulnerabilities, CVE checks | Security audits, pre-release |
| **custom** | User-defined role | Special tasks |

## Cleaning Up

```
/cleanup-team           # Show members and select who to remove
/cleanup-team --all     # Terminate all members and delete team
/cleanup-team --unused  # Terminate idle members only
/cleanup-team --default # Keep planner/implementer, remove others
```

## Configuration

### Skill model and effort

The `create team` skill is configured to run with `model: sonnet` and `effort: high` for more reliable team orchestration and fallback handling.

### Teammate model

Teammates use the standard Opus model by default.

### Auto-Setup

When a team is created, the following are configured automatically:
- Planner: `/loop 10m /writing-specs update spec`
- Implementer: Periodic TaskList checks
- Colors: Auto-assigned (not programmable)
