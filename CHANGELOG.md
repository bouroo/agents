# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Pre-4.0 entries were retired in the v4 fresh start; the full history lives in git
tags and log (`v1.0.0` through `v3.11.0`).

## [4.3.0] - 2026-09-03

### Added

- **`skills/system-diagramming`**: self-contained system diagramming — turn a
  codebase or system description into one interactive HTML artifact (inline
  SVG, dark/light themes, pan/zoom, hover tracing, search) with no installs
  and no network. Author a small typed JSON IR inside the bundled template
  (five kinds: architecture, workflow, sequence, dataflow, lifecycle; the
  renderer draws it deterministically), then gate it with the bundled stdlib
  validator (`E_*`/`W_*` diagnostics) before handoff. Exports, motion, and
  share cards are out of scope.

### Changed

- **`skills/confluence`**: both supported MCP servers are now first-class -
  the official Rovo remote server (OAuth; read/search/Teamwork-Graph surface)
  and mcp-atlassian (open-source; hosted, e.g. mcp-atlassian.soomiles.com, or
  local stdio with an API token; full page CRUD). Adds tool-shape detection
  (server names are arbitrary; camelCase-with-cloudId vs snake_case-pinned-to-
  one-site), a per-operation routing table with write-defaults-to-mcp-atlassian
  when both are connected, mcp-atlassian transport rules (storage-format macros
  first-class, `confluence_update_page_section` as the low-blast-radius path,
  `version_comment` on updates, read-back via `convert_to_markdown: false`),
  and hosted-endpoint setup. Retracts the wrong claim that the local stdio
  fallback shared Rovo's tool surface.

## [4.2.0] - 2026-09-02

### Added

- **`skills/go-modernize`**: Go modernization discipline keyed to the module's
  declared version (`go` directive in go.mod, toolchain fallback): run `go fix`
  (Go ≥ 1.26) or the standalone `modernize` analyzer with `-diff`-then-apply
  review, plus a write-modern-from-the-start idiom table. A reference file
  maps every fixer (evidence: go1.26.7's fixer set vs current
  `modernize@latest` — overlapping but non-identical; `bloop`, `fmtappendf`,
  `appendclipped`, `slicesdelete` documented upstream but not in either yet).
  A second reference encodes the one-shared-`gopls serve -mcp.listen` MCP
  singleton pattern (login-time supervisor + held-open stdin; legacy
  HTTP+SSE transport; per-host wiring by client transport class, stdio-only
  hosts via a bridge) verified end-to-end on this machine. Ports are
  discovered, not fixed: probe for a live instance, else bind a free high
  port (49152–65535) and publish it (`~/.local/state/gopls-mcp.port`) for
  hosts/bridges to resolve at connect time.

- **`skills/solution-architecture`**: solution-architecture discipline distilled
  from the Awesome AI Architect knowledge base (15 topics): frame ASRs as SEI
  quality-attribute scenarios, choose patterns/styles by context and trade-off,
  record significant decisions as ADRs (Y-statement core, MADR template),
  model in C4 zoom levels, size with three-point estimates, and govern with
  federated standards plus automated conformance. Eight references carry the
  depth (requirements, quality attributes, patterns, decisions, modeling,
  delivery contexts, governance, communication); descriptions across the five
  discovery manifests now say seven on-demand skills.

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
