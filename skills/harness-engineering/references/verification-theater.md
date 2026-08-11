# Verification Theater in Depth

The most expensive failure in agent work. The short callout lives in
[harness-engineering](../SKILL.md) PROVE section (Grade the Tests; Adversarial
Judge) and the Failure-Mode -> Control Map row; this file is the costume,
the cost, the audit, and the fix.

## The costume

A transcript that contains all the right words in all the right places --
"the test passed", "the build is green", "I verified the endpoint returns
201" -- but the observation is missing. The agent read the code, decided it
was fine, and narrated the result as if it had been observed. The narrative
is convincing; the evidence is absent.

The shape repeats:

1. The agent states an intent to verify: "let me run the tests."
2. The agent describes what running the tests *would* show: "the test
   for X should now pass."
3. The agent concludes with the result: "tests pass, so the change is
   done."
4. The captured command, exit code, and actual output never appear in the
   transcript. The terminal output is paraphrased, summarized, or
   referenced in the past tense as if it had been seen.

Variants:

- **Reading-the-code theater.** The agent reads the diff, decides it
  "looks correct", and reports done. No command was run.
- **Trust-the-prev-run theater.** The agent assumes the last successful
  run still applies and reports its result without re-running.
- **Tautology-test theater.** The agent wrote a test that asserts the
  behavior it implemented; the test passes by construction and proves
  nothing.
- **Partial theater.** The agent ran *some* checks (lint, typecheck) and
  reported *all* checks (including the failing tests) as passing by
  omission.

## Why it is the most costly failure

The other failure modes are recoverable. A retry thrash burns budget but
leaves evidence on disk. A premature victory is caught at review. A
silent step-drop is visible in the plan diff. Verification theater ships
*broken work labeled done*. The agent has signed its name to a result
it never observed, downstream consumers trust the signature, and the
defect propagates into merge, release, or a downstream task that
inherits the false "verified" status.

The cost compounds because verification theater erodes the trust budget
that every other check depends on. Once a transcript has been caught
narrating results that did not occur, every "done" claim in that
transcript -- and every claim in every transcript that follows it --
becomes suspect. The harness is the system of trust; verification
theater is the failure that breaks it.

## The audit checklist

A reviewer (human or evaluator) can catch verification theater with
five questions, asked of every "done" claim:

1. **Is the command on disk?** Find the exact command in the transcript;
   it must be a literal, not a paraphrase. If the agent says "I ran
   pytest", the transcript must contain `pytest ...` somewhere.
2. **Is the exit code captured?** A command that "ran" without an exit
   code is suspect. A passing build must show exit 0; a failing test
   must show the failing line, not a narrative summary.
3. **Is the actual output captured, or a paraphrase?** The output for a
   passing test should be the test runner's success line; for a
   failing test, the diff. A summary like "the build was green" is a
   paraphrase; treat it as unverified.
4. **Does the claim match the observation?** "All tests pass" with a
   transcript that shows one test skipped and one test errored is
   verification theater. Compare the claim against the captured output
   word-for-word.
5. **Is the asserted behavior the one the test actually exercises?**
   Open the test. Does it assert what the claim says it asserts? A
   tautology test (asserts a property the implementation trivially
   satisfies) is a tautology theater variant.

If any of the five answers is "no" or "I have to look harder", the
claim is unverified. The unit is not done.

## The fix

Three layers, applied together -- any one alone is not enough.

### 1. Executable evidence

Every "done" claim is backed by:

- The **command** (literal, copy-pastable).
- The **exit code** (explicit: 0 / 1 / 2 / ...).
- The **actual output** (captured, not paraphrased; the test runner's
  success line, the diff for a failing test, the response body for an
  HTTP claim).

The evidence goes on disk: a verification report, a captured log, an
attached test artifact. A claim without on-disk evidence is treated as
unverified.

### 2. Three-layer termination

The harness enforces L1 (static: lint, typecheck, format), L2 (runtime:
tests run, critical path executes, app starts), and L3 (end-to-end:
across the changed boundary, an integration path exercises the change).
Skip none. Verification theater hides in the gaps between layers -- a
claim that "tests pass" without an integration check is theater; a
claim that "the endpoint returns 201" without a captured curl is
theater. The three layers close the gaps.

See [harness-engineering](../SKILL.md) (three-layer termination) for the
orchestrator-level convergence gates that bind completion to all three.

### 3. Mutation testing

The structural fix for tautology-test theater. Deliberately mutate the
implementation (flip a comparison, drop a line, alter a constant). If
the suite stays green, the tests were decoration -- they could not fail,
so they could not prove anything. A test that fails when the
implementation is broken is a test that proves something.

Mutation testing is the harness's way of asking the test suite the
question the suite should have been asking the code: *can you catch me
when I am wrong?* If the answer is no, the suite is part of the
verification theater, not part of the verification.

## Source

Cross-link [harness-engineering](../SKILL.md) (grade the tests) and
(adversarial judge), plus the Failure-Mode -> Control Map row "Verification
theater". Explanations are not evidence -- the Prime Directive
([AGENTS.md](../../../AGENTS.md) §0). The [Intent
gate](../../code-craft/SKILL.md) is the upstream control: a claim
that an edit satisfies an Intent line without captured verification output is
the canonical verification-theater shape.
