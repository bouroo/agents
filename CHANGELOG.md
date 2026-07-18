# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.5.0] - 2026-07-18

### Added
- `go-essential` skill: production-readiness rules for Go (code style, naming, error handling, safety, structs and interfaces, concurrency, context, testing, project and design, design patterns, observability, documentation, performance, safe refactoring). Ships as a core SKILL.md plus fourteen deep-dive references under `skills/go-essential/references/`. Registered in `plugin.json` and `marketplace.json`; catalog copy now reads "seven on-demand skills".

### Changed
- `agents/conductor.md` operational boundary hardened: pre-flight classification is now mandatory every turn (delegate / read-only direct / halt); self-execution (editing source, running the toolchain, or committing outside a sub-agent) is a logged Structural failure, not a shortcut. Granular `permission` block denies destructive git and all `edit` outside `.agents/`, allows a whitelist of read-only inspection commands, and prompts (`ask`) on everything else. `steps` raised from 50 to 60.
- Plugin and marketplace manifests bumped from 1.4.0 to 1.5.0.

### Fixed
- Em/en-dash characters across `skills/go-essential/references/*.md` that tripped `scripts/checks.py` gate G6 (no-dash) replaced with ASCII hyphens; the gate is green again.

## [1.4.0] - 2026-07-17

### Added
- `judge-phase` registered in `plugin.json` `commands[]` and the marketplace catalog text. The command itself shipped in v1.3.0 but was missing from both manifests; the catalog copy still read "four slash commands".
- Mermaid diagram requirement added to `repo-documentation` flow docs (`docs/flows/`) so flow explanations carry a visual alongside the prose.

### Changed
- `AGENTS.md` slimmed from 132 to 114 lines; rhetorical scaffolding trimmed, hard constraints and the artifact-gate vocabulary retained; the four-phase "Spec, plan, implement, verify" rhythm replaced by the fable-method `think/act/prove` vocabulary.
- `agents/conductor.md` re-cut around the fable-method `think/act/prove/grow` rhythm. Direct `edit` of `AGENTS.md` removed from the conductor's allowlist (delegation-only).
- `skills/harness-engineering/SKILL.md` slimmed (431 lines removed, 197 retained): per-section "Rules" enumerations that duplicated the `AGENTS.md` router copy dropped; the failure-mode table and reference points for sections 11/12/14/18 retained.
- `skills/spec-driven-development/SKILL.md` REASONS canvas reordered and re-lettered: the two `S` sections are now distinct -- `S` (Safeguards, non-negotiable constraints) and a new terminal `S` (Signoff, approval + rollout gate). The previous single-`S` ambiguity is gone.
- `skills/performance-patterns/SKILL.md` and `skills/effective-code-craft/references/intent-gate.md`: prose tightened; absolute "always" claims softened to scope-bound guidance; relative cross-link paths corrected.
- `plugin.json` description and `marketplace.json` description updated to reflect five commands and the think/act/prove loop. The catalog copy was stuck at the v1.3.0 wording.

### Fixed
- `marketplace.json` was pinned to `1.3.0` in both the top-level and the plugin-entry `version` fields while `plugin.json` already read `2.0.0` -- same stale-version class as the v1.3.0 marketplace duplicate fix, re-merged here.
- `marketplace.json` description still said "four slash commands" and "spec, plan, implement, and verify loop" after `judge-phase` shipped; reworded to "five slash commands" and "think/act/prove loop".
- Em-dash characters in `skills/performance-patterns/SKILL.md` that tripped `scripts/checks.py` G6 replaced with ASCII `-` to satisfy the no-dash gate.

## [1.3.0] - 2026-07-16

### Added
- Four forced artifact-gate report lines (INTENT, TWINS, AUTH, PENDING) in AGENTS.md and `effective-code-craft`: a mechanical sweep owed at decision points (behavior changed, defect fixed, outward action taken, prescribed follow-up untaken). Conductor convergence now blocks on a clean artifact-gate sweep.
- Two adversarial verification eval scenarios: `s3-artifact-gate` (the gate fires on missing owed lines even when the work is correct) and `s4-twin-check` (searching the whole project for the same defect after fixing one site). Seed results in `eval/results/r3.json` and `r4.json` carry `passed: null` per the repo honesty rule.
- `harness-engineering` failure-mode rows for verification theater, false completion, retry thrash, unprompted fixing, and debris-left-behind; loop/memory engineering boundary definitions.

### Changed
- `judge-phase` and `verify-phase` commands enforce the artifact-gate sweep during adversarial verification and verification passes.
- Phase command docs (document/judge/refactor/review/verify) and conductor boundary definitions unified on the artifact-gate vocabulary; orphan headings in `spec-driven-development` cleaned up.

## [1.2.0] - 2026-07-16

