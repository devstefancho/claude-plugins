#!/bin/bash
set -euo pipefail

# Usage: bare-clone.sh --url URL --path PATH --branch BRANCH

usage() {
  echo "Usage: $0 --url URL --path PATH --branch BRANCH"
  exit 1
}

URL=""
TARGET_PATH=""
BRANCH=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --url) URL="$2"; shift 2 ;;
    --path) TARGET_PATH="$2"; shift 2 ;;
    --branch) BRANCH="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; usage ;;
  esac
done

if [ -z "$URL" ] || [ -z "$TARGET_PATH" ] || [ -z "$BRANCH" ]; then
  echo "ERROR: --url, --path, and --branch are all required" >&2
  usage
fi

if [ -d "$TARGET_PATH/.bare" ]; then
  echo "ERROR: $TARGET_PATH/.bare already exists" >&2
  exit 1
fi

# 1. Create project directory
mkdir -p "$TARGET_PATH"

# 2. Clone as bare repository
git clone --bare "$URL" "$TARGET_PATH/.bare"

# 3. Create gitdir pointer
echo "gitdir: ./.bare" > "$TARGET_PATH/.git"

# 4. Configure fetch refspec
git -C "$TARGET_PATH" config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"

# 5. Fetch all remote branches
git -C "$TARGET_PATH" fetch origin

# 6. Create trees directory
mkdir -p "$TARGET_PATH/trees"

# 7. Create initial worktree
git -C "$TARGET_PATH" worktree add "./trees/$BRANCH" "$BRANCH"

echo ""
echo "Bare repository setup complete!"
echo ""
echo "Location: $TARGET_PATH"
echo "Structure:"
echo "  .bare/              (bare repository)"
echo "  .git                (gitdir pointer)"
echo "  trees/"
echo "    $BRANCH/          (initial worktree)"
echo ""
echo "Next steps:"
echo "  cd $TARGET_PATH/trees/$BRANCH"
