---
name: go-modernize
description: "Modernize Go code per the target Go version: detect the version from go.mod's go directive (fallback: installed toolchain), run go fix / the modernize analyzer to auto-rewrite legacy idioms, and write modern Go from the start. Use when modernizing, reviewing, or writing Go."
---

# Go Modernize

Modern Go is not a style opinion — it is a function of the module's declared version. Everything here is keyed to the `go` directive in `go.mod` (the same gate `go fix` uses); the installed toolchain version means nothing for what language features the module may use.

**When to load:** writing Go, modernizing a module, or migrating old idioms after a version bump. Do not load for correctness or performance work — that is [craft](../craft/SKILL.md) / [performance](../performance/SKILL.md).

## 1. Detect the target version

1. Read the `go` directive from `go.mod` (e.g. `go 1.24.0`). It is the authority: fixers and analyzers silently skip rewrites the module is not entitled to.
2. Fallback (no go.mod): `go version`. Never suggest a feature newer than the directive; if modernizing *to* a newer version, the version bump is a separate, deliberate change (one commit).

## 2. Rewrite existing code

Run in `-diff` mode first, review the patch, then apply — mechanically-applied fixes still get human-readable review before landing:

- Go ≥ 1.26 — built-in `go fix` (fixers gated on the go.mod directive):
  `go fix -diff ./...` → review → `go fix ./...`. Opt out per fixer with `-NAME=false` (e.g. `-newexpr=false`); list fixers with `go tool fix help`.
- Any version — `modernize` analyzer from `golang.org/x/tools` (standalone, overlapping but not identical fixer set — see [analyzers](references/analyzers.md)):
  `go run golang.org/x/tools/go/analysis/passes/modernize/cmd/modernize@latest -fix -diff ./...` → review → drop `-diff` to apply.
- Editor/agent session — `gopls` ≥ 0.20 exposes diagnostics (including modernize) as MCP tools. Run **one shared instance**, not one per host (each `gopls mcp` spawn is a fresh process with cold caches and duplicate memory): `gopls serve -mcp.listen=<addr>` under a login-time supervisor. Ports are detected, never hardcoded — probe for a live instance first, else bind a free high port and publish it for hosts to resolve at connect time (pattern, port discipline, and per-host snippets in [gopls-mcp](references/gopls-mcp.md)). Use its diagnostics to catch violations early, its symbol tools for renames.

Fixes are safe-by-construction (behavior-preserving) but are only as good as their analyzer: keep version bumps, dependency upgrades, and modernization in separate commits so any regression bisects to one cause.

## 3. Write modern from the start

Before writing a construct, spend it against the version table ([analyzers](references/analyzers.md) holds the full inventory). Most-targeted rewrites:

| Instead of | Write | Needs |
|---|---|---|
| `interface{}` | `any` | 1.18 |
| `if a < b { x = a } else { x = b }` | `x = min(a, b)` | 1.21 |
| manual `contains` loop | `slices.Contains` / `ContainsFunc` | 1.21 |
| `sort.Slice` | `slices.Sort` | 1.21 |
| `[]byte(fmt.Sprintf(...))` | `fmt.Appendf(nil, ...)` | 1.20 |
| `for i := 0; i < n; i++` | `for i := range n` | 1.22 |
| `x := x` re-declarations in range loops | (delete — loopvar is per-iteration) | 1.22 |
| `w.Wait`-style `wg.Add(1)`/`go`/`wg.Done()` | `wg.Go(func(){...})` | 1.25 |
| `for k, v := range m { dst[k] = v }` | `maps.Copy(dst, src)` | 1.23 |
| `for i := len(s) - 1; i >= 0; i--` | `for _, v := range slices.Backward(s)` | 1.23 |
| `omitempty` on required-when-set fields | `omitzero` | 1.24 |
| `for range strings.Split(s, "\n")` | `strings.SplitSeq` | 1.24 |
| `for i := 0; i < b.N; i++` benchmarks | `for b.Loop()` (not yet auto-fixed) | 1.24 |
| `context.WithCancel` in tests | `t.Context()` | 1.24 |
| `errors.As(err, &x)` where x holds a pointer type | `errors.AsType` returns (ptr, ok) | 1.26 |
| helper returning `&local` | `new(expr)` | 1.26 |

Prefer stdlib before third-party for exactly these cases — the analyzer enforces them, so drifting back is visible in review.

**Termination:** after any application, prove with the standard ladder — `gofmt -l .`, `go vet ./...`, build, tests — at the level the change touches (§7 of the manifesto). A clean diff with a failing build is not done.
