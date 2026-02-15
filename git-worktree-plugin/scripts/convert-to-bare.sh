#!/bin/bash
set -euo pipefail

# Usage: convert-to-bare.sh --project-root ROOT

usage() {
  echo "Usage: $0 --project-root ROOT"
  exit 1
}

PROJECT_ROOT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project-root) PROJECT_ROOT="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; usage ;;
  esac
done

if [ -z "$PROJECT_ROOT" ]; then
  echo "ERROR: --project-root is required" >&2
  usage
fi

BACKUP_DIR="$PROJECT_ROOT/.git-backup"

# ── Precondition checks ──

if [ ! -d "$PROJECT_ROOT/.git" ]; then
  echo "ERROR: .git 디렉토리가 없거나 이미 bare repo입니다" >&2
  exit 1
fi

if [ -n "$(git -C "$PROJECT_ROOT" status --porcelain)" ]; then
  echo "ERROR: uncommitted changes가 있습니다. 커밋하거나 stash 후 다시 시도하세요" >&2
  exit 1
fi

BRANCH=$(git -C "$PROJECT_ROOT" branch --show-current)
if [ -z "$BRANCH" ]; then
  echo "ERROR: detached HEAD 상태입니다. 브랜치를 체크아웃하세요" >&2
  exit 1
fi

# ── Backup ──
echo "백업 생성: $BACKUP_DIR"
cp -a "$PROJECT_ROOT/.git" "$BACKUP_DIR"

# ── Rollback function ──
rollback() {
  echo "ERROR 발생. 롤백 시작..." >&2
  cd "$PROJECT_ROOT"
  # Clean up .bare
  [ -d "$PROJECT_ROOT/.bare" ] && rm -rf "$PROJECT_ROOT/.bare"
  # Clean up trees/
  [ -d "$PROJECT_ROOT/trees" ] && rm -rf "$PROJECT_ROOT/trees"
  # Restore .git
  if [ -f "$PROJECT_ROOT/.git" ]; then
    rm "$PROJECT_ROOT/.git"
  fi
  if [ -d "$BACKUP_DIR" ]; then
    mv "$BACKUP_DIR" "$PROJECT_ROOT/.git"
    echo "롤백 완료. 원래 상태로 복원되었습니다." >&2
  fi
  exit 1
}
trap rollback ERR

# ── Convert ──
cd "$PROJECT_ROOT"

# .git/ → .bare/
mv .git .bare
echo "gitdir: ./.bare" > .git

# Configure fetch
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin

# Create worktree
mkdir -p trees
git worktree add --force "trees/$BRANCH" "$BRANCH"

# Clean orphan files in project root (keep .bare, .git, trees, .git-backup)
for item in * .[!.]*; do
  case "$item" in
    .bare|.git|.git-backup|trees) continue ;;
    *) rm -rf "$item" ;;
  esac
done

# ── Verify ──
if [ ! -d "trees/$BRANCH" ]; then
  echo "ERROR: worktree 생성 실패" >&2
  rollback
fi

echo ""
echo "변환 완료!"
echo "구조:"
echo "  .bare/          (bare repository)"
echo "  .git            (gitdir pointer)"
echo "  .git-backup/    (원본 .git 백업 - 문제없으면 삭제 가능)"
echo "  trees/$BRANCH/  (worktree)"
echo ""
echo "다음 단계: cd trees/$BRANCH"

trap - ERR
