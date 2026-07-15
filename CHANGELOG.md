# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- Fable-method methodology blended into existing skills: Intent Gate (effective-code-craft), Hard Verify Bound plus verification-theater detection plus enriched failure modes (harness-engineering).
- `scripts/checks.py`: 9-gate deterministic validator covering manifests, frontmatter, cross-references, em/en-dash discipline, and AGENTS.md budget.

### Changed
- Conductor agent reframed as Kilo primary mode with think/act/prove phase rhythm.
- README de-coupled from tool-specific model names; the example config now uses generic placeholders.

[1.0.0]: https://github.com/bouroo/agents/releases/tag/v1.0.0