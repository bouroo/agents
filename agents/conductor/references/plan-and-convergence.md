# Plan Mode, Convergence, and Failure Handling

Detail for the conductor. The [SKILL.md](../../conductor.md) owns the contract; this owns the depth, loaded on demand.

## Plan Mode (unit graph)

Decompose the task into a **unit graph**. Each unit:

| field | meaning |
|---|---|
| `id` | `U1`, `U2`, ... stable across compaction |
| `behavior` | the user-visible behavior this unit delivers |
| `scope` | files/dirs the owner may touch |
| `done_cmd` | the executable check that proves the unit (a unit without one is a planning failure) |
| `deps` | unit ids that must pass first |
| `owner` | `conductor` (planning) / `coder` / `discover` |

Emit `INTENT: <user-visible behavior change>` on the first behavior-changing unit. Write `.agents/plans/{slug}/canvas.md` and `state.json`; the ledger is canonical across compaction. Choose a fan-out topology via [composition-patterns](../../../skills/harness-engineering/references/composition-patterns.md).

## State (on disk, canonical)

```
.agents/plans/{slug}/
  canvas.md           # unit graph + DONE_WHEN
  state.json          # task_slug, active_unit, units[], decision_log[]
  decision-log.md     # decisions and rationale (append-only)
  retro.md            # failure modes and harness learnings
.agents/handoff/
  {unit-id}.summary.md  # subagent handoff per unit
```

`state.json` unit entry:

```json
{
  "id": "U1",
  "owner": "coder",
  "done_cmd": "make test",
  "status": "in_progress | completed | blocked | failed",
  "evidence": { "L1": "pass|fail|na", "L2": "...", "L3": "..." },
  "handoff": ".agents/handoff/U1.summary.md",
  "state": "pending | running | passing | blocked | failed"
}
```

**Clock-in:** `ROOT=$(git rev-parse --show-toplevel) && mkdir -p "$ROOT/.agents/plans/{slug}" "$ROOT/.agents/handoff"` -> load `state.json` if it exists -> verify the git working tree -> decompose or take a read-only decision.
**Clock-out:** update `state.json` + `decision-log.md` -> verify a clean checkout -> summarize completed units and evidence.

## Convergence gates

Before issuing a final verdict, pass **Hard** (all required) and review **Advisory**:

**Hard:**
- [ ] Every unit `passing`.
- [ ] L1/L2/L3 evidence captured per unit (dialed to complexity).
- [ ] Mutation probe run and reverted.
- [ ] Git tree clean (no leftover probes/debris).
- [ ] Artifact lines owed are present (INTENT/TWINS/AUTH/PENDING).

**Advisory:**
- [ ] Spec parity (DONE_WHEN met; no scope creep).
- [ ] SCOPE respected (files touched are a subset of declared SCOPE).
- [ ] Error norms respected (no swallowed errors; no branching on error strings).
- [ ] Decision log current.

## Failure classes -- classify, then act

When a turn or subagent return fails, classify before acting:

1. **Semantic** (`done_cmd` exit != 0 after claimed pass): route to `coder (fix)` with the failing output and repro.
2. **Structural** (unit fails >= 2 times): decompose finer (re-plan) or reassign mode; pull in `discover (explore)` for surface reading.
3. **Environment / Tooling** (missing tools, permissions, network): return `blocked` with an environment hypothesis.
4. **Spec Ambiguity** (contradictory/missing requirements): route to `discover (explore)`, or present precise choices to the user if undecidable.
5. **Recurring** (same class across >= 2 units): halt; append the pattern to `retro.md`; upgrade harness controls.

## Routing cheatsheet

| Task shape | Route |
|---|---|
| Implement/fix a behavior within SCOPE | `coder (implement|fix)` |
| Verify a claim with executable evidence | `coder (verify)` |
| Adversarially judge a high-stakes "done" | `coder (judge)` |
| Explore unfamiliar code / map surface | `discover (explore)` |
| Version-sensitive external answer | `discover (lookup)` |
| Review a diff against the rubric | `discover (review)` |
| Bounded edit (typo/rename/format/one-line, one file) | conductor direct (natural) |
