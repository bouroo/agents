# Pattern Catalog (condensed from refactoring.guru/design-patterns)

Language-agnostic; shape notes name the mechanism, not a language. Each entry:
intent / use when / skip when / shape. Read only the entries the pain→pattern
table shortlisted. "Skip when" outranks "use when": if any skip condition holds,
drop the candidate. Before writing any skeleton, check the codebase's own idioms —
a pattern in its classic form is wrong wherever the language already dissolves it.

## Contents

- [Creational](#creational): [Builder](#builder) · [Abstract Factory](#abstract-factory) · [Factory Method](#factory-method) · [Prototype](#prototype) · [Singleton](#singleton)
- [Structural](#structural): [Adapter](#adapter) · [Bridge](#bridge) · [Composite](#composite) · [Decorator](#decorator) · [Facade](#facade) · [Flyweight](#flyweight) · [Proxy](#proxy)
- [Behavioral](#behavioral): [Chain of Responsibility](#chain-of-responsibility) · [Command](#command) · [Iterator](#iterator) · [Mediator](#mediator) · [Memento](#memento) · [Observer](#observer) · [State](#state) · [Strategy](#strategy) · [Template Method](#template-method) · [Visitor](#visitor)
- [Cross-cutting notes](#cross-cutting-notes)

## Creational

### Builder
Intent: assemble a complex object step by step, away from its constructor.
Use when: constructors take 4+ params with many optional/identical-typed ones, or the
same assembly steps must yield different representations.
Skip when: named/optional args (Python kwargs, TS object literals, C# initializer
syntax) already read like a builder.
Shape: builder type with chainable step methods and one `Build()` that validates.

### Abstract Factory
Intent: create families of related objects without binding to concrete types.
Use when: several products must switch together (e.g. `Dialect{Conn, Migrator, Seeder}`
for each DB vendor), and new families are expected.
Skip when: one product family exists, or products switch independently — Factory
Method or plain interface + constructor is enough.
Shape: one factory interface whose methods return the family's interfaces.

### Factory Method
Intent: let callers get an abstraction without knowing the concrete type or construction.
Use when: creation needs branching logic, defaults, or setup that callers must not repeat.
Skip when: a plain constructor is a one-liner — just expose it.
Shape: factory function/class returning an interface; a registry only for plugin discovery.

### Prototype
Intent: produce new objects by copying a prototype instead of building from scratch.
Use when: construction is expensive (deep default structures) and copies diverge.
Skip when: a literal or constructor is cheap — copying adds aliasing bugs for zero gain.
Shape: explicit `clone()` (deep-copy owned references yourself).

### Singleton
Intent: exactly one instance, globally reachable.
Use when: one shared resource genuinely must exist once (process-wide config, pool).
Skip when: the only motive is lazy init or avoiding parameter passing — inject the
value; globals hide dependencies and break tests. Check the stdlib first: DB pools,
HTTP clients, and loggers already exist as one-instance objects.
Shape: module-level instance or language singleton facility (`OnceLock`, double-checked
lock); prefer DI wiring in `main`/composition root.

## Structural

### Adapter
Intent: make an incompatible interface fit the one your code expects.
Use when: gluing a third-party or legacy API to your domain interface; keeps vendor
types out of your core.
Skip when: you control both sides — change one side instead.
Shape: thin wrapper class/struct holding the foreign client, implementing your interface.

### Bridge
Intent: split one type across two orthogonal dimensions so each evolves independently.
Use when: you would otherwise need an N×M class explosion (Shape×Renderer, Msg×Sender).
Skip when: dimensions are stable — composition via a field/parameter is already the
bridge; a named pattern adds nothing.
Shape: abstraction holds an implementor interface reference; both vary independently.

### Composite
Intent: treat individual objects and compositions uniformly via a tree.
Use when: hierarchical structures (UI widgets, org trees, file trees) where operations
recurse over leaves and groups the same way.
Skip when: the hierarchy is shallow or fixed — a list of children with a loop is fine.
Shape: common component interface implemented by both `Leaf` and `Group{children}`.

### Decorator
Intent: add responsibilities by wrapping, without modifying the wrapped type or callers.
Use when: cross-cutting layers stack at runtime: logging, metrics, retry, auth around
one interface.
Skip when: one layer, known at compile time — edit the function; or the language has
language-level decorators/middleware that already express it.
Shape: wrapper implementing the same interface, delegating and adding behavior.

### Facade
Intent: one simple entry point over a subsystem with many moving parts.
Use when: callers wire 5+ subsystem types themselves; give them one type with few methods.
Skip when: subsystem calls are one-liners anyway — a facade over a facade is indirection.
Shape: class/struct holding the subsystem objects, exposing task-level methods.

### Flyweight
Intent: share state across many fine-grained objects to cut memory.
Use when: thousands/millions of near-identical objects, profiled as a memory problem.
Skip when: unmeasured — interning via a hash map covers typical cases.
Shape: a shared pool of immutable values, referenced by index/pointer.

### Proxy
Intent: control access to the real object — lazy load, cache, check permissions, stand
in for remote.
Use when: access needs a gate that callers should not see, same interface as the real thing.
Skip when: callers can just call the gate themselves.
Shape: wrapper with the same interface holding the real impl (or a connection).

## Behavioral

### Chain of Responsibility
Intent: pass a request through handlers; each may act and stop it or pass it on.
Use when: ordered, optional steps (middleware, validation chains, escalation rules).
Skip when: steps are fixed and unconditional — a plain sequence of function calls.
Shape: handler interface or function list; each decides to continue or stop.

### Command
Intent: turn a request into a value so it can be queued, logged, undone.
Use when: you need undo/redo, deferred execution, an audit trail of operations.
Skip when: calls happen immediately and once — pass a function/lambda and be done.
Shape: command object with `do()`/`undo()` (or fn + args); history list for undo.
Durability: in-memory history dies with the process; journal commands to disk when
undo must survive exit. For remote stores the real undo primitive is soft-delete or
versioning, not in-memory backups — name it instead of faking undo.

### Iterator
Intent: expose sequential access to a container's elements without its internals.
Use when: custom data structure with non-trivial traversal (graph, tree, paged remote API).
Skip when: data is a built-in collection — the language's native iteration already
is this pattern.
Shape: iterator/generator/sequence object with `next()` semantics.

### Mediator
Intent: centralize N-way communication so components stop referencing each other.
Use when: components' direct references form a hairball and changing one forces others.
Skip when: 2-3 components talk directly and clearly — a mediator there is a god object.
Shape: broker object (or event bus) that peers post to; peers know only the broker.

### Memento
Intent: snapshot an object's state for later restore, without exposing internals.
Use when: editor-style undo/rollback of a rich, encapsulated state object.
Skip when: state is plain data — copy it; value semantics make machinery pointless.
Shape: immutable snapshot token + caretaker stack; snapshots stay out of the public API.

### Observer
Intent: one source notifies many consumers about events without knowing them.
Use when: event fan-out (metrics, notifications, cache invalidation) with consumers
added over time.
Skip when: one consumer, known at compile time — call the function directly.
Shape: list of callbacks or event emitter; for cross-process scale, a message broker
replaces this pattern.

### State
Intent: an object changes behavior when its internal phase changes.
Use when: many methods branch on a mode field and transitions have real rules
(order: cart → paid → shipped, each with different valid actions).
Skip when: one or two `if mode == ...` checks — a plain field is clearer.
Shape: state interface with per-state implementations held in a field; transitions
swap the field.

### Strategy
Intent: swap an algorithm behind a stable interface.
Use when: algorithms are selected at runtime (compression, pricing, retry policies) or
injected per test.
Skip when: one algorithm exists — YAGNI; add the seam when the second arrives.
Shape: algorithm interface or function type injected at call site; an interface only
when strategies carry their own config.

### Template Method
Intent: fix the skeleton of an algorithm; let variants override steps.
Use when: several operations share an invariant sequence (run migrations, then seed,
then verify) with variant steps.
Skip when: only one variant exists or the skeleton is 3 lines — write it out.
Shape: skeleton method/function taking hook functions or overridable step methods.

### Visitor
Intent: add operations over a stable set of types without changing those types.
Use when: the type set is fixed and new operations keep arriving (AST passes, compilers).
Skip when: types change often, or one new operation — add a method instead.
Shape: visitor interface with one `visitX()` per type plus `accept(visitor)` on nodes;
or exhaustive pattern matching where the language has it.

## Cross-cutting notes

- Prefer the smallest mechanism: plain code > language idiom (lambdas, mixins,
  channels, pattern matching) > named pattern.
- Patterns are named refactoring targets, not badges: introduce one when the second
  real use appears; delete one when its variation disappears.
- Interfaces belong at the consumer side, small (1-3 methods), and only when a second
  implementation exists or is imminent.
