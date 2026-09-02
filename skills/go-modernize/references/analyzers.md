# Analyzer / fixer inventory

Rewrites performed by the two fixer tools. They overlap but are not identical — check the live set with `go tool fix help` (built-in, Go ≥ 1.26) or the modernize binary's usage (`-flags` prints JSON) — the set below is evidence from go1.26.7 and `modernize@latest` (2026-08). "Runs": both / fix only / standalone only.

| Runs | Analyzer | Rewrite | Feature since |
|---|---|---|---|
| both | `any` | `interface{}` → `any` | 1.18 |
| standalone | `unsafefuncs` | `unsafe.Pointer(uintptr(p)+uintptr(n))` → `unsafe.Add(p, n)` | 1.17 |
| both | `stringscut` | `strings.Index` + slicing → `strings.Cut` | 1.18 |
| both | `stringscutprefix` | `HasPrefix`/`TrimPrefix` pairs → `strings.CutPrefix`/`CutSuffix` | 1.20 |
| fix | `fmtappendf` | `[]byte(fmt.Sprintf(...))` → `fmt.Appendf(nil, ...)` | 1.20 |
| both | `minmax` | if/else min/max → `min(a, b)` / `max(a, b)` | 1.21 |
| both | `slicescontains` | membership loops → `slices.Contains`/`ContainsFunc` | 1.21 |
| standalone | `slicesclip` | `x[:len(x):len(x)]` → `slices.Clip(x)`; `append([]T(nil), s...)` → `slices.Clone(s)` | 1.21 |
| both | `slicessort` | `sort.Slice` with basic-type less → `slices.Sort` | 1.21 |
| standalone | `atomictypes` | `atomic.AddInt32(&x, 1)` → `atomic.Int32` methods | 1.19 |
| both | `forvar` | remove `x := x` loop-variable copies | 1.22 |
| both | `rangeint` | `for i := 0; i < n; i++` → `for i := range n` | 1.22 |
| both | `reflecttypefor` | `reflect.TypeOf(x)` → `reflect.TypeFor[T]()` | 1.22 |
| both | `mapsloop` | copy/insert loops → `maps.Copy`/`Insert`/`Clone`/`Collect` | 1.23 |
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
| both | `plusbuild` | strip obsolete `// +build` lines (keep `//go:build`) | 1.18 |
| fix | `buildtag` | validate `//go:build` / `// +build` consistency (vet-style check) | — |
| fix | `hostport` | validate address format passed to `net.Dial` (vet-style check) | — |
| fix | `inline` | apply `go:fix inline` directive-based inlining | — |

Notes:

- x.tools documentation also lists `appendclipped`, `bloop` (→ `for b.Loop()`), and `slicesdelete`; neither go1.26.7's `go fix` nor current `modernize@latest` ships them — treat the table above as the live set and re-check on toolchain upgrade.
- Selection is per-analyzer in both tools (`-NAME`, `-NAME=false`/omit to disable); `-diff` with `-fix` prints a unified patch and exits non-zero when non-empty.
- Test files are analyzed by default (singlechecker `-test` defaults true).