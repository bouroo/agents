# Plays

> Load on demand from [delivery](../SKILL.md): the practices that turn each stage into steps a team can run, and the per-stage measurement pairs that say whether a practice worked.

A **play** is a named practice with five parts: what it changes, how to start, the steps, the governance, and how to measure it. The plays are modular: an organization transforms the stages it needs, in its own order, and a play with no prerequisites is a valid starting point.

## Stage 1 — Plan

### Capture as `intent.md`

**What changes.** An idea stops waiting for someone to write it up. Intent is captured once, in the originator's own words, as a version-controlled artifact the next stage can act on.

**Getting started.** None. Infrastructure: a shared, version-controlled home for intent the product owner watches — for one product, an `intent/` folder in the product repo, so the artifact chain sits next to the code derived from it; a dedicated intent repo earns its overhead only when intent spans many repositories, and in a monorepo it is a directory. Contributors who do not use version control still commit through a connector, so the home's access policy matters.

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
Claims handlers, portal team, claims-core API.

## Constraints
No new PII in the portal session. Existing authentication only.

## Open questions
Do third-party loss adjusters need access too?
```

**Governance.** The evidence is the committed `intent.md`, which lists the author, the timestamp, and the full revision history in the version-control history of the intent home. The product owner approves, and the accept-or-reject decision that sends the intent into Design is recorded as the merge or the closed review.

**Measure.** *Leading:* time from first conversation to a committed `intent.md`, read from the version-control history, which records author and timestamp — the expectation is to fall from a multi-week elicitation cycle to hours. *Lagging:* the survival rate, the share of `intent.md` files the product owner accepts into Design rather than closes, plus the number of changes made to an `intent.md` after the first `spec.md` commit for the same change.

## Stage 2 — Design

### Requirements and design in one session

**What changes.** Requirements and design collapse into one session, and policy applies while the spec is written rather than being discovered in a review weeks later.

**Getting started.** An `intent.md`, plus the organization's brand, security, compliance, and UX policies written as skills. Infrastructure: a product owner with agent access; no engineering skill is required.

**Steps.**

1. The product owner opens a session with the organization's skills available and attaches the `intent.md`.
2. The prompt points at the `intent.md`, names the constraints, and demands flagged concerns. Run it by hand first, then codify it as an organization-level command; from there, make the acceptance of `intent.md` the trigger — a non-interactive job fires on the merge, runs the pass with the skills loaded, and commits `spec.md` as a pull request.
3. The same product owner reviews the spec against the idea: does the spec solve the stated problem, and are the open questions from `intent.md` answered or carried forward?
4. Work through the flagged concerns first — they are the points an analyst would have escalated. The product owner resolves each with its policy owner before engineering sees the spec.
5. Commit `spec.md` alongside `intent.md`. The file pair records what was asked for and what was decided.
6. The product owner decides whether the spec and intent progress to build, consulting a technical lead for anything the organization classes as higher risk. A human always makes this call, and accepting the spec is what starts the planning pass in Build.

**What it looks like (the prompt).**

```markdown
Read the attached intent.md and produce a requirements and design spec for
integrating it into our existing codebase. Apply the skills available to you
so the plan conforms to our brand guidelines, security policies and UX
standards. Document the spec fully as spec.md, ready to hand to the
engineering team. Describe clearly any areas of concern, especially where you
cannot satisfy contradicting policies.
```

**Governance.** The live policy is read and applied while the spec is written. The spec, the prompt that produced it, and the skill versions in force are all logged in version control. The product owner signs off the spec and routes flagged concerns to the named policy owners.

**Measure.** *Leading:* elapsed time between the `intent.md` commit and the `spec.md` commit for the same change, against the old requirements-plus-design cycle. *Lagging:* requirements rework after build starts — count `spec.md` commits dated after the first `PLAN.md` commit for the same change.

## Stage 3 — Build

### Plan first, then implement

**What changes.** Nothing is implemented without an accepted plan. Institutional knowledge becomes files the agent reads, and the guardrails run as code rather than as habits.

**Getting started.** The intent artifact (`intent.md` or `spec.md`) if one exists; the project context file helps. Infrastructure: an agent session with access to the repository.

**Steps.**

1. Start a session in a read-only planning phase, hand it the approved `spec.md`, and let it interview the engineer, iterating on the plan until the engineer is happy with it. The agent can read the codebase without changing anything, so changing course is still a matter of editing a document.
2. Write the plan down before dispatching anything: the files that change, the order of work, the risks, and the proof.
3. Commit the approved plan as `PLAN.md`. It joins the audit trail, and the review pass in Deploy checks the eventual diff against it.
4. Accept the plan and implement. With a solid plan, the implementation is often a single pass.
5. When implementation departs from the plan, update `PLAN.md` in the same commit. A hook can enforce the synchronization.

```markdown
# Plan: claims status self-service (from intent.md 2026-06-02)

