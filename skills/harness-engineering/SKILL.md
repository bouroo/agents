---
name: harness-engineering
description: >
  Harness-engineering norms that stop capable agents from failing: repo-as-record, split
  instructions, WIP=1, executable completion evidence, three-layer termination, cross-session
  state persistence, observability, and clean-session exits — plus the design vocabulary for
  building harnesses (feedforward guides vs feedback sensors; computational vs inferential
  controls), gates-over-prompts, separating reasoning from computation, grading tests via
  mutation testing, and engineering the whole lifecycle. Use when designing agent workflows,
  checkpoints, verification rules, or orchestrator agents. Grounded in the OpenAI/Anthropic
  harness canon, Martin Fowler's harness-engineering model, the Salesforce agentic-reliability
  patterns, and the 12-lecture "Learn Harness Engineering" series.
compatibility: opencode, kilo
disable-model-invocation: false
---

# Harness Engineering — Agent-Loadable Norms

A strong model still fails when the closed-loop system around it is weak. The harness does not make the model smarter; it constrains behavior, preserves context, defeats premature victory, verifies with executable evidence, and makes runtime observable. Load this topic doc on demand when designing agent workflows, checkpoints, verification rules, or orchestrator agents.

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
- Prune stale tool outputs and large pasted content between turns; they consume the window forever if left.
- Run compaction before major transitions, not mid-step: a clean summary at a phase boundary beats lossy compression under deadline pressure.
- Where supported, summarize with a cheaper or larger-context model than the working agent.
- The most recent turns survive compaction; put the next executable action in the latest assistant turn or a tracked file — never rely on mid-history instructions being retained.
- When context is tight, a clean reset from repo files (clock-in) beats continuing on a lossy, half-remembered thread.

