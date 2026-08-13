#!/usr/bin/env bash
#
# install.sh: install this repo into supported AI tools.
#
# The host list is NOT hardcoded here. It is read from registries/hosts.json
# (the host-adapter registry) via python3, which this repo already requires.
# Adding a host = adding an entry to registries/hosts.json; no change here.
#
# Per adapter, symlinks into the host's config dir:
#   AGENTS.md   -> config_file   (GEMINI.md / CLAUDE.md / AGENTS.md)
#   skills/     -> skills/        (when surfaces.skills)
#   commands/   -> commands/      (when surfaces.commands)
#   agents/     -> agents_path    (when surfaces.agents; e.g. agents/ or agent/)
#   references/ -> references/    (when surfaces.agents; depth docs loaded by agents)
#
# agents/ and commands/ ship in each host's NATIVE format: flat <name>.md files
# (opencode/kilo discover agents/<name>.md and commands/<name>.md). claude is
# excluded from the agents surface: its subagent frontmatter (name/description/
# tools/model) differs from the opencode-native format in agents/, so symlinking
# would conflict. claude still gets skills/ and commands/.
# skills/ ship nested skills/<name>/SKILL.md (the Agent Skills standard).
#
# Modes:
#   install.sh install           # link all adapters (default)
#   install.sh uninstall         # remove symlinks
#   install.sh status            # show link state
#   install.sh list              # list adapters from the registry
# Options: --dry-run  --force  <adapter-code>
#
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOSTS_REG="$REPO_DIR/registries/hosts.json"
DOCTRINE="AGENTS.md"

log() { printf '%s\n' "$*" >&2; }

if ! command -v python3 >/dev/null 2>&1; then
  log "error: python3 is required (used to read registries/hosts.json)"
  exit 1
fi
if [[ ! -f "$HOSTS_REG" ]]; then
  log "error: registry not found: $HOSTS_REG"
  exit 1
fi

# Emit adapter rows: code|config_dir|config_file|skills|commands|agents|ref|agents_path
# $HOME stays literal here; expanded per-row below without eval.
# `ref` is the agents surface gate: progressive-disclosure depth docs in
# references/ are only useful to a host that also consumes the agents/ surface.
read_registry() {
  python3 -c '
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
for a in d.get("adapters", []):
    s = a.get("surfaces", {})
    ap = s.get("agents_path") or ""
    ag = bool(s.get("agents"))
    print("|".join([
        a.get("code", ""),
        a.get("config_dir", ""),
        a.get("config_file", ""),
        "1" if s.get("skills") else "0",
        "1" if s.get("commands") else "0",
        "1" if ag else "0",
        "1" if ag else "0",
        ap,
    ]))
' "$HOSTS_REG"
}

MODE="install"
DRY_RUN=0
FORCE=0
FILTER=""
for arg in "$@"; do
  case "$arg" in
    install|uninstall|status|list) MODE="$arg" ;;
    --dry-run) DRY_RUN=1 ;;
    --force) FORCE=1 ;;
    -h|--help)
      sed -n '2,28p' "${BASH_SOURCE[0]}"
      exit 0
      ;;
    *) FILTER="$arg" ;;
  esac
done

expand_home() { printf '%s' "${1//\$HOME/$HOME}"; }

link_artifact() {
  local src="$1" dest="$2" label="$3"
  if [[ -L "$dest" ]]; then
    local cur; cur="$(readlink "$dest")"
    if [[ "$FORCE" == "1" ]]; then
      if [[ "$DRY_RUN" == "1" ]]; then log "  ($label) replace symlink $dest"; else rm "$dest"; fi
    elif [[ "$cur" == "$src" || "$cur" == "$REPO_DIR/$src" ]]; then
      log "  ($label) already linked"
      return 0
    else
      log "  ($label) SKIP: $dest is a symlink elsewhere -> $cur (use --force to replace)"
      return 0
    fi
  elif [[ -e "$dest" ]]; then
    log "  ($label) SKIP: $dest exists and is a real file/dir (not clobbered)"
    return 0
  fi
  if [[ "$DRY_RUN" == "1" ]]; then
    log "  ($label) link $dest -> $src"
  else
    mkdir -p "$(dirname "$dest")"
    ln -s "$src" "$dest"
    log "  ($label) linked $dest"
  fi
}

unlink_artifact() {
  local dest="$1" label="$2"
  if [[ -L "$dest" ]]; then
    if [[ "$DRY_RUN" == "1" ]]; then log "  ($label) remove symlink $dest"; else rm "$dest"; fi
    log "  ($label) removed $dest"
  elif [[ -e "$dest" ]]; then
    log "  ($label) SKIP: $dest is real (not a symlink); not removed"
  else
    log "  ($label) absent"
  fi
}