## Files that change
portal/src/claims/StatusPanel.tsx (new), claims-api/routes/status.py,
claims-api/tests/test_status.py

## Order of work
1. Add the status endpoint behind existing auth.
2. Panel against the endpoint.
3. Wire into the portal nav.

## Risks
The claims-core API rate-limits at 50 rps; the panel must cache.

## Proof
test_status.py covers the four claim states; screenshot matches the
approved mock.
```

**Governance.** Design review happens before any code is generated, when changing course is still a matter of editing a document. The planning phase enforces this itself, since the agent cannot edit files until the engineer accepts the plan. The plan and its revisions are logged along with who accepted it. Routine changes are approved by the engineer; anything the organization classes as higher risk goes to a tech lead or architect.

**Measure.** *Leading:* the share of changes that merge from the first implementation pass, and the time from plan approval to merged PR with the required data in the PR metadata. *Lagging:* rework cycles per change, and how often the merged diff still matches the committed `PLAN.md`.

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
- Build: make build
- Test: make test (unit), make itest (integration, needs docker)
- Lint: make lint (runs in CI; fix before pushing)

## Conventions
- Java 21, Spring Boot 3. No new Lombok.
- Money is always BigDecimal, never double.
- Every endpoint needs an integration test in src/itest.

## Architecture
- api/ holds REST controllers, core/ holds domain logic,
  adapters/ talks to external systems.
- Kafka events are defined in schemas/; never edit generated classes.

## Things the agent gets wrong
- Do not bump dependency versions; the platform team owns them.
- The legacy v1/ package is frozen; changes go in v2/.
```

**Governance.** The file is version controlled, so the instructions the agent works to are reviewable and auditable. Team conventions apply through the file, changes to it are logged in history, and code owners approve those changes in review.

**Measure.** *Leading:* how often the agent repeats a mistake the context file should have caught, tracked through its history. *Lagging:* time to first merged PR for a new member of the team, read from the PR history.

### Skills as institutional knowledge

**What changes.** The organization makes its institutional knowledge operational. The instructions are explicit, version-controlled, applied broadly, and updated centrally when policy changes.

**Getting started.** One policy with a named owner and a written source of truth.

**Steps.**

1. Pick one piece of knowledge enforced inconsistently today — a security standard, an API design convention, a brand rule.
2. Write it as a skill: a folder with a `SKILL.md` whose frontmatter says when it triggers and whose body says what to do. An engineer writes it from the policy owner's source of truth, using the agent to help.
3. Put the skill in the repository so it ships with the code, or distribute it organization-wide through a plugin marketplace.
4. Test that the skill triggers: ask for the relevant task in different ways and confirm the skill loads each time.
5. When the policy changes, change the skill and have the policy owner sign off the change.
6. Engineers pick up the new version automatically in their next session.

```markdown
---
name: secure-api-review
description: Apply the API security standard. Use whenever creating or
  modifying an external-facing endpoint, reviewing API code, or
  generating an OpenAPI spec.
---
# Secure API review

When you create or change an API endpoint:
1. Authentication: every endpoint requires the gateway JWT;
   no anonymous routes outside /health.
2. Input validation: validate request bodies against the OpenAPI
   schema and reject unknown fields.
3. Audit: every state-changing endpoint emits an audit event with
   actor, action, entity and timestamp.
4. Data classification: fields tagged pii in the schema must never
   appear in logs or error messages.

Run scripts/check-endpoints.sh and include its output in your summary.
```

