#!/usr/bin/env bash
#
# install.sh - detect AI coding tools on this machine and install the shared
# setup into each one's configuration directory. The core method is
# host-agnostic; ONLY this script knows concrete hosts. Its knowledge lives in
# the HOSTS table below: adding a harness is one line here.
#
# Per host it installs:
#   AGENTS.md -> <instruction file>   (the entry point, renamed per host)
#   skills/ -> skills/                (whole-directory link: git pull in this
#                                      repo updates the host, new skills
#                                      included. A host whose skills/ holds
#                                      foreign entries gets per-skill links
#                                      instead so nothing is shadowed; content
#                                      still updates on pull, new skills need
#                                      an install re-run. Dot-directories never
#                                      ship as skills.)
#
# Host table format: code|config_dir|instruction_file|skills
#   skills is 1/0. An empty instruction_file means the host has no global
#   instruction surface, so doctrine installs to the workspace instead and only
#   the skills row applies. No current host leaves it empty.
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

log() { printf '%s\n' "$*" >&2; }

# Host table. Antigravity shares the gemini config dir, so it needs no own row.
# Format: code|config_dir|instruction_file|skills
HOSTS=(
  "gemini|$HOME/.gemini|GEMINI.md|1"
  "codex|$HOME/.codex|AGENTS.md|1"
  "claude|$HOME/.claude|CLAUDE.md|1"
  "qwen|$HOME/.qwen|AGENTS.md|1"
  "opencode|$HOME/.config/opencode|AGENTS.md|1"
  "kilo|$HOME/.config/kilo|AGENTS.md|1"
  "openclaw|$HOME/.openclaw/workspace|AGENTS.md|1"
  "hermes|$HOME/.hermes|SOUL.md|1"
  "pi|$HOME/.pi/agent|AGENTS.md|1"
  "omp|$HOME/.omp/agent|AGENTS.md|1"
  "minimax|$HOME/.minimax|AGENTS.md|1"
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
    -h|--help) awk 'NR > 1 && /^#/ { print; next } NR > 1 { exit }' "${BASH_SOURCE[0]}"; exit 0 ;;
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
    dir="$(expand_home "$(field 2 "$h")")"
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
  local src="$1" dest="$2" label="$3" copy="${4:-$COPY}"
  if [[ ! -e "$src" ]]; then log "  ($label) SKIP: source missing: $src"; return 0; fi
  if [[ -L "$dest" ]]; then
    local cur; cur="$(readlink "$dest")"
    if [[ "$cur" == "$src" && "$copy" == "0" ]]; then log "  ($label) already linked"; return 0; fi
    if [[ "$FORCE" != "1" ]]; then log "  ($label) SKIP unmanaged link $dest -> $cur (use --force)"; return 0; fi
    [[ "$DRY_RUN" == "1" ]] || rm -f "$dest"
  elif [[ -e "$dest" ]]; then
    if [[ "$copy" == "1" && "$FORCE" == "1" ]]; then
      [[ "$DRY_RUN" == "1" ]] || rm -rf "$dest"
    else
      log "  ($label) SKIP real file/dir $dest (never clobbered)"; return 0
    fi
  fi
  mkdir -p "$(dirname "$dest")"
  if [[ "$copy" == "1" ]]; then
    [[ "$DRY_RUN" == "1" ]] && { log "  ($label) copy -> $dest"; return 0; }
    cp -R "$src" "$dest"
    log "  ($label) copied -> $dest"
  else
    [[ "$DRY_RUN" == "1" ]] && { log "  ($label) link $dest -> $src"; return 0; }
    ln -s "$src" "$dest"
    log "  ($label) linked $dest"
  fi
}

