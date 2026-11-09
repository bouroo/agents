# Plays — Build

> Load on demand from [delivery](../SKILL.md): the practices that put the plan, the shared knowledge, and the enforced guardrails in place before the change ships.

## Stage 3 — Build

### Plan first, then implement

**What changes.** Nothing is implemented without an accepted plan. Institutional knowledge becomes files the agent reads, and the guardrails run as code rather than as habits.

**Getting started.** The intent artifact (`intent.md` or `spec.md`) if one exists; the project context file helps. Infrastructure: an agent session with access to the repository.

**Steps.**

1. Start a session in a read-only planning phase, hand it the approved `spec.md`, and let it interview the engineer, iterating on the plan until the engineer is happy with it. The agent can read the codebase without changing anything, so changing course is still a matter of editing a document.
2. Write the plan down before dispatching anything: the files that change, the order of work, the risks, and the proof.
3. Interrogate the plan before accepting it — ask what the change could break, which step is most risky, and what other options were considered and rejected. A plan that has not been questioned has not been tested, and the answers belong in the plan's own **Rejected options** section, not only in the conversation.
4. Iterate until someone who has never seen the conversation could implement the change from the plan alone. That is the completeness test: a plan needing a thread of context to be understood is a document, not a plan.
5. Commit the approved plan as `PLAN.md`. It joins the audit trail, and the review pass in Deploy checks the eventual diff against it.
6. Accept the plan and implement. With a solid plan, the implementation is often a single pass.
7. When implementation departs from the plan, update `PLAN.md` in the same commit. A pre-action check can enforce the synchronization.

```markdown
# Plan: claims status self-service (from intent.md 2026-06-02)

## Files that change
portal/ui/claims/StatusPanel (new), claims-service/routes/status,
claims-service/tests/status

## Order of work
1. Add the status endpoint behind existing auth.
2. Panel against the endpoint.
3. Wire into the portal navigation.

## Risks
The claims service rate-limits; the panel must cache.

## Proof
The status test covers the four claim states; the screenshot matches the
approved mock.
```

**Governance.** *What is enforced:* design review happens before any code is generated, when changing course is still a matter of editing a document — the planning phase enforces this itself, since the agent cannot edit files until the engineer accepts the plan. *What the evidence is:* the committed `PLAN.md` and its revisions, with who accepted it. *Where it is logged:* version control, so the review pass in Deploy can diff the shipped change against the plan. *Who approves:* routine changes are approved by the engineer; anything the organization classes as higher risk goes to a technical lead or architect.

**Measure.** *Leading:* the share of changes that merge from the first implementation pass, and the time from plan approval to merged change request with the required data in the change-request metadata. *Lagging:* rework cycles per change, and how often the merged diff still matches the committed `PLAN.md`. Read both: a fast first pass with unchanged rework means the plan was skipped, not that it worked.

### The project context file

**What changes.** Knowledge that used to sit in people's heads and on wikis becomes a file the agent reads at the start of every session, maintained by the whole team and iterated on whenever a mistake is made.

**Getting started.** A repository and one engineer who knows the codebase well.

**Steps.**

1. Bootstrap a context file from what the repository already shows.
2. Cut it down to what a new joiner would need on day one: the build, test, and lint commands, the conventions that matter, and the things the agent keeps getting wrong.
3. Check it into version control at the repository root so the whole team shares one version and changes are reviewed like code.
4. When the agent makes a mistake twice, the correction goes into the file.
5. Keep it under a page. The agent reads all of it at the start of every session, and anything stale is taking up context for no benefit.

```markdown
# Payments service

## Commands
- Build: the repository's build target, run locally before pushing.
- Test: the unit-test target, and the integration-test target, which needs
  the service container running.
- Lint: the lint target; the continuous-integration pipeline runs it, so
  fix before pushing.

## Conventions
- The service targets the supported runtime version. Do not introduce a new
  dependency without a decision record.
- Monetary amounts use the exact decimal type the domain defines, never a
  floating-point type.
- Every externally reachable route needs an integration test.

## Architecture
- The route layer holds transport concerns, the domain layer holds the
  business rules, the adapter layer talks to external systems.
- Event payloads are defined in the schemas directory; never edit the
  generated classes.

## Things the agent gets wrong
- Do not bump dependency versions; the platform team owns them.
- The legacy module is frozen; changes go in the current module.
```

