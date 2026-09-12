---
name: domain-modeling
description: "Actively build and sharpen a project's domain language while designing: challenge terms against the glossary, pin canonical ones, stress-test relationships with edge-case scenarios, cross-reference code claims, and keep CONTEXT.md current. Use when design work touches domain terms, the glossary, CONTEXT.md, or a decision record."
---

# Domain Modeling

The *active* discipline for a project's domain language — for when you are **changing** the model, not consuming it. Merely reading `CONTEXT.md` for vocabulary is a one-line habit any skill can do; this skill owns the design session that introduces, sharpens, or contradicts a term.

> **Override.** A project-level glossary or decision-record convention that explicitly supersedes this skill wins.

## Five habits

1. **Challenge against the glossary.** A term conflicting with the existing language in `CONTEXT.md` is called out on the spot: the glossary defines X, you seem to mean Y — which is it?
2. **Sharpen fuzzy language.** Vague or overloaded terms get a proposed canonical one: "you say _account_ — Customer or User? Those are different things." Pin it in the glossary with an `_Avoid_` list.
3. **Stress-test with concrete scenarios.** A relationship under discussion gets edge-case scenarios that force the boundaries between concepts to be precise.
4. **Cross-reference the code.** A claim about how things work is checked against the code; a contradiction is surfaced immediately — the same authority rank as the `INTENT:` gate: user statement > spec > checks > code.
5. **Update `CONTEXT.md` inline.** A resolved term is written down the moment it settles, never batched.

**Exit:** the session ends when every term under discussion is either pinned in `CONTEXT.md` or explicitly deferred; no term is left settled-in-conversation-but-unwritten. If a term cannot be resolved in scope, record it as an open question rather than guessing a definition.

## The artifact: CONTEXT.md

`CONTEXT.md` at the repo root is **a glossary and nothing else** — no implementation details, not a spec, not a scratchpad. Entries are opinionated: pick the best term, list the rest under `_Avoid_`. Create it lazily, when the first term resolves. Multi-context repos put a `CONTEXT-MAP.md` at the root listing each context and where its `CONTEXT.md` lives, mirroring [solution-architecture](../solution-architecture/SKILL.md)'s bounded contexts. Entry format, rules, and the map template: [context-format](references/context-format.md).

## ADRs, offered sparingly

Offer a decision record only when all three hold: **hard to reverse** (changing your mind later costs meaningfully), **surprising without context** (a future reader will ask why), and **the result of a real trade-off** (genuine alternatives existed). Missing any one, skip it. Format, naming, and lifecycle are canonically owned by [solution-architecture](../solution-architecture/SKILL.md) §3 and its [decisions reference](../solution-architecture/references/decisions.md) — never a second format.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Treating `CONTEXT.md` as a spec or scratchpad | Glossary and nothing else; implementation detail goes elsewhere |
| Batching term updates | Write each resolved term the moment it settles |
| Listing synonyms neutrally | Be opinionated: one canonical term, the rest under `_Avoid_` |
| An ADR for every choice | Only the triad trigger; standards-covered or throwaway calls get none |
| Vendoring a second ADR template | Defer to solution-architecture's format and lifecycle |

## Cross-references

- [grilling](../grilling/SKILL.md) interviews where terms are being pinned: fuzzy language is sharpened mid-round, not after.
- [solution-architecture](../solution-architecture/SKILL.md) owns ADR format and lifecycle; its bounded contexts are what a `CONTEXT-MAP.md` charts.

Adapted from [mattpocock/skills](https://github.com/mattpocock/skills) (`domain-modeling`, MIT).