**Governance.** A skill is a control, though an advisory one. It makes the agent likely to apply the policy while the code is written, and nothing forces a session to comply. A policy that must always hold needs something deterministic behind the skill — a hook that blocks the action, or a review pass that re-checks the policy at the merge. The skill makes violations rare and the hook makes them close to impossible. Skill invocations are logged in session traces, and the policy owner reviews skill changes like code.

**Measure.** *Leading:* time from the policy owner approving a policy change to the updated skill merging, taken from the PR on the skill folder. *Lagging:* review findings that cite the policy, which should fall towards zero once the skill applies the policy while the code is written. Where they do not fall, either the skill is not triggering or its text has drifted from the official policy.

### Hooks as build-time guardrails

**What changes.** A skill is an advisory control; a hook is the deterministic layer behind it. Most agent actions are file edits and shell commands during implementation, so the build phase is where hooks fire most often.

Build-phase hooks can block edits to protected paths such as generated classes or a frozen package; run the formatter and linter after file edits so drift never accumulates; keep credentials out of the diff.

Back any skill whose policy has to hold without exception. A hook runs on each action that matches it, so build-phase hooks should be fast and scoped to the file that changed. Heavier checks such as the full test suite belong at the commit or the merge request.

A hook that asks a human for approval belongs with the gates in Deploy, because an approval prompt during the build puts a person back on the critical path of every session running in parallel.

**Governance.** Controls fire where the work happens, so a control that must apply to every session lives in the repository rather than in one operator's setup. Repository-scoped hooks apply to all sessions, and what a session does is logged and attributed to the engineer who ran it.

**Measure.** *Leading:* the number of build-phase hook invocations that blocked an action, and the share of sessions that hit a block, read from the session traces. *Lagging:* policy violations reaching the main branch after the hook was installed, from the incident tracker.

### Parallel sessions and subagents

**What changes.** One engineer can drive several streams of work at once. A parallel session is another full session working a separate task in its own worktree; each independent session knows nothing about the others, and the engineer steering them is the only thing they share. A subagent runs inside a single session as a scoped helper with its own context window and tool limits, and suits jobs that recur in multiple tasks.

**Getting started.** The project context file, since all sessions read it. The feedback loop (Stage 4) also helps, because less supervision is needed when a session can verify its own work. Infrastructure: a version-controlled repository, since isolation comes from worktrees and permission settings tuned so sessions are not waiting on approval prompts for commands the organization considers safe.

**Steps.**

1. Split the work into tasks that touch different files, using the plan to see where the work is independent. Tasks that share files run in a single session, one after another.
2. Give each parallel task its own worktree and branch. A worktree is a separate checkout, which stops sessions colliding on files.
3. Two or three sessions is a sensible starting point. The practical ceiling is how many streams one person can review properly, so add sessions only while review keeps up.
4. Turn repeated jobs into subagents, each defined in a markdown file with a name, a description of when to use it, and the tools it may touch: a simplifier that strips needless complexity after the main work finishes, a verifier that runs the app and checks behavior, a researcher that explores the codebase and reports back without flooding the main context. Check the definitions into version control so the whole team shares them.

```markdown
---
name: verifier
description: Runs the app and checks the change works before the session
  reports done
tools: Bash, Read
---
Start the app with make run. Exercise the changed behavior and the two
nearest neighboring flows. Report what you ran, what you saw, and any
behavior that does not match plan.md. Do not fix anything; report only.
```

**Governance.** More sessions means more output, so the controls have to come from configuration in the repository. Hooks and permission settings there apply to all sessions, and what a session does is logged and attributed to the engineer who ran it.

**Measure.** *Leading:* concurrent sessions per engineer while review quality holds, counted from the session traces, and the share of the day spent steering rather than waiting. *Lagging:* changes merged per engineer per week, read alongside the rework rate from the PR history.

## Stage 4 — Test

### Give the session a feedback loop

