[![Last commit](https://img.shields.io/github/last-commit/bouroo/agents?logo=github)](https://github.com/bouroo/agents)
![Type](https://img.shields.io/badge/type-AI%20agent%20config-blue)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](./LICENSE.md)

# bouroo/agents

A shared setup for autonomous coding agents that is **agnostic of programming languages, agent frameworks, and agent harnesses**: one governance manifesto, twelve on-demand skills, and four routine-task command workflows. Any coding agent that reads repository instruction files can consume it as-is — no installer, no manifests, no per-tool copies.

## What's inside

```
├── AGENTS.md                          the manifesto: intake route, decision gates,
│                                      the execution graph, verification dial,
│                                      context/state rules, hard constraints
├── skills/
│   ├── craft/                         twelve commandments + INTENT/TWINS/AUTH/PENDING gates
│   ├── performance/                   measure-first cycle + four-overhead-source routing
│   ├── verification/                  right-sizing dial, evidence as anchors, mutation probe,
│   │   └── references/                judge protocol; flowcharts.md renders the execution
│   │                                  graph as decision charts; evolution.md the governed
│   │                                  GROW cycle
│   ├── teamwork/                      the coordination graph: topology ladder, task ledger,
│   │                                  file ownership, spawn briefs, adversarial verification
│   ├── wayfinder/                     efforts too big for one session: map of decision
│   │                                  tickets on the tracker; fog of war; one ticket
│   │                                  per session
│   ├── confluence/                    operate Atlassian wikis via Rovo or
│   │                                  mcp-atlassian MCP servers
│   ├── go-modernize/                  modernize Go per go.mod's declared version;
│   │                                  go fix / modernize analyzer, idiom table
│   ├── solution-architecture/         ASRs + SEI scenarios, pattern selection by tradeoff,
│   │   └── references/                ADRs, C4 modeling, estimation/governance/delivery
│   ├── grilling/                      in-session decision interviewing: design tree,
│   │                                  numbered frontier rounds, facts vs decisions
│   ├── domain-modeling/               active domain-language discipline: CONTEXT.md
│   │   └── references/                glossary, edge-case scenarios, ADR trigger triad
│   ├── system-diagramming/            system maps as one interactive HTML: typed JSON IR,
│   │                                  bundled template + validator, no installs
│   └── graph-engineering/             the execution-graph grammar: nodes, typed edges,
│       └── references/               caps, anchors, shapes, cost; worked topologies
├── commands/
│   ├── cmd-verify.md                  quality-gate pipeline with a fix/re-verify loop
│   ├── cmd-review.md                  severity-grouped code review with one verdict
│   ├── cmd-refactor.md                behavior-preserving restructure, measured before/after
│   └── cmd-document.md                bootstrap/sync a docs/ tree (systems, flows,
│                                      ADRs, API endpoints; glossary -> CONTEXT.md)
├── .claude-plugin/, .cursor-plugin/   marketplace plugin + listing metadata
├── gemini-extension.json              extension discovery metadata
└── scripts/
    ├── check.py                       five deterministic gates (CI runs these)
    └── install.sh                     detect tools on a machine and install
```

## The execution model

Every job runs as an **execution graph**: THINK -> ACT -> PROVE -> GROW are the role-nodes most jobs need, edges are typed and conditional, and every cycle is capped — the forbidden shape is a node re-entering itself with no new evidence. Three graph structures organize anything above trivial: the **task graph** (what: units, dependencies, DONE_WHEN), the **coordination graph** (who: solo -> delegation -> team), and the **state graph** (how it operates: the repository as system of record). Every proof chain terminates in an **anchor** — a fixed external node like a spec clause, the user's words, or captured command output that the machinery may read but never rewrite; the authority rank (user statement > spec > checks > code) is the anchor ordering. The grammar lives in [graph-engineering](./skills/graph-engineering/SKILL.md); GROW is the governed evolution operator that edits the machinery future runs execute ([evolution](./skills/verification/references/evolution.md)).

## The doctrine in one line

Classify before working (trivial / fit / shape); owe named gates at decision points (`INTENT:` `TWINS:` `AUTH:` `PENDING:`); run every job as an execution graph with typed edges and capped cycles; terminate every proof chain in an anchor; prove with layered evidence (L1 static / L2 runtime / L3 end-to-end), a mutation probe, and a hard verify bound of 3 failed cycles; grow by governed evolution — recurring failures become deterministic gates, and controls better models make redundant are cut.

## Using it

Manual consumption only:

- **Manifesto** — copy `AGENTS.md` content into your assistant's instruction file at whatever location your tool reads, or point the tool at this file directly.
- **Skills** — copy or symlink individual `skills/<name>/` directories into the skill path your runtime discovers (they carry standard Agent-Skills frontmatter: `name` + `description`).
- **Commands** — `commands/<name>.md` are self-contained routine-task workflows (verify / review / refactor / document); paste their arguments after invocation wherever your tool surfaces custom prompts, or load them on demand.
- **Marketplaces** — the repository ships plugin/extension discovery metadata at its canonical paths (`.claude-plugin/`, `.cursor-plugin/`, `gemini-extension.json`), so Agent-Skills-compatible CLIs can add it directly from GitHub (`npx skills add bouroo/agents`) and host marketplaces consume it without any generation step.
- **Local installer** — `scripts/install.sh` detects which compatible tools live on the machine and links (or copies) the setup into each one's config directory:

  ```bash
  ./scripts/install.sh detect               # what did we find?
  ./scripts/install.sh install              # all detected tools
  ./scripts/install.sh install --dry-run    # preview the exact actions
  ./scripts/install.sh status               # per-tool link state
  ./scripts/install.sh uninstall            # removes only links pointing into this repo
  ```


If a previous major version installed symlinks on your machine, remove them with that version's uninstaller from git history — v4 ships nothing that writes outside this repository.

## Verification

```bash
python3 scripts/check.py --all
```

| Gate | Enforces |
| --- | --- |
| `budget` | `AGENTS.md` stays within its line budget (the concision charter) |
| `frontmatter` | every skill/command carries valid, colon-safe Agent-Skills metadata |
| `links` | every relative Markdown link resolves |
| `agnostic` | core doctrine is free of host-binding tokens |
| `manifests` | marketplace manifests parse; version fields agree across files |

CI runs all five on every push and pull request.

## Versioning

Git tags are the version source; release notes live in [CHANGELOG.md](./CHANGELOG.md). Licensed Apache-2.0 ([LICENSE.md](./LICENSE.md)).
