# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

_No changes yet._

## [3.0.0] - 2026-08-05

A ground-up reimplementation into an architecture that is **completely agnostic** of programming languages, agent frameworks, and host tools, while shipping every artifact in each popular harness's **native** discovery format. The coder-squad doctrine (governance router + conductor/coder/discover squad + THINK-ACT-PROVE-GROW loop + skills + eval honesty layer) is preserved and concisely re-implemented; only its *home* and *form* change. This is a **breaking** release for filesystem consumers; the doctrine itself is continuous with v2. Compatibility verified against the official schemas for [opencode](https://opencode.ai/docs/agents/), [Claude Code](https://code.claude.com/docs/en/sub-agents), [kilo](https://kilo.ai/docs/customize/workflows), [skills.md](https://skills.md/docs), and [agents.md](https://agents.md/).

### Added

- **Native harness compatibility.** Artifacts ship in each harness's own discovery format, not a custom one: **agents** are flat `agents/<name>.md` (opencode identity-by-filename; Claude Code `.claude/agents/`); **commands** are flat `commands/<name>.md` with an `agent` binding (opencode + kilo `.kilo/commands/` + Claude Code); **skills** are nested `skills/<name>/SKILL.md` per the [Agent Skills standard](https://skills.md/docs); **AGENTS.md** is a plain root Markdown file per the open [agents.md](https://agents.md/) standard.

- **Cross-host agent frontmatter.** Each agent carries a superset both kinds of harness read: `name` + `description` + `mode` (primary/subagent) + `tools` (for name-gated harnesses) + `permission` (a per-capability allow/ask/deny object for capability-gated harnesses). This enforces the read-only (`conductor`/`discover`) vs mutating (`coder`) boundary on every host -- a host that gates by tool name honors `tools`; one that gates by capability honors `permission`.

- **Host-agnostic core.** `AGENTS.md`, `agents/*.md`, `commands/*.md`, and the seven core skills contain no host-binding tokens and no language-bias doctrine. A new gate **`G17_agnostic_core`** scans every core file for host tokens (dotdirs, host config filenames, plugin-manifest paths, tool names) and fails on any leak. The three domain adapters (`go-essential`, `openapi-spec`, `confluence`) are excluded -- they legitimately name their domain.

- **Registries (single source of truth).** `registries/modules.json` (module registry: core squad + optional domain adapters) and `registries/hosts.json` (host-adapter registry: an abstract host contract + adapter instances). Adding a host is now an entry in a file, not a code change.

- **Abstract host-adapter installer.** `adapters/install.sh` (and `adapters/install.ps1`, `adapters/link.sh` shim) read `registries/hosts.json`; no hardcoded tool list lives in the core. Same `install`/`uninstall`/`status`/`list` modes, same `--dry-run`/`--force`/`<adapter>` options, same eight hosts as v2 (gemini, antigravity, antigravity-ide, codex, claude, qwen, opencode, kilo) -- now data, not code.

- **Three-tier customization resolver.** `scripts/resolve-customization.py` merges `customize.toml` base -> team (`.agents/custom/`) -> user layers with the bmad merge rules (scalars override; tables deep-merge; arrays-of-tables keyed by `code`/`id` replace+append). Optional -- artifacts function fully with inline defaults; a manual fallback is documented.

- **New gates.** `G16_registries_parse` (both registries parse, adapter codes unique) and `G17_agnostic_core` (core free of host tokens). The gate count is now 17 (authoritative via `checks.py --list`).
- **Endpoint-documentation (API) doc type.** *(added in beta.2)* The `document` command and `repo-documentation` skill gain an API category: one HTTP endpoint per file at `docs/api/<service>/`, authored from the new [api.md](skills/repo-documentation/references/api.md) template. The command bootstraps the matching `docs/templates/api.md` and wires an API doc to the [confluence](skills/confluence/SKILL.md) adapter's endpoint-page template, translating the doc's mermaid sequence diagram to PlantUML source for that generator.
- **Mermaid diagram support in the confluence adapter.** *(added in beta.2)* A new [mermaid.md](skills/confluence/references/mermaid.md) reference documents the native `mermaid` macro (raw CDATA body, no compression), its mirror-image newline rule (one statement per real newline -- the opposite of PlantUML sequence messages), and the byte-identical round-trip proof. The storage-format guide adds the macro template; the markdown-to-storage converter now renders mermaid fences.

