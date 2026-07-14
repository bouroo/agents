#!/usr/bin/env bash
#
# install.sh  --  install this repo as a plugin into supported AI tools.
#
# Complementary to link.sh: link.sh is the lightweight symlink path,
# install.sh is the plugin-marketplace path. Both coexist.
#
# Per detected tool, links the plugin artifacts into the tool's config dir:
#   AGENTS.md  -> tool-specific filename (GEMINI.md / CLAUDE.md / AGENTS.md)
#   commands/  -> commands/
#   skills/    -> skills/
#   agents/    -> tool-specific agents dir (agents/ or agent/) for opencode/kilo
#
# Modes:
#   install.sh install           # link all detected tools (default)
#   install.sh uninstall         # remove symlinks
#   install.sh status            # show current linkage state
#   install.sh list              # list detected tools + target paths
#
# Options:
#   --dry-run                    # print actions without executing
#   --force                      # replace stale symlinks (NEVER clobber real files)
#   <tool-name>                  # last arg: filter to a single tool
#
# Tools supported (mirrors link.sh TARGETS exactly):
#   gemini, antigravity, antigravity-ide  -> ~/.gemini/GEMINI.md
#   codex                                  -> ~/.codex/AGENTS.md
#   claude                                 -> ~/.claude/CLAUDE.md
#   qwen                                   -> ~/.qwen/AGENTS.md
#   opencode                               -> ~/.config/opencode/AGENTS.md (agents -> agents/)
#   kilo                                   -> ~/.config/kilo/AGENTS.md    (agents -> agent/)
#
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

ACTION="install"
FILTER=""
DRY_RUN="0"
FORCE="0"

usage() {
  cat <<'USAGE'
Usage: install.sh [install|uninstall|status|list] [--dry-run] [--force] [tool-name]

Modes:
  install     link plugin artifacts into every detected tool (default)
  uninstall   remove the symlinks previously created
  status      show current linkage state for detected tools
  list        list detected tools and their target paths (no changes)

Options:
  --dry-run   print actions without executing them
  --force     replace a stale symlink (never overwrite a real file/dir)

Tool filter:
  <tool-name> apply the action to a single tool only
  (gemini, antigravity, antigravity-ide, codex, claude, qwen, opencode, kilo)
USAGE
}

for arg in "$@"; do
  case "$arg" in
    install|uninstall|status|list)
      ACTION="$arg"
      ;;
    --dry-run)
      DRY_RUN="1"
      ;;
    --force)
      FORCE="1"
      ;;
    -h|--help|help)
      usage
      exit 0
      ;;
    gemini|antigravity|antigravity-ide|codex|claude|qwen|opencode|kilo)
      FILTER="$arg"
      ;;
    *)
      echo "install.sh: unknown argument: $arg" >&2
      usage
      exit 1
      ;;
  esac
done

log()  { echo "[install] $*"; }
warn() { echo "[install] WARNING: $*" >&2; }
dry()  { echo "[install] (dry-run) $*"; }

TARGETS=(
  "gemini:$HOME/.gemini:GEMINI.md:"
  "antigravity:$HOME/.gemini:GEMINI.md:"
  "antigravity-ide:$HOME/.gemini:GEMINI.md:"
  "codex:$HOME/.codex:AGENTS.md:"
  "claude:$HOME/.claude:CLAUDE.md:"
  "qwen:$HOME/.qwen:AGENTS.md:"
  "opencode:$HOME/.config/opencode:AGENTS.md:agents"
  "kilo:$HOME/.config/kilo:AGENTS.md:agent"
)

# What we ship from the plugin
PLUGIN_FILE="AGENTS.md"
PLUGIN_DIRS=(commands skills)
PLUGIN_AGENTS_DIR="agents"

# link a single src -> dst artifact (file or dir)
# uses symlinks by default to stay idempotent and easy to update.
link_artifact() {
  local src="$1"
  local dst="$2"
  local label="$3"

  if [[ ! -e "$src" && ! -L "$src" ]]; then
    warn "source $src missing  --  cannot link"
    return 1
  fi

  if [[ -L "$dst" ]]; then
    local current
    current="$(readlink "$dst")"
    if [[ "$current" == "$src" ]]; then
      log "tool already linked ($label)"
      return 0
    fi
    if [[ "$FORCE" == "1" ]]; then
      if [[ "$DRY_RUN" == "1" ]]; then
        dry "replace stale symlink $dst (currently -> $current) -> $src"
      else
        rm -f "$dst"
        ln -s "$src" "$dst"
      fi
      log "linked $dst -> $src"
      return 0
    fi
    warn "$dst is a symlink to $current (not $src); pass --force to replace"
    return 1
  fi

  if [[ -e "$dst" ]]; then
    warn "$dst exists as a real file/directory  --  skipping to avoid data loss"
    return 1
  fi

  if [[ "$DRY_RUN" == "1" ]]; then
    dry "link $dst -> $src"
  else
    ln -s "$src" "$dst"
  fi
  log "linked $dst -> $src"
}

unlink_artifact() {
  local dst="$1"

  if [[ -L "$dst" ]]; then
    if [[ "$DRY_RUN" == "1" ]]; then
      dry "remove symlink $dst (-> $(readlink "$dst"))"
    else
      rm -f "$dst"
      log "removed $dst"
    fi
  elif [[ -e "$dst" ]]; then
    warn "$dst exists but is not a symlink  --  leaving alone"
  fi
}

