---
description: Initialize AI coding config for a new or existing project
subtask: true
---

You are initializing this project for AI-assisted development. Set up the configuration files that help AI agents work effectively on this codebase.

## Context

Project root contents:
!`ls -la`

Project structure:
!`find . -maxdepth 3 -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/vendor/*' -not -path '*/__pycache__/*' -not -path '*/.venv/*' -not -path '*/target/*' -not -path '*/dist/*' | head -80`

Git info:
!`git log --oneline -5 2>/dev/null && git remote -v 2>/dev/null || echo "Not a git repo"`

## Steps

1. **Detect project type**: Identify language, framework, build tool, and package manager from config files.

2. **Create AGENTS.md**: Generate a concise project context document covering:
   - What the project does
   - Tech stack and versions
   - Directory structure with purpose of each top-level dir
   - Commands: build, test, lint, typecheck, dev server, deploy
   - Key architecture decisions
   - Coding conventions found in the codebase

   Keep it under 150 lines. Only include verified commands.

3. **Create .gitignore entries**: If common AI artifacts aren't ignored, suggest additions (e.g., `.opencode/`, `.kilo/`).

4. **Summary**: Report what was created and any next steps.

## Rules

- Only create AGENTS.md. Don't create other config files unless explicitly asked.
- Don't modify existing working configuration.
- Verify commands before documenting them. If uncertain, note them as unverified.
- Follow conventions already present in the codebase.
- No speculative content.
