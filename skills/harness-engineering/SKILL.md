---
name: harness-engineering
description: >
  Harness-engineering norms that stop capable agents from failing: repo-as-record, split
  instructions, WIP=1, executable completion evidence, three-layer termination, cross-session
  state persistence, observability, and clean-session exits. Use when designing agent workflows,
  checkpoints, or verification rules, or when an agent risks overreach, premature victory, or
  context loss. Grounded in the OpenAI and Anthropic harness canon and the 12-lecture "Learn
  Harness Engineering" series.
compatibility: opencode, kilo
disable-model-invocation: false
---

# Harness Engineering — Agent-Loadable Norms

A strong model still fails when the closed-loop working system around it is weak. The harness does not make the model smarter; it constrains behavior, preserves context, defeats premature victory, verifies with executable evidence, and makes runtime observable. Load this topic doc on demand when designing agent workflows, checkpoints, or verification rules.

## 1. Repository as System of Record

**Why:** Conversation state is lost every session; decisions and evidence must survive.

**Rules**
- Treat files, not chat, as the system of record.
- Write decisions to a decision log under `.agents/plans/`.
- Persist progress, verification results, and next actions in versioned artifacts.
- Make every meaningful state change a diff that can be reviewed, reverted, or branched.
- Restart work from repo files; do not rely on memory of prior turns.
- Name artifacts so their purpose is obvious: `decision-log.md`, `progress.md`, `verification-report.md`.
- Link related artifacts explicitly; never assume the next session will guess relationships.

**Source:** Lecture 1 (OpenAI: "operational record"; Anthropic: "handoff files").

## 2. Split Instructions; No Giant File

**Why:** Long mid-file instructions are lost; routing and constraints must sit at boundaries.

**Rules**
- Keep `AGENTS.md` to 50–200 lines: overview, hard constraints, links to topic docs.
- Put detail in on-demand topic docs like this one.
- State every rule with `SOURCE` (why added), `APPLICABILITY` (when needed), and `EXPIRY` (when removable).
- Audit rules like technical debt; remove or refresh stale ones.
- Place critical constraints at the TOP or BOTTOM of a file; never bury them mid-file.
- Use descriptive filenames and headings so the right doc loads fast.
- Cross-reference rather than duplicate; one source of truth per rule.

**Source:** Lecture 4 / "Lost in the Middle" (Liu et al., 2023).

## 3. Keep Context Alive Across Sessions

**Why:** Each session starts with wiped short-term memory; the cost of reconstructing state dominates.

**Rules**
- Clock in: read progress log, decision log, and last verification state before writing code.
- Clock out: update progress log, decision log, and next action before ending.
- Persist: what's done/in-progress/blocked, the "why" behind decisions, verification results, and the very next executable step.
- Use git commits as checkpoints after every verified completion.
- Target: new session reaches executable state in ≤ ~3 minutes.
- Short tasks finish in-session; tasks needing > ~60% of the window prepare a handoff.
- Beware "context anxiety": rushed finishes near the window limit. A clean reset often beats lossy compaction.
- Write handoffs in the imperative: "Next session runs X, then Y, then verifies Z."

**Source:** Lecture 5.

## 4. WIP = 1; Draw Task Boundaries

**Why:** Parallel unfinished work lowers completion rate and leaves the repo in an unclean state.

**Rules**
- Activate exactly ONE task at a time.
- Finish and verify the active task before starting the next.
- Completion evidence must be executable ("curl returns 201", "test passes"), not subjective.
- Externalize a machine-readable scope surface with states: `not_started`, `in_progress`, `blocked`, `passing`.
- Track Verified Completion Rate: `VCR = verified / activated`.
- Block new activations when `VCR < 1.0`.
- Prefer less work fully finished over more work half-done.
- Define "done" as a checklist before starting; accept no fuzzy exits.
- If a task blocks, record the blocker, notify if needed, and move only to an unblock action.

**Source:** Lecture 7.

## 5. Prevent Premature Victory

**Why:** Agents are systematically overconfident; the harness, not the agent, must judge completion.

