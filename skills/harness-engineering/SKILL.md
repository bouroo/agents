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
---

# Harness Engineering — Agent-Loadable Norms

A strong model still fails when the closed-loop system around it is weak. The harness constrains behavior, preserves context, defeats premature victory, verifies with executable evidence, makes runtime observable.

## 1. Repository as System of Record

**Why:** Conversation state is lost every session; decisions and evidence must survive.
**Rules**
- Treat files, not chat, as the system of record. Restart work from repo files, never from memory of prior turns.
- Decisions → `.agents/plans/decision-log.md`; progress/verification → `.agents/plans/progress.md` + `verification-report.md`.
- Every meaningful state change is a diffable, revertable artifact.
- Name artifacts so their purpose is obvious; link related ones explicitly — never assume the next session infers relationships.
**Source:** Lecture 1 (OpenAI: "operational record"; Anthropic: "handoff files").

## 2. Split Instructions; No Giant File

**Why:** Long mid-file instructions are lost; routing and constraints belong at boundaries.
**Rules**
- Keep `AGENTS.md` to 50–200 lines: overview, hard constraints, links to topic docs.
- Put detail in on-demand topic docs (like this one); inline nothing a skill already owns.
- Tag every rule with `SOURCE` / `APPLICABILITY` / `EXPIRY`; audit like technical debt.
- Critical constraints at the top or bottom of a file; never buried mid-file.
- Cross-reference rather than duplicate — one source of truth per rule.
**Source:** Lecture 4 / "Lost in the Middle" (Liu et al., 2023).

## 3. Keep Context Alive Across Sessions

**Why:** Each session starts with wiped short-term memory; reconstruction cost dominates.
**Rules**
- Clock in/out: update progress log, decision log, last verification, next executable step.
- Persist in `.agents/plans/`: state, decision "why", verification results, next action.
- Use git commits as checkpoints after every verified completion.
- Target: new session reaches executable state in ≤ ~3 minutes.
- Short tasks finish in-session; tasks needing > ~60% of the window prepare a handoff.
- Beware "context anxiety" near the window limit — a clean reset often beats lossy compaction.
- Write handoffs in the imperative: "Next session runs X, then Y, then verifies Z."
**Source:** Lecture 5.

## 4. WIP = 1; Draw Task Boundaries

**Why:** Parallel unfinished work lowers completion rate and leaves the repo unclean.
**Rules**
- Activate exactly ONE task at a time; finish and verify before starting the next.
- Completion evidence must be executable ("curl returns 201", "test passes"), not subjective.
- Externalize a machine-readable scope surface with states `not_started` / `in_progress` / `blocked` / `passing`.
- Track `VCR = verified / activated`; block new activations when `VCR < 1.0`.
- Prefer less work fully finished over more work half-done.
- Define "done" as a checklist before starting; reject fuzzy exits.
- If blocked, record the blocker, notify if needed, move only to an unblock action.
**Source:** Lecture 7.

## 5. Prevent Premature Victory

**Why:** Agents are systematically overconfident; the harness, not the agent, judges completion.
**Rules**
- Externalize the termination judgment; never trust a "feels done" signal.
- Run three-layer validation in order: L1 static, L2 runtime (tests, app start, critical paths), L3 end-to-end; skip none.
- Error feedback must be actionable with repair steps (not "test failed" — say which env var, template, or line).
- Do not refactor until core functionality is verified.
- Separate worker from checker; use an independent evaluator.
- Require a failing test or reproduction before fixing a bug.
- Capture exact command, expected output, actual output for every verification claim.
**Source:** Lecture 9.

## 6. Observability Belongs in the Harness

**Why:** Without runtime signals you cannot tell whether a run succeeded, partially succeeded, or left a mess.
**Rules**
- Capture signals the harness can act on: started-and-ready, critical paths executed, side effects correct (DB writes, files), temp resources cleaned up.
- Log structured, actionable fields; never log secrets.
- Logs for debugging, metrics for performance, traces for request flow.
- Emit readiness probes for long-running services.
- Verify side effects by reading back what was written, not by trusting the write call.
**Source:** Lecture 11.

## 7. Every Session Leaves a Clean State

**Why:** A dirty checkout destroys the next session's startup budget and breeds silent drift.
**Rules**
- Before clocking out: confirm standard startup and verification still work.
- Update the progress log; leave no half-finished work unrecorded.
- Ensure the next session can continue without manual fixes.
- Prefer a small, committed, passing checkpoint over a large, unverified, half-done change.
- Revert speculative edits rather than leaving them uncommitted.
- State the next action explicitly enough that another agent could pick it up.
**Source:** Lecture 12.

## 8. Context Budget & Compaction

