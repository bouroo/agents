---
name: spec-driven-development
description: "Specification-first workflow that treats prompts as version-controlled artifacts within the THINK-ACT-PROVE-GROW loop. Use when starting a new feature, drafting technical requirements, resolving ambiguous requests, or bridging intent and implementation."
---

# Spec-Driven Development

A prompt-as-artifact workflow integrated into the loop. **Spec is truth. Code serves spec, not the reverse.**

> **Override.** A project-level specification policy that explicitly supersedes this skill wins.

**Stance:** value simplicity and explicitness; apply rigor only when risk warrants it. The spec is the durable contract; the code is its executable shadow. Batch the canvas + implement + verify in one pass; round-trips cost more than in-turn tool results.

## Modes

- **Design mode (THINK)** shaping a feature, service, or module. Ask about architecture preference and risk tolerance before proposing a spec; favor the smallest pattern that satisfies the requirement.
- **Implementation mode (ACT)** executing a spec. Honor it exactly; surface contradictions as questions, never silent drift.

## The REASONS canvas

Capture intent before code. Mark spikes explicitly (lightweight canvas: R + A only).

| Letter | Means | Holds |
|---|---|---|
| **R** | Requirements | User-visible behavior the system must deliver |
| **E** | Entities | Domain nouns and their relationships |
| **A** | Approach | Architecture, patterns, data flow, module structure |
| **O** | Operations | Per-entity commands and queries the system must expose (CRUD, search, sync): the API surface |
| **S** | Safeguards | Non-negotiable constraints: latency, size, error rates, quotas, security |
| **N** | Norms | Cross-cutting rules: naming, error handling, documentation, clarity |

## Fitness levels (set rigor by risk)

| Level | Trigger | Canvas |
|---|---|---|
| Trivial | typo, rename, one-liner, no new behavior | skip the canvas; note the skip |
| Lightweight | small additive change, isolated module | R + A |
| Standard | normal feature, clear risk profile | full REASONS |
| Heavyweight | cross-cutting, infra, security-sensitive, irreversible | full REASONS + explicit safeguards + review |

## What every spec carries

- **Requirements** user-visible behavior, stated as testable outcomes.
- **Operations** the endpoint/command inventory per entity; a missing operation is a visible gap at review time.
- **Approach** architecture and data flow; the smallest pattern that works.
- **Safeguards** numeric, non-negotiable (P99 < 200ms at 1k QPS; not "should be fast").
- **Test scenarios** happy path, error path, edge cases, at least one end-to-end.
- **Error handling** typed errors, no in-band sentinels, wrap-with-context propagation.
- **Norms** naming, docs, clarity conventions.

## Authority order (when sources disagree)

**user statement > spec > tests > current code.** Framing ("make tests pass") is not intent. When reality contradicts a locked spec, the spec is the bug: open a change, don't drift.

## Spec <-> code sync

- **Logic change:** spec first, then code. Spec is truth.
- **Refactor:** code first, then sync spec. Never land one side without the other.
- A test that disagrees with the spec is the suspect, not the spec.

## Anti-patterns

| Smell | Fix |
|---|---|
| Naming safeguards as goals ("should be fast") | Make safeguards numeric and non-negotiable |
| Locked spec contradicting reality | Open a change; don't drift |
| Refactor without spec sync | Sync both sides; never land one alone |
| Logic change code-first | Spec first; spec is truth |
| Tests promoted above spec | Authority order: user > spec > tests > code |
| Heavyweight canvas on a spike | Mark spikes; use R + A only |

## References

- [code-craft](../code-craft/SKILL.md) the Intent gate and code craft commandments.
- [harness-engineering](../harness-engineering/SKILL.md) structured handoffs, failure-mode controls, GROW.