status_artifact() {
  local src="$1" dest="$2" label="$3"
  if [[ -L "$dest" ]]; then
    local cur; cur="$(readlink "$dest")"
    if [[ "$cur" == "$src" || "$cur" == "$REPO_DIR/$src" ]]; then
      log "  ($label) OK -> $src"
    else
      log "  ($label) STALE -> $cur (expected $src)"
    fi
  elif [[ -e "$dest" ]]; then
    log "  ($label) REAL-FILE (not a symlink) at $dest"
  else
    log "  ($label) not installed"
  fi
}

if [[ "$MODE" == "list" ]]; then
  log "Adapters from registries/hosts.json:"
  while IFS='|' read -r code config_dir config_file sk cmd ag rf ap; do
    printf '  %-16s %s  (%s)%s%s\n' "$code" "$config_dir" "$config_file" \
      "$([[ "$ag" == "1" ]] && printf ' agents->%s' "$ap")" \
      "$([[ "$rf" == "1" ]] && printf ' refs' )"
  done < <(read_registry)
  exit 0
fi

log "mode=$MODE dry-run=$DRY_RUN force=$FORCE${FILTER:+ filter=$FILTER}"

while IFS='|' read -r code config_dir config_file sk cmd ag rf ap; do
  [[ -n "$code" ]] || continue
  if [[ -n "$FILTER" && "$code" != "$FILTER" ]]; then continue; fi
  dir="$(expand_home "$config_dir")"
  log "[$code] -> $dir"
  case "$MODE" in
    install)
      link_artifact "$REPO_DIR/$DOCTRINE" "$dir/$config_file" "doctrine"
      [[ "$sk" == "1" ]] && link_artifact "$REPO_DIR/skills" "$dir/skills" "skills"
      [[ "$cmd" == "1" ]] && link_artifact "$REPO_DIR/commands" "$dir/commands" "commands"
      [[ "$ag" == "1" && -n "$ap" ]] && link_artifact "$REPO_DIR/agents" "$dir/$ap" "agents"
      # Progressive-disclosure depth docs (references/) sit alongside
      # agents/; only link them when the host consumes the agents surface,
      # so the cross-refs from each agent contract resolve at runtime.
      [[ "$rf" == "1" ]] && link_artifact "$REPO_DIR/references" "$dir/references" "references"
      # Migrate installs made before claude dropped the agents surface: a
      # pre-3.4.2 `install claude` left ~/.claude/agents symlinked to this
      # repo's opencode-native agents/, which conflicts with claude's own
      # subagent frontmatter. Remove that stale symlink now; never touch a
      # real dir the user owns; only a symlink we created.
      [[ "$code" == "claude" && -L "$dir/agents" ]] && unlink_artifact "$dir/agents" "agents-legacy"
      ;;
    uninstall)
      unlink_artifact "$dir/$config_file" "doctrine"
      [[ "$sk" == "1" ]] && unlink_artifact "$dir/skills" "skills"
      [[ "$cmd" == "1" ]] && unlink_artifact "$dir/commands" "commands"
      [[ "$ag" == "1" && -n "$ap" ]] && unlink_artifact "$dir/$ap" "agents"
      [[ "$rf" == "1" ]] && unlink_artifact "$dir/references" "references"
      # Same legacy cleanup on uninstall: the flag is off now, so the normal
      # path above skips ~/.claude/agents, but a stale symlink may remain.
      [[ "$code" == "claude" && -L "$dir/agents" ]] && unlink_artifact "$dir/agents" "agents-legacy"
      ;;
    status)
      status_artifact "$REPO_DIR/$DOCTRINE" "$dir/$config_file" "doctrine"
      [[ "$sk" == "1" ]] && status_artifact "$REPO_DIR/skills" "$dir/skills" "skills"
      [[ "$cmd" == "1" ]] && status_artifact "$REPO_DIR/commands" "$dir/commands" "commands"
      [[ "$ag" == "1" && -n "$ap" ]] && status_artifact "$REPO_DIR/agents" "$dir/$ap" "agents"
      [[ "$rf" == "1" ]] && status_artifact "$REPO_DIR/references" "$dir/references" "references"
      ;;
  esac
done < <(read_registry)

case "$MODE" in
  install) log "summary: install finished; pass '$0 status' to verify" ;;
  uninstall) log "summary: uninstall finished; pass '$0 status' to verify" ;;
esac
[[ "$DRY_RUN" == "1" ]] && log "(--dry-run: no filesystem changes were made)"
exit 0
