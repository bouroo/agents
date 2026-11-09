# Analyzer / fixer inventory

**Derive this from the live sources — never trust the snapshot below.** The canonical list of modernize analyzers, each with the feature it requires, is the package documentation:

    https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize

The *running* set is whatever the installed tool reports, and it outranks both this file and that page. Run:

    go tool fix help        # Go >= 1.26 built-in fixers
    modernize -flags        # x/tools modernize binary (prints JSON)

**Refresh — on any toolchain bump, and whenever a rewrite is reported as unknown:**

1. Read the package doc for the analyzer set and each analyzer's required Go feature.
2. Dump the installed set (`go tool fix help`, `modernize -flags`) and reconcile. In the doc but not the tool: upstream-only. In the tool but not the doc: newer than the page.
3. Correct the version column against the release that actually added the feature: `$(go env GOROOT)/api/go1.N.txt` records exactly which release added each stdlib symbol — read it rather than recalling.
4. Run `python3 scripts/check.py modernize`; it pins the version column below and cross-checks `GOROOT/api` whenever a toolchain is present.

The table is a reconciliation, not a source of truth; the snapshot below records a reconciliation against go1.26.8 and a 2026-09 modernize build. "Runs": both / fix only (built-in `go fix` only) / standalone only (`modernize` only).

| Runs | Analyzer | Rewrite | Feature since |
|---|---|---|---|
| both | `any` | `interface{}` → `any` | 1.18 |
| standalone | `unsafefuncs` | `unsafe.Pointer(uintptr(p)+uintptr(n))` → `unsafe.Add(p, n)` | 1.17 |
| both | `stringscut` | `strings.Index` + slicing → `strings.Cut` | 1.18 |
| both | `stringscutprefix` | `HasPrefix`/`TrimPrefix` pairs → `strings.CutPrefix`/`CutSuffix` | 1.20 |
| fix | `fmtappendf` | `[]byte(fmt.Sprintf(...))` → `fmt.Appendf(nil, ...)` | 1.19 |
| both | `minmax` | if/else min/max → `min(a, b)` / `max(a, b)` | 1.21 |
| both | `slicescontains` | membership loops → `slices.Contains`/`ContainsFunc` | 1.21 |
| standalone | `slicesclip` | `x[:len(x):len(x)]` → `slices.Clip(x)`; `append([]T(nil), s...)` → `slices.Clone(s)` | 1.21 |
| both | `slicessort` | `sort.Slice` with basic-type less → `slices.Sort` | 1.21 |
| standalone | `atomictypes` | `atomic.AddInt32(&x, 1)` → `atomic.Int32` methods | 1.19 |
| both | `forvar` | remove `x := x` loop-variable copies | 1.22 |
| both | `rangeint` | `for i := 0; i < n; i++` → `for i := range n` | 1.22 |
| both | `reflecttypefor` | `reflect.TypeOf(x)` → `reflect.TypeFor[T]()` | 1.22 |
| both | `mapsloop` | copy/insert loops → `maps.Copy`/`Clone` (1.21) or `Insert`/`Collect` (1.23) | 1.21 |
| standalone | `slicesbackward` | reverse-index loops → `for _, v := range slices.Backward(s)` | 1.23 |
| both | `omitzero` | `omitempty` → `omitzero` on struct fields | 1.24 |
| both | `stringsseq` | `for range strings.Split(...)` → `strings.SplitSeq(...)` (also `Fields`) | 1.24 |
| both | `testingcontext` | `context.WithCancel` in tests → `t.Context()` | 1.24 |
| both | `waitgroup` (`waitgroupgo` in modernize) | `wg.Add(1)`/`go`/`defer wg.Done()` → `wg.Go(func(){...})` | 1.25 |
| standalone | `reflecttypeassert` | `v.Interface().(T)` → type-parameterized `reflect.TypeAssert` | 1.25 |
| standalone | `errorsastype` | `errors.As(err, &x)` → type-parameterized `errors.AsType` (ptr, ok) | 1.26 |
| both | `newexpr` | helper returning `&local` → `new(expr)` | 1.26 |
| both | `stditerators` | `Len()`/`At(i)` loops → `for v := range x.All()` iterators | 1.23 |
| both | `stringsbuilder` | repeated `s += ...` in loops → `strings.Builder` | 1.10 |
| standalone | `embedlit` | nested struct literals `U: U{x: 1}` → `U{x: 1}` | 1.27 |
| standalone | `importcomment` | delete obsolete canonical-import comments | — |
| both | `plusbuild` | strip obsolete `// +build` lines (keep `//go:build`) | 1.17 |
| fix | `buildtag` | validate `//go:build` / `// +build` consistency (vet-style check) | — |
| fix | `hostport` | validate address format passed to `net.Dial` (vet-style check) | — |
| fix | `inline` | apply `go:fix inline` directive-based inlining | — |

Notes:

- The package doc also lists `appendclipped`, `bloop` (→ `for b.Loop()`), and `slicesdelete`. None appears as a selectable flag in the snapshot's tools (go1.26.8 / 2026-09): documented upstream, not yet shipped. Re-check on toolchain upgrade rather than assuming.
- Selection is per-analyzer in both tools (`-NAME`, `-NAME=false`/omit to disable); `-diff` with `-fix` prints a unified patch and exits non-zero when non-empty (built-in `go fix`) or zero (modernize).
- Test files are analyzed by default (singlechecker `-test` defaults true).
