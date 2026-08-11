# Bootstrap a docs/ tree

Run when the target repo has no `docs/` tree. Create the layout exactly once; if a `docs/` tree already exists, use it as-is and skip this.

## Layout to create

```
docs/
  README.md                    # index: explains the layout
  glossary.md                  # stub: short preamble + empty ## Terms
  systems/                     # one doc per system
  flows/                       # one doc per cross-system flow
  api/                         # one doc per HTTP endpoint (per-endpoint)
  architecture/
    decisions/                 # ADRs
  templates/                   # copied-in templates (see below)
```

## README index

`docs/README.md` explains the layout: what each directory holds, how systems relate to flows, where ADRs live, and how the glossary is used. It is the human and agent entry point to the tree.

## Glossary stub

`docs/glossary.md` gets a short preamble on its purpose, then an empty section:

```
## Terms
```

Add Title Case terms here as they are introduced.

## Templates

Copy the four templates from the `repo-documentation` skill into `docs/templates/`:

- [system.md](../../../skills/repo-documentation/references/system.md) -> `docs/templates/system.md`
- [flow.md](../../../skills/repo-documentation/references/flow.md) -> `docs/templates/flow.md`
- [adr.md](../../../skills/repo-documentation/references/adr.md) -> `docs/templates/adr.md`
- [api.md](../../../skills/repo-documentation/references/api.md) -> `docs/templates/api.md`

These copies let the repo customize its own templates; the skill's siblings remain the canonical reference.

## After bootstrap

Proceed to Locate (step 3 of the command) and draft the first doc from the freshly copied templates.