**Rules**
- Externalize the termination judgment; never trust a "feels done" signal.
- Run three-layer validation in order: L1 syntax/static analysis, L2 runtime behavior (tests, app start, critical paths), L3 system-level end-to-end.
- Do not skip a layer.
- Error feedback must be actionable and include repair steps: not "test failed" but "POST /x returned 500 — check env var Y; template at path Z".
- Do not refactor until core functionality is verified.
- Separate the worker from the checker: use an independent evaluator for verification.
- Require a failing test or reproduction before fixing a bug.
- Capture the exact command, expected output, and actual output for every verification claim.

**Source:** Lecture 9.

## 6. Observability Belongs in the Harness

**Why:** Without runtime signals, you cannot tell whether a run succeeded, partially succeeded, or left a mess.

**Rules**
- Capture signals the harness can act on: did it start and reach ready?
- Did critical paths execute?
- Were side effects (DB writes, files) correct?
- Were temporary resources cleaned up?
- Log structured, actionable fields.
- Never log secrets or credentials.
- Use logs for debugging, metrics for performance, and traces for request flow.
- Emit readiness probes for long-running services.
- Verify side effects by reading back what was written, not by trusting the write call.

**Source:** Lecture 11.

## 7. Every Session Leaves a Clean State

**Why:** A dirty checkout destroys the next session's startup budget and breeds silent drift.

**Rules**
- Before clocking out: confirm standard startup still works.
- Confirm standard verification still runs.
- Update the progress log.
- Leave no half-finished work unrecorded.
- Ensure the next session can continue without manual fixes.
- Prefer a small, committed, passing checkpoint to a large, unverified, half-done change.
- Revert speculative edits rather than leaving them uncommitted.
- State the next action explicitly enough that another agent could pick it up.

**Source:** Lecture 12.

## 8. Context Budget & Compaction

**Why:** Every token in `AGENTS.md` and the system prompt persists across auto-compaction; detail buried there is paid for on every turn and is the first thing lost when context pressure rises.

**Rules**
- Treat `AGENTS.md` as a router: overview, hard constraints, and links to on-demand skill docs. Keep it ≤ ~200 lines.
- Push detail into skill docs (like this one) that load only when relevant; never inline a skill's body into `AGENTS.md`.
- Prefer `@file` / `{file:...}` references and lazy on-demand loading over pasting large bodies into the prompt.
- Run compaction before major transitions, not mid-step: a clean summary at a phase boundary beats lossy compression under deadline pressure.
- The most recent turns survive compaction; put the next executable action in the latest assistant turn or a tracked file — never rely on mid-history instructions being retained.
- When context is tight, a clean reset from repo files (clock-in) beats continuing on a lossy, half-remembered thread.

**Source:** Kilo — Context Condensing (https://kilo.ai/docs/customize/context/context-condensing); "Lost in the Middle" (Liu et al., 2023).

## Quick Checklist (clock-in / clock-out)

**Clock in**
- [ ] Read `AGENTS.md` and relevant topic docs.
- [ ] Read progress log, decision log, and last verification results.
- [ ] Identify the single active task from the scope surface.
- [ ] Run standard startup/verification to confirm baseline passes.
- [ ] Set the active task state to `in_progress`.

**Clock out**
- [ ] Verification passes at L1, L2, and L3 for the active task.
- [ ] Progress log and decision log are updated.
- [ ] Standard verification still runs on the current state.
- [ ] No half-finished work is left unrecorded.
- [ ] Next session has an explicit first action.
- [ ] Active task state is `passing` or `blocked` with a recorded reason.

## References

- OpenAI: Harness Engineering — https://openai.com/index/harness-engineering/
- Anthropic: Effective harnesses for long-running agents — https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Anthropic: Harness design for long-running application development — https://www.anthropic.com/engineering/harness-design-long-running-apps
- Learn Harness Engineering (12 lectures) — https://walkinglabs.github.io/learn-harness-engineering/en/
- Lost in the Middle (Liu et al., 2023) — https://arxiv.org/abs/2307.03172
- Kilo — Prompt Engineering — https://kilo.ai/docs/customize/prompt-engineering
- Kilo — Context Condensing — https://kilo.ai/docs/customize/context/context-condensing
