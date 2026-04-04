# Writing Specs Plugin

Spec-driven development skill with conflict detection and reporting. Replaces `spec-manager-plugin`.

## Installation

```bash
/plugin install writing-specs-plugin@devstefancho-claude-plugins
```

## Trigger Keywords

- "스펙 생성해줘", "스펙 업데이트해줘", "스펙 작성해줘"
- "create spec", "update spec", "write spec"

## How It Works

1. **Search** - Searches existing specs for conflicts/duplicates/outdated content
2. **Decision** - Asks user how to proceed if related specs exist
3. **Write** - Creates/updates spec using a fixed template (Purpose, Requirements, Approach, Verification)
4. **Report** - Outputs a concise report of what was done

## Directory Structure

```
specs/
├── feature-name.md
├── api/
│   └── endpoint-auth.md
└── auth/
    └── jwt-tokens.md
```

- Files go in `specs/` with optional 1-depth subdirectories
- Filenames use lowercase-with-hyphens

## Differences from spec-manager-plugin

| Feature | spec-manager | writing-specs |
|---------|-------------|---------------|
| Execution | Main context | Fork (subagent) |
| Template | XML tags, 6 scope templates | Markdown headings, 1 universal template |
| Conflict search | Basic duplicate check | Keyword search + outdated detection |
| Report | None | Structured report after every operation |
| Directory | `specs/{scope}/` | `specs/` with optional subdirs |
