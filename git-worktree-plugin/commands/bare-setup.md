---
description: Clone repository as bare and setup worktree structure for parallel branch work
allowed-tools: Bash, AskUserQuestion
---

# Bare Repository Setup

Clone a repository as bare and configure it for git worktree workflow.

<context>
This command sets up a new project with a bare repository structure that enables parallel branch work using git worktrees.

Example structure after setup:
```
project-name/
├── .bare/              # Bare git repository
├── .git                # File pointing to .bare
└── trees/
    └── main/           # Initial worktree (working directory)
```
</context>

<instruction>

## Step 1: Get Repository URL

Use AskUserQuestion to get the repository URL:

```
Question: "Enter the repository URL (SSH or HTTPS)"
Header: "URL"
Options:
- User provides URL in text input (Other option)
```

Validate URL format:
- SSH: starts with `git@` (e.g., `git@github.com:owner/repo.git`)
- HTTPS: starts with `https://` (e.g., `https://github.com/owner/repo.git`)

If invalid, show error and ask again.

## Step 2: Determine Project Location

Extract project name from URL (e.g., `agent-web` from `git@github.com:org/agent-web.git`)

Use AskUserQuestion:

```
Question: "Where should the project be created?"
Header: "Location"
Options:
- "Current directory (./{project-name}) (Recommended)" - Create in current working directory
- "Parent directory (../{project-name})" - Create one level up
```

Note: User can select "Other" for custom path

## Step 3: Confirm Setup

Show summary and use AskUserQuestion:

```
Question: "Ready to setup bare repository with this configuration?"
Header: "Confirm"

Display summary:
- Repository: {url}
- Location: {full-path}
- Structure: .bare/ + trees/{branch}/

Options:
- "Proceed (Recommended)" - Create the bare repository setup
- "Cancel" - Abort operation
```

If "Cancel" selected, abort and inform user.

## Step 4: Execute Git Commands

Run these commands in sequence:

1. Create project directory:
```bash
mkdir -p {project-path}
```

2. Clone as bare repository:
```bash
git clone --bare {url} {project-path}/.bare
```

If clone fails:
- Show the git error message
- Common issues: "Permission denied" (SSH key), "Repository not found" (URL incorrect)
- Abort operation

3. Create gitdir pointer file:
```bash
echo "gitdir: ./.bare" > {project-path}/.git
```

4. Configure fetch refspec (enables git pull/push for all branches):
```bash
git -C {project-path} config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
```

5. Fetch all remote branches:
```bash
git -C {project-path} fetch origin
```

6. Create trees directory for worktrees:
```bash
mkdir -p {project-path}/trees
```

## Step 5: Select Initial Branch

Get available branches:
```bash
git -C {project-path} branch -r
```

Use AskUserQuestion:

```
Question: "Which branch should be the initial worktree?"
Header: "Branch"
Options:
- "main (Recommended)" - if origin/main exists
- "develop" - if origin/develop exists
- "master" - if origin/master exists (legacy)
```

Only show options for branches that exist. User can select "Other" for different branch.

## Step 6: Create Initial Worktree

Create the initial worktree:
```bash
git -C {project-path} worktree add ./trees/{branch} {branch}
```

If branch doesn't exist locally but exists on remote:
```bash
git -C {project-path} worktree add ./trees/{branch} origin/{branch}
```

## Step 7: Display Completion Summary

Output completion message:

```
Bare repository setup complete!

Location: {project-path}
Structure:
  .bare/              (bare repository)
  .git                (gitdir pointer)
  trees/
    {branch}/         (initial worktree - your working directory)

Next steps:
  cd {project-path}/trees/{branch}

Useful commands:
  git worktree list              - List all worktrees
  git worktree add ./trees/new-branch -b feat/new origin/main
                                 - Create new worktree with branch
  git fetch origin               - Fetch latest from remote
```

</instruction>

<important>
- The `.bare` directory contains the actual git repository data
- The `.git` file (not directory) is a pointer to `.bare`
- All worktrees should be created under `./trees/` directory
- The fetch refspec configuration is essential for `git fetch` and `git pull` to work properly
- Each worktree is a separate working directory for parallel branch development
</important>

<examples>
Usage examples:

1. Basic usage (interactive):
```
/bare-setup
```

2. With repository URL:
```
/bare-setup git@github.com:myorg/myrepo.git
```

Result structure:
```
myrepo/
├── .bare/
├── .git
└── trees/
    └── main/
        ├── src/
        ├── package.json
        └── ...
```
</examples>
