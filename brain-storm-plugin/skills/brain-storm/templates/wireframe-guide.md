# Wireframe Guide

ASCII wireframe conventions for UI ideas. Follow these rules for consistency.

## Box Drawing Characters

Use Unicode box-drawing characters for all borders:

```
┌─────────────────────────┐
│  Component Name         │
├─────────────────────────┤
│  Content area           │
└─────────────────────────┘
```

Characters: `┌ ─ ┐ │ └ ┘ ├ ┤ ┬ ┴ ┼`

## Interactive Elements

- Buttons: `[ Button Text ]`
- Text input: `[ input field_________ ]`
- Checkbox checked: `[x] Label`
- Checkbox unchecked: `[ ] Label`
- Radio selected: `(●) Label`
- Radio unselected: `(○) Label`
- Dropdown: `[ Select ▼ ]`
- Link: `<Link Text>`

## Layout Rules

- Minimum 10 lines for any wireframe
- Show the most important screen or state first
- Use `...` for truncated or repeated content
- Add annotations with `← description` or `// comment` for non-obvious elements
- Indent nested components by 2 spaces

## Example

```
┌─────────────────────────────────────┐
│  ☰  App Title              [👤]    │
├─────────────────────────────────────┤
│                                     │
│  ┌───────────┐  ┌───────────┐      │
│  │  Card 1   │  │  Card 2   │      │
│  │  desc...  │  │  desc...  │      │
│  │ [ View ]  │  │ [ View ]  │      │
│  └───────────┘  └───────────┘      │
│                                     │
│  ┌───────────┐  ┌───────────┐      │
│  │  Card 3   │  │  Card 4   │      │
│  │  desc...  │  │  desc...  │      │
│  │ [ View ]  │  │ [ View ]  │      │
│  └───────────┘  └───────────┘      │
│                                     │
│         [ Load More ]               │
└─────────────────────────────────────┘
```
