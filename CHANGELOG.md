# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Pre-4.0 entries were retired in the v4 fresh start; the full history lives in git
tags and log (`v1.0.0` through `v3.11.0`).

## [6.0.0-beta.1] - 2026-09-12

First published form of the v6 lifecycle foundation. Tagged as a **beta**: the
publish flows that ship the release are new this cycle and have not yet run
end-to-end in CI, so the tag is marked prerelease and does not become the
"latest" download for consumers until a stable tag is cut.

### Added

- **`scripts/release_notes.py`**: prints one version's CHANGELOG section
  verbatim, so a release body is the committed bytes rather than a
  paraphrase. Exits non-zero when a tag has no matching section, failing the
  release instead of publishing an empty body.
- **`.github/workflows/release.yml`**: on a pushed `v<major>.<minor>.<patch>`
  tag, re-runs the gates on the tagged commit, extracts the release body, and
  publishes the GitHub Release. A tag carrying a prerelease suffix (`-beta.1`,
  `-rc.1`) is marked `prerelease: true` and never becomes "latest"; promoting a
  beta to stable is a new tag on the merge commit, never a re-point of the tag
  already published.
- **`skills/lifecycle/`**: the doctrine's new spine — the AI-native delivery
  lifecycle. Seven stages (intent, spec, plan, build, test, release, operate),
  the artifact each commits, its exit check, and the seven **seats** that own
  them (Originator, Steward, Architect, Implementer, Verifier, Approver,
  Operator). The loop is explicitly non-linear: `Test -> Build` is the canonical
  review back-edge and `Operate -> Intent` reopens the lifecycle. Two
  constraints never bend however the seats collapse — the Implementer never
  approves its own work, and the Verifier is independent of what it judges.
  Org-specific roles collapse into the seven (release manager -> Approver,
  auditor -> Verifier, on-call -> Operator). Distilled from Anthropic's
  *AI-native SDLC playbook* as method; its org apparatus and host product
  mechanisms are deliberately not adopted.
- **`skills/evals/`** and **`evals/suite.json`**: continuous evals as a named
  control — a harness regression suite of realistic tasks, each a prompt plus
  objective checks, run on schedule and on any change to the manifesto, a
  skill, a hook, or the pinned model. A change that lowers the pass rate blocks
  the merge. Evals are how GROW proves an evolution helped rather than merely
  shipped.
- **`evals` gate** in `scripts/check.py`: validates that `evals/suite.json`
  exists and every eval is well-formed (non-empty id, prompt, and mechanical
  checks carrying a `cmd` and an `expect_exit`). The suite is now seven gates.

### Changed

- **`AGENTS.md`**: re-authored onto the lifecycle spine. §4 becomes **The
  Delivery Lifecycle** (stage/artifact/seat/exit-check table, the loop's
  back-edges, the seat cast, human judgment at the seams, evals as the
  process regression control); the execution graph moves to §4.2 as the engine
  that shapes work *inside* a stage. §7 gains the evals-regression rule; §11's
  map lists the three new skills. Budget raised 200 -> 250 lines; the manifesto
  is 166.
- **`skills/plan-authoring` -> `skills/artifacts`**: generalized from one
  artifact to the chain — deterministic `intent.md` and `spec.md` shapes added
  alongside `PLAN.md` and its `STATUS.md` ledger, one artifact per lifecycle
  stage. All live referrers updated (`AGENTS.md`, `README.md`, `grilling`,
  `verification`, `wayfinder`); historical CHANGELOG entries are not rewritten.
- **`skills/graph-engineering`**: reframed as the grammar of work *inside* a
  stage, composing with the lifecycle rather than being the top level;
  section references now point at §4.2.
- **Commands** re-pointed at their stages: `cmd-verify` and `cmd-review` ->
  Test, `cmd-refactor` -> Build, `cmd-document` -> Spec.
- **`README.md`**: rewritten around the lifecycle foundation; skill tree,
  execution-graph section, one-line doctrine, and the gate table updated.
- Version fields bumped to 6.0.0 across the four versioned manifests, and each
  manifest's skill list expanded from fourteen to sixteen.

### Motivation

- v5 answered *how one job runs* (the execution graph) but had no answer for
  *where a job sits in the delivery loop, what artifact it commits, or who owns
  an approval* — the foundation-level absence the SDLC playbook names. Its
  thesis, that code stopped being the bottleneck once agents could write it
  faster than humans could plan and ship around it, reorganizes the doctrine
  around a non-linear artifact-driven loop with human judgment concentrated at
  the approval seams. The other three researched sources (Bowne-Anderson's
  harness article, the flowtivity graph-engineering guide, the z.ai devpack
  best-practice page) were audited and found already distilled as of 5.7.0 or
  carrying no adoptable delta; their material stays where it is.

