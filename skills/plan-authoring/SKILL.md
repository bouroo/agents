---
name: plan-authoring
description: "The deterministic plan-document pattern: one PLAN.md per effort with a fixed section order, work packages as WPn, a DONE_WHEN checklist of executable checks, a dated status ledger, and a grounded mermaid diagram. Use when writing a plan, aligning or reviewing an existing one, or when a plan shape drifted across efforts."
---

# Plan authoring

Plans that only humans read may be prose. Plans an execution session must resume from need a **deterministic shape**: same sections in the same order, same vocabulary for the same things, so any session — or the next agent — can parse one, diff one, or write one without archaeology. The alternative was observed cost: three efforts, three shapes, an alignment pass that hunted orphan `Phase` tokens instead of moving work.

## What makes it deterministic

**One artifact per effort**: `<plans-root>/<feature-slug>/PLAN.md` (kebab-case slug). The filename is invariant — `PLAN.md`, not `plan.md` or `PLAN-<topic>.md` — so a glob finds every plan. Render artifacts (wiki mirrors, images) live in `<slug>/wiki/`; the retrospective as `<slug>/retro.md`. The finished PLAN.md is the source of truth; mirrors are downstream copies. A finished effort gets `retro.md`; the plans-root carries a `README.md` index (one table row per plan: name, scope, status) and the `TEMPLATE.md` this skeleton mirrors.

**Fixed section order** (template mirrors this; project template wins on conflict — see Override):

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
## Execution status (dated)
## PENDING (prescribed but untaken)
```

**One vocabulary, everywhere.** Sections, package labels, and in-text references use
the same tokens: work packages are `WPn` (WP0 allowed as baseline/migration), never
"phase", "step", or bare `Pn`. Refer to packages as `WPn` in prose and status entries;
the sweep below catches strays. Old heading names (`Context`, `Phases`, `Verification`,
`Backlog`) are the drift signatures the sweep hunts.

## The nine sections

**INTENT** — the §0-style gate as a plan section: what the code will do, the driver
(user statement with date, ticket, spec clause). If code / check / spec disagree, the
disagreement is the finding — resolve by anchor rank before any work package.

**Current state (verified facts)** — what exists today, every claim anchored: file:line,
command output, module-state tables, branch state. No speculation; unknowns become
questions under Decisions or items under PENDING.

**Decisions (user-confirmed YYYY-MM-DD)** — numbered and dated, each naming who confirmed
it. Derived decisions (recorded, not asked) continue the numbering under a lead-in.

**Design** — the target shape: contracts, policies, API shapes, schemas. Lead with one
`mermaid` diagram: `sequenceDiagram` for request flows, `flowchart` for topology and
migration shapes. Ground it: every node/edge must correspond to a fact or decision
already recorded in the plan — the diagram is a view of the plan, not a new source.
(Confluence mirrors render PlantUML; keep a puml twin in `<slug>/wiki/` when mirroring.)

**Work packages** — execution order; `### WPn — <repo/slice>: <deliverable>`. Each WP
names files to touch, mechanics, and its own verify command. Sizing: one WP = one MR
(or one reviewable unit) — if it spans two repos, it's two WPs joined by a sequencing
note, not one WP spanning both.

**Risks** — table or bullets, including accepted risks and why they are accepted.

**DONE_WHEN** — the anchor every execution session cites; write it while writing the WPs.
One checkbox per terminal check, each naming command plus expected observable (exit 0,
query count, response body). A check that cannot name its command doesn't belong here.
This is the plan's contract with [verification](../verification/SKILL.md): the judge
re-runs exactly these.

**Execution status** — a dated ledger, newest on top, cite-don't-narrate: what landed,
where (branch/commit/tag, merged or not), what is blocked and on what. **Probe before
writing it**: run the cheapest observable check (glob a migration, grep a go.mod) rather
than trusting the transcript; state the branch, because working-tree evidence can
contradict the default branch — "LANDED" claims must name the branch they hold on.
Update every session that moves the plan.

**PENDING** — follow-ups deliberately not taken: TWINS siblings, deferred tickets,
ride-alongs. Write "None recorded." if empty. An unlisted pending action reads as fraud.

## Alignment / drift sweep (deterministic)

Run when adopting the pattern over existing plans, after renaming sections, or when a
plan is judged:

```bash
# heading order + vocabulary
grep -n '^## ' <slug>/PLAN.md
# orphan tokens after renames (Phase/phase/Backlog/old filenames); expect zero hits
grep -rn 'Phase\|phase\|Backlog\|plan\.md' <slug>/PLAN.md
# every DONE_WHEN item names a check
grep -c '^\- \[ \]' <slug>/PLAN.md
```

Mechanical rules: check heading sequence against the fixed order; one status line under
the title (Date · Status · Scope); every in-text label resolves to a heading (`WP2` ->
`### WP2`); DONE_WHEN count matches the checkbox count; diagrams parse (balanced
`alt/subgraph … end`, quoted labels). Two fruitless sweeps on one file -> stop and read
the file end to end.

## Cross-references

- [grilling](../grilling/SKILL.md) produces the decisions; this pattern gives its one-recommendation plan a deterministic body to fill.
- [wayfinder](../wayfinder/SKILL.md) the map's decisions-so-far graduate into PLAN.md work packages when a build effort starts.
- [verification](../verification/SKILL.md) judges a finished plan against DONE_WHEN; status entries owe the same evidence standard as any done claim.
