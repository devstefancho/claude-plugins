# Frontend Plugin

Code review skill for React/Next.js component design based on established design principles.

## Installation

```bash
/plugin marketplace add .
/plugin install frontend-plugin@devstefancho-claude-plugins
```

## Included Skills

### Component Design Reviewer

Reviews the design quality of React/Next.js components against the following principles:

- **Single Responsibility Principle (SRP)** - One component, one responsibility
- **Props Design** - Props drilling detection and interface design
- **Composition Pattern** - Proper use of composition over inheritance
- **Reusability** - Component reuse opportunities
- **Custom Hooks Separation** - Logic extraction into custom hooks

## Trigger Keywords

- "Review this component's design"
- "Analyze the component structure of UserDashboard.tsx"
- "Check for props drilling issues"

**Auto-activates on:**
- React/Next.js component review requests
- Component structure analysis
- Props design reviews
- Component refactoring suggestions

## See Also

- [SKILL.md](skills/component-design-reviewer/SKILL.md) - Skill definition
- [PRINCIPLES.md](skills/component-design-reviewer/PRINCIPLES.md) - Detailed principles
- [EXAMPLES.md](skills/component-design-reviewer/EXAMPLES.md) - Code examples
