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
#   agents/   -> agents/              (per-file agent definitions)
#
# The agents column declares the destination subdir, the formats the host
# accepts, and a copy flag. Syntax: <subdir>[:<fmt>...][:copy]
#   agents             dest subdir 'agents', format md (default), symlinked
#   agents:md          consume common/<base>.md, install as <base>.md
#   agents:md-plain    consume common/<base>.plain.md, install as <base>.md (the
#                      dest name strips '.plain'): the no-name variant, for hosts
#                      that reject a 'name:' key and derive the id from the filename
#   agents:toml:copy   consume common/<base>.toml, copied (host rejects symlinks)
#   -                  host has no agents surface
# A file agents/common/<f> applies to a host iff the host declares <f>'s format
# AND agents/<code>/<installed-name> does not exist (host-specific file wins by
# installed basename). Format 'md' never consumes a '*.plain.md' file; 'md-plain'
# consumes only '*.plain.md'.
# Host-specific files from agents/<code>/ install first, then common files.
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
AGENTS_COMMON_DIR="common"

log() { printf '%s\n' "$*" >&2; }

# Host table. Antigravity shares the gemini config dir, so it needs no own row.
# Format: code|config_dir|instruction_file|skills|commands|agents
#   surfaces are 1/0; agents declares the destination subdir, the accepted
#   formats, and a copy flag: <subdir>[:<fmt>...][:copy], or '-' for no surface.
#   Default format is md, so a bare 'agents' parses as agents + md.
#
# An empty instruction_file means the host has no global instruction surface:
# doctrine installs to the workspace instead (its rules file is project-level),
# and only the skills row applies. No current host leaves it empty.
HOSTS=(
  "gemini|$HOME/.gemini|GEMINI.md|1|1|agents:md"
  "codex|$HOME/.codex|AGENTS.md|1|1|agents:toml:copy"
  "claude|$HOME/.claude|CLAUDE.md|1|1|agents:md"
  "qwen|$HOME/.qwen|AGENTS.md|1|1|agents:md"
  "opencode|$HOME/.config/opencode|AGENTS.md|1|1|agents:md-plain"
  "kilo|$HOME/.config/kilo|AGENTS.md|1|1|agents:md-plain"
  "openclaw|$HOME/.openclaw/workspace|AGENTS.md|1|0|-"
  "hermes|$HOME/.hermes|SOUL.md|1|0|-"
  "pi|$HOME/.pi/agent|AGENTS.md|1|0|agents:md"
  "minimax|$HOME/.minimax|AGENTS.md|1|0|-"
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
    -h|--help) sed -n '2,44p' "${BASH_SOURCE[0]}"; exit 0 ;;
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

# parse_agents_spec <spec> - sets agents_dir, agents_copy, agents_formats.
#   spec: <subdir>[:<fmt>...][:copy] | -
parse_agents_spec() {
  local spec="$1" tok i
  agents_dir=""; agents_copy=0; agents_formats=""
  case "$spec" in
    -|"") return 0 ;;
  esac
  local _toks
  IFS=':' read -r -a _toks <<< "$spec"
  agents_dir="${_toks[0]}"
  for (( i=1; i<${#_toks[@]}; i++ )); do
    tok="${_toks[$i]}"
    case "$tok" in
      copy) agents_copy=1 ;;
      "") ;;
      *) agents_formats+=" $tok" ;;
    esac
  done
  [[ -n "$agents_formats" ]] || agents_formats=" md"
}

agents_has_format() { # <ext>
  local ext="$1" f
  for f in $agents_formats; do [[ "$f" == "$ext" ]] && return 0; done
  return 1
}

