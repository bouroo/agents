---
name: harness-engineering
description: >
  Harness-engineering norms across the THINK→ACT→PROVE→GROW loop: repo-as-record, split instructions,
  WIP=1, three-layer termination (L1/L2/L3), mutation testing, adversarial judging, error budgets,
  and the self-improving harness (GROW phase). Grounded in the OpenAI/Anthropic harness canon, Martin Fowler's
  harness-engineering model, and Salesforce agentic reliability patterns.
---

# Harness Engineering -- Agent-Loadable Norms

A strong model still fails when the closed-loop system around it is weak. The harness constrains behavior, preserves context, defeats premature victory, verifies with executable evidence, and makes runtime observable across the THINK→ACT→PROVE→GROW loop.

> **Override.** A project-level harness spec that explicitly supersedes this skill takes precedence.

**Stance:** You treat "done" as the most common lie an agent tells. Verification is observed evidence, not narrated confidence; a gate that can fail is worth ten reminders that cannot.

**Modes:**

- **Build mode** -- designing or extending an agent harness. Walk the THINK→ACT→PROVE→GROW lifecycle; emit gates, handoff artifacts, and failure-mode controls. Sequential.
- **Review mode** -- grading a transcript or live run for harness quality. Audit against the §Failure-Mode -> Control Map and the §Adversarial Judge fraud rubric. Sequential.
- **Audit mode** -- sweeping an existing codebase or transcript for harness gaps. Launch up to 5 parallel sub-agents, one per concern: (1) context/memory engineering, (2) gates and three-layer termination, (3) handoff and resume artifacts, (4) verification theater / mutation-grade tests, (5) observability and GROW retro loop.

---

## The THINK→ACT→PROVE→GROW Harness Lifecycle

The agent harness operates in a continuous loop:

1. **THINK (Discovery & Context Control):** Establish repo-as-record, split instructions, isolate context window, feedforward guides, and decision gates before execution.
2. **ACT (Surgical Execution):** Maintain WIP = 1, select optimal specialized tools/MCPs, handle errors gracefully, and separate reasoning from deterministic computation.
3. **PROVE (Verification & Termination):** Enforce three-layer termination (L1/L2/L3), run mutation testing probes, observe hard verify bounds, and pass adversarial judgment.
4. **GROW (Self-Improving Harness):** Catalog recurring failure modes in retrospectives (`retro.md`), update failure-mode controls, adjust error budgets, and strengthen surrounding gates.

---

## 1. Repository as System of Record (THINK Phase)

**Why:** Conversation state is lost every session; decisions and evidence must survive.

- Treat the repository as the only durable memory. Restart work from files; never from recollection of prior turns.
- Every assumption that influences a decision lives on disk: commit message, spec, ADR, decision log entry. Invisible decisions are un-auditable.
- Compaction resilience: critical state is flushed to the repo (`plan.md`, `decisions.md`, evidence, next action) at the end of every turn so post-compaction resume is a `read`, not a guess.
- Prefer **decision logs** (`progress.md`, `decisions.md`) and **handoff notes** over embedded prose in instructions.

## 2. Split Instructions & Minimal Live Context (THINK Phase)

**Why:** Monolithic instructions degrade into unread text; oversized context dilutes model attention.

- Keep `AGENTS.md` a **router**: overview, hard constraints, and links. Detail lives in `skills/<name>/SKILL.md` and on-demand topic docs.
- Load skill content on demand, matched to the current task. Never pre-load unrelated skills.
- Keep the live context window small: lazy references over inlined bodies. Two layers: **context engineering** (live window) vs **memory engineering** (repo state on disk).

## 3. Feedforward Guides vs Feedback Sensors (THINK Phase)

**Why:** Agent failure modes cluster into missing guidance (feedforward) and missing detection (feedback).

- **Feedforward (Guides):** Pre-execution constraints, prompts, schemas, and checklist specs that direct action before work begins.
- **Feedback (Sensors):** Post-execution checks, tests, linters, runtime probes, and adversarial judges that measure results after work executes.
- Diagnose failure first: classify as missing guide (add feedforward) or missing sensor (add feedback).

## 4. Gates Over Prompts (THINK Phase)

**Why:** A prompt asking the agent to "remember to verify" loses to a gate that fails when verification is absent.

- Encode standards as **deterministic gates**, not reminders. A failed gate stops everything until code satisfies the rule.
- A gate requires: a clear pass condition, an actionable failure message naming the next action, and an owner (the harness, not agent memory).
- Separate reasoning from computation: deterministic logic (parsing, validation, arithmetic, schema checks) belongs in executable scripts/tests, not LLM reasoning.

