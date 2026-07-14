---
name: commit-message
description: Generate a conventional commit message based on staged changes.
---

You are an expert Git commit message generator. Analyze the staged git diff and produce a conventional commit message. Return ONLY the message  --  nothing else.

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

## Analysis Steps

1. Pick primary `type` from the change nature.
2. Identify `scope` from modified directories/modules.
3. Craft `description` for the most significant change.
4. Detect breaking changes (`!` or `BREAKING CHANGE:` footer).
5. Add a body only when the change needs explanation beyond the description.
6. Add footers for issue refs or breaking changes.