**What changes.** Every session checks its own work before a human sees it, and the configuration that steers the agent gets regression-tested like the code it writes. Always give the agent a way to verify its own work — tests, a build, a screenshot diff. The session checks its own work and fixes its own mistakes before an engineer sees them.

The feedback loop is not the same as a verifier subagent. The loop runs through the whole task as many times as the work; the verifier subagent packages the final check by running a fresh context window once the session believes the work is done, so the verdict is not colored by the assumptions that produced the code.

**Getting started.** A test suite and a build that run locally with one command each. For UI work, a way for the agent to see the result is crucial — a browser tool or a screenshot utility.

**Steps.**

1. If checking the work today takes a sequence of commands and environment knowledge, wrap it in a single target such as `make test` or `npm test` that exits non-zero on failure.
2. In the project context file's Commands section, list each command with an example of a healthy output.
3. Make the target quantifiable so the agent can check the work without asking: "all tests in `test_status.py` pass", "the screenshot matches the attached mock", "the endpoint returns 200 with the new field".
4. For bug fixes, write the failing test first. Ask for the bug to be reproduced as a test, run it, and confirm it fails for the reason expected. Commit that test. Only then ask for a fix without editing the test, with a hook enforcing the restriction. A test that existed before the fix, and that the agent could not rewrite, is proof the bug is gone.
5. For UI work, close the loop with a visual check: implement, screenshot, compare, adjust. Two or three rounds is normal, and the result should improve with each one.
6. Make verification part of "done". The instruction lives in the project context file. Run the checks before reporting a task complete, and show the output.
7. Protect the loop itself, because an agent fixing code must not be able to weaken the check on that code. A hook that blocks edits to test files during a fix task does this; the alternative is to check the diff in review and reject any change that touches a test.

**Governance.** *What is enforced:* verification before a task is reported done, and the block on the agent editing test files during a fix, implemented as hooks where the organization wants them guaranteed. *What the evidence is:* the literal output of the test command, the build log, or the screenshot diff that the agent ran and pasted, so the evidence comes from the toolchain. *Where it is logged:* in the session transcript, which the observability export forwards to the organization's stack, and in the PR's check run, where the reviewer and any later auditor can both see it. *Who approves:* the code owner reviewing the PR, who can concentrate on intent and risk because the mechanical evidence is already attached.

**Measure.** *Leading:* first-pass CI success rate for agent-written changes, which the CI system already supports. *Lagging:* review time per PR, which should fall once the tests catch what reviewers used to catch, and the change failure rate from an incident tracker.

### Continuous evals

**What changes.** Evals are the AI-native equivalent of stage-gate QA: a suite that runs whenever the agent's configuration changes. When a new model is swapped in or a prompt is rewritten, the eval suite says whether the agent still does the work to the same standard. Treat the suite as live: as models improve, cases that once discriminated stop doing so, and new ones must be added from ongoing monitoring.

**Getting started.** The project context file and the feedback loop. Infrastructure: CI that can run the agent non-interactively, and an API key with budget for eval runs.

**Steps.**

1. The platform engineer collects 20 to 50 real tasks from recent work with the expected outcome.
2. Write each task as an eval: the prompt plus the checks that define acceptable — tests pass, lint clean, behavior unchanged, policy followed.
3. The suite runs non-interactively in CI on a schedule and on any change to the context file, skills, or hooks, since that configuration steers the agent and deserves the regression testing code gets.
4. Gate configuration changes on the results. A skill change that drops the pass rate gets reviewed before it merges.
5. Each production incident gets an eval, written by the team that owned the incident, and stays in the suite as a regression test.

**Governance.** Evals give QA a gate that keeps up with agent output. The pass-rate threshold is enforced as a merge check, runs are logged so results can be compared over time, and the team that owns the configuration change approves it.

**Measure.** *Leading:* the eval pass rate over time, reported by the suite on every run, and how long a production incident takes to become a permanent eval. *Lagging:* regressions caught in CI compared with regressions found in production, derived from the incident tracker.

## Stage 5 — Deploy

### Agentic review in both directions

**What changes.** The agent both gives and receives reviews. It reviews incoming changes against the organization's policies and addresses review comments on its own changes. Every change gets an identical set of review passes, with findings ranked by severity. Human attention moves up a level: whether the change does what the plan intended and whether the risk is acceptable.

