#!/usr/bin/env bash

set -euo pipefail

link_configs() {
    local target_dir="$1"
    local agent_file="$2"
    local agents_dir="$3"

    mkdir -p "$target_dir"

    rm -f "$target_dir/commands"
    rm -f "$target_dir/skills"

    ln -sf ~/.agents/AGENTS.md "$target_dir/$agent_file"
    ln -sf ~/.agents/commands "$target_dir/commands"
    ln -sf ~/.agents/skills "$target_dir/skills"

    if [[ -n "$agents_dir" ]]; then
        local agents_path="$target_dir/$agents_dir"
        if [[ -e "$agents_path" && ! -L "$agents_path" ]]; then
            echo "WARNING: $agents_path exists as a real directory — skipping agents symlink to avoid data loss" >&2
        else
            rm -f "$agents_path" 2>/dev/null || true
            ln -sf ~/.agents/agents "$agents_path"
        fi
    fi
}

declare -a TARGETS=(
    "$HOME/.claude:CLAUDE.md:"
    "$HOME/.gemini:GEMINI.md:"
    "$HOME/.config/opencode:AGENTS.md:agents"
    "$HOME/.config/kilo:AGENTS.md:agent"
    "$HOME/.qwen:AGENTS.md:"
)

for target in "${TARGETS[@]}"; do
    IFS=':' read -r dir agent_file agents_dir <<< "$target"
    link_configs "$dir" "$agent_file" "$agents_dir"
done
