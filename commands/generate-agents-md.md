---
description: Generate or update AGENTS.md for a project
---

Generate or update an `AGENTS.md` file for this project. Execute the full workflow without stopping for confirmation.

$ARGUMENTS

## Instructions

If `$ARGUMENTS` is empty:
1. Scan the project structure: directories, key files, config files
2. Identify the language, framework, build system, test runner, linter
3. Read existing instruction files (CONTRIBUTING.md, .cursor/rules, etc.)
4. Generate the `AGENTS.md` file

If `$ARGUMENTS` is provided:
1. Use the provided brief as the basis for the AGENTS.md
2. Still scan the project to validate and supplement the brief
3. Generate the AGENTS.md following the same structure

**Do not stop to ask what to include.** Scan, analyze, and write the file autonomously.

## AGENTS.md Structure

```markdown
# Project Name

One-line description.

## Project Structure
- `dir/` — purpose

## Commands
- Build: `cmd`
- Test: `cmd`
- Lint: `cmd`

## Conventions
- Pattern 1
- Pattern 2
```

Keep it concise — AGENTS.md should be scannable in under 2 minutes. Focus on what an AI agent needs to be effective.

## Rules

- Write the file. Do not output the content and ask for approval.
- If an AGENTS.md already exists, update it — do not create a second file.
- Preserve any existing sections that are still accurate.
- Remove sections that no longer apply after scanning.