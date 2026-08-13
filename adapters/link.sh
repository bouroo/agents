#!/usr/bin/env bash
#
# link.sh: backward-compat shim that execs install.sh (verb translation).
#
# Legacy vocabulary:   link     -> install       |  unlink  -> uninstall
#                      status                      |  list / help  pass through
# Extra args (tool filter, --dry-run, --force) are passed through unchanged.
#
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cmd=""
rest=()
for a in "$@"; do
  case "$a" in
    link) cmd="install" ;;
    unlink) cmd="uninstall" ;;
    install|uninstall|status|list) cmd="$a" ;;
    *) rest+=("$a") ;;
  esac
done
[[ -n "$cmd" ]] || cmd="install"

exec "$HERE/install.sh" "$cmd" "${rest[@]+"${rest[@]}"}"
