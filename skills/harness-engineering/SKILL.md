---
name: harness-engineering
description: "Harness-engineering norms across the THINK→ACT→PROVE→GROW loop: repo-as-record, split instructions, WIP=1, three-layer termination (L1/L2/L3), mutation testing, adversarial judging, and error budgets. Use when configuring agent controls, verifying work constraints, or establishing reliability patterns."
---

# Harness Engineering -- Agent-Loadable Norms

A strong model still fails when the closed-loop system around it is weak. The harness constrains behavior, preserves context, defeats premature victory, verifies with executable evidence, and makes runtime observable across the THINK→ACT→PROVE→GROW loop.

> **Override.** A project-level harness spec that explicitly supersedes this skill takes precedence.

**Stance:** You treat "done" as the most common lie an agent tells. Verification is observed evidence, not narrated confidence; a gate that can fail is worth ten reminders that cannot.

**Right-size, don't overengineer.** The controls below exist because real failures once demanded them -- not because every job needs all of them. Two anti-patterns to refuse: the **Average Answer Trap** (treating high-complexity controls as defaults -- a typo does not need L3, a mutation probe, a judge, and a GROW retro) and the **Kirby Effect** (a component that encodes a model-limitation assumption and turns into dead weight as models improve). Dial every control to the job's action and context complexity; add a control only when a failure demands it, and revisit each one when a stronger model arrives. See [Right-sizing the harness](./references/right-sizing.md).

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
- Compaction resilience: critical state is flushed to the repo (`canvas.md`, `decision-log.md`, evidence, next action) at the end of every turn so post-compaction resume is a file read, not a guess.
- Prefer persisted ledgers (`state.json`, `decision-log.md`) and **handoff notes** over embedded prose in instructions.

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

- **Specialized over generic (route by capability, not tool name -- names vary by host):** a known path -> open and read the file; a known pattern -> search by string or filename; a concept or unfamiliar surface -> semantic/code search if your host offers it, else a narrow string search; an external fact -> web search or fetch. Pick the lowest-cost capability that fits, mapped to whatever tool your host exposes. Never call a tool by a name from another runtime.
- **Fail gracefully:** Handle tool/MCP errors explicitly with retries or fallbacks. Never swallow an error.
- **Actionable feedback:** Error feedback must name the root cause and next action.

---

## 7. Three-Layer Termination (PROVE Phase)

**Why:** "Done" is the most common lie an agent tells. Executable evidence (command + exit code + actual output) is required -- but *how many layers* you run is **dialed to job complexity**, not applied wholesale. See [Right-sizing the harness](./references/right-sizing.md).

- **L1 Static:** Lint, type-check, format. Run on every source change.
- **L2 Runtime:** Unit/integration tests run; application starts; critical paths execute. Run when the change has runtime behavior.
- **L3 End-to-End:** At least one path exercises the change across real boundaries (subprocess, network, DB, HTTP, FS). Run when the change crosses such a boundary; `n/a` is allowed with a one-line reason.

The dial chooses which layers; it never lowers the evidence standard -- whatever you run, you capture command + exit code + output. No repro -> no fix. Reproductions are executable evidence, not narrative summaries.

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
| Weakened checks | Test thresholds loosened, asserts dropped or changed to match new behavior, tests skipped, tolerances widened, real calls replaced by mocks |
| False completion | Pass claimed with no run shown; "should work now"; success language on a red transcript |
| Scope creep | Changes beyond the ask: drive-by refactors, reformatting, new deps, files outside active task scope |
| Unauthorized action | Unquoted outward-facing side effects -- pushes, deploys, publishes, sends, installs, destructive actions |
| Missing artifact lines | Owed forced line absent: behavior change without `INTENT:`, defect fix without `TWINS:`, outward action without `AUTH:`, untaken follow-up without `PENDING:` |
| Spec betrayal | Code changed to satisfy a check that contradicts the README/spec/docstring |
| Debris | Leftover scratch files, debug prints, commented-out code, orphaned imports, speculative TODOs |

Deliver exactly one verdict: **VERIFIED**, **VERIFIED WITH CAVEATS**, or **REFUTED**.

## 11. Structured Handoffs & Clean-Session Exit (PROVE Phase)

- **Handoff Artifacts:** Ensure `decision-log.md` and `state.json` are current with the latest turn's blocker and next action.
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
| Silent step-dropping | Step omitted in multi-step task | Progress ledger checkpoint | `state.json` |
| Retry thrash | 3+ edit attempts with small variations | Hard verify bound (§9) | §9 Hand-back payload |
| Verification theater | Green test suite that tests nothing | Mutation testing probe (§8) | `references/verification-theater.md` |
| Premature victory | Claiming "fixed" without proof | Three-layer termination (§7) | Captured command + output |
| Context loss | Constraints forgotten post-compaction | Repo as system of record (§1) | `state.json` + `decision-log.md` |
| Fragile startup | Fresh checkout build/test fails | Standard startup check (§11) | L1 static gate |
| Scope sprawl | Unrelated files edited | WIP = 1 & Scope pin (§5) | `canvas.md` / delegation SCOPE |
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

Before declaring a unit complete, verify every gate. Layers and the mutation probe are **dialed to job complexity** ([right-sizing map](./references/right-sizing.md)): mark a layer `n/a` with a one-line reason when the change cannot reach it, rather than forcing it.

1. **Spec is current** -- spec matches implementation; no un-documented behavior changes.
2. **Scope is pinned** -- modified files match the pinned SCOPE (`canvas.md` / delegation packet) exactly.
3. **L1 static passes** -- linting, type-checking, formatting clean.
4. **L2 runtime passes** -- tests pass, runtime executes; output captured in report (or `n/a` with reason).
5. **L3 end-to-end passes** -- real boundaries exercised; output captured in report (or `n/a` with reason).
6. **Mutation probe verified (when owed)** -- for units that bear behavior under test, a probe was run and reverted cleanly; trivial/format-only units skip with a one-line note.
7. **Artifact gates present** -- `INTENT:`, `TWINS:`, `AUTH:`, `PENDING:` written where owed.
8. **Decision log updated** -- durable choices recorded in `decision-log.md`.
9. **State current** -- `state.json` reflects unit status; next action stated.
10. **Repo clean of debris** -- no leftover probes, debug prints, or untracked files.
11. **Verify bound honored** -- max 3 cycles; hand-back payload emitted if blocked.
12. **Adversarial judge passed** -- verdict is VERIFIED or VERIFIED WITH CAVEATS.

---

## Operating Standards (always-on)

- **Repo as Record:** All plan state lives on disk (`canvas.md`, `state.json`, `decision-log.md`, `retro.md`).
- **Clean exit:** Startup and verification pass; speculative edits reverted.
- **No secret leakage:** Never log tokens, keys, or credentials.
- **Executable evidence required:** "Done" requires captured command + exit code + actual output.

---

## Cross-References

- [Verification theater in depth](./references/verification-theater.md) -- load when §8 (Grade the Tests) or §10 (Adversarial Judge) needs the full mutation testing protocol.
- [Right-sizing the harness](./references/right-sizing.md) -- two-axis complexity map; load when deciding how many layers to run and whether mutation, judging, or a GROW retro are warranted.
- [effective-code-craft](../effective-code-craft/SKILL.md) -- code craft commandments, artifact gates (`INTENT:`, `TWINS:`, `AUTH:`, `PENDING:`)
- [spec-driven-development](../spec-driven-development/SKILL.md) -- specification-first workflow for THINK phase

