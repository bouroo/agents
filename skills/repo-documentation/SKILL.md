---
name: repo-documentation
description: Repo-local documentation system for humans and agents: a docs/ tree of systems, flows, architecture/ADRs, and a glossary. Use when the repo maintains a docs/ tree and a behavior, interface, invariant, or domain-term change occurs that requires updating project documentation.
---

# Repo-Local Documentation

Source code is the implementation source of truth; `docs/` explains the system at a useful abstraction across the THINK→ACT→PROVE→GROW loop. The repo you are working in keeps its own `AGENTS.md` (or `docs/README.md`) as the routing/index layer.

> **Precondition.** This skill applies to repos that maintain a `docs/` tree. When loaded from the `document-phase` command, it also covers bootstrapping `docs/` from scratch. When loaded passively (during review or refactor), it activates only if `docs/` already exists -- do not impose docs on a repo mid-review.

> `AGENTS.md` tells agents where to look and how to work; `docs/` explains how the application works.

**Stance:** You treat documentation as a first-class deliverable written for the reader who has never seen this codebase. Code shows *what*; docs explain *why*, *when*, and *what can go wrong*. A comment that only restates the code wastes the reader's time.

**Modes:**

- **Write mode (THINK & ACT)** -- generating or filling in missing documentation (system/flow/ADR/glossary). Work sequentially through the Agent Workflow; or parallelize across independent docs using sub-agents.
- **Review mode (PROVE)** -- auditing existing docs for completeness, accuracy, and style against current implementation. Use up to 5 parallel sub-agents, one per doc layer (systems, flows, architecture/ADR, glossary, README/index).
- **Sync mode (GROW)** -- updating existing docs to match code changes and runtime evolution. Update only docs whose behavior/interface/invariant/domain-term changed.

---

## Integration with the THINK→ACT→PROVE→GROW Loop

1. **THINK Phase:** Read `AGENTS.md` and `docs/` to gather context on system boundaries, domain entities, and ADR constraints before making edits.
2. **ACT Phase:** Keep implementation surgical (WIP = 1). When code changes observable behavior or contracts, draft or update corresponding system/flow docs.
3. **PROVE Phase:** Verify that documentation matches executable reality (L1/L2/L3 testing). Ensure markdown links resolve and diagrams reflect updated behavior.
4. **GROW Phase:** Update glossary entries, ADR statuses (`Superseded`, `Accepted`), and system docs as the repo evolves to maintain a self-improving operational record.

---

## Core Idea

Durable repo-local docs close the context gap for both humans and agents. Without them, contributors have to infer behavior, boundaries, domain terms, and architectural constraints from scattered source and one-off comments. With them:

- New readers onboard quickly without full-codebase exploration.
- Reviews catch behavior changes, stale assumptions, and missing-impact bugs.
- Agents make safer changes because invariants and interfaces are explicit.

Docs are plain Markdown, reviewed alongside code, with no separate publishing infrastructure.

---

## When to Use (and When Not To)

Document behavior that is **central, risky, frequently changed, hard to infer, or user-visible / security / billing / data-integrity sensitive**. Don't document every file; skip trivial helpers and generated code.

| Document | Skip if |
|---|---|
| System doc | The area is trivial, auto-generated, or a thin wrapper over a well-known library |
| Flow doc | The behavior stays inside one system and is already covered there |
| ADR | The decision is a routine implementation detail, small refactor, or temporary workaround |
| Glossary term | The word has no product-specific meaning beyond its common meaning |

---

## The `docs/` Layout

```
docs/
  README.md
  STYLE.md
  glossary.md
  systems/
  flows/
  architecture/
    README.md
    decisions/
      README.md
  templates/
    system.md
    flow.md
    adr.md
```

Exact filenames can follow the host repo's conventions; the conceptual structure should remain clear.

---

## Documentation Types

| Type | Location | Purpose | Use when |
|---|---|---|---|
| **System** | `docs/systems/` | A coherent behavior area (a module, package, service, feature, integration, or domain concern) | A reader would otherwise inspect several files to understand how a part of the app works |
| **Flow** | `docs/flows/` | Behavior crossing systems, with multi-step state transitions | Crosses multiple systems, has several steps, is frequently changed/debugged, involves external services, or has security/billing/data-integrity/user-visible implications |
| **Architecture** | `docs/architecture/` | Cross-system structure, durable constraints, tradeoffs | Topic affects more than one system; explains *why* the app is shaped a certain way |
| **ADR** | `docs/architecture/decisions/` | Durable architectural decisions with context and tradeoffs | Decision shapes the system beyond a single implementation detail |
| **Glossary** | `docs/glossary.md` | Title Case domain terms used across the app | Word has product-specific meaning that is easy to misread |

