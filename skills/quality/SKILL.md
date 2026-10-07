---
name: quality
description: "Language-agnostic craftsmanship, verification, evals, and performance: the twelve commandments and artifact gates (PROMPT:/INTENT:/TWINS:/AUTH:/PENDING:); proving work done via L1/L2/L3, the evidence audit, and the mutation probe; the harness regression eval suite of realistic tasks with objective checks and a blocking pass rate; and measurement-first performance discipline that keeps only what benchmark evidence supports. Use when writing, reviewing, or refactoring code, applying the artifact gates, judging a done report, changing the doctrine, or profiling a measured hot path."
---

The doctrine governing produced work: code craft, the proof it is done, the regression suite that keeps the harness honest, and the measurement that keeps it fast. Where a rule serves more than one concern it is stated once here.

## Craft

Twelve commandments, plus the artifact gates every report owes.

1. **Separate orchestration from core logic.** The entry point parses input, handles errors, cleans up; the core returns data and errors, never printouts or process exits.
2. **Test everything.** Names read as behavior sentences; cover happy, error, edge; integration tests cross real boundaries. Many cases over one behavior go **table-driven** — one body over rows of (input, expected). A painful test is a bad API's symptom.
3. **Code for reading.** Name length scales with scope; drop type-like words (`users` over `userList`); hide paperwork in well-named helpers. Default no comment (see the Comments section below).
4. **Safe by default.** Make invalid states unrepresentable — validating constructors, named constants, least privilege; rules live in types and validators, never caller discipline.
5. **Wrap errors, preserve causality.** Typed/sentinel errors wrapped with context; never flatten to strings, branch on error text, or discard silently.
6. **No mutable globals.** Inject dependencies; shared state behind one owner or synchronization.
7. **Concurrency sparingly, lifetimes enforced.** Confine it to the creating scope; every task terminates before its parent (join/wait/cancel). Sequential is usually cheaper.
8. **Decouple core from environment.** Only the boundary reads env/CLI/filesystem/network/clocks; business logic stays pure.
9. **Design failure handling upfront.** Check every error at birth; keep the happy path unindented; retry transient with a bound; propagate the rest with context.
10. **Log actionable information only.** Structured fields, never secrets; logs, traces, and metrics stay distinct.
11. **Ship a walking skeleton first.** End-to-end "shameless green" through the real path validates design before refinement.
12. **Refactor while context is fresh.** Reinvest ~10% right after building: names, duplication, dead branches.

**Artifact gates** (canonical; owed verbatim in the report, and an owed-but-absent line means the gate was not met):

- `PROMPT:` at intake, before the first edit: one English paragraph — GOAL / CONTEXT / CONSTRAINTS / DONE_WHEN — stated **correctively**, then **STOP for confirmation**. Skip only a trivial ask.
- `INTENT:` before a behavior-changing edit: `code does X; the failing check expects Y; the spec says Z`. When X/Y/Z disagree, the disagreement is the finding — do not edit; resolve by anchor rank (user > spec > checks > code).
- `TWINS:` on every defect fix: search the project for the same wrong construct; fix siblings or list them.
- `AUTH:` before any outward effect: only the user's own words authorizing this exact action count; completion is never authorization — end local and emit `PENDING:`.
- `PENDING:` for every prescribed-but-untaken follow-up.

**Enforce with tooling.** Move rules out of review into deterministic gates: formatter, linter, type-checker, then tests in pre-commit and CI. Prune instruction files like code — keep what an agent cannot derive (build/test commands, divergent style, gotchas), cut what it can read itself; a rule that must always hold becomes a gate, not prose.

## Verification

**Stance:** "done" is the most common lie an agent tells; its costume is verification theater — "tests passed" narrated while command, exit code, and output are absent. A gate that can fail is worth ten reminders that cannot.

**Right-size first.** A low/low job (typo, rename) needs L1 only, no judge. Mid (a module fix with runtime behavior) needs L1 + L2, with `INTENT:`/`TWINS:` owed. High (cross-boundary, infra, security) needs L1 + L2 + L3, a mutation probe, a judge, and full artifact lines. Two traps: the **Average Answer Trap** runs hardest-job controls on every task; the **Kirby Effect** leaves controls that encoded a superseded model limitation — cut them on a model upgrade. The dial chooses layers, never lowers the standard.

