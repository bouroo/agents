---
name: harness-engineering
description: >
  Harness-engineering norms that stop capable agents from failing: repo-as-record, split
  instructions, WIP=1, executable completion evidence, three-layer termination, cross-session
  state persistence, observability, and clean-session exits -- plus the design vocabulary for
  building harnesses (feedforward guides vs feedback sensors; computational vs inferential
  controls), gates-over-prompts, separating reasoning from computation, grading tests via
  mutation testing, and engineering the whole lifecycle. Use when designing agent workflows,
  checkpoints, verification rules, or orchestrator agents. Grounded in the OpenAI/Anthropic
  harness canon, Martin Fowler's harness-engineering model, the Salesforce agentic-reliability
  patterns, and the 12-lecture "Learn Harness Engineering" series.
---

# Harness Engineering -- Agent-Loadable Norms

A strong model still fails when the closed-loop system around it is weak. The harness constrains behavior, preserves context, defeats premature victory, verifies with executable evidence, and makes runtime observable. These norms are referenceable: each section is a clause the harness can require, instrument, or assert against.

> **Override.** A project-level harness spec that explicitly supersedes this skill takes precedence.

**Stance:** You treat "done" as the most common lie an agent tells. Verification is observed evidence, not narrated confidence; a gate that can fail is worth ten reminders that cannot.

**Modes:**

- **Build mode** -- designing or extending an agent harness. Walk §1-§18 in order; emit gates, handoff artifacts, and failure-mode controls. Sequential.
- **Review mode** -- grading a transcript or live run for harness quality. Audit against the §14 Failure-Mode -> Control Map and the §18 judge fraud rubric. Sequential.
- **Audit mode** -- sweeping an existing codebase or transcript for harness gaps. Launch up to 5 parallel sub-agents, one per concern: (1) context/memory engineering, (2) gates and three-layer termination, (3) handoff and resume artifacts, (4) verification theater / mutation-grade tests, (5) observability and tool-error handling.

## 1. Repository as System of Record

**Why:** Conversation state is lost every session; decisions and evidence must survive.

- Treat the repository as the only durable memory. Restart work from files; never from recollection of prior turns.
- Every assumption that influences a decision lives on disk: commit message, spec, ADR, decision log entry. Invisible decisions are un-auditable.
- Compaction resilience: critical state is flushed to the repo (plan, decisions, evidence, next action) at the end of every turn so post-compaction resume is a `read`, not a guess.
- Prefer **decision logs** (`progress.md`, `decisions.md`) and **handoff notes** over embedded prose in instructions.

## 2. Split Instructions

**Why:** A single monolithic instruction file degrades into a wall of unread text; agents attend to early sections and ignore late ones (Lost-in-the-Middle).

- Keep `AGENTS.md` a **router**: overview, hard constraints, and links. Detail lives in `skills/<name>/SKILL.md` and on-demand topic docs.
- Load skill content on demand, matched to the current task. Never pre-load unrelated skills.
- Every token kept in the always-on file is paid every turn; every token in a skill is paid only when that skill is invoked. The router file should be the smallest set of high-signal rules.
- Splitting also enables variant instructions per agent role, per project, per environment -- without rewriting a global prompt.

## 3. Minimal Live Context

**Why:** Model attention is a finite budget; oversized context dilutes signal.

- Keep the live window small: smallest high-signal tokens, lazy references over inlined bodies.
- Prune stale tool outputs and superseded reasoning. Re-read on demand rather than carrying forward verbatim.
- Two layers, kept distinct: **context engineering** (the live window) and **memory engineering** (what outlives the window -- decision log, progress file, spec, handoff note, ADR).
- Reference, don't copy: link to a file or skill instead of inlining its body into the working set.

## 4. WIP = 1

**Why:** Parallel workstreams, unfinished work, and "I'll finish later" accumulate state that breaks resume and review.

- Finish and verify the current task before starting the next. One open unit of work at a time.
- A "unit" has a clear definition of done (acceptance criteria), an owner, and a verification path. If two units need to advance together, split them at the gate, not in flight.
- Parked work goes to disk with a clear resumption note, not into the live context.

