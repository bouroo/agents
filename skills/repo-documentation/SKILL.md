---
name: repo-documentation
description: "Repo-local documentation system for humans and agents: a docs/ tree of systems, flows, architecture/ADRs, API endpoint pages, and a glossary. Use when the repo maintains a docs/ tree and a behavior, interface, invariant, or domain-term change occurs that requires updating project documentation."
---

# Repo-Local Documentation

## Overview

Source code is the implementation source of truth; `docs/` explains the system at a useful abstraction for a reader who has never seen the codebase. Code shows *what* happens; docs explain *why* it exists, *when* it applies, and *what can go wrong*. The repo keeps `AGENTS.md` (or `docs/README.md`) as the routing and index layer: `AGENTS.md` tells agents where to look and how to work; `docs/` explains how the application works.

Docs are plain Markdown, reviewed alongside code, with no separate publishing infrastructure. A comment that only restates the code wastes the reader's time.

## When to Load

Load when the repo maintains a `docs/` tree and a change touches any of:

- system responsibility, runtime or user-visible behavior
- internal workflow, data model, persistence, or external integration
- public API, configuration, or error handling
- security/auth behavior, a documented invariant, or a glossary-defined domain term

When loaded passively during a review or refactor, activate only if `docs/` already exists; do not impose docs on a repo mid-review. Document behavior that is central, risky, frequently changed, hard to infer, or sensitive (security, billing, data integrity). Skip trivia:

| Document | Skip if |
|---|---|
| System | trivial, auto-generated, or a thin wrapper over a well-known library |
| Flow | stays inside one system and is already covered there |
| ADR | a routine implementation detail, small refactor, or temporary workaround |
| Glossary term | carries no product-specific meaning beyond its common meaning |
| API | the endpoint is fully specified by the OpenAPI contract (`docs/openapi.yaml`) |

## docs/ Layout

```
docs/
  README.md          index and how to navigate the docs
  systems/           one doc per system or subsystem
  flows/             one doc per important cross-system flow
  api/               one doc per HTTP endpoint (per-endpoint contract pages)
  architecture/      architecture overviews and decisions/
    decisions/       one ADR per decision
  glossary.md        product-specific terms
  templates/         copies of the sibling templates below
```

## Modes

- **Write** -- generate or fill in missing docs (system, flow, ADR, glossary). Work the docs sequentially, or parallelize independent docs across sub-agents.
- **Review** -- audit existing docs for completeness, accuracy, and style against the current implementation. Use up to five parallel sub-agents, one per layer (systems, flows, architecture/ADRs, glossary, index).
- **Sync** -- update existing docs to match code and runtime changes. Update only docs whose behavior, interface, invariant, or domain term changed.

## Documentation Types

| Type | Location | Use when |
|---|---|---|
| System | `docs/systems/` | a reader would otherwise inspect several files to understand how a part of the app works |
| Flow | `docs/flows/` | crosses multiple systems, has several steps, is frequently changed or debugged, or has security/billing/data-integrity/user-visible implications |
| Architecture | `docs/architecture/` | a topic affects more than one system, or explains why the app is shaped a certain way |
| ADR | `docs/architecture/decisions/` | a decision shapes the system beyond a single implementation detail |
| API | `docs/api/` | one HTTP endpoint's contract (method, path, auth, request/response, status codes, sequence) needs a standalone, human-readable page |
| Glossary | `docs/glossary.md` | a word has product-specific meaning that is easy to misread |

A system that grows complex, becomes cross-system, or meets a flow criterion is promoted to `docs/flows/`; the system doc links to the new flow doc.

## ADR Rules

Every ADR carries YAML frontmatter:

- `status` (required): `Proposed`, `Accepted`, `Superseded`, `Deprecated`, or `Rejected`.
- `date` (required): `YYYY-MM-DD`.
- `superseded_by` (required only when `status: Superseded`): repo-relative path to the replacement ADR.

Only `Accepted` ADRs are current guidance. Never rewrite an accepted ADR to change its decision: create a new ADR, mark the old one `Superseded`, and link it with `superseded_by`. Small non-decision corrections (typos, links) are allowed. Architectural decisions are human-owned: agents draft ADR text and keep ADRs aligned with code; humans accept them.

## Source Maps

Every system and flow doc includes a **Source map** section linking the most important source files via relative Markdown links. Do not list every file; prefer entry points, state definitions, handlers, services, jobs, tests, and integration files.

## Style

Apply to everything you write or review:

- **Concision** -- the shortest version that carries the idea. Remove ornament and hollow transitions; never drop facts, warnings, or requested depth.
- **Intent over paraphrase** -- docs explain *why*, *when*, and constraints, not *what* the signature says.
- **No invented context** -- omit unsupported rationale, marketing words (`seamless`, `robust`), or future promises. Leave a gap as `[NEEDS CLARIFICATION]` rather than speculate.
- **Preserve meaning when editing** -- keep modality intact (`must`/`should`/`may` are different obligations); preserve conditions, warnings, and required actions. A cleaner sentence that changes obligations is wrong.
- Stable headings; relative Markdown links for related docs and source; glossary headings use Title Case (`## Email Verification`) in finished docs.

## Keeping Docs Updated

Docs are part of the diff. Every change that touches system behavior, workflows, data models, persistence, integrations, security/auth, invariants, APIs, or glossary terms must update the affected doc in the same change. If docs and code disagree, do one of: update the doc to match the code, fix the code to match the doc, or record the gap as a follow-up and flag it for review.

## References

Three sibling templates, copied into the working repo's `docs/templates/`:

- [system.md](references/system.md) -- for `docs/systems/`
- [flow.md](references/flow.md) -- for `docs/flows/`
- [adr.md](references/adr.md) -- for `docs/architecture/decisions/`
- [api.md](references/api.md) -- for `docs/api/` (one HTTP endpoint per file)

Related skills:

- [code-craft](../code-craft/SKILL.md) -- clear doc style, artifact gates
- [harness-engineering](../harness-engineering/SKILL.md) -- repo as system of record
- [spec-driven-development](../spec-driven-development/SKILL.md) -- specification-first workflow
