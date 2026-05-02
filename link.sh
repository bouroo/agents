#!/usr/bin/env bash

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

info()  { echo "[link] $*"; }
warn()  { echo "[link] WARNING: $*" >&2; }

symlink() {
    local src="$1" dst="$2"

    if [[ -L "$dst" && "$(readlink "$dst")" == "$src" ]]; then
        return 0
    fi

    if [[ -e "$dst" && ! -L "$dst" ]]; then
        warn "$dst exists as a real file/directory — skipping to avoid data loss"
        return 1
    fi

    rm -f "$dst" 2>/dev/null || true
    ln -sf "$src" "$dst"
    info "linked $dst -> $src"
}

link_configs() {
    local target_dir="$1"
    local agent_file="$2"
    local agents_dir="${3:-}"

    mkdir -p "$target_dir"

    symlink "$REPO_DIR/AGENTS.md" "$target_dir/$agent_file"
    symlink "$REPO_DIR/commands"  "$target_dir/commands"
    symlink "$REPO_DIR/skills"    "$target_dir/skills"

    if [[ -n "$agents_dir" ]]; then
        symlink "$REPO_DIR/agents" "$target_dir/$agents_dir"
    fi
}

unlink_configs() {
    local target_dir="$1"
    local agent_file="$2"
    local agents_dir="${3:-}"

    for path in "$target_dir/$agent_file" "$target_dir/commands" "$target_dir/skills"; do
        if [[ -L "$path" ]]; then
            rm -f "$path"
            info "removed $path"
        fi
    done

    if [[ -n "$agents_dir" && -L "$target_dir/$agents_dir" ]]; then
        rm -f "$target_dir/$agents_dir"
        info "removed $target_dir/$agents_dir"
    fi
}

status_configs() {
    local target_dir="$1"
    local agent_file="$2"
    local agents_dir="${3:-}"

    local base="$target_dir/$agent_file"
    if [[ -L "$base" ]]; then
        local dest
        dest="$(readlink "$base")"
        if [[ "$dest" == "$REPO_DIR/AGENTS.md" ]]; then
            echo "  OK  $base"
        else
            echo "  ??  $base -> $dest (not pointing to $REPO_DIR)"
        fi
    elif [[ -e "$base" ]]; then
        echo "  !!  $base exists but is not a symlink"
    else
        echo "  --  $base (not linked)"
    fi

    for name in commands skills; do
        local p="$target_dir/$name"
        if [[ -L "$p" && "$(readlink "$p")" == "$REPO_DIR/$name" ]]; then
            echo "  OK  $p"
        elif [[ -L "$p" ]]; then
            echo "  ??  $p -> $(readlink "$p")"
        elif [[ -e "$p" ]]; then
            echo "  !!  $p exists but is not a symlink"
        else
            echo "  --  $p (not linked)"
        fi
    done

    if [[ -n "$agents_dir" ]]; then
        local a="$target_dir/$agents_dir"
        if [[ -L "$a" && "$(readlink "$a")" == "$REPO_DIR/agents" ]]; then
            echo "  OK  $a"
        elif [[ -L "$a" ]]; then
            echo "  ??  $a -> $(readlink "$a")"
        elif [[ -e "$a" ]]; then
            echo "  !!  $a exists but is not a symlink"
        else
            echo "  --  $a (not linked)"
        fi
    fi
}

TARGETS=(
    "$HOME/.claude:CLAUDE.md:"
    "$HOME/.gemini:GEMINI.md:"
    "$HOME/.config/opencode:AGENTS.md:agents"
    "$HOME/.config/kilo:AGENTS.md:agent"
    "$HOME/.qwen:AGENTS.md:"
    "$HOME/.codex:AGENTS.md:"
    "$HOME/.cursor:CURSOR.md:"
)

ACTION="${1:-link}"

for target in "${TARGETS[@]}"; do
    IFS=':' read -r dir agent_file agents_dir <<< "$target"
    if [[ ! -d "$dir" ]]; then
        if [[ "$ACTION" == "link" ]]; then
            info "skipping $dir (directory does not exist)"
        fi
        continue
    fi
    case "$ACTION" in
        unlink)
            unlink_configs "$dir" "$agent_file" "$agents_dir"
            ;;
        status)
            echo "[$dir]"
            status_configs "$dir" "$agent_file" "$agents_dir"
            ;;
        link|"")
            link_configs "$dir" "$agent_file" "$agents_dir"
            ;;
        *)
            echo "Usage: $0 [link|unlink|status]"
            exit 1
            ;;
    esac
done

if [[ "$ACTION" != "status" ]]; then
    info "Done. Use '$0 status' to verify, '$0 unlink' to remove."
fi
