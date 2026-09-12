---
name: cmd-document
description: "Bootstrap or sync a repo's docs/ tree (systems, flows, ADRs, API endpoints, glossary) with code changes. Use when a behavior, interface, invariant, or domain-term change must be reflected in project documentation."
---

# Document - Sync docs/ With Code

Docs and code must agree; a stale doc is a bug. Documentation is a **Spec**-stage artifact (§4) that tracks the code through Build and Test — bootstrap a `docs/` tree where none exists, sync an existing one, and run it as an execution graph inside that stage (§4.2). One well-written doc beats many shallow ones.

## Target

The area to document (`auth`, `email-verification flow`, `sessions-vs-tokens ADR`). **Empty -> detect from `git diff` / `git diff --cached`** and document what changed. `--type=<system|flow|adr|api|glossary>` pins the doc type; without it, infer from the target and ask only if genuinely ambiguous.

## Doc types

| Type | Covers | Lives at |
| --- | --- | --- |
| system | one subsystem's responsibilities and boundaries | `docs/systems/<system>.md` |
| flow | a cross-system runtime path | `docs/flows/<flow>.md` |
| adr | one architecture decision, immutable once accepted | `docs/architecture/decisions/<slug>.md` |
| api | one HTTP endpoint: contract, auth, errors, sequence | `docs/api/<service>/<endpoint>.md` |
| glossary term | a Title Case domain concept | entry in `CONTEXT.md` at the repo root; format: [domain-modeling](../skills/domain-modeling/SKILL.md) |

Document as a system until it crosses systems; then promote to a flow.

## Steps

1. **Assess** — no `docs/` tree: bootstrap the minimal layout (`docs/README.md` index, `systems/`, `flows/`, `architecture/decisions/`, `api/`; the glossary lives at the repo root as `CONTEXT.md`, created lazily on the first resolved term). Present: use it as-is — never rearrange someone's tree.
2. **Locate** — read the index/map; find the affected system doc, related flows, endpoint pages, governing ADRs, and glossary terms, and decide honestly whether the change needs a new doc or an edit to an existing one.
3. **Draft** — each doc states purpose, inputs/outputs, key invariants, and a source map (the code paths that implement it) so readers can navigate both directions. Mark unresolved points `[NEEDS CLARIFICATION]`; never invent content.
4. **Sync surroundings** — a new Title Case term -> a `CONTEXT.md` entry (opinionated definition + `_Avoid_` list); a new flow -> linked from its systems and the index; an accepted ADR -> propagate consequences into affected docs; any docs-vs-code disagreement -> update whichever side is wrong, or flag the gap explicitly.
5. **Verify** — every relative link resolves; ADR frontmatter valid; the repo gate is green.

## ADR lifecycle

Proposed -> Accepted. An Accepted ADR is **never rewritten** — supersede it with `status: Superseded` plus `superseded_by: <file>`. Frontmatter requires `status` (allowed value), `date` (`YYYY-MM-DD`), and context + decision + consequences sections.

## Done =

- Every relative link in new/updated docs and their source maps resolves.
- ADR frontmatter valid; superseded entries carry a real `superseded_by`.
- The repo's own gate (formatter / link-check / markdown lint / tests) exits zero — noted as absent if none ships.

**Hand back when:** the named area cannot be located or inferred from the diff; docs contradict verified code and cannot be reconciled in scope.