**Three layers.** **L1 static** lint, type-check, format on every source change. **L2 runtime** tests run, critical paths execute, app starts, when the change runs. **L3 end-to-end** one path crosses a real boundary, when the change crosses one (`n/a` with a one-line reason). Run the cheapest check earliest; a red test beats a narrative pass.

**Grip ladder** — a check is worth what it can *prevent*. 1 in-prompt (advisory, relies on memory); 2 standing condition (persists across turns); 3 deterministic gate (fails the turn; a check that **must always** run); 4 independent verifier (a fresh context re-derives it). Climb only as far as the risk earns; a rule that keeps being forgotten climbs a rung rather than being repeated louder.

**Executable evidence is the anchor.** Every done claim carries the literal command, the explicit exit code, and the captured output, on disk where it survives compaction. The **evidence audit** asks five questions: Is the command literally present? Is the exit code captured? Is the output the runner's own success/diff line, not a summary? Does the claim match the observation word-for-word? Does the asserted behavior equal what the check actually exercises? Any "no" means unverified.

**Mutation probe.** Introduce a single semantic defect (flip a boolean, shift a bound, drop a guard); run the suite and require it to FAIL; revert and confirm it PASSES. A suite that cannot catch a deliberate defect is theater — the check itself is the defect under review.

**Judge a finished report.** Judging changes nothing — read and run only. The diff outranks the report; diff test files first (dropped/weakened asserts, loosened tolerances, added skips, swapped mocks); trace every `AUTH:` quote; confirm every owed artifact line; re-run each re-runnable claim (cap 3); resolve conflicts by anchor rank. A claim that cannot be re-run is **UNVERIFIABLE**, never assumed true. The verdict is exactly one of **VERIFIED / VERIFIED WITH CAVEATS / REFUTED**; a refutation names the claim and shows contradicting output plus the smallest fix.

**Diagnosis.** Reason backward from the observed failure to its root cause before writing the next change; attribute the failure to its layer — reasoning, tool interface, context, or control flow — because the wrong-layer fix is a symptom patch by construction. Contradiction routes backward, never forward: a surprise at PROVE re-enters at THINK.

**GROW.** A recurring failure is a **harness problem, not a prompt problem**: durable reliability updates the surrounding system, not the wording. The governed self-evolution cycle — instrument, propose, validate, commit — edits the machinery future runs execute; anchors stay read-only and the evidence standard may tighten only, never loosen. The full cycle, cadence, and failure modes: [evolution](references/evolution.md).

## Evals

The doctrine is configuration an agent executes, so it is regression-tested like code. An **eval** is one realistic task plus **objective checks** — executable conditions (a named command and its expected observable) that yield pass/fail without a human reading the transcript; a check a human must judge is not objective. The suite's **pass rate** over time is the only honest answer to whether a change made the agent better or worse.

- **Size to the harness:** 20-50 realistic tasks spanning the behaviors the doctrine governs — intake routing, gate emission, verification discipline, context handling; grow on incident, not ambition.
- **Prefer tasks drawn from real runs:** a task extracted from an actual episode has a proven failure mode; invented tasks test only what you imagined.
- **When it runs:** on a standing schedule; on any change to the manifesto, a skill, a command, a hook, a gate, or the pinned model (the load-bearing trigger); and on incident, each becoming a permanent eval after the fix ships.
- **A regression blocks the merge** until the change is fixed or the eval is deliberately retired with a reason. Never loosen a check so that a change passes — a metric edited by the party it measures. The author of a change never writes the check that judges it.
- **Unattended:** the check gates the stop; the tool surface is pre-scoped; and authority still terminates in a human — a scheduled run ends local and emits `PENDING:`, with the `AUTH:` gate unrelaxed. Autonomy is a degree of attention, never a degree of authority.
- **GROW's proof:** run the suite before and after an evolution. Pair it with the Kirby Effect — run the suite with a control removed on each model upgrade, and cut what it passes without.