**Source:** Kilo — Context Condensing (https://kilo.ai/docs/customize/context/context-condensing); "Lost in the Middle" (Liu et al., 2023).

---

## 9. Guides vs Sensors — the Design Vocabulary for Building Harnesses

**Why:** Naming the two control directions lets you design a harness deliberately instead of bolting on rules reactively.

**Rules**
- **Guides (feedforward)** anticipate behavior and steer *before* the agent acts — `AGENTS.md`, skills, codemods, style configs. They raise the odds of a good first attempt.
- **Sensors (feedback)** observe *after* the agent acts and enable self-correction — tests, linters, type-checkers, build, AI review. They are most powerful when their output is written for LLM consumption (e.g. a lint message that includes the fix).
- You need **both directions**: feedback-only repeats the same mistakes; feedforward-only never learns whether its rules worked.
- Distinguish **computational** controls (deterministic, CPU-fast, reliable — run on every change) from **inferential** ones (semantic judgment, GPU, slower, non-deterministic — reserve for what deterministic tools cannot decide).
- Prefer computational controls; add inferential ones only where semantic judgment adds value beyond what types/tests/linters express.
- **Shift quality left:** place cheap computational sensors pre-commit and pre-integration; reserve expensive inferential sensors (broad code review, mutation testing) for post-integration.
- Run **continuous drift sensors** outside the change lifecycle: dead-code detection, coverage-quality analysis, dependency scanners.
- Treat the harness as a governor regulating three dimensions — **maintainability** (easiest, most tooling), **architecture fitness** (fitness functions, perf/observability budgets), and **behaviour** (hardest; spec as feedforward, test suite + manual review as feedback).

**Source:** Martin Fowler — Harness engineering for coding agent users (https://martinfowler.com/articles/harness-engineering.html).

## 10. Gates Enforce; Prompts Only Request

**Why:** A prompt is a request, not a rule. It lives in finite context, gets summarized away, and shifts run to run — anything the agent merely "chooses to follow" eventually slips.

**Rules**
- Move every standard you actually care about **out of the prompt and into an enforced gate** — versioned, visible to the whole team, applied to humans and agents alike.
- A failed gate stops everything until the code satisfies the rule, leaving the agent one path forward: produce a solution that passes.
- Prompts communicate preferences; gates guarantee properties. Make the important preferences into properties.
- This repo practices the pattern: `scripts/validate-agents.sh` enforces frontmatter contracts and the router line budget — it does not merely ask for them.
- A single gate is rarely enough — a capable agent optimizes against the literal rule, not the goal behind it (forbid mocks and it writes a thin wrapper that *is* a mock). Measure **intent, not form**.

**Source:** Salesforce — Maintaining Code Quality at Agent Speed, Pattern 3 (https://engineering.salesforce.com/maintaining-code-quality-at-agent-speed-7-patterns-for-agentic-engineering/).

## 11. Separate Reasoning from Computation

**Why:** Conflating reasoning with deterministic computation is where agent systems become unreliable. Language models handle ambiguity well; deterministic code handles precision. Ask each to do only its job.

**Rules**
- If logic can be expressed as a deterministic algorithm and validated with tests, it **should not live in the model**: arithmetic, optimization, scheduling, resource allocation, sorting, parsing, validation, routing, precedence resolution.
- For tasks that must produce the same answer every time, use a real solver/function/validator — not LLM reasoning. The valuable property of deterministic code is *consistency*: same input → same output.
- Route work as **reasoning → deterministic computation → reasoning**: an agent produces structured output, a deterministic engine transforms it, another agent applies the result.
- **Explanations are not evidence.** An agent that reasons plausibly but emits a broken output has still failed. Treat an agent as successful only when objective validation confirms it is correct — reviewer-agent confidence is not validation.
- **Failure→cause diagnostic:** recurring arithmetic/precision errors point to missing deterministic computation; context confusion points to poor context isolation; repeated implementation errors point to insufficient validation. Fix the cause, not the symptom.

**Source:** Salesforce — How to Build Reliable AI Agents, Patterns 1–2 & 5 (https://engineering.salesforce.com/how-to-build-reliable-ai-agents-5-engineering-patterns-from-a-production-system/).

## 12. Grade the Tests, Not Just the Code

**Why:** When the same agent writes the code and the tests, the tests inherit whatever it misunderstood. A passing suite says the tests ran — not that the software is right. The first thing that breaks is often the test suite, not the code.

**Rules**
- The code-author must not be the sole author and judge of the tests. This **extends** §5's worker≠checker rule from *code* to *tests*.
- Don't treat a green suite as proof of correctness; treat it as one signal. Tests that hug the happy path, assert the wrong behavior, or drift alongside an implementation bug all pass.
- **Prefer mutation testing to grade the tests:** deliberately mutate the implementation (flip a comparison, drop a line, alter a constant); if the suite stays green, those tests were decoration, not coverage.
- **Layer validation** — no single technique carries the full weight of confidence. The more trust a change needs before it ships, the more *independent* layers (unit → integration → end-to-end → mutation) it must pass.
- Sequence for agent-written code: validate behavior at the system boundary early (API/E2E), so you only review code that actually works; generate deep unit tests last as a regression net once the implementation stabilizes.

**Source:** Salesforce — Maintaining Code Quality at Agent Speed, Patterns 2 & 5.

## 13. Catalog Failure Modes; Engineer the Lifecycle

**Why:** Every agent has predictable, recurring failure modes. Treating each as a prompting bug smooths the edges without removing the behavior; the durable fix is harness work, and bottlenecks relocate as speed rises.

**Rules**
- Study how your specific agent fails; catalog the recurring patterns, and build safeguards that assume those patterns will return.
- A recurring failure is a **harness problem, not a prompt problem.** When something breaks, ask "what change to the surrounding system would make this failure harder to repeat?" — context management, verification, tooling, state — before rewriting the prompt.
- Log recurring failure modes (and the control that fixed them) in `.agents/plans/{slug}/retro.md` so the harness improves over time.
- **Engineer the lifecycle, not just the code.** Faster generation relocates the bottleneck downstream — into review, testing, CI/CD, and release. Optimize generation alone and the traffic jam just moves one step later.
- **Deliberate friction is leverage, not waste.** A gate, a mutation run, a review checkpoint is the system pausing to ask "can this be trusted?" Strip those out for speed and you carry problems further before anyone notices. Make *confidence* scale with *generation*.

**Source:** Salesforce — Maintaining Code Quality at Agent Speed, Patterns 4, 6 & 7; How to Build Reliable AI Agents, Pattern 5.

---

## Appendix A — Orchestrator Convergence Gates

Canonical checklist shared by the orchestrator agents (`conductor`, `squad-lead`). Verify all before declaring a unit converged. Each agent keeps its compact form inline and points here as the source of truth.

1. **Spec ⇄ Code parity** — no orphan code without spec; no orphan spec without code.
2. **Green by evidence** — build + test + lint pass, read from the Tester's output (the orchestrator does not run it).
3. **Reviewer sign-off** — a Reviewer pass found no spec divergence, boundary leak, or dead code.
4. **Boundary respect** — changes stay inside agreed scope.
5. **Norms hold** — naming, error handling, guard clauses, no silent catches (Reviewer confirms).
6. **Safeguards intact** — performance/security invariants hold under the new tests.
7. **Integration proven** — ≥1 end-to-end path exercises the change across module boundaries.
8. **Executable completion evidence** — every "done" claim is backed by a passing executable check (test/endpoint/build), never "the code looks fine".
9. **Three-layer termination** — L1 static (lint/typecheck), L2 runtime (tests run, critical path executes), L3 end-to-end across the changed boundary. No layer skipped.
10. **No refactor-before-verify** — core functionality is verified before any cleanup/optimization touches the changed code.
11. **Assumptions still hold** *(decisive orchestrators)* — every recorded best-practice assumption is still valid or has been updated with rationale.

## Appendix B — On-Disk State Schema (source of truth across compaction)

`.agents/plans/{task-slug}/`
- `story.md` — user request + intent + assumptions.
- `canvas.md` — REASONS plan (non-trivial work only). Decisive orchestrators include an explicit `## Assumptions` section listing every best-practice decision made.
- `state.json` — phase, active/completed squad members, pending ops.
- `retro.md` — lessons learned and recurring failure modes (append-only).
- `decision-log.md` — the "why" behind decisions (alternatives rejected, invariants chosen). Append-only.

`.agents/handoff/`
- `$TASK_ID.md` — full subagent report.
- `$TASK_ID.summary.md` — concise summary (orchestrator reads this).
- `$TASK_ID.scratchpad.md` — working notes.

After compaction, **re-read `state.json` and the plan dir first** to reconstruct context. Disk beats memory.

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
- Martin Fowler: Harness engineering for coding agent users — https://martinfowler.com/articles/harness-engineering.html
- Salesforce: Maintaining Code Quality at Agent Speed (7 patterns) — https://engineering.salesforce.com/maintaining-code-quality-at-agent-speed-7-patterns-for-agentic-engineering/
- Salesforce: How to Build Reliable AI Agents (5 patterns) — https://engineering.salesforce.com/how-to-build-reliable-ai-agents-5-engineering-patterns-from-a-production-system/
- Learn Harness Engineering (12 lectures) — https://walkinglabs.github.io/learn-harness-engineering/en/
- Lost in the Middle (Liu et al., 2023) — https://arxiv.org/abs/2307.03172
- Kilo — Prompt Engineering — https://kilo.ai/docs/customize/prompt-engineering
- Kilo — Context Condensing — https://kilo.ai/docs/customize/context/context-condensing
