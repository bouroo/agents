---
name: spec-driven-development
description: >
  Specification-first workflow that treats prompts as version-controlled artifacts. Use when starting a new
  feature, resolving ambiguous requirements, or bridging intent and implementation. Grounded in Martin Fowler's
  SPDD and GitHub Spec-kit.
---

# Spec-Driven Development

A prompt-as-artifact workflow. **Spec is truth. Code serves spec, not the reverse.**

> **Override.** A project-level specification policy that explicitly supersedes this skill takes precedence.

**Stance:** You value simplicity and explicitness. You apply rigor only when risk warrants it; you push back on premature abstraction and on heavyweight process for trivial work. The spec is the durable contract; the code is its executable shadow.

**Modes:**

- **Design mode** -- shaping a new feature, service, or module. Ask about architecture preference and risk tolerance before proposing a spec; favor the smallest pattern that satisfies the requirement. Use the Fitness Levels table to set rigor.
- **Resolve mode** -- disambiguating conflicting or vague requirements. Produce the REASONS canvas; surface every `[NEEDS CLARIFICATION]`; stop and wait rather than guess.
- **Implement mode** -- locked spec -> code. Generate code *from* the locked spec, not alongside it; verify against acceptance criteria at L1/L2/L3.
- **Sync mode** -- keeping spec and code aligned after the fact. Logic change: spec first, then code. Refactor: code first, then spec. Never land one without the other.

## REASONS Canvas

Use this 7-part structure for every non-trivial spec. Fill every section. Mark unknowns with `[NEEDS CLARIFICATION]`.

| Letter | Section | Capture |
|---|---|---|
| **R** | Requirements | Problem statement, Definition of Done, acceptance criteria |
| **E** | Entities | Domain objects, relationships, boundaries, data flow |
| **A** | Approach | Chosen strategy, alternatives rejected and why, key trade-offs |
| **S** | Safeguards | Non-negotiable constraints: latency, size, error rates, quotas, security |
| **O** | Outline | Ordered, testable execution phases (the implementation plan) |
| **N** | Norms | Cross-cutting rules: naming, error handling, documentation, clarity |
| **S** | Signoff | Approval criteria, reviewers, rollout gate, rollback plan |

### Template

```markdown
## R  --  Requirements
- Problem statement
- Definition of Done (measurable)
- Acceptance criteria (testable)

## E  --  Entities
- Domain objects and relationships
- Existing vs. new boundaries
- Data flow between entities

## A  --  Approach
- Chosen strategy and rationale
- Alternatives considered and rejected
- Key trade-offs

## S  --  Safeguards
- Performance ceilings (latency, memory, size limits with numbers)
- Error-rate / availability budgets
- Security rules (no secrets in logs, least privilege)
- Quotas and cost ceilings
- Invariants that must hold

## O  --  Outline
- Ordered, testable phases
- Each phase precise enough for a subagent to execute without ambiguity
- Test scenarios: happy path, error path, edge cases
- At least one phase exercises an end-to-end boundary

## N  --  Norms
- Naming: scope-proportional, no context/type repetition
- Error handling: explicit returns, guard-clause-first, wrap-with-context
- Documentation: name-first sentences for public symbols
- Reference [effective-code-craft](../effective-code-craft/SKILL.md) for the full norm set

## S  --  Signoff
- Approval criteria (who reviews, what evidence is required)
- Stakeholders
- Rollout gate (metrics, feature flag, canary plan)
- Rollback plan (how to revert safely)
```

## Spec Structure (sections inside a spec document)

Beyond the REASONS canvas, a complete spec document typically carries:

- **Problem** -- the user need in one paragraph; surface the problem, not a presumed solution.
- **Entities** -- domain objects and their relationships.
- **Approach** -- chosen strategy with rejected alternatives.
- **Constraints** -- non-negotiable boundaries (latency, cost, security, compatibility).
- **Phases** -- ordered execution steps, each independently testable.
- **Test scenarios** -- happy path, error path, edge cases, at least one end-to-end.
- **Safeguards** -- invariants and numeric limits that must hold at all times.
- **Error handling** -- typed errors, no in-band sentinels, wrap-with-context propagation.

## Prompt Lifecycle

Treat the spec as a versioned artifact moving through six states:

```
draft → review → lock → implement → feedback → evolve
```

- **draft** -- canvas is incomplete or under debate; safe to rewrite.
- **review** -- canvas is complete; reviewers challenge Requirements, Approach, Safeguards.
- **lock** -- signed off; code generation may begin; any change requires re-opening.
- **implement** -- code is produced *from* the locked spec, not alongside it.
- **feedback** -- tests, runtime, and user signal are recorded against the spec.
- **evolve** -- feedback triggers spec updates, which re-enter at `review`.

A locked spec that disagrees with reality is a bug -- open a new change, don't silently drift.

## Fitness Levels

Match the rigor of the canvas to the risk of the work:

| Level | Scenario | Effort guidance |
|---|---|---|
| **Spike / throwaway** | Exploration, time-boxed learning, throwaway prototypes. | Lightweight canvas (R + A only); explicitly mark "spike" so reviewers don't enforce production norms. |
| **Prototype** | User-facing but limited audience; intent clear, shape unknown. | Full REASONS at lower fidelity; lightweight tests; signoff by one reviewer. |
| **Production** | Default for shipped features, services, and modules. | Full REASONS, executable tests at L1/L2/L3, signed-off safeguards. |
| **Critical** | High-compliance, hard-constraint, multi-team, cross-cutting systems. | Full REASONS + ADR + mutation testing + formal review + rollout gate + rollback plan. |

Decision rule: when in doubt, round up one level -- downgrading a critical change costs more than upgrading a small one.

## Spec ⇄ Code Sync

The two artifacts must never diverge silently.

- **Logic change** (new behavior, modified behavior) → **spec first, then code.** Lock the new spec; generate code from it; verify against acceptance criteria.
- **Refactor (no behavior change)** → **code first, then spec.** Land the refactor with green tests; sync the spec to reflect the new structure.
- **Bidirectional feedback** -- production reality informs spec evolution. Hotfixes land in code, then the spec is updated retroactively so the governance loop closes.
- **Never land one side without the other.** A spec without code is an abandoned promise; code without spec is undocumented behavior.

## Constitutional Gates (Spec-kit)

Keep these SPDD-specific gates. Use [effective-code-craft](../effective-code-craft/SKILL.md) for general code norms -- state only SPDD-specific additions in the canvas's **N -- Norms** section:

- **Simplicity** -- prefer ≤3 projects initially; resist premature decomposition.
- **Anti-abstraction** -- use natural language types; add no valueless layers.
- **Test-first** and **Integration-first** -- write tests before implementation; prefer real-boundary end-to-end coverage.
- **Library-first** and **CLI interface** -- build reusable libraries with a thin CLI shim; make every feature reachable from the command line.
- **Named construction** -- use explicit fields/parameters for external types and omit zero-value defaults.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Spec describes *how* (implementation) instead of *what/why* | Rewrite the requirement as an observable behavior with acceptance criteria |
| Skipping the canvas because "the task is small" | Use Fitness Levels; downgrade deliberately and note the assumption, never silently |
| Naming safeguards as goals ("the system should be fast") | Make safeguards numeric and non-negotiable ("P99 < 200ms at 1k QPS") |
| Phase has no test scenario | Every phase lists at least happy path, error path, and one edge case |
| Treating the locked spec as immutable when reality contradicts it | A locked spec that disagrees with reality is a bug -- open a new change, don't drift |
| Refactor lands without a spec sync | Refactor: code first, then sync spec. Never land one side without the other |
| Logic change lands with code first | Logic change: spec first, then code. Spec is truth |
| Tests promoted above spec when they disagree | Authority order: user statement > spec > tests > current code. Framing ("make tests pass") is not intent |
| Heavyweight REASONS canvas on a spike | Mark spikes explicitly; use lightweight canvas (R + A only) |

## When to Use

Use the REASONS canvas when:

- Starting a new feature, service, or module.
- Resolving ambiguous or conflicting requirements.
- Bridging intent and implementation across a team.
- Refactoring without losing context.
- Working on logic-heavy, repeatable, high-constraint systems.

Skip the canvas (and note the assumption) for trivial fixes, spikes, one-off scripts, or pure aesthetic work -- see the Fitness Levels table above.