## [5.7.0] - 2026-09-12

### Added

- **`skills/graph-engineering/references/harness-design.md`**: the harness-design
  reference the execution-graph grammar lacked — the minimal-harness ladder
  (prompt/retrieval -> fixed workflow -> agent loop) with the walking-skeleton
  build order; the pattern catalogue (augmented LLM, prompt chaining, routing,
  parallelization, orchestrator-workers, evaluator-optimizer, agent) mapped onto
  the grammar's shapes and edges; voting vs. sectioning with the decorrelation
  caveat; tool-surface (ACI) design — document for the model, poka-yoke the
  arguments, iterate on observed misuse; scoping the tool surface; server-side
  context injection; layer attribution for failures; and the anti-framework
  stance. Distilled from Anthropic's *Building effective agents* and Hugo
  Bowne-Anderson's *Stop overengineering your agent harness*, adopted as method
  with numbers re-derived locally.

### Changed

- **`skills/graph-engineering`**: the description, three new short sections
  (enter at the least-agency rung; fan-out's two rationales; design the tool
  surface), three new common-mistake rows, and the reference linked. The agency
  ladder is named as the shape ladder viewed from the agency axis.
- **`AGENTS.md`**: §4 routes to the minimal-harness ladder — enter at the least
  agency that closes on evidence, a prompt or fixed workflow before an agent
  loop, the smallest shape before a graph; §11's graph-engineering row lists the
  new reference.
- **`skills/teamwork`**: the spawn-brief contract now scopes the worker's tool
  surface to its task — a narrower surface means less confusion, misuse, and
  injection exposure.
- **`skills/verification`**: Diagnosis attributes a failure to its layer —
  reasoning, tool interface, context, or control flow — before patching, since a
  wrong-layer fix is a symptom patch by construction.
- **`README.md`**: the skills tree lists the harness-design reference.
- Version fields bumped to 5.7.0 across the four versioned manifests.

### Motivation

- The doctrine governed how one job runs (shapes, typed edges, caps, anchors,
  cost) but said little about designing the harness that runs it. A coverage
  sweep against the two sources found the workflow-vs-agent ladder,
  voting-vs-sectioning, tool-surface (ACI) design, scoped tool access,
  server-side context injection, layer-attribution diagnosis, and the
  anti-framework stance absent, with the correlated-lens hazard present but
  voting unnamed. The reference adds the missing method without restating what
  the "Right-size, don't overengineer" banner and the Kirby Effect already
  encode — those are sharpened, not duplicated.

## [5.6.0] - 2026-09-11

### Changed

- **`AGENTS.md`**: the completion-non-authorization rule generalized to all
  destructive and outward-reaching commands, example-free — finishing a task,
  a clean tree, or a green build authorizes nothing beyond it; §3's AUTH gate
  and §10's hard constraint both state the general form, with outward steps
  named in `PENDING:` until the user approves.
- **`skills/craft`**: the AUTH gate definition carries the same generalization,
  with the concrete `PENDING: <step> - awaiting your authorization` pattern.
- Version fields bumped to 5.6.0 across the four versioned manifests.

### Motivation

- Review feedback on v5.5.0: naming `git push` alone was too narrow — the same
  completion-non-authorization logic covers every outward or irreversible step
  (pushes, releases, deletes, publishes). v5.5.0 had shipped an hour earlier
  in the same day; the generalization replaces the narrow rule before any
  dependent procedure could anchor on it.

## [5.5.0] - 2026-09-11

### Changed

- **`AGENTS.md`**: `git push` is now named as the canonical AUTH case (§3) —
  finishing a task, a clean tree, or a green build never authorizes reaching the
  remote; agents end at local commits and report. §10 gains the matching hard
  constraint: never `git push` without the user's explicit go-ahead; ending at
  local commits with the push named in `PENDING:` is a clean exit.
- **`skills/craft`**: the AUTH gate definition carries the same weave — the
  completed-task/clean-tree/green-build non-authorization and the concrete
  `PENDING: push - awaiting your authorization` pattern.

### Motivation

- Users reported agents pushing to the remote as a side effect of finishing a
  task. The doctrine's AUTH gate spoke of outward effects only in the abstract,
  and nothing said "done ≠ pushed". The rule is now named at every surface that
  enforces AUTH, with host-side enforcement (permission ask-rules / hooks)
  remaining a per-machine, per-host concern — the doctrine portable layer
  states the rule; the deterministic layer is owned by each harness config.
