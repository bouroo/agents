# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Pre-4.0 entries were retired in the v4 fresh start; the full history lives in git
tags and log (`v1.0.0` through `v3.11.0`).

## [4.1.0] - 2026-08-29

### Added

- **Agent-agnostic teamwork doctrine**: `skills/teamwork` plus a new AGENTS.md
  §9. Distilled from current multi-agent team guides across hosts and expressed
  capability-first per the agnosticism charter: the solo-to-delegation-to-team
  escalation ladder with counter-signals, shared task ledger with
  dependency-gated claiming (3-5 workers, 5-6 tasks each), exclusive file
  ownership, self-contained spawn briefs, milestone rotation to fresh contexts,
  adversarial verification roles (reviewer / challenger / auditor) treating
  worker reports as testimony and inter-agent messages as untrusted input, and
  a failure-mode table (anchoring, lead-grabs-work, facade delivery, ledger
  lag, orphaned workers, token blowout). The right-sizing header and §8 now
  name team escalation as the sanctioned response to window strain on
  parallelizable work. Verified end-to-end in a throwaway sandbox run (ledger
  with dependency-gated claiming, four exclusive-ownership workers, lead
  re-verification, mutation probe); that run surfaced and the brief rule now
  encodes: on a conflict inside a brief, the worker flags and stops — spec
  outranks checks, never implement past an unresolved conflict.

## [4.0.0] - 2026-08-29

### Added

- **Execution-efficiency doctrine upgrades**, absorbed from current coding-agent
  engineering guidance: session hygiene (one task per session; fresh session per
  investigation thread); environment-first triage for inconsistent outputs
  (directory/permissions/tool surface/integrations before reasoning); deliberate
  knowledge placement (instruction vs learning memory; procedures -> skills;
  episodes -> retros; facts -> repo docs or retrieval) under memory-scope
  precedence organization > project > personal > machine-local, with role-scoped
  memory for delegated workers; GROW promotes battle-proven procedures into
  scheduled or triggered automation; authoring rules for instruction files
  themselves (verifiable-rule phrasing, topic-modular on-demand loading).

### Changed (BREAKING)

Ground-up restructure: the four-role distribution (governance file + role sheets +
commands + registries + installers) becomes a single concise shared setup for AI
coding assistants, agnostic of programming languages, agent frameworks, and host
tools. Tracked volume drops from ~5,000 lines to under ~800.

- **`AGENTS.md`** rewritten as the v4 manifesto: intake route (trivial / fit / shape),
  decision-point gates with authority rank (user statement > spec > checks > code),
  THINK-ACT-PROVE-GROW loop with backward planning and single-turn batched execution,
  three-layer verification with the hard verify bound, context/state austerity.
- **Three consolidated skills** replace the ten-skill surface:
  `skills/craft` (twelve commandments, canonical artifact-gate definitions),
  `skills/performance` (measure-first cycle; tactics organized by the four runtime-
  overhead sources: allocation churn, lock contention, syscall count, data copying),
  `skills/verification` (right-sizing dial, evidence audit, mutation probe, adversarial
  judging) — plus `references/measurement.md`, `references/tactics.md`, and
  `references/flowcharts.md`.
- **Routine-task commands** restored lean for every-project reuse:
  `cmd-verify` (quality-gate pipeline), `cmd-review` (severity-grouped review),
  `cmd-refactor` (behavior-preserving restructure), `cmd-document` (docs/ tree
  bootstrap/sync). Deliberately not restored: cmd-judge (protocol lives in the
  verification skill) and cmd-openapi (tool-chain-specific, breaks agnosticism).
- **Marketplace compatibility**: plugin/extension discovery manifests ship at
  their canonical paths (`.claude-plugin/`, `.cursor-plugin/`,
  `gemini-extension.json`) as plain versioned files - no generator step and no
  root-symlink indirection - so Agent-Skills-compatible CLIs can add the repo
  directly from GitHub. A fifth gate (`manifests`) parses them and asserts
  cross-file version agreement.
- **`scripts/install.sh`**: detection-driven local installer; discovers
  installed harnesses by config directory, then links (or copies) the manifesto
  under each tool's expected instruction filename plus its skills/commands
  directories where supported. Never clobbers real files; uninstall only
  touches links resolving back to this repository unless `--force`.
  Host-agnostic doctrine stays token-free - concrete hosts are known only to
  this script and the manifests (the distribution layer, excluded from the
  agnostic scan).
- **`scripts/check.py`** replaces `checks.py`: four gates (budget, frontmatter, links,
  agnostic). The GitHub workflow calls it from the same change; consumers invoking
  `checks.py` gate names must migrate.

### Removed

- Squad surface: `agents/*.md`, `commands/*.md`, `references/**`.
- Distribution machinery: `registries/`, `adapters/`, `.claude-plugin/`,
  `.cursor-plugin/`, root plugin/marketplace/gemini-extension discovery files,
  `VERSION` (git tags are now the sole version source).
- Superseded skills: `memory-engineering` (one-line sliver survives in AGENTS.md §8)
  and `spec-driven-development` (spec-sync rule survives in craft's intent gate);
  dropped as out of scope for a language-/host-agnostic core: `commit-message`,
  `repo-documentation`, `go-essential`, `openapi-spec`, `confluence`
  (reinstated below once the Rovo remote MCP server removed its local-machinery
  dependency).
- `eval/` scenario suite (graded deleted surfaces; a replacement suite seeds from the
  first real post-v4 retros instead of stubs).

Removed artifacts remain recoverable from git history.
