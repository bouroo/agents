# Go adapter

Go's ceiling is declared in `go.mod` and is unusually explicit: everything here is keyed to the `go` directive (the same gate `go fix` uses). The installed toolchain version means nothing for what language features the module may use — a modern toolchain happily compiles an old module.

Implements [modernize-coding](../../SKILL.md) for Go.

## 1. Detect the baseline

1. Read the `go` directive from `go.mod` (e.g. `go 1.24.0`). It is the authority: fixers and analyzers silently skip rewrites the module is not entitled to.
2. Fallback (no go.mod): `go version`. Never suggest a feature newer than the directive; modernizing *to* a newer version is a separate, deliberate change (one commit).

## 2. Rewrite existing code

Run in `-diff` mode first, review the patch, then apply — mechanically-applied fixes still get human-readable review before landing:

- Go >= 1.26 — built-in `go fix` (fixers gated on the go.mod directive):
  `go fix -diff ./...` → review → `go fix ./...`. Opt out per fixer with `-NAME=false` (e.g. `-newexpr=false`); list fixers with `go tool fix help`.
- Any version — the `modernize` analyzer from `golang.org/x/tools` (standalone, overlapping but not identical fixer set; the authoritative, always-current list is the [package documentation](https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize), and the analyzer inventory reconciles it against the installed tools for the version table below):
  `go run golang.org/x/tools/go/analysis/passes/modernize/cmd/modernize@latest -fix -diff ./...` → review → drop `-diff` to apply.
- Editor/agent session — `gopls` >= 0.20 exposes diagnostics (including modernize) as MCP tools. Run **one server per workspace** from that workspace: `gopls mcp -listen=localhost:0` is official headless mode and keeps the session, file watcher, and root discovery consistent. Reserve `serve -mcp.listen` for an attached LSP process with matching workspace intent. Use diagnostics to catch violations early, symbol tools for renames, and load gopls's own instructions.

Fixes are safe-by-construction (behavior-preserving) but are only as good as their analyzer: keep version bumps, dependency upgrades, and modernization in separate commits so any regression bisects to one cause.

## 3. Write current from the start

Before writing a construct, spend it against the version table (the analyzer inventory reconciles the full inventory against the installed tools and the [package doc](https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize)). Most-targeted rewrites:

| Instead of | Write | Needs |
|---|---|---|
| `interface{}` | `any` | 1.18 |
| `if a < b { x = a } else { x = b }` | `x = min(a, b)` | 1.21 |
| manual `contains` loop | `slices.Contains` / `ContainsFunc` | 1.21 |
| `sort.Slice` | `slices.Sort` | 1.21 |
| `[]byte(fmt.Sprintf(...))` | `fmt.Appendf(nil, ...)` | 1.19 |
| `for i := 0; i < n; i++` | `for i := range n` | 1.22 |
| `x := x` re-declarations in range loops | (delete — loopvar is per-iteration) | 1.22 |
| `w.Wait`-style `wg.Add(1)`/`go`/`wg.Done()` | `wg.Go(func(){...})` | 1.25 |
| `for k, v := range m { dst[k] = v }` | `maps.Copy(dst, src)` | 1.21 |
| `for i := len(s) - 1; i >= 0; i--` | `for _, v := range slices.Backward(s)` | 1.23 |
| `omitempty` on required-when-set fields | `omitzero` | 1.24 |
| `for range strings.Split(s, "\n")` | `strings.SplitSeq` | 1.24 |
| `for i := 0; i < b.N; i++` benchmarks | `for b.Loop()` (not yet auto-fixed) | 1.24 |
| `context.WithCancel` in tests | `t.Context()` | 1.24 |
| `errors.As(err, &x)` where x holds a pointer type | `errors.AsType` returns (ptr, ok) | 1.26 |
| helper returning `&local` | `new(expr)` | 1.26 |

Prefer the standard library before third-party for exactly these cases — the analyzer enforces them, so drifting back is visible in review.

**Termination:** after any application, prove with the standard ladder — `gofmt -l .`, `go vet ./...`, build, tests — at the level the change touches (§7 of the manifesto). A clean diff with a failing build is not done.
