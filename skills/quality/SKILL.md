---
name: quality
description: "Use when writing, reviewing, refactoring, or judging code, and when deciding whether work is actually done — especially when a done report needs judging, tests pass but you do not believe them, or a hot path must get faster. Covers the twelve commandments, the artifact gates (PROMPT:, INTENT:, TWINS:, AUTH:, PENDING:, L1:), L1/L2/L3 evidence, the evidence audit and mutation probe, the Generate-Verify-Refine-Deliver loop, the blocking eval suite, and measurement-first performance — even if the ask never says 'quality' or 'verify'. Not for architecture-level decisions (architecture), wiki operations (confluence), or repository-wide search (indexed-search)."
license: Apache-2.0
---

The doctrine governing produced work: code craft, the proof it is done, the regression suite that keeps the harness honest, and the measurement that keeps it fast. Where a rule serves more than one concern it is stated once here.

## Craft

Twelve commandments, plus the artifact gates every report owes.

1. **Separate orchestration from core logic.** The entry point parses input, handles errors, cleans up; the core returns data and errors, never printouts or process exits.
2. **Test everything.** Names read as behavior sentences; cover happy, error, edge; integration tests cross real boundaries. Many cases over one behavior go **table-driven** — one body over rows of (input, expected). A painful test is a bad API's symptom. Tests and doubles obey the type discipline of the code under test: mocks, fakes, and stubs are typed against the real interface, never loosened because "it's only a test" — a loosely-typed double makes the test compile against a lie.
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

- `PROMPT:` at intake, before the first edit: one English paragraph — GOAL / CONTEXT / CONSTRAINTS / DONE_WHEN — stated **correctively**. The run stops for confirmation only when the corrected reading could change the work materially — a genuine ambiguity, a competing reasonable interpretation, or an irreversible or outward action; a small, local, reversible, unambiguous reading proceeds and names the reading it acted on. Skip the gate only for a trivial ask.
- `INTENT:` before a behavior-changing edit: `code does X; the failing check expects Y; the spec says Z`. When X/Y/Z disagree, the disagreement is the finding — do not edit; resolve by anchor rank (user > spec > checks > code).
- `TWINS:` on every defect fix: search the project for the same wrong construct; fix siblings or list them.
- `AUTH:` before any outward effect: only the user's own words authorizing this exact action count; completion is never authorization — end local and emit `PENDING:`.
- `PENDING:` for every prescribed-but-untaken follow-up.
- `L1:` in the done report on every source change: the project's own lint/format/type-check commands — **discovered from its manifests and scripts** (the dependency and task manifests, the pre-action check configuration, the continuous-integration pipeline definition), never assumed absent; absence is claimed only after checking those. Each command carries its literal command line and exit code; a red command fails done. `L1: n/a — <one-line reason>` only when the change touched no source.

**Enforce with tooling.** Move rules out of review into deterministic gates: formatter, linter, type-checker, then tests in the pre-action check and the continuous-integration pipeline. Prune instruction files like code — keep what an agent cannot derive (build/test commands, divergent style, gotchas), cut what it can read itself.

## Verification

**Stance:** "done" is the most common lie an agent tells; its costume is verification theater — "tests passed" narrated while command, exit code, and output are absent. A gate that can fail is worth ten reminders that cannot.

**Right-size first.** A low/low job (typo, rename) needs L1 only, no judge. Mid (a module fix with runtime behavior) needs L1 + L2, with `INTENT:`/`TWINS:` owed. High (cross-boundary, infra, security) needs L1 + L2 + L3, a mutation probe, a judge, and full artifact lines. Two traps: the **Average Answer Trap** runs hardest-job controls on every task; the **Kirby Effect** leaves controls encoding a superseded model limitation — cut them on a model upgrade. The dial chooses layers, never lowers the standard.

**A green suite is not the verdict when the work is split.** When correctness depends on several agents, a graph of steps, or a division of labor, a passed end task shows the outcome held once, not that the system is better organized — a stronger model or more compute produce the same curve. Such work is judged on six dimensions: effectiveness, efficiency, robustness, structural fidelity, operational correctness, and evolution and governance — each defined in [evaluation](references/evaluation.md).

**Three layers.** **L1 static** lint, type-check, format on every source change, owed as the `L1:` line (the artifact gates above). **L2 runtime** tests run, critical paths execute, the app starts, when the change runs. **L3 end-to-end** one path crosses a real boundary, when the change crosses one (`n/a` with a one-line reason). Run the cheapest check earliest; a red test beats a narrative pass.

**Grip ladder** — a check is worth what it can *prevent*. 1 in-prompt (advisory, relies on memory); 2 standing condition (persists across turns); 3 deterministic gate (fails the turn; a check that **must always** run); 4 independent verifier (a fresh context re-derives it). Climb only as far as the risk earns; a rule that keeps being forgotten climbs a rung, not louder prose.

**Executable evidence is the anchor.** Every done claim carries the literal command, the explicit exit code, and the captured output, on disk where it survives compaction. The **evidence audit** asks five questions: Is the command literally present? Is the exit code captured? Is the output the runner's own success/diff line, not a summary? Does the claim match the observation word-for-word? Does the asserted behavior equal what the check exercises? Any "no" means unverified.

