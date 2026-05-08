---
description: Generate or update AGENTS.md for a project from codebase analysis or a brief
---

You are generating or updating an AGENTS.md — the primary project context document for AI coding agents.

## Target
$ARGUMENTS

## Sources
!`find . -maxdepth 3 -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/vendor/*' -not -path '*/__pycache__/*' -not -path '*/.venv/*' -not -path '*/target/*' -not -path '*/dist/*' -not -path '*/.next/*' | head -80`
@AGENTS.md

## Steps

1. **Detect stack**: Identify language, framework, build/test/lint tools from config files (package.json, Cargo.toml, go.mod, pyproject.toml, Makefile, .eslintrc, etc.).
2. **Map architecture**: Identify entry points, core modules, test directories, config locations. Build a simple directory tree if non-obvious.
3. **Extract conventions**: Parse config files for actual commands (not assumed defaults). Note any project-specific rules.
4. **Update existing AGENTS.md** — preserve structure, merge changes, do not overwrite unless brief says to.
5. **Write or update** a concise AGENTS.md (under 150 lines) covering:
   - Project overview and tech stack
   - Directory structure with purpose annotations
   - Commands: build, test, lint, typecheck, dev
   - Coding conventions observed (naming, patterns, error handling)
   - Architecture decisions and key file:line pointers

## Embedded Principles

- **Specs as first-class artifacts**: AGENTS.md is version-controlled, reviewed, not throwaway
- **REASONS-aligned**: Surface Requirements, Entities, Approach, Structure, Operations, Norms, Safeguards
- **Iterative update**: Modify existing AGENTS.md rather than overwriting; sync spec ↔ code on changes
- **Write for reading**: Dense, scannable sections; consistent naming; file:line pointers for large code
- **No speculative content**: Only document what exists — verified commands, actual conventions
- **Decouple from environment**: Detect from configs, not hardcoded assumptions

## Rules

- Under 150 lines total. Be dense but scannable.
- Only include verified working commands. Skip assumed defaults.
- Use file:line references for large code sections instead of inlining.
- If AGENTS.md exists above, update it — never overwrite unless brief explicitly says so.
- Persist AGENTS.md across compaction — it is the reliable context anchor.

## Output

Write the AGENTS.md to the project root. Confirm what was generated or updated.