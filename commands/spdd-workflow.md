---
description: Run the structured prompt-driven development (SPDD) workflow end to end
---

# SPDD Workflow

```
Story → Analysis → Canvas → Generate → Test → Review → Sync
```

Feature / story (from arguments, optional): **$ARGUMENTS**. If empty, ask the user for the one-sentence story before starting.

1. **Story** — capture the user problem in plain language; surface the problem, not the solution.
2. **Analysis** — identify entities, constraints, risks, and unknowns before writing anything.
3. **Canvas** — fill the REASONS canvas (R, E, A, S, O, N, S). Leave no section empty; mark unknowns explicitly.
4. **Generate** — write code from the spec, not intuition. Test-first, library-first, CLI-reachable.
5. **Test** — verify the code satisfies every canvas section. Tests are the executable spec.
6. **Review** — check for orphans (code without spec, spec without code) and constitutional gates.
7. **Sync** — land spec and code together; a stale spec is a bug.

## Bidirectional Sync Rule

- **Logic change** → update the spec first, then regenerate the code from the updated spec.
- **Refactor (no behavior change)** → update the code first, then sync the spec to describe the new shape.

Never merge one side without the other.