## Performance

Optimize only after correctness holds, and only by measurement. Every optimization claim cites **benchmark evidence** — command + output + delta. No measurement, no change; intuition about bottlenecks is wrong ~80% of the time.

**The measure-first cycle: Define, Benchmark, Diagnose, Improve, Compare.** Define one target metric (latency, throughput, memory, CPU) and its target value; benchmark one function at a time and capture the baseline to a numbered file; diagnose by ruling out external bottlenecks first, then route the signal; improve ONE change at a time; compare with a statistical comparator and paste the delta. The artifact is the evidence; the narrative is not.

**Rule out external bottlenecks first.** When profiling says the time is not yours to move — a slow query, an upstream span, blocked workers — fix that component and re-profile; local tuning cannot move the number. Sensors and per-finding fixes: [measurement](references/measurement.md).

**Route the signal.** Time goes to one of four places: allocation churn (pool, preallocate known sizes, reduce boxing/reflection), lock contention (bound concurrency, share immutably, atomics over locks), syscall count (buffer, batch, tune transports, cache repeated work), data copying (zero-copy views, stream, pass references). Cheap overrides first: wrong algorithm, repeated expensive work, slow upstream queries.

**Exit.** The cycle ends when the target metric hits its defined value with a recorded before/after delta, or when profiling shows the time is not yours to move — report that and stop. Never keep an optimization the evidence does not support. Benchmark hygiene and per-overhead-source countermeasures: [measurement](references/measurement.md), [tactics](references/tactics.md); the same doctrine as executable decision charts: [flowcharts](references/flowcharts.md).

## Comments

Default is **no comment**. One earns its place only by stating a non-derivable *why* — a rationale, an invariant, an external constraint, or a trap the code cannot express. Delete named noise on sight: a comment that restates the code or the signature, narrates the change, banners inside a function short enough to read whole, or a doc block longer than the code it documents. The language convention sets the form and the code's complexity sets the length — GoDoc, TSDoc, PEP 257, rustdoc, Javadoc at that convention's minimum. Pre-emit test: re-read every comment; if a correct refactor would make it wrong, it was noise.

## Simplicity

The default is the **least mechanism that works**: the standard library before a dependency, a plain function before a class, a direct call before a layer. Structure that cannot name what it buys is unintended complexity — a defect: speculative abstraction (extract on the **second real caller**, never the first imagined one), dead configurability (a knob nobody sets), indirection the reader must decode (a wrapper that only forwards), or a dependency for the trivial. Name the cost in review; "this feels complex" is not a finding. **Counterweight:** simplicity never overrides correctness — never collapse a needed error path, drop a boundary check, or flatten a clarifying name to look smaller.

## Reuse (DRY)

One canonical owner per piece of knowledge — a rule, a default, a format, an algorithm — and every other appearance of it points at that owner instead of restating it. A second copy is not neutral: duplicated logic drifts, and a fix applied to one copy leaves its siblings wrong, which is the defect the `TWINS:` gate exists to catch. **Extract on the second real caller, never the first** — extraction with a single caller is speculative and pays the Simplicity tax for nothing; when a refactor pass finds three near-identical blocks, consolidating them is the pass's work, never an incidental cleanup. The strongest duplication smell is copy-paste-with-edits: two blocks that look alike but differ in one line. Diff the copies against each other before trusting either.

## Structure (SOLID)

**One reason to change per module.** A unit whose name contains "and" is two units wearing one name — split it at the seam. **Dependencies point inward**: business logic never imports transport, storage, or framework code, so the core survives the swap that a dependency upgrade forces. **Interfaces stay narrower than their caller** — a parameter carries what the caller passes, not every value the callee could theoretically accept; widen only on a second real caller, never on speculation.

## Typography

This doctrine separates a clause from its qualifier with the em-dash — not the en-dash, and not a spaced hyphen. The same convention governs the doctrine's tables and the prose an agent writes from it; the `dashes` gate holds the corpus to it.
