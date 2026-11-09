# Re-deriving the Rust table

Rust's claims need a real crate to check, but they are all locally verifiable — no network.

## Editions and MSRV

Run:

```bash
rustc -h | grep edition                 # accepted editions + which is stable
cargo metadata --no-deps --format-version 1 | jq '.packages[0] | {edition, rust_version}'
```

`rustc --edition` accepts `2015|2018|2021|2024|future`; stable is **2024**. Cargo **enforces** `rust-version`: setting it above the installed toolchain fails the build with `error: rustc X is not supported by the following package: requires rustc Y`. That makes the MSRV a real ceiling, not a comment.

## Fixer behaviour — verify, do not assume

Create a throwaway crate and watch what each tool actually rewrites. Run:

```bash
cargo new /tmp/probe && cd /tmp/probe
# seed idiom lints, then:
cargo clippy                      # report-only — read the suggestions
cargo clippy --fix                # apply; prints "Fixed src/main.rs (N fixes)"
git diff                          # the review surface
cargo fix --edition               # migrates BOTH Cargo.toml and source
```

Confirmed rewrites from `cargo clippy --fix` on a seeded snippet: `vec![1,2,3]` → `[1,2,3]`, `s.len() > 0` → `!s.is_empty()`.

## The trap: no dry-run

Unlike Go's `go fix -diff`, **Rust's fixers have no `--dry-run`** — verified against `cargo fix --help` and `cargo clippy --fix --help`. The diff-first discipline therefore rests on git. Run:

```bash
git status --porcelain                    # empty; cargo fix refuses a dirty tree
cargo clippy                              # report-only pass
cargo clippy --fix                        # apply
git diff                                  # review
```

Passing `--allow-dirty` to skip the refusal removes the only guarantee that `git diff` shows the *whole* change. Don't reach for it to get moving.

## MSRV vs stdlib

`rust-version` gates language features, but a crate can compile on its MSRV and still call a stdlib item added later — the compiler will accept it if the *installed* toolchain has it. Check the item's "Since" line in the stdlib docs against `rust-version` rather than trusting a successful local build.