**Mutation probe.** Introduce a single semantic defect (flip a boolean, shift a bound, drop a guard); run the suite and require it to FAIL; revert and confirm it PASSES. A suite that cannot catch a deliberate defect is theater — the check itself is the defect under review. The probe belongs to high-risk work: on a small, local, reversible change the evidence audit already names the command, its exit code, and its output.

**Judge a finished report.** Judging changes nothing — read and run only. The diff outranks the report; diff test files first (dropped/weakened asserts, loosened tolerances, added skips, swapped mocks); trace every `AUTH:` quote; confirm every owed artifact line (an absent `L1:` line on a source-change report refutes done on the spot); re-run each re-runnable claim (cap 3); resolve conflicts by anchor rank. A claim that cannot be re-run is **UNVERIFIABLE**, never assumed true. The verdict is one of **VERIFIED / VERIFIED WITH CAVEATS / REFUTED**; a refutation names the claim, shows the output, gives the fix.


**Diagnosis.** Reason backward from the observed failure to its root cause before writing the next change; attribute the failure to its layer — reasoning, tool interface, context, or control flow — because the wrong-layer fix is a symptom patch by construction. Contradiction routes backward: a surprise at PROVE re-enters at THINK.

**GROW.** A recurring failure is a **harness problem, not a prompt problem**: durable reliability updates the surrounding system, not the wording. The governed self-evolution cycle — instrument, propose, validate, commit — edits the machinery future runs execute; anchors stay read-only and the evidence standard may tighten only, never loosen. When running that cycle, read [evolution](references/evolution.md) for its cadence and failure modes.

## Verification Loop

Generation alone is **Generate-and-Deliver** — legal only for a trivial ask. A deliverable that is **large, irreversible, outward-facing, cross-session, or hard to re-derive cheaply** ships through **Generate-Verify-Refine-Deliver**: what the model first produces is a draft, never the deliverable. Every other deliverable is verified in place (see Right-size below) — the loop is sized down, never skipped.

**Personas.** The **Generator** and the **Verifier** are separate mental personas. The Verifier's job is to actively seek the reasons the output is wrong or incomplete — adversarial, never confirmatory; a Verifier whose verdict is "looks good" has produced verification theater, not verification. The Verifier re-derives the user's constraints from the pinned `PROMPT:` line and checks the artifact against them point-by-point — each explicit constraint earns its own verdict.

**Verification is a separate role.** The writer judging its own output is role confusion: the context that produced the defect argues against it, and confirmation bias makes that argument cheap. The verifying role gets the artifact, the pinned ask, and fresh context, never the writer's reasoning.
- **Requirement Check** — every constraint carries **Pass / Fail / Partial**; a Fail or Partial returns to generation, and each fix is re-verified before the next pass, bounded by the 3-failed-cycle rule.
- **Logic Audit** — the edge cases and reasoning flaws the generator missed, each named together with its resolution.
- **Final Verdict** — exactly one of **Ready / Needs Revision**.

**Verification Report** (Requirement Check / Logic Audit / Final Verdict) is emitted before the deliverable, never after it.

**Right-size.** The full loop is owed on the triggers named above. A small, local, reversible change is verified in place — re-read the diff against the pinned ask, run the check, name the evidence — and the report says so in one line. The loop is sized down, never forgotten.

## Evals

The doctrine is configuration an agent executes, so it is regression-tested like code. An **eval** is one realistic task plus **objective checks** — executable conditions (a named command and its expected observable) yielding pass/fail without a human reading the transcript; a check a human must judge is not objective. The suite's **pass rate** over time is the only honest answer to whether a change made the agent better or worse.

- **Size to the harness:** 20-50 realistic tasks spanning the behaviors the doctrine governs — intake routing, gate emission, verification discipline, context handling; grow on incident, not ambition.
- **Prefer tasks drawn from real runs:** a task extracted from an actual episode has a proven failure mode; invented tasks test only what you imagined.
- **When it runs:** on a standing schedule; on any change to the manifesto, a skill, a command, a description, the trigger set, a pre-action check, a gate, or the pinned model (the load-bearing trigger); and on incident, each becoming a permanent eval after the fix ships.
- **A regression blocks the merge** until the change is fixed or the eval is deliberately retired with a reason. Never loosen a check so that a change passes — a metric edited by the party it measures. The author of a change never writes the check that judges it.
- **Unattended:** the check gates the stop; the tool surface is pre-scoped; and authority still terminates in a human — a scheduled run ends local and emits `PENDING:`, with the `AUTH:` gate unrelaxed. Autonomy is a degree of attention, never of authority.
- **GROW's proof:** run the suite before and after an evolution. Pair it with the Kirby Effect — run the suite with a control removed on each model upgrade, and cut what it passes without.
- **Separate the system's gain from the model's.** A pass-rate rise after adding agents, tools, retries, or context proves nothing on its own: a stronger model, a longer window, or more compute produces the same curve. Hold the budget fixed (same model, same token and retry ceiling) and ablate a claimed structural change — run the suite with the structure removed and require the delta to disappear. A gain that survives only at a larger budget is a purchase, not an improvement. Its mechanics and evidence are in [evaluation](references/evaluation.md).

