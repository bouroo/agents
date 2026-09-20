---
name: design-pattern-selection
description: |
  Pick the right design pattern for an implementation task — or conclude none is
  needed — in any programming language, and deliver the choice with tradeoffs and
  a minimal skeleton. Load this skill when the user asks "which design pattern
  should I use", "is there a pattern for X", "how should I structure this code",
  names a GoF pattern from refactoring.guru (singleton, factory, builder,
  observer, strategy, decorator, adapter, ...), or asks to make code extensible
  (multiple providers/plugins, notifications, undo, middleware, output formats).
  Do NOT use for system- or microservice-level architecture decisions (use
  solution-architecture), for modernizing existing code toward current idioms
  (use modernize-coding), or for general code review.
---

# Design Pattern Selection

Catalog anchor: https://refactoring.guru/design-patterns — 22 GoF patterns
(5 creational, 7 structural, 10 behavioral). This skill is decision-first: most
pattern requests need no pattern, and modern languages collapse several classics
into plain idioms. Full condensed catalog: `references/patterns.md`.

## Inputs to collect

From the user's code or message, pin down before choosing anything:

- The pain: what is hard to change, duplicated, or tangled *right now*? A concrete
  symbol or file is best.
- The variation axis: what changes over time — inputs, algorithms, structure, consumers?
- The language and its existing idioms: interfaces/traits, function values,
  generics, middleware already present in the tree.

If the user names a pattern but no pain, ask what problem they expect it to solve,
or read the code. Implementing a named pattern without a stated pain produces
speculative code the next reader must delete.

## Procedure

1. **Restate the pain as one variation sentence.** "X varies / gets added / is
   duplicated." A pattern solves a variation problem; if you cannot write this
   sentence, there is nothing to solve.
2. **Apply the no-pattern gate first.** If the variation is hypothetical, or the
   plain solution is under ~50 lines with no duplication, answer "no pattern" and
   give the plain code. This is a valid, common verdict. Also check buy-vs-build:
   if a library already owns this variation (e.g. fsspec for storage backends,
   tenacity for retries), the pattern question is largely moot — say so before
   structuring anything.
3. **Match pain → candidates** using the table below. Read the matching entries in
   `references/patterns.md` for intent, use-when, skip-when, and shape.
4. **Shortlist at most 2 candidates.** Compare on: what it buys (citing the pain),
   what it costs (new types, indirection, test surface), and whether a language
   idiom replaces it (see Language reality checks and the language's own
   conventions in the codebase).
5. **Look for the collapse.** Two listed pains often resolve to one mechanism —
   e.g. expressing work as data (a plan of operations) serves both undo and
   reporting. Prefer the single restructure over two patterns; say so when it fires.
6. **Deliver** per the output contract.

### Pain → pattern table

| Pain (what varies / hurts) | Candidates |
| --- | --- |
| Telescoping constructors, many optional params | Builder |
| Families of related products chosen together | Abstract Factory |
| One product; creation point should hide behind an interface | Factory Method |
| Expensive setup; need copies | Prototype |
| One shared resource (config, pool, registry) | Singleton — check stdlib first; usually a module-level object or DI |
| Two interfaces don't fit (usually third-party) | Adapter |
| One type split across two independent dimensions | Bridge |
| Tree structures; uniform treatment of leaf and group | Composite |
| Layer behavior without touching callers | Decorator (often: wrappers / middleware) |
| Subsystem with too many entry points | Facade |
| Huge count of identical small objects | Flyweight (usually: just share references) |
| Lazy / controlled / remote access to an object | Proxy |
| Pipeline of steps that each decide whether to continue | Chain of Responsibility (middleware chain) |
| Operations as queueable, undoable, loggable requests | Command |
| Walk a custom container without exposing internals | Iterator (built-in iterators usually suffice) |
| N×N direct chatter between components | Mediator |
| Snapshot and restore object state | Memento |
| Many consumers of one event stream | Observer (callbacks / event emitter) |
| Behavior changes with an internal phase | State |
| Swap algorithms at runtime | Strategy (often: function values / lambdas) |
| Fixed skeleton, variant steps | Template Method (often: hook functions) |
| New operations over a stable set of types | Visitor (rare; consider plain methods) |

### Language reality checks

Applied at shortlist time; when one fires, prefer the idiom over the classic form:

- First-class functions collapse Strategy, Command-lite, and Template Method
  steps into function values/lambdas in Go, TS/JS, Python, Rust, modern Java/C#.
- Observer with one compile-time-known consumer is a direct call; grow to a
  callback list / event emitter only when a second subscriber appears.
- Factories are constructors selected in one wiring place (`main` / composition
  root); a factory *interface* needs a real second family, not a second product.
- stdlib usually already owns Singleton-type resources: DB pools, HTTP clients,
  loggers. Wrap them in globals only when wiring is genuinely impossible.
- Duck typing (Python, TS) and implicit interfaces (Go) shrink Adapter to a thin
  wrapper struct — the pattern survives, the ceremony does not.
- Value/copy semantics (Go structs, Rust `Clone`, Python `dataclasses.replace`)
  make Memento a plain copy; build machinery only for rich, encapsulated state.

## Output contract

Answer in this order:

1. **Verdict**: pattern name — or "no pattern, plain code".
2. **Why**: one sentence citing the pain, plus what it buys vs costs here.
3. **Skeleton**: minimal code in the user's language — interfaces plus one
   concrete implementation, nothing speculative. When the pattern holds state
   across operations (undo, journal, queue), state where that data lives across
   process exits; if the skeleton is in-memory only, flag that explicitly.
4. **Revisit signal**: the concrete change that should trigger adding or removing
   the pattern.

## Failure handling

- Two candidates tie → take the one with fewer new types, and say the tie out loud.
- User insists on a named pattern with no pain → implement it, but flag the cost
  in one line and name the simplest alternative.

## Examples

Input: "Payment service must support stripe/paypal/adyen and send email/slack/
webhook notifications on status change."

Output: `PaymentProvider` interface + one constructor per provider (Factory Method
intent, no registry); notifications as a list of callbacks or an event emitter
(Observer idiom). Skip Abstract Factory: only one product family. Skip a pub/sub
library: three consumers, one process.
