---
name: modernize-coding
description: "Bring a project's code to current patterns — detect what the project itself declares and uses (manifests, toolchain config, prevailing conventions), modernize toward that ceiling, and write current style from the start. Use when modernizing, reviewing, or writing code in an existing project."
---

# Modernize Coding

"Modern" is a property of **the project you are working in**, not of a language release. The same construct is current in one repository and out of place in another, because what a project may use is set by what it declares, what its toolchain supports, and what its neighbours already do. So the question is never *is this the newest syntax?* — it is **what does this project use, and is this code behind it?**

**When to load:** modernizing a codebase, reviewing a diff for outdated patterns, or writing new code into an existing project. Not for correctness or performance work — that is [craft](../craft/SKILL.md) / [performance](../performance/SKILL.md).

## 1. Detect the project's ceiling

Read the project, not the internet. Three sources, in order of authority:

1. **What the project declares** — manifests and toolchain config name the supported baseline: `go.mod`'s `go` directive, `package.json` `engines` and dependency ranges, `tsconfig.json` `target`/`lib`, `pyproject.toml` `requires-python`, `.tool-versions`, `.nvmrc`, CI matrix. This is the ceiling: a construct newer than the declared baseline is not modernization, it is a break.
2. **What the tooling actually runs** — the installed compiler/interpreter and linters disclose what is genuinely available, and catch a manifest that has drifted from reality.
3. **What the neighbours do** — the prevailing idiom within the project is the tie-breaker where the declared baseline permits several forms. Consistency (§1 of the manifesto) decides: when the project writes it one way, matching it beats importing a fresher idiom. Departing needs a reason, not a preference.

**Modernize toward the project's own ceiling, never past it.** A construct the project cannot yet compile is not an improvement. If the ceiling itself is the problem, that is a separate, deliberate change — bump the baseline in its own commit, then modernize against the new one.

## 2. Rewrite existing code

Prefer the project's own automated fixers over hand-editing: a mechanical rewrite is reviewable as a patch and reproducible on the next file. The shape is the same everywhere —

1. **Find the project's fixer** for the ecosystem (compiler-assisted rewrites, codemods, linters with autofix, an editor/agent language server). The [Go adapter](references/go/guide.md) is the worked example.
2. **Run it in diff mode first** — never apply blind. Review the patch as a reviewer, not an operator.
3. **Apply, then prove** with the project's own gates: formatter, linter, type-check, build, tests (§7 of the manifesto — a clean diff with a failing build is not done).

Keep modernization in **its own commit**, apart from behavior changes, dependency upgrades, and baseline bumps, so any regression bisects to one cause. Automated fixes preserve behavior by construction only as far as their analyzer is correct — review is the check, not the tool's confidence.

## 3. Write current from the start

Before writing a construct, ask the §1 question — *what does this project use?* — and write that. Two failure modes, opposite directions:

- **Behind**: hand-rolling what the project's own baseline and libraries already provide. Fixer-enforced in the ecosystems that have one, so drift back is visible in review.
- **Ahead**: reaching for syntax newer than the declared baseline, or idiom that ignores how the project writes everything else. Compiles locally, breaks the build elsewhere, and reads as foreign either way.

Prefer the project's dependencies and standard library before adding a new one to approximate either.

## 4. Language adapters

The method above is language-agnostic. Per-ecosystem specifics — the fixer tooling, the version-to-feature tables, the language-server workflow — live in adapters, loaded only when the project is in that language. The pattern for any new adapter: name the ecosystem's fixer and its diff/apply switch, and name the **declared baseline** the rewrites key to.

| Adapter | Fixer tooling | Baseline source | Version table |
|---|---|---|---|
| [Go](references/go/guide.md) | `go fix` / `modernize` analyzer / gopls MCP | `go.mod` `go` directive | [analyzers](references/go/analyzers.md) |
| [Java](references/java/guide.md) | OpenRewrite / Error Prone / `jdeprscan` | `pom.xml` or Gradle `release` | in [guide](references/java/guide.md) · [verify](references/java/verify.md) |
| [Rust](references/rust/guide.md) | `cargo fix --edition` / `clippy --fix` | `Cargo.toml` `edition` + `rust-version` | in [guide](references/rust/guide.md) · [verify](references/rust/verify.md) |
| [Python](references/python/guide.md) | `ruff --fix` (UP) / pyupgrade | `pyproject.toml` `requires-python` | in [guide](references/python/guide.md) |
| [TypeScript / JS](references/typescript/guide.md) | `tsc --target` / ESLint `--fix` / jscodeshift | `tsconfig.json` `target` + `package.json` `engines` | in [guide](references/typescript/guide.md) |

Adding a language means adding a row and a reference file — not changing this skill. Two anchors are worth copying when you do: where the ecosystem ships a local machine-readable record of when each feature landed (Go's `GOROOT/api`, Java's `src.zip` `@since` tags), the [modernize gate](../../scripts/check.py) can cross-check the table against it — see the Java [verify](references/java/verify.md) note for the method.
