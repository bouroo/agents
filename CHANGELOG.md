# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.7.0] - 2026-07-19

### Added
- `lsp` permission enabled on `coder`, `conductor`, and `discover` agents so they can use language-server tooling (go-to-definition, find-references, hover, diagnostics) when the host runtime exposes an LSP tool.

### Changed
- Permission blocks in `agents/coder.md`, `agents/conductor.md`, and `agents/discover.md` rewritten from explicit allow-list + `*: ask`/`*: deny` fallback to a single broad allow followed by specific destructive-command denials. Under Kilo's "last matching rule wins" precedence the broad allow MUST come first and the denials MUST come after, so the deny-list still wins. Net effect: fewer user prompts during normal operation while the same destructive-command guardrails (force-push, reset --hard, clean -fd, commit --amend, rm -rf /, rm -rf ~, sudo) remain in force.
- `conductor` edit policy moved from `deny` with narrow allow-rules to `allow` with `external_directory: ask` enforcing the worktree boundary (any access outside the current working directory prompts at runtime; the user can save the pattern).
- `README.md` Kilo/Opencode config example replaced abstract `<your-model-here>` placeholders with concrete Anthropic model IDs and now includes `coder` and `discover` subagent entries alongside the built-in agents.
- All plugin manifests (`.agents/plugins/{claude,cursor,gemini,legacy}/`) bumped from 1.6.1 to 1.7.0.

## [1.6.1] - 2026-07-19

### Added
- `coder` and `discover` named subagents. The eight-role squad (Architect, Explorer, Scout, Implementer, Fixer, Tester, Reviewer, Judge) consolidates into two agent files: `agents/coder.md` mutates source and runs the toolchain across implement / fix / verify / judge modes; `agents/discover.md` is strictly read-only across plan / explore / lookup / review modes. Each ships its own `permission:` block so the conductor's restrictive policy does not propagate (the "write/edit permission denied" inheritance fix).

### Changed
- `agents/conductor.md` routing rewritten around the two named squad members: `task:` allow-list switched from `general`/`explore` to `coder`/`discover`; the squad table, routing cheatsheet, THINK/ACT/PROVE phase prose, and failure-routing table all reference the new names. Permission block restructured under the open `permission:` frontmatter schema; default `edit` policy tightened from `ask` to `deny` with explicit allow-rules only for `.agents/handoff/**` and `.agents/plans/**`. Steps raised from 60 to 120.
- All plugin manifests (`.agents/plugins/{claude,cursor,gemini,legacy}/`) bumped from 1.6.0 to 1.6.1.

## [1.6.0] - 2026-07-19

### Added
- skills.sh / Claude Code plugin marketplace compatibility. New `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` manifests declare every skill via `./skills/<name>` paths (Claude Code convention) so `npx skills add bouroo/agents` discovers and installs them across Claude Code, Cursor, Codex, OpenCode, Kilo, Cline, Copilot, Antigravity, AMP, Gemini CLI, and 30+ other compatible runtimes tracked at skills.sh.
- Cursor plugin marketplace compatibility. New `.cursor-plugin/plugin.json` and `.cursor-plugin/marketplace.json` per the official [cursor/plugins](https://github.com/cursor/plugins) schema declare all seven skills, the conductor agent, and the five phase commands.
- Gemini CLI extension compatibility. New `gemini-extension.json` at repo root per the [Gemini CLI extensions reference](https://geminicli.com/docs/extensions/reference/); installs via `gemini extensions install https://github.com/bouroo/agents` and surfaces `skills/`, `commands/`, and `agents/` to Gemini CLI and Antigravity CLI.
- Consolidated manifest source-of-truth under `.agents/plugins/<tool>/` -- every tool-specific plugin manifest now lives canonically in one of `.agents/plugins/{claude,cursor,gemini,legacy}/`, surfaced at its tool-discovery path via a symlink. `.gitignore` updated to keep `.agents/plans/` and `.agents/handoff/` (the per-project runtime ledger) ignored while shipping `.agents/plugins/`.
- `G10_claude_plugin_manifests`, `G11_cursor_plugin_manifests`, `G12_gemini_extension_manifest`, and `G13_plugin_symlinks` gates in `scripts/checks.py`. G10-G12 validate the manifest contents (parse, required keys, declared-skill paths resolve on disk, name patterns); G13 enforces the symlink invariant so a future edit at a discovery path cannot silently fork from `.agents/plugins/<tool>/`. Brings the deterministic gate count from 9 to 13.
- Per-skill `## References` sections (or expanded existing ones) across all seven skills, applying the agentskills.io best-practice of progressive disclosure: each entry carries an explicit "load when X" hint instead of a bare link, so the agent pulls depth on demand rather than eagerly.
- skills.sh badge and Agent-Skills spec / best-practices / optimizing-descriptions links in `README.md` References.

### Changed
- `link.sh` is now a thin backward-compat shim (54 lines, down from 195) that execs `install.sh` after translating the legacy verbs (`link` -> `install`, `unlink` -> `uninstall`). Tool filters (`gemini`, `antigravity`, `antigravity-ide`, `codex`, `claude`, `qwen`, `opencode`, `kilo`), `--dry-run`, `--force`, `-h|--help|help`, and bare tool names are forwarded verbatim. All symlink logic, idempotency, dry-run, and the summary line now live in exactly one place (`install.sh`); the two scripts are interchangeable from the user's perspective. README Quick Start D documents both vocabularies side by side.
- `go-essential` Cross-References rewritten: every `references/*.md` entry now carries a "load when <section> hits <situation>" hint per the agentskills.io progressive-disclosure pattern, instead of a flat `·`-separated list.
- `harness-engineering` References rewritten with the same "load when X" discipline -- each of the 17 cited sources is anchored to the section it defends or extends.
- `effective-code-craft` Cross-References and References split: sibling-skill links separate from external craft sources (JetBrains 10x, Google style, Clean Code, Pragmatic Programmer, Feathers), each with a "load when" hint.
- `repo-documentation` ships an explicit `## Templates (load on demand)` block pointing at `system.md` / `flow.md` / `adr.md` plus a `## References` section (Diataxis, Nygard ADRs, Mermaid syntax) -- the prior single paragraph is now progressive-disclosure-graded.
- `performance-patterns` Cross-References (sibling skills) separated from `## References` (goperf.dev, Google style, Brendan Gregg USE method, Rust perf book) with "load when" hints.
- `spec-driven-development` gains a `## References` section (Fowler SPDD, GitHub Spec-Kit, Sutton's Bitter Lesson) with "load when" hints.
- `commit-message` gains a `## References` section (Conventional Commits 1.0.0, Keep a Changelog, Angular format, git-log pretty formats).
- README rewritten: "Quick Start" split into A (skills.sh CLI), B (Cursor plugin marketplace), C (Gemini CLI extension), D (symlink installer); "Compatibility" section contrasts five install paths; "What's inside" tree shows the new `.agents/plugins/` source-of-truth layout and the discovery-path symlinks.
- Bumped all manifest versions (`.agents/plugins/{claude,cursor,gemini,legacy}/*`) from 1.5.0 to 1.6.0.

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
[1.7.0]: https://github.com/bouroo/agents/releases/tag/v1.7.0
[1.6.1]: https://github.com/bouroo/agents/releases/tag/v1.6.1
[1.6.0]: https://github.com/bouroo/agents/releases/tag/v1.6.0
