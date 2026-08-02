---
name: commit-message
description: Generate a conventional commit message based on staged changes in the PROVE and GROW phases. Use this skill when asked to write a commit message, generate a commit, or summarize staged git changes.
---

# Commit Message Generator

Generate Conventional Commits based on staged git diffs, serving as durable decision records across the THINK→ACT→PROVE→GROW loop.

> **Override.** A repo-level commit convention (e.g. `COMMIT.md`, Angular-style, emoji-prefix) that explicitly supersedes Conventional Commits takes precedence; match the repo's existing log before inventing a style.

**Stance:** You write the commit message for the reviewer skimming the log six months from now. Each entry answers *what changed for the reader* -- internal refactors without user-visible impact belong in the body, not the headline.

---

## Conventional Commits Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

| Type | Use for | SemVer |
|---|---|---|
| `feat` | New feature or functionality | MINOR |
| `fix` | Bug fix or error correction | PATCH |
| `docs` | Documentation only |  --  |
| `style` | Whitespace, formatting, semicolons |  --  |
| `refactor` | Code change with no feature/fix |  --  |
| `perf` | Performance improvement |  --  |
| `test` | Adding or fixing tests |  --  |
| `build` | Build system or external dependency changes |  --  |
| `ci` | CI/CD configuration changes |  --  |
| `chore` | Maintenance, tooling |  --  |
| `revert` | Reverting a previous commit |  --  |

### Scope

- Parens: `feat(api):`, `fix(ui):`. Common: `api`, `ui`, `auth`, `db`, `config`, `deps`, `docs`.
- Monorepos: package or module name. Keep concise and lowercase.

### Description

- Imperative mood (`add`, not `added`/`adds`); lowercase first letter; no trailing period.
- Max 72 chars. Concise but descriptive.

### Body (optional)

- Blank line after description, then explain *what* and *why*, not *how*.
- Wrap at 72 chars; use for complex changes needing rationale.

### Footer (optional)

- Blank line after body.
- Breaking change: `BREAKING CHANGE: description` (or `!` after type/scope).
- Issue refs: `Refs: #123`, `Closes: #456`.
- Artifact gates: include `INTENT:`, `TWINS:`, `AUTH:`, or `PENDING:` lines where applicable per PROVE phase requirements.

---

## Analysis Steps

1. Pick primary `type` from the change nature.
2. Identify `scope` from modified directories/modules.
3. Craft `description` for the most significant change.
4. Detect breaking changes (`!` or `BREAKING CHANGE:` footer).
5. Add a body only when the change needs explanation beyond the description.
6. Add footers for issue refs, breaking changes, or artifact gate lines.

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| `feat` for an internal refactor with no user-visible change | Use `refactor`; reserve `feat`/`fix` for changes the consumer observes |
| Description in past tense (`added`, `fixed`) | Imperative mood (`add`, `fix`) -- the commit describes what applying it does |
| Description capitalized and period-terminated | Lowercase first letter, no trailing period; max 72 chars |
| Vague description (`update code`, `misc fixes`) | Name the specific change; the reader skims the log, not the diff |
| Inventing a scope that does not exist in the repo | Use the package/module/area name already in use; omit scope if none fits |
| Mixing many unrelated changes in one commit | Split into one commit per logical change; each commit should roll back cleanly on its own |
| Breaking change without `!` or `BREAKING CHANGE:` footer | Mark it explicitly so consumers and tooling (SemVer bump) can detect it |
| Body restating the diff | Body explains *what* and *why*, not *how*; the diff already shows how |
| Body wraps at >72 chars | Wrap at 72; reviewers read logs in narrow terminals |

---

## Cross-References

- [effective-code-craft](../effective-code-craft/SKILL.md) -- Intent, Twin, Auth, and Pending artifact gates
- [harness-engineering](../harness-engineering/SKILL.md) -- decision log discipline and repo-as-record

