---
description: Create PR with auto-generated title and description
allowed-tools: Bash(git status:*), Bash(git log:*), Bash(git diff:*), Bash(git push:*), Bash(gh pr create:*)
---

Create a pull request by following these steps:

1. Run these commands in parallel to understand the current state:
   - `git status` - Check branch status and tracking
   - `git log origin/main..HEAD --oneline` - See commits that will be in the PR
   - `git diff origin/main...HEAD` - See all changes compared to origin's main branch

2. Analyze all changes and commits to draft:
   - PR title: Concise summary following the repo's commit message style
   - PR body with this format:
     ```
     ## Summary
     - [Bullet point 1]
     - [Bullet point 2]
     - [Bullet point 3]

     ## Test plan
     - [ ] [Test step 1]
     - [ ] [Test step 2]

     🤖 Generated with [Claude Code](https://claude.com/claude-code)
     ```

3. Push current branch to origin with `-u` flag if needed

4. Create PR using:
   ```bash
   gh pr create --title "PR title here" --body "$(cat <<'EOF'
   ## Summary
   - Point 1
   - Point 2

   ## Test plan
   - [ ] Step 1

   🤖 Generated with [Claude Code](https://claude.com/claude-code)
   EOF
   )"
   ```

5. Return the PR URL when done

IMPORTANT:
- Compare with origin/main (not local main)
- Review ALL commits from branch point, not just latest commit
- Keep title concise and descriptive
- Make summary bullets focus on "why" not just "what"