- Version fields bumped to 5.5.0 across the four versioned manifests.

## [5.4.0] - 2026-09-11

### Added

- **`skills/confluence`**: the read-collapse playbook — when page-body reads return
  `<<ccr:…>>` pointers instead of content, the pointer is a *deterministic* cached
  result (identical retries are futile; cap two per variable change), with read
  fallbacks (title-scoped `siteSearch` probes — `ancestor` excludes the parent
  itself; adjacent-version `page_diff` as both read oracle and post-edit recovery
  for section edits) and write discipline while reads are down: schema-bounded
  sections only, no changelog/dictionary rewrites, no full-body reconstruction from
  excerpts; park gaps in a dated footer comment.

### Changed

- **`AGENTS.md`**: §2 bounded evidence now treats pointer/ref results as
  deterministic — cap identical retries at two, then vary one variable or hand the
  blocker back; §10 gains two hard constraints — never loop a failed call on
  identical arguments (transient transport faults excepted), and never overwrite
  content unread in-session (append-only or schema-bounded fallbacks + PENDING;
  a body rebuilt from excerpts/memory and pushed over an unread original is
  fabrication).
- Motivation: the 2026-09-11 MBF-wiki sync hit a collapsed-read retry loop, then a
  near-miss pair of fabricated full-body rewrites (caught before push, originals
  intact). The recovered techniques — diff-as-recovery-oracle, schema-bounded
  section edits, footer-comment checklists — are promoted from episode to doctrine.
- Version fields bumped to 5.4.0 across the four versioned manifests.

## [5.3.0] - 2026-09-10

### Changed

- **`skills/plan-authoring`**: the execution ledger is no longer a plan section —
  PLAN.md is a planning-phase artifact, and execution state lives in a sibling
  `<slug>/STATUS.md` (dated, newest on top, cite-don't-narrate, probe-before-write
  unchanged). Plans-root index rows gain a STATUS.md link; the drift sweep now hunts
  `Execution status` inside PLAN.md; nine sections become eight;
  [verification](skills/verification/SKILL.md)'s judgment-contract cross-reference
  follows the ledger.
- Version fields bumped to 5.3.0 across the four versioned manifests.

## [5.2.0] - 2026-09-10

### Added

- **`skills/indexed-search`**: drive a trigram-indexed search tool when the host
  has one — probe first, drive the index/serve lifecycle when present, fall back
  to ripgrep then the built-in Grep; no install steps. Covers the index-earns-keep
  decision, staleness rules (`--no-index` for fresh edits; a stale-index miss is
  not evidence of absence), `--` pattern discipline, machine output (`--json`,
  `--vimgrep`, `-q` exit codes), and the flags that silently degrade to a full scan.

### Changed

- **Skill count 13 -> 14** across all discovery surfaces: AGENTS.md §11 repository
  map and §2 tool routing, README, and the five marketplace manifests. Version
  fields bumped to 5.2.0.

## [5.1.0] - 2026-09-10

### Added

- **`skills/plan-authoring`**: the deterministic plan-document pattern — one `PLAN.md`
  per effort with a fixed nine-section order, work packages as `WPn`, a DONE_WHEN
  checklist of executable checks, a dated status ledger, and a grounded mermaid
  diagram; deterministic alignment/drift sweep included. Grilling's approved plan,
  wayfinder's graduated decisions, and verification's judgment contract now all
  route through it.

### Changed

- **Skill count 12 -> 13** across all discovery surfaces: AGENTS.md §11 repository
  map, README, and the five marketplace manifests (`.claude-plugin`,
  `.cursor-plugin`, `gemini-extension.json`), whose descriptions now list
  plan-authoring. Version fields bumped to 5.1.0.
- **README verification section drift fixed**: documents the six gates (the v5.0.1
  `privacy` gate was missing) and the `plan-authoring` tree entry.

## [5.0.1] - 2026-09-09

### Added

- **`skills/confluence` storage-form template anchor**: decoded a live family
  page (v5; its identity lives in machine-local memory, never in the
  doctrine) and recorded it as
  the mcp-atlassian surface of the "BFF API Specification" family in
  [references/page-template.md](skills/confluence/references/page-template.md) — H2/H3 ladder and `<hr>` rhythm, editor-v2 table attributes (`ac:local-id` / `data-table-width` / `data-highlight-colour`), status/expand/code macro forms, M/O span syntax, changed-row `#fffae6` shading, sample-wrapper captions, and both table column sets. The template-match workflow now graduates decoded anchors into instance-variant records, and the publish checklist (now six gates) validates against the matched anchor.

