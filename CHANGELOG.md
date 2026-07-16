# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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