# skill_dirs - the skill directories this repository actually ships, used for
# per-skill placement, migration, uninstall and status. A dot-directory under
# skills/ is machine-local runtime state (a coding CLI drops its own skills
# into skills/.system/), never doctrine: keep it untracked (see .gitignore),
# since a whole-dir link exposes everything in the directory.
skill_dirs() {
  local d
  for d in "$REPO_DIR/$SKILLS_DIR"/*/; do
    [[ -d "$d" ]] || continue
    [[ "$(basename "$d")" == .* ]] && continue
    printf '%s\n' "${d%/}"
  done
}

# place_skills <skills-dir> - link the whole repository skills/ directory when
# the target is absent, a link, or a real dir holding only our own artifacts
# (per-skill links are migrated away first). One directory link means git pull
# updates the host with no re-run, new skills included. When the dir holds
# foreign entries (the host's own skills, a CLI's skills/.system/ state), a
# whole-dir link would shadow them, so fall back to per-skill placement.
place_skills() {
  local dest_dir="$1" src entry foreign
  if [[ -d "$dest_dir" && ! -L "$dest_dir" ]]; then
    foreign=0
    while IFS= read -r entry; do
      ours "$entry" || foreign=1
    done < <(find "$dest_dir" -mindepth 1 -maxdepth 1)
    if [[ "$foreign" == "1" ]]; then
      log "  ($SKILLS_DIR/) $dest_dir holds foreign entries: per-skill links (a dir link would shadow them)"
      while IFS= read -r src; do
        place "$src" "$dest_dir/$(basename "$src")" "$SKILLS_DIR/$(basename "$src")"
      done < <(skill_dirs)
      return 0
    fi
    if [[ "$DRY_RUN" == "1" ]]; then
      log "  ($SKILLS_DIR/) link $dest_dir -> $REPO_DIR/$SKILLS_DIR (replaces real dir)"
      return 0
    fi
    while IFS= read -r entry; do
      rm -f "$entry"
    done < <(find "$dest_dir" -mindepth 1 -maxdepth 1)
    rmdir "$dest_dir"
  fi
  place "$REPO_DIR/$SKILLS_DIR" "$dest_dir" "$SKILLS_DIR/"
}

# remove_skills <skills-dir> - remove our whole-dir link, or our per-skill
# links (fallback/legacy), then the directory itself only when nothing else
# (a user's own skill) remains.
remove_skills() {
  local dest_dir="$1" src
  if [[ -L "$dest_dir" ]]; then
    remove_one "$dest_dir" "$SKILLS_DIR/"
    return 0
  fi
  while IFS= read -r src; do
    remove_one "$dest_dir/$(basename "$src")" "$SKILLS_DIR/$(basename "$src")"
  done < <(skill_dirs)
  if [[ -d "$dest_dir" && ! -L "$dest_dir" ]]; then
    [[ "$DRY_RUN" == "1" ]] || rmdir "$dest_dir" 2>/dev/null || true
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
  cdir="$(expand_home "$(field 2 "$h")")"
  instr="$(field 3 "$h")"
  has_skills="$(field 4 "$h")"
  [[ -n "$instr" ]] && has_instr=1 || has_instr=0

  case "$MODE" in

  detect)
    [[ -d "$cdir" ]] && log "detected: $code ($cdir)"
    ;;

  list)
    log "$code | $(field 2 "$h") | instruction=${instr:-(none: project-level only)} | skills=$has_skills"
    ;;

  install)
    log "== $code =="
    if [[ ! -d "$cdir" && "$ALL" != "1" ]]; then
      log "  not detected (use --all to create $cdir)"
      continue
    fi
    [[ "$has_instr" == "1" ]] && place "$REPO_DIR/$MANIFESTO" "$cdir/$instr" "$MANIFESTO->$instr"
    [[ "$has_skills" == "1" ]] && place_skills "$cdir/$SKILLS_DIR"
    ;;

  uninstall)
    log "== $code =="
    [[ "$has_instr" == "1" ]] && remove_one "$cdir/$instr" "$instr"
    [[ "$has_skills" == "1" ]] && remove_skills "$cdir/$SKILLS_DIR"
    ;;

  status)
    if [[ ! -d "$cdir" ]]; then log "$code: absent (no $cdir)"; continue; fi
    out=""
    entries=("$instr:$cdir/$instr")
    for entry in "${entries[@]}"; do
      name="${entry%%:*}"
      dest="${entry#*:}"
      [[ -n "$name" ]] || continue
      if ours "$dest"; then s="ok"
      elif [[ -L "$dest" ]]; then s="stale"
      elif [[ -e "$dest" ]]; then s="real"
      else s="-"; fi
      out+=" $name=$s"
    done
    # Skills: a whole-dir link into this repo is the desired state (ok); a
    # real dir reports how many shipped skills are linked per-skill (fallback
    # for hosts that keep their own entries in skills/).
    sk_dest="$cdir/$SKILLS_DIR"
    if [[ -L "$sk_dest" ]]; then
      if ours "$sk_dest"; then out+=" $SKILLS_DIR=ok"
      else out+=" $SKILLS_DIR=stale"; fi
    elif [[ -d "$sk_dest" ]]; then
      sk_total=0; sk_ok=0
      while IFS= read -r src; do
        sk_total=$((sk_total + 1))
        ours "$sk_dest/$(basename "$src")" && sk_ok=$((sk_ok + 1))
      done < <(skill_dirs)
      if [[ "$sk_total" == "0" ]]; then out+=" $SKILLS_DIR=-"
      elif [[ "$sk_ok" == "$sk_total" ]]; then out+=" $SKILLS_DIR=per-skill ($sk_ok/$sk_total)"
      elif [[ "$sk_ok" == "0" ]]; then out+=" $SKILLS_DIR=foreign"
      else out+=" $SKILLS_DIR=partial ($sk_ok/$sk_total)"; fi
    else
      out+=" $SKILLS_DIR=-"
    fi
    log "$code:$out"
    ;;
  esac
done

if [[ "$MODE" == "detect" && ${#FILTERS[@]} -eq 0 ]]; then
  log "tip: run '$0 install' to install into every detected tool"
fi
exit 0