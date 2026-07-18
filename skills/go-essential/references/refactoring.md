# Refactoring - Depth

Loaded on demand from [go-essential](../SKILL.md) §11. The headline rules live there; this file
expands the workflow, tooling, safety net, and structural patterns.

> **Stance:** you never change structure and behavior in the same step. You keep a green test
> net, prefer behavior-preserving tools over hand-edits, and land changes as small, reviewable
> PRs. Version control is the safety net underneath the test safety net.

## Persona and Modes

You are a Go refactoring engineer. Refactoring (Fowler) is changing internal structure to make
code easier to understand or cheaper to modify, **without changing observable behavior**.

- **Plan mode** (mandatory gate before any edit) - use `gopls` to map structure and blast radius,
  build a refactoring inventory, decide ordering, get explicit user sign-off before touching
  code.
- **Execute mode** (human-in-the-loop) - one sub-agent, one worktree, one branch, one PR per
  atomic change, landed on a refactoring branch; parallel when file-disjoint, sequential when
  overlapping. Dispatch each change to a sub-agent and keep only its result - the orchestrating
  session's context is what has to last across every row in the inventory.
- **Simple-sweep mode** - a single mechanical, behavior-preserving transform applied tree-wide
  (e.g. one `gofmt -r` rule). The only case where an automated agent-to-agent sweep is
  appropriate; verify green afterwards.
- **Review mode** - verify structural/behavioral separation and behavior preservation before
  approving a refactoring PR.

**Do not use Workflows/`ultracode`** for a multi-step refactor needing progressive human review
between merges - Workflows run agent-to-agent with no human checkpoint between stages, which is
exactly what a staged refactor requires between every merge.

## The Core Loop

**Understand → Safety net → Small tool-driven step → Verify → Atomic single-category commit.**
Repeat.

1. **Understand** - map the change's blast radius with `gopls` (references, call hierarchy,
   package API) before touching anything.
2. **Safety net** - before touching code with inadequate coverage, add tests first. Gate the
   strategy on the *blast radius's* coverage, not global coverage. Treat writing that test as
   your own mechanism for checking the change - a green suite you wrote yourself is what lets
   you tell "this is behavior-preserving" from "I hope this is behavior-preserving."
3. **Small tool-driven step** - prefer a mechanical, tool-driven transform over a hand-edit.
4. **Verify** - `go build ./... && go vet ./... && go test ./...`; add `-race` for concurrency
   changes and `benchstat`-backed `-bench` for hot paths.
5. **Atomic single-category commit** - purely structural or purely behavioral, never both.

## Hard Rules (Expanded)

### Never mix structural and behavioral changes

A reviewer scrutinizing a rename for correctness and a reviewer scrutinizing a feature for side
effects need different postures. Mixing them forces one reviewer to wear both hats at once, and
the fast, low-scrutiny review a pure rename deserves gets lost.

### Split a code move from a code optimization into two sequential PRs

Both are structural, but they need different verification: the move is proven safe by `gopls`
plus build/test, the optimization needs benchmarks and a closer correctness read. They touch the
same code, so run them sequentially rather than in parallel worktrees - parallelizing just moves
the conflict to merge time.

Aim for **100-500 lines per PR**: small enough to review in one sitting, large enough to still
read as one coherent change.

### Prefer `gopls` Rename/Inline over LLM hand-edits

Both are behavior-preserving by construction:

- **Rename** refuses on shadowing, interface-satisfaction breakage, or malformed code rather
  than silently producing a bad diff.
- **Inline** substitutes side-effect-bearing arguments into `var` temporaries rather than
  duplicating them.

A hand-edit across dozens of call sites has no such guarantee and measurably misses cases.

### Generate a rewrite tool when a change recurs across many sites

Escalate in order of increasing power:

| Tool             | Power                                         | Use for                                                   |
| ---------------- | --------------------------------------------- | --------------------------------------------------------- |
| `gofmt -r`       | Pattern → replacement on AST nodes            | Simple syntactic sweeps (e.g. `context.Background()` → `ctx`) |
| `eg`             | Write a Go rewrite rule with full Go syntax   | Tree-wide refactor with logic                             |
| `gopatch`        | Structured, repo-wide, reviewable patches     | Comprehensive mechanical edits with verification          |
| `go/analysis` fixer / `//go:fix inline` | Custom analyzer with auto-fix    | Library-level migration recipes                           |
| `dave/dst`       | AST manipulation preserving comments/formatting | When comment survival matters                           |

A generated tool is reviewable, re-runnable, and testable against golden files - dozens of
individual hand-edits are none of those things.

### Use a type alias for every type moved across packages

```go
// In the old package, after the type has been copied to its new home:
package old
import "example.com/project/newpkg"
type User = newpkg.User   // type alias - old and new names are interchangeable
```

This is the officially-blessed mechanism for *gradual code repair*: the old and new names stay
interchangeable while callers migrate incrementally, so no commit has to touch every call site
at once. Remove the alias only after a full release cycle of no internal references to the old
path.

### Break import cycles with a consumer-side interface first

Go resolves interfaces implicitly, so the producer package never has to import the consumer's
interface. This is the cheapest, most surgical fix for a cycle - try it before a package split
or extracting a shared leaf package.

```go
// package consumer (was importing producer, creating a cycle)
type Producer interface { Do(context.Context) error }

type Service struct{ p Producer }
```

### Grep for tag and reflection references after any rename

`gopls` Rename only guards against *compilation* breakage. It cannot see:

- **Struct tags** that still reference the old field name (`json:"oldName"`)
- **`text/template` / `html/template`** field references
- **`reflect`-driven dispatch** (ORM field mappings, DI containers, codec internals)
- **String-based lookups** in config, SQL column mappings, etc.

After any rename, grep across the repo for the old name in strings, tags, and template files.

### Pause for human sign-off before

- Any cross-package move or package split
- Any exported-API change or deprecation
- Any deletion
- Introducing a new major version
- Touching code with no tests

These are the moves where a wrong call is expensive to undo.

### Load the security skill whenever a step changes logic

A mechanical, tool-verified transform can't introduce a vulnerability, but a behavioral change
can. Treat "changes what the code does" as the trigger for a security-and-safety pass, not an
afterthought reserved for the final review. See [Safety](./safety.md) for the security and safety
checklists.

### Revert rather than debug forward

Start every step from a clean, committed baseline. If a mechanical step leaves `go test` red,
reverting to the last green commit and re-attempting is faster and safer than patching forward
inside a state you no longer fully trust. Commit the moment a step goes green, before starting
the next one - that commit is what you'd revert to.

## Risk Stratification

| Risk       | Transforms                                                                                                                              | Safety requirement                                       |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| **Low**    | `gopls` Rename, Extract Variable/Constant, Inline Variable, `gofmt -s`, organize imports, local `refactor.rewrite.*` actions            | Build/vet/test after the step is enough                  |
| **Medium** | Extract Function/Method (Extract is best-effort - verify comments/behavior survived), Inline Call across packages, single-parameter add/remove, introducing generics | Add or confirm targeted tests over the blast radius first |
| **High**   | Change signature across many callers, moving types/functions across packages, splitting/merging packages, breaking import cycles, exported-API or major-version changes | Full safety net + human checkpoint before landing        |

## Safety Net - Coverage-Adaptive Strategy

Gate the strategy on the *blast radius's* test coverage, not the repo's global coverage.

| Coverage of blast radius | Strategy                                                                                             |
| ------------------------ | ---------------------------------------------------------------------------------------------------- |
| **High** (≥80%)          | Proceed; existing tests are the safety net. Run `go test ./...` and `-race` after each step.          |
| **Medium** (40-80%)      | Add targeted tests for the untested paths in the blast radius before the refactor.                    |
| **Low** (<40%)           | Write **characterization tests** (golden/output capture) that pin current behavior before refactoring. |

**Characterization test libraries:**

- `github.com/sebdah/goldie` / `github.com/bradleyjkemp/cupaloy` - golden-file testing for
  snapshot-based behavior pinning.
