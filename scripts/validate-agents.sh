#!/usr/bin/env bash
# Thin shim: all validation lives in scripts/checks.py (single source).
#
# The previous 258-line bash implementation was a duplicate re-implementation of
# checks.py gates G3-G5 (frontmatter) and G9 (AGENTS.md line budget). Keeping
# two validators in two languages let them drift; this shim preserves the
# documented entrypoint name (README.md, CI) without forking the logic.
#
# Usage unchanged: bash scripts/validate-agents.sh [--all|--help]
set -euo pipefail
exec python3 "$(dirname "$0")/checks.py" "$@"
