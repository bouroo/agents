---
name: modernize-coding
description: "Bring a project's code to current patterns — detect what the project itself declares and uses (manifests, toolchain config, prevailing conventions), modernize toward that ceiling, and write current style from the start. Use when modernizing, reviewing, or writing code in an existing project."
---

# Modernize Coding

"Modern" is a property of **the project you are working in**, not of a language release: the same construct is current in one repository and out of place in another. The question is never *is this the newest syntax?* but **what does this project use, and is this code behind it?**

**When to load:** modernizing a codebase, reviewing a diff for outdated patterns, or writing new code into an existing project. Not for correctness or performance work — that is [craft](../craft/SKILL.md) / [performance](../performance/SKILL.md).

## 1. Detect the project's ceiling

Read the project, not the internet. Three sources, in order of authority:

1. **What the project declares** — the supported baseline: `go.mod`'s `go` directive, `package.json` `engines` and dependency ranges, `tsconfig.json` `target`/`lib`, `pyproject.toml` `requires-python`, `.tool-versions`, `.nvmrc`, CI matrix. A construct newer than this is a break, not a modernization.
2. **What the tooling actually runs** — the installed compiler/interpreter and linters disclose what is genuinely available and catch a manifest that has drifted from reality.
3. **What the neighbours do** — the prevailing idiom is the tie-breaker where the baseline permits several forms. When the project writes it one way, matching it beats importing a fresher idiom; departing needs a reason, not a preference.

**Modernize toward the project's own ceiling, never past it.** A construct the project cannot yet compile is not an improvement. If the ceiling itself is the problem, that is a separate change: bump the baseline in its own commit, then modernize against the new one.

## 2. Rewrite existing code

Default to the project's own automated fixer: a mechanical rewrite is reviewable as a patch and reproducible on the next file.

1. **Find the project's fixer** — the adapter for its language (below).
2. **Run it in diff mode first** — never apply blind; review the patch as a reviewer, not an operator.
3. **Apply, then prove** with the project's own gates: formatter, linter, type-check, build, tests (§7 of the manifesto — a clean diff with a failing build is not done).

Escape hatch: hand-edit only where no fixer covers the rewrite, then run the same gates.

Keep modernization in **its own commit**, apart from behavior changes, dependency upgrades, and baseline bumps, so any regression bisects to one cause. Automated fixes preserve behavior only as far as their analyzer is correct — review is the check, not the tool's confidence.

## 3. Write current from the start

Before writing a construct, ask the §1 question — *what does this project use?* — and write that. Two failure modes, opposite directions:

- **Behind**: hand-rolling what the baseline and libraries already provide. Fixer-enforced where one exists, so drift back is visible in review.
- **Ahead**: syntax newer than the baseline, or idiom that ignores how the project writes everything else. Compiles locally, breaks the build elsewhere, reads as foreign either way.

Prefer the project's dependencies and standard library before adding a new one.

## 4. Language adapters

The method above is language-agnostic. Load only the adapter for the project's language; each names the ecosystem's default fixer and the declared baseline the rewrites key to. Adding a language means adding a reference file, not changing this skill.

**Go** — default `go fix` (Go >= 1.26; else the `modernize` analyzer); baseline `go.mod` `go` directive.
- [Go guide](references/go/guide.md)
- [Analyzer inventory](references/go/analyzers.md)
- [gopls MCP](references/go/gopls-mcp.md)

**Java** — default OpenRewrite; baseline `pom.xml` / Gradle `release`.
- [Java guide](references/java/guide.md)
- [Java verify](references/java/verify.md)

**Rust** — default `cargo fix --edition`; baseline `Cargo.toml` `edition` + `rust-version`.
- [Rust guide](references/rust/guide.md)
- [Rust verify](references/rust/verify.md)

**Python** — default `ruff --fix` (UP rules); baseline `pyproject.toml` `requires-python`.
- [Python guide](references/python/guide.md)
- [Python verify](references/python/verify.md)

**TypeScript / JS** — default `eslint --fix`; baseline `tsconfig.json` `target` + `package.json` `engines`.
- [TypeScript / JS guide](references/typescript/guide.md)
- [TypeScript / JS verify](references/typescript/verify.md)

Where the ecosystem ships a local machine-readable record of when each feature landed (Go's `GOROOT/api`, Java's `src.zip` `@since` tags), the [modernize gate](../../scripts/check.py) cross-checks the adapter table against it; the Java verify reference gives the method.
