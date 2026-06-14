# AGENTS.md

System-wide instructions for AI coding agents. Language-agnostic, environment-independent, tool-neutral.

## Harness Engineering (behavioral controls)

- Repo is the system of record: state lives in files under `.agents/plans/`, not chat.
- Split instructions, never bloat the entry file: keep this file a router; load topic docs on demand.
- Mind the context budget: every line here persists across auto-compaction, so externalize detail into skill docs and load them on demand — see skills/harness-engineering §8.
- WIP = 1: one active task at a time; finish+verify before starting the next.
- Completion evidence is executable ("test passes", "endpoint returns 200"), never "the code looks fine".
- Three-layer termination before declaring done: L1 static, L2 runtime, L3 end-to-end; no layer skipped.
- Don't declare victory early; don't refactor before core is verified; separate worker from checker.
- Keep context alive across sessions: clock-in (read progress/decisions/last verification) and clock-out (update them) every session.
- Every session leaves a clean state: startup + verification still run; no half-finished work unrecorded.

Detailed norms + clock-in/out checklist: [skills/harness-engineering/SKILL.md](skills/harness-engineering/SKILL.md) — load when designing workflows, checkpoints, or verification rules.

## 1. Spec-First (Spec is Truth)

- Specs precede code, version with it, and drive implementation.
- When code and spec diverge: fix the spec first, then the code. Never patch code without updating the spec.
- No speculative features. If it is not in the spec, do not build it.
- A stale spec is a bug. Treat specs as first-class, reviewable artifacts.
- Store specs, canvases, and progress trackers under `.agents/plans/`.
- Ask user questions if any ambiguity is unclear, and clarify if necessary.

## 2. Three Core Skills (Structured Prompt-Driven Development)

1. **Abstraction-first** — Design objects, collaborations, and boundaries before generating code. Clarity of intent precedes implementation.
2. **Alignment** — Lock scope explicitly: what we will do, what we will not, what remains open. Make it visible in the spec.
3. **Iterative review** — Treat output as a controlled loop, not a one-shot draft: spec → generate → verify → refine → repeat.

## 3. REASONS Canvas

For any non-trivial task, structure thinking across these seven dimensions:

- **R**equirements — problem statement, definition of done, acceptance criteria.
- **E**ntities — domain objects and their relationships.
- **A**pproach — strategy to meet requirements; alternatives considered and rejected.
- **S**tructure — where the change fits; components, dependencies, interfaces.
- **O**perations — concrete, testable implementation steps in order.
- **N**orms — cross-cutting engineering standards (naming, patterns, defensive coding).
- **S**afeguards — non-negotiable constraints (invariants, performance limits, security rules).

Leave no section empty. Mark unknowns explicitly; do not gloss them over.

## 4. Workflow Rules

- **Design before generate** — clarify objects, boundaries, and collaborations first.
- **Lock intent** — state scope, non-goals, and open questions up front.
- **Sync, don't hand off** — spec and code evolve together; reflect changes both ways.
- **Verify core before optimize** — make it work, then make it right, then make it fast.
- **Iterative review** — for logic corrections, update the spec first, then regenerate code; for refactors, change code first, then sync the spec.
- **Use tools effectively** — read before editing, search before assuming, validate after writing, lint and typecheck after changes.
- **Executable completion** — "done" means behavior verified by a passing check, not code that looks right; require a failing test/repro before fixing a bug.

## 5. Cross-Cutting Norms (Engineering Commandments)

Apply these across any language or runtime.

**Structure**
- Write libraries, not monoliths. Keep entry points minimal; place domain logic in modules with clean public APIs.
- Return data, not side effects. Return errors, do not crash.
- Decouple from environment — config flows inward; domain logic has no knowledge of env vars, paths, or CLI args.

**Safety**
- Make invalid states unrepresentable. Validate at boundaries. Prefer constants over magic values.
- Design for errors — check every error; retry transient failures; propagate the rest. Never silently ignore.
- Wrap errors with context and preserve the cause chain. Define sentinel errors; never inspect error strings.
- Be safe by default — least privilege, sensible defaults, validating constructors.

**State & Concurrency**
- Avoid mutable global state. Use explicit dependency injection over global defaults.
- Use concurrency sparingly. Keep it localized. Ensure every spawned task terminates before its enclosing scope exits.
- Share immutable data; synchronize only when mutation is unavoidable.

**Observability**
- Log only actionable information. Structured fields, never secrets. Use tracing for request debugging, metrics for performance.

**Reading & Testing**
- Write code for reading — consistent naming, short functions, named helpers, intent documented at the component level.
- Test as you write. Test names read as sentences. Cover happy, error, and edge paths. Tests are living documentation.

## 6. Performance Patterns (Quick Reference)

Optimize deliberately, after correctness is proven.

- **Memory** — preallocate collections when size is known; pool reusable objects in hot paths; align data structures by size to avoid padding; avoid boxing of value types; prefer zero-copy (slices, views, references) over duplication; keep short-lived values on the stack.
- **GC pressure** — minimize heap allocations, reuse buffers, prefer value types in hot paths.
- **Concurrency** — bound work with worker pools; prefer atomics over locks for simple counters and flags; lazy-initialize expensive resources; share immutable data; propagate cancellation and deadlines across all spawned work.
- **I/O** — buffer streams with workload-tuned sizes; batch small operations to amortize per-request overhead.
- **Build** — enable release optimization flags (inlining, escape analysis, dead-code elimination); apply profile-guided optimization where available; measure before and after.

## 7. Agent Interaction Protocol

- **Load skills first** — before delegating or executing, load the relevant skill (harness-engineering, spec-driven-development, effective-code-craft, performance-patterns) so its guidance is in context.
- **Use the task tool for subagents** — delegate independent, well-scoped subtasks; do not over-fanout for trivial work.
- **Filesystem handoffs** — exchange specs, plan trackers, and intermediate artifacts between agents via files under `.agents/plans/`, not via prompt injection.
- **Synthesize** — after subagents complete, reconcile their outputs against the spec, resolve conflicts, and re-verify against the REASONS canvas before declaring done.
- **Worktree isolation** — when working in parallel on independent concerns, use a separate worktree per concern to avoid contention.
- **Separate worker from checker** — the agent that produces work must not be the sole judge of it; route verification to an independent reviewer/tester pass.
