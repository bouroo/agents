# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.10.1] - 2026-08-21

### Changed

- **Commands no longer bind a single agent in frontmatter.** All six `commands/*.md` drop `agent:`/`phase:` frontmatter: the command body describes the workflow, and the orchestrator (v3.10.0 bounded-unit delegation) picks the right agent per unit: `discover` for analysis, `worker` per bounded unit, `validator` for high-stakes verification. A single-agent binding invited handing a whole multi-step workflow to one fresh-context worker, the delegation shape behind the early-stop reports.
- **G5 tightened** (`ALLOWED_COMMAND_KEYS`): `agent` and `phase` are now unknown keys, so the single-agent binding cannot ship again. Mutation-probed.

## [3.10.0] - 2026-08-21

### Added

- **Worker `partial` verdict and `Early-stop:` return line.** A worker returning before its `done_cmd` executes now owes an `Early-stop:` line (why stopped, what completed, proposed unit split), and may return `partial` with analysis plus a unit-split proposal instead of silently grinding past its context on an oversized delegation packet. The worker also refuses oversized packets outright: a packet bundling a whole multi-step workflow is a planning failure, not a SCOPE.
- **Orchestrator bounded-unit delegation rule (planning step 4).** Delegation packets carry one unit with one `done_cmd`; multi-step workflows are split before dispatch, with `discover` doing analysis and `worker` receiving bounded units. A worker returning `partial` on an oversized packet is correct behavior.
- **Orchestrator early-return triage protocol.** Empty returns (suspect host/provider first, one minimal-probe redispatch, then stop with environment evidence), thin/`partial` returns (accept analysis, split, re-delegate), a marked-take-over rule for bounded work (never silent, never high-stakes), and a 3-thin-returns hard stop.
- **Failure class 5 (Early Return) in the convergence taxonomy**, provider-probe guidance in class 3, and two new delegation cheatsheet rows.

### Changed

- **`cmd-refactor` role split.** The workflow now runs analysis on `discover (explore)` and hands the plan to `worker` per bounded unit with its own `done_cmd` and evidence, instead of one whole-workflow delegation. Fresh-context workers handed the entire workflow stall mid-analysis.
- **Delegation-packet return schema** now enumerates per-role verdict enums plus the `Early-stop:` field.

## [3.9.5] - 2026-08-20

### Fixed

- **Delegated agents no longer die on their first model call on capability-gating hosts.** `worker.md`, `validator.md`, and `discover.md` carried `disallowedTools: Agent`, a Claude Code-only frontmatter key the v3.8.x cross-host work added on the assumption other hosts silently ignore unknown keys. They do not: on OpenCode and Kilo the agent config normalizer folds unknown top-level keys into `options`, which the provider receives as model options; the provider rejects the bogus param, the subagent emits no text and no tool use, and the task tool returns empty, so the orchestrator reports "The delegated task returned without doing any actual work." on every workflow (the orchestrator itself has no such key, which is why primaries worked and delegates did not). Removed the key from all three agents; the no-spawn rule is carried natively by `permission.task: {"*": deny}` (already present in worker/validator, added to discover, which previously had no task deny at all).
- **G4 now fails on non-portable agent frontmatter keys** (`checks.py`): a new `ALLOWED_AGENT_KEYS` set (`name`/`description`/`mode`/`color`/`permission`) makes any host-specific top-level key a hard FAIL, so this class of breakage cannot ship again. Mutation-probed: injecting `disallowedTools` into `agents/worker.md` fails G4; removing it passes.
- Corrected the `install.sh` header comment that documented the false "extra keys are ignored, so one file serves all three" claim.

## [3.9.4] - 2026-08-14

### Changed

- **Confluence: mandatory content-quality rules for endpoint pages** (page-template.md): every nested field as its own dotted-path table row (never collapsed); sample request/response are full payloads with internally consistent mock data covering every documented field; opaque raw-JSON pass-throughs stay single-row ("opaque, relayed verbatim", never fabricate sub-fields); field names verified from the source's serialization tags, not memory. SKILL.md pointer updated.
- **Confluence: instance-variant section** (page-template.md): a tenant's "BFF API Specification" page family (H2 sections with `<hr>`, `panel-info` opener, fixed-width metadata table with `rowspan` dependency rows, DD-MM-YYYY change-log rows with mention/status spans, plain wide code-block sequence diagrams instead of `plantumlcloud`, M/O/C coloring, passthrough status-code rows, per-call field-mapping tables). Rule: when extending an existing page family, match siblings rather than the canonical layout. Includes the transport note that remote-MCP html handled ~25 KB bodies without a 502 split on this instance.

## [3.9.3] - 2026-08-14

### Changed

