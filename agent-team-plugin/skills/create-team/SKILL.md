---
name: create-team
description: Create an agent team with planner and implementer teammates for spec-driven development. Use when user says "create team", "팀 생성", "팀 만들어줘", "agent team", or wants to set up a planner+implementer workflow in a worktree session.
model: sonnet
effort: high
allowed-tools: Bash, Agent, SendMessage, TeamCreate, TaskCreate, TaskList, TaskUpdate, Read, AskUserQuestion
---

# Create Team

Creates a planner + implementer agent team for the current worktree session.

## Workflow

### Step 1: Determine team name

Run `git branch --show-current` to get the current branch name. Convert to kebab-case team name:
- Remove `worktree-` prefix if present
- Replace `+` with `-`
- Example: `worktree-feat+electron-app` → `feat-electron-app`

### Step 2: Create the team

Call `TeamCreate` with:
- `team_name`: the derived team name
- `description`: "Planner + Implementer team"

### Step 3: Spawn teammates (parallel)

Spawn both teammates **in parallel** using the Agent tool in a single message with two tool calls:

**Planner:**
- `team_name`: the team name
- `name`: "planner"
- `description`: "Planner - brainstorm and spec writing"
- `prompt`: Read the full content of [templates/planner-prompt.md](templates/planner-prompt.md) and pass it as the prompt
- `run_in_background`: true

**Implementer:**
- `team_name`: the team name
- `name`: "implementer"
- `description`: "Implementer - code and test writing"
- `prompt`: Read the full content of [templates/implementer-prompt.md](templates/implementer-prompt.md) and pass it as the prompt
- `run_in_background`: true

### Step 4: Loop setup

Send loop configuration via SendMessage:
- To "planner": If `/writing-specs` skill is available, "Run `/loop 10m /writing-specs update spec` to periodically check and update specs." Otherwise skip this loop setup.
- To "implementer": "After completing assigned work, check TaskList for new tasks. You can run `/loop 10m check TaskList for unassigned tasks and report to team-lead` to automate this."

### Step 5: Display work guide

Read [templates/work-guide.md](templates/work-guide.md) and display the content to the user.
Teammate colors are auto-assigned from a hardcoded palette and cannot be configured programmatically.

## Fallback

If teammate spawning via the Agent tool fails with `team_name` or another internal error in the current session (known issue anthropics/claude-code#40270):
1. Inform the user that team creation succeeded but teammate spawning failed in the current execution context
2. Suggest spawning teammates manually:
   - Open separate terminal windows
   - Run `claude` in each with the planner/implementer prompts
   - Use SendMessage for coordination
3. Do not claim the Agent tool is globally unavailable unless the session explicitly shows that tool is missing

## Notes

- Teammates are full Claude Code sessions, not subagents
- Both teammates can use all tools including Write, Edit, Bash
- Both can run skills like `/writing-specs`, `/loop`
- `/loop` is session-scoped and expires after 7 days
- Teammate colors are auto-assigned from hardcoded palette (red, blue, green, yellow...) — not configurable
- All communication flows through team-lead (planner <-> implementer direct messaging disabled by prompt rules)
- Teammate model defaults to standard Opus.
