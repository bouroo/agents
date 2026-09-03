---
name: system-diagramming
description: "Turn a codebase or system description into a polished, interactive system map: author a small typed JSON IR inside one self-contained HTML template (inline SVG, dark/light themes, pan/zoom, search) and gate it with the bundled validator — no installs, no network. Use when the user asks to visualize architecture, infrastructure, workflows, API sequences, data pipelines, or state machines, or to convert/beautify Mermaid diagrams."
---

# System Diagramming

One deliverable: a single self-contained HTML file — an inline-SVG system map drawn deterministically from a typed JSON IR embedded in the file, with dark/light themes, pan/zoom, hover tracing, and node search built in. Layout judgment is the agent's; drawing is the template's. Everything lives in this directory — the [template](references/template.html) (IR contract in its header comment) and the stdlib [validator](references/validate.py): nothing to install, nothing to fetch. Exports, motion, and share cards are out of scope; the browser's own screenshot/print covers them.

**When to load:** asked to visualize architecture, topology, CI/CD, request lifecycles, pipelines, or state machines — or to beautify Mermaid. The design decisions themselves are [solution-architecture](../solution-architecture/SKILL.md) territory; this skill renders them.

## 1. Choose the kind

| Kind | Use for | Layout convention |
|---|---|---|
| `architecture` | components, services, storage, trust boundaries | grid + auto routes; `groups` draw the boundaries |
| `workflow` | processes, approval gates, CI/CD, tool calls | left-to-right columns, `orient: "h"`; groups as stage bands |
| `sequence` | API call chains, request lifecycles, async traces | participants across the top with `lifeline: true`; one `points` edge per message row |
| `dataflow` | pipelines, ETL/ELT, lineage, consumers | like architecture; `emphasis` the stores and transforms |
| `lifecycle` | state machines, retries, waits, terminal outcomes | state pills on a rail; `dashed` for retry/wait, `emphasis` for terminal |

## 2. Author the IR — artifact first

The IR is the JSON inside the template's `ir` script block; the field contract is the template's header comment. Write the IR before fiddling with anything visual.

- ≤ 12 primary nodes, one obvious main path, short side branches; place on a 20px grid with ≥ 24px clear gap between boxes; canvas 1000–1400 wide.
- Roles are the palette (`frontend` `backend` `database` `cloud` `security` `messagebus` `external` `state` `participant`) — never inline colors.
- Relationship labels are semantic data: name the protocol/action/direction; never delete a label to fix layout.
- Box-to-box edges need only an `orient: "h"|"v"` hint; explicit `points` polylines are for sequence message rows.
- Preserve exact product names, identifiers, protocols, and API paths.
- Cards: at most 3–4 conclusion cards; every claim in a card must be visible in the diagram.

## 3. Deliver

Copy the template, replace its `ir` block with yours, write `<slug>.html`.

## 4. Validate -> prove

```bash
python3 <this-skill>/references/validate.py <slug>.html
```

- `E_*` lines are defects: fix the diagnosed subject only, rerun — the §7 hard bound (3 failed cycles) stops the loop.
- `W_*` lines are judgment calls: resolve them or knowingly accept.
- L2: view it — open the file or take a headless-browser screenshot; never claim the diagram renders without one look. No browser available? Say so and hand over the validated file.

## 5. Iterate

Edit the `ir` block in place — it is the source of truth — and re-validate. Never edit the renderer script; if it drifted, regenerate from the template.

Mermaid in: read it for topology and meaning, then author fresh IR — `flowchart`/`graph` -> `workflow` (`architecture` for component maps), `sequenceDiagram` -> `sequence`, `stateDiagram` -> `lifecycle`; never carry Mermaid styling over.

## Output

Report the artifact path, kind, and the validator receipt (0 errors). The file plus the receipt outrank the narrative — claim only what the validator printed and you viewed.