**Getting started.** An updated project context file; skills if the review passes enforce written policies; defined subagents. Infrastructure: a repository with the review integration installed, either a managed review service enabled by an admin or the agent running in your own CI. Branch protection policies that require a code owner's approval are also worthwhile.

**Steps.**

1. The managed service is the fastest start: an admin enables it and selects repositories. Run the review in your own CI when you need control of the pipeline or want API calls routed through your own cloud agreement.
2. The tech lead writes the review policy at the repository root, divided into the passes the organization cares about: bugs and logical errors; security and vulnerabilities; compliance against the spec, the plan, and design principles. The policy also defines what counts as Important as opposed to a Nit, and what to skip.
3. The tech lead sets the human threshold. Findings do not approve or block a change on their own, and branch protection still requires approval from a code owner. A platform engineer who wants to gate merges on findings reads the severity counts the check run publishes as a machine-readable tally.
4. When a reviewer or the author tags the agent on a review comment, the agent addresses the comment and pushes the fix. The thread records both the request and the change. Teams wrap the loop in a command that sweeps the unresolved review comments and failing checks, addresses them, and pushes the fixes, until the change is green and waiting only on code owner approval.
5. Review findings feed back into the context file. When a review flags a mistake for the second time, the correction goes in as part of that review, and because review reads the file the mistake is caught from the next change onwards. Review also flags when a change has made the file outdated.
6. Once a month the tech lead tunes the setup by rating findings so the reviewer improves, and by capping Nit volume in the policy. Generated paths and anything CI already enforces are excluded.

```markdown
# Review instructions

## Passes
Run three passes and tag each finding with its pass:
- Bugs: logic errors, broken edge cases, subtle regressions
- Security: injection risks, authentication gaps, PII in logs
- Compliance: the change matches spec.md, PLAN.md and our design principles

## What Important means here
Reserve Important for findings that would break behavior, leak data
or breach a policy. Style and naming are nits.

## Cap the nits
Report at most five nits per review; summarize the rest as a count.

## Do not report
Generated files under src/gen/ and anything CI already enforces.
```

**Governance.** Separation of duties is preserved, because the agent that wrote the code has no way to approve it. The review policy applies to all changes, and findings, fixes, ratings, and approvals are logged in the PR history, so the PR is the audit record. Approval comes from a human through branch protection, informed by the findings.

**Measure.** *Leading:* time to first review, which should fall to minutes, and the share of review comments resolved without a human touching the branch, with data stored directly on the version-control platform. *Lagging:* defects and vulnerabilities caught before merge set against those escaping to production, from the PR history and the incident tracker.

### Hooks as approval gates

**What changes.** A hook can also ask, pausing the action until a specific person approves, which is what release gating needs. The play sits in Deploy because the release gate is the clearest case, but hooks are not deploy-specific: they run wherever the agent acts. They can block edits to migrations and infrastructure without a change ticket during Build, and stop the agent editing test files during a fix task in Test.

**Getting started.** A written list of the approvals the change process requires.

**Steps.**

1. Engineering leadership, with change management and compliance, lists the human approval gates that must survive: change management sign-off, release authorization, edits to protected paths.
2. The platform engineer expresses each gate as a hook — a script that runs before the agent acts and can allow, ask, or block.
3. Team hooks go in the repository's shared settings file; non-negotiable hooks go in managed settings owned by the platform or IT admin, where individual engineers cannot switch them off.
4. A block should explain itself, so when a hook stops an action the reason and the route to approval appear in the agent's output.

```json
{
    "hooks": {
      "PreToolUse": [
        {
          "matcher": "Bash",
          "hooks": [
            { "type": "command",
              "command": "${PROJECT_DIR}/hooks/production-gate.sh" }
          ]
        }
      ]
    }
}
```

**And the gate itself.**

```bash
#!/bin/bash
# Production deploys require a named release authorization
cmd=$(jq -r '.tool_input.command' < /dev/stdin)
if [[ "$cmd" == *"deploy"* && "$cmd" == *"production"* ]]; then
   if [ -z "$RELEASE_APPROVAL" ]; then
     echo "Production deploys need a release authorization." >&2
     exit 2 # exit 2 blocks the action; the message goes to the agent
   fi
fi
exit 0
```