## 5. Three-Layer Termination

**Why:** "Done" is the most common lie an agent tells. The harness judges completion -- never trust a "feels done" signal.

Execution evidence (command + exit code + actual output) is required at every layer; skip none.

- **L1 static** -- lint, type-check, format. Cheap, fast, catches a class of mistakes that downstream layers cannot see.
- **L2 runtime** -- tests run; the application starts; critical paths execute. Confirms code is alive.
- **L3 end-to-end** -- at least one path exercises the change across real boundaries (network, FS, DB, browser, external API). Confirms the code does what it claims.

No repro -> no fix. Reproductions are evidence, not narratives.

## 6. Structured Handoffs

**Why:** Sessions end; compaction summarizes. The harness must hand off state that a fresh session can resume from without re-derivation.

- Standard handoff artifacts:
  - **Decision log** (`decisions.md`) -- dated, append-only, with rationale and the assumption that was recorded.
  - **Progress file** (`progress.md`) -- ordered steps, current step, what is done, what is open.
  - **Handoff note** (`handoff.md` or latest assistant turn) -- the next executable action, current blocker, decisions made this turn.
  - **ADR** -- for durable, cross-system architectural decisions.
- The latest assistant turn must contain: next action, current blocker, decisions made this turn. Treat the conversation summary as a hint, not a record.
- Skills are themselves a handoff surface: load before acting, not after.

## 7. Clean-Session Exit

**Why:** The next session's startup budget depends on a clean state; leftover speculative edits consume attention and introduce false positives.

- Before exiting, confirm: standard startup commands pass; verification (L1/L2/L3) passes; progress log updated; speculative edits reverted; next action stated in the latest turn.
- "Standard startup + verification still passes" is the floor. Anything less is a dirty checkout.
- A clean exit is itself a checked artifact, not a politeness.

## 8. Observability

**Why:** If the harness can't see what the agent decided, checked, or skipped, it cannot learn from failure.

- Trace decisions, checkpoints, and outcomes to the repo. A transcript that cannot be reconstructed from the repo is incomplete.
- Surface state at every gate (intent, twins, auth, pending) so downstream reviewers and judges can audit without re-deriving.
- Surface errors with context: which command, which input, which environment, which expected output. An opaque failure is a hidden failure.
- Prefer **structured logs and JSONL traces** to free-form prose -- they survive compaction and parse in tests.

## 9. Feedforward vs Feedback

**Why:** Agent failure modes cluster into two classes -- missing guidance (feedforward) and missing detection (feedback) -- and the fixes are different.

- **Feedforward guides** -- proactive instructions before an action: constraints, examples, templates, prior decisions. Reduce the chance of a wrong move.
- **Feedback sensors** -- reactive checks after an action: assertions, tests, gates, judges. Detect a wrong move that already happened.
- **Computational controls** -- the harness *computes* the right value (typed parser, schema validator, deterministic solver) and the agent consumes the output.
- **Inferential controls** -- the harness *prompts* the agent to reason correctly. Cheap to add, weak alone. Always pair inferential controls with a computational or feedback check.
- Diagnose first: classify the failure as **missing guide** (add feedforward) or **missing sensor** (add feedback), then reach for the fix that matches.

## 10. Gates Over Prompts

**Why:** A prompt that asks the agent to "remember to verify" loses to a gate that fails the build when verification is absent.

