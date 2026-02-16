#!/usr/bin/env bash
set -euo pipefail

# local-install.sh - Symlink-based local plugin testing
# Usage: bash local-install.sh <link|unlink> <plugin-name>
# Example: bash local-install.sh link git-worktree-plugin

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MARKETPLACE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
MARKETPLACE_NAME="devstefancho-claude-plugins"
INSTALLED_PLUGINS_JSON="$HOME/.claude/plugins/installed_plugins.json"
CACHE_DIR="$HOME/.claude/plugins/cache/$MARKETPLACE_NAME"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

usage() {
  echo "Usage: bash $0 <link|unlink> <plugin-name>"
  echo "Example: bash $0 link git-worktree-plugin"
  exit 1
}

error() {
  echo -e "${RED}Error: $1${NC}" >&2
  exit 1
}

info() {
  echo -e "${GREEN}$1${NC}"
}

warn() {
  echo -e "${YELLOW}$1${NC}"
}

# Validate arguments
[[ $# -ne 2 ]] && usage
ACTION="$1"
PLUGIN_NAME="$2"
[[ "$ACTION" != "link" && "$ACTION" != "unlink" ]] && usage

PLUGIN_KEY="${PLUGIN_NAME}@${MARKETPLACE_NAME}"
PLUGIN_LOCAL_DIR="$MARKETPLACE_ROOT/$PLUGIN_NAME"

# Check jq is available
command -v jq &>/dev/null || error "jq is required but not installed. Install with: brew install jq"

# Check installed_plugins.json exists
[[ -f "$INSTALLED_PLUGINS_JSON" ]] || error "installed_plugins.json not found at $INSTALLED_PLUGINS_JSON"

# Check plugin exists in installed_plugins.json
ENTRY=$(jq -r --arg key "$PLUGIN_KEY" '.plugins[$key] // empty' "$INSTALLED_PLUGINS_JSON")
[[ -z "$ENTRY" ]] && error "Plugin '$PLUGIN_KEY' is not installed.\nRun: /plugin install $PLUGIN_NAME@$MARKETPLACE_NAME"

# Get current install path and version
CURRENT_INSTALL_PATH=$(echo "$ENTRY" | jq -r '.[0].installPath')
CURRENT_VERSION=$(echo "$ENTRY" | jq -r '.[0].version')

do_link() {
  # Validate local plugin directory exists
  [[ -d "$PLUGIN_LOCAL_DIR" ]] || error "Local plugin directory not found: $PLUGIN_LOCAL_DIR"
  [[ -f "$PLUGIN_LOCAL_DIR/.claude-plugin/plugin.json" ]] || error "plugin.json not found in $PLUGIN_LOCAL_DIR/.claude-plugin/"

  # Check if already symlinked
  if [[ -L "$CURRENT_INSTALL_PATH" ]]; then
    LINK_TARGET=$(readlink "$CURRENT_INSTALL_PATH")
    warn "Already symlinked: $CURRENT_INSTALL_PATH -> $LINK_TARGET"
    exit 0
  fi

  # Read dev version from local plugin.json
  DEV_VERSION=$(jq -r '.version' "$PLUGIN_LOCAL_DIR/.claude-plugin/plugin.json")
  [[ -z "$DEV_VERSION" || "$DEV_VERSION" == "null" ]] && error "Could not read version from $PLUGIN_LOCAL_DIR/.claude-plugin/plugin.json"

  PLUGIN_CACHE_DIR="$CACHE_DIR/$PLUGIN_NAME"
  TARGET_DIR="$PLUGIN_CACHE_DIR/$DEV_VERSION"

  # Backup existing cache directory if it exists and is not a symlink
  if [[ -d "$TARGET_DIR" && ! -L "$TARGET_DIR" ]]; then
    BACKUP_DIR="${TARGET_DIR}.bak"
    if [[ -d "$BACKUP_DIR" ]]; then
      warn "Backup already exists at $BACKUP_DIR, removing old backup"
      rm -rf "$BACKUP_DIR"
    fi
    info "Backing up: $TARGET_DIR -> ${TARGET_DIR}.bak"
    mv "$TARGET_DIR" "$BACKUP_DIR"
  fi

  # Create symlink
  mkdir -p "$PLUGIN_CACHE_DIR"
  ln -s "$PLUGIN_LOCAL_DIR" "$TARGET_DIR"
  info "Symlink created: $TARGET_DIR -> $PLUGIN_LOCAL_DIR"

  # Backup installed_plugins.json
  cp "$INSTALLED_PLUGINS_JSON" "${INSTALLED_PLUGINS_JSON}.bak"
  info "Backed up: installed_plugins.json -> installed_plugins.json.bak"

  # Update installed_plugins.json with new installPath and version
  TEMP_FILE=$(mktemp)
  jq --arg key "$PLUGIN_KEY" \
     --arg path "$TARGET_DIR" \
     --arg ver "$DEV_VERSION" \
     '.plugins[$key][0].installPath = $path | .plugins[$key][0].version = $ver' \
     "$INSTALLED_PLUGINS_JSON" > "$TEMP_FILE"
  mv "$TEMP_FILE" "$INSTALLED_PLUGINS_JSON"
  info "Updated installed_plugins.json: installPath=$TARGET_DIR, version=$DEV_VERSION"

  echo ""
  info "=== Link complete ==="
  info "Plugin '$PLUGIN_NAME' is now linked to local development directory."
  info "Restart Claude Code to apply changes."
}

do_unlink() {
  # Check if backup exists
  BACKUP_JSON="${INSTALLED_PLUGINS_JSON}.bak"
  [[ -f "$BACKUP_JSON" ]] || error "No backup found at $BACKUP_JSON. Cannot restore original state."

  # Read original entry from backup
  ORIGINAL_ENTRY=$(jq -r --arg key "$PLUGIN_KEY" '.plugins[$key] // empty' "$BACKUP_JSON")
  [[ -z "$ORIGINAL_ENTRY" ]] && error "Plugin '$PLUGIN_KEY' not found in backup file."

  ORIGINAL_INSTALL_PATH=$(echo "$ORIGINAL_ENTRY" | jq -r '.[0].installPath')
  ORIGINAL_VERSION=$(echo "$ORIGINAL_ENTRY" | jq -r '.[0].version')

  # Remove symlink if current path is a symlink
  if [[ -L "$CURRENT_INSTALL_PATH" ]]; then
    rm "$CURRENT_INSTALL_PATH"
    info "Removed symlink: $CURRENT_INSTALL_PATH"
  else
    warn "Current install path is not a symlink: $CURRENT_INSTALL_PATH"
  fi

  # Restore backed-up cache directory if exists
  CURRENT_VERSION_FROM_JSON=$(jq -r --arg key "$PLUGIN_KEY" '.plugins[$key][0].version' "$INSTALLED_PLUGINS_JSON")
  BACKUP_CACHE="${CACHE_DIR}/${PLUGIN_NAME}/${CURRENT_VERSION_FROM_JSON}.bak"
  if [[ -d "$BACKUP_CACHE" ]]; then
    RESTORE_TARGET="${CACHE_DIR}/${PLUGIN_NAME}/${CURRENT_VERSION_FROM_JSON}"
    mv "$BACKUP_CACHE" "$RESTORE_TARGET"
    info "Restored cache: $BACKUP_CACHE -> $RESTORE_TARGET"
  fi

  # Restore installed_plugins.json from backup for this plugin entry
  TEMP_FILE=$(mktemp)
  jq --arg key "$PLUGIN_KEY" \
     --arg path "$ORIGINAL_INSTALL_PATH" \
     --arg ver "$ORIGINAL_VERSION" \
     '.plugins[$key][0].installPath = $path | .plugins[$key][0].version = $ver' \
     "$INSTALLED_PLUGINS_JSON" > "$TEMP_FILE"
  mv "$TEMP_FILE" "$INSTALLED_PLUGINS_JSON"
  info "Restored installed_plugins.json: installPath=$ORIGINAL_INSTALL_PATH, version=$ORIGINAL_VERSION"

  echo ""
  info "=== Unlink complete ==="
  info "Plugin '$PLUGIN_NAME' has been restored to original installed state."
  info "Restart Claude Code to apply changes."
}

case "$ACTION" in
  link)   do_link   ;;
  unlink) do_unlink ;;
esac
