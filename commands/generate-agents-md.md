---
description: Generate or update AGENTS.md for a project from codebase analysis or a brief
---

You are generating an AGENTS.md file for the current project. This file serves as the primary context document for AI coding agents working on this codebase.

## Steps

1. **Analyze the codebase**: Identify language, framework, build system, test runner, lint tools, and project structure.
2. **Detect conventions**: Read existing config files (package.json, Cargo.toml, go.mod, pyproject.toml, Makefile, etc.). Extract lint commands, test commands, build commands.
3. **Understand architecture**: Map the directory structure. Identify entry points, core modules, test directories, config locations.
4. **Generate AGENTS.md**: Write a concise document covering:
   - Project overview (what it does)
   - Tech stack and versions
   - Directory structure
   - Commands: build, test, lint, typecheck, dev server
   - Coding conventions observed in the codebase
   - Architecture decisions and patterns
   - Any project-specific rules or constraints
5. **Review**: Ensure the file is accurate, concise, and actionable.

## Context Management

- AGENTS.md is write-protected and persists across compaction. It's the most reliable place for project context.
- Keep AGENTS.md concise (under 150 lines). Dense, structured content survives compaction better.
- Use file:line references in AGENTS.md for large code pointers rather than inlining code.

## Rules

- Keep it under 150 lines. Be concise.
- Only include commands that actually work. Verify if uncertain.
- Follow conventions already present in the codebase.
- If an existing AGENTS.md exists, update it — don't overwrite from scratch unless the brief says so.
- No speculative content. Only document what exists.

## Output

Write the AGENTS.md to the project root. Confirm what was generated.
