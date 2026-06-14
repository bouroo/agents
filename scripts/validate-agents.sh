#!/usr/bin/env bash
set -euo pipefail

# Static validation for opencode-format artifacts in the repo.
# No build tool exists; this script is the verification gate.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$REPO/skills"
COMMANDS_DIR="$REPO/commands"
AGENTS_DIR="$REPO/agents"
AGENTS_MD="$REPO/AGENTS.md"

PASS=0
FAIL=0

# Print a failure message and exit immediately.
fail() {
    echo "[FAIL] $1" >&2
    exit 1
}

# Print a pass message.
pass() {
    echo "[PASS] $1"
    PASS=$((PASS + 1))
}

# Extract frontmatter block (lines between 1st and 2nd ^---$).
frontmatter() {
    awk '
        /^---$/ {
            count++
            if (count == 1) next
            if (count == 2) exit
        }
        count == 1 { print }
    ' "$1"
}

# Validate all skills.
validate_skills() {
    if [ ! -d "$SKILLS_DIR" ]; then
        return 0
    fi

    for skill_dir in "$SKILLS_DIR"/*/; do
        [ -d "$skill_dir" ] || continue
        name="$(basename "$skill_dir")"
        skill_file="$skill_dir/SKILL.md"

        if [ ! -f "$skill_file" ]; then
            fail "skill $name: SKILL.md missing"
        fi

        # Frontmatter present.
        fm="$(frontmatter "$skill_file")"
        if [ -z "$fm" ]; then
            fail "skill $name: frontmatter missing"
        fi

        # name field exists and equals directory basename.
        fm_name="$(echo "$fm" | awk '/^name:/ { sub(/^name:[[:space:]]*/, ""); print; exit }')"
        if [ -z "$fm_name" ]; then
            fail "skill $name: name field missing"
        fi
        if [ "$fm_name" != "$name" ]; then
            fail "skill $name: name '$fm_name' does not match directory '$name'"
        fi

        # name matches regex.
        if ! printf '%s' "$fm_name" | grep -Eq '^[a-z0-9]+(-[a-z0-9]+)*$'; then
            fail "skill $name: name '$fm_name' does not match required pattern"
        fi

        # description field exists and length 1..1024.
        desc="$(echo "$fm" | awk '
            /^description:/ {
                found = 1
                # Remove key label.
                sub(/^description:[[:space:]]*/, "")
                line = $0
                # If block scalar indicator, strip it and any leading indent.
                if (line ~ /^>[[:space:]]*/) {
                    sub(/^>[[:space:]]*/, "", line)
                }
                desc = line
                # Read subsequent lines until next top-level key or EOF.
                while ((getline nextline) > 0) {
                    # Top-level key (no leading spaces) or closing marker already
                    # consumed by frontmatter extraction.
                    if (nextline ~ /^[A-Za-z0-9_-]+:/) break
                    # Continuation line: strip leading whitespace/block markers.
                    cleaned = nextline
                    sub(/^[[:space:]]+/, "", cleaned)
                    if (desc == "") {
                        desc = cleaned
                    } else {
                        desc = desc " " cleaned
                    }
                }
                print desc
                exit
            }
        ')"
        if [ -z "$desc" ]; then
            fail "skill $name: description missing"
        fi
        len="${#desc}"
        if [ "$len" -lt 1 ] || [ "$len" -gt 1024 ]; then
            fail "skill $name: description length $len not in 1..1024"
        fi

        pass "skill $name: frontmatter ok"
    done
}

# Validate all commands.
validate_commands() {
    if [ ! -d "$COMMANDS_DIR" ]; then
        return 0
    fi

    allowed_keys="description agent subtask model template"

    for cmd_file in "$COMMANDS_DIR"/*.md; do
        [ -f "$cmd_file" ] || continue
        name="$(basename "$cmd_file" .md)"

        fm="$(frontmatter "$cmd_file")"
        if [ -z "$fm" ]; then
            fail "command $name: frontmatter missing"
        fi

        desc="$(echo "$fm" | awk '/^description:/ { print; exit }')"
        if [ -z "$desc" ]; then
            fail "command $name: description missing"
        fi

        # Check for unknown top-level frontmatter keys.
        unknown="$(echo "$fm" | awk -v allowed="$allowed_keys" '
            BEGIN { split(allowed, arr, " "); for (i in arr) ok[arr[i]] = 1 }
            /^[A-Za-z0-9_-]+:/ {
                key = $0
                sub(/:.*$/, "", key)
                if (!(key in ok)) print key
            }
        ')"
        if [ -n "$unknown" ]; then
            fail "command $name: unknown key(s): $(echo "$unknown" | tr "\n" " ")"
        fi

        pass "command $name"
    done
}

# Validate all agents.
validate_agents() {
    if [ ! -d "$AGENTS_DIR" ]; then
        return 0
    fi

    allowed_modes="primary subagent all"
    allowed_permissions="read edit glob grep list bash task external_directory todowrite webfetch websearch lsp skill question doom_loop"

    for agent_file in "$AGENTS_DIR"/*.md; do
        [ -f "$agent_file" ] || continue
        name="$(basename "$agent_file" .md)"

        fm="$(frontmatter "$agent_file")"
        if [ -z "$fm" ]; then
            fail "agent $name: frontmatter missing"
        fi

        desc="$(echo "$fm" | awk '/^description:/ { print; exit }')"
        if [ -z "$desc" ]; then
            fail "agent $name: description missing"
        fi

        # mode validation (optional).
        mode="$(echo "$fm" | awk '/^mode:/ { sub(/^mode:[[:space:]]*/, ""); print; exit }')"
        if [ -n "$mode" ]; then
            found=0
            for m in $allowed_modes; do
                if [ "$m" = "$mode" ]; then
                    found=1
                    break
                fi
            done
            if [ "$found" -ne 1 ]; then
                fail "agent $name: invalid mode '$mode'"
            fi
        fi

        # permission sub-keys.
        perm_keys="$(echo "$fm" | awk '
            /^permission:/ {
                # Read lines until next top-level key or EOF.
                while ((getline line) > 0) {
                    # Stop at next top-level key or end of frontmatter already handled.
                    if (line ~ /^[A-Za-z0-9_-]+:/) exit
                    # Capture two-space-indented keys.
                    if (line ~ /^  [A-Za-z0-9_-]+:/) {
                        key = line
                        sub(/^  /, "", key)
                        sub(/:.*$/, "", key)
                        print key
                    }
                }
                exit
            }
        ')"
        for key in $perm_keys; do
            found=0
            for p in $allowed_permissions; do
                if [ "$p" = "$key" ]; then
                    found=1
                    break
                fi
            done
            if [ "$found" -ne 1 ]; then
                fail "agent $name: unknown permission '$key'"
            fi
        done

        pass "agent $name"
    done
}

# Validate AGENTS.md router budget.
validate_agents_md() {
    if [ ! -f "$AGENTS_MD" ]; then
        fail "AGENTS.md: file missing"
    fi

    lines="$(wc -l < "$AGENTS_MD" | tr -d ' ')"
    if [ "$lines" -gt 200 ]; then
        fail "AGENTS.md: $lines lines (> 200)"
    fi

    pass "AGENTS.md: $lines lines (≤ 200)"
}

# Main.
validate_skills
validate_commands
validate_agents
validate_agents_md

TOTAL=$((PASS + FAIL))
echo "All checks passed ($TOTAL artifacts)."
exit 0