- Encode standards as **gates**, not reminders. A failed gate stops everything until the code satisfies the rule, leaving exactly one path forward: produce a solution that passes.
- Order gates so the cheapest, highest-signal checks run first (L1 -> L2 -> L3).
- A gate has: a clear pass condition, a clear failure message that names the next action, and an owner (the harness, not the agent's memory).
- "Said I would" is not a gate; "ran and passed" is.

## 11. Separate Reasoning from Computation

**Why:** Models handle ambiguity; deterministic code handles precision. Putting arithmetic, parsing, routing, validation, or scheduling in model reasoning trades accuracy for explainability.

- **Deterministic logic** -- arithmetic, parsing, validation, scheduling, routing, schema checks -- lives in tested code, not LLM reasoning. Use a parser, not a sentence; use a solver, not an intuition.
- **Reasoning** is for the parts that are genuinely ambiguous: tradeoff selection, intent interpretation, design choices with multiple valid answers.
- **Explanations are not evidence.** Plausible reasoning with broken output is still a failure; reviewer-agent confidence is not validation. Treat an agent as successful only when objective validation confirms it -- specifically, captured command + exit code + actual output, not a narrative summary.
- **Verification theater** is the most common gap between the two: the agent reports a passing test as proof, the transcript shows the test ran, but the test was a tautology or a one-line assertion that the implementation trivially satisfies. A test that cannot fail cannot prove anything. See [Verification theater in depth](./references/verification-theater.md) and the Failure-Mode -> Control Map row in §14.
- **Failure->cause diagnostic:** arithmetic/precision errors -> missing deterministic computation; context confusion -> poor context isolation; repeated implementation errors -> insufficient validation. Fix the cause, not the symptom.

## 12. Grade the Tests

**Why:** A green suite is one signal, not proof. Tests that hug the happy path, assert wrong behavior, or drift alongside an implementation bug all pass.

- Treat a green suite as one signal, not proof.
- Apply **mutation testing** -- perturb the implementation in known-bad ways and confirm tests fail. A test suite that is green under mutation is not testing anything.
- Cover: negative cases, boundary cases, error paths, contracts (return shape, error types), and adversarial inputs.
- The risk is not just a weak test -- it is **verification theater**: the agent reports a passing test as proof, the transcript shows the test ran, but the test was a tautology or a one-line assertion that the implementation trivially satisfies. A test that cannot fail cannot prove anything.

## 13. Catalog Failure Modes; Engineer the Lifecycle

**Why:** Every agent has predictable, recurring failure modes. Treating each as a prompting bug smooths edges without removing the behavior; the durable fix is harness work, and bottlenecks relocate as speed rises.

- Study how your specific agent fails; catalog recurring patterns; build safeguards assuming those patterns return.
- A recurring failure is a **harness problem, not a prompt problem.** Ask "what change to the surrounding system -- context, verification, tooling, state -- would make this failure harder to repeat?" before rewriting the prompt.
- Log recurring failure modes (and the control that fixed them) in `.agents/plans/{slug}/retro.md` so the harness improves.
- Engineer the **whole lifecycle**, not just the generation step: planning, dispatch, verification, recovery, handoff, judge, retro. A fast generator inside a slow lifecycle produces a slow system.
- See the Failure-Mode -> Control Map in §14 for the canonical names: unprompted fixing, silent step-dropping, retry thrash, verification theater, premature victory, context loss, cold-start confusion, scope sprawl, fragile startup, weak handoff, subjective review. The map is the catalog.

## 14. Failure-Mode -> Control Map

**Why:** When a long-running agent stalls, the fastest recovery is to name the failure mode and reach for the single artifact that fixes it -- not to add prose to a global instruction file.

| Failure mode | What it looks like | Primary fix | Supporting artifact |
| --- | --- | --- | --- |
| Unprompted fixing | Agent edits files outside the active task without being asked | Scope pin in the active plan; latest-turn state | `progress.md`, scope guardrail |
| Silent step-dropping | Plan steps disappear between turns; agent claims "done" without the step | Plan as record; gate per step | `progress.md` step ledger |
| Retry thrash | Same edit attempted 3+ times with small variations; output oscillates near failure | Hard verify bound (§15) | §15 hand-back contract |
| Verification theater | Tests run, agent reports green, change is unproven | Gate on mutation-grade tests | `./references/verification-theater.md` |
| Premature victory | "All done" with no execution evidence at L1/L2/L3 | Three-layer termination gate | §5 + spec-side `INTENT:` line |
| Context loss | Decisions, constraints, or prior failures forgotten after compaction or long tasks | Make the repo the system of record; checkpoint next action in latest turn | progress log + decision log + handoff |
| Cold-start confusion | Next session restarts from zero; re-derives context | Decision log + handoff note in repo, not in chat | structured handoff (§6) |
| Scope sprawl | Agent adds adjacent cleanup, refactors, or speculative features | Pin scope in plan; reject out-of-scope deltas at review | plan + scope guardrail |
| Fragile startup | First `install` / `build` / `test` command in a fresh checkout fails | Standard startup + verification gate, run before and after | startup script + L1 gate |
| Weak handoff | Next agent re-asks the same questions, misses constraints | Structured handoff artifacts in repo | §6 handoff note schema |
| Subjective review | Reviewer says "looks fine" without grounded criteria | Adversarial judge with a fraud rubric | §18 judge protocol |

Add the smallest artifact that directly addresses the observed failure mode -- never dump more text into one global instruction file.

## 15. Hard Verify Bound

**Why:** A repeated failure is a harness problem, not a prompt problem (see §13). When the same issue keeps failing verification, the next attempt is statistically unlikely to succeed without a structural change. Silent retry thrash is itself a failure mode (see §14): the agent burns budget, drifts from the intent, and the transcript loses meaning. The bound exists to force a structured hand-back instead.

- **Cycle counter:** a "verify cycle" is one execute-verify pair. Implementation -> L1/L2/L3 -> outcome. Each failure is one cycle.
- **On the 3rd failed cycle on the same issue, STOP.** Do not start a 4th attempt.
- **Classify the failure before the next move:**
  - The repeated error is a mechanical mistake (typo, off-by-one, copy-paste drift) -> back to **implementation**: a fresh attempt with a tighter check is appropriate.
  - The repeated error is surprising or contradicts your understanding -> back to **analysis/spec**: the model of the problem is wrong; the issue needs a sharper spec or a new reproduction, not another guess.
- **Hand-back payload** -- on the 3rd failed cycle, produce a structured hand-back instead of a 4th attempt. The payload contains:
  1. What was tried -- the sequence of attempts and their deltas.
  2. Actual output -- captured command + exit code + stderr/stdout from each attempt, verbatim.
  3. Current hypothesis -- the best current explanation for why it still fails, with the evidence that supports it.
  4. Recommended next move -- sharpen the spec, add a reproduction, swap a tool, or escalate to a human.
- **Counts as a fail-stop, not a soft retry.** The agent's next action is the hand-back, not another implementation attempt.

**Source:** Learn Harness Engineering -- failure-mode -> control.

## 16. Tool & MCP Usage

**Why:** An agent's effectiveness depends on selecting the right tool for each sub-task. MCP (Model Context Protocol) servers extend the agent's toolkit with domain-specific capabilities; misusing or ignoring available tools is a systematic failure mode.

- **Specialized over generic.** Use the lowest-cost tool that fits the lookup: known path -> `read`; known symbol/pattern -> `grep`/`glob`; intent/concept -> `semantic_search`; unfamiliar surface -> `explore`; external/version-sensitive fact -> `websearch`/`webfetch`.
- **Fail gracefully on tool errors.** Tool and MCP calls can fail (timeout, auth, invalid input). Handle errors explicitly: retry transient failures, fall back to alternative tools, surface persistent failures rather than silently dropping them. **Never swallow an error.**
- **Match tool to the boundary.** Trigger code paths through MCP / tools, not through the model. Routes, parsers, schema checks belong in tested code.
- **Surface tool failures with repair steps.** "Test failed" is not actionable; "missing env var `FOO_API_KEY`; set in `.env.local` per README §Setup" is. Error feedback must name the next action.

## 17. Error Budget

**Why:** Reliability is a budget problem, not a perfection problem. A system without an error budget over-spends on safety mechanisms; a system without a budget loses the ability to weigh tradeoffs.

- Allocate an error budget for the unit (feature, release, sprint): how many failures of which severity are tolerable.
- Track failure rates per failure mode; when a mode exceeds its share, the response is a harness change, not a prompt change.
- Pair the budget with the Failure-Mode -> Control Map (§14): each row has a target rate and a control to apply when the rate is exceeded.

## 18. Adversarial Judge

**Why:** The most documented failure of coding agents is claiming success regardless of reality: "fixed, all tests pass" on broken work, tests quietly weakened until they pass, scope silently expanded. A read-only reviewer reading the diff and scoring on a rubric catches some of this; an adversarial judge that treats the report as a set of untrusted claims catches more. The judge's stance is fixed: **a report is a set of claims, not evidence.** Nothing is believed that was not observed. Triggered via the [`judge-phase`](../../commands/judge-phase.md) command.

**Fraud rubric** -- the judge pattern-matches the report against known frauds:

| Fraud | Signal |
| --- | --- |
| Weakened checks | Diff shows test thresholds loosened, asserts removed, mocks broadened to hide failures |
| False completion | A pass claimed with no run shown; a partial pass reported as full; "should work now"; success language on a failure transcript |
| Scope creep | Files modified outside the active task; adjacent cleanup bundled in |
| Unauthorized action | Deletions, force operations, secret reads, network calls beyond the task |
| Missing artifact lines | Required `INTENT:` / `TWINS:` / `AUTH:` / `PENDING:` markers absent on a behavior change |
| Spec betrayal | Implementation diverges from the spec without a spec update; spec updated to match a buggy impl |
| Debris | Debug prints left in; commented-out code; speculative TODOs; unrelated reformatting |

- **Deliver a verdict, evidence first.** VERIFIED (every load-bearing claim reproduced, no frauds); VERIFIED WITH CAVEATS (sound, but list exactly what could not be re-run and any minor debris); REFUTED (a claim failed reproduction or a fraud was found -- name the exact claim, show the contradicting output, state the smallest fix). Never soften a refutation to be polite; never inflate a caveat into a refutation to look rigorous.
- **The judge reads the report like an untrusted witness.** A claim without a captured command + exit code + actual output is not evidence; it is testimony.

## 19. Skill Composition

**Why:** Skills are the unit of harness composition. A skill is a self-contained, on-demand load of norms, vocabulary, and procedures for a class of task.

- One skill per coherent concern. The harness loads skills matched to the task; never loads an unrelated skill "just in case".
- Skills declare a **description** that names what they are for and a **trigger** ("Use when..."). The description is the routing key.
- Skills compose: a task may load `repo-documentation` for the spec, `effective-code-craft` for the code shape, and `harness-engineering` for the verification rules. Each skill stays small; composition does the rest.
- A skill that is referenced but never loaded is dead text; a skill that is loaded but uncited is over-instruction.

---

## Appendix A: Convergence Checklist

Before declaring a unit done, every gate must pass. The checklist is the contract between the implementer and the judge.

1. **Spec is current** -- the spec describes the change that was made, including any drift the change introduced (behavior changed -> spec first, code second).
2. **Scope is pinned** -- only files inside the active plan are modified; out-of-scope deltas are reverted or escalated.
3. **L1 static passes** -- lint, type-check, format all green; run the project's own scripts, not improvised commands.
4. **L2 runtime passes** -- tests run; the application starts; critical paths execute; captured command + exit code in the report.
5. **L3 end-to-end passes** -- at least one path exercises the change across real boundaries; captured command + exit code in the report.
6. **Norms hold** -- naming, error handling, guard clauses, no silent catches (Reviewer confirms).
7. **Artifact gates present** -- `INTENT:` / `TWINS:` / `AUTH:` / `PENDING:` lines written on a behavior change (see [Intent gate in depth](../effective-code-craft/references/intent-gate.md)).
8. **Decision log updated** -- durable decisions recorded with rationale and assumption (commit message or `decisions.md`).
9. **Progress log updated** -- `progress.md` step ledger reflects actual state; next action is the last entry.
10. **Repo is clean of debris** -- no debug prints, commented-out code, unrelated reformatting, untracked scratch files.
11. **Verify bound honored** -- if a single issue has hit 3 failed verify cycles, the unit halts and produces a hand-back per §15 rather than continuing.
12. **Adversarial judge = VERIFIED (or VERIFIED WITH CAVEATS with the caveats listed)** -- run the fraud rubric in §18; capture the verdict in the report.

---

## Operating Standards (always-on)

These are the rules an agent follows at all times, not only inside a specific section.

- **Always-on artifacts** -- every active plan directory holds:
  - `task.md` -- the brief and acceptance criteria.
  - `progress.md` -- ordered steps, current step, what's done, what's open.
  - `decisions.md` -- dated, append-only log of decisions, with rationale and assumption.
  - `retro.md` -- lessons learned and recurring failure modes (append-only).
- **Clean exit** -- before stopping or handing off, `progress.md` is current; the latest turn states the next action; the spec is in sync with the code; L1/L2/L3 pass; no debris; no speculative edits.
- **Single answer per turn** -- one well-tested answer beats several drafts.
- **No secrets in logs** -- never log credentials, tokens, keys, session cookies, or PII.
- **No declaration without evidence** -- "done" requires captured command + exit code + actual output.

## References

Load on demand; do not pull these into context up front. The body above carries everyday use; load a source only when the matching section needs defence or extension.

- [Verification theater in depth](./references/verification-theater.md) -- load when §12 (Grade the Tests) or §18 (Adversarial Judge) needs the fraud rubric and mutation-testing protocol in full.
- [Effective code craft](../effective-code-craft/SKILL.md) and [Intent gate in depth](../effective-code-craft/references/intent-gate.md) -- load when §11 (Separate Reasoning from Computation) meets a behavior change that needs classification.
- OpenAI: Harness Engineering -- https://openai.com/index/harness-engineering/ (the "repo as operational record" claim in §1; load when defending repo-as-record against narrated-status).
- Anthropic: Effective harnesses for long-running agents -- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents (small next steps, handoff files; load when sizing a unit in §4 WIP = 1).
- Anthropic: Harness design for long-running application development -- https://www.anthropic.com/engineering/harness-design-long-running-apps (worker/checker separation, premature-victory prevention; load when shaping §18 Adversarial Judge).
- Martin Fowler: Harness engineering for coding agent users -- https://martinfowler.com/articles/harness-engineering.html (feedforward vs feedback vocabulary in §9; load when designing a new gate).
- Salesforce: Maintaining Code Quality at Agent Speed (7 patterns) -- https://engineering.salesforce.com/maintaining-code-quality-at-agent-speed-7-patterns-for-agentic-engineering/ (gates-over-prompts, grade-the-tests; load for §10 and §12).
- Salesforce: How to Build Reliable AI Agents (5 patterns) -- https://engineering.salesforce.com/how-to-build-reliable-ai-agents-5-engineering-patterns-from-a-production-system/ (explanations != evidence; load for §6 Structured Handoffs and §17 Error Budget).
- Learn Harness Engineering (12 lectures) -- https://walkinglabs.github.io/learn-harness-engineering/en/ (synthesized canon; load when stitching sections into a new harness design).
- Lost in the Middle (Liu et al., 2023) -- https://arxiv.org/abs/2307.03172 (why instructions must be split, not bloated; load for §2 Split Instructions and §3 Minimal Live Context).
- Kilo -- Prompt Engineering -- https://kilo.ai/docs/customize/prompt-engineering (think-then-do loop; load when aligning the harness with the host tool's default loop).
- Kilo -- Context Condensing -- https://kilo.ai/docs/customize/context/context-condensing (compaction discipline; load for §3 Minimal Live Context and the §7 Clean-Session Exit handoff).
- OpenAI: Unrolling the Codex agent loop -- https://openai.com/index/unrolling-the-codex-agent-loop/ (intervention points; load for §16 Tool & MCP Usage).
- Anthropic: Demystifying evals for AI agents -- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents (evaluator rubrics; load when calibrating §18 judge rubric).
- LangChain: Improving Deep Agents with harness engineering -- https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering (guides/sensors applied to deep agents; load for §9 Feedforward vs Feedback).
- Cursor: Continually improving our agent harness -- https://cursor.com/blog/continually-improving-agent-harness (iterate the harness as models improve; load for §19 Skill Composition).
- Replit: Decision-Time Guidance: Keeping Replit Agent Reliable -- https://blog.replit.com/decision-time-guidance (situational guidance at the decision point; load for §10 Gates Over Prompts and §13 Catalog Failure Modes).
