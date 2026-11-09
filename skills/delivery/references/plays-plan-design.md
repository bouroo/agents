# Plays — Plan and Design

> Load on demand from [delivery](../SKILL.md): the two practices that capture an intent and turn it into a spec, each with its five parts and its measurement pair.

## Stage 1 — Plan

### Capture as `intent.md`

**What changes.** An idea stops waiting for someone to write it up. Intent is captured once, in the originator's own words, as a version-controlled artifact the next stage can act on.

**Getting started.** None. Infrastructure: a shared, version-controlled home for intent the product owner watches — for one product, an `intent/` folder in the product repository, so the artifact chain sits next to the code derived from it; a dedicated intent repository earns its overhead only when intent spans many repositories, and in a monorepository it is a directory. Contributors who do not use version control still commit through a connector, so the home's access policy matters.

**Steps.**

1. The originator describes the problem in their own words — what they cannot do today, who is affected, what better looks like, what is out of scope. No formal language required.
2. Brainstorm until the idea is concrete. The agent asks the questions an analyst would ask: scope, users, constraints, what success looks like.
3. Ask for the result as `intent.md` using the organization's template, which a technical team member encodes as a skill and signs off with a lead. The template covers the problem, the proposed outcome, the affected users and systems, the constraints, and the open questions.
4. The originator corrects anything the agent misunderstood.
5. Commit `intent.md`. Author and timestamp join the record, and the product owner picks it up from there.

```markdown
# Intent: claims status self-service
Author: J. Ortiz (claims operations). Status: draft.

## Problem
Customers phone the contact center to ask where their claim is.
Handlers spend roughly a third of call time on status-only queries.

## Proposed outcome
Customers see claim status, next step and expected date in the portal.

## Affected users and systems
Claims handlers, portal team, the claims service.

## Constraints
No new personal data in the portal session. Existing authentication only.

## Open questions
Do third-party loss adjusters need access too?
```

**Governance.** *What is enforced:* the artifact format and the capture step itself, so an intent cannot be accepted into Design without a committed file. *What the evidence is:* the committed `intent.md`, which lists the author, the timestamp, and the full revision history in the version-control history of the intent home. *Where it is logged:* that same history, so any reader can reconstruct the intent and its amendments. *Who approves:* the product owner, and the accept-or-reject decision that sends the intent into Design is recorded as the merge or the closed review.

**Measure.** *Leading:* time from first conversation to a committed `intent.md`, read from the version-control history, which records author and timestamp — the expectation is to fall from a multi-week elicitation cycle to hours. *Lagging:* the survival rate, the share of `intent.md` files the product owner accepts into Design rather than closes, plus the number of changes made to an `intent.md` after the first `spec.md` commit for the same change. Read both: intent files committed faster but closed as often as before means the capture got faster, not the decisions.

## Stage 2 — Design

### Requirements and design in one session

**What changes.** Requirements and design collapse into one session, and policy applies while the spec is written rather than being discovered in a review weeks later.

**Getting started.** An `intent.md`, plus the organization's brand, security, compliance, and experience policies written as skills. Infrastructure: a product owner with agent access; no engineering skill is required.

**Steps.**

1. The product owner opens a session with the organization's skills available and attaches the `intent.md`.
2. The prompt points at the `intent.md`, names the constraints, and demands flagged concerns. Run it by hand first, then codify it as an organization-level command; from there, make the acceptance of `intent.md` the trigger — a non-interactive job fires on the merge, runs the pass with the skills loaded, and commits `spec.md` as a change request.
3. The same product owner reviews the spec against the idea: does the spec solve the stated problem, and are the open questions from `intent.md` answered or carried forward?
4. Work through the flagged concerns first — they are the points an analyst would have escalated. The product owner resolves each with its policy owner before engineering sees the spec.
5. Commit `spec.md` alongside `intent.md`. The file pair records what was asked for and what was decided.
6. The product owner decides whether the spec and intent progress to build, consulting a technical lead for anything the organization classes as higher risk. A human always makes this call, and accepting the spec is what starts the planning pass in Build.

**What it looks like (the prompt).**

```markdown
Read the attached intent.md and produce a requirements and design spec for
integrating it into our existing codebase. Apply the skills available to you
so the plan conforms to our brand guidelines, security policies and
experience standards. Document the spec fully as spec.md, ready to hand to
the engineering team. Describe clearly any areas of concern, especially where
you cannot satisfy contradicting policies.
```

**Governance.** *What is enforced:* the live policy is read and applied while the spec is written, because the skills are loaded into the session rather than recalled afterwards. *What the evidence is:* the spec, the prompt that produced it, and the skill versions in force, all logged in version control. *Where it is logged:* version control, next to the `intent.md` the spec answers. *Who approves:* the product owner signs off the spec and routes flagged concerns to the named policy owners; a technical lead joins for higher-risk work.

**Measure.** *Leading:* elapsed time between the `intent.md` commit and the `spec.md` commit for the same change, against the old requirements-plus-design cycle. *Lagging:* requirements rework after build starts — count `spec.md` commits dated after the first `PLAN.md` commit for the same change. Read both: a shorter design cycle with unchanged rework means the spec was written faster, not that it was better.
