# Rust adapter

Rust's baseline is two independent numbers, and both matter: the **edition** (`Cargo.toml` `edition`, an opt-in language dialect) and the **MSRV** (`Cargo.toml` `rust-version`, the oldest compiler the crate supports). A crate on edition 2021 with `rust-version = "1.70"` may not use a 2024-edition feature *or* a 1.75 stdlib API.

Implements [modernize-coding](../../SKILL.md) for Rust.

## 1. Detect the baseline

1. **Edition** — `edition = "2021"` (or `"2024"`) in `Cargo.toml`. A *language dialect*, not a version: each edition is opt-in and migrations are mechanical.
2. **MSRV** — `rust-version = "1.70"` in `[package]`. The real ceiling for stdlib and language features. Absent, the crate claims no floor — say so rather than assuming latest.
3. **Running** — `rustc --version`. Verified: cargo **enforces** MSRV, failing the build with `error: rustc 1.98.1 is not supported by the following package: requires rustc 1.99`. An MSRV claim is load-bearing, not decorative.

## 2. Rewrite existing code

Rust has genuine first-class migration tooling — the strongest of any adapter here, because editions were designed to be migrated.

- **Edition migration** (the signature move): `cargo fix --edition` rewrites both `Cargo.toml` and source. Verified: it emits `Migrating Cargo.toml from 2021 edition to 2024` and `Migrating src/main.rs from 2021 edition to 2024`. Run once per edition step; do not skip editions.
- **Idiom migration**: `cargo fix --edition-idioms` applies edition-idiom lints (e.g. `dyn`-prefixing trait objects, removing needless `&`/`ref`).
- **Clippy autofix** — the workhorse for everyday modernization. Verified to rewrite source: `vec![1, 2, 3]` → `[1, 2, 3]`, `if s.len() > 0` → `if !s.is_empty()`, reported as `Fixed src/main.rs (2 fixes)`.
  `cargo clippy --fix --allow-dirty --allow-no-vcs`

**Diff-first is different here.** Verified: `cargo fix` and `cargo clippy --fix` have **no `--dry-run`** (unlike Go's `go fix -diff`). The equivalent discipline is a clean git tree:

```bash
git status --porcelain          # must be empty; cargo fix refuses a dirty tree by default
cargo clippy                    # report-only pass first — read what it wants to change
cargo clippy --fix              # apply
git diff                        # review the actual patch
```

`cargo fix` refuses to run on a dirty tree unless `--allow-dirty` is passed — treat that refusal as a feature, not an obstacle: it is what makes `git diff` a trustworthy review surface afterwards.

## 3. Write current from the start

| Instead of | Write | Needs |
|---|---|---|
| `vec![1, 2, 3]` where the length never changes | array `[1, 2, 3]` | clippy lint |
| `if s.len() > 0` | `if !s.is_empty()` | clippy lint |
| `&String` / `&Vec<T>` parameter | `&str` / `&[T]` | pre-1.0 idiom |
| `.iter().map(..).collect::<Vec<_>>().len()` | `.iter().filter(..).count()` | pre-1.0 idiom |
| `impl Trait` in return position for a fixed type | concrete type or `impl Trait` deliberately | 1.26 |
| `loop { match ... }` over `Option`/`Result` | `?` / `while let` / `if let` | 2018 |
| `extern crate foo;` | `use foo::...;` | 2018 |
| `try!(x)` | `x?` | 2018 |
| `dyn Trait` written as bare `Trait` | `dyn Trait` (required in 2021) | 2021 |
| `.into_iter()` disambiguation surprises | explicit `array::IntoIter` / `.iter()` | 2021 |
| `format!` + push into a `String` in a loop | `write!` into one `String`, or `join` | 1.0 |
| `Box<dyn Error>` in an app with rich errors | `anyhow`/`thiserror`, or `impl Error` | crate choice |

**Editions** (opt-in; migrate in order): 2015 → 2018 (path/`extern crate`/`dyn`) → 2021 (disjoint captures, `IntoIterator` for arrays, panic macro consistency) → **2024** (current stable; stricter `self`/`super` paths, `unsafe extern`, `gen` keyword reservation). Verified: `rustc --edition` accepts `2015|2018|2021|2024|future`, stable is 2024.

## 4. Verify

`cargo fmt --check` → `cargo clippy -- -D warnings` → `cargo build` → `cargo test`, plus `cargo doc --no-deps` when public API moved. Edition jumps touch semantics, so test after each edition step rather than after all of them.

**Termination:** a clean diff with a failing build is not done (§7 of the manifesto).
