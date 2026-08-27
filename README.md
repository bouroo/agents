[![Last commit](https://img.shields.io/github/last-commit/bouroo/agents?logo=github)](https://github.com/bouroo/agents)
![Type](https://img.shields.io/badge/type-AI%20agent%20config-blue)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](./LICENSE.md)

# bouroo/agents

A shared setup for AI coding assistants that is **agnostic of programming languages, agent frameworks, and host tools**: one governance manifesto plus three on-demand skills, ~740 lines total. Any coding agent that reads repository instruction files can consume it as-is — no installer, no manifests, no per-tool copies.

## What's inside

```
├── AGENTS.md                          the manifesto: intake route, decision gates,
│                                      THINK-ACT-PROVE-GROW loop, verification dial,
│                                      context/state rules, hard constraints
├── skills/
│   ├── craft/                         twelve commandments + INTENT/TWINS/AUTH/PENDING gates
│   ├── performance/                   measure-first cycle + four-overhead-source routing
│   └── verification/                  right-sizing dial, evidence audit, mutation probe,
│       └── references/flowcharts.md   judge protocol; the loop as decision charts
└── scripts/check.py                   four deterministic gates (CI runs this)
```

## Using it

Manual consumption only:

- **Manifesto** — copy `AGENTS.md` content into your assistant's instruction file at whatever location your tool reads, or point the tool at this file directly.
- **Skills** — copy or symlink individual `skills/<name>/` directories into the skill path your runtime discovers (they carry standard Agent-Skills frontmatter: `name` + `description`).

If a previous major version installed symlinks on your machine, remove them with that version's uninstaller from git history — v4 ships nothing that writes outside this repository.

## The doctrine in one line

Classify before working (trivial / fit / shape); owe named gates at decision points (`INTENT:` `TWINS:` `AUTH:` `PENDING:`); work THINK -> ACT -> PROVE -> GROW with backward planning and batched execution; prove with layered evidence (L1 static / L2 runtime / L3 end-to-end), a mutation probe, and a hard verify bound of 3 failed cycles; grow by converting recurring failures into deterministic gates and cutting controls better models make redundant.

## Verification

```bash
python3 scripts/check.py --all
```

| Gate | Enforces |
|---|---|
| `budget` | `AGENTS.md` stays within its line budget (the concision charter) |
| `frontmatter` | every skill carries valid, colon-safe Agent-Skills metadata |
| `links` | every relative Markdown link resolves |
| `agnostic` | core doctrine is free of host-binding tokens |

CI runs all four on every push and pull request.

## Versioning

Git tags are the version source; release notes live in [CHANGELOG.md](./CHANGELOG.md). Licensed Apache-2.0 ([LICENSE.md](./LICENSE.md)).
