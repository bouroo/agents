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

A strong model still fails when the closed-loop system around it is weak. The harness constrains behavior, preserves context, defeats premature victory, verifies with executable evidence, makes runtime observable.

## 1. Repository as System of Record

**Why:** Conversation state is lost every session; decisions and evidence must survive.
**Rules**
- Treat files, not chat, as the system of record. Restart work from repo files, never from memory of prior turns.
- Decisions to `.agents/plans/decision-log.md`; progress/verification to `.agents/plans/progress.md` + `verification-report.md`.
- Every meaningful state change is a diffable, revertable artifact.
- Name artifacts so their purpose is obvious; link related ones explicitly -- never assume the next session infers relationships.
**Source:** Lecture 1 (OpenAI: "operational record"; Anthropic: "handoff files").

## 2. Split Instructions; No Giant File

**Why:** Long mid-file instructions are lost; routing and constraints belong at boundaries.
**Rules**
- Keep `AGENTS.md` to 50-200 lines: overview, hard constraints, links to topic docs.
- Put detail in on-demand topic docs (like this one); inline nothing a skill already owns.
- Tag every rule with `SOURCE` / `APPLICABILITY` / `EXPIRY`; audit like technical debt.
- Critical constraints at the top or bottom of a file; never buried mid-file.
- Cross-reference rather than duplicate -- one source of truth per rule.
**Source:** Lecture 4 / "Lost in the Middle" (Liu et al., 2023).

## 3. Keep Context Alive Across Sessions

