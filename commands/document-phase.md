---
description: Document phase  --  bootstrap repo docs or sync an existing docs/ tree (systems, flows, ADRs, glossary) with code changes
---

# Document Phase

Bootstrap or update the repo's `docs/` documentation so it stays in sync with the code. Docs and code must agree  --  a stale doc is a bug.

> **Agent:** requires `edit` + `bash` (read)  --  run on the implementing/build agent, not `plan` or `conductor`.

Target area (optional): **$ARGUMENTS**. Interpret as the system, flow, ADR, or glossary area to document (e.g. `auth`, `email-verification flow`, `session-vs-token ADR`). If empty, detect what changed with `git diff`/`git diff --cached` and document the affected system or flow.

---

## 0. Load the documentation skill

Before anything else, load the **`repo-documentation` skill** via the skill tool. It carries the full doctrine for repo-local docs and ships the three copy-in templates (`system.md`, `flow.md`, `adr.md`) as siblings of `SKILL.md`. This command is the trigger; the skill is the reference. Refer back to it at each step for the canonical wording.

---

## When to document (and when not to)

Document when behavior is central, risky, frequently changed, hard to infer from a single file, or has security, billing, data-integrity, or user-visible implications. **Do not document every file.** Skip purely local helpers, generated code, or trivial utilities. Prefer one well-written system or flow doc over many shallow ones.

---

## 1. Assess

Check whether the target repo already has a `docs/` tree; the answer dictates the path.

- **If `docs/` is absent** → **bootstrap** it:
  - Create `docs/`, `docs/systems/`, `docs/flows/`, `docs/architecture/decisions/`, and `docs/templates/`.
  - Create `docs/README.md`  --  an index that explains the layout (what goes in `systems/`, `flows/`, `architecture/decisions/`, `templates/`, and the glossary at `docs/glossary.md`) and links to the doc types.
  - Create `docs/glossary.md` as a stub with a short preamble and an empty `## Terms` section.
  - Copy the three skill templates (`system.md`, `flow.md`, `adr.md`) from the `repo-documentation` skill's siblings into `docs/templates/`. This lets the repo customize them over time.
  - Then proceed to step 2 to document the target area.
- **If `docs/` is present** → proceed directly to step 2. Use the existing tree structure as-is; do not rearrange or copy templates that are already there.

---

## 2. Locate

Find the right place in the docs tree before writing anything.

- Read `AGENTS.md` and/or `docs/README.md` if present for the docs map and the docs/AGENTS division of labor.
- Identify the affected system doc in `docs/systems/` and any related flow docs in `docs/flows/`.
- Check `docs/architecture/decisions/` for ADRs that govern the area.
- Check `docs/glossary.md` for Title Case domain terms used here.
- If the target area has no existing doc, decide whether it warrants one (see *When to document*).

---

## 3. Choose Type

Pick exactly one type for the new or updated doc; resist creating new categories.

- **System**  --  a coherent area of application behavior (module, package, service, feature area). Use when behavior is local and easy to explain in one place.
- **Flow**  --  behavior that **crosses systems, has several steps or states, is frequently changed or debugged, involves external services, or has security/billing/data-integrity/user-visible implications**. Promote from a system doc when it grows complex.
- **ADR**  --  a durable technical decision that shapes more than one system (auth strategy, async webhook processing, ownership of state, idempotency mandates, adapter boundaries). Status: `Proposed` until approved, then `Accepted`. Never rewrite an accepted ADR to change the decision; create a new ADR and mark the old one `Superseded` with `superseded_by`.
- **Glossary**  --  a Title Case domain term that is reused across systems and is easy to misunderstand (Account, Workspace, Session, Verification Token, etc.).

Use the granularity rules from the `repo-documentation` skill: keep behavior inside a system doc until it crosses systems or meets any flow criterion, then promote to a flow doc.

---

## 4. Draft from Template

Templates live with the `repo-documentation` skill, and (after bootstrap) a working copy also lives at `docs/templates/` in the target repo.

- If `docs/templates/` exists, prefer it  --  the repo may have customized the templates. The skill's sibling templates remain the canonical reference.
- If `docs/templates/` is absent (a pre-existing `docs/` tree that was never bootstrapped via this command), reference the skill's sibling templates directly without creating a tree in the working repo.

Hard requirements when drafting:

- **Source map**  --  include a `## Source map` section with Markdown relative links to the most important source files (entry points, state definitions, handlers, services, jobs, key tests). Do not list every file unless the system is small.
- **Related docs**  --  link to other systems, flows, ADRs, and glossary entries via relative Markdown links.
- **Mark uncertainty**  --  if behavior is hard to infer, write `[NEEDS CLARIFICATION]` or "uncertain  --  verify against code" rather than inventing an explanation. Unsupported guesses are worse than gaps.
- **ADRs**  --  every ADR begins with YAML frontmatter: `status` (Proposed/Accepted/Superseded/Deprecated/Rejected), `date` (`YYYY-MM-DD`), and `superseded_by` (required only when Superseded). Do not add other frontmatter fields.
- **Glossary**  --  Title Case headings; use the same Title Case form in finished prose when it improves clarity.

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