### Added
- `judge-phase` command: adversarial verification of finished work -- treats a "done" report as claims, re-runs verifications, hunts the classic frauds (weakened checks, false completion, scope creep, spec betrayal, debris), and delivers a VERIFIED / VERIFIED WITH CAVEATS / REFUTED verdict. Distinct from the trusting `review-phase`.
- `harness-engineering` §18: the Judge stance and fraud-table doctrine backing `judge-phase`.
- `effective-code-craft` "Classify the Ask" section: triviality gate (one file, under ~10 changed lines, no new behavior, no searching) plus the question / task / plan-first classification table with tie-breaks.
- `harness-engineering` §14: "Analysis paralysis" failure-mode row with the "one batch plus one follow-up, then a stated reason or stop" research bound.
- `eval/scenarios/s2-fraudulent-work/`: seed scenario (five planted frauds behind a confident completion report) probing the adversarial-verification rule; `eval/results/r2.json` committed as seed (`passed: null`) per the repo's honesty rule.

### Changed
- Conductor PROVE phase now includes the Judge role alongside Tester and Reviewer.
- `README.md` command table registers `judge-phase`.
- Bumped `plugin.json` and `marketplace.json` versions from 1.0.0 to 1.2.0; the manifests had drifted behind the release tags.

### Fixed
- `CHANGELOG.md` en-dash in the skill-name length entry broke the G6 no-dash gate in CI; replaced with an ASCII hyphen.

## [1.1.0] - 2026-07-16

### Added
- Plugin packaging (`plugin.json`, `marketplace.json`) and cross-platform installers (`install.sh` POSIX, `install.ps1` Windows).
- Skill-name length constraint (1-64 chars) validation gate (`scripts/validate-agents.sh`).
- Adversarial judge-phase in the conductor agent and accompanying doc cleanup.
- CI workflow (`.github/workflows/validate.yml`) running `scripts/checks.py` and `scripts/validate-agents.sh` on push/PR to `main` and `develop`.
- Kilo/Opencode configuration example in `README.md`.

### Changed
- Decision-making framework refined: removed the single-question constraint for ambiguous, high-impact, hard-to-reverse decisions.
- Context-compaction protocols and documentation workflows (`document-phase` command, `repo-documentation` module) defined in agent operating doctrine.
- Conductor "Clock-in" mandates ledger bootstrapping (`mkdir -p .agents/*`) before any file write.
- `.agents/` directory location clarified and ignored in the config repo.
- Opencode schema and context-management guidelines updated.

## [1.0.1] - 2026-07-15

### Added
- CI workflow running `scripts/checks.py` and `scripts/validate-agents.sh` on every push/PR to `main` and `develop`.
- `scripts/validate-agents.sh`: skill-name length constraint (1-64 chars) gate.
- Kilo/Opencode configuration example (model, agent, compaction, provider blocks) in `README.md`.
- `document-phase` command and `repo-documentation` module registered in `README.md`.

### Changed
- Conductor "Clock-in" now mandates a "Bootstrap the ledger" step that creates `.agents/*` directories before any file write; explicit `mkdir -p .agents/*` permission granted.
- Decision-making framework: removed the "one question" constraint for ambiguous high-impact decisions; allows flexible follow-up questioning.
- `AGENTS.md` codifies Context Management practices (lazy loading, semantic indexing) and adds Compaction Resilience / Context Condensing guidance.
- `.gitignore` excludes `.agents/` to keep runtime state out of the configuration repo; docs clarify that `.agents/` paths are project-workspace-relative.

### Removed
- `SKILL.md` content in `skills/harness-engineering/` trimmed during refactor.

## [1.0.0] - 2026-07-14

### Added
- Plugin packaging: `plugin.json` and `marketplace.json` manifests for cross-tool installation.
- Cross-platform installers: `install.sh` (POSIX) and `install.ps1` (Windows).
- `scripts/checks.py`: 9-gate deterministic validator covering manifests, frontmatter, cross-references, em/en-dash discipline, and AGENTS.md budget.

### Changed
- Conductor agent reframed as Kilo primary mode with think/act/prove phase rhythm.
- README de-coupled from tool-specific model names; the example config now uses generic placeholders.

[1.0.0]: https://github.com/bouroo/agents/releases/tag/v1.0.0
[1.0.1]: https://github.com/bouroo/agents/releases/tag/v1.0.1
[1.1.0]: https://github.com/bouroo/agents/releases/tag/v1.1.0
[1.2.0]: https://github.com/bouroo/agents/releases/tag/v1.2.0
[1.3.0]: https://github.com/bouroo/agents/releases/tag/v1.3.0
[1.4.0]: https://github.com/bouroo/agents/releases/tag/v1.4.0
[1.5.0]: https://github.com/bouroo/agents/releases/tag/v1.5.0