# format the status of a single artifact: OK / stale symlink / real block / missing
status_one() {
  local src="$1" dst="$2"

  if [[ -L "$dst" ]]; then
    local dest
    dest="$(readlink "$dst")"
    if [[ "$dest" == "$src" ]]; then
      echo "  OK    $dst"
    else
      echo "  ??    $dst -> $dest (expected $src)"
    fi
  elif [[ -e "$dst" ]]; then
    echo "  !!    $dst exists but is not a symlink"
  else
    echo "  --    $dst (not linked)"
  fi
}

install_tool() {
  local name="$1" dir="$2" agent_file="$3" agents_dir="$4"

  if [[ ! -d "$dir" ]]; then
    log "$dir does not exist  --  skipping $name"
    return 0
  fi

  mkdir -p "$dir"

  local updated=0
  local skipped=0

  if [[ "$DRY_RUN" != "1" ]]; then
    log "tool $name: linking into $dir"
  else
    dry "tool $name: would link into $dir"
  fi

  if link_artifact "$REPO_DIR/$PLUGIN_FILE" "$dir/$agent_file" "config"; then
    updated=$((updated + 1))
  else
    skipped=$((skipped + 1))
  fi

  local d
  for d in "${PLUGIN_DIRS[@]}"; do
    if link_artifact "$REPO_DIR/$d" "$dir/$d" "$d/"; then
      updated=$((updated + 1))
    else
      skipped=$((skipped + 1))
    fi
  done

  if [[ -n "$agents_dir" ]]; then
    if link_artifact "$REPO_DIR/$PLUGIN_AGENTS_DIR" "$dir/$agents_dir" "agents/"; then
      updated=$((updated + 1))
    else
      skipped=$((skipped + 1))
    fi
  fi

  TOOL_UPDATED="$updated"
  TOOL_SKIPPED="$skipped"
}

uninstall_tool() {
  local name="$1" dir="$2" agent_file="$3" agents_dir="$4"

  if [[ ! -d "$dir" ]]; then
    log "$dir does not exist  --  nothing to remove for $name"
    return 0
  fi

  log "tool $name: removing links from $dir"

  unlink_artifact "$dir/$agent_file"
  local d
  for d in "${PLUGIN_DIRS[@]}"; do
    unlink_artifact "$dir/$d"
  done
  if [[ -n "$agents_dir" ]]; then
    unlink_artifact "$dir/$agents_dir"
  fi
}

status_tool() {
  local name="$1" dir="$2" agent_file="$3" agents_dir="$4"

  echo "[$name]"

  if [[ ! -d "$dir" ]]; then
    echo "  --    $dir (config directory does not exist)"
    return 0
  fi

  status_one "$REPO_DIR/$PLUGIN_FILE" "$dir/$agent_file"
  local d
  for d in "${PLUGIN_DIRS[@]}"; do
    status_one "$REPO_DIR/$d" "$dir/$d"
  done
  if [[ -n "$agents_dir" ]]; then
    status_one "$REPO_DIR/$PLUGIN_AGENTS_DIR" "$dir/$agents_dir"
  fi
}

list_tool() {
  local name="$1" dir="$2" agent_file="$3" agents_dir="$4"

  local present="no"
  [[ -d "$dir" ]] && present="yes"
  printf "  %-18s  config=%s  config_file=%-12s  detected=%s" \
    "$name" "$dir" "$agent_file" "$present"
  if [[ -n "$agents_dir" ]]; then
    printf "  agents_dir=%s" "$agents_dir"
  fi
  echo ""
}

UPDATED=0
SKIPPED=0
DETECTED=0
TOOL_UPDATED=0
TOOL_SKIPPED=0

for target in "${TARGETS[@]}"; do
  IFS=':' read -r name dir agent_file agents_dir <<< "$target"

  if [[ -n "$FILTER" && "$name" != "$FILTER" ]]; then
    continue
  fi

  case "$ACTION" in
    list)
      list_tool "$name" "$dir" "$agent_file" "$agents_dir"
      if [[ -d "$dir" ]]; then
        DETECTED=$((DETECTED + 1))
      fi
      ;;
    install)
      TOOL_UPDATED=0
      TOOL_SKIPPED=0
      install_tool "$name" "$dir" "$agent_file" "$agents_dir"
      UPDATED=$((UPDATED + TOOL_UPDATED))
      SKIPPED=$((SKIPPED + TOOL_SKIPPED))
      if [[ -d "$dir" ]]; then
        DETECTED=$((DETECTED + 1))
      fi
      ;;
    uninstall)
      uninstall_tool "$name" "$dir" "$agent_file" "$agents_dir"
      ;;
    status)
      status_tool "$name" "$dir" "$agent_file" "$agents_dir"
      if [[ -d "$dir" ]]; then
        DETECTED=$((DETECTED + 1))
      fi
      ;;
    *)
      usage
      exit 1
      ;;
  esac
done

case "$ACTION" in
  list)
    if [[ "$DETECTED" -eq 0 ]]; then
      echo ""
      echo "no tools detected (none of the supported config directories exist on this machine)"
    else
      echo ""
      echo "$DETECTED tool(s) detected"
    fi
    ;;
  install)
    echo ""
    log "summary: $UPDATED artifact(s) updated, $SKIPPED skipped across $DETECTED tool(s) detected"
    if [[ "$FORCE" == "1" ]]; then
      log "(--force enabled: stale symlinks were replaced)"
    fi
    if [[ "$DRY_RUN" == "1" ]]; then
      log "(--dry-run: no filesystem changes were made)"
    fi
    ;;
  uninstall)
    log "summary: uninstall finished; pass '$0 status' to verify"
    if [[ "$DRY_RUN" == "1" ]]; then
      log "(--dry-run: no filesystem changes were made)"
    fi
    ;;
  status)
    : # no summary
    ;;
esac

exit 0
