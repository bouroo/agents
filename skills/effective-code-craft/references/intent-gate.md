# Intent Gate in Depth

A forced artifact at the behavior-change decision point. The short form lives in [effective-code-craft](../effective-code-craft/SKILL.md); this file is the why and the worked cases.

## The rule

Before any behavior-changing edit, emit one literal line:

```
INTENT: code does <X>; the failing check expects <Y>; the spec says <Z>
```

The line must appear verbatim in your final report. If you change behavior, the report is incomplete without it.

Fill all three slots by actually opening the relevant artifacts:

- **X** = what the code currently does. Read it. Do not infer.
- **Y** = what the failing check expects. Read the failing test, log line, or
  validator output. Quote the error.
- **Z** = what the spec says. Open the README, docstring, design doc, or
  behavior contract. If none exists, say so -- the absence is the third slot.

## Authority order

When X, Y, and Z disagree, the agent does NOT edit. The disagreement is the
finding. The ladder that resolves it:

1. **Explicit user statement** -- the user named the intended behavior in
   this session. Wins over everything.
2. **Spec** -- the written contract (README, docstring, design doc, ADR).
3. **Tests** -- the executable specification, but only when they express
   intent, not when they assert current behavior.
4. **Current code behavior** -- what the code does now. The lowest rung; it
   is the thing being questioned.

A framing like "fix the code" or "make the tests pass" is **not** a statement
of intended behavior. It names an action, not a destination. Tests that
contradict the spec do not promote themselves above the spec; the ladder
still applies.

### Example at each rung

- **User statement wins.** User: "rate limit to 100 req/min, not 10." Spec
  says 10. Test asserts 10. Edit toward 100 -- the user just promoted it.
- **Spec wins over tests.** Spec says "returns 400 on bad input." Test
  asserts 200. Edit the test (and code) toward 400, then report the
  disagreement as a finding.
- **Tests win over current code.** Spec is silent. Tests assert
  "filters empty list." Code panics on empty list. Edit the code; the
  test is the only written contract.
- **Current code is the only signal.** No spec, no tests, no user
  statement. Stop and ask. Do not infer intent from "what the code does."

## Worked examples

### Agree -- proceed

The user reports: "the user list is unsorted, but the spec says
alphabetical-by-name and the test `TestUserList_Alphabetical` is failing
with `got [Bob, Alice], want [Alice, Bob]`."

```
INTENT: code does return users in insertion order; the failing test
TestUserList_Alphabetical expects alphabetical order; the spec says
"users are listed alphabetically by name"
```

X, Y, Z all point the same direction. Proceed: sort by name, run the
test, capture command + output, report.

### Disagree -- finding, not edit

The user reports: "the CLI crashes on no-arg; the test expects exit 0."

Spec is silent on no-arg behavior. The test was added last week by
whoever touched the CLI last. Reading the spec introduction: "the CLI is
strict -- unknown args produce a usage error and exit 2."

```
INTENT: code does exit 1 on no args; the failing test expects exit 0
on no args; the spec says "unknown args produce a usage error and exit 2"
```

X and Z agree (both reject no-args with a nonzero exit). Y disagrees
(test expects 0). The disagreement is the finding: the test encodes a
behavior the spec rejects. Do not edit the code to satisfy Y. Report:

> INTENT check failed. Code and spec agree on exit-code-on-no-args.
> Test `TestCLI_NoArg` expects exit 0, which contradicts the spec. The
> test should be removed or corrected to match the spec; the code is
> already correct. Recommend updating the test (or the spec, if the
> user wants the looser behavior).

## Framing is not behavior

The most common trap: a task framed as "fix the code" or "make the
tests pass" tempts the agent to treat Y (the test) as the destination.
This inverts the ladder -- tests become the authority over spec, and
spec becomes decoration. They are not decoration.

A test is a snapshot of someone's understanding at the time it was
written. The spec is the durable contract. When they disagree, the test
is the suspect, not the spec.

## Triviality gate

A pure typo, a mechanical rename with no behavior change, or a
formatter-only edit skips the gate. The agent notes the skip in the
report ("pure rename; no behavior change; INTENT gate skipped"). Any
edit that could change observable behavior -- return value, exit code,
log line, side effect, timing, ordering -- must pass the gate.

## Source

fable-method -- Sahir619/fable-method. See also
[harness-engineering](../harness-engineering/SKILL.md) §11 (separate
reasoning from computation) and §5 (prevent premature victory).