### Changed

- **`skills/confluence` SKILL.md diagram and prove rules tightened**: the `data` param must be encoded by the reference's **gated encoder** (percent-encode `safe="/"` → raw deflate level 6 → padded base64; pure base64, no `%`) with its `GATE OK` line obtained **before** any publish; publish-then-prove now names the `<<ccr:…>>` collapsed-read-back failure mode and routes it to the diff/version/search probe ladder.

## [5.0.0] - 2026-09-09

v5 re-authors the doctrine's execution model from a cycle to an **execution graph**, absorbing four graph-engineering sources — flowtivity's 2026 guide, Eigent's graph-engineering and self-evolved-agents essays, and the arXiv survey 2608.21156 — while keeping v4's gates, verification layers, and budgets intact. Section numbering unchanged (§2 intake … §11 map).

### Added

- **Anchors (§0, §10)**: every proof chain terminates in a fixed external node — a spec clause, the user's own words, a red test, captured command output — the machinery may read but never rewrite; the authority rank is restated as the anchor ordering (user statement > spec > checks > code).
- **`skills/verification/references/evolution.md`**: governed self-evolution — GROW formalized as instrument -> propose -> validate -> commit, with intra-/inter-episode cadence, read-only anchors and evidence standard, adversarial validation, and the Kirby audit at model upgrades.
- **`skills/graph-engineering` knowledge edges**: `SUPERSEDES`, `DEPENDS_ON`, `DECIDED_BY`, `CAUSED`, `IMPLEMENTS`, `REFERENCES` — dated like facts.

### Changed

- **`AGENTS.md` §4 "The Execution Graph"** replaces the loop as the execution model: THINK -> ACT -> PROVE -> GROW are role-nodes; edges are typed and conditional; every cycle is capped; the forbidden shape is the unrouted cycle. §8/§9 name the three graphs (task / coordination / state).
- **`skills/graph-engineering`** re-based from escalation matrix to the doctrine's graph grammar: nodes closing on evidence, six execution edges (`PRODUCES`, `VERIFIES`, `ROUTES`, `RETURNS`, `FAN_OUT`, `JOINS`), caps, anchor routing, four shapes on a concision ladder, three-graph organization, query routing, cost gate; the v4 five-stage method (audit, identify, design, implement, type) is retained as the loop-to-graph conversion path — now from the v4 loop rather than a legacy build; [topologies](skills/graph-engineering/references/topologies.md) reworked around the canonical review graph.
- **`skills/verification`** re-anchored: executable evidence as the anchor class of last resort; GROW as the governed evolution operator.
- **`skills/teamwork`** re-anchored as the coordination graph: topology ladder, ledger as task graph, spawn briefs as node contracts.
- Flowcharts, `cmd-document`, craft, wayfinder, and README synchronized to the graph ontology.
- `skills/go-modernize` gopls MCP guidance rewritten: the shared `serve -mcp.listen` singleton, port probing, and supervisor/bridge setup replaced by gopls's official headless MCP mode.

### Not adopted

- Benchmark figures from all four sources (claims, not facts — re-derive locally); host-specific tooling and tool names; free-running self-modification (evolution stays governed).

## [4.7.0] - 2026-09-08

### Added

