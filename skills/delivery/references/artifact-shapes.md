# Artifact Shapes

> Load on demand from [delivery](../SKILL.md): the deterministic shapes the Lifecycle stages commit, their shared vocabulary, and the drift sweep that keeps an existing plan well-formed.

An artifact an execution session must **resume from** needs a **deterministic shape**: same sections in the same order, same vocabulary for the same things. Plans only humans read may stay prose. Three durable shapes belong to the lifecycle stages — `intent.md` (Intent), `spec.md` (Spec), `PLAN.md` + `STATUS.md` (Plan).

## Where the chain lives

`<plans-root>/<feature-slug>/` (kebab-case) holds the chain: `PLAN.md`, the sibling `STATUS.md` ledger, and `retro.md` when done; render artifacts live in `<slug>/wiki/`. The filename is invariant — `PLAN.md`, never `plan.md` or `PLAN-<topic>.md`. The plans-root carries a `README.md` index, one row per plan. `intent.md` and `spec.md` live beside the code they govern (an `intent/` directory) or inside the effort directory, each a single named, version-controlled file.

## intent.md

The originator's own words, problem as experienced not diagnosed:

```markdown
# <Title> — intent
Date: YYYY-MM-DD · Status: DRAFT | ACCEPTED · Originator: <who>
## Problem
## Affected parties
## Desired outcome
## Constraints
## Exclusions
## Open questions
```

**Exclusions** is load-bearing: what this does *not* attempt is the boundary the spec later respects. Unresolved **Open questions** stay listed rather than silently answered.

## spec.md

Requirements and design produced together, not as analyst/designer handoffs:

```markdown
# <Title> — spec
Date: YYYY-MM-DD · Status: DRAFT | ACCEPTED · Steward: <who>
## Requirements
## Design
## Risks and contradictions
## Unresolved decisions
```

**Risks and contradictions** names where the intent fights itself. A spec that pretends to have decided everything has hidden the decisions, not made them. A hard-to-reverse choice graduates to an ADR.

## PLAN.md

The deterministic execution shape:

```markdown
# <Title> — plan
Date: YYYY-MM-DD · Status: DRAFT | APPROVED | IN PROGRESS | DONE · Scope: <repos touched>
## INTENT
## Current state (verified facts)
## Decisions (user-confirmed YYYY-MM-DD)
## Design
## Work packages
## Risks
## DONE_WHEN (executable evidence)
## PENDING (prescribed but untaken)
```

**One vocabulary, everywhere**: work packages are **`WPn`** (WP0 allowed as baseline/migration), never "phase", "step", or bare `Pn`. Section by section: **INTENT** is the §0 gate as prose — what the code will do and its driver; if code, check, and spec disagree, the disagreement is the finding, resolved by anchor rank before any work package. **Current state** is the repository as observed, every claim anchored (file:line, command output). **Decisions** are numbered, dated, naming who confirmed them. **Design** leads with one `mermaid` diagram grounded in facts already recorded. **Work packages** run in execution order, `### WPn — <repo/slice>: <deliverable>`, each naming files to touch, mechanics, and its own verify command; one WP is one reviewable unit. **Risks** include accepted risks and why. **DONE_WHEN** is the anchor every execution session cites — one checkbox per terminal check, naming command plus expected observable; a check that cannot name its command does not belong. **PENDING** lists follow-ups deliberately not taken (write "None recorded." if empty); an unlisted pending action reads as fraud.

## STATUS.md

**STATUS.md** is the sibling ledger, not a section: the plan stays a planning artifact, and execution progress never leaks into it. Newest on top, cite-don't-narrate: what landed where (branch/commit/tag, merged or not), what is blocked and on what. Probe before writing it — run the cheapest observable check rather than trusting the transcript — and name the branch, because working-tree evidence can contradict the default branch.

## Drift sweep

Drift sweep for an existing plan: heading order matches the fixed sequence; one status line under the title; every in-text label resolves to a heading; `DONE_WHEN` count matches the checkbox count; diagrams parse. Mechanical checks: `grep -n '^## ' <slug>/PLAN.md` for order, `grep -rn 'Phase\|phase\|Backlog\|plan\.md\|Execution status' <slug>/PLAN.md` for orphan tokens (expect zero), `grep -c '^\- \[ \]' <slug>/PLAN.md` so every `DONE_WHEN` item is a check.
