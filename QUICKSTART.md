# Code Style Plugin - Quick Start Guide

## Get Started in 5 Minutes

### Step 1: Add Marketplace (1 min)

```bash
cd /path/to/claude-plugins
claude

# Inside Claude Code
/plugin marketplace add .
```

### Step 2: Install Plugin (2 min)

```bash
/plugin install code-style-plugin@devstefancho-claude-plugins
```

Select "Install now" and restart Claude Code

### Step 3: Test (2 min)

Create a code file or use an existing file:

```
Can you analyze @src/example.ts from a code style perspective?
```

or

```
Review this code. @src/services/user.ts
```

---

## Usage Examples

### Example 1: File Review

```
Analyze the code style of @src/controllers/userController.ts
```

**Result**: Detailed review based on 5 principles (SRP, DRY, Simplicity, YAGNI, Type Safety)

### Example 2: Function Review

```typescript
// Can you review this function?
async function handleUserData(data: any) {
  if (data) {
    if (data.user) {
      if (data.user.id) {
        const userId = data.user.id;
        const user = await getUser(userId);
        if (user) {
          const posts = await getPosts(userId);
          const comments = await getComments(userId);
          const followers = await getFollowers(userId);
          return {
            user,
            posts,
            comments,
            followers,
            timestamp: new Date()
          };
        }
      }
    }
  }
  return null;
}
```

**Possible Feedback**:
- Deep nesting (Simplicity First)
- Multiple responsibilities (SRP)
- `any` type usage (Type Safety)

---

## Key Features

### Automatic Checks

| Principle | What's Checked |
|-----------|----------------|
| **SRP** | Does the function/class have single responsibility? Is function length appropriate? |
| **DRY** | Is there repeated code? Should common logic be extracted? |
| **Simplicity** | Is there unnecessary complexity? Is nesting too deep? |
| **YAGNI** | Is there unused code? Are there unnecessary features? |
| **Type** | Is `any` used? Are types clearly defined? |

### Additional Checks

- Naming conventions (camelCase, PascalCase, UPPER_SNAKE_CASE)
- Function size and complexity
- Comments and documentation quality
- Error handling

---

## Reading Review Reports

### Critical Issues
Issues that must be fixed
- Clear potential for bugs
- Serious code smells

### Warnings
Items recommended for improvement
- Reduced maintainability
- Potential problems

### Suggestions
Suggestions worth considering
- Code improvement ideas
- Better pattern suggestions

---

## FAQ

### Q: Plugin won't install
A:
1. Run `/plugin marketplace add .` again
2. Restart Claude Code
3. Run `/plugin install code-style-plugin@devstefancho-claude-plugins` again

### Q: Skill doesn't activate automatically
A:
1. Restart Claude Code
2. Include keywords like "code review", "analyze", "improve" in your request
3. Explicitly: "Can you use the code-style-reviewer skill?"

### Q: I want to check only specific principles
A:
Specify in your request:
```
Focus on SRP and type safety only. @file.ts
```

### Q: How to share with team?
A:
1. Commit plugin directory to Git repository
2. Team members run:
   ```bash
   /plugin install code-style-plugin@your-org/claude-plugins
   ```

---

## Next Steps

1. **Basic Usage** - Start with examples from this guide
2. **Deep Dive** - Read `code-style-plugin/PRINCIPLES.md`
3. **Study Examples** - Learn from `code-style-plugin/EXAMPLES.md`
4. **Team Application** - Apply to project and share with team
5. **Customization** - Modify SKILL.md to reflect team rules

---

## Help Commands

Inside Claude Code:

```bash
# Check plugins
/plugin

# Check installed skills
/help

# Open settings
/config
```

---

**Happy Coding!**