The commands are named by role — build, unit test, integration test, lint — and each names the single target the agent runs. A context file that lists a stack's commands by name teaches the agent a vendor's vocabulary instead of the repository's; a file that names the target, what it covers, and what a healthy result looks like teaches the practice.

**Governance.** *What is enforced:* the file is version controlled, so the instructions the agent works to are reviewable and auditable. *What the evidence is:* the file's own history, which records who changed which instruction. *Where it is logged:* version control, with changes reviewed like code. *Who approves:* the code owners approve changes to the file in review, and a mistake the agent made twice is the ticket that asks for the change.

**Measure.** *Leading:* how often the agent repeats a mistake the context file should have caught, tracked through its session history. *Lagging:* time to first merged change request for a new member of the team, read from the change-request history. Read both: fewer repeats with unchanged onboarding time means the file serves the agent and not the newcomer, and the second practice needs its own change.

### Skills as institutional knowledge

**What changes.** The organization makes its institutional knowledge operational. The instructions are explicit, version-controlled, applied broadly, and updated centrally when policy changes.

**Getting started.** One policy with a named owner and a written source of truth.

**Steps.**

1. Pick one piece of knowledge enforced inconsistently today — a security standard, an interface design convention, a brand rule.
2. Write it as a skill: a folder with a `SKILL.md` whose frontmatter says when it triggers and whose body says what to do. An engineer writes it from the policy owner's source of truth, using the agent to help.
3. Put the skill in the repository so it ships with the code, or distribute it organization-wide through the organization's skill distribution.
4. Test that the skill triggers: ask for the relevant task in different ways and confirm the skill loads each time.
5. When the policy changes, change the skill and have the policy owner sign off the change.
6. Engineers pick up the new version automatically in their next session.

```markdown
---
name: secure-interface-review
description: Apply the interface security standard. Use whenever creating
  or modifying an externally reachable endpoint, reviewing interface code, or
  producing an interface definition.
---
# Secure interface review

When you create or change an externally reachable endpoint:
1. Authentication: every endpoint requires the gateway credential;
   no anonymous routes outside the health check.
2. Input validation: validate request bodies against the published schema
   and reject unknown fields.
3. Audit: every state-changing endpoint emits an audit event with
   actor, action, entity and timestamp.
4. Data classification: fields tagged personal data in the schema must never
   appear in logs or error messages.

Run the endpoint check script and include its output in your summary.
```

**Governance.** *What is enforced:* a skill is a control, though an advisory one — it makes the agent likely to apply the policy while the code is written, and nothing forces a session to comply. A policy that must always hold needs something deterministic behind the skill — a pre-action check that blocks the action, or a review pass that re-checks the policy at the merge. The skill makes violations rare and the deterministic check makes them close to impossible. *What the evidence is:* the skill file's own version history and the review findings that cite the policy. *Where it is logged:* session traces record skill invocations, and version control records the change. *Who approves:* the policy owner reviews skill changes like code.

**Measure.** *Leading:* time from the policy owner approving a policy change to the updated skill merging, taken from the change request on the skill folder. *Lagging:* review findings that cite the policy, which should fall towards zero once the skill applies the policy while the code is written. Read both: a fast policy-to-skill turnaround with findings unchanged means the skill is not triggering, or its text has drifted from the official policy.

### Pre-action checks as build-time guardrails

**What changes.** A skill is an advisory control; a pre-action check script is the deterministic layer behind it. Most agent actions are file edits and command runs during implementation, so the build phase is where the checks fire most often.

Build-phase checks can block edits to protected paths such as generated code or a frozen module; run the formatter and linter after file edits so drift never accumulates; keep credentials out of the diff.

Back any skill whose policy has to hold without exception. A check runs on each action that matches it, so build-phase checks should be fast and scoped to the file that changed. Heavier checks such as the full test suite belong at the commit or the change request.

A check that asks a human for approval belongs with the gates in Deploy, because an approval prompt during the build puts a person back on the critical path of every session running in parallel.

**Getting started.** One skill whose policy must hold without exception, and the file paths it protects. Infrastructure: a place to put the check script — the repository's shared settings file — so every session inherits it.

**Steps.**

1. Pick the policy that must always hold, and the action it governs: an edit to a generated or frozen path, a formatter that must run after every write, a credential that must never reach the diff.
2. Write the check as a fast, scoped script: it inspects the file that changed, not the whole tree, and it fails loudly rather than silently.
3. Put it in the repository's shared settings file so every session inherits it, and confirm it fires by making the action it guards.
4. Keep the heavier checks out of it. The full test suite belongs at the commit or the change request; a check that is slow gets bypassed or ignored.