- **`skills/graph-engineering` query routing**: route retrieval by question type, distilled from the same [flowtivity guide](https://flowtivity.ai/blog/graph-engineering-2026-guide-openclaw-codex/) — similarity search answers lookups ("what does X do?"), graph traversal answers multi-hop questions ("why did X change, what is downstream"); graphs lose on simple lookups, high-volume retrieval, and low entity resolution; keep a cheap index for lookups beside the typed edges for the multi-hop path. New pitfall row: traversal where a lookup would do.

## [4.6.0] - 2026-09-08

### Added

- **`skills/graph-engineering`**: graph engineering for agent workflows, distilled from [flowtivity's graph-engineering guide](https://flowtivity.ai/blog/graph-engineering-2026-guide-openclaw-codex/) — whose benchmark figures are claims and are deliberately not adopted (measure locally): the loop-vs-graph decision matrix (simple/complex × low/high concurrency → single, parallel, or staged loop, or an explicit graph, entered only on three or more concurrent verification steps plus branching decision routing), the five-stage method (audit the loops → identify concurrency → design a 3-5-node topology with every edge condition written → implement and measure → type the edges), six typed edges (`SUPERSEDES`, `DEPENDS_ON`, `DECIDED_BY`, `CAUSED`, `IMPLEMENTS`, `REFERENCES` — an untyped edge is a missing decision, and facts expire), the cost gate (judge by cost per successful completion, never wall-clock alone; the guide's claimed ~50% pass-rate breakeven is re-derived, not cited; a graph that loses the gate steps back down to a staged loop), and `references/topologies.md` with the canonical Planner→Worker→parallel Reviewers→Synthesizer→gate topology, edge-condition routing patterns, the cost arithmetic, and temporal-validity rules.

### Changed

- **AGENTS.md §4 "The Loop"** routes jobs that need three or more concurrent verification steps or branching decision routing to shape execution as an explicit graph via `skills/graph-engineering` (batching stays within-turn; teamwork stays the substrate); the Repository Map gains the skill row, and README plus the five discovery manifests count twelve on-demand skills and list `graph-engineering`.

## [4.5.0] - 2026-09-07

### Added

- **`skills/grilling`**: the plan-first interview method, distilled from [mattpocock/skills](https://github.com/mattpocock/skills) (`grilling`, MIT): decisions mapped as a design tree and worked in numbered frontier rounds — every question whose prerequisites are settled, each with a recommended answer — facts dispatched to sub-agents while only decisions reach the user, done when the frontier is empty: one-recommendation plan, then STOP for approval.
- **`skills/domain-modeling`**: the active domain-language discipline, adapted from the same source (MIT): five habits (challenge terms against the glossary, sharpen fuzzy language to canonical ones, stress-test relationships with edge-case scenarios, cross-reference code claims, update `CONTEXT.md` inline), `CONTEXT.md` at the repo root as a glossary and nothing else (opinionated `_Avoid_` entries, lazy creation, `CONTEXT-MAP.md` for multi-context repos), and the ADR trigger triad — offered only when hard to reverse, surprising without context, and a real trade-off; format reference in `references/context-format.md`.

### Changed

- **AGENTS.md §2 "Decide, don't ask"** now states the fact/decision split: facts are the agent's to look up; only decisions reach a human. The plan-first Shape line links `skills/grilling` for the full method; §5 routes design work touching domain terms, the glossary, or a decision record to `skills/domain-modeling`; the Repository Map gains both rows.
- **Glossary unified on `CONTEXT.md`** at the repo root: `cmd-document`'s `--type=glossary` and its bootstrap layout retarget from `docs/glossary.md`, with format owned by `skills/domain-modeling`; README's tree follows. One language, one source of truth.
- **Scoping cross-references**: wayfinder's Grilling tickets route to `skills/grilling` for technique, with "frontier" disambiguated (map tickets across sessions vs open questions within one session); solution-architecture §3 notes domain-modeling owns the conversation-time ADR trigger while format and lifecycle stay canonical there.
- **`skills/confluence`**: three hard-won publish lessons from one day of blank-diagram debugging. (1) The `plantumlcloud` `data` encoding is not standard PlantUML base64 and varies between pages on the same instance — prove an encoder against the `data` param of a page that demonstrably renders in a browser (a sibling's mere existence proves nothing), re-encoding byte-for-byte before trusting it; recipe pinned as percent-encode → raw deflate (level 6) → standard base64 with padding kept. (2) A collapsible raw-source expand must use the native `expand` macro in storage format — Confluence silently strips an HTML `<details>` element from the stored body. (3) Multi-KB write payloads can be silently corrupted in the MCP client→server hop (`InputValidationError … could not be parsed as JSON`, reported bytes ~3× the payload) — a transport defect, not an authoring mistake: switch transport via smaller `confluence_update_page_section` or full-body `confluence_update_page` with `content_file`; and read-backs now rank probes by descending strength, led by `confluence_get_page_diff` (with the caveat that search indexes lag and never index macro parameters).

## [4.4.0] - 2026-09-06

### Added

- **`skills/wayfinder`**: plan an effort too big for one agent session as a shared map of decision tickets on the repo's issue tracker — destination named first, map as index (not store), HITL/AFK ticket types (research, prototype, grilling, task), fog of war graduated into tickets as the frontier advances, out-of-scope recorded where ruled out, claim-before-work for concurrent sessions, at most one ticket resolved per session; the map is done when nothing is left to decide before someone goes and does the thing. AGENTS.md routes plan-first efforts too big or foggy for one session to it and scopes it against teamwork: teamwork parallelizes one job across contexts, wayfinder persists one effort across sessions.

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