# common_map <code> <basename> - echo the installed basename for common/<basename>
# on this host, or return 1 if it does not apply. A '*.plain.md' file is the
# no-name variant (format md-plain) installed as '<base>.md'.
common_map() {
  local code="$1" base="$2" fmt dest
  [[ -n "$agents_dir" ]] || return 1
  if [[ "$base" == *.plain.md ]]; then
    fmt="md-plain"; dest="${base%.plain.md}.md"
  else
    fmt="${base##*.}"
    [[ "$fmt" == "$base" ]] && return 1
    dest="$base"
  fi
  agents_has_format "$fmt" || return 1
  [[ -e "$REPO_DIR/agents/$code/$dest" ]] && return 1
  printf '%s\n' "$dest"
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
  agents_spec="$(field 6 "$h")"
  parse_agents_spec "$agents_spec"
  [[ -n "$instr" ]] && has_instr=1 || has_instr=0

  case "$MODE" in

  detect)
    [[ -d "$cdir" ]] && log "detected: $code ($cdir)"
    ;;

  list)
    log "$code | $(field 2 "$h") | instruction=${instr:-(none: project-level only)} | skills=$has_skills | commands=$has_cmds | agents=${agents_spec:--}"
    ;;

  install)
    log "== $code =="
    if [[ ! -d "$cdir" && "$ALL" != "1" ]]; then
      log "  not detected (use --all to create $cdir)"
      continue
    fi
    [[ "$has_instr" == "1" ]] && place "$REPO_DIR/$MANIFESTO" "$cdir/$instr" "$MANIFESTO->$instr"
    [[ "$has_skills" == "1" ]] && place "$REPO_DIR/$SKILLS_DIR" "$cdir/$SKILLS_DIR" "$SKILLS_DIR/"
    [[ "$has_cmds" == "1" ]] && place "$REPO_DIR/$COMMANDS_DIR" "$cdir/$COMMANDS_DIR" "$COMMANDS_DIR/"
    if [[ -n "$agents_dir" ]]; then
      if [[ -d "$REPO_DIR/agents/$code" ]]; then
        for f in "$REPO_DIR/agents/$code"/*; do
          [[ -e "$f" ]] || continue
          place "$f" "$cdir/$agents_dir/$(basename "$f")" "agents/$(basename "$f")" "$agents_copy"
        done
      fi
      for f in "$REPO_DIR/agents/$AGENTS_COMMON_DIR"/*; do
        [[ -e "$f" ]] || continue
        base="$(basename "$f")"
        dest="$(common_map "$code" "$base")" || continue
        place "$f" "$cdir/$agents_dir/$dest" "agents/$AGENTS_COMMON_DIR/$base" "$agents_copy"
      done
    fi
    ;;

  uninstall)
    log "== $code =="
    [[ "$has_instr" == "1" ]] && remove_one "$cdir/$instr" "$instr"
    remove_one "$cdir/$SKILLS_DIR" "$SKILLS_DIR/"
    remove_one "$cdir/$COMMANDS_DIR" "$COMMANDS_DIR/"
    if [[ -n "$agents_dir" ]]; then
      if [[ -d "$REPO_DIR/agents/$code" ]]; then
        for f in "$REPO_DIR/agents/$code"/*; do
          [[ -e "$f" ]] || continue
          remove_one "$cdir/$agents_dir/$(basename "$f")" "agents/$(basename "$f")"
        done
      fi
      for f in "$REPO_DIR/agents/$AGENTS_COMMON_DIR"/*; do
        [[ -e "$f" ]] || continue
        base="$(basename "$f")"
        dest="$(common_map "$code" "$base")" || continue
        remove_one "$cdir/$agents_dir/$dest" "agents/$AGENTS_COMMON_DIR/$base"
      done
    fi
    ;;

  status)
    if [[ ! -d "$cdir" ]]; then log "$code: absent (no $cdir)"; continue; fi
    out=""
    for entry in "$instr:$cdir/$instr" "$SKILLS_DIR:$cdir/$SKILLS_DIR" "$COMMANDS_DIR:$cdir/$COMMANDS_DIR"; do
      name="${entry%%:*}"
      dest="${entry#*:}"
      [[ -n "$name" ]] || continue
      if ours "$dest"; then s="ok"
      elif [[ -L "$dest" ]]; then s="stale"
      elif [[ -e "$dest" ]]; then s="real"
      else s="-"; fi
      out+=" $name=$s"
    done
    as="-"  # agents: meaningful only when the host declares an agents surface
    if [[ -n "$agents_dir" ]]; then
      atotal=0; aours=1; alink=0; areal=0
      if [[ -d "$REPO_DIR/agents/$code" ]]; then
        for f in "$REPO_DIR/agents/$code"/*; do
          [[ -e "$f" ]] || continue
          atotal=1
          d="$cdir/$agents_dir/$(basename "$f")"
          ours "$d" || aours=0
          [[ -L "$d" ]] && alink=1
          [[ -e "$d" || -L "$d" ]] && areal=1
        done
      fi
      for f in "$REPO_DIR/agents/$AGENTS_COMMON_DIR"/*; do
        [[ -e "$f" ]] || continue
        base="$(basename "$f")"
        dest="$(common_map "$code" "$base")" || continue
        atotal=1
        d="$cdir/$agents_dir/$dest"
        ours "$d" || aours=0
        [[ -L "$d" ]] && alink=1
        [[ -e "$d" || -L "$d" ]] && areal=1
      done
      if [[ "$atotal" == "1" ]]; then
        if [[ "$aours" == "1" ]]; then as="ok"
        elif [[ "$alink" == "1" ]]; then as="stale"
        elif [[ "$areal" == "1" ]]; then as="real"
        else as="-"; fi
      fi
    fi
    out+=" agents=$as"
    log "$code:$out"
    ;;
  esac
done

if [[ "$MODE" == "detect" && ${#FILTERS[@]} -eq 0 ]]; then
  log "tip: run '$0 install' to install into every detected tool"
fi
exit 0