**Promotion rule:** a system that grows complex, becomes cross-system, or meets a flow criterion gets promoted to `docs/flows/`. The system doc links to the new flow doc.

---

## ADR Rules

Every ADR begins with YAML frontmatter:

- `status` (required) -- one of `Proposed`, `Accepted`, `Superseded`, `Deprecated`, `Rejected`.
- `date` (required) -- `YYYY-MM-DD`.
- `superseded_by` (required only when `status: Superseded`) -- repo-relative path to the replacement ADR.

Only **`Accepted`** ADRs are current guidance. Never rewrite an accepted ADR to change the decision -- create a new one and mark the old `Superseded`, linking with `superseded_by`. Small non-decision corrections (typos, links) are allowed.

**Architectural decisions are human-owned.** Agents draft ADR text from accepted decisions and keep existing ADRs aligned with code; humans accept.

---

## Source Maps

Every system and flow doc includes a **Source map** section that links the most important source files via relative Markdown links. Don't list every file -- prefer entry points, state definitions, handlers, services, jobs, tests, and integration files.

---

## Style

Apply to every piece of documentation you write or review:

- **Concision** -- write the shortest version that carries the idea. Remove ornament and hollow transitions. Never drop facts, warnings, or user-requested depth.
- **Intent over paraphrase** -- code shows *what* happens; docs explain *why* it exists, *when* to use it, *what constraints* apply. A comment that only restates the signature wastes the reader's time.
- **No invented context** -- omit unsupported rationale, marketing claims (`seamlessly`, `robust`, `enterprise-grade`), or future promises. Leave gaps visible (`[NEEDS CLARIFICATION]`) rather than filling with speculation.
- **Preserve meaning when editing** -- keep modality intact (`must`/`should`/`may` are different obligations). Preserve conditions, warnings, required actions. A cleaner sentence that changes obligations is wrong.

Formatting:

- Clear, direct Markdown; stable headings.
- Relative Markdown links for related docs and source files.
- Explain behavior, responsibilities, flows (mermaid diagrams), invariants, pitfalls -- not every line.
- Stay concise enough to read before making changes.
- **Glossary headings use Title Case** (e.g. `## Email Verification`, `## Verification Token`). Prefer that Title Case form in finished docs when it improves clarity. Lowercase is fine in drafts, comments, identifiers, or informal notes.

---

## Keeping Docs Updated (GROW Phase Discipline)

Docs are part of the diff. Every change that touches any of the following must update the affected doc in the same change:

- System responsibilities, runtime behavior, user-visible behavior.
- Internal workflows, data models, persistence behavior, external integrations.
- Public APIs, configuration, error handling.
- Security or auth behavior, important invariants or assumptions.
- Testing or debugging expectations.
- Glossary-defined domain concepts.

Reviewers treat docs as part of the change. If docs and code disagree, do one of:

1. Update the docs to match the code.
2. Update the code to match the documented intent.
3. Explicitly call out the mismatch for review.

---

## Agent Workflow

1. Read the working repo's `AGENTS.md`.
2. Use `docs/README.md` to find relevant docs.
3. Read the system / flow / architecture / glossary docs for the area.
4. Inspect source files for implementation details.
5. Make the code change (ACT phase).
6. Update affected docs if behavior, responsibilities, flows, invariants, assumptions, interfaces, or glossary-defined concepts changed.
7. Ensure docs and code agree before finishing (PROVE & GROW phases).

---

## Validation

Run the working repo's doc/link checks and validators (e.g. Markdown linters, link checkers, doc-style scripts). Verify after every change that affected docs render, links resolve, and `docs/` still matches code.

---

## Templates

This skill ships three sibling templates that you can copy into the working repo's `docs/templates/`:

- [system.md](./references/system.md) -- for `docs/systems/`.
- [flow.md](./references/flow.md) -- for `docs/flows/`.
- [adr.md](./references/adr.md) -- for `docs/architecture/decisions/`.

---

## Cross-References

- [effective-code-craft](../effective-code-craft/SKILL.md) -- Code for reading, clear doc style
- [harness-engineering](../harness-engineering/SKILL.md) -- Repository as system of record, self-improving harness (GROW)
- [spec-driven-development](../spec-driven-development/SKILL.md) -- Specification-first workflow (THINK phase)

---

## References

- *Docs as a System* (lukewilson2002) -- the repo-local documentation model this skill encodes.
- *Diátaxis* (Grand) -- https://diataxis.fr/
- *Documenting Architecture Decisions* (Nygard) -- https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- Mermaid flowchart syntax -- https://mermaid.js.org/syntax/flowchart.html
