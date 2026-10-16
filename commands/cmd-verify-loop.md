---
name: cmd-verify-loop
description: "Verify loop (PROVE): write the oracle before the code, generate the draft, hunt it with an adversarial Verifier in a fresh context, and refine until the findings are spent. Use to give a major deliverable a verdict instead of an assertion."
---

# Agentic Verification Loop

Generation is the cheap half; verification is the bottleneck, so the agent verifies its own output before a human ever reads it. This is the **Test** stage's adversarial pass (§4, the PROVE node), composing with the [quality-gate pipeline](../skills/quality/SKILL.md) rather than replacing it — the gates prove the change builds and passes, this loop proves the change is right. **No options: fully autonomous** — no arguments, nothing to ask, no verdict to negotiate; the loop runs to one verdict or its cap, and the only stop before that is a missing Verifier, which it names rather than papers over.

## Scope

Default: one deliverable — a diff, a document, an answer that will be acted on. A trivial change stays on the gates; this loop earns its cost on work whose correctness someone would otherwise have to assume. It requires a Verifier that can read the draft without the context that produced it; where no fresh context is available, say so and stop — self-review is not the second pair of eyes, it is the same one twice.

## Loop

Cap: **three verify/refine cycles on one issue**, then hand back the draft and the log with the open finding intact — never run past the cap, never spend it to bury a finding that needs a human.

1. **Frame** — restate DONE_WHEN, then write the oracle *before* generating: a requirement-coverage list, an executable check, or a differential baseline against the prior system. Write the check before the code.
2. **Generate** — the Generator produces the draft against that oracle and hands it over as an artifact, not a conversation. The draft freezes here; every later step reads it and never rewrites it.
3. **Verify** — hand the draft and the oracle to a Verifier in a fresh context, one that never produced the draft; otherwise generator and verifier share a single misunderstanding and call it agreement. One pass hunts: requirement gaps, factual inaccuracies, internal contradictions, plausible-but-wrong implementations, and whether the check itself distinguishes correct from plausible-incorrect.
4. **Log** — every finding lands in the Verification Log carrying its evidence (command and exit code, `file:line`, or the quoted claim). An empty log is justified only by listing what was probed; silence is not success, and a deliverable that never met an adversarial pass has no verdict.
5. **Refine** — the Refiner integrates the log at the root cause, never a band-aid, and the loop returns to step 3 with the refined draft. Checks stay fast and deterministic: a slow or flaky check teaches the agent to retry rather than to fix.
6. **Report** — emit the block below; the draft and the log ship with the deliverable, so the human audits the reasoning, not just the result.

## Done =

Every oracle item passes or is refuted with evidence, the Verifier was independent of the draft, and the log names what it probed. A REFUTED verdict carries the smallest fix that would flip it; a VERIFIED WITH CAVEATS verdict names the caveat in the log, never only in the verdict.

Report every loop in this fixed, machine-scannable shape:
```
Draft: <what the Generator produced>
Verification Log: <finding + evidence | probes listed, none found>
Final Deliverable: <what the human receives>
verdict: VERIFIED | VERIFIED WITH CAVEATS | REFUTED
```

**Abort:** the cap reached on one issue with a finding still open — hand back the draft, the log, and the open finding rather than another cycle.