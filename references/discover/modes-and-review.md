# Discover Modes and Review Rubric

Depth for discover. The [SKILL.md](../../agents/discover.md) owns the contract; this owns the detail.

## explore (THINK)

Goal: give the orchestrator enough to decide without reading the code itself.

Return:
- **Locations:** exact file paths + line ranges for the relevant surface.
- **Shape:** 2-5 sentences on how the code is organized and how it works.
- **Coupling:** what else touches this surface; what would ripple from a change.
- **Risk:** sharp edges, invariants, concurrency, error-handling conventions the worker must match.

Name the surface you actually inspected. Never generalize from a grep count ("appears 12 times" without reading those sites is not exploration).

## lookup (THINK)

Goal: answer a version-sensitive or external question with grounded confidence.

Return:
- **Answer:** the fact, stated plainly.
- **Source:** URL + the version/release you pinned it to.
- **Repo grounding:** how it maps to this repo's dependencies/config (versions in manifests, lockfiles, CI).
- **Caveats:** where the answer could be wrong (version drift, config override, platform).

If sources conflict, say so and pick the most authoritative. Do not present an inference as a fact.

## review (PROVE)

Read the spec, the diff plus its neighbors, SCOPE, assumptions, and the worker's verification handoff. Do not re-run commands. Grade every rubric row; any missing grade is a failure. Findings include severity and a concrete location/repro. If evidence is stale or incomplete, route to `worker (verify)` (or `validator` for independent re-execution).

| # | Grade | What "pass" requires |
|---|---|---|
| 1 | spec-parity | DONE_WHEN met; no scope creep; no spec betrayal |
| 2 | boundary | SCOPE respected; files touched are a subset of declared SCOPE |
| 3 | error-norms | no swallowed errors; guard clauses where the codebase uses them; wrapped propagation with context; no branching on error strings |
| 4 | test-posture | happy + error + edge paths covered; at least one e2e across a real boundary; tests assert behavior, not implementation |
| 5 | l1l2l3-evidence | command + exit code + output captured per layer, dialed to complexity |
| 6 | artifact-lines | INTENT/TWINS/AUTH/PENDING owed are present |
| 7 | assumptions | assumptions made explicit; no silent guesses |

If a red test conflicts with a narrative pass, the red test wins and routes to `worker (fix)`.

## When you get stuck

Return `blocked`:

1. **Repro:** the minimal unanswered question, missing source, or smallest scope exposing the ambiguity.
2. **Hypothesis:** one sentence naming the spec gap, missing primary citation, unmet dependency, unavailable runtime evidence, or environment constraint.

Do not invent an answer or cross the source/toolchain boundary to obtain one.