**The check script's neutral shape.** Every pre-action check script takes the proposed action as input and returns one of three verdicts — **allow**, **ask**, or **block** — so the same script shape serves a build-time guardrail and an approval gate. The verdict is the exit status, and the script prints the reason, which is what reaches the agent.

```
read the proposed action from standard input
inspect only what the rule covers
allow  -> exit 0, print nothing
ask    -> exit 1, print the named approver and what would satisfy the rule
block  -> exit 2, print the rule and the route to approval
```

The three verdicts are the whole contract: `allow` lets the action proceed, `ask` pauses it until a named person answers, and `block` stops it outright. A script that only ever blocks cannot express a release gate, and a script that only ever allows cannot express a rule.

**Governance.** *What is enforced:* the check fires on every action it matches, so a policy that must apply to every session lives in the shared project configuration rather than in one operator's setup. *What the evidence is:* the check's own verdict and its exit status on each invocation. *Where it is logged:* the session trace, which records what the session did and attributes it to the engineer who ran it. *Who approves:* the code owners, through the review of the shared settings file the check lives in.

**Measure.** *Leading:* the number of build-phase check invocations that blocked an action, and the share of sessions that hit a block, read from the session traces. *Lagging:* policy violations reaching the main branch after the check was installed, from the incident tracker. Read both: a rising block count with unchanged violations means the check fires but the rule it guards does not cover the escape.

### Parallel sessions and subagents

**What changes.** One engineer can drive several streams of work at once. A parallel session is another full session working a separate task in its own checkout; each independent session knows nothing about the others, and the engineer steering them is the only thing they share. A subagent runs inside a single session as a scoped helper with its own context window and tool limits, and suits jobs that recur in multiple tasks.

**Getting started.** The project context file, since all sessions read it. The feedback loop (Stage 4) also helps, because less supervision from the engineer is needed when a session can verify its own work. Infrastructure: a version-controlled repository, since isolation comes from a separate checkout per session and permission settings tuned so sessions are not waiting on approval prompts for commands the organization considers safe.

**Steps.**

1. Split the work into tasks that touch different files, using the plan to see where the work is independent. Tasks that share files run in a single session, one after another.
2. Give each parallel task its own checkout and branch. A separate checkout stops sessions colliding on files.
3. Two or three sessions is a sensible starting point. The practical ceiling is how many streams one person can review properly, so add sessions only while review keeps up.
4. Turn repeated jobs into subagents, each defined in a markdown file with a name, a description of when to use it, and the tools it may touch: a simplifier that strips needless complexity after the main work finishes, a verifier that runs the application and checks behavior, a researcher that explores the codebase and reports back without flooding the main context. Check the definitions into version control so the whole team shares them.

```markdown
---
name: verifier
description: Runs the application and checks the change works before the
  session reports done
---
Start the application using the run target named in the project context
file. Exercise the changed behavior and the two nearest neighboring flows.
Report what you ran, what you saw, and any behavior that does not match the
plan. Do not fix anything; report only.
```

**Autonomy is tiered by guardrail maturity, not only by environment.** A session may run unattended once the guardrails around it have earned it: a tuned context file, skills that encode policy, pre-action checks that block unsafe actions, and a test suite the session can run itself. A tight spec, a small blast radius, and code the tests already cover are the preconditions for letting edits through without a per-edit prompt. The shift is away from a person watching the agent make each edit and towards reviewing artifacts after a longer autonomous session — and those sessions are what make parallelism practical in the first place, since each runs in its own checkout.

The ladder is earned, not assumed: start with the per-edit prompt, drop it as the guardrails above prove themselves, and add it back where a session shows it is not ready. A guardrail that never fires is untested; one that fires constantly is noise.

**Governance.** *What is enforced:* more sessions means more output, so the controls have to come from configuration in the repository — checks and permission settings there apply to all sessions. *What the evidence is:* the session traces, one per session, each attributed. *Where it is logged:* the session traces, forwarded by the organization's observability export. *Who approves:* the code owner reviewing the resulting change request; no session approves its own output.

**Measure.** *Leading:* concurrent sessions per engineer while review quality holds, counted from the session traces, and the share of the day spent steering rather than waiting. *Lagging:* changes merged per engineer per week, read alongside the rework rate from the change-request history. Read both: more sessions with rising rework means the parallelism is outrunning the review, not that the sessions are fast.
