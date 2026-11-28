---
name: swe
description: Use when writing, implementing, reviewing, or refactoring code in any language — craft best practices for clarity, naming, errors, trust boundaries, security, resources, concurrency, tests, idiom currency, and unslopping AI-generated code, text, and UI. Auto-applies to related engineering work; the project's own conventions and linters win on conflict. Craft knowledge, not a workflow stage (plan/verify/review/refactor own those).
---

# Software Engineering Craft

Cross-language principles for code an agent would otherwise get wrong. Formatting belongs to the project's formatter and linters; this skill owns the judgment they cannot. The project's declared ceiling and prevailing idiom win over any rule here — a construct newer than the ceiling is a break, not an improvement.

## 1. Fit the project

- Match the declared ceiling (manifests, engine/target directives, toolchain, CI matrix) and what neighbouring code does; read the project before importing a fresher idiom.
- Keep idioms current within that ceiling: replace deprecated APIs and outdated patterns with their modern equivalents, grounded in the language/framework's official release notes, never memory. Run the ecosystem's fixer in diff first; do renames through language-aware tooling (LSP rename, codemod), not grep/sed sweeps that miss call sites.
- Prefer the stdlib/framework built-in over a new dependency for what the ceiling already provides; a little copying beats a little dependency. Don't abstract before the pattern is stable.

## 2. Clarity over cleverness

- Handle errors and edge cases first with early return; keep the happy path flat; drop `else` after a branch that returns.
- Extract complex conditions into named booleans; prefer a switch over an if-else chain comparing one variable.
- Functions short and focused, one job, ≤4 parameters — beyond that group inputs into an options struct rather than wrapping lines.
- Name length matches scope; no stutter (the package/type context is already present at the call site); one consistent name per concept; booleans read as questions (`is`/`has`/`can`); the zero value means invalid/unset, with an explicit sentinel. No `util`/`helper` grab-bags.
- Follow the language's casing and visibility convention; comments explain why, not what; delete stale comments rather than port them.

## 3. Unslop AI-generated output

Strip the tells of machine-generated code and text; preserve meaning and match the project's voice.

- Code: delete comments that restate the code, boilerplate "for later", wrappers/factories/config with a single caller, and generic names — prefer deletion over addition.
- Words: cut AI vocabulary (additionally, crucial, delve, enhance, foster, landscape, pivotal, showcase, testament, underscore, vibrant) and abstract metaphor nouns (substrate, nexus, scaffolding, paradigm, flywheel); say "use", not "utilize"/"leverage"; name the mechanism or the number, not how it feels.
- Text: no trailing "-ing" filler ("ensuring…"), vague attribution, "not just X but Y", forced triples, generic conclusions, praise/chatbot openers, or decorative emojis; at most one hedge, active voice, one idea per sentence, plain words.
- UI: AI-looking screens (purple gradients, glows, emoji labels, shouty copy, uneven spacing) get a direction drawn from the product, then fixed pass by pass — spacing, color, icons, copy, type, layout.
- A sentence that could appear unchanged in another project's docs is slop; cut it.

## 4. Errors

- Check every returned error; never swallow or discard it.
- Wrap with context at each layer and preserve the cause chain for programmatic inspection (`Is`/`As`-style), not string matching.
- Handle once: an error is logged OR returned, never both — duplicate handling clutters aggregation.
- Expected conditions are returned errors or sentinels; reserve panic/throw for truly unrecoverable bugs, not control flow.
- Translate internal errors into user-safe messages; log technical detail server-side; never leak secrets, stack traces, or PII to users or logs.

## 5. Trust boundaries and security

- Validate all untrusted input where it crosses a trust boundary; internal code trusts that boundary, so defending it protects everything downstream.
- Parameterized queries; pass command arguments separately, never shell-concatenate; escape output for its context (HTML/JS/URL).
- Scope untrusted file paths to an allowed root; never trust client headers for identity or authorization — check permissions server-side on every handler.
- Vetted crypto only, never roll your own: crypto-random for tokens/secrets, constant-time comparison for secrets, authenticated encryption (AEAD), slow memory-hard hashing for passwords.
- Secrets come from env/secret managers, never hardcoded; fail closed on crypto/auth errors.
- Before flagging, trace the data flow: upstream protection adjusts severity, never dismisses a finding; document any downgrade inline so it is reviewable and not re-flagged.

## 6. Resources and resilience

- Acquire, then schedule release immediately (`defer`/`finally`/`using`/context manager); report close/flush errors when durability matters.
- Timeout every external call; limit everything (pool sizes, queue depths, buffers); retry with backoff and a cancellation check between attempts.
- Stream large data; never load an unbounded set into memory.
- Avoid implicit global state and init-time side effects; use explicit constructors and inject dependencies so code is testable.

## 7. Concurrency

- Every concurrent task needs an owner, a stop signal, and a way to wait — no fire-and-forget.
- Prefer ownership transfer (message passing) over shared mutable state; protect shared state with the right primitive; send copies, not shared references.
- Propagate cancellation and wait on the done signal; bound spawning rather than growing unbounded.
- Add concurrency only with measured need; run race detection in CI and detect task/goroutine leaks in tests.

## 8. Tests

- Assert observable behavior and public contracts, not implementation details — coupling to internals turns every refactor into a test rewrite.
- Table-driven with named cases; independent of execution order; parallelize independent tests.
- Mock interfaces at the consumer, not concrete types; keep unit tests fast, isolated, deterministic; separate integration tests behind a tag/marker.
- Cover error and edge paths, not just the happy path; coverage is a gap finder, not a target.

## 9. Leave it green

- Run the project's gates after each change — formatter, linter, type-check, build, tests; a clean diff that fails the build is not done. Performance work only on a measured hot path, after correctness is proven.
- Report pattern → change with the command and output that prove it, and `OWED:` noted-but-unapplied opportunities. Record explicitly declined suggestions so they are not re-raised.