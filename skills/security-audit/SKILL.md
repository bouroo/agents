---
name: security-audit
description: "Vulnerability review of a codebase, API, service, CLI, or library: the candidate gate that separates a real boundary violation from a best-practice deviation, severity calibrated to demonstrated impact, needs_validation discipline, attack-class coverage, and the report shape. Use for a security question, a focused security review, triage of a reported finding, threat modeling, or a full audit. The full audit workflow runs only on explicit request."
---

# Security Audit

**Stance:** a finding is a boundary violation with a victim, not a best-practice deviation. The failure mode is a report of "missing rate limit" and "consider rotating keys" — claims that cost an owner more to triage than they are worth, and bury the one real defect beneath. A candidate that cannot name who is harmed and how does not survive the gate.

Load [craft](../craft/SKILL.md) for the artifact gates and [verification](../verification/SKILL.md) for the evidence discipline this skill applies. An audit is [Test](../lifecycle/SKILL.md)-stage work, run by the Verifier seat — never by the author of the code under review.

## Modes

Loading this skill authorizes neither a full audit nor any file creation.

- **Guidance (default)** — a security question, a focused review, triage of a reported finding, or methodology. Use only the parts you need, answer in the conversation, write nothing.
- **Full audit** — only when the user explicitly asks to audit or pen-test, asks for a full, comprehensive, or end-to-end review, or requests a report artifact. Then run the workflow and write `REPORT.md`.

If the request could be either, ask one question before creating files.

## The candidate gate

Every candidate names all six, or it is not a finding:

1. the **lower-trust principal** — who acts
2. the **input or action** it controls
3. the **intended control** — what is supposed to stop it
4. the **boundary crossed**
5. the **affected principal or resource** — who is harmed
6. the **concrete result**, observable by an owner

This is §0's anchor discipline aimed at security: the chain terminates in a real victim and a real effect — not in a missing practice, a guessed deployment, a generic crash, or self-impact (your own authority affecting only you).

## Three states

- **`confirmed`** — source evidence plus a bounded local check establish the whole chain. Only these carry severity.
- **`needs_validation`** — one specific, source-grounded boundary hypothesis blocked by one *exact* missing fact (a proxy, identity provider, browser, deployment, or runtime behavior absent from the repository). State the missing fact and the safe check that resolves it. **No severity**: this is a blocked hypothesis, not a low-confidence finding.
- **`rejected`** — the claim failed. Record the claim and why, so the next run does not re-litigate it ([artifacts](../artifacts/SKILL.md) ledger discipline).

## Severity (confirmed only)

- **critical** — unauthenticated code execution, full data-store access, or takeover of arbitrary accounts.
- **high** — an explicit control *fully defeated* with real consequences: authentication bypass, cross-tenant read or write, stored script execution, authenticated code execution, unauthenticated remote stop of a shared service.
- **medium** — a real boundary violation with limited blast radius, uncommon preconditions, or narrowly confined consequences.
- **low** — disclosure of non-secret internals, or an effect needing sustained effort for minimal gain.
- **informational** — confirmed, minimal impact, useful mainly as a prerequisite for a larger finding.

Severity reflects **demonstrated** impact, never theoretical reach. The high/medium discriminator: does the result fully defeat an explicit control, or only weaken it? If you cannot state the concrete damage, it is lower than it feels.

## Execution boundary

Source inspection is read-only. A local check is bounded: the target's own build or tests, against fixtures with dummy principals and dummy secrets, stopping at the minimum effect that establishes the defect. Never probe a deployed endpoint, shared service, production identity, other users' data, or a live control plane; never test availability against a shared process; never publish an artifact, alter a release, or spend paid quota. Never log or commit a secret (§10).

Absence from the repository is not absence in production, and presence is not assumed: proxy, browser, identity-provider, packaging, and deployment behavior are real controls, so one you cannot verify becomes `needs_validation` with the exact missing fact — never a guess in either direction.

Any outward or irreversible step needs `AUTH:` (§3) — the user's own words authorizing *this exact action*. Loading the skill, finishing a scan, or finding a real bug authorizes none of it.

## Hunting

Coverage units are **entry surface × boundary × attack class**, never files. [`references/attack-classes.md`](references/attack-classes.md) lists the classes, each domain's rules for choosing them, and what is not a finding; every unit traces untrusted input from its entry point toward a dangerous sink.

Stay solo for a focused review. Fan out when coverage justifies it (§9 [teamwork](../teamwork/SKILL.md)): one hunter per unit with no shared file, then an agent that did *not* find a candidate re-derives it before it reaches `confirmed` ([verification](../verification/SKILL.md) judge protocol). A hunter's report is testimony; independent re-derivation is evidence.

A fix names the invariant the code must enforce and the narrowest change that enforces it at the last trusted decision point — or it becomes a `needs_validation` for the control you cannot see. The audit describes fixes; it does not edit the target. Applying them is a separate task.

## Report

A full audit writes `REPORT.md` with these sections, in order:

1. **Scope** — target, source ref (commit, and whether the worktree is dirty), what is in and out of scope.
2. **Coverage** — the units examined. Never imply the run was exhaustive; state the gaps.
3. **Findings** — per confirmed finding: severity, the six-field boundary chain, evidence as `file:line` plus the captured command and output, and the smallest effective fix.
4. **Needs validation** — per record: the hypothesis, the exact missing fact, and the safe resolution.
5. **Rejected** — the claim and why it failed.

Keep the report target-neutral: no live-probe instructions, and never present scanner output as stronger than what was actually observed.
