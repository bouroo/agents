# Completion Audit, Autonomy, and the Capability Dial

Depth for the orchestrator. The [SKILL.md](../../../agents/orchestrator.md) owns the contract; this owns the depth, loaded on demand.

## Completion audit (before any "done")

Before declaring a unit or task complete, audit the actual current state against the objective not against effort, intent, or memory of earlier work.

1. **Enumerate scope.** Restate the objective as concrete deliverables and re-derive every requirement from the user message, spec, and DONE_WHEN explicit items, named files, commands, tests, gates.
2. **Build a prompt-to-artifact checklist.** Map each requirement to the concrete evidence that would prove it (a passing command, a file, a green gate, an observed behavior).
3. **Inspect real evidence per item.** Run/read the command output, test result, file, or PR state for each row. Do not rely on a recollection that it passed.
4. **Check coverage, not just green.** A passing suite, a complete manifest, or a successful verifier is evidence **only if it covers every requirement**. A green signal over the wrong surface is a proxy, not proof.
5. **Treat uncertainty as not-done.** Any requirement that is missing, incomplete, weakly scoped, or unverified means keep working do more verification or finish the work. Do not rely on elapsed effort, partial progress, or a plausible final answer as proof.

Proxy signals to reject as sole proof of completion: passing tests that do not exercise the changed behavior, a build that succeeds without running the relevant tests, a verifier over a stale tree, a narrative summary with no re-run command.

## Autonomy and persistence

Stay with the work end-to-end within the current turn whenever feasible. Do not stop at analysis or half-finished fixes; do not end a turn while a process needed for the request is still running. Carry the work through implementation, verification, and a clear account of the outcome unless the user explicitly pauses or redirects.

Unless the user explicitly asks for a plan, asks a question, is brainstorming, or otherwise signals no code changes yet, assume they want the change made or the tools run implement, do not just propose. If the cause, risk, or fix is uncertain, say what is uncertain and what evidence is missing; do not invent a confident explanation. On a blocker, try to work through it before handing the problem back.

The limit on autonomy is the hard boundary: outward/irreversible/destructive actions still require `AUTH:` and the decide-don't-ask gate (AGENTS.md §2), and the 3-cycle hard verify bound still holds.

## Capability and effort dial (host-agnostic)

This harness pins no model or effort tier each host selects its model. What the orchestrator dials instead is **verification depth**, by complexity ([right-sizing](../../../skills/harness-engineering/references/right-sizing.md)):

| Complexity | Decompose | Verify |
|---|---|---|
| Low / Low | act directly; skip ceremony | L1; self-verify (worker) |
| Mid / Mid | small unit graph; delegate | L1/L2; `discover (review)` on demand; `validator` on demand |
| High / High | full unit graph; fan out | L1/L2/L3; `validator (verify\|judge)` required for high-stakes claims |

The dial chooses **which** controls apply, never the evidence standard: a red test beats a narrative pass at every tier.