**Why:** Every token in `AGENTS.md` and the system prompt persists across auto-compaction; buried detail is paid every turn and lost first under pressure.
**Rules**
- Treat `AGENTS.md` as a router (overview, hard constraints, links to skill docs); keep ≤ ~200 lines.
- Push detail into skill docs that load only when relevant; never inline a skill body into `AGENTS.md`.
- Prefer `@file` / `{file:...}` references and lazy on-demand loading over pasting large bodies.
- Prune stale tool outputs and large pasted content between turns — they consume the window forever if left.
- Run compaction at phase boundaries, not mid-step: a clean summary beats lossy compression. Use a cheaper or larger-context model than the working agent where supported.
- Recent turns survive compaction; put the next executable action in the latest assistant turn or a tracked file — never rely on mid-history instructions being retained.
- When context is tight, a clean reset from repo files (clock-in) beats a lossy, half-remembered thread.
**Source:** Kilo — Context Condensing (https://kilo.ai/docs/customize/context/context-condensing); "Lost in the Middle" (Liu et al., 2023).

---

## 9. Guides vs Sensors — the Design Vocabulary for Building Harnesses

**Why:** Naming the two control directions lets you design a harness deliberately instead of bolting on rules reactively.
**Rules**
- **Guides (feedforward)** steer *before* the agent acts — `AGENTS.md`, skills, codemods, style configs; raise odds of a good first attempt.
- **Sensors (feedback)** observe *after* and enable self-correction — tests, linters, type-checkers, build, AI review. Most powerful when output is written for LLM consumption.
- You need **both directions**: feedback-only repeats mistakes; feedforward-only never learns whether its rules worked.
- Distinguish **computational** controls (deterministic, CPU-fast, reliable — run every change) from **inferential** ones (semantic, slower, non-deterministic). Prefer computational; add inferential only where semantic judgment adds value beyond types/tests/linters.
- **Shift quality left:** cheap computational sensors pre-commit and pre-integration; reserve expensive inferential sensors (review, mutation testing) for post-integration.
- Run **continuous drift sensors** outside the lifecycle: dead-code detection, coverage-quality analysis, dependency scanners.
- Govern three dimensions — **maintainability** (most tooling), **architecture fitness** (fitness functions, perf/observability budgets), **behaviour** (hardest; spec as feedforward, tests + manual review as feedback).
- **Decision-time guidance over prompt-stuffing:** inject short situational guidance at the decision point (lightweight classifier or context check) instead of every rule into the system prompt — keeps the root instruction a router, surfaces the right constraint only when it applies. (Replit — Decision-Time Guidance.)
**Source:** Martin Fowler — Harness engineering for coding agent users (https://martinfowler.com/articles/harness-engineering.html).

## 10. Gates Enforce; Prompts Only Request

**Why:** A prompt is a request, not a rule — it lives in finite context, gets summarized away, and shifts run to run; anything the agent merely "chooses to follow" eventually slips.
**Rules**
- Move every standard you actually care about **out of the prompt and into an enforced gate** — versioned, visible to the whole team, applied to humans and agents alike.
- A failed gate stops everything until the code satisfies the rule, leaving exactly one path forward: produce a solution that passes.
- Prompts communicate preferences; gates guarantee properties. Make important preferences into properties.
- This repo practices the pattern: `scripts/validate-agents.sh` enforces frontmatter contracts and the router line budget — it does not merely ask for them.
- One gate is rarely enough — a capable agent optimizes against the literal rule, not the goal (forbid mocks and the agent ships a thin wrapper that *is* a mock). Measure **intent, not form**.
**Source:** Salesforce — Maintaining Code Quality at Agent Speed, Pattern 3 (https://engineering.salesforce.com/maintaining-code-quality-at-agent-speed-7-patterns-for-agentic-engineering/).

## 11. Separate Reasoning from Computation

**Why:** Models handle ambiguity; deterministic code handles precision. Confusing which is which is where agent systems become unreliable.
**Rules**
- If logic can be expressed deterministically and validated with tests, it **should not live in the model** — arithmetic, scheduling, sorting, parsing, validation, routing, optimization, resource allocation, precedence.
- For tasks that must produce the same answer every time, use a real solver/function/validator — not LLM reasoning. (Determinism's valuable property is *consistency*: same input → same output.)
- Route work as **reasoning → deterministic computation → reasoning**: agent produces structured output, a deterministic engine transforms it, another agent applies the result.
- **Explanations are not evidence.** Plausible reasoning with broken output is still a failure; reviewer-agent confidence is not validation. Treat an agent as successful only when objective validation confirms it.
- **Failure→cause diagnostic:** arithmetic/precision errors → missing deterministic computation; context confusion → poor context isolation; repeated implementation errors → insufficient validation. Fix the cause, not the symptom.
**Source:** Salesforce — How to Build Reliable AI Agents, Patterns 1–2 & 5 (https://engineering.salesforce.com/how-to-build-reliable-ai-agents-5-engineering-patterns-from-a-production-system/).

## 12. Grade the Tests, Not Just the Code

**Why:** When the same agent writes the code and the tests, the tests inherit whatever it misunderstood. A green suite says the tests ran, not that the software is right.
**Rules**
- The code-author must not be the sole author and judge of tests — extends §5's worker≠checker rule from *code* to *tests*.
- Treat a green suite as one signal, not proof. Tests that hug the happy path, assert wrong behavior, or drift alongside an implementation bug all pass.
- **Prefer mutation testing to grade the tests:** deliberately mutate the implementation (flip a comparison, drop a line, alter a constant); if the suite stays green, those tests were decoration, not coverage.
- **Layer validation** — the more trust a change needs before it ships, the more *independent* layers (unit → integration → end-to-end → mutation) it must pass.
- Sequence for agent-written code: validate at the system boundary early (API/E2E), so you only review code that actually works; deep unit tests last as a regression net once the implementation stabilizes.
- **Agents are poor self-judges:** they identify issues then talk themselves into approving. Tune any evaluator rubric on completed work vs. human judgment, sharpen pass/fail where they diverge; plan 3–5 tuning rounds — a rubric is a sensor needing calibration. (Learn Harness Engineering — evaluator-rubric.)
**Source:** Salesforce — Maintaining Code Quality at Agent Speed, Patterns 2 & 5.

## 13. Catalog Failure Modes; Engineer the Lifecycle

**Why:** Every agent has predictable, recurring failure modes. Treating each as a prompting bug smooths edges without removing the behavior; the durable fix is harness work, and bottlenecks relocate as speed rises.
**Rules**
- Study how your specific agent fails; catalog recurring patterns; build safeguards assuming those patterns return.
- A recurring failure is a **harness problem, not a prompt problem.** Ask "what change to the surrounding system — context, verification, tooling, state — would make this failure harder to repeat?" before rewriting the prompt.
- Log recurring failure modes (and the control that fixed them) in `.agents/plans/{slug}/retro.md` so the harness improves.
- **Engineer the lifecycle, not just the code.** Faster generation relocates the bottleneck downstream (review, testing, CI/CD, release).
- **Deliberate friction is leverage, not waste.** A gate, mutation run, or review checkpoint is the system asking "can this be trusted?" — stripping them moves problems further before anyone notices. Make *confidence* scale with *generation*.
**Source:** Salesforce — Maintaining Code Quality at Agent Speed, Patterns 4, 6 & 7; How to Build Reliable AI Agents, Pattern 5.

## 14. Failure-Mode → Control Map

**Why:** When a long-running agent stalls, the fastest recovery is to name the failure mode and reach for the single artifact that fixes it — not to add prose to a global instruction file.
| Failure mode | What it looks like | Primary fix | Supporting artifact |
| --- | --- | --- | --- |
| Cold-start confusion | New session spends most of its time rediscovering setup and status | Make the repository the system of record | progress log (`.agents/plans/` + progress.md) |
| Scope sprawl | Agent starts several features and finishes none cleanly | Restrict active scope (WIP=1) | feature list / scope surface |
| Premature completion | Agent claims done after edits but before runnable proof | Bind completion to executable evidence | clean-state checklist + three-layer termination (§5) |
| Fragile startup | Every session re-learns how to boot the project | Standardize setup and verification | init.sh / standard startup path |
| Weak handoff | Next session cannot tell what is verified, broken, or next | End with an explicit handoff | session-handoff / `.agents/handoff/` |
| Subjective review | Review quality depends on taste or memory | Score output with fixed categories | evaluator rubric (6 dimensions) |

Add the smallest artifact that directly addresses the observed failure mode — never dump more text into one global instruction file.

**Source:** Learn Harness Engineering — method-map.

## 15. Harness Simplification & the Quality Document

**Why:** Every harness component encodes an assumption about what the model *cannot* do. As models improve, those assumptions go stale and the component becomes overhead — dead weight paid every turn.
**Rules**
- **Stale-assumption test:** snapshot quality → remove one harness component → run the benchmark suite → snapshot again → if grades did not drop, the component was overhead (restore only if grades drop).
- **Quality document:** snapshot grading each product domain and architectural layer (A–D) across verification status, agent legibility, test stability, and key gaps — codebase health over time, not session output. Distinct from the rubric ("did the agent do good work this session?"); the quality document scores "is the project getting stronger or weaker?".
- Tie back to §13: simplification is the inverse of accretion — both are harness work, not prompt work.
**Source:** Anthropic — Harness design for long-running application development; Learn Harness Engineering — quality-document.

## 16. Tools & MCP — Understanding Agent Capabilities

**Why:** An agent's effectiveness depends on selecting the right tool for each sub-task. MCP (Model Context Protocol) servers extend the agent's toolkit with domain-specific capabilities; misusing or ignoring available tools is a systematic failure mode.
**Rules**
- **Tool selection is a decision, not a guess.** Match the tool to the task's semantics and cost: known path → `read`; known pattern → `grep`/`glob`; intent/concept → `semantic_search`; unfamiliar surface → `explore`; external/version-sensitive fact → `websearch`/`webfetch`; domain workflow → matching MCP server or skill. Prefer specialized over generic; lowest-cost tool that fits.
- **MCP servers are domain extensions.** Treat each MCP server as a specialized capability boundary — understand what it exposes (tools, resources, prompts) and when to invoke it vs. falling back to general tools. Prefer MCP tools when they provide structured, validated access to a domain (e.g., database queries, API interactions, file-type-specific operations).
- **Discover before assuming.** When an MCP server is available, inspect its exposed tools and their schemas before calling. Don't guess parameter shapes or capabilities — read the tool description.
- **Compose tools, don't nest them.** Chain tool outputs through agent reasoning (tool A → interpret → tool B), not by embedding one tool call inside another. Each tool call should be independently auditable.
- **Fail gracefully on tool errors.** Tool and MCP calls can fail (timeout, auth, invalid input). Handle errors explicitly: retry transient failures, fall back to alternative tools, surface persistent failures rather than silently dropping them.
- **Prefer computational tools over inferential reasoning** for deterministic tasks — a database MCP query beats asking the model to recall data; a linter MCP beats asking the model to check style.
**Source:** Kilo — Prompt Engineering; Martin Fowler — Harness Engineering §9 (Guides vs Sensors); AGENTS.md "Decision-Making Framework".

---

## Appendix A — Orchestrator Convergence Gates

Canonical checklist shared by the orchestrator agent (`orchestrator`). Verify all before declaring a unit converged; the agent keeps a compact form inline and points here as the source of truth.

1. **Spec ⇄ Code parity** — no orphan code without spec; no orphan spec without code.
2. **Green by evidence** — build + test + lint pass, read from the Tester's output (orchestrator does not run it).
3. **Reviewer sign-off** — no spec divergence, boundary leak, or dead code.
4. **Boundary respect** — changes stay inside agreed scope.
5. **Norms hold** — naming, error handling, guard clauses, no silent catches (Reviewer confirms).
6. **Safeguards intact** — performance/security invariants hold under the new tests.
7. **Integration proven** — ≥1 end-to-end path exercises the change across module boundaries.
8. **Executable completion evidence** — every "done" claim backed by a passing executable check (test/endpoint/build), never "the code looks fine".
9. **Three-layer termination** — L1 static (lint/typecheck), L2 runtime (tests run, critical path executes), L3 end-to-end across the changed boundary. No layer skipped.
10. **No refactor-before-verify** — core functionality verified before any cleanup/optimization touches the changed code.
11. **Assumptions still hold** *(decisive orchestrators)* — every recorded best-practice assumption is still valid or has been updated with rationale.

## Appendix B — On-Disk State Schema (source of truth across compaction)

> Paths are project-workspace-relative (`.agents/` lives in the target project's root via `git rev-parse --show-toplevel`, never in `~/.agents/`).

`.agents/plans/{task-slug}/`
- `story.md` — user request + intent + assumptions.
- `canvas.md` — REASONS plan (non-trivial work only); decisive orchestrators add an explicit `## Assumptions` section listing every best-practice decision.
- `state.json` — phase, active/completed squad members, pending ops.
- `retro.md` — lessons learned and recurring failure modes (append-only).
- `decision-log.md` — the "why" behind decisions (alternatives rejected, invariants chosen; append-only).

`.agents/handoff/`
- `$TASK_ID.md` — full subagent report.
- `$TASK_ID.summary.md` — concise summary (orchestrator reads this).
- `$TASK_ID.scratchpad.md` — working notes.

After compaction, **re-read `state.json` and the plan dir first**. Disk beats memory.

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
- OpenAI: Unrolling the Codex agent loop — https://openai.com/index/unrolling-the-codex-agent-loop/
- Anthropic: Demystifying evals for AI agents — https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- LangChain: Improving Deep Agents with harness engineering — https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering
- Cursor: Continually improving our agent harness — https://cursor.com/blog/continually-improving-agent-harness
- Replit: Decision-Time Guidance: Keeping Replit Agent Reliable — https://blog.replit.com/decision-time-guidance