#!/usr/bin/env bash
#
# install.sh - detect AI coding tools on this machine and install the shared
# setup into each one's configuration directory. The core doctrine is
# host-agnostic; ONLY this script knows concrete hosts. Its knowledge lives in
# the HOSTS table below: adding a harness is one line here.
#
# Per host it installs:
#   AGENTS.md -> <instruction file>   (the manifesto, renamed per host)
#   skills/   -> skills/              (whole directory, when the host has one)
#   commands/ -> commands/            (when the host surfaces custom commands)
#
# Usage:
#   install.sh detect               show every compatible tool found on this machine
#   install.sh list                 show every supported tool in the table
#   install.sh install [<code>...]  install; default = all DETECTED tools
#   install.sh uninstall [<code>...]  remove what we installed (symlinks pointing
#                                   into this repo; real files need --force)
#   install.sh status               state of every artifact on every tool
#
# Options:
#   --all       include undetected tools too (creates their config dirs)
#   --copy      copy artifacts instead of symlinking (updates do not propagate;
#               re-run install --force --copy to refresh)
#   --force     replace foreign symlinks / refresh copies / uninstall real files
#   --dry-run   print planned actions without touching anything
#   -h          this help
#
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFESTO="AGENTS.md"
SKILLS_DIR="skills"
COMMANDS_DIR="commands"

log() { printf '%s\n' "$*" >&2; }

# Host table. Antigravity shares the gemini config dir, so it needs no own row.
# Format: code|config_dir|instruction_file|skills|commands   (surfaces 1/0)
HOSTS=(
  "gemini|$HOME/.gemini|GEMINI.md|1|1"
  "codex|$HOME/.codex|AGENTS.md|1|1"
  "claude|$HOME/.claude|CLAUDE.md|1|1"
  "qwen|$HOME/.qwen|AGENTS.md|1|1"
  "opencode|$HOME/.config/opencode|AGENTS.md|1|1"
  "kilo|$HOME/.config/kilo|AGENTS.md|1|1"
  "openclaw|$HOME/.openclaw/workspace|AGENTS.md|1|0"
  "hermes|$HOME/.hermes|SOUL.md|1|0"
  "pi|$HOME/.pi/agent|AGENTS.md|1|0"
)

MODE="detect"
DRY_RUN=0; FORCE=0; COPY=0; ALL=0; FILTERS=()

for arg in "$@"; do
  case "$arg" in
    detect|list|install|uninstall|status) MODE="$arg" ;;
    --dry-run) DRY_RUN=1 ;;
    --force) FORCE=1 ;;
    --copy) COPY=1 ;;
    --all) ALL=1 ;;
    -h|--help) sed -n '2,34p' "${BASH_SOURCE[0]}"; exit 0 ;;
    -*) log "error: unknown option $arg"; exit 2 ;;
    *) FILTERS+=("$arg") ;;
  esac
done

expand_home() { printf '%s' "${1//\$HOME/$HOME}"; }
field() { printf '%s' "$2" | cut -d'|' -f"$1"; }

