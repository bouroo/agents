---
description: Stage changes and create a well-structured commit
---

You are creating a git commit for the current changes. Analyze the diff, stage appropriate files, and write a clear commit message.

## Arguments

$ARGUMENTS

## Context

Current status:
!`git status --short`

Staged changes:
!`git diff --cached --stat`

Unstaged changes:
!`git diff --stat`

Recent commit style:
!`git log --oneline -10 2>/dev/null || echo "No commits yet"`

## Steps

1. **Review changes**: Read the diff to understand what changed and why.

2. **Stage files**:
   - If `$ARGUMENTS` specifies files or a scope, stage only those.
   - If no arguments, stage all modified and new files.
   - Do NOT stage files that shouldn't be committed (secrets, large generated files, build artifacts).

3. **Write commit message**:
   - Follow the existing commit style from the log above.
   - If no clear style exists, use Conventional Commits: `type(scope): description`
   - Types: feat, fix, refactor, docs, test, chore, perf, ci, build
   - Keep the subject line under 72 characters.
   - If the change is complex, add a bullet-point body explaining what and why.

4. **Execute**: Run `git commit` with the message.

5. **Report**: Show the commit hash, files changed, and the message used.

## Rules

- Never commit secrets, API keys, or credentials.
- Never use `--no-verify` or `--force`.
- One logical change per commit. If changes are unrelated, suggest splitting.
- Don't push unless explicitly asked.
- If the working tree is clean, report that and stop.
