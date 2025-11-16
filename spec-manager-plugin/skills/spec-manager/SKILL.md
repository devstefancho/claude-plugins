---
name: spec-manager
description: Manage specification files for spec-driven development. Use when creating, updating, or deleting spec files. Supports feat, fix, docs, refactor, and chore scopes.
allowed-tools: Read, Write, Glob, Grep, Bash, AskUserQuestion
---

# Spec Manager

Manages specification files in `specs/{scope}/{work-name}.md` for spec-driven development workflow.

## Principles

1. **One spec = one task** (unless frontend + backend work together)
2. **No "before" sections** - Focus only on the final desired state
3. **XML tag format** - Use XML tags for structure (varies by scope)
4. **Minimal code examples** - Avoid code in specs; if necessary, keep it brief and illustrative
5. **Check for duplicates** - Always verify if similar specs exist before creating

## Operations

### Create
1. Analyze request and infer scope (feat/fix/docs/refactor/chore)
2. Search `specs/{scope}/` for similar existing specs
3. If found, ask: "Create new", "Update existing", or "Cancel"
4. If ambiguous scope, ask user to confirm
5. Generate filename (lowercase-with-hyphens)
6. Use appropriate template based on scope
7. Fill in XML tags based on user request

### Update
1. List existing specs in relevant scope
2. Let user select which to update
3. Verify update aligns with original purpose
4. If purpose changed significantly, suggest new spec
5. Apply changes while maintaining XML structure

### Delete
1. List all specs organized by scope
2. Let user select spec(s) to delete
3. Confirm and remove

### List
Display all specs organized by scope directory structure.

## Templates

See templates directory for scope-specific XML tag structures:
- `feat` → [templates/feat-template.md](templates/feat-template.md)
- `fix` → [templates/fix-template.md](templates/fix-template.md)
- `docs` → [templates/docs-template.md](templates/docs-template.md)
- `refactor` → [templates/refactor-template.md](templates/refactor-template.md)
- `chore` → [templates/chore-template.md](templates/chore-template.md)

Each template uses different XML tags appropriate to its scope.
