# Governed Self-Evolution (GROW)

> Load on demand from [verification](../SKILL.md): the machinery behind the GROW node — how the system changes the system, under what guardrails, and what it may never change alone. Agents propose; anchors and gates accept.

## The loop to beat

Self-evolution done wrong is the loop validating itself: an agent notices a failure, edits its own instructions, and reports the harness improved — with the edit as its only evidence. Every story of runaway or degraded self-modification is this shape. The corrective is structural, not tonal: **GROW is a graph, not a vibe** — a closed cycle whose every step closes on evidence and whose every authority chain terminates in an anchor.

## The evolution cycle

| Step | Does | Closes on |
| --- | --- | --- |
| **Instrument** | catalog the failure in `.agents/plans/{slug}/retro.md` — the trigger, the wrong behavior, the rule violated (cited by rule, never rottable path), the recurrence count | the failing evidence itself |
| **Propose** | convert the finding into a deterministic gate or rule change as a reviewed diff to the harness (a check, a flowchart node, a table row) | the diff; one line of rationale per change |
| **Validate** | run the new gate against the recorded failures — it must fail on the old evidence and pass on good runs; adversarial judging per [verification](../SKILL.md) | command + exit code + output on both sides |
| **Commit** | land versioned (git history is the rollback), noted in the changelog, retro closed with the gate's location | a green gates run on the whole repo |

An uncommitted proposal is a pending item, not an improvement; a committed one without validate-step evidence is fraud by the evidence audit.

## Cadence: what may change, when

- **Intra-episode** (inside one session): state under `.agents/` — checkpoints, scratch notes, a scoped run's own checklist. Evolve freely; it dies with the episode and touches no one else.
- **Inter-episode** (doctrine, gates, skills, shared instructions — what future runs execute): evolve only through the full cycle above, and only when the evidence clears the recurrence bar — a failure seen **twice or more**, or one whose cost was severe enough to catalog immediately. A first-time stumble is an episode note, not a doctrine edit.

This split is the harness analogue of the wayfinder rule that decisions change one ticket at a time: the machinery that future runs execute must not churn on single-run noise.

## What may never self-modify

- **Anchors.** A step that benefits from a rule may not rewrite the rule: spec clauses, the user's words, red tests, and captured evidence are read-only to the machinery (the [graph grammar's](../../graph-engineering/SKILL.md) anchor rules). Target changes route to the anchor's owner.
- **The evidence standard.** No evolution may weaken L1/L2/L3, the caps, or the audit questions — a gate may get stricter; loosening is a user decision (`AUTH:`).
- **Verification's independence.** The role that validates an evolution may not be the role that proposes it — the same separation teamwork demands of implementer and auditor.

## At model upgrades: the Kirby audit

Every control is a bet that some failure keeps happening. When a stronger model lands, re-audit the accumulated gates: cut the ones whose failure class the new model no longer produces, tighten the ones it still does. The harness shrinks as models improve — an evolution pass that only ever adds controls is not done.

## Failure modes

| Mode | Looks like | Fix |
| --- | --- | --- |
| Prompt tweaking as evolution | nudging wording after each failure, nothing durable | a durable failure is a gate; a one-off is an episode note |
| Gate theater | new check that passes the code that prompted it *and* everything else | validate against the recorded failures — it must fail on them |
| Self-granted loosening | "the bound was too strict, I'll allow 5 cycles now" | evidence-standard changes need `AUTH:` |
| Churn | doctrine edited every session | the recurrence bar; batch noise into episode notes |
| Untracked control | rule enforced by habit, absent from files | if it matters, it is a gate; if not, delete it |

## Cross-references

- [verification](../SKILL.md) the GROW node this file works out; judging an evolution proposal is adversarial judging like any done report.
- [graph-engineering](../../graph-engineering/SKILL.md) the anchor and cap grammar this cycle inherits.
- [wayfinder](../../wayfinder/SKILL.md) cross-session efforts keep their decisions one ticket at a time; doctrine keeps its changes one validated gate at a time.