**Descriptions are gated by measurement, not by prose.** A skill's `description` is the entire triggering decision — the host loads nothing else before deciding whether the skill applies — so it is the one field where wording is behavior. Two halves are mandatory: a **trigger clause** phrased as an instruction ("Use when …") naming the user intents and phrasings that apply, including asks that never name the domain; and a **boundary** ("Not for …") naming the near-miss another skill owns. Widen until the positives fire; sharpen until the near-misses stay quiet; the `descriptions` gate asserts both.
- **Trigger evals hold a labelled query set with a held-out split.** The trigger query set in the evals directory carries, per skill, at least 8 should-trigger and 6 should-not-trigger prompts written the way a user writes them — file paths, casual phrasing, the need stated without the domain word, buried in a larger ask — with near-misses as negatives, since an irrelevant one tests nothing. Run each 3 times with the trigger runner and score a **trigger rate**: positives pass above threshold, negatives below. Edit from **train** failures only; **validation** is scored, never tuned on.

**Bundled references load on a stated condition.** A `SKILL.md` body loads whole, so a bundled file earns its place only when the link says *when* to open it ("read `references/api-errors.md` if the API returns non-200"); an unconditioned "details: references/x.md" is context the run either pays for every turn or never finds. Keep the condition in the link's paragraph.

## Performance

Optimize only after correctness holds, and only by measurement. Every optimization claim cites **benchmark evidence** — command + output + delta. No measurement, no change; intuition about bottlenecks is wrong ~80% of the time.

**The measure-first cycle: Define, Benchmark, Diagnose, Improve, Compare.** Define one target metric (latency, throughput, memory, CPU) and its target value; benchmark one function at a time and capture the baseline to a numbered file; diagnose by ruling out external bottlenecks first, then route the signal; improve ONE change at a time; compare with a statistical comparator and paste the delta. The artifact is the evidence.

**Rule out external bottlenecks first.** When profiling says the time is not yours to move — a slow query, an upstream span, blocked workers — fix that component and re-profile; local tuning cannot move the number. Read [measurement](references/measurement.md) for its sensors or a per-finding fix.

**Route the signal.** Time goes to one of four places: allocation churn (pool, preallocate known sizes, reduce boxing/reflection), lock contention (bound concurrency, share immutably, atomics over locks), syscall count (buffer, batch, tune transports, cache repeated work), data copying (zero-copy views, stream, pass references). Cheap overrides first: wrong algorithm, repeated expensive work, slow upstream queries.

**Exit.** The cycle ends when the target metric hits its defined value with a recorded before/after delta, or when profiling shows the time is not yours to move — report the stop. Never keep an optimization the evidence does not support. When a benchmark needs hygiene, read [measurement](references/measurement.md) and [tactics](references/tactics.md) for the countermeasures; the same doctrine as decision charts is in [flowcharts](references/flowcharts.md).

## Comments

Default is **no comment**. One earns its place only by stating a non-derivable *why* — a rationale, an invariant, an external constraint, or a trap the code cannot express. Delete named noise on sight: a comment that restates the code or the signature, narrates the change, banners inside a function short enough to read whole, or a doc block longer than the code it documents. The language's own documentation convention sets the form and the code's complexity the length, at that convention's minimum. Pre-emit test: re-read every comment; if a correct refactor would make it wrong, it was noise.

## Simplicity

The default is the **least mechanism that works**: the standard library before a dependency, a plain function before a class, a direct call before a layer. Structure that cannot name what it buys is unintended complexity — a defect: speculative abstraction (extract on the **second real caller**, never the first imagined one), dead configurability (a knob nobody sets), indirection the reader must decode (a wrapper that only forwards), or a dependency for the trivial. Name the cost in review; "this feels complex" is not a finding. **Counterweight:** simplicity never overrides correctness — never collapse a needed error path, drop a boundary check, or flatten a name.

## Reuse (DRY)

One canonical owner per piece of knowledge — a rule, a default, a format, an algorithm — and every other appearance points at that owner instead of restating it. A second copy is not neutral: duplicated logic drifts, and a fix applied to one copy leaves its siblings wrong, the defect the `TWINS:` gate catches. The strongest duplication smell is copy-paste-with-edits: two blocks that look alike but differ in one line. Diff the copies before trusting either.

## Structure (SOLID)

**One reason to change per module.** A unit whose name contains "and" is two units wearing one name — split it at the seam. **Dependencies point inward**: business logic never imports transport, storage, or framework code, so the core survives the swap a dependency upgrade forces. **Interfaces stay narrower than their caller** — a parameter carries what the caller passes, not every value the callee could accept; widen only on a second real caller, never on speculation.

## Typography

This doctrine separates a clause from its qualifier with the em-dash — not the en-dash, and not a spaced hyphen. The same convention governs the doctrine's tables and the prose an agent writes from it; the `dashes` gate holds the corpus to it.
