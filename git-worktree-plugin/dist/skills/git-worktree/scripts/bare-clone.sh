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

# 4. Ensure bare flag is set (worktree 추가 시 false로 바뀔 수 있으므로 명시적 설정)
git -C "$TARGET_PATH" config core.bare true

# 5. Configure fetch refspec and map local refs to remote tracking refs
# (git clone --bare already fetched data, so no network fetch needed)
git -C "$TARGET_PATH" config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
cd "$TARGET_PATH"
for ref in $(git for-each-ref --format='%(refname:short)' refs/heads/); do
  git update-ref "refs/remotes/origin/$ref" "refs/heads/$ref"
done

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
