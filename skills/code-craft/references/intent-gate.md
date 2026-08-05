# Intent Gate in Depth

A forced artifact at the behavior-change decision point. The short form lives in [code-craft](../SKILL.md); this file is the why and the worked cases.

## The rule

Before any behavior-changing edit, emit one literal line:

```
INTENT: code does <X>; the failing check expects <Y>; the spec says <Z>
```

The line must appear verbatim in your final report. If you change behavior, the report is incomplete without it. Fill all three slots by actually opening the artifacts:

- **X** = what the code does today. Read it; run it if needed. State observed behavior, not assumed.
- **Y** = what the failing check expects. Read the failing test, log line, or validator output. Quote the error.
- **Z** = what the spec demands. Read the README, docstring, design doc, or task. Quote the clause.

## When X, Y, Z disagree

The disagreement is the finding. Do NOT edit. Report the three values and stop. The user decides which is authoritative. Common splits:

- Code and spec agree, test is wrong -> the test is the suspect (not the spec); propose fixing the test.
- Code and test agree, spec is silent -> fill the gap; ask which behavior is intended.
- Test and spec agree, code is wrong -> this is the normal fix; proceed, then emit `TWINS:`.

The spec is the durable contract. When test and spec disagree, the test is the suspect.

## Worked case

A list endpoint returns insertion order; the test `TestUserList_Alphabetical` fails; the design doc says "results sorted alphabetically by name":

```
INTENT: code does return users in insertion order; the failing test
expects alphabetical order; the spec says "sorted alphabetically by name"
```

X, Y, Z agree that current behavior is wrong -> proceed to fix; emit `TWINS:` for any sibling endpoints.

## Triviality gate

A pure typo, a mechanical rename with no behavior change, or a formatter-only edit skips the gate. Note the skip in the report ("pure rename; no behavior change; INTENT gate skipped"). Any edit that could change observable behavior -- return value, exit code, log line, side effect, timing, ordering -- must pass the gate.

## Source

See also [harness-engineering](../../harness-engineering/SKILL.md) (separate reasoning from computation).