**Managed controls.** A team hook lives in the repository and an engineer can weaken it; a control the organization declares non-negotiable lives in **managed settings** owned by the platform or IT admin, deployed by device management or an admin console, where no engineer, project file, or command-line flag can widen or switch off the rules. The layers stack, and each closes a gap the one below it leaves:

- **Permission deny rules** keep secrets out of the agent's context and block arbitrary network egress through its tools; the matching **allow rules** pre-approve the safe inner loop, so the deny list does not turn into prompt fatigue.
- **Disabling the bypass mode, and allowing only managed permission rules**, means no engineer, project file, or flag can widen the rules.
- **A sandbox** closes the gap permissions cannot: a tool-level deny on web fetches does not stop a shell command reaching the network, so an OS-level domain allowlist blocks egress outright. Making the sandbox fail when it cannot initialize, and refusing to retry a failed command outside it, turns it into a gate rather than a suggestion.
- **Credential rules** close the gap the deny list leaves: a sandboxed shell command can still read an SSH key or a cloud credential file by default, so those reads are denied and the named secrets are stripped from the environment of every sandboxed command.
- **Allowing only managed hooks** means the approval gates above are the only hooks that run, so nothing local can add to or replace them.
- **Restricting marketplaces** means every skill, agent, hook, and tool server on an engineer's machine arrived through the organization's approved source, never from a home directory; allowing only managed tool servers makes the agent's tool surface an allowlist the platform team owns.
- **A minimum version floor** refuses to start below the approved release, so the controls are enforced by a build the organization has actually assessed.

Treat this as a starting point to tailor, not a template to copy: every deny trades against capability, and the right balance depends on the data classification of the repository.

**Governance.** Hooks are the approval gates. The gate condition is enforced every time, for everyone. Allow and block decisions are logged with a timestamp. The gate also defines what counts as approval, whether that is an approved change ticket or the release manager's sign-off.

**Measure.** *Leading:* time spent waiting on each approval gate; every hook decision is written to the observability export with a timestamp and an allow-or-block verdict, so the wait is visible per gate. *Lagging:* gate violations reaching production before and after hooks, from the incident tracker.

### CI/CD integration and deployment

**What changes.** Run the agent non-interactively inside the pipeline, sandbox the execution so long-running agents run safely, expose deployment through tool integrations, and rehearse the rollback paths before the agent ever needs them. The agent runs non-interactively inside the pipeline for the judgment steps, in a sandbox with scoped credentials. Deployment tooling is exposed through an allowlist of tools scoped per environment, so the workflow that wrote and tested the change can also ship it and roll it back, inside the gates the organization defines.

**Getting started.** The agent in the review loop and hooks as approval gates, because the gates must exist before automation accelerates anything through them. Infrastructure: a CI platform that can run the agent non-interactively, model access through the API or a cloud agreement where traffic must stay in-house, tool integrations for the deployment targets, and a sandbox profile for agent jobs with no standing production credentials.

**Steps.**

1. Start with read-only judgment steps. Run the agent non-interactively in a pipeline job to triage a failed build, summarize a flaky test, or draft the changelog.
2. Add write steps behind the existing gates for jobs like fixing lint, updating generated docs, or addressing review comments. Anything the agent writes arrives as a pull request through branch protection, and the agent has no route to push to the main branch.
3. Sandbox the execution. Agent jobs run in containers under a network policy with short-lived scoped tokens, and hold no production credentials by default.
4. Expose deployment through tools. Deploy, status, and rollback become allowlisted operations scoped per environment, so the agent's deployment powers are a list rather than a shell script with credentials.
5. Tier the autonomy by environment. In development the agent deploys freely. In production the agent prepares the release and the release manager authorizes it, and a hook enforces the production gate. Staging sits somewhere in the middle.
6. Rollback should be the most rehearsed path in the pipeline — a single command the agent can run, exercised regularly in staging. The closing-the-loop play in Maintain calls this rollback when a control band is breached, so it has to be proven in advance.