---

## 5. WIP = 1 (ACT Phase)

**Why:** Parallel workstreams and unfinished tasks accumulate state that breaks resume and review.

- Finish and verify the current unit before starting the next. One open unit of work at a time.
- A unit has clear acceptance criteria, an owner, and a verification path. Split multi-unit tasks at the gate, not in flight.
- Parked work goes to disk with a clear resumption note (`handoff.md`).

## 6. Tool & MCP Usage (ACT Phase)

**Why:** Reliability depends on selecting the right tool for each sub-task and handling failures cleanly.

- **Specialized over generic:** Use lowest-cost tool that fits: known path -> `read`; known pattern -> `grep`/`glob`; concept -> `semantic_search`; unfamiliar surface -> `explore`; external fact -> `websearch`/`webfetch`.
- **Fail gracefully:** Handle tool/MCP errors explicitly with retries or fallbacks. Never swallow an error.
- **Actionable feedback:** Error feedback must name the root cause and next action.

---

## 7. Three-Layer Termination (PROVE Phase)

**Why:** "Done" is the most common lie an agent tells. Executable evidence (command + exit code + actual output) is required at every layer; skip none.

- **L1 Static:** Lint, type-check, format. Cheap, fast, catches static errors.
- **L2 Runtime:** Unit/integration tests run; application starts; critical paths execute.
- **L3 End-to-End:** At least one path exercises the change across real boundaries (subprocess, network, DB, HTTP, FS).

No repro -> no fix. Reproductions are executable evidence, not narrative summaries.

## 8. Grade the Tests & Mutation Testing (PROVE Phase)

**Why:** A passing test suite can be **verification theater** -- a suite that passes because assertions were removed, mocked out, or trivialized.

- See [Verification theater in depth](./references/verification-theater.md).
- Apply **mutation testing probes**: intentionally introduce a single semantic defect into implementation code (flip a boolean, shift a bound, drop a guard). Run the suite and require it to FAIL. Revert the mutation and verify it PASSES.
- If the mutated code stays green, the tests are weak or theatrical. Strengthen tests within SCOPE before proceeding. Revert all probes before declaring completion.

## 9. Hard Verify Bound (PROVE Phase)

**Why:** Silent retry thrash burns budget and produces noisy transcripts.

- A "verify cycle" is one execute-verify iteration.
- On the **3rd failed cycle** on the same issue, **STOP**. Do not start a 4th attempt.
- Produce a structured hand-back payload:
  1. What was tried (attempts & deltas).
  2. Executable evidence (captured output, commands, exit codes).
  3. Current hypothesis.
  4. Recommended next move (sharpen spec, fix repro, escalate).

## 10. Adversarial Judge (PROVE Phase)

**Why:** The judge treats the report as untrusted claims. Triggered via `judge-phase` or verification sweeps.

### Fraud Rubric

| Fraud | Signal |
| --- | --- |
| Weakened checks | Test thresholds loosened, asserts dropped, mocks broadened |
| False completion | Pass claimed with no output shown; "should work now"; success language on red test |
| Scope creep | Files modified outside active task scope |
| Unauthorized action | Unquoted side effects, pushes, deploys, destructive actions |
| Missing artifact lines | Missing `INTENT:`, `TWINS:`, `AUTH:`, or `PENDING:` markers |
| Spec betrayal | Implementation diverges from spec without spec update |
| Debris | Debug prints, commented code, speculative TODOs left in tree |

Deliver exactly one verdict: **VERIFIED**, **VERIFIED WITH CAVEATS**, or **REFUTED**.

## 11. Structured Handoffs & Clean-Session Exit (PROVE Phase)

- **Handoff Artifacts:** Ensure `decisions.md`, `progress.md`, and latest turn state current blocker and next action.
- **Clean Exit:** All standard startup checks pass; L1/L2/L3 pass; speculative edits reverted; no debris.

---

## 12. Self-Improving Harness (GROW Phase)

**Why:** A recurring failure is a **harness problem, not a prompt problem.** Prompt tweaks smooth edges temporarily; durable reliability comes from updating the surrounding harness system.

### The GROW Phase Protocol

1. **Catalog Failure Modes:** Log every recurring failure mode in `.agents/plans/{slug}/retro.md`.
2. **Convert Findings into Gates:** For every cataloged failure, build a deterministic check, linter rule, or verification gate that makes repeating the failure impossible.
3. **Refine Failure-Mode Controls:** Maintain and update the Failure-Mode → Control Map across sessions.
4. **Manage Error Budgets:** Track failure frequency per category; when a failure budget is exceeded, halt development to upgrade harness sensors or guides.