selected_hosts() {
  local h code wanted dir f
  for h in "${HOSTS[@]}"; do
    code="$(field 1 "$h")"
    raw_dir="$(field 2 "$h")"
    dir="$(expand_home "$raw_dir")"
    wanted=0
    if [[ ${#FILTERS[@]} -gt 0 ]]; then
      for f in "${FILTERS[@]}"; do [[ "$f" == "$code" ]] && wanted=1; done
    elif [[ "$ALL" == "1" || "$MODE" == "uninstall" || "$MODE" == "status" ]]; then
      wanted=1
    else
      [[ -d "$dir" ]] && wanted=1
    fi
    [[ "$wanted" == "1" ]] && printf '%s\n' "$h"
  done
}

ours() { # dest is a symlink pointing inside this repo
  [[ -L "$1" ]] || return 1
  case "$(readlink "$1")" in
    "$REPO_DIR"|"$REPO_DIR"/*) return 0 ;;
    *) return 1 ;;
  esac
}

# place <source-abs> <dest> <label>
place() {
  local src="$1" dest="$2" label="$3"
  if [[ ! -e "$src" ]]; then log "  ($label) SKIP: source missing: $src"; return 0; fi
  if [[ -L "$dest" ]]; then
    local cur; cur="$(readlink "$dest")"
    if [[ "$cur" == "$src" && "$COPY" == "0" ]]; then log "  ($label) already linked"; return 0; fi
    if [[ "$FORCE" != "1" ]]; then log "  ($label) SKIP unmanaged link $dest -> $cur (use --force)"; return 0; fi
    [[ "$DRY_RUN" == "1" ]] || rm -f "$dest"
  elif [[ -e "$dest" ]]; then
    if [[ "$COPY" == "1" && "$FORCE" == "1" ]]; then
      [[ "$DRY_RUN" == "1" ]] || rm -rf "$dest"
    else
      log "  ($label) SKIP real file/dir $dest (never clobbered)"; return 0
    fi
  fi
  mkdir -p "$(dirname "$dest")"
  if [[ "$COPY" == "1" ]]; then
    [[ "$DRY_RUN" == "1" ]] && { log "  ($label) copy -> $dest"; return 0; }
    cp -R "$src" "$dest"
    log "  ($label) copied -> $dest"
  else
    [[ "$DRY_RUN" == "1" ]] && { log "  ($label) link $dest -> $src"; return 0; }
    ln -s "$src" "$dest"
    log "  ($label) linked $dest"
  fi
}

# remove_one <dest> <label>
remove_one() {
  local dest="$1" label="$2"
  if ours "$dest"; then
    [[ "$DRY_RUN" == "1" ]] || rm -f "$dest"
    log "  ($label) removed link $dest"
  elif [[ -e "$dest" ]]; then
    if [[ "$FORCE" == "1" ]]; then
      [[ "$DRY_RUN" == "1" ]] || rm -rf "$dest"
      log "  ($label) removed $dest (--force)"
    else
      log "  ($label) SKIP real/copied $dest (use --force)"
    fi
  fi
}

for h in $(selected_hosts); do
  code="$(field 1 "$h")"
  raw_cdir="$(field 2 "$h")"
  cdir="$(expand_home "$raw_cdir")"
  instr="$(field 3 "$h")"
  has_skills="$(field 4 "$h")"
  has_cmds="$(field 5 "$h")"

  case "$MODE" in

  detect)
    [[ -d "$cdir" ]] && log "detected: $code ($cdir)"
    ;;

  list)
    log "$code | $(field 2 "$h") | instruction=$(field 3 "$h") | skills=$has_skills | commands=$has_cmds"
    ;;

  install)
    log "== $code =="
    if [[ ! -d "$cdir" && "$ALL" != "1" ]]; then
      log "  not detected (use --all to create $cdir)"
      continue
    fi
    place "$REPO_DIR/$MANIFESTO" "$cdir/$instr" "$MANIFESTO->$instr"
    [[ "$has_skills" == "1" ]] && place "$REPO_DIR/$SKILLS_DIR" "$cdir/$SKILLS_DIR" "$SKILLS_DIR/"
    [[ "$has_cmds" == "1" ]] && place "$REPO_DIR/$COMMANDS_DIR" "$cdir/$COMMANDS_DIR" "$COMMANDS_DIR/"
    ;;

  uninstall)
    log "== $code =="
    remove_one "$cdir/$instr" "$instr"
    remove_one "$cdir/$SKILLS_DIR" "$SKILLS_DIR/"
    remove_one "$cdir/$COMMANDS_DIR" "$COMMANDS_DIR/"
    ;;

  status)
    if [[ ! -d "$cdir" ]]; then log "$code: absent (no $cdir)"; continue; fi
    out=""
    for entry in "$instr:$cdir/$instr" "$SKILLS_DIR:$cdir/$SKILLS_DIR" "$COMMANDS_DIR:$cdir/$COMMANDS_DIR"; do
      name="${entry%%:*}"
      dest="${entry#*:}"
      if ours "$dest"; then s="ok"
      elif [[ -L "$dest" ]]; then s="stale"
      elif [[ -e "$dest" ]]; then s="real"
      else s="-"; fi
      out+=" $name=$s"
    done
    log "$code:$out"
    ;;
  esac
done

if [[ "$MODE" == "detect" && ${#FILTERS[@]} -eq 0 ]]; then
  log "tip: run '$0 install' to install into every detected tool"
fi
exit 0