### Changed

- **Repository layout.** `agents/<name>.md` (flat, native); `commands/<name>.md` (flat, native); `skills/<name>/SKILL.md` (nested, native). `AGENTS.md` is rewritten as a **governance agent persona + squad navigator** (120 lines, under the 220-line budget).

- **Skill relocations.** `effective-code-craft` -> `code-craft` (frontmatter `name` and dir align with the lint label). The three language/tool skills are top-level siblings: `skills/go-essential`, `skills/openapi-spec`, `skills/confluence` -- all ten skills are one level deep so every one-level skill scanner (opencode, Claude Code) discovers them.

- **Manifests relocated + generated.** `.agents/plugins/<tool>/` -> `adapters/manifests/<host>/`. The discovery-path symlinks (`.claude-plugin/`, `.cursor-plugin/`, `gemini-extension.json`, root `plugin.json`/`marketplace.json`) now target `adapters/manifests/`. `scripts/gen-manifests.py` reads `VERSION` + on-disk inventory + registries and writes all seven host manifests (flat agent/command paths); `G15_manifests_generated` fails on hand-edit drift. The `confluence` adapter's hard-coded tenant was scrubbed to placeholders (URLs read from settings/env).

### Removed

- v2 flat agent files (`agents/*.md`), `commands/`, the root `install.sh`/`install.ps1`/`link.sh` (moved to `adapters/`), and `.agents/plugins/` (moved to `adapters/manifests/`). v2 content is preserved in git history.
- *(beta.2)* This config repo's own v2-era `docs/` tree (`README.md`, `ADR 0001`, the multi-host-install flow, the coder-squad system doc, the glossary, and the `docs/templates/`). The repo now documents itself via `AGENTS.md` + skills; a `docs/` tree is a concern of the *target* repo, bootstrapped on demand by the `document` command, not shipped here.

### Upgrade (breaking for filesystem consumers)

- The native-format change (flat `agents/<name>.md` + `commands/<name>.md`) leaves **STALE** symlinks at hosts installed from v2. Run `adapters/install.sh install --force` (or `link.sh install --force`) to refresh; the installer detects STALE links and refuses to clobber real files without `--force`.
- Skill paths changed for four skills (`effective-code-craft` -> `code-craft`; `go-essential`, `openapi-spec`, `confluence` now top-level). Re-run the installer or `npx skills add bouroo/agents` after upgrading.

## [2.11.0] - 2026-08-04

### Added