**Governance.** The governing principle is that the agent may act up to the production gate and cannot pass it. Branch protection turns anything the agent writes into a pull request, with no direct path to the main branch. The production deploy hook blocks the release until a named release manager authorizes it. Each non-interactive run acts under the agent's own identity, so the pipeline log separates what the agent did from what the engineer who triggered it did. Per-environment permission tiers set how much the agent may do on the way to the gate.

**Measure.** *Leading:* the share of pipeline failures triaged without paging a human, taken from the CI logs. *Lagging:* delivery and operational metrics, which the CI system and deployment tooling already emit.

## Stage 6 — Maintain

### Closing the loop

**What changes.** The loop closes. A trigger invokes the agent with no person in the invocation path, and what it finds re-enters the pipeline as `intent.md`. A continuously running monitoring agent could, off the back of a bug ticket being raised, create an `intent.md` and flow through the requirements, plan, build, test, and review phases. Maintain runs headless, with an independent confidence gate between stages — a deterministic check or an adversarial reviewing agent — deciding whether the previous stage's output continues or escalates to a human.

**Getting started.** The `intent.md` format that gives the loop a structured output to restart. The agent accelerated PR reviews, hooks as an action boundary, and a rollback path for the pipeline (which the highest autonomy tier invokes). Infrastructure: a metrics store the detection script can query, read access to the repository, a way to run the agent non-interactively, or an agent service that receives webhooks.

**Steps.**

1. The service owner or platform engineer picks one metric with a stable rolling baseline, such as CI test failure rate, post-deploy error rate, or PR cycle time.
2. They write the detection script — typically mean and standard deviation over a rolling window with rules that catch slow drift as well as spikes. The script is version controlled and unit tested, and detection stays entirely deterministic, with no model involved.
3. Response tiers are defined in version-controlled config. At one deviation the script only logs; at two it invokes the agent read-only to diagnose; at three the agent may act, though only by opening a pull request into the review gate or triggering a pre-approved runbook.
4. The trigger layer can be a scheduled workflow, a webhook from the existing monitoring stack, or a timer inside the network. The agent runs stateless, either as a non-interactive step on a CI runner or as a service in a sandboxed container. Because the run is stateless and non-interactive, a loop can begin and end without anyone starting it.
5. The agent writes its diagnosis as `intent.md` in the Plan format, covering the anomaly and its evidence, a proposed outcome, the affected systems, and any open questions. From there the finding goes through the pipeline like anything else.
6. The service owner or on-call engineer triages the queue, routing product-facing findings to the product owner: fix now, schedule, or dismiss. Dismissals tune the bands and help reduce noise.
7. When a fix ships, add an eval for the incident, so such issues are protected against going forwards.

```yaml
metric: ci_test_failure_rate
baseline: rolling_30d
rules: western_electric
tiers:
  1sigma: { action: log }
  2sigma: { action: diagnose,
            tools: "Read,Grep,Bash(gh run view *)" }
  3sigma: { action: propose,
            routes: [pull_request, runbook:rollback-deploy] }
```

**Governance.** The tier boundaries are enforced from version-controlled config, with permissions and managed settings denying production access. Invocations, findings, and triage decisions are logged with a timestamp. A service owner triages and approves findings, resulting changes go through the normal review gate, and the runbooks the agent may trigger were approved in advance.

**Measure.** *Leading:* time from band breach to an `intent.md` in the triage queue, against the old time from incident to post-mortem action; the detection script's log has the breach timestamp and the tier. *Lagging:* the share of findings that become merged fixes — triage queue against actual PR history — and repeat incidents of the same class, which should fall as the fixes add cases to the eval suite.

**Worked examples.**

- When the CI test failure rate breaches the third tier, the agent quarantines the flaky test or opens a revert PR, and the review gate decides.
- When the post-deploy error rate breaches the third tier with a deployment in the window, the agent triggers the existing rollback pipeline.
- When PR cycle time trips a drift rule, the agent writes a report for engineering leadership, which shows the harness works for process metrics as well as production ones.

### Recurring codebase scans