- `go-cmp` (`github.com/google/go-cmp/cmp`) - deep equality with readable diffs, ideal for
  asserting "output unchanged before/after."

**Verification command reference:**

```bash
go build ./...                              # compile after every step
go vet ./...                                # static checks
go test ./...                               # behavior preservation
go test -race ./...                         # concurrency behavior unchanged
go test -bench=. -benchmem -count=6 ./... | tee new.txt
benchstat old.txt new.txt                   # hot path unchanged (expect `~`)
go test -cover -coverpkg=./... ./...        # scoped coverage of blast radius
go tool cover -func=coverage.out             # per-function coverage
```

## Structural Patterns

### Package-boundary design

- **`internal/`** is enforced by the toolchain - packages here cannot be imported outside the
  module. Use it for everything proprietary.
- **`pkg/`** only for genuinely exportable code; don't create it speculatively.
- **Packages are lowercase, singular, match the directory name.**

When a package grows too large, prefer extracting a sub-package whose name describes the
abstraction (not `util`, `helpers`, `common`).

### Breaking import cycles

In priority order:

1. **Consumer-side interface** (cheapest) - define the interface where consumed; producer never
   imports it.
2. **Extract shared code to a leaf package** that both cycle members import.
3. **Package split** - the most invasive; reserve for when 1 and 2 don't resolve the cycle.

### Exported-API and versioning moves

For library code:

- Deprecate the old name with a doc comment (`// Deprecated: use NewName.`) and keep it working
  for a full release cycle.
- Use a **type alias** (`type Old = New`) so callers' code keeps compiling while they migrate.
- Remove the deprecated symbol only at a major version bump.

## Workflow: Plan → Stage → Land

A refactor of any real size does not land as one commit or even one PR - it lands as an ordered
sequence of small, independently reviewable PRs, staged on a refactoring branch, with a human
approving each merge.

### Planning gate (mandatory before edits)

1. Use `gopls` to map blast radius: references, incoming/outgoing calls, package API surface.
2. Build a **refactoring inventory** - one row per atomic change, with: target file(s), tool
   (gopls/gofmt/eg/gopatch), risk level, dependencies on other rows.
3. Decide ordering against three interacting constraints:
   - **Structural before behavioral** - never land a behavior change on top of an in-flight
     structural one.
   - **Conflict avoidance** - file-disjoint changes can run in parallel; overlapping changes
     run sequentially.
   - **Dependency order** - if row B depends on row A's new structure, A merges first.
4. Get explicit user sign-off on the plan before any edit.

### Git model

- One `refactor/<topic>` branch for the whole effort.
- One worktree, one branch, one PR per atomic change. Each PR is reviewable independently.
- Stack PRs when they depend on each other; keep the stack shallow (≤3) or reviewers lose
  context.

### The `// REFACTOR(step N): ...` marker convention

When mid-refactor and a step is too large to land in one PR but too coupled to split, drop a
TODO marker at the seam:

```go
// REFACTOR(step 2): move this interface to the consumer package once
// call sites migrate. Tracked in #1234.
```

This makes unfinished work greppable and survives across PRs.

### Parallel vs. sequential

- **Parallel** (separate worktrees, separate PRs): file-disjoint changes, no shared dependency.
- **Sequential** (stacked PRs): overlapping files, or row B depends on row A's new structure.
- **Never parallelize overlapping changes** - it just moves the conflict from edit time to merge
  time.

## When NOT to Refactor

Refactoring is an investment that only pays off if a future change is coming to spend it on.
Question it when:

- **The code works and nothing planned will touch it again.** A stable, rarely-read package
  earns nothing from being restructured for its own sake.
- **It's critical production code with no tests.** The human checkpoint requires a
  characterization-test baseline and explicit sign-off - for a genuinely critical path, treat
  that gate as non-negotiable.
- **The deadline is tight.** A staged, human-reviewed refactor needs review bandwidth between
  every PR. Under time pressure it either stalls or gets rushed.
- **There's no clear purpose.** "Refactor this" with no reason behind it is refactoring for its
  own sake. Confirm the purpose during the planning gate's sign-off.

## Diagnose

1. `gopls` refusing a Rename or Inline is a real semantic hazard, not a tool bug - investigate
   the shadowing/interface conflict before forcing the change by hand.
2. `go vet ./...` / `golangci-lint run` flagging a new issue after a step - fix before
   committing, don't accumulate lint debt mid-refactor.
3. `go test -race ./...` reporting any race - stop, the concurrency behavior changed.
4. `benchstat old.txt new.txt` reporting anything other than `~` on a hot path - stop and revert
   or optimize. A "refactor" that regresses performance is a behavior change.
5. `go tool cover -func` on the touched packages, scoped with `-coverpkg=./...` - this is the
   strategy gate for how aggressively you can proceed.

## Common Mistakes

| Mistake                                                            | Fix                                                                                  |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| Mixing structural and behavioral changes in one commit            | Split into two PRs; the rename/extract lands first, the behavior change second       |
| Hand-editing across dozens of call sites                          | Use `gopls` Rename/Inline; escalate to `eg`/`gopatch` for mechanical sweeps          |
| Renaming a field without checking struct tags                     | Grep for the old name in tags, templates, `reflect`, and string-based lookups        |
| `gopls` Rename refused, hand-edit forced through                  | Investigate the shadowing/interface conflict - `gopls` is flagging a real hazard     |
| Moving a type to a new package in one commit                      | Use a type alias so callers migrate incrementally                                    |
| Debugging forward from a red state mid-refactor                   | Revert to last green commit; re-attempt the mechanical step                         |
| Refactoring critical code with no tests                           | Write characterization tests first; get human sign-off at the planning gate          |
| Landing a 2000-line refactor as one PR                            | Split into 100-500-line atomic single-category PRs                                  |
| Running overlapping refactors in parallel worktrees               | Sequential stacked PRs - parallelizing just moves the conflict to merge time         |
| Skipping the planning gate                                         | Mandatory: map blast radius, build inventory, get sign-off before any edit          |
| Treating a benchmark regression as a "perf issue, file a ticket"  | A regression during a refactor is a behavior change - revert or fix before landing   |
| Using Workflows/`ultracode` for a multi-step refactor             | Reserve for single-pass mechanical sweeps; multi-step needs human review between merges |

## Audit Sub-Agents (Parallel)

When auditing a refactor plan or in-flight refactor across a codebase, split into 4 parallel
sub-agents:

1. **Structural/behavioral separation** - every commit and PR is purely one category.
2. **Tool usage** - `gopls`/`gofmt -r`/`eg`/`gopatch` preferred over hand-edits; generated
   tools for recurring patterns.
3. **Safety net** - coverage of blast radius checked; characterization tests in place for
   untested code; benchmarks for hot paths.
4. **Structural integrity** - import cycles broken via consumer-side interfaces; type aliases
   for cross-package moves; exported-API deprecation lifecycle respected.

## Cross-References

- Depth on what to rename identifiers *to*: see [Naming](./naming.md) - this file owns *how*
  to apply a rename safely at scale.
- Target directory/package layout: see [Project and Design](./project-and-design.md) - this
  file owns the mechanics of moving code there without breaking callers.
- Control-flow clarity and function shape: see [Code Style](./code-style.md).
- Target patterns (functional options, DI, consumer-side interfaces): see
  [Design Patterns](./design-patterns.md).
- Test-writing practices that make the safety net trustworthy: see [Testing](./testing.md).
- Benchmarking methodology for hot-path verification: see [Performance](./performance.md).
- Security and safety review for any step that changes logic: see [Safety](./safety.md).
- Language-agnostic harness-engineering norms (WIP=1, three-layer termination, handoff
  artifacts) that underpin this workflow: [harness-engineering](../../harness-engineering/SKILL.md).

## Sources

Builds on Martin Fowler's *Refactoring* (2nd ed.), the Go team's
[`gopls`](https://pkg.go.dev/golang.org/x/tools/gopls) code-action API, and the
[`go/analysis`](https://pkg.go.dev/golang.org/x/tools/go/analysis) framework.
