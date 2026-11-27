---
name: verify
description: Use after completing substantive work, before claiming any work is done, or whenever a report or agent claims work is complete. Two entry modes share one mechanism — judge a completion report, or bring a working tree green through the gate pipeline — always by running checks and reading outputs. Merge judgment on a diff is the review skill.
---

# Verify Completion

Two entry modes share one mechanism: judge a completion report, or bring a working tree green. Both run checks and read outputs; neither trusts a summary, including your own.

## 1. Claims, not facts

- Treat the report as a set of claims; believe nothing you did not observe.

## 2. Re-run every claimed check

- Run each claimed command yourself and read its output, never the summary of it.
- Use the commands the project declares in its manifests, task runner, and pipeline.

## 3. Gate pipeline, one batched pass

- Run format, lint, type check, security scan, tests, and the project's own committed pre-checks in one ordered pass, discovered from its manifests and pipeline.
- Note absent tooling only after checking those declarations; a silent skip is a false pass.
- Never auto-fix a security finding; report it and escalate.

## 4. Root-cause fixes only

- Apply the narrowest fix at the cause, then re-run that stage.
- Hard bound: three fix-and-reverify iterations on one issue, then report it blocked; never re-run past the cap.

## 5. Dial to stakes

- Static checks on every source change, runtime tests when the change runs, and one end-to-end path when it crosses a real boundary.
- For high-stakes changes, prove the check can fail with a mutation probe before trusting it.

## 6. Hunt the known frauds

- A check weakened or deleted to make the suite green.
- A step skipped but reported done.
- "All tests pass" with no command or output shown.

## 7. Batch or destructive operations

- Plan the operation, validate the plan against a source of truth, then execute.

## 8. Verdict and report

- One verdict — VERIFIED / VERIFIED WITH CAVEATS / REFUTED — outcome first, with honest caveats.
- Report each stage in the fixed shape `stage | command | exit | result`, so the result is machine-scannable.

## 9. Gotchas

- Verifying by re-reading the diff only, instead of running the checks.
- Trusting a green result whose command you never saw.
- Accepting a summary in place of the output.