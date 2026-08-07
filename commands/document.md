---
description: "Bootstrap or sync a repo's docs/ tree (systems, flows, ADRs, API, glossary) with code changes. Use when a behavior, interface, invariant, or domain-term change must be reflected in project documentation."
argument-hint: "[system|flow|adr|api|glossary area] [--type=<system|flow|adr|api|glossary>]"
agent: coder
phase: ACT
---

# Document -- sync the docs/ tree with code changes

Docs and code must agree; a stale doc is a bug. This command bootstraps a `docs/` tree where none exists and keeps an existing one in sync with code, so documentation stays accurate inside the THINK-ACT-PROVE-GROW loop.

Runs on the mutating worker (the coder), not the orchestrator: it needs file-edit and shell access to read the tree and write Markdown.

## When to use

A change touches system behavior, workflow, data model, persistence, integration, security/auth, an invariant, an API, or a glossary term. Apply the skill's *When to Use* bar -- central, risky, frequently changed, hard to infer, or sensitive (security, billing, data integrity). Do not document every file; one well-written system or flow doc beats many shallow ones.

## Inputs

- **$ARGUMENTS** (optional): the system, flow, ADR, or glossary area to document, e.g. `auth`, `email-verification flow`, `session-vs-token ADR`.
- If empty, detect what changed with `git diff` / `git diff --cached` and document the affected system or flow.
- **Options** (ride inside `$ARGUMENTS`, any order, `key=value`):
  - `--type=<system|flow|adr|api|glossary>` -- force the doc type instead of choosing it from the skill's granularity rules. Use only when the change clearly maps to one type.
- Parsing `$ARGUMENTS` is this command's job -- the host only forwards the string. See [command inputs](../skills/harness-engineering/references/agent-computer-interface.md).

## Steps

1. **Load the skill.** Load `repo-documentation` before anything else. It owns doc-type doctrine, ADR lifecycle rules (Proposed -> Accepted; never rewrite an accepted ADR, supersede it with `superseded_by`), source maps, glossary form, and granularity rules (system until it crosses systems, then promote to flow). Refer back to it at each step.
2. **Assess.** Does the target repo have a `docs/` tree?
   - Absent -> bootstrap: create the layout, index, glossary stub, and copy in the templates. See [bootstrap](document/references/bootstrap.md).
   - Present -> use the existing tree as-is; do not rearrange or duplicate templates.
3. **Locate.** Read `AGENTS.md` and/or `docs/README.md` for the docs map. Find the affected system doc (`docs/systems/`), related flows (`docs/flows/`), endpoint docs (`docs/api/`), governing ADRs (`docs/architecture/decisions/`), and Title Case terms in `docs/glossary.md`. If no doc exists, decide whether the area warrants one. A change that touches an HTTP endpoint warrants an endpoint doc in `docs/api/<service>/`.
4. **Choose type.** Pick exactly one: system / flow / ADR / API / glossary. If `$ARGUMENTS` set `--type`, use that; otherwise choose from the skill, not memory, and resist inventing categories. For **API**, the doc covers one HTTP endpoint and lives at `docs/api/<service>/<endpoint>.md` (per-endpoint); publish the same endpoint to a wiki via the [confluence](../skills/confluence/SKILL.md) adapter's endpoint-page template (`page_template.py`), translating the doc's mermaid sequence to PlantUML source for that generator.
5. **Draft from template.** Prefer `docs/templates/` (the repo may have customized them); otherwise reference the skill's templates directly without creating a tree. Follow the skill's structural rules for source maps, ADR frontmatter, related-docs linking, and the `[NEEDS CLARIFICATION]` convention.
6. **Sync surroundings.** Update linked docs, not just the target: a new Title Case term -> `glossary.md`; a new flow -> link from its system(s) and `README.md`; a new system -> register in the docs map; an accepted ADR -> propagate its consequence into affected docs. Reconcile any docs-vs-code disagreement by updating docs, fixing code, or flagging the gap.
7. **Verify.** Confirm every relative link resolves, ADR frontmatter is valid, and the repo's own gate is green (see Success metrics).

## Success metrics

- Every relative Markdown link in new/updated docs and their source maps points to a real file in the target repo (spot-check by searching the tree).
- ADR frontmatter is valid: `status` is an allowed value, `date` is `YYYY-MM-DD`, and `status: Superseded` carries a `superseded_by` pointing to a real file.
- The target repo's own quality gate (formatter, link-check, Markdown linter, validator, pre-commit hook, or test suite) exits zero. If the repo ships no gate, note the absence.

## Failure metrics

- A broken link, invalid frontmatter, or a non-zero gate after a fix attempt -- fix and re-run; do not declare done with any check red.
- Docs contradict verified code and the contradiction cannot be reconciled within scope -- hand back with the mismatch called out.
- The area named in $ARGUMENTS cannot be located and cannot be inferred from the diff -- hand back rather than invent context.

## References

- [repo-documentation](../skills/repo-documentation/SKILL.md) -- doc types, ADR lifecycle, source maps, glossary, granularity rules; ships the templates.
- Templates (copied into `docs/templates/`): [system.md](../skills/repo-documentation/references/system.md) | [flow.md](../skills/repo-documentation/references/flow.md) | [adr.md](../skills/repo-documentation/references/adr.md) | [api.md](../skills/repo-documentation/references/api.md).
- [bootstrap](document/references/bootstrap.md) -- exact layout to create when `docs/` is absent.
