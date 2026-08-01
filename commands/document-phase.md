---
description: Document phase  --  bootstrap repo docs or sync an existing docs/ tree (systems, flows, ADRs, glossary) with code changes
---

# Document Phase

Bootstrap or update the repo's `docs/` documentation so it stays in sync with the code as part of the THINK→ACT→PROVE→GROW loop. Docs and code must agree  --  a stale doc is a bug.

> **Agent:** requires file-edit + shell access (to read the tree)  --  run on the implementing/build agent, not `plan` or `conductor`.

Target area (optional): **$ARGUMENTS**. Interpret as the system, flow, ADR, or glossary area to document (e.g. `auth`, `email-verification flow`, `session-vs-token ADR`). If empty, detect what changed with `git diff`/`git diff --cached` and document the affected system or flow.

---

## 0. Load the documentation skill

Before anything else, load the **`repo-documentation` skill** via the skill tool. It carries the full doctrine for repo-local docs and ships the three copy-in templates (`system.md`, `flow.md`, `adr.md`) as siblings of `SKILL.md`. This command is the trigger; the skill is the reference. Refer back to it at each step for canonical wording on doc types, ADR frontmatter rules, source maps, glossary usage, and the granularity rules (system until it crosses systems, then promote to flow).

---

## When to document (and when not to)

Apply the skill's *When to Use* criteria -- central, risky, frequently changed, hard to infer, or security/billing/data-integrity/user-visible. **Do not document every file**; prefer one well-written system or flow doc over many shallow ones.

---

## 1. Assess

Check whether the target repo already has a `docs/` tree; the answer dictates the path.

- **If `docs/` is absent** → **bootstrap**: create `docs/`, `docs/systems/`, `docs/flows/`, `docs/architecture/decisions/`, `docs/templates/`; create `docs/README.md` as an index explaining the layout; create `docs/glossary.md` as a stub with a short preamble and an empty `## Terms` section; copy the three skill templates from `repo-documentation`'s siblings into `docs/templates/`. Then proceed to step 2.
- **If `docs/` is present** → proceed directly to step 2. Use the existing tree structure as-is; do not rearrange or copy templates that are already there.

---

## 2. Locate

- Read `AGENTS.md` and/or `docs/README.md` if present for the docs map and the docs/AGENTS division of labor.
- Identify the affected system doc in `docs/systems/` and any related flow docs in `docs/flows/`.
- Check `docs/architecture/decisions/` for ADRs that govern the area.
- Check `docs/glossary.md` for Title Case domain terms used here.
- If the target area has no existing doc, decide whether it warrants one (see *When to document*).

---

## 3. Choose Type

Pick exactly one type for the new or updated doc; resist creating new categories. The four types (system / flow / ADR / glossary), their granularity rules, and when to promote system → flow live in the `repo-documentation` skill -- choose there, not from memory. ADR lifecycle rules (Proposed → Accepted; never rewrite an accepted ADR, supersede it with `superseded_by`) are defined in the skill.

---

## 4. Draft from Template

- If `docs/templates/` exists, prefer it  --  the repo may have customized the templates. The skill's sibling templates remain the canonical reference.
- If `docs/templates/` is absent (a pre-existing `docs/` tree never bootstrapped via this command), reference the skill's sibling templates directly without creating a tree in the working repo.

The skill owns the structural rules -- Source map contents, ADR frontmatter fields, related-docs linking, glossary Title-Case form, and the `[NEEDS CLARIFICATION]` convention. Reference it while drafting; do not re-derive the field lists here.

---

## 5. Sync

Update the surrounding docs in the target repo, not just the target.

- If a Title Case term is introduced or its meaning changes, update `docs/glossary.md` and search for existing usages.
- If a flow doc is created, link it from the relevant system doc(s) under `## Important flows` and from `docs/README.md` if it is a primary flow.
- If a new system is created, register it in `docs/README.md`'s docs map.
- If an ADR is accepted and changes behavior, propagate the consequence into affected system/flow docs.
- Ensure docs and code agree before finishing. If they disagree, either update docs to match code, update code to match documented intent, or explicitly call out the mismatch for review.

---

## 6. Verify

Three checks before reporting done. Use the target repo's own tooling  --  nothing from this command's host environment.

1. **Links resolve**  --  every relative Markdown link in the new/updated doc (and its Source map) points to a real file in the target repo. Use `rg` to spot-check.
2. **ADR frontmatter is valid**  --  `status` is one of the allowed values; `date` is `YYYY-MM-DD`; `superseded_by` is present when `status: Superseded` and points to a real file.
3. **Repo gate**  --  run the target repo's own formatter, link-check, Markdown linter, validator, pre-commit hook, and/or test suite  --  whatever it ships as its quality gate. Enforce a zero exit code. If the repo has no gate, note the absence and proceed.

If any check fails, fix and re-run. Do not declare done with broken links, invalid frontmatter, or a failing gate.

---

## Reporting

State the target area, the type chosen and why, files created or updated, the template used, whether the Glossary/README maps were touched, the gate command(s) invoked and exit code(s), and a one-line verdict  --  **DOCS SYNCED** or **BLOCKED**.
