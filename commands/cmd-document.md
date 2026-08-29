---
name: cmd-document
description: "Bootstrap or sync a repo's docs/ tree (systems, flows, ADRs, API endpoints, glossary) with code changes. Use when a behavior, interface, invariant, or domain-term change must be reflected in project documentation."
---

# Document - Sync docs/ With Code

Docs and code must agree; a stale doc is a bug. Bootstraps a `docs/` tree where none exists and keeps an existing one synchronized inside the THINK-ACT-PROVE-GROW loop. One well-written doc beats many shallow ones.

## Target

Argument: the area to document (`auth`, `email-verification flow`, `sessions-vs-tokens ADR`). If empty, detect from `git diff` / `git diff --cached` and document what changed. Option `--type=<system|flow|adr|api|glossary>` pins the doc type; without it, infer the type from the target and ask only if genuinely ambiguous.

## Doc types

| Type | Covers | Lives at |
| --- | --- | --- |
| system | one subsystem's responsibilities and boundaries | `docs/systems/<system>.md` |
| flow | a cross-system runtime path | `docs/flows/<flow>.md` |
| adr | one architecture decision, immutable once accepted | `docs/architecture/decisions/<slug>.md` |
| api | one HTTP endpoint: contract, auth, errors, sequence | `docs/api/<service>/<endpoint>.md` |
| glossary term | a Title Case domain concept | entry in `docs/glossary.md` |

**Granularity rule:** document as a system until it crosses systems; then promote to a flow.

## Steps

1. **Assess.** No `docs/` tree? Bootstrap the minimal layout: `docs/README.md` (index linking every system), `systems/`, `flows/`, `architecture/decisions/`, `api/`, `glossary.md`. Present? Use it as-is; never rearrange someone's tree.
2. **Locate.** Read the docs index/map; find the affected system doc, related flows, endpoint pages, governing ADRs, and glossary terms. Decide honestly whether the change warrants a new doc or an edit to an existing one.
3. **Draft.** Each doc states purpose, inputs/outputs, key invariants, and a source map (code paths that implement it) so future readers can navigate both directions. Mark unresolved points `[NEEDS CLARIFICATION]` rather than inventing content.
4. **Sync surroundings,** not just the target: new Title Case term -> glossary; new flow -> linked from its systems and the index; accepted ADR -> propagate consequences into affected docs; any docs-vs-code disagreement reconciled by updating whichever side is wrong, or flagging the gap explicitly.
5. **Verify.** Every relative link resolves; ADR frontmatter valid; repo gate green.

## ADR lifecycle

Statuses: Proposed -> Accepted; an Accepted ADR is **never rewritten** - supersede it with `status: Superseded` plus `superseded_by: <file>`. Frontmatter requires `status` (allowed value), `date` (`YYYY-MM-DD`), and context + decision + consequences sections.

## Done =

- Every relative link in new/updated docs (and their source maps) points to a real file.
- ADR frontmatter valid; superseded entries carry a real `superseded_by`.
- The target repo's own gate (formatter / link-check / markdown lint / tests) exits zero - noted as absent if none ships.

Hand back when: the named area cannot be located or inferred from the diff; docs contradict verified code and cannot be reconciled in scope.
