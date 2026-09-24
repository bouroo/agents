---
name: artifacts
description: "The deterministic artifact-chain pattern: one fixed-section document per lifecycle stage — intent, spec, and the PLAN.md plan with its sibling STATUS.md ledger — same sections in the same order, work packages as WPn, a DONE_WHEN checklist of executable checks, and a grounded mermaid diagram. Use when writing an intent, a spec, or a plan, aligning or reviewing an existing one, or when an artifact's shape drifted across efforts."
---

# Artifacts

An artifact an execution session must **resume from** needs a **deterministic shape**: same sections in the same order, same vocabulary for the same things, so any session can parse one, diff one, or write one without archaeology. Plans only humans read may stay prose. This skill owns the three durable shapes — **`intent.md`** (Intent), **`spec.md`** (Spec), **`PLAN.md`** + `STATUS.md` (Plan); the stage map is [lifecycle](../lifecycle/SKILL.md).

> **Override.** A project-level artifact template that explicitly supersedes this skill wins.

## One artifact per effort

`<plans-root>/<feature-slug>/` (kebab-case slug) holds the effort's chain: `PLAN.md`, the sibling `STATUS.md` ledger, and `retro.md` when done; render artifacts (wiki mirrors, images) live in `<slug>/wiki/`. The filename is invariant — `PLAN.md`, never `plan.md` or `PLAN-<topic>.md` — so a glob finds every plan. The finished `PLAN.md` is the source of truth; mirrors are downstream copies. The plans-root carries a `README.md` index, one row per plan: name, scope, status, `STATUS.md` link.

`intent.md` and `spec.md` live beside the code they govern (an `intent/` directory) or inside the effort directory; each is a single named, version-controlled file, never a wiki page the repository cannot diff.

## The three shapes

### intent.md — what and why, before any design

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

The originator's own words wherever possible: the problem as experienced, not as diagnosed. **Exclusions** is load-bearing — what this explicitly does *not* attempt is the boundary the spec later respects. Unresolved **Open questions** stay listed rather than silently answered; they are the spec's input.

### spec.md — requirements and design, compressed

```markdown
# <Title> — spec

Date: YYYY-MM-DD · Status: DRAFT | ACCEPTED · Steward: <who>

## Requirements
## Design
## Risks and contradictions
## Unresolved decisions
```

Requirements and design are produced together, not as separate analyst and designer handoffs. **Risks and contradictions** names where the intent fights itself; **Unresolved decisions** is honest about what is open — a spec that pretends to have decided everything has hidden the decisions, not made them. A hard-to-reverse choice graduates to an ADR ([solution-architecture](../solution-architecture/SKILL.md)), whose format and lifecycle are canonical there.

### PLAN.md — the deterministic execution shape

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

**One vocabulary, everywhere.** Sections, labels, and in-text references use the same tokens: work packages are `WPn` (WP0 allowed as baseline/migration), never "phase", "step", or bare `Pn`. Old heading names (`Context`, `Phases`, `Verification`, `Backlog`) are the drift signatures the sweep below hunts.

## The eight sections of PLAN.md

- **INTENT** — the §0-style gate as a plan section: what the code will do, and the driver (user statement with date, ticket, spec clause). If code / check / spec disagree, the disagreement is the finding — resolve by anchor rank before any work package.
- **Current state (verified facts)** — the repository as observed, every claim anchored: file:line, command output, module-state tables, branch state. No speculation; unknowns become questions under Decisions or items under PENDING.
- **Decisions (user-confirmed YYYY-MM-DD)** — numbered and dated, each naming who confirmed it. Derived decisions (recorded, not asked) continue the numbering under a lead-in.
- **Design** — the target shape: contracts, policies, API shapes, schemas. Lead with one `mermaid` diagram: `sequenceDiagram` for request flows, `flowchart` for topology and migration shapes. Ground it: every node and edge corresponds to a fact or decision already recorded — the diagram is a view of the plan, not a new source.
- **Work packages** — execution order; `### WPn — <repo/slice>: <deliverable>`. Each WP names files to touch, mechanics, and its own verify command. Sizing: one WP = one reviewable unit (or one MR); spanning two repos makes it two WPs joined by a sequencing note.
- **Risks** — table or bullets, including accepted risks and why they are accepted.
- **DONE_WHEN** — the anchor every execution session cites; write it while writing the WPs. One checkbox per terminal check, naming command plus expected observable (exit 0, query count, response body). A check that cannot name its command does not belong here. This is the plan's contract with [verification](../verification/SKILL.md): the judge re-runs exactly these.
- **STATUS.md (sibling file, not a section)** — the plan is a planning-phase artifact; execution state never leaks into it. `<slug>/STATUS.md` is the dated ledger, newest on top, cite-don't-narrate: what landed where (branch/commit/tag, merged or not), what is blocked and on what. **Probe before writing it**: run the cheapest observable check (glob a migration, grep a go.mod) rather than trusting the transcript; name the branch, because working-tree evidence can contradict the default branch — "LANDED" claims state the branch they hold on. Update every session that moves the plan.
- **PENDING** — follow-ups deliberately not taken: TWINS siblings, deferred tickets, ride-alongs. Write "None recorded." if empty. An unlisted pending action reads as fraud.

## Alignment / drift sweep (deterministic)

Run when adopting the pattern over existing artifacts, after renaming sections, or when judging one:

```bash
grep -n '^## ' <slug>/PLAN.md                                   # heading order + vocabulary
grep -rn 'Phase\|phase\|Backlog\|plan\.md\|Execution status' <slug>/PLAN.md  # orphan tokens; expect zero
grep -c '^\- \[ \]' <slug>/PLAN.md                              # every DONE_WHEN item is a check
```

Mechanical rules: heading sequence matches the fixed order; one status line under the title (Date · Status · Scope — the artifact's lifecycle, not execution progress); every in-text label resolves to a heading (`WP2` → `### WP2`); DONE_WHEN count matches the checkbox count; diagrams parse (balanced `alt/subgraph … end`, quoted labels); no `Execution status` section in PLAN.md — that heading lives in STATUS.md. Two fruitless sweeps on one file → stop and read it end to end.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Mixing intent, spec, and plan into one document | One artifact per stage; each is a checkpoint the next stage resumes from |
| An intent that diagnoses rather than states the problem | Record what was experienced, in the originator's words |
| A spec with no Unresolved decisions | List what is open; a settled-looking spec hid the decisions |
| Answering open questions silently in the spec | Promote them to decisions, or leave them open |
| Execution progress leaking into PLAN.md | It belongs in the sibling STATUS.md |
| A WP with no verify command | Size it until it names one, or split it |
| A DONE_WHEN item that cannot name its command | Rewrite it as a check, or it is not terminal |
| `Phase` / `step` / bare `Pn` tokens | One vocabulary: `WPn` |

## Cross-references

- [lifecycle](../lifecycle/SKILL.md) owns the stages; this skill owns the artifacts they commit.
- [grilling](../grilling/SKILL.md) produces the decisions; this pattern gives its one-recommendation plan a deterministic body to fill.
- [wayfinder](../wayfinder/SKILL.md) the map's decisions graduate into PLAN.md work packages when a build effort starts.
- [verification](../verification/SKILL.md) judges a finished plan against DONE_WHEN; STATUS.md entries owe the same evidence standard as any done claim.
- [solution-architecture](../solution-architecture/SKILL.md) owns the ADR format the spec's hard-to-reverse decisions graduate into.
- [evals](../evals/SKILL.md) the eval suite and the plans-root index are artifacts too; give them a shape rather than ad-hoc.