**Why:** Each session starts with wiped short-term memory; reconstruction cost dominates.
**Rules**
- Clock in/out: update progress log, decision log, last verification, next executable step.
- Persist in `.agents/plans/`: state, decision "why", verification results, next action.
- Use git commits as checkpoints after every verified completion.
- Target: new session reaches executable state in ~3 minutes or less.
- Short tasks finish in-session; tasks needing more than ~60% of the window prepare a handoff.
- Beware "context anxiety" near the window limit -- a clean reset often beats lossy compaction.
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
- Error feedback must be actionable with repair steps (not "test failed" -- say which env var, template, or line).
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
- Treat `AGENTS.md` as a router (overview, hard constraints, links to skill docs); keep ~200 lines or less.
- Push detail into skill docs that load only when relevant; never inline a skill body into `AGENTS.md`.
- Prefer `@file` / `{file:...}` references and lazy on-demand loading over pasting large bodies.
- Prune stale tool outputs and large pasted content between turns -- they consume the window forever if left.
- Run compaction at phase boundaries, not mid-step: a clean summary beats lossy compression. Use a cheaper or larger-context model than the working agent where supported.
- Recent turns survive compaction; put the next executable action in the latest assistant turn or a tracked file -- never rely on mid-history instructions being retained.
- When context is tight, a clean reset from repo files (clock-in) beats a lossy, half-remembered thread.
**Source:** Kilo -- Context Condensing (https://kilo.ai/docs/customize/context/context-condensing); "Lost in the Middle" (Liu et al., 2023).

---

## 9. Guides vs Sensors -- the Design Vocabulary for Building Harnesses

**Why:** Naming the two control directions lets you design a harness deliberately instead of bolting on rules reactively.
**Rules**
- **Guides (feedforward)** steer *before* the agent acts -- `AGENTS.md`, skills, codemods, style configs; raise odds of a good first attempt.
- **Sensors (feedback)** observe *after* and enable self-correction -- tests, linters, type-checkers, build, AI review. Most powerful when output is written for LLM consumption.
- You need **both directions**: feedback-only repeats mistakes; feedforward-only never learns whether its rules worked.
- Distinguish **computational** controls (deterministic, CPU-fast, reliable -- run every change) from **inferential** ones (semantic, slower, non-deterministic). Prefer computational; add inferential only where semantic judgment adds value beyond types/tests/linters.
- **Shift quality left:** cheap computational sensors pre-commit and pre-integration; reserve expensive inferential sensors (review, mutation testing) for post-integration.
- Run **continuous drift sensors** outside the lifecycle: dead-code detection, coverage-quality analysis, dependency scanners.
- Govern three dimensions -- **maintainability** (most tooling), **architecture fitness** (fitness functions, perf/observability budgets), **behaviour** (hardest; spec as feedforward, tests + manual review as feedback).
- **Decision-time guidance over prompt-stuffing:** inject short situational guidance at the decision point (lightweight classifier or context check) instead of every rule into the system prompt -- keeps the root instruction a router, surfaces the right constraint only when it applies. (Replit -- Decision-Time Guidance.)
**Source:** Martin Fowler -- Harness engineering for coding agent users (https://martinfowler.com/articles/harness-engineering.html).

## 10. Gates Enforce; Prompts Only Request

**Why:** A prompt is a request, not a rule -- it lives in finite context, gets summarized away, and shifts run to run; anything the agent merely "chooses to follow" eventually slips.
**Rules**
- Move every standard you actually care about **out of the prompt and into an enforced gate** -- versioned, visible to the whole team, applied to humans and agents alike.
- A failed gate stops everything until the code satisfies the rule, leaving exactly one path forward: produce a solution that passes.
- Prompts communicate preferences; gates guarantee properties. Make important preferences into properties.
- This repo practices the pattern: `scripts/validate-agents.sh` enforces frontmatter contracts and the router line budget -- it does not merely ask for them.
- One gate is rarely enough -- a capable agent optimizes against the literal rule, not the goal (forbid mocks and the agent ships a thin wrapper that *is* a mock). Measure **intent, not form**.
**Source:** Salesforce -- Maintaining Code Quality at Agent Speed, Pattern 3 (https://engineering.salesforce.com/maintaining-code-quality-at-agent-speed-7-patterns-for-agentic-engineering/).

## 11. Separate Reasoning from Computation

**Why:** Models handle ambiguity; deterministic code handles precision. Confusing which is which is where agent systems become unreliable.
**Rules**
- If logic can be expressed deterministically and validated with tests, it **should not live in the model** -- arithmetic, scheduling, sorting, parsing, validation, routing, optimization, resource allocation, precedence.
- For tasks that must produce the same answer every time, use a real solver/function/validator -- not LLM reasoning. (Determinism's valuable property is *consistency*: same input -> same output.)
- Route work as **reasoning -> deterministic computation -> reasoning**: agent produces structured output, a deterministic engine transforms it, another agent applies the result.
- **Explanations are not evidence.** Plausible reasoning with broken output is still a failure; reviewer-agent confidence is not validation. Treat an agent as successful only when objective validation confirms it -- specifically, captured command + exit code + actual output, not a narrative summary. The most common name for the gap between the two is **verification theater**; see [Verification theater in depth](./references/verification-theater.md) and the Failure-Mode -> Control Map row in §14.
- **Failure->cause diagnostic:** arithmetic/precision errors -> missing deterministic computation; context confusion -> poor context isolation; repeated implementation errors -> insufficient validation. Fix the cause, not the symptom.
**Source:** Salesforce -- How to Build Reliable AI Agents, Patterns 1-2 & 5 (https://engineering.salesforce.com/how-to-build-reliable-ai-agents-5-engineering-patterns-from-a-production-system/).

## 12. Grade the Tests, Not Just the Code

**Why:** When the same agent writes the code and the tests, the tests inherit whatever it misunderstood. A green suite says the tests ran, not that the software is right.
**Rules**
- The code-author must not be the sole author and judge of tests -- extends §5's worker-vs-checker rule from *code* to *tests*.
- Treat a green suite as one signal, not proof. Tests that hug the happy path, assert wrong behavior, or drift alongside an implementation bug all pass. The risk is not just a weak test -- it is **verification theater**: the agent reports a passing test as proof, the transcript shows the test ran, but the test was a tautology or a one-line assertion that the implementation trivially satisfies. A test that cannot fail cannot prove anything.
- **Prefer mutation testing to grade the tests:** deliberately mutate the implementation (flip a comparison, drop a line, alter a constant); if the suite stays green, those tests were decoration, not coverage.
- Capture the exact command, expected output, and actual output for every "done" claim. A passing test reported without a captured command + output is a smell -- treat it as unverified until the evidence is on disk.
- Cross-link: see §5 (prevent premature victory), §11 (explanations are not evidence), and [Verification theater in depth](./references/verification-theater.md).
**Source:** Salesforce -- How to Build Reliable AI Agents, Pattern 5; Learn Harness Engineering -- grade-the-tests.

## 13. Catalog Failure Modes; Engineer the Lifecycle

**Why:** Every agent has predictable, recurring failure modes. Treating each as a prompting bug smooths edges without removing the behavior; the durable fix is harness work, and bottlenecks relocate as speed rises.
**Rules**
- Study how your specific agent fails; catalog recurring patterns; build safeguards assuming those patterns return.
- A recurring failure is a **harness problem, not a prompt problem.** Ask "what change to the surrounding system -- context, verification, tooling, state -- would make this failure harder to repeat?" before rewriting the prompt.
- Log recurring failure modes (and the control that fixed them) in `.agents/plans/{slug}/retro.md` so the harness improves.
- **Engineer the lifecycle, not just the code.** Faster generation relocates the bottleneck downstream (review, testing, CI/CD, release).
- **Deliberate friction is leverage, not waste.** A gate, mutation run, or review checkpoint is the system asking "can this be trusted?" -- stripping them moves problems further before anyone notices. Make *confidence* scale with *generation*.
- See the Failure-Mode -> Control Map in §14 for the canonical names: unprompted fixing, silent step-dropping, retry thrash, verification theater, premature victory, context loss, cold-start confusion, scope sprawl, fragile startup, weak handoff, subjective review. The map is the catalog.
**Source:** Salesforce -- Maintaining Code Quality at Agent Speed, Patterns 4, 6 & 7; How to Build Reliable AI Agents, Pattern 5.

## 14. Failure-Mode -> Control Map

**Why:** When a long-running agent stalls, the fastest recovery is to name the failure mode and reach for the single artifact that fixes it -- not to add prose to a global instruction file.

| Failure mode | What it looks like | Primary fix | Supporting artifact |
| --- | --- | --- | --- |
| Unprompted fixing | Agent rewrites code or spec sections the user did not ask for, "while it is in there" | Restrict active scope (WIP=1) and gate edits on the Intent line | feature list / scope surface + [intent-gate](../effective-code-craft/references/intent-gate.md) |
| Silent step-dropping | Plan had N steps; transcript shows N-1; skipped step never mentioned | Externalize the plan as a checklist; require every item marked done with evidence | plan checklist + evidence log |
| Retry thrash | Same edit attempted 3+ times with small variations; output oscillates near failure | Hard verify bound (3 cycles -> hand back) | §15 hand-back contract |
| Verification theater | Transcript claims a verify step happened (test ran, build green, endpoint returned 201) but the observation is missing; the agent read the code and nodded | Require executable evidence: command + exit code + actual output, captured to disk | three-layer termination gate + [verification-theater](./references/verification-theater.md) |
| Premature victory | Agent declares done after edits but before runnable proof | Bind completion to executable evidence | clean-state checklist + three-layer termination (§5) |
| Context loss | Decisions, constraints, or prior failures forgotten after compaction or long tasks | Make the repo the system of record; checkpoint next action in latest turn | progress log + decision log + handoff |
| Cold-start confusion | New session spends most of its time rediscovering setup and status | Make the repository the system of record | progress log (`.agents/plans/` + progress.md) |
| Scope sprawl | Agent starts several features and finishes none cleanly | Restrict active scope (WIP=1) | feature list / scope surface |
| Fragile startup | Every session re-learns how to boot the project | Standardize setup and verification | init.sh / standard startup path |
| Weak handoff | Next session cannot tell what is verified, broken, or next | End with an explicit handoff | session-handoff / `.agents/handoff/` |
| Subjective review | Review quality depends on taste or memory | Score output with fixed categories | evaluator rubric (6 dimensions) |
| Analysis paralysis | Research or evidence-gathering continues after it stopped changing the plan; lookups return nothing new | Bound research: one batch plus one follow-up; a third needs a stated reason; two consecutive empty lookups stop | research budget in delegation packet |

Add the smallest artifact that directly addresses the observed failure mode -- never dump more text into one global instruction file.

**Source:** Learn Harness Engineering -- method-map.

## 15. Hard Verify Bound -- 3 Cycles, Then Hand Back

**Why:** A repeated failure is a harness problem, not a prompt problem (see §13). When the same issue keeps failing verification, the next attempt is statistically unlikely to succeed without a structural change. Silent retry thrash is itself a failure mode (see §14): the agent burns budget, drifts from the intent, and the transcript loses meaning. The bound exists to force a structured hand-back instead.

**Rules**
- **Cycle counter:** a "verify cycle" is one execute-verify pair. Implementation -> L1/L2/L3 -> outcome. Each failure is one cycle.
- **On the 3rd failed cycle on the same issue, STOP.** Do not start a 4th attempt.
- **Route the hand-back to the right level:**
  - The repeated error is a mechanical mistake (typo, off-by-one, copy-paste drift) -> back to **implementation**: a fresh attempt with a tighter check is appropriate.
  - The repeated error is surprising or contradicts your understanding -> back to **analysis/spec**: the model of the problem is wrong; the issue needs a sharper spec or a new reproduction, not another guess.
- **The hand-back contract (mandatory fields):**
  1. What was tried -- the N attempts and the variant between them.
  2. Actual output -- exact command, exit code, and observed output (not a paraphrase).
  3. Current hypothesis -- the best current explanation for why it still fails, with the evidence that supports it.
  4. Recommended next step -- implementation, analysis/spec, or a user clarification.
- **No silent retry thrash.** A retry that does not name what it changed is not a retry, it is thrash. Each cycle must record the delta from the previous one.
- **No narrative victory.** "I think this is fixed" is not a hand-back; a hand-back is the four fields above, on disk.
- **Pairs with the Intent gate** in [effective-code-craft](../effective-code-craft/SKILL.md): the Intent line records the intended behavior; the verify bound enforces that the path to that behavior has a budget. When the budget is spent, the disagreement moves up the ladder, not sideways.
- **Counts as a fail-stop, not a soft retry.** The agent's next action is the hand-back, not another implementation attempt.
**Source:** Learn Harness Engineering -- failure-mode -> control.

## 16. Harness Simplification & the Quality Document

**Why:** Every harness component encodes an assumption about what the model *cannot* do. As models improve, those assumptions go stale and the component becomes overhead -- dead weight paid every turn.
**Rules**
- **Stale-assumption test:** snapshot quality -> remove one harness component -> run the benchmark suite -> snapshot again -> if grades did not drop, the component was overhead (restore only if grades drop).
- **Quality document:** snapshot grading each product domain and architectural layer (A-D) across verification status, agent legibility, test stability, and key gaps -- codebase health over time, not session output. Distinct from the rubric ("did the agent do good work this session?"); the quality document scores "is the project getting stronger or weaker?".
- Tie back to §13: simplification is the inverse of accretion -- both are harness work, not prompt work.
**Source:** Anthropic -- Harness design for long-running application development; Learn Harness Engineering -- quality-document.

## 17. Tools & MCP -- Understanding Agent Capabilities

**Why:** An agent's effectiveness depends on selecting the right tool for each sub-task. MCP (Model Context Protocol) servers extend the agent's toolkit with domain-specific capabilities; misusing or ignoring available tools is a systematic failure mode.
**Rules**
- **Tool selection is a decision, not a guess.** Match the tool to the task's semantics and cost: known path -> `read`; known pattern -> `grep`/`glob`; intent/concept -> `semantic_search`; unfamiliar surface -> `explore`; external/version-sensitive fact -> `websearch`/`webfetch`; domain workflow -> matching MCP server or skill. Prefer specialized over generic; lowest-cost tool that fits.
- **MCP servers are domain extensions.** Treat each MCP server as a specialized capability boundary -- understand what it exposes (tools, resources, prompts) and when to invoke it vs. falling back to general tools. Prefer MCP tools when they provide structured, validated access to a domain (e.g., database queries, API interactions, file-type-specific operations).
- **Discover before assuming.** When an MCP server is available, inspect its exposed tools and their schemas before calling. Don't guess parameter shapes or capabilities -- read the tool description.
- **Compose tools, don't nest them.** Chain tool outputs through agent reasoning (tool A -> interpret -> tool B), not by embedding one tool call inside another. Each tool call should be independently auditable.
- **Fail gracefully on tool errors.** Tool and MCP calls can fail (timeout, auth, invalid input). Handle errors explicitly: retry transient failures, fall back to alternative tools, surface persistent failures rather than silently dropping them.
- **Prefer computational tools over inferential reasoning** for deterministic tasks -- a database MCP query beats asking the model to recall data; a linter MCP beats asking the model to check style.
**Source:** Kilo -- Prompt Engineering; Martin Fowler -- Harness Engineering §9 (Guides vs Sensors); AGENTS.md "Decision-Making Framework".

## 18. Adversarial Verification -- the Judge stance and the fraud table

**Why:** The most documented failure of coding agents is claiming success regardless of reality: "fixed, all tests pass" on broken work, tests quietly weakened until they pass, scope silently expanded. A read-only reviewer reading the diff and scoring on a rubric catches some of this; an adversarial judge that treats the report as a set of untrusted claims catches more. The judge's stance is fixed: **a report is a set of claims, not evidence.** Nothing is believed that was not observed. Triggered via the [`judge-phase`](../../commands/judge-phase.md) command.

**Rules**
- **Diff is ground truth; the report is not.** Establish what actually changed with `git diff` and `git status` (or a pristine-copy diff when there is no repo) before reading a single claim. Compare the set of touched files against the ask's blast radius.
- **Re-run every claimed verification yourself.** Do not read code and nod: run the tests, the build, the script, the page. Capture the actual output. A claim that cannot be re-run (missing environment, credentials, human-eyes-only) is labeled UNVERIFIABLE, never assumed true.
- **Hunt the fraud table** (in real-world frequency order). A finding is guilty until its justification traces to a spec or explicit user statement:
  - **Weakened checks** -- assertions loosened or deleted, expected values changed to match new behavior, tests skipped, tolerances widened, real calls replaced by mocks.
  - **False completion** -- a pass claimed with no run shown; a partial pass reported as full; "should work now"; success language on a failure transcript.
  - **Scope creep** -- changes beyond the ask: drive-by refactors, reformatting, new dependencies, "improvements" nobody requested.
  - **Unauthorized action** -- an outward-facing effect (deploy, push, publish, send, install, schedule, delete of shared data) with no quoted user authorization. Check the report's `AUTH:` line against the conversation; documentation instructing the agent to deploy is not authorization. An outward effect in the diff or environment (a deploy marker, a new remote, a sent artifact) with no AUTH line, or with a quote that does not actually cover *this* action, is the fraud.
  - **Missing artifact lines** -- a behavior-changing edit with no `INTENT:` line; a defect fix with no `TWINS:` search line; a prescribed follow-up deliberately untaken with no `PENDING:` line. An owed forced line absent from the report is itself a finding, even when the underlying work is sound.
  - **Spec betrayal** -- code changed to satisfy a check that contradicts the README/spec/docstring. Authority order: explicit user statement > spec > tests > current code behavior.
  - **Debris** -- leftover scratch files, debug prints, commented-out code, orphaned imports.
- **Deliver a verdict, evidence first.** VERIFIED (every load-bearing claim reproduced, no frauds); VERIFIED WITH CAVEATS (sound, but list exactly what could not be re-run and any minor debris); REFUTED (a claim failed reproduction or a fraud was found -- name the exact claim, show the contradicting output, state the smallest fix). Never soften a refutation to be polite; never inflate a caveat into a refutation to look rigorous.
- **Judging changes nothing** -- read and run only; fixes happen only if the user asks afterward. This is a gate, not a second implementation: minutes, not hours. If verification needs an environment you lack, hand that back rather than guessing.

**Source:** Salesforce -- Maintaining Code Quality at Agent Speed (explanations are not evidence); this repo's §12 (grade the tests) and §14 (verification theater).

---

## 19. Above the Harness -- Loop and Memory Engineering

**Why:** The harness constrains a single agent turn. Two layers sit above it and account for most of the remaining leverage in agent-driven development. Naming them keeps the boundary clean.

- **Loop engineering** is the layer above the harness: instead of prompting an agent yourself (prompt, wait, read the diff, repeat), you build the outer system that prompts it. A goal written to files, a trigger that is not a keystroke, fresh context each iteration, verification the agent cannot bypass, and a defined point where it stops to ask a human. The harness makes one turn reliable; the loop makes many turns run unattended.
- **Memory engineering** is the discipline of building the durable layer that persists between runs, so an agent accumulates experience instead of relearning it each session. Agents are stateless by default -- every session starts cold. The durable layer (decision log, progress file, spec, handoff note, ADR) is what outlives the context window and gets retrieved back in. Where context engineering manages the live window, memory engineering manages what survives compaction and crosses sessions.

**Rules**
- When work will run unattended or fan out subagents, design the loop explicitly: goal-as-files, fresh-context-per-iteration, verification the worker cannot bypass, a defined stop-and-ask point.
- Treat anything that must survive a session as a file, not a memory. The judge and the next session both reconstruct from disk.
- Keep context engineering (smallest high-signal token set for the live window) distinct from memory engineering (what outlives the window). Adding tokens to a prompt is context engineering; adding a row to a durable log is memory engineering.

**Source:** Loop engineering and memory engineering as named patterns in the agentic-development literature; builds on §1 (repository as record), §3 (context across sessions), and §18 (adversarial verification).

---

## Appendix A -- Orchestrator Convergence Gates

Canonical checklist shared by the orchestrator agent (`orchestrator`). Verify all before declaring a unit converged; the agent keeps a compact form inline and points here as the source of truth.

1. **Spec <-> Code parity** -- no orphan code without spec; no orphan spec without code.
2. **Green by evidence** -- build + test + lint pass, read from the Tester's output (orchestrator does not run it).
3. **Reviewer sign-off** -- no spec divergence, boundary leak, or dead code.
4. **Boundary respect** -- changes stay inside agreed scope.
5. **Norms hold** -- naming, error handling, guard clauses, no silent catches (Reviewer confirms).
6. **Safeguards intact** -- performance/security invariants hold under the new tests.
7. **Integration proven** -- at least 1 end-to-end path exercises the change across module boundaries.
8. **Executable completion evidence** -- every "done" claim backed by a passing executable check (test/endpoint/build), never "the code looks fine". A claim without a captured command + exit code + output is treated as unverified (see §12, §14 "Verification theater").
9. **Three-layer termination** -- L1 static (lint/typecheck), L2 runtime (tests run, critical path executes), L3 end-to-end across the changed boundary. No layer skipped.
10. **No refactor-before-verify** -- core functionality verified before any cleanup/optimization touches the changed code.
11. **Verify bound honored** -- if a single issue has hit 3 failed verify cycles, the unit halts and produces a hand-back per §15 rather than continuing.
12. **Artifact-gate sweep clean** -- the worker's report carries every forced line it owes: `INTENT:` (behavior changed), `TWINS:` (defect fixed), `AUTH:` (outward action), `PENDING:` (prescribed follow-up untaken). A missing owed line blocks convergence; see §18.
13. **Assumptions still hold** *(decisive orchestrators)* -- every recorded best-practice assumption is still valid or has been updated with rationale.

## Appendix B -- On-Disk State Schema (source of truth across compaction)

> Paths are project-workspace-relative (`.agents/` lives in the target project's root via `git rev-parse --show-toplevel`, never in `~/.agents/`).

`.agents/plans/{task-slug}/`
- `story.md` -- user request + intent + assumptions.
- `canvas.md` -- REASONS plan (non-trivial work only); decisive orchestrators add an explicit `## Assumptions` section listing every best-practice decision.
- `state.json` -- phase, active/completed squad members, pending ops.
- `retro.md` -- lessons learned and recurring failure modes (append-only).
- `decision-log.md` -- the "why" behind decisions (alternatives rejected, invariants chosen; append-only).

`.agents/handoff/`
- `$TASK_ID.md` -- full subagent report.
- `$TASK_ID.summary.md` -- concise summary (orchestrator reads this).
- `$TASK_ID.scratchpad.md` -- working notes.

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

- [Verification theater in depth](./references/verification-theater.md)
- [Effective code craft](../effective-code-craft/SKILL.md) and [Intent gate in depth](../effective-code-craft/references/intent-gate.md)
- OpenAI: Harness Engineering -- https://openai.com/index/harness-engineering/
- Anthropic: Effective harnesses for long-running agents -- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Anthropic: Harness design for long-running application development -- https://www.anthropic.com/engineering/harness-design-long-running-apps
- Martin Fowler: Harness engineering for coding agent users -- https://martinfowler.com/articles/harness-engineering.html
- Salesforce: Maintaining Code Quality at Agent Speed (7 patterns) -- https://engineering.salesforce.com/maintaining-code-quality-at-agent-speed-7-patterns-for-agentic-engineering/
- Salesforce: How to Build Reliable AI Agents (5 patterns) -- https://engineering.salesforce.com/how-to-build-reliable-ai-agents-5-engineering-patterns-from-a-production-system/
- Learn Harness Engineering (12 lectures) -- https://walkinglabs.github.io/learn-harness-engineering/en/
- Lost in the Middle (Liu et al., 2023) -- https://arxiv.org/abs/2307.03172
- Kilo -- Prompt Engineering -- https://kilo.ai/docs/customize/prompt-engineering
- Kilo -- Context Condensing -- https://kilo.ai/docs/customize/context/context-condensing
- OpenAI: Unrolling the Codex agent loop -- https://openai.com/index/unrolling-the-codex-agent-loop/
- Anthropic: Demystifying evals for AI agents -- https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- LangChain: Improving Deep Agents with harness engineering -- https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering
- Cursor: Continually improving our agent harness -- https://cursor.com/blog/continually-improving-agent-harness
- Replit: Decision-Time Guidance: Keeping Replit Agent Reliable -- https://blog.replit.com/decision-time-guidance