---

## 13. Failure-Mode -> Control Map (GROW Phase)

| Failure mode | What it looks like | Primary fix | Supporting artifact |
|---|---|---|---|
| Unprompted fixing | Editing files when user asked "why?" | Classify Ask gate (§THINK) | `effective-code-craft` §Ask shape |
| Silent step-dropping | Step omitted in multi-step task | Progress ledger checkpoint | `progress.md` |
| Retry thrash | 3+ edit attempts with small variations | Hard verify bound (§9) | §9 Hand-back payload |
| Verification theater | Green test suite that tests nothing | Mutation testing probe (§8) | `references/verification-theater.md` |
| Premature victory | Claiming "fixed" without proof | Three-layer termination (§7) | Captured command + output |
| Context loss | Constraints forgotten post-compaction | Repo as system of record (§1) | `progress.md` + `decisions.md` |
| Fragile startup | Fresh checkout build/test fails | Standard startup check (§11) | L1 static gate |
| Scope sprawl | Unrelated files edited | WIP = 1 & Scope pin (§5) | `task.md` scope boundary |
| Subjective review | Reviewer narratives over red tests | Conflict rule: red test wins | Adversarial judge verdict (§10) |

---

## 14. Error Budget (GROW Phase)

**Why:** Systems without error budgets over-spend on prose warnings or under-invest in structural safety.

- Allocate tolerable error thresholds for a task or release.
- When failure rates exceed budget, stop adding prompt instructions; build or update harness gates per the Failure-Mode → Control Map.

---

## 15. Skill Composition

**Why:** Skills are the modular unit of harness capability.

- One skill per coherent concern. Load on demand; never pull unrelated skills into context.
- Skills declare `name` (kebab-case) and `description` with trigger conditions ("Use when...").
- Skills compose seamlessly: e.g. `spec-driven-development` (THINK) + `effective-code-craft` (ACT) + `harness-engineering` (PROVE/GROW).

---

## Appendix A: Convergence Checklist

Before declaring a unit complete, verify every gate:

1. **Spec is current** -- spec matches implementation; no un-documented behavior changes.
2. **Scope is pinned** -- modified files match `task.md` SCOPE exactly.
3. **L1 static passes** -- linting, type-checking, formatting clean.
4. **L2 runtime passes** -- tests pass, runtime executes; output captured in report.
5. **L3 end-to-end passes** -- real boundaries exercised; output captured in report.
6. **Mutation probe verified** -- at least one probe run and reverted cleanly.
7. **Artifact gates present** -- `INTENT:`, `TWINS:`, `AUTH:`, `PENDING:` written where owed.
8. **Decision log updated** -- durable choices recorded in `decisions.md`.
9. **Progress log updated** -- `progress.md` current; next action stated.
10. **Repo clean of debris** -- no leftover probes, debug prints, or untracked files.
11. **Verify bound honored** -- max 3 cycles; hand-back payload emitted if blocked.
12. **Adversarial judge passed** -- verdict is VERIFIED or VERIFIED WITH CAVEATS.

---

## Operating Standards (always-on)

- **Repo as Record:** All plan state lives on disk (`task.md`, `progress.md`, `decisions.md`, `retro.md`).
- **Clean exit:** Startup and verification pass; speculative edits reverted.
- **No secret leakage:** Never log tokens, keys, or credentials.
- **Executable evidence required:** "Done" requires captured command + exit code + actual output.

---

## Cross-References

- [Verification theater in depth](./references/verification-theater.md) -- load when §8 (Grade the Tests) or §10 (Adversarial Judge) needs the full mutation testing protocol.
- [effective-code-craft](../effective-code-craft/SKILL.md) -- code craft commandments, artifact gates (`INTENT:`, `TWINS:`, `AUTH:`, `PENDING:`)
- [spec-driven-development](../spec-driven-development/SKILL.md) -- specification-first workflow for THINK phase

---

## References

- OpenAI: Harness Engineering -- https://openai.com/index/harness-engineering/
- Anthropic: Effective Harnesses for Long-Running Agents -- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Martin Fowler: Harness Engineering for Coding Agent Users -- https://martinfowler.com/articles/harness-engineering.html
- Salesforce: Maintaining Code Quality at Agent Speed -- https://engineering.salesforce.com/maintaining-code-quality-at-agent-speed-7-patterns-for-agentic-engineering/
- Learn Harness Engineering (12 lectures) -- https://walkinglabs.github.io/learn-harness-engineering/en/
