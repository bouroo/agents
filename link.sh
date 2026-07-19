#!/usr/bin/env bash
#
# link.sh  --  thin compatibility shim over install.sh.
#
# All symlink logic has been consolidated into install.sh. This script exists
# for backward compatibility with the documented CLI:
#
#   link.sh [link|unlink|status] [tool-name]
#
# It translates the legacy verbs and execs install.sh with the same arguments
# install.sh accepts natively:
#
#   link         -> install       (default when no action verb is given)
#   unlink       -> uninstall
#   status       -> status
#   list         -> list          (forwarded, install.sh-native)
#
# Tool filters (gemini, antigravity, antigravity-ide, codex, claude, qwen,
# opencode, kilo) and the flags --dry-run, --force, -h|--help|help are
# passed through unchanged. Install.sh owns TARGETS, idempotency, dry-run,
# and the summary line; this shim owns only the verb translation.
#
# For the canonical installer documentation see install.sh --help.
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_SH="$SCRIPT_DIR/install.sh"

if [[ ! -x "$INSTALL_SH" && ! -f "$INSTALL_SH" ]]; then
  echo "[link] install.sh not found at $INSTALL_SH" >&2
  exit 1
fi

# Translate the first positional action verb (link/unlink) to install.sh's
# vocabulary (install/uninstall). status/list/help pass through verbatim.
# Anything else (a bare tool name, --flag, or empty) is forwarded untouched
# so install.sh's default action (install) and its own arg parser take over.
translate_and_exec() {
  local -a forwarded=()
  local first="${1:-}"
  case "$first" in
    link)    forwarded+=("install");  shift ;;
    unlink)  forwarded+=("uninstall"); shift ;;
    status|list|-h|--help|help) forwarded+=("$first"); shift ;;
    "")      : ;;  # no action -> install.sh defaults to install
    *)       forwarded+=("$first"); shift ;;  # bare tool name or flag
  esac
  forwarded+=("$@")
  exec "$INSTALL_SH" "${forwarded[@]}"
}

translate_and_exec "$@"
