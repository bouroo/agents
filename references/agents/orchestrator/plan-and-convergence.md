# Plan Mode, Convergence, and Failure Handling

Detail for the orchestrator. The [SKILL.md](../../../agents/orchestrator.md) owns the contract; this owns the depth, loaded on demand.

## Plan Mode (unit graph)

Decompose the task into a **unit graph**. Each unit:

| field | meaning |
|---|---|
| `id` | `U1`, `U2`, ... stable across compaction |
| `behavior` | the user-visible behavior this unit delivers |
| `scope` | files/dirs the owner may touch |
| `done_cmd` | the executable check that proves the unit (a unit without one is a planning failure) |
| `deps` | unit ids that must pass first |
| `owner` | `orchestrator` (planning) / `worker` / `validator` / `discover` |

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
  "owner": "worker",
  "done_cmd": "make test",
  "status": "in_progress | completed | blocked | failed",
  "evidence": { "L1": "pass|fail|na", "L2": "...", "L3": "..." },
  "verified_by": "worker | validator | null",
  "handoff": ".agents/handoff/U1.summary.md",
  "state": "pending | running | passing | blocked | failed"
}
```

**Clock-in:** `ROOT=$(git rev-parse --show-toplevel) && mkdir -p "$ROOT/.agents/plans/{slug}" "$ROOT/.agents/handoff"` -> load `state.json` if it exists -> verify the git working tree -> decompose or take a read-only decision.
**Clock-out:** update `state.json` + `decision-log.md` -> verify a clean checkout -> summarize completed units and evidence.

**Compaction rule (canonical across compaction):** when the window strains, `state.json` + `canvas.md` + `decision-log.md` + handoff summaries ARE the execution state. Every field a fresh context needs to resume deterministically (active unit, per-unit status + evidence pointers, pending artifact gates, SCOPE) survives compaction because it is on disk, not in conversation. Never summarize the session into prose; re-read the ledger.

## Convergence gates

Before issuing a final verdict, pass **Hard** (all required) and review **Advisory**:

**Hard:**
- [ ] Every unit `passing`.
- [ ] L1/L2/L3 evidence captured per unit (dialed to complexity).
- [ ] High-stakes units independently verified by `validator` (not just the worker's self-verify).
- [ ] Mutation probe run and reverted.
- [ ] Git tree clean (no leftover probes/debris).
- [ ] Artifact lines owed are present (INTENT/TWINS/AUTH/PENDING).

**Advisory:**
- [ ] Spec parity (DONE_WHEN met; no scope creep).
- [ ] SCOPE respected (files touched are a subset of declared SCOPE).
- [ ] Error norms respected (no swallowed errors; no branching on error strings).
- [ ] Decision log current.

## Failure classes classify, then act

When a turn or subagent return fails, classify before acting:

1. **Semantic** (`done_cmd` exit != 0 after claimed pass): route to `worker (fix)` with the failing output and repro.
2. **Structural** (unit fails >= 2 times): decompose finer (re-plan) or reassign mode; pull in `discover (explore)` for surface reading.
3. **Environment / Tooling** (missing tools, permissions, network, provider/model routing): return `blocked` with an environment hypothesis. Probe with a minimal packet on a known-good path before blaming doctrine; a provider-dependent failure is host-side by definition.
4. **Spec Ambiguity** (contradictory/missing requirements): route to `discover (explore)`, or present precise choices to the user if undecidable.
5. **Early Return** (empty or thin subagent return; no executed `done_cmd`; `Early-stop:` marker): triage per the early-return protocol in the [orchestrator contract](../../../agents/orchestrator.md) (one minimal-probe redispatch, then split units or hand back). Marked take-over allowed for bounded work; never silent, never high-stakes.
6. **Recurring** (same class across >= 2 units): halt; append the pattern to `retro.md`; upgrade harness controls.

## Routing cheatsheet

| Task shape | Route |
|---|---|
| Implement/fix a behavior within SCOPE | `worker (implement|fix)` |
| Self-verify work with executable evidence | `worker (verify)` |
| Independently verify a high-stakes "done" | `validator (verify)` |
| Adversarially judge claimed evidence / hunt frauds | `validator (judge)` |
| Explore unfamiliar code / map surface | `discover (explore)` |
| Version-sensitive external answer | `discover (lookup)` |
| Review a diff against the rubric | `discover (review)` |
| Bounded edit (typo/rename/format/one-line, one file) | orchestrator direct (natural) |
| Thin/empty subagent return with analysis | accept analysis, split units, re-delegate (marked take-over only if bounded) |
| Multi-step workflow demand | split into units first; never delegate a whole workflow as one packet |