**What changes.** A security scan is a point-in-time statement about a codebase under a particular model, and both halves go stale: the code changes every week, and each model generation finds vulnerabilities the previous one missed. The AI-native answer is to run the scan on a schedule, without a human in the invocation path, and send what it finds through the same gates as any other change.

**Getting started.** The review gate and hooks as approval gates, so findings go through review like any other change, and the `intent.md` format for findings too large for a single change. Infrastructure: a hosted scanning service, or a scheduled job running the agent non-interactively against each repository.

**Steps.**

1. The security lead connects the repositories and organizes them into projects by repo, service, or team, so ownership of findings is clear from the start.
2. Run a first full scan of the most critical repositories, including ones scanned before by other tools or earlier models. Treat the first scan as the baseline; it will likely surface findings in code that was considered clean.
3. Set a schedule per project. Weekly is a sensible default for actively developed services; scope scans to a directory or branch where a repository is large or mixed.
4. Triage findings with the confidence rating in hand. Dismiss with a reason, so the dismissal is recorded and the same finding does not return as new on the next run.
5. For a bounded finding, open the suggested patch, review it, and send it through the review gate like any other change. The agent that proposed the fix has no route to approve it.
6. For anything wider than one patch, such as an architectural weakness or a pattern repeated across services, write it up as `intent.md` in the Plan format and start it at Plan.
7. When a fix is released to production, add an eval for the vulnerability class to the suite, so the configuration that steers the agent is tested against that class from then on.
8. Export findings to the organization's existing tracker and audit systems, where auditors already expect them.

**Governance.** The scan runs under the organization's admin controls: which repositories are connected, who holds a scan seat, and the spend limit are all set centrally. Every finding has a validation result and a confidence rating, and every dismissal has a reason, so the scan history is an audit record of what was found, fixed, and consciously accepted. Fixes reach production through the review gate and branch protection rather than from the scan itself. The scan augments existing static analysis and dependency scanning; the deterministic checks stay in CI, and the model-driven scan covers the context-dependent vulnerabilities those checks are not built to find.

**Measure.** *Leading:* share of connected repositories on a schedule, and time from a finding being reported to its patch entering the review gate, read from the scan history and the PR metadata. *Lagging:* vulnerabilities found by the scheduled scan set against those found in production or by external report, from the incident tracker; and the trend in findings per scan on repositories that have been through several runs, which should fall as fixes and evals accumulate.

### Incidents arriving from anywhere

Incidents can arrive through channels other than a monitoring system — a ticket, a message on an incident channel, an external report. The agent can be a member of those channels under its own identity, so each new incident gets a first responder and the response itself becomes part of the loop and the memory for future incidents.

The conversation and institutional knowledge stay in the channel, with anyone in the channel able to guide and action the response. Any team member can test hypotheses, explore new options, and investigate in real time, with the channel history adding to the auditability. Through the tool integrations the agent verifies the metric is back at baseline and confirms it in the thread, writes the post-mortem to a version-controlled lessons file that future investigations can read, and triages work the same way: a small, well-bounded fix arrives as a pull request through the review gate, and anything larger is written up as `intent.md` for Plan, at which point the loop starts feeding itself.

## Choosing where to start

The plays are independent enough to adopt in any order, and the dependency is not the same as the order: a play with no prerequisites needs nothing first, and every other play names what it builds on.

1. **Plan** — capture as `intent.md` needs nothing. It is the cheapest change with the largest effect on the stages to its left.
2. **Design** — needs an `intent.md` and the policies written as skills.
3. **Build** — the project context file, the skills, and the hooks each need the one before; the context file needs only a repository.
4. **Test** — the feedback loop needs the context file's commands; the evals need the feedback loop.
5. **Deploy** — the review policy needs the context file; the approval gates need the written list of approvals; the pipeline needs both.
6. **Maintain** — closing the loop needs the `intent.md` format, the approval gates, and a rehearsed rollback path.

**Measure the loop, not the tasks.** Each play names a leading indicator — something that moves before the outcome — and a lagging indicator — the outcome itself. Read both together: a leading indicator that improves while the lagging one does not means the practice measures activity, not progress.