- **`confluence` skill.** Durable operating doctrine for the `mcp-atlassian` server: surface and register the MCP tools when they do not load mid-session (a `mcp_bridge.py` stdio bridge calls the same server's real tools), resolve `/x/<id>` shortlinks to page ids, and author Confluence pages so code blocks and PlantUML diagrams render -- native storage format, never markdown. The Prime Directive is to use the configured MCP (not curl/REST) and to prove renders by decoding the stored body (the REST `body.view` returns a JS stub for macro-rendered content), never by trusting it. Ships four references (access, storage-format, plantuml, page-template) and a `page_template.py` generator matching the hand-built endpoint-page layout. The skill count in every host plugin manifest description is updated (eight to nine).

## [2.10.0] - 2026-08-04

### Changed

- **Comment policy is now a strict default, not advice.** `effective-code-craft` skill §3 "Code for Reading" replaces three loose bullets with a three-gate test a comment must clear before it is written: (1) naming is exhausted -- no clearer name, named helper, or local constant would make the line self-evident; (2) it states *why*, never *what*; (3) the *why* is not derivable by a reader fluent in the language. Banner dividers (`// ===== helpers =====`), section headers, and tracker-duplicating `// TODO` markers are now named as noise and omitted. Addresses recurring user reports that coder agents generated too many source comments; a prior pass (2.4.0) softened the rule but did not make omission the path of least resistance.

- **Doc comments must follow the language's official documentation convention strictly -- not freeform prose.** Added a per-language table (godoc, TSDoc / JSDoc, rustdoc, docstring, Javadoc / Doxygen) naming each convention's doc marker and the one rule the toolchain renders; a private helper takes no doc comment, an exported symbol takes a correct one. Propagated to `agents/coder.md` Hard Rules and `AGENTS.md` §8 Hard Constraints so the strict-convention requirement lands at the points that gate behavior.

### Added

- **godoc rule in `go-essential`.** Every exported identifier takes a `//` comment directly above it that opens with the identifier name as a complete sentence; `//` only (never `/* */`); exactly one package comment per package. The strongest codified doc convention was previously absent from the Go skill.

- **Doc-convention linting in `verify-phase`.** The PROVE lint stage now runs the language's doc-convention linter (`golangci-lint` / `revive`, `eslint-plugin-jsdoc`, `ruff` / `pydocstyle`, `cargo clippy`) so missing or malformed doc comments fail computationally rather than by LLM judgment; if the project configures no doc linter, the stage notes the absence and proceeds. Turns the comment-noise rule into a gate, not a guideline.

## [2.9.1] - 2026-08-03

### Fixed

- **`validate-openapi.mjs` is modeline-compatible.** The bundled validator now resolves the OpenAPI meta-schema from a [yaml-language-server modeline](https://github.com/redhat-developer/yaml-language-server#using-a-modeline) at the top of the spec -- the same `# yaml-language-server: $schema=<url>` comment the Red Hat YAML language server reads in editors (VS Code, IntelliJ) -- so the directive is a single source of truth shared by tooling and the validator. A new `parseModeline()` reads both the standard form and the IntelliJ-compatible `# $schema: <url>` form from the leading comment block; a legacy root `$ref` key remains supported as a backward-compatible fallback, and `$schema=none` is honored as a disable. The JSON-Schema dialect is now taken from the fetched meta-schema's own `$schema` rather than from the instance root. This finished a migration that had been left half-done and inconsistent: the template already used modeline comments (one pointing at the dialect, one a non-standard `$ref=` the editor ignores), the validator read root data keys the template no longer carried, and `SKILL.md` documented a third form -- so the validator could not validate its own template.
- **Template modeline corrected.** `openapi-template.yaml` replaces its two broken modeline lines with a single correct one pointing at the frozen OpenAPI 3.2 meta-schema.
- **`SKILL.md` directive section synced** to the modeline form (standard + IntelliJ), with the root-key trap retained only as a legacy note; hard rule and mistake-table row updated.

## [2.9.0] - 2026-08-03

### Added

- **Agent-Computer Interface (ACI) and composition-patterns references.** Two gaps that both [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) and [Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) stress hardest were absent from the doctrine, and are now closed as load-on-demand references under the existing `harness-engineering` skill (skill inventory unchanged at nine; the root `AGENTS.md` stays a lean router). New `skills/harness-engineering/references/agent-computer-interface.md` covers *designing* tools, slash commands, and MCPs -- the counterpart to `AGENTS.md` §2, which only covers *routing* which capability to call. Its checklist: self-contained contracts, non-overlapping responsibilities, poka-yoke arguments (absolute paths over relative, typed enums over free strings, required over optional where ambiguity is the failure mode), token-efficient returns (structure before bodies), and the feedback loop that a repeated tool misuse is a spec bug, not a model bug -- routed to the §13 Failure-Mode -> Control Map. New `skills/harness-engineering/references/composition-patterns.md` is the delegation topology menu -- prompt chaining, routing, parallelization (sectioning vs. voting), orchestrator-workers (the Conductor default), evaluator-optimizer (the coder judge mode) -- with explicit guidance to pick the smallest topology the job can hold and refuse the Average Answer Trap. Both references follow the repo's `## Source` convention: internal provenance only; external article citations live in `README.md`.
- **Pointers wired and context loop calibrated.** `AGENTS.md` gains three one-liners: tool *design* routing in §2 (load the ACI reference when authoring a tool), topology selection in §3, and a §7 "calibrate, don't preload" bullet that puts context on the same failure-driven discipline as controls (start minimal, add a line only when an observed failure demands it). `agents/conductor.md` and the `harness-engineering` skill cross-references point to the new references. `README.md` further-reading cites both Anthropic source articles.

## [2.8.0] - 2026-08-02

### Changed
- **Cross-reference drift closed across the doctrine.** Every `§N` pointer to `harness-engineering` was verified against the skill's current section numbering and corrected where a renumber had left it stale. Fixes span `AGENTS.md` (Failure-Mode map §14->§13), the three reference files (`verification-theater.md`, `intent-gate.md`, `memory-layers.md`), and the eval layer (`s2-fraudulent-work/README.md`, `RESULTS.md`, `results/r2.json`) -- the Adversarial-Judge stance is §10, not §18, and the three-layer binding is §7. Broken anchors actively mislead agents to the wrong section, so this is a correctness fix, not a style change.
- **`AGENTS.md` rewritten to surface under-used source knowledge.** The root doctrine already cited all eight grounding sources but under-surfaced several high-value concepts; they are now integrated in place while the file stays a lean router (the §0-§9 numbering is preserved, and it remains well under the G9 200-line budget): the **GOAL / CONTEXT / CONSTRAINTS / DONE_WHEN** task frame (§3); **guides (feedforward) vs sensors (feedback)**, "keep quality left", and computational-vs-inferential controls (§6); the two right-sizing axes -- action-complexity and context-complexity (Scope); the loop's **Decide** (one recommendation, not a survey) and **Report** (outcome-first, honest caveats) micro-steps (§3); and the explicit **instruction-memory vs learning-memory** split (§7). The trailing `Sources:` footer was removed.
- **Source provenance consolidated into the README.** Per the single-reference rule, every external provenance section was removed from the doctrine and skill files -- the `## References` / `## Reference` sections in all nine `skills/*/SKILL.md` plus two reference files, and the `## Source Attribution` sections in `go-essential` (SKILL and four references) -- so the README's categorized `## References` is now the only home for source links. The README gained the four previously-uncited sources (Fable Method, z.ai best-practice, z.ai memory-mechanism, O'Reilly *Stop Overengineering Your Agent Harness*) under a new **Agent instruction & memory** sub-heading, and its THINK→ACT→PROVE→GROW summary was synced to the sharpened §3 wording. Internal navigation (`skill -> skill`, `skill -> its own references/`) and the operational URLs the `openapi-spec` skill validates against are preserved; only provenance and attribution moved.
- **Concision pass: single-owner the duplicated norms.** Each `skills/` pointer in `AGENTS.md` is now a brief "load when X" hint (load effective-code-craft when writing/reviewing code; performance-patterns when profiling; harness-engineering when verifying beyond L1; memory-engineering when persisting learnings) so the router tells the agent *when* to pull each skill, and the inline guides/sensors and right-sizing definitions were trimmed to action-verbs. Role files stop re-defining shared norms: `conductor.md`'s four-phase loop (318->294 lines) and §14 GROW now defer to `AGENTS.md` §3/§9, and the comment rule is single-owned by `effective-code-craft` (`coder.md`, `review-phase.md` now point instead of restating). No norm changed -- only where each definition lives.

## [2.7.0] - 2026-08-01

### Added
- **z.ai best-practice gaps closed.** Cross-checked the [z.ai Devpack best-practice guide](https://docs.z.ai/devpack/resources/best-practice.md) against this repo; most of its guidance (plan-before-execute, project-level config files, full dev loop, skills for reusable workflows, repo-as-record) is already present and more rigorous here. Two genuine gaps closed: (1) the conductor's delegation packet gains a `CONSTRAINTS` field for non-negotiable engineering rules a cold subagent cannot derive from the repo (perf budgets, security boundaries, dependency limits, backward-compat) -- distinct from `SPEC` (the behavior contract: what the code must *do*) and right-sized (omit when none apply); (2) `AGENTS.md` §7 gains two session-boundary bullets: one task per conversation, fresh sessions for branch/exploration work, and that long sessions compress safely because the repo -- not the conversation -- is the system of record. Automation-triggers for stable workflows were deliberately skipped (out of scope for a static config bundle).
- **`memory-engineering` skill + Instruction/Learning separation.** New `skills/memory-engineering` skill (with `references/memory-layers.md`) codifies cross-session *learning* memory, distilled from Z.ai's Devpack memory mechanism. Its core rule -- the one most agents get wrong -- is **Instruction ≠ Learning memory**: agent-learned corrections and preferences must never be written into instruction files (`AGENTS.md`/`CLAUDE.md`, build docs), because they then drift behavior silently, become indistinguishable from deliberate standards, and resist removal; learning memory has its own auditable, forgettable files. The skill adds the Type (semantic/episodic/procedural) x Scope (project/user/local) grid, the retrieve/construct/update workflow (with *forgetting* as a first-class step), and file hygiene (a sub-200-line `MEMORY.md` index, one fact per file, scoped loading, `.local.md` for uncommitted machine-local facts). For harnesses with no native memory feature, it defines a project-root fallback at `.agents/memory/` (alongside `.agents/plans/` and `.agents/handoff/`), reusing this repo's existing hidden runtime-state convention and avoiding collision with the `agents/` subagent-definition dirs that OpenCode and similar tooling scan. `AGENTS.md` §7 gains three terse bullets (the rule, the retrieve/update workflow, the fallback) and stays a router; deep detail lives in the skill. Registered across all plugin manifests; version `2.6.0` -> `2.7.0`.
- **Generated manifests from a single source.** New `scripts/gen-manifests.py` (stdlib-only: `json`/`pathlib`/`argparse`) renders all seven host manifests under `.agents/plugins/<tool>/` from three derivable sources: the on-disk inventory (`skills/*`, `commands/*.md`, and `agents/*.md` filtered to `mode: primary`), a new root `VERSION` file, and embedded per-host templates. The skill/command/agent arrays and the version were previously hand-copied across four manifest files in three formats (bare names, `./skills/<n>`, `skills/<n>/SKILL.md`) and seven version locations; adding or removing one skill meant editing four files by hand. They are now derived and cannot drift. First generation is byte-identical to the checked-in files (proven by `gen-manifests.py --check`). New **`G15_manifests_generated`** gate in `scripts/checks.py` re-runs the generator in `--check` mode and fails if any checked-in manifest diverges, so a hand-edit or stale regeneration cannot silently ship; it pairs with `G7`/`G10`-`G13` (which validate that the generated output is well-formed).

### Changed
- **Commands ↔ skills consistency sweep (dedup, broken refs, filename drift).** An overlap audit across `commands/`, `skills/`, and `agents/` found the doctrine *layering* clean (AGENTS.md ↔ agents ↔ skills repetition is justified cold-subagent role-splitting) but three classes of drift in the supporting docs. All fixed: (1) **Five stale `§N` pointers** in commands cited section numbers that had drifted -- `judge-phase` pointed at a non-existent §18 (fraud table is §10) and §12 (grade-the-tests is §8); `review-phase` §11 (mutation is §8); `verify-phase` §10 for gates (gates are §4) and §15 for the recovery ladder (it is §9); plus a byte-identical duplicate line in `review-phase`. Corrected, and each ref now carries the heading name so future renumbering is self-correcting. (2) **Plan-artifact filename drift** -- `harness-engineering` named the plan state `task.md`/`progress.md`/`decisions.md` while the conductor (the only writer) writes `canvas.md`/`state.json`/`decision-log.md`; the skill's own convergence checklist gated against files that never get created. The skill now uses the writer's canonical names throughout. The `retro.md` two-home ambiguity (plan-scoped vs cross-session learning memory) is resolved in `memory-engineering/references/memory-layers.md`: `retro.md` is plan-scoped episodic, durable lessons graduate to `.agents/memory/`. (3) **Doctrine duplication** in three phase commands that *said* "the skill is the reference" then re-published the skill's content -- `document-phase` (ADR field lists, source-map rules, doc-type criteria), `openapi-phase` (the verbatim mode-selection rule and interview protocol), `judge-phase` (a fraud rubric richer than its skill's, proving two maintained copies had drifted). Stripped to the `refactor`/`review-phase` clean pattern (trigger + orchestration + pointer); the judge-phase's richer fraud signals were migrated into `harness-engineering` §10 as the single canonical table, and the command retains only its judge-specific hunting procedure. Net: one source of truth per doctrine; all 45 `checks.py` gates pass.


### Changed
- **Single validator.** `scripts/validate-agents.sh` (a 258-line bash re-implementation of `checks.py` gates G3-G5 frontmatter and G9 line-budget) is now an 11-line shim that `exec`s `scripts/checks.py`. Two validators in two languages could diverge; the documented entrypoint name is preserved while the duplicate logic is removed. CI (`.github/workflows/validate.yml`) now runs `checks.py --all` once instead of both scripts. The gate count is no longer hand-maintained in prose (it had drifted to "9 gates" in CI, "13-gate" in the README, "14"/"Fourteen" in the `checks.py` docstring); `--help` derives it from the `GATES` registry, and it is referenced as such everywhere else.

## [2.6.0] - 2026-07-30

### Added
- New **`openapi-spec`** skill and **`openapi-phase`** command: generate or repair an OpenAPI 3.2 contract into the working project's `docs/openapi.yaml` and validate it against the canonical OAS meta-schema. The skill carries verified external facts (OpenAPI 3.2.0 is the latest stable, released 2025-09-19; the immutable meta-schema is `https://spec.openapis.org/oas/3.2/schema/2025-11-23`, a JSON Schema 2020-12 document) and documents the **root-key directive trap**: that meta-schema sets `unevaluatedProperties: false` at the document root and forbids `$schema`/`$ref` there, so the requested two-line header is a *validation directive* -- stripped from the instance before validation, not spec content. Auto-detects **introspect mode** (reads framework route/handler signatures across Express/Fastify/Koa, Flask/Django/FastAPI, Spring, ASP.NET, Go net/http/gin/echo/chi, Rails) vs **interview mode** (greenfield or off-repo API). Ships two copy-in artifacts: `skills/openapi-spec/references/openapi-template.yaml` (an OpenAPI 3.2.0 skeleton with the inline directive header) and `skills/openapi-spec/references/validate-openapi.mjs` (fetches the meta-schema, dereferences its single `$dynamicRef "#meta"` to a local `$ref` because Ajv does not reliably resolve same-document dynamic anchors, strips the directive, and validates with Ajv 2020-12; deps `ajv` + `js-yaml`). The validator was proven against a valid template (exit 0), a deliberately broken spec (exit 1, reporting both the `unevaluatedProperties` violation and the missing `openapi` field), and a directive-less document (exit 2, refuses to run).
- Registered `openapi-spec` + `openapi-phase` across all plugin manifests (Claude, Cursor, legacy/OpenCode/Kilo, Gemini) and bumped the package version `2.5.1` -> `2.6.0`.

### Fixed
- The two Claude plugin manifests (`.agents/plugins/claude/plugin.json`, surfaced at the repo root via the `.claude-plugin/plugin.json` symlink) listed only six of seven skills in their `skills` array -- `go-essential` was present in the description text and in every other manifest (Cursor, legacy, Claude marketplace) but absent from this one array. Added `go-essential` (alongside `openapi-spec`) so the array matches its own description and the sibling manifests.

## [2.5.1] - 2026-07-27

### Fixed
- Resolves user-reported **`Tool call not found`** errors when this repo's agent config loads into a runtime whose tool names differ from the names the doctrine prescribed. Operating doctrine previously routed work by **host-specific tool names** (`read`, `grep`/`glob`, `semantic_search`, `explore`, `websearch`/`webfetch` -- Kilo/OpenCode-style); when the same `AGENTS.md` loaded into Claude Code, Cursor, Codex, and others, the agent followed the instruction and emitted a call to a tool that did not exist in that host. All such instruction text is now **capability-based** rather than name-based -- "open and read the file", "search by string or filename", "semantic/code search if your host offers it, else a narrow string search", "web search or fetch" -- with a defensive clause: *only call tools that actually exist in your runtime; never invoke a capability by a name borrowed from another tool.* Changed in `AGENTS.md` §2, `harness-engineering` SKILL.md §6 (plus a backticked `read` noun in §1), `conductor` permitted direct actions, the four phase commands' capability refs, and the `README` context-management note. Agent `permission:` frontmatter blocks are intentionally unchanged -- they are host config (consumed by hosts that understand them, silently ignored by those that don't) and never cause the model to emit a tool call.

## [2.5.0] - 2026-07-24

### Added
- New **right-sizing** reference, `skills/harness-engineering/references/right-sizing.md`: a two-axis complexity map (Action Complexity x Context Complexity) and a control dial telling the agent how many verification layers to run and whether mutation testing, adversarial judging, or a GROW retro are warranted. Distilled from O'Reilly Radar, *Stop Overengineering Your Agent Harness* (the Average Answer Trap and the Kirby Effect). Routed from `harness-engineering` SKILL.md, `AGENTS.md`, `coder.md`, `conductor.md`, and `verify-phase`.

### Changed
- Verification is now **complexity-proportional**, not universal. L1 (static) runs on every source change; L2 (runtime) runs when the change has runtime behavior; L3 (end-to-end) runs when the change crosses a real boundary (`n/a` allowed with a one-line reason). The mutation probe runs only when the unit bears behavior under test, not "at least one per run." Executable evidence is still never optional -- the dial chooses which layers, never the evidence standard. Replaces the prior "skip none" stance in `harness-engineering` §7 + Appendix A, `coder` Verify mode, `AGENTS.md` §6, and `verify-phase`.
- **Conductor planner/actor split softened.** Delegation remains the default (separating planning from execution is a real reliability gain), but the hard "never mutate source / structural harness failure" stance is replaced by a narrow **trivial-work escape hatch**: for Low/Low units (typo, rename, format-only, one-line fix, no cross-file spread) the conductor may make that one edit and run the single relevant check directly instead of paying a full round-trip, provided it still self-verifies and preserves WIP = 1. The safety floor (installs, full builds, test suite, commits, destructive git, outward side effects) is unchanged and never relaxed. Recognizes the Kirby Effect: the strict split encoded a model-limitation assumption that becomes dead weight as models improve; revisit when a stronger model arrives.
- **harness-engineering** skill gains a "Right-size, don't overengineer" stance naming the Average Answer Trap and the Kirby Effect, with the O'Reilly article added to References.
- `AGENTS.md` (also the global `CLAUDE.md`) gains a **scope guard**: it is coding-agent doctrine and should not be auto-applied to non-coding or low-complexity jobs (support, sales, Q&A). Points at the right-sizing map.

## [2.4.0] - 2026-07-23

### Changed
- Tightened the comment policy across the prompt surface to address user reports that the agent added too many source comments. New default posture: **comments are the exception, not the rule** -- add one only when a clearer name or named helper cannot convey the *why* (a non-obvious constraint, invariant, external contract, or historical gotcha); prefer fixing clarity over annotating it. Propagated to the `coder` agent Hard Rules (new "Concise comments" rule), `AGENTS.md` Hard Constraints (new rule), `effective-code-craft` skill §3 "Code for Reading" (default-no stance, "can a name/helper make this self-evident?" decision test, "never annotate the obvious" bullet) and its smell table (strengthened "comment that restates the code" row + new "over-commenting" row), and `review-phase` readability lens (flag restating/obvious/narrating comments and over-commenting as SHOULD FIX). A reader of the source should see code that explains itself, with prose reserved for what names cannot.

## [2.3.1] - 2026-07-22

### Fixed
- Two skills (`harness-engineering`, `repo-documentation`) failed to load with "Invalid YAML frontmatter": their `description:` value was an unquoted plain scalar containing a colon-space (`: `), which strict YAML scanners reject (ScannerError) while the repo's lenient frontmatter parser silently accepted it. Both descriptions are now wrapped in double quotes (no inner quotes, so no escaping needed). The other five skills parsed fine and are unchanged.

### Added
- New prevention gate `G14_frontmatter_colon_safe` in `scripts/checks.py`: scans frontmatter across `skills/`, `commands/`, and `agents/` and FAILs on any top-level scalar value that is unquoted and contains a colon followed by whitespace (the exact class that broke the two skills). Quoted values, block scalars (`>`/`|`), and nested mapping lines are exempt. Stdlib-only (no new dependency). Gate count rises 13 -> 14; docstring, help epilog, and argparse description updated.

## [2.3.0] - 2026-07-22

### Added
- New code-craft discipline: source comments document the code, not the agent's process. Comments MUST NOT cite internal harness artifacts  -  plan/task IDs (`U1`, `T16`), decision IDs (`D5`, `D8`), spec line numbers (`spec §3`), handoff paths (`.agents/handoff/...`), or tracking tokens (`PENDING;`)  -  and must follow the project's idiomatic doc style (godoc, JSDoc, rustdoc, PyDoc, Doxygen). Propagated to the `coder` agent hard rules, the `review-phase` command readability lens, and the `effective-code-craft` skill clarity norm + smell-table row. A reader of the source must never need to know the agent's planning vocabulary to understand the code.

## [2.2.0] - 2026-07-22

### Changed
- Migrated `plan` mode (the Architect role: unit-graph decomposition, `done_cmd`, `INTENT:` gate, `canvas.md`/`state.json` ledger) from `agents/discover.md` into `agents/conductor.md`. Conductor now owns planning directly and writes planning artifacts under `.agents/plans/{slug}/`; the four `discover (plan)` delegation references in conductor.md are repointed to conductor ownership with `discover (explore)` available for deeper surface reading. `discover` now owns only explore / lookup / review. `README.md` agent table updated to match.
- `README.md` model-name examples simplified (dropped `-5`/`-4-5` version suffixes from claude-sonnet/haiku/opus examples) and References section reorganized: "Lost in the Middle" moved under a new Methodology subsection; Harness engineering canon expanded to 11 citations (adds Learn Harness Engineering lecture series, OpenAI Harness Engineering, Anthropic Effective Harnesses + Harness Design, OpenAI Codex agent loop, Anthropic Demystifying evals, LangChain, Cursor, Replit).
- `agents/conductor.md` absorbs Plan Mode (Architect role: unit-graph decomposition, `done_cmd`, `INTENT:` gate, `canvas.md`/`state.json` ledger); `agents/discover.md` narrows to explore / lookup / review (Architect role, Plan Mode section, and `plan` alias removed).
- All plugin manifests (legacy/OpenCode/Kilo, Claude Code, Cursor, Gemini) bumped to `2.2.0`.

## [2.1.0] - 2026-07-22

### Added
- Restored `go-essential` skill: language-specific operating doctrine for robust, high-performance, idiomatic Go. Ships as a core `SKILL.md` synthesizing the JetBrains 10x Commandments and goperf.dev, plus four deep-dive references under `skills/go-essential/references/` (concurrency, error-handling, networking, performance) loaded lazily via progressive disclosure.
- `agents/conductor.md`: "Outer-loop contract (loop engineering)" paragraph under the ACT phase  --  every task must satisfy the five loop-engineering requirements (goal-to-file, non-keystroke trigger, fresh context per iteration, unbypassable verification, defined stop condition).
- `AGENTS.md` §7: context engineering sharpened ("a line is signal only if the agent cannot discover it itself") and memory engineering expanded to three layers (episodic: handoff/retro; semantic: AGENTS.md/decision-log; procedural: skills/) each with a generate/store/retrieve/update/forget lifecycle.
- `skills/harness-engineering/SKILL.md`: two new citations (Tessl Patterns agentic-development-workflow; ETH Zurich "How to Build Your AGENTS.md" study quantifying the AGENTS.md budget penalty).

### Changed
- All six language-agnostic skill descriptions (`commit-message`, `effective-code-craft`, `harness-engineering`, `performance-patterns`, `repo-documentation`, `spec-driven-development`) rewritten as single-line, trigger-focused strings per the Agent Skills description-optimization guidance.
- `skills/repo-documentation/`: template files (`system.md`, `flow.md`, `adr.md`) moved into a sibling `references/` tree for progressive-disclosure consistency; cross-links inside `SKILL.md` updated to `./references/<name>.md`.
- All plugin manifests (legacy/OpenCode/Kilo, Claude Code, Cursor, Gemini) bumped to `2.1.0` and now register `go-essential`; catalog copy updated from "six" to "seven on-demand skills".

## [2.0.0] - 2026-07-22

### Added
- Integrated Fable Method THINK→ACT→PROVE→GROW loop core across router and workflows.
- Added GROW phase for self-improving harness (cataloging failure modes in retro logs, building deterministic gates).

### Changed
- Updated all agents, skills, and commands for the THINK→ACT→PROVE→GROW loop.
- Updated slash commands (`verify-phase`, `judge-phase`, `review-phase`, `refactor-phase`, `document-phase`) to reference their respective phases in the loop.
- Updated all plugin manifests (`claude`, `cursor`, `gemini`, `legacy`) to version `2.0.0` and 6 on-demand skills.

### Removed
- **Breaking:** Removed `go-essential` skill for a pure language-agnostic focus.
- Removed Go-specific smells and checklist items from commands and references.

## [1.7.1] - 2026-07-21

### Fixed
- Changed `discover` agent broad permission limit from `deny` to `ask` (`agents/discover.md`).
- Fixed typo `"pyhton3"` to `"python3"` in `discover` permissions (`agents/discover.md`).

### Changed
- Documented absolute path anchoring for `.agents/` workflows (`agents/conductor.md`).
- Added `"python3 *"` to `discover` permissions (`agents/discover.md`).

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
[1.7.1]: https://github.com/bouroo/agents/releases/tag/v1.7.1
[2.0.0]: https://github.com/bouroo/agents/releases/tag/v2.0.0
[2.1.0]: https://github.com/bouroo/agents/releases/tag/v2.1.0
[2.3.1]: https://github.com/bouroo/agents/releases/tag/v2.3.1
[2.3.0]: https://github.com/bouroo/agents/releases/tag/v2.3.0
[2.2.0]: https://github.com/bouroo/agents/releases/tag/v2.2.0
