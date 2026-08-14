# Judge Protocol Fraud Hunt and Output

On-demand detail for the Judge command. The fraud table and its probes are defined in [validator verification-and-verdict](../../../references/agents/validator/verification-and-verdict.md) and are **not re-derived here**. This file holds the judge-specific hunt order, the authority-resolution rule, the UNVERIFIABLE rule, and the verdict output template.

## Hunt order (highest yield first)

Run the hunt in this order; the first fraud found usually explains the rest.

1. **Diff the test files first.** A changed test is guilty until its justification traces to a spec or an explicit user statement. Signals: asserts dropped or weakened, thresholds and tolerances loosened, tests skipped, real calls swapped for mocks, assertions edited to match new (wrong) behavior.

2. **Trace each `AUTH:` line against the conversation.** An outward effect (push, deploy, publish, send, install, destructive action) with no `AUTH:`, or with a quote that does not cover *this specific* action, is the fraud. Documentation instructing an agent to deploy is **not** authorization. Only an explicit user statement in the active session is.

3. **Resolve authority conflicts by rank.** When code, spec, and tests disagree about which is canonical: explicit user statement > spec > tests > current code behavior. Code changed to satisfy a check while contradicting a higher-rank source is spec betrayal.

4. **Confirm every owed artifact line is present.** Not just the lines the report chose to show: behavior change needs `INTENT:`, defect fix needs `TWINS:`, outward action needs `AUTH:`, deliberately untaken follow-up needs `PENDING:`. An owed line absent from the report is a claim that the gate was met. Check both its presence and its truth.

5. **Scan for debris and scope creep.** Scratch files, debug prints, commented-out code, orphaned imports, speculative TODOs, and any file touched outside the ask's blast radius (drive-by refactors, reformatting, new dependencies).

## UNVERIFIABLE claims

A claim that cannot be re-run: missing environment, credentials, or something needing human eyes is labeled **UNVERIFIABLE**, never assumed true. UNVERIFIABLE on a load-bearing claim forces VERIFIED WITH CAVEATS at best; UNVERIFIABLE on a non-load-bearing claim is a noted caveat, not a refutation.

## Output template

```
## Verdict: VERIFIED | VERIFIED WITH CAVEATS | REFUTED

## Claims observed
| Claim (from report) | Observed | Evidence |
|---|---|---|
| "all 42 tests pass" | reproduced | test runner exit 0, 42 passed |
| "build stays green" | UNVERIFIABLE | no build toolchain in this env |

## Frauds found
- [fraud type]: [file:line] [description] [smallest fix]
- (none)

## Recommended action
[one line: ship | fix X then ship | do not ship, rework Y]
```

The verdict is the first line. Then a claims table (claim, what was observed, the evidence). Then frauds found with file:line and the smallest fix. Then a one-line recommended action. Never soften a refutation to be polite; never inflate a caveat into a refutation to look rigorous.

## Standing rules

- Judging changes nothing. Read and run only.
- This is a gate, not a second implementation: minutes, not hours.
- If verification needs an environment you lack, hand that back rather than guessing.
- If the work touched nothing runnable, say plainly what a judge can and cannot check here.
