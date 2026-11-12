# Plays — Test

> Load on demand from [delivery](../SKILL.md): the practices that give a session its own feedback loop and that regression-test the agent's own configuration.

## Stage 4 — Test

### Give the session a feedback loop

**What changes.** Every session checks its own work before a human sees it, and the configuration that steers the agent gets regression-tested like the code it writes. Always give the agent a way to verify its own work — tests, a build, a screenshot diff. The session checks its own work and fixes its own mistakes before an engineer sees them.

The feedback loop is not the same as a verifier subagent. The loop runs through the whole task as many times as the work; the verifier subagent packages the final check by running a fresh context window once the session believes the work is done, so the verdict is not colored by the assumptions that produced the code.

**Getting started.** A test suite and a build that run locally with one command each. For interface work, the agent needs a way to see the result — a browser tool or a screenshot utility.

**Steps.**

1. If checking the work today takes a sequence of commands and environment knowledge, wrap it in a single target such as the repository's unit-test target, and make it exit non-zero on failure.
2. In the project context file's Commands section, list each command with an example of a healthy output.
3. Make the target quantifiable so the agent can check the work without asking: "all status tests pass", "the screenshot matches the attached mock", "the endpoint returns success with the new field".
4. For bug fixes, write the failing test first. Ask for the bug to be reproduced as a test, run it, and confirm it fails for the reason expected. Commit that test. Only then ask for a fix without editing the test, with a pre-action check enforcing the restriction. A test that existed before the fix, and that the agent could not rewrite, is proof the bug is gone.
5. For interface work, close the loop with a visual check: implement, screenshot, compare, adjust. Two or three rounds is normal, and the result should improve with each one.
6. Make verification part of "done". The instruction lives in the project context file. Run the checks before reporting a task complete, and show the output.
7. Protect the loop itself, because an agent fixing code must not be able to weaken the check on that code. A pre-action check that blocks edits to test files during a fix task does this; the alternative is to check the diff in review and reject any change that touches a test.

**Governance.** *What is enforced:* verification before a task is reported done, and the block on the agent editing test files during a fix, implemented as pre-action checks where the organization wants them guaranteed. *What the evidence is:* the literal output of the test command, the build log, or the screenshot diff that the agent ran and pasted, so the evidence comes from the toolchain. *Where it is logged:* in the session transcript, which the observability export forwards to the organization's stack, and in the change request's check run, where the reviewer and any later auditor can both see it. *Who approves:* the code owner reviewing the change request, who can concentrate on intent and risk because the mechanical evidence is already attached.

**Measure.** *Leading:* first-pass continuous-integration success rate for agent-written changes, which the pipeline already supports. *Lagging:* review time per change request, which should fall once the tests catch what reviewers used to catch, and the change failure rate from an incident tracker. Read both: a higher first-pass rate with unchanged review time means the pipeline is green because the checks are weak, not because the work is better.

### Continuous evals

**What changes.** Evals are the AI-native equivalent of stage-gate quality assurance: a suite that runs whenever the agent's configuration changes. When a new model is swapped in or a prompt is rewritten, the eval suite says whether the agent still does the work to the same standard. Treat the suite as live: as models improve, cases that once discriminated stop doing so, and new ones must be added from ongoing monitoring.

**Getting started.** The project context file and the feedback loop. Infrastructure: a continuous-integration pipeline that can run the agent non-interactively, and a model-access budget for eval runs.

**Steps.**

1. The platform engineer collects 20 to 50 real tasks from recent work with the expected outcome.
2. Write each task as an eval: the prompt plus the checks that define acceptable — tests pass, lint clean, behavior unchanged, policy followed.
3. The suite runs non-interactively in the pipeline on a schedule and on any change to the context file, skills, or pre-action checks, since that configuration steers the agent and deserves the regression testing code gets.
4. Gate configuration changes on the results. A skill change that drops the pass rate gets reviewed before it merges.
5. Each production incident gets an eval, written by the team that owned the incident, and stays in the suite as a regression test.

**Governance.** *What is enforced:* the pass-rate threshold, enforced as a merge check, so a configuration change that lowers the standard cannot merge on its own. *What the evidence is:* the suite's own report, one per run, with the pass rate and the per-case verdicts. *Where it is logged:* the pipeline's run history, so results can be compared over time. *Who approves:* the team that owns the configuration change; the eval suite is the check, not the approver.

**Measure.** *Leading:* the eval pass rate over time, reported by the suite on every run, and how long a production incident takes to become a permanent eval. *Lagging:* regressions caught in the pipeline compared with regressions found in production, derived from the incident tracker. Read both: a rising pass rate with unchanged production regressions means the suite has stopped discriminating.
