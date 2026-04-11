# Brain Storm Plugin

Brainstorm future features and improvements based on the current codebase, then generate standalone HTML previews for UI-heavy ideas. This plugin packages both ideation and prototype-preview workflows into one installation.

## Installation

```bash
/plugin marketplace add .
/plugin install brain-storm-plugin@devstefancho-claude-plugins
```

## Included Skills

### 1. `brain-storm`

Use this skill to scan a codebase, propose grounded ideas, add ASCII wireframes, and save selected ideas into `brain-storm/` for later refinement.

Typical triggers:

- "brainstorm"
- "feature ideas"
- "what could we build"
- "improvement ideas"
- "clean up brainstorm notes"

### 2. `ui-prototype-preview`

Use this skill after a UI-focused brainstorm idea has been saved and you want a richer HTML mockup with a clear visual point of view.

Typical triggers:

- "prototype preview"
- "generate HTML preview"
- "turn this idea into a mockup"
- "create a UI prototype"
- "make the design stronger"

### 3. `/ui-prototype-preview` command

Use the slash command when you want a lightweight entry point for prototype generation. The skill remains the real implementation; the command is only a thin wrapper for more explicit invocation and better argument discoverability.

Examples:
- `/ui-prototype-preview running-portfolio-narrative-dashboard`
- `/ui-prototype-preview running-portfolio-narrative-dashboard editorial dark`
- `/ui-prototype-preview @brain-storm/running-portfolio-narrative-dashboard.md create 3 variants using our brand colors`

The command should resolve the source idea, read or scaffold a design brief when needed, and then invoke the `ui-prototype-preview` workflow.

## How It Works

1. **Codebase Scan** - Analyze the product structure and existing brainstorm notes.
2. **Ideation** - Generate 3-5 ideas with complexity ratings and quick wireframes.
3. **Deduplication** - Check existing brainstorm notes before writing new files.
4. **Write** - Save selected ideas using a consistent markdown template.
5. **Prototype Preview** - Turn selected UI ideas into standalone HTML files with a deliberate aesthetic direction.
6. **Cleanup** - Detect already-implemented ideas and remove them after user confirmation.
7. **Report** - Return concise next-step guidance for specs or preview revisions.

## Output Structure

```text
brain-storm/
├── dashboard-analytics.md
├── auth/
│   └── sso-login.md
├── design/
│   └── dashboard-analytics-design.md
└── previews/
    ├── dashboard-analytics.html
    └── dashboard-analytics-editorial-dark.html
```

- Idea notes live in `brain-storm/` with optional one-level subdirectories.
- Design briefs live in `brain-storm/design/`.
- HTML previews live in `brain-storm/previews/`.
- Filenames use lowercase-with-hyphens.

## Design Brief Workflow

When a prototype needs multiple variants, exact colors, typography rules, or stronger brand constraints, use a design brief file rather than overloading the prompt.

Recommended path:
1. Save or auto-generate `brain-storm/design/{idea-name}-design.md`.
2. Put variant count, aesthetic directions, color tokens, references, and anti-patterns in that file.
3. Run `/ui-prototype-preview {idea title}`.
4. Refine the design brief and rerun as needed.

If no design brief exists and the request is complex, the skill should scaffold one automatically from the template and continue with a first-pass prototype.

## Recommended Workflow

1. Generate and save promising ideas with `brain-storm`.
2. For UI-heavy ideas, create a mockup with `/ui-prototype-preview {idea title}`.
3. If you need stronger control, create or edit `brain-storm/design/{idea-name}-design.md` with brand colors, typography notes, variant strategy, and constraints.
4. Turn the validated idea into a buildable spec with `/writing-specs {idea title}`.