- **Confluence: every diagram ships with its raw source in a collapsed expand.** A rendered `plantumlcloud` macro alone leaves the diagram source unrecoverable from the published page. The confluence skill now mandates the pair pattern (mirrored in [page-template](skills/confluence/references/page-template.md)): render the macro, then immediately follow it with the same PlantUML source in an `expand > code` block titled "Raw sequence diagram source" (decode the macro's `data` param to obtain the source). Two forms: remote-MCP (`html`) emits `<details><summary>` wrapping an HTML-escaped `<pre><code class="language-none">` block (arrows `->`/`-->` contain `>` and must be escaped); stdio-bridge (`storage`) emits `expand_macro(...)` wrapping `code_macro(source, language="none")`.

## [3.9.2] - 2026-08-14

### Changed

- **Doctrine: fewest-round-trips principle added to AGENTS.md (§4).** The loop intro now states that a model round-trip is the expensive unit and a tool result inside one turn is cheap, so a task should become one runtime-managed command graph (independent reads, searches, and calls dispatched together) so deterministic execution continues without another model round-trip. Tightened the §1 right-sizing blockquote and two §11 nav lines; removed a §9-duplicate sentence from §2. Net smaller while gaining the rule. All 18 gates pass.

## [3.9.1] - 2026-08-14

### Fixed

- **Claude Code now receives the `agents/` surface.** A stale pre-3.4.2 decision kept `surfaces.agents: false` for claude in `registries/hosts.json`, so `install claude` linked only doctrine/skills/commands/references and skipped `~/.claude/agents/`. The exclusion was made when the opencode-native agent frontmatter (`mode`/`color`/`permission`) conflicted with Claude's subagent format. After the v3.8.0-v3.9.0 cross-host compatibility work, the agent frontmatter is now a superset each host reads only its own keys from: `name`/`description`/`disallowedTools` are Claude-native; `mode`/`permission` are unknown keys Claude ignores. Re-enabled the surface (`agents: true`, `agents_path: "agents"`).
  - Removed the stale `agents-legacy` unlink in `install.sh` (both install and uninstall branches) that would have immediately unlinked `~/.claude/agents` after linking it.
  - Updated the install.sh header comment that documented the exclusion.
  - README line179 already claimed Claude Code compatibility; now the code matches.

## [3.9.0] - 2026-08-14

### Changed

- **Layout: `references/` reorganized into domain-named subtrees.** Agent depth docs moved from `references/<role>/` to `references/agents/<role>/`; command depth docs moved out of `commands/cmd-<name>/references/` into `references/workflows/cmd-<name>/`. This consolidates all progressive-disclosure depth under one `references/` tree with a clear domain split: `agents/` for per-role doctrine, `workflows/` for per-command protocol.
  - **8 files moved** via `git mv` (preserving history): 5 agent refs (orchestrator x2, worker, validator, discover) and 3 command refs (cmd-document/bootstrap, cmd-judge/judge-protocol, cmd-refactor/refactor-checklist).
  - **Every cross-reference updated**: 8 links in `agents/*.md` and `commands/*.md`, plus 9 internal links in the moved files themselves (agent refs moved one level deeper, so `../../` links needed an extra `../`).
  - **install.sh gate decoupled**: the `references/` symlink was gated on `surfaces.agents: true` only. Since command depth docs now live in `references/`, the gate fires for `surfaces.agents OR surfaces.commands`. Verified via dry-run: all command-capable hosts now get `references/`; skills-only hosts correctly skip it.
  - README tree diagram updated. No doctrine change.

- **Cross-host compatibility verified and fixed for OpenCode, Kilo Code, and Claude Code.** Tested all three target hosts against their official documentation; found and fixed three frontmatter conflicts:
  - **`tools:` replaced with `disallowedTools: Agent`.** The v3.8.0 `tools:` field (comma-separated string) was valid for Claude Code but deprecated-as-object in OpenCode, where a string value would be misinterpreted. Replaced with `disallowedTools: Agent` (Claude Code's deny-list syntax; an unknown key silently ignored by OpenCode/Kilo). The `permission.task: {"*": "deny"}` block already covers the same constraint for capability-gating hosts.
  - **Invalid `list` permission key removed.** OpenCode's permission vocabulary (`/docs/permissions`) and Kilo's custom-modes doc both confirm `list` is not a valid key. Removed from all four agents. Remaining keys (`read`, `edit`, `glob`, `grep`, `bash`, `task`, `webfetch`, `websearch`, `lsp`, `todowrite`) are verified valid across both hosts.
  - **`color` field kept as hex.** OpenCode and Kilo both accept hex colors; Claude Code accepts only named colors. Hex is correct for the two agents-surface hosts; Claude does not receive the agents surface, so the field is cosmetic there.

### Added

- **G4 permission-key gate.** `ALLOWED_AGENT_PERM_KEYS` in `scripts/checks.py` updated to the union of OpenCode + Kilo permission vocabularies (sourced from their official docs), and wired into the G4 gate so future drift toward invalid keys fails CI.

## [3.8.1] - 2026-08-14

### Changed

- **Commands and skills rewritten with the batch discipline.** Extended the Tura-informed treatment (v3.8.0 applied it to the four agents) across all six phase commands and all ten skills:
  - **Goal-backward + batch, per command.** Every phase command (`refactor`, `verify`, `review`, `judge`, `openapi`, `document`) now opens with a compact "How to work (fewest round-trips)" note: define done backward (from the Success-metrics gate), then batch the reads/edits/verify into one pass. A round-trip is the expensive unit; an in-turn tool result is cheap.
  - **Skills tightened.** Prose compressed in every SKILL.md; the batch principle folded into skills that drive sequential work (`code-craft`, `harness-engineering`, `spec-driven-development`). Verified/pinned facts preserved exactly (OpenAPI 3.2.0 schema URL, Go version features, Confluence MCP surface and PlantUML compression algorithm).
  - **Net static-token reduction** across commands + skills combined, despite adding the new discipline, with per-file trimming offsetting the added sections. The real token win is at execution time: fewer model round-trips per command run.
- No doctrine change; no frontmatter schema change; all 18 gates pass.

## [3.8.0] - 2026-08-14

### Changed

- **Agent prompts rewritten for fewer tokens and better results (Tura-informed).** Analyzed the Tura runtime harness (its runtime-managed command graph and backward-reasoning model) and folded the two transferable techniques into all four squad agents:
  - **Batch, do not ReAct.** Each executor now opens with a "How to work (fewest round-trips)" discipline: gather every read in one pass, then edit, then run the toolchain once, instead of paying a model round-trip per tool call. A round-trip is the expensive unit; a tool result inside one turn is cheap.
  - **Goal backward.** Start from DONE (the `done_cmd`), reconstruct the current state, name the gap, then act. Replaces open-ended "figure it out" framing with a deterministic reasoning order.
  - **Stripped dead weight.** Removed unresolvable relative-link reference lists (4-6 per agent) and compressed verbose prose into high-signal imperatives. Subagents do not inherit AGENTS.md, so each body stays self-contained; only the truly redundant restatement was cut.
  - Net system-prompt body reduction: ~17% overall (worker -23%, validator -17%, orchestrator -19%, discover -9%), measured after frontmatter, despite adding the new reasoning discipline.
- **Cross-host compatibility: Claude Code tool allowlists.** Added a `tools:` field (Read/Edit/Write/Glob/Grep/Bash/WebFetch/WebSearch/TodoWrite, omitting the delegation tool) to the three subagents so they work as-is when copied into a `.claude/agents/` directory. Capability-gating hosts continue to use the existing `permission:` block; allowlist hosts use `tools:`. The orchestrator (primary) keeps full tool access including delegation. No host-binding tokens introduced; G17 stays green.

### Fixed

- Frontmatter comments in the subagents no longer name specific hosts; the core stays host-agnostic per G17.

## [3.7.0] - 2026-08-13

### Changed

- **Layout migration: agent depth docs out of `agents/`.** Cursor's plugin editor recursively auto-discovers `agents/` and was treating each `agents/<role>/references/*.md` depth doc as a standalone agent (5 spurious picker entries). Moved them to a sibling `references/<role>/<doc>.md` tree; cross-refs in `agents/*.md` and `commands/cmd-judge*` rewritten; `adapters/install.sh` extended to symlink `references/` alongside `agents/` for hosts with `surfaces.agents: true` (opencode, kilo). No doctrine change.
- **Prose de-dash sweep.** Removed AI-style ASCII `--` separators across the doctrine (~600 sites in 59 files) for a cleaner read. Where removal would fuse two clauses or invert meaning, minimal ASCII punctuation (`.`, `;`, `:`, `,`) was restored in place; literal `--` tokens (CLI flags like `--force`, `--help`, numeric ranges like `80-90%`) are untouched. No behavior change; all 18 gates pass.

## [3.6.0] - 2026-08-13

### Changed

- **Squad re-init: autonomous four-role harness (Tura-informed).** Three roles restructured into four: `conductor` -> **`orchestrator`** (primary; plans, delegates, runs the completion audit, converges, GROWs), `coder` -> **`worker`** (mutating implement/fix/verify), and a new **`validator`** (independent adversarial verifier). `discover` unchanged. Removes the self-judge conflict of interest: the worker that wrote the code no longer judges its own high-stakes "done"; `worker.judge` mode is removed and `cmd-judge` now dispatches the validator.

### Added

- **`validator` agent** (`agents/validator.md` + depth doc): `verify`/`judge` modes, the fraud table, a probe-only edit constraint (every mutation probe reverted), and a verdict handoff schema.
- **Orchestrator completion-audit doctrine**: prompt-to-artifact checklist (never accept proxy signals; treat uncertainty as not-done), autonomy/persistence, and a host-agnostic capability/effort dial.

### Rewired

- Every cross-reference updated across `AGENTS.md` (§3/§4/§11), `registries/modules.json`, `README.md`, all six commands, `harness-engineering` (SKILL + composition-patterns), the install/manifest scripts, the `eval/s5` scenario, and regenerated `adapters/manifests/**`. `git mv` preserved history for the moved reference files.

## [3.5.2] - 2026-08-11

### Changed

- **`confluence` skill: diagram doctrine corrected.** Diagrams default to **PlantUML** (the only tech reproducible from page storage XML); the native `mermaid` macro is not installed on every instance, and `mermaid-cloud` stores its source out-of-band (UI-insert-only). Mermaid is now manual-only.
- **`page_template.py` refactored**: metadata table emits bold `<th>` label rows + centered `<td>` values (no fixed pixel widths), generalized off the specific tenant to generic defaults; new helpers added.
- **Tenant scrub**: `mcp_bridge.py` example `page_id` changed to a placeholder.

### Fixed

- Em/en-dash characters in three `confluence` references replaced with `--` to satisfy `G6_no_dash_chars`.

## [3.5.1] - 2026-08-11

### Fixed

- **Cross-reference drift sweep.** Stale `§N` pointers corrected across `harness-engineering` and `go-essential` references, and two off-by-one `AGENTS.md` references (`§6` -> `§7` for the hard verify bound; `§7` -> `§8` for context); a dangling "Appendix A" removed.
- **Stale "Self-Execution" failure class removed** from the orchestrator convergence doc  it contradicted the dialed-choice stance and was the one Kirby-Effect dead-weight cut from the doctrine audit.

## [3.5.0] - 2026-08-11

Doctrine rewrite integrating six source methodologies (Fable think/act/prove, O'Reilly "stop overengineering your agent harness", KiloCode AGENTS.md standard + context-condensing guide, JetBrains 10x commandments, goperf.dev) without bloat; the skills already owned ~90% of the mechanism.

### Changed

- **AGENTS.md rewritten** (stable §0-§11 numbering preserved, no cross-reference breaks):
  - **Front-loaded autonomy (§2):** new Ask-Shape intake (`Question` / `Plan-first` / `Task`) and a Trivial Path (one file, <10 lines -> fix, check, report; skip ceremony).
  - **Fit gate (§2):** "where does the answer live?"  reachable source -> read; unknown -> search; only-own-inference -> STOP and ask (never fabricate); recurring specialized procedure -> make a skill.
  - **Self-aware anti-overengineering (preamble):** the Kirby Effect, the two-axis right-sizing, and the Reduce/Offload/Isolate toolkit. The doctrine now polices its own weight.
  - **GROW gains a prune mechanism (§4, §10):** at each model upgrade or after a control never fires, re-audit and cut dead-weight controls  self-improving is now executable (the harness can shrink).
  - **All three Fable hard bounds present (§7):** the third ("if you cannot name one executable check confirming DONE, stop and ask") was missing and is added alongside the 3-cycle bound.
  - **§5/§9 dedup** (code-craft hard rules have one home each); **§6 de-Go-ified** (cut language-specific jargon and an unsourced statistic from the agnostic core); **AUTH gate enacted inline (§4)**.

### Fixed

- Dangling judge fraud-rubric references; stale `effective-code-craft` display names (renamed to `code-craft` in 3.0.0); wrong code-craft section names; `cmd-refactor` unconditionally profiling; `cmd-openapi` validate loop lacking the 3-cycle bound; `cmd-review` trivial-diff escape.

### Added

- **Reduce / Offload / Isolate section** in the right-sizing reference.

## [3.4.2] - 2026-08-10

Install fix: claude no longer receives the `agents/` surface. The opencode-native agent frontmatter (`mode`/`color`/`permission`) conflicts with claude's subagent format (`name`/`description`/`tools`/`model`); claude still gets `AGENTS.md`, `skills/`, and `commands/`. `install.sh` also removes any stale `~/.claude/agents` symlink left by a pre-3.4.2 install.

## [3.4.1] - 2026-08-08

Backwards-compatible doctrine refinement: reach for an atomic value before a mutex whenever the guarded state stands alone (single counter/flag/pointer = atomic, not mutex; mutex justified only when the critical section spans multiple fields). Surfaced in the language-agnostic `performance-patterns` and `go-essential` §4 (atomic-over-mutex pointer line, code swap, common-mistakes row, pre-spawn checklist).

## [3.4.0] - 2026-08-07

Backwards-compatible release: agents reach for built-in file/search/edit tools before bash. The rule is a feedforward guide (AGENTS.md §2): `cat`/`head`/`tail` -> Read, `grep`/`rg` -> Grep, `find`/`ls` -> Glob, scoped edit -> Edit, new file -> Write; bash reserved for genuine commands (test, build, git, installer, pipeline). New *tool-routing-drift* row in the GROW failure-mode map; permission-block notes.

## [3.3.0] - 2026-08-07

The six phase commands renamed to a `cmd-` prefix and bundled with their reference files (`commands/cmd-<name>/`). Groups commands by surface, matches the exposed invocation names, and unifies the layout with the native-compatibility table. Cross-references updated; the manifest generator and `G5` read disk filenames, so no gate logic changed.

### Fixed

- `memory-engineering` and `openapi-spec` reference paths refreshed; `s2-fraudulent-work` and `eval/RESULTS.md` updated to renamed commands.

## [3.2.0] - 2026-08-07

Backwards-compatible feature release: commands become extensible through the portable `$ARGUMENTS` channel (the one token every host substitutes), with a small closed `key=value` grammar per command and `argument-hint` autocomplete where a host shows it. New **`G18_portable_command_inputs`** gate makes the cross-host contract deterministic; a command-inputs portability matrix added to the ACI reference.

## [3.1.0] - 2026-08-06

First follow-on stable release: three new host adapters (Hermes, OpenClaw, Pi) join `registries/hosts.json`. Backwards-compatible  the host list is data, so existing installs are unaffected.

## [3.0.0-beta.3] - 2026-08-06

Third beta of the v3 reimplementation, continuing the natural-delegation arc (beta-numbered only on the git tag and here; `VERSION` and manifests stay `3.0.0`).

### Changed

- **Squad role lock collapsed; delegation is now natural.** The enforced mutating-vs-read-only boundary is removed; roles become soft specialization defaults  conductor/discover can edit and run the toolchain directly when that is the natural path. Delegation remains the default for non-trivial or parallel work; it is a dialed choice, not a mandate. The universal hard constraints, executable evidence, and the AUTH/decide-don't-ask gate on outward actions are unchanged.
- **Delegation dials widened for independent work** (WIP=1 now scopes to the active decision thread; independent units may fan out; PROVE routes review/judge by the right-sizing dial).
- **AGENTS.md §3 de-linked** (per-agent bullets removed from the squad header; the three agent files remain the definition layer, linked from §11).

### Added

- **Eval scenario `s5-natural-delegation`** (seed; `passed: null` per the honesty rule).

## [3.0.0] - 2026-08-06

A ground-up reimplementation into an architecture **completely agnostic** of languages, agent frameworks, and host tools, while shipping every artifact in each popular harness's **native** discovery format. The coder-squad doctrine (governance router + conductor/coder/discover squad + THINK-ACT-PROVE-GROW loop + skills + eval honesty layer) is preserved and concisely re-implemented; only its *home* and *form* change. **Breaking** for filesystem consumers; the doctrine is continuous with v2. Compatibility verified against opencode, Claude Code, kilo, skills.md, and agents.md schemas. Supersedes the beta.1-beta.3 pre-releases (the natural-delegation arc).

### Added

- **Native harness compatibility.** Agents are flat `agents/<name>.md`; commands are flat `commands/<name>.md` with an `agent` binding; skills are nested `skills/<name>/SKILL.md` (Agent Skills standard); `AGENTS.md` is a root Markdown file (agents.md standard).
- **Cross-host agent frontmatter.** Each agent carries `name` + `description` + `mode` + `permission` (per-capability allow/ask/deny). Roles are soft specialization defaults, not a tool-gated boundary. The `tools:` field was dropped (opencode treats it as a deprecated boolean and rejected the comma-string form).
- **Host-agnostic core.** `AGENTS.md`, `agents/*.md`, `commands/*.md`, and the seven core skills contain no host-binding tokens; new **`G17_agnostic_core`** gate fails on any leak (domain adapters excluded).
- **Registries (single source of truth).** `registries/modules.json` (modules) + `registries/hosts.json` (host adapters). Adding a host is now an entry in a file, not a code change.
- **Abstract host-adapter installer.** `adapters/install.sh` (+ `install.ps1`, `link.sh` shim) read `registries/hosts.json`; no hardcoded tool list in the core.
- **Three-tier customization resolver.** `scripts/resolve-customization.py` merges base -> team -> user layers (bmad merge rules); optional, with a documented manual fallback.
- **New gates** `G16_registries_parse` + `G17_agnostic_core`.
- **Endpoint-documentation (API) doc type** (`document` command + `repo-documentation` skill: one endpoint per file at `docs/api/<service>/`).
- **Mermaid diagram support in the confluence adapter** (native macro reference + markdown-to-storage converter).

### Changed

- **Repository layout.** Flat `agents/` and `commands/`; nested `skills/`; `AGENTS.md` rewritten as a governance persona + squad navigator (under the G9 budget).
- **Skill relocations.** `effective-code-craft` -> `code-craft`; the three language/tool skills are top-level siblings so every one-level skill scanner discovers them.
- **Manifests relocated + generated.** `adapters/manifests/<host>/`; `scripts/gen-manifests.py` writes all host manifests from `VERSION` + inventory + registries; **`G15_manifests_generated`** fails on hand-edit drift. Confluence adapter tenant scrubbed to placeholders.

### Removed

- v2 flat agent files, `commands/`, root installers (moved to `adapters/`), and `.agents/plugins/` (moved to `adapters/manifests/`). v2 content preserved in git history; the config repo's v2-era `docs/` tree removed (this repo documents itself via `AGENTS.md` + skills).

## [2.11.0] - 2026-08-04

### Added

- **`confluence` skill.** Durable operating doctrine for the `mcp-atlassian` server: surface/register MCP tools when they do not load mid-session (a `mcp_bridge.py` stdio bridge calls the server's real tools), resolve `/x/<id>` shortlinks, and author pages so code blocks and PlantUML diagrams render native storage format, never markdown. Ships four references + `page_template.py`.

## [2.10.0] - 2026-08-04

### Changed

- **Comment policy is now a strict default, not advice.** `code-craft` §3 replaces loose bullets with a three-gate test a comment must clear (naming exhausted; states *why* not *what*; the *why* not derivable by a fluent reader). Banner dividers and tracker-duplicating `// TODO` named as noise.
- **Doc comments must follow the language's official convention strictly**, not freeform prose (per-language table: godoc, TSDoc/JSDoc, rustdoc, docstring, Javadoc/Doxygen).

### Added

- **godoc rule in `go-essential`** (every exported identifier takes a `//` comment opening with the identifier name).
- **Doc-convention linting in `verify-phase`** (runs the language's doc linter so malformed doc comments fail computationally).

## [2.9.1] - 2026-08-03

### Fixed

- **`validate-openapi.mjs` is modeline-compatible.** The validator resolves the OpenAPI meta-schema from a yaml-language-server modeline comment (single source of truth shared with editors); new `parseModeline()` reads standard + IntelliJ forms, with a legacy root-`$ref` fallback. Finished a migration left half-done (template, validator, and SKILL had documented three different directive forms).
- Template modeline corrected to a single correct line; `SKILL.md` directive section synced.

## [2.9.0] - 2026-08-03

### Added

- **Agent-Computer Interface (ACI) and composition-patterns references** under `harness-engineering`: ACI covers *designing* tools/slash commands/MCPs (self-contained contracts, non-overlapping responsibilities, poka-yoke arguments, token-efficient returns); composition-patterns is the delegation topology menu (chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer)  pick the smallest topology the job can hold.
- **Pointers wired and context loop calibrated** in `AGENTS.md` (tool-design routing §2, topology §3, "calibrate, don't preload" §7), agents, skills, and README.

## [2.8.0] - 2026-08-02

### Changed

- **Cross-reference drift closed** across the doctrine (every `§N` pointer to `harness-engineering` verified and corrected; a correctness fix, not style).
- **AGENTS.md rewritten to surface under-used source knowledge** (GOAL/CONTEXT/CONSTRAINTS/DONE_WHEN frame; guides-vs-sensors; computational-vs-inferential controls; right-sizing axes; Decide/Report micro-steps; instruction-vs-learning memory split) while staying a lean router.
- **Source provenance consolidated into the README**  every external `## References`/`## Source Attribution` section removed from doctrine/skill files so the README's categorized `## References` is the single home for source links.
- **Concision pass: single-owner the duplicated norms**  AGENTS.md pointers are brief "load when X" hints; role files stop re-defining shared norms.

## [2.7.0] - 2026-08-01

### Added

- **z.ai best-practice gaps closed.** Conductor delegation packet gains a `CONSTRAINTS` field (non-negotiable rules a cold subagent cannot derive, distinct from `SPEC`); `AGENTS.md` §7 gains session-boundary bullets (one task per conversation; fresh sessions for branch work).
- **`memory-engineering` skill + Instruction/Learning separation.** Core rule  **Instruction ≠ Learning memory**: agent-learned corrections must never be written into instruction files (they drift behavior silently and resist removal). Adds the Type x Scope grid, the retrieve/construct/update/forget workflow, file hygiene, and a `.agents/memory/` fallback for harnesses with no native memory.
- **Generated manifests from a single source.** `scripts/gen-manifests.py` (stdlib-only) renders all seven host manifests from the on-disk inventory + a root `VERSION` file; new **`G15_manifests_generated`** gate prevents hand-edit drift.

### Changed

- **Single validator.** `scripts/validate-agents.sh` (a 258-line bash reimplementation) is now an 11-line shim that `exec`s `checks.py`; the gate count is no longer hand-maintained in prose (derived via `--help`).

## [2.6.0] - 2026-07-30

### Added

- **`openapi-spec` skill + `openapi-phase` command.** Generate or repair an OpenAPI 3.2 contract into `docs/openapi.yaml` and validate against the canonical OAS meta-schema. Carries verified external facts (OpenAPI 3.2.0 latest stable; the meta-schema sets `unevaluatedProperties: false` at root) and documents the root-key directive trap. Auto-detects introspect vs interview mode; ships a copy-in template + Ajv validator.

### Fixed

- Claude plugin manifest `skills` array listed only six of seven skills (`go-essential` absent); added.

## [2.5.1] - 2026-07-27

### Fixed

- **`Tool call not found` resolved.** Operating doctrine previously routed work by **host-specific tool names**; when the same `AGENTS.md` loaded into a different host, the agent emitted calls to tools that did not exist. All such instruction text is now **capability-based** ("open and read the file", "search by string", "web search or fetch"), not name-based, with a defensive clause: *only call tools that actually exist in your runtime*. `permission:` frontmatter blocks are unchanged (host config, never cause a model tool call).

## [2.5.0] - 2026-07-24

### Added

- **right-sizing reference** (`harness-engineering/references/right-sizing.md`): two-axis complexity map (Action x Context) + a control dial for verification depth, mutation testing, adversarial judging, GROW retro.

### Changed

- **Verification is now complexity-proportional**, not universal. L1 (static) every change; L2 (runtime) when the change has runtime behavior; L3 (e2e) when it crosses a boundary. Executable evidence is still never optional  the dial chooses layers, never the standard.
- **Conductor planner/actor split softened** with a trivial-work escape hatch for Low/Low units (typo, rename, one-line fix)  self-verify and WIP=1 preserved; the safety floor unchanged.
- `harness-engineering` gains a "Right-size, don't overengineer" stance; `AGENTS.md` gains a scope guard (coding-agent doctrine, not for non-coding/low-complexity jobs).

## [2.4.0] - 2026-07-23

### Changed

- **Comment policy tightened.** New default posture: **comments are the exception, not the rule**  add one only when a clearer name/helper cannot convey the *why*. Propagated to coder Hard Rules, AGENTS.md Hard Constraints, `code-craft` §3 + smell table, and `review-phase`.

## [2.3.1] - 2026-07-22

### Fixed

- **Invalid YAML frontmatter** in two skills (`harness-engineering`, `repo-documentation`): unquoted plain-scalar `description:` containing a colon-space that strict scanners reject. Both wrapped in double quotes.

### Added

- **`G14_frontmatter_colon_safe`** gate in `scripts/checks.py`: FAILs on any unquoted top-level scalar value containing a colon-space. Gate count 13 -> 14.

## [2.3.0] - 2026-07-22

### Added

- **code-craft discipline: comments document the code, not the agent's process.** Comments MUST NOT cite internal harness artifacts  plan/task IDs, decision IDs, spec line numbers, handoff paths, tracking tokens  and must follow the project's idiomatic doc style. A reader of the source must never need the agent's planning vocabulary to understand the code.

## [2.2.0] - 2026-07-22

### Changed

- **Migrated plan mode** (Architect role: unit-graph decomposition, `done_cmd`, `INTENT:` gate, ledger) from `discover` into `conductor`; `discover` narrows to explore/lookup/review. README agent table updated; all manifests bumped to 2.2.0.
- README model-name examples simplified (dropped version suffixes); References section reorganized with expanded harness-engineering canon.

## [2.1.0] - 2026-07-22

### Added

- `conductor.md`: "Outer-loop contract (loop engineering)"  every task satisfies the five loop-engineering requirements (goal-to-file, non-keystroke trigger, fresh context, unbypassable verification, defined stop).
- `AGENTS.md` §7: context engineering sharpened ("a line is signal only if the agent cannot discover it itself") and memory engineering expanded to three layers.
- `harness-engineering`: two new citations (Tessl Patterns; ETH Zurich AGENTS.md budget study).

### Changed

- All six skill descriptions rewritten as single-line, trigger-focused strings.
- `repo-documentation` templates moved into a sibling `references/` tree for progressive-disclosure consistency.
- Manifests bumped to 2.1.0 and now register `go-essential`.

## [2.0.0] - 2026-07-22

### Added

- Integrated Fable Method THINK→ACT→PROVE→GROW loop core across router and workflows.
- GROW phase for a self-improving harness (cataloging failure modes in retro logs, building deterministic gates).

### Changed

- Updated all agents, skills, and commands for the loop; slash commands renamed to reference their phases; all manifests bumped to 2.0.0.

### Removed

- **Breaking:** Removed `go-essential` skill for a pure language-agnostic focus; removed Go-specific smells/checklist items from commands and references.

## [1.7.1] - 2026-07-21

### Fixed

- `discover` broad permission limit changed `deny` -> `ask`; fixed `"pyhton3"` -> `"python3"` typo.

### Changed

- Documented absolute path anchoring for `.agents/` workflows; added `"python3 *"` to `discover` permissions.

## [1.7.0] - 2026-07-19

### Added

- `lsp` permission on `coder`, `conductor`, `discover` agents (go-to-definition, find-references, hover, diagnostics) when the host exposes an LSP tool.

### Changed

- Permission blocks rewritten from explicit allow-list + fallback to a single broad allow followed by specific destructive-command denials (last-matching-rule-wins under Kilo)  fewer prompts, same destructive guardrails.
- `conductor` edit policy moved to `allow` with `external_directory: ask` enforcing the worktree boundary.
- README config example replaced placeholders with concrete model IDs + `coder`/`discover` subagent entries. Manifests bumped to 1.7.0.

## [1.6.1] - 2026-07-19

### Added

- **`coder` and `discover` named subagents.** The eight-role squad consolidates into two agent files: `coder` (mutates source, runs the toolchain across implement/fix/verify/judge) and `discover` (read-only across plan/explore/lookup/review). Each ships its own `permission:` block (the "write/edit permission denied" inheritance fix).

### Changed

- `conductor.md` routing rewritten around the two named members; default `edit` policy tightened `ask` -> `deny` with explicit allow-rules only for `.agents/handoff/**` and `.agents/plans/**`; steps raised 60 -> 120. Manifests bumped to 1.6.1.

## [1.6.0] - 2026-07-19

### Added

- **skills.sh / Claude Code / Cursor / Gemini CLI marketplace compatibility.** New plugin/marketplace manifests per each harness's official schema so `npx skills add bouroo/agents` discovers skills across 30+ runtimes; `gemini-extension.json` at repo root for Gemini/Antigravity CLI.
- **Consolidated manifest source-of-truth** under `.agents/plugins/<tool>/`, surfaced at tool-discovery paths via symlinks.
- **Gates G10-G13** in `scripts/checks.py` (manifest validation + symlink invariant). Gate count 9 -> 13.
- **Per-skill `## References` sections** applying the progressive-disclosure best-practice ("load when X" hints instead of bare links).
- skills.sh badge and Agent-Skills spec links in README.

### Changed

- `link.sh` is now a thin backward-compat shim (54 lines, down from 195) that `exec`s `install.sh`; all cross-reference sections rewritten with "load when" hints; README rewritten (Quick Start split into skills.sh CLI / Cursor / Gemini / symlink installer paths). Manifests bumped to 1.6.0.

## [1.5.0] - 2026-07-18

### Added

- **`go-essential` skill:** production-readiness rules for Go (style, naming, error handling, safety, concurrency, context, testing, performance, safe refactoring). Ships as a core SKILL.md plus fourteen deep-dive references.

## [1.4.0] - 2026-07-17

### Added

- `judge-phase` registered in `plugin.json` and the marketplace catalog (shipped in 1.3.0 but missing from both manifests); Mermaid diagram requirement added to `repo-documentation` flow docs.

### Changed

- `AGENTS.md` slimmed (132 -> 114 lines); rhetorical scaffolding trimmed, hard constraints + artifact-gate vocabulary retained; "spec, plan, implement, verify" rhythm replaced by the fable-method `think/act/prove`.
- `conductor.md` re-cut around think/act/prove/grow (direct `edit` of `AGENTS.md` removed); `harness-engineering` slimmed (431 lines removed); `spec-driven-development` REASONS canvas reordered (distinct Safeguards + Signoff); absolute "always" claims softened to scope-bound guidance. Manifests bumped to 1.5.0.

### Fixed

- `marketplace.json` stale version (`1.3.0` while `plugin.json` read `2.0.0`); stale "four slash commands" description; em-dash characters tripping G6.

## [1.3.0] - 2026-07-16

### Added

- **Forced artifact-gate report lines (INTENT/TWINS/AUTH/PENDING)** in AGENTS.md and `code-craft`: a mechanical sweep owed at decision points; conductor convergence blocks on a clean sweep.
- Two adversarial verification eval scenarios (`s3-artifact-gate`, `s4-twin-check`); `harness-engineering` failure-mode rows (verification theater, false completion, retry thrash, unprompted fixing, debris-left-behind).

### Changed

- `judge-phase` and `verify-phase` enforce the artifact-gate sweep; phase command docs unified on the gate vocabulary.

## [1.2.0] - 2026-07-16

### Added

- **`judge-phase` command**: adversarial verification of finished work  treats a "done" report as claims, re-runs verifications, hunts the classic frauds, delivers a VERIFIED / VERIFIED WITH CAVEATS / REFUTED verdict (distinct from the trusting `review-phase`).
- `harness-engineering` Judge stance + fraud-table; `code-craft` "Classify the Ask" triviality gate; "Analysis paralysis" failure-mode row; `s2-fraudulent-work` seed scenario.

### Changed

- Conductor PROVE phase now includes the Judge role alongside Tester and Reviewer; README command table registers `judge-phase`; manifests bumped 1.0.0 -> 1.2.0.

### Fixed

- CHANGELOG en-dash broke G6 in CI; replaced with ASCII hyphen.

## [1.1.0] - 2026-07-16

### Added

- Plugin packaging (`plugin.json`, `marketplace.json`) and cross-platform installers (`install.sh` POSIX, `install.ps1` Windows).
- Skill-name length constraint (1-64 chars) validation gate; adversarial judge-phase in the conductor agent; CI workflow running validators on push/PR to `main`/`develop`; Kilo/Opencode config example in README.

### Changed

- Decision-making framework refined (removed the single-question constraint for ambiguous high-impact decisions); context-compaction and documentation workflows defined in agent doctrine; conductor "Clock-in" mandates ledger bootstrapping; `.agents/` location clarified and ignored.

## [1.0.1] - 2026-07-15

### Added

- CI workflow running `scripts/checks.py` and `scripts/validate-agents.sh` on every push/PR to `main` and `develop`.
- `scripts/validate-agents.sh`: skill-name length constraint gate; Kilo/Opencode configuration example in README; `document-phase` command and `repo-documentation` module registered.

### Changed

- Conductor "Clock-in" mandates a "Bootstrap the ledger" step (`mkdir -p .agents/*`) before any file write; context-management and compaction-resilience guidance added to AGENTS.md; `.gitignore` excludes `.agents/`.

## [1.0.0] - 2026-07-14

### Added

- Plugin packaging (`plugin.json`, `marketplace.json`) for cross-tool installation; cross-platform installers (`install.sh` POSIX, `install.ps1` Windows); `scripts/checks.py`: 9-gate deterministic validator (manifests, frontmatter, cross-references, em/en-dash discipline, AGENTS.md budget).

### Changed

- Conductor agent reframed as Kilo primary mode with think/act/prove phase rhythm; README de-coupled from tool-specific model names (generic placeholders).
