---
name: commit-message
description: "Generate a Conventional Commit message from staged git changes. Use when asked to write a commit message, generate a commit, or summarize staged changes."
---

# Commit Message Generator

Generate Conventional Commits from staged diffs -- durable decision records the loop writes during PROVE/GROW.

> **Override.** A repo-level commit convention (Angular-style, emoji-prefix, a `COMMIT.md`) that explicitly supersedes Conventional Commits wins; match the repo's existing log before inventing a style.

**Stance:** write for the reviewer skimming the log six months from now. Each entry answers *what changed for the reader* -- internal refactors with no user-visible impact belong in the body, not the headline.

## Inputs

- `$ARGUMENTS` (optional): caller hints that override inference from the diff.
  - `--type=<feat|fix|perf|refactor|...>` -- force the commit type instead of classifying the dominant change.
  - `--scope=<area>` -- force the scope; must match a real area in the repo, else omit.
- If empty, classify type and scope from `git diff --cached` (current behavior).
- Parsing `$ARGUMENTS` is this skill's job -- the host only forwards the string. See [command inputs](../harness-engineering/references/agent-computer-interface.md).

## Format

```
<type>(<scope>): <description>     <- headline, imperative mood, <=72 chars, lowercase, no trailing period

<body>                             <- wrapped at 72; explains what + why, not how

<footer>                           <- BREAKING CHANGE: ..., Co-authored-by, issue refs
```

## Types

| Type | When | Bump |
|---|---|---|
| `feat` | New feature (user-visible) | MINOR |
| `fix` | Bug fix / error correction | PATCH |
| `perf` | Performance improvement | PATCH |
| `refactor` | Code change that neither fixes a bug nor adds a feature | none |
| `docs` | Documentation only | none |
| `test` | Adding or correcting tests | none |
| `build` | Build system, dependencies, tooling | none |
| `ci` | CI config and scripts | none |
| `chore` | Maintenance, releases, housekeeping | none |
| `revert` | Reverting a prior commit | undo prior bump |

**Breaking change:** add `!` after type/scope (`feat!:`) and a `BREAKING CHANGE: <what + migration>` footer. Consumers and SemVer tooling detect it.

## Steps

1. `git diff --cached` -- read the staged change; if nothing staged, say so and stop.
2. Classify the dominant change into one type; if `$ARGUMENTS` set `--type`, use it (validate it matches the diff -- do not claim `fix` for a change that adds behavior). If it spans many, split into one commit per logical change (each rolls back cleanly alone).
3. Write the headline: imperative mood, lowercase first word, specific (not "update code"), <=72 chars, no trailing period. If `$ARGUMENTS` set `--scope`, use it; otherwise use the repo's existing area name, or omit scope if none fits.
4. Write the body: *what* and *why*, not *how* (the diff shows how). Wrap at 72.
5. Add a footer for breaking changes and attribution.

## Common mistakes

| Mistake | Fix |
|---|---|
| Capitalized, period-terminated headline | Lowercase first letter, no trailing period; <=72 chars |
| Vague description ("update code") | Name the specific change |
| Inventing a scope that does not exist | Use the repo's existing area name; omit scope if none fits |
| Many unrelated changes in one commit | Split into one commit per logical change |
| Breaking change without `!` / footer | Mark it explicitly for SemVer tooling |
| Body restates the diff | Body explains what + why, not how |
| Body wraps past 72 | Wrap at 72 for narrow terminals |

## References

- [code-craft](../code-craft/SKILL.md) -- INTENT/TWINS/AUTH/PENDING artifact gates.
- [harness-engineering](../harness-engineering/SKILL.md) -- decision-log discipline, repo-as-record.
