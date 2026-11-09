# Plays — Deploy

> Load on demand from [delivery](../SKILL.md): the practices that review a change, gate it, and ship it under a pipeline that enforces the same rules for everyone.

## Stage 5 — Deploy

### Agentic review in both directions

**What changes.** The agent both gives and receives reviews. It reviews incoming changes against the organization's policies and addresses review comments on its own changes. Every change gets an identical set of review passes, with findings ranked by severity. Human attention moves up a level: whether the change does what the plan intended and whether the risk is acceptable.

**Getting started.** An updated project context file; skills if the review passes enforce written policies; defined subagents. Infrastructure: a repository with the review integration installed, either a managed review service enabled by an administrator or the agent running in your own pipeline. Branch protection policies that require a code owner's approval are also worthwhile.

**Steps.**

1. The managed service is the fastest start: an administrator enables it and selects repositories. Run the review in your own pipeline when you need control of the pipeline or want model traffic routed through your own agreement.
2. The technical lead writes the review policy at the repository root, divided into the passes the organization cares about: bugs and logical errors; security and vulnerabilities; compliance against the spec, the plan, and design principles. The policy also defines what counts as Important as opposed to a Nit, and what to skip.
3. The technical lead sets the human threshold. Findings do not approve or block a change on their own, and branch protection still requires approval from a code owner. A platform engineer who wants to gate merges on findings reads the severity counts the check run publishes as a machine-readable tally.
4. When a reviewer or the author tags the agent on a review comment, the agent addresses the comment and pushes the fix. The thread records both the request and the change. Teams wrap the loop in a command that sweeps the unresolved review comments and failing checks, addresses them, and pushes the fixes, until the change is green and waiting only on code owner approval.
5. Review findings feed back into the context file. When a review flags a mistake for the second time, the correction goes in as part of that review, and because review reads the file the mistake is caught from the next change onwards. Review also flags when a change has made the file outdated.
6. Once a month the technical lead tunes the setup by rating findings so the reviewer improves, and by capping Nit volume in the policy. Generated paths and anything the pipeline already enforces are excluded.

```markdown
# Review instructions

## Passes
Run three passes and tag each finding with its pass:
- Bugs: logic errors, broken edge cases, subtle regressions
- Security: injection risks, authentication gaps, personal data in logs
- Compliance: the change matches spec.md, PLAN.md and our design principles

## What Important means here
Reserve Important for findings that would break behavior, leak data
or breach a policy. Style and naming are nits.

## Cap the nits
Report at most five nits per review; summarize the rest as a count.

## Do not report
Generated files under the generated directory and anything the pipeline
already enforces.
```

**Governance.** *What is enforced:* separation of duties is preserved, because the agent that wrote the code has no way to approve it — the review policy applies to all changes, and branch protection still demands the code owner. *What the evidence is:* the findings, the fixes, the ratings, and the approvals, all recorded in the change request history. *Where it is logged:* the change request history, which makes the change request the audit record. *Who approves:* a human through branch protection, informed by the findings.

**Measure.** *Leading:* time to first review, which should fall to minutes, and the share of review comments resolved without a human touching the branch, with data stored directly on the version-control platform. *Lagging:* defects and vulnerabilities caught before merge set against those escaping to production, from the change request history and the incident tracker. Read both: faster first review with unchanged escape rate means the review is shallower, not that the change is safer.

### Pre-action checks as approval gates

**What changes.** A pre-action check script can also ask, pausing the action until a specific person approves, which is what release gating needs. The play sits in Deploy because the release gate is the clearest case, but the checks are not deploy-specific: they run wherever the agent acts. They can block edits to migrations and infrastructure without a change ticket during Build, and stop the agent editing test files during a fix task in Test.

**Getting started.** A written list of the approvals the change process requires.

**Steps.**

1. Engineering leadership, with change management and compliance, lists the human approval gates that must survive: change management sign-off, release authorization, edits to protected paths.
2. The platform engineer expresses each gate as a check script that runs before the agent acts and can allow, ask, or block.
3. Team checks go in the repository's shared settings file; non-negotiable checks go in organization-managed settings owned by the platform or IT administration, where individual engineers cannot switch them off.
4. A block should explain itself, so when a check stops an action the reason and the route to approval appear in the agent's output.

**The gate's neutral shape.** A gate is one check script with three verdicts, and the verdict is the exit status:

| Verdict | Exit status | Meaning |
| --- | --- | --- |
| allow | 0 | the rule does not apply; the action proceeds |
| ask | 1 | the action waits for a named approver; the script prints who and what would satisfy the rule |
| block | 2 | the action is refused; the script prints the rule and the route to approval |

```
read the proposed action from standard input
if the rule does not cover the action:
    exit 0                      # allow
if a named approval is already recorded for this action:
    exit 0                      # allow
if the rule permits a person to approve:
    print "waiting on <named approver>; <what would satisfy the rule>"
    exit 1                      # ask
print "<rule violated>; <route to approval>"
exit 2                          # block
```

The gate defines what counts as approval — the recorded authorization, the named role, or the change ticket — and it checks that definition rather than assuming one. The same shape serves a build-time guardrail and a release gate, so an organization has one mechanism and one audit trail, not two.

**The control ladder.** Controls come in layers, and each layer closes a gap the one below leaves:

1. **Advisory** — prose policy, a project context file, a skill. It makes a violation rare, because the agent applies the policy as it writes rather than discovering it in a review weeks later. It cannot guarantee anything, because nothing forces a session to comply.
2. **Project-level deterministic** — a pre-action check script that can allow, ask, or block, a check that exits non-zero, a branch rule demanding a named approval, a sandbox whose refusal to initialize means the command does not run unsandboxed. This is where most of the enforcement belongs, because a control that must apply to every session lives in the shared project configuration and every session inherits it. **A control an individual can switch off is not a control.**
3. **Organization-managed** — owned by the platform or IT administration and deployed centrally, where no individual, project file, or command-line flag can widen or switch off the rules. This tier exists because the project tier is still one person's configuration away from being widened.

Each tier closes a specific gap left open below it:

- **Permission deny rules matching allow rules.** Deny rules keep secrets out of the agent's context and block arbitrary network egress through its tools; the matching allow rules pre-approve the safe inner loop, so the deny list does not turn into prompt fatigue.
- **A sandbox.** Permissions cannot close every gap: a tool-level deny on network fetches does not stop a command reaching the network, so an environment-level allowlist blocks egress outright. Making the sandbox fail when it cannot initialize, and refusing to retry a failed command outside it, turns it into a gate rather than a suggestion.
- **Credential denial at the filesystem and environment level.** A sandboxed command can still read a key file or a credential store by default, so those reads are denied and the named secrets are stripped from the environment of every sandboxed command.
- **Managed-only extensions and tool servers.** Allowing only organization-managed extensions and tool servers makes the agent's tool surface an allowlist the platform team owns, so nothing local can add to or replace it.
- **A version floor.** Refusing to start below the approved version means the controls are enforced by a build the organization has actually assessed, not by whatever version a machine happens to carry.

Treat the ladder as a starting point to tailor, not a template to copy: every deny trades against capability, and the right balance depends on the data classification of the repository.

**Governance.** *What is enforced:* the check scripts are the approval gates. The gate condition is enforced every time, for everyone — a release that passed the gate last week passes this week, and no engineer routes around it. *What the evidence is:* each allow and block decision, logged with a timestamp, together with the gate that produced it. *Where it is logged:* the organization's observability export, and the change request history for gated merges, so a later reader can reconstruct who released what and on which authorization. *Who approves:* the gate defines what counts as approval — a named release authorization, a change-management sign-off, or a recorded change ticket — and that definition belongs to the gate, not to the agent's reading of it.

**Measure.** *Leading:* time spent waiting on each approval gate; every check decision is written to the observability export with a timestamp and an allow-or-block verdict, so the wait is visible per gate. *Lagging:* gate violations reaching production before and after the checks, from the incident tracker. Read both: shorter waits with unchanged violations means the gate is being approved without being read, which is a gate that has become a formality.

### Pipeline integration and deployment

**What changes.** Run the agent non-interactively inside the continuous-integration pipeline, sandbox the execution so long-running agents run safely, expose deployment through allowlisted tool operations, and rehearse the rollback paths before the agent ever needs them. The agent runs non-interactively inside the pipeline for the judgment steps, in a sandbox with scoped credentials. Deployment tooling is exposed through an allowlist of operations scoped per environment, so the workflow that wrote and tested the change can also ship it and roll it back, inside the gates the organization defines.

**Getting started.** The agent in the review loop and the pre-action checks as approval gates, because the gates must exist before automation accelerates anything through them. Infrastructure: a continuous-integration pipeline that can run the agent non-interactively, model access through the organization's own agreement where traffic must stay in-house, tool operations for the deployment targets, and a sandbox profile for agent jobs with no standing production credentials.

**Steps.**

1. Start with read-only judgment steps. Run the agent non-interactively in a pipeline job to triage a failed build, summarize a flaky test, or draft the changelog.
2. Add write steps behind the existing gates for jobs like fixing lint, updating generated docs, or addressing review comments. Anything the agent writes arrives as a change request through branch protection, and the agent has no route to push to the main branch.
3. Sandbox the execution. Agent jobs run under a network policy with short-lived scoped tokens, and hold no production credentials by default.
4. Expose deployment through allowlisted operations. Deploy, status, and rollback become listed operations scoped per environment, so the agent's deployment powers are a list rather than a shell script with credentials.
5. Tier the autonomy by environment. In development the agent deploys freely. In production the agent prepares the release and the release manager authorizes it, and a check script enforces the production gate. Staging sits somewhere in the middle.
6. Rollback should be the most rehearsed path in the pipeline — a single operation the agent can run, exercised regularly in staging. The closing-the-loop play in Maintain calls this rollback when a control band is breached, so it has to be proven in advance.

**The pipeline's neutral shape.** The pipeline is a set of jobs, each with a declared trigger, a sandboxed execution context, and an exit status. What the pipeline must do, whatever drives it:

- **Trigger.** A job runs on a named event — a change merged, a branch updated, a schedule, a request from an external service — and on nothing else. A trigger nobody can name is a job that fires by surprise.
- **Environment.** The job runs sandboxed, with short-lived scoped credentials and a network policy, and holds no standing production credential.
- **Gates.** Every job that writes passes through the same gates a session passes through, so the pipeline does not become the path around the approval gates.
- **Exit status.** Each job exits non-zero on failure, and a failed job stops the ones that depend on it rather than letting them run on stale state.
- **Evidence.** The job's log, its exit status, and the artifacts it produces are retained, so a later reader can see what ran, what it decided, and what it changed.
- **Identity.** Each non-interactive run acts under the agent's own identity, so the pipeline log separates what the agent did from what the engineer who triggered it did.

**Governance.** *What is enforced:* the agent may act up to the production gate and nothing past it. Branch protection turns anything the agent writes into a change request, with no direct path to the main branch, and the production gate check blocks the release until a named release manager authorizes it. *What the evidence is:* the pipeline log, the check run attached to the change request, and the release record with its authorization. *Where it is logged:* the pipeline's run history and the release record, both queryable afterwards. *Who approves:* the release manager, for the production step; per-environment permission tiers set how much the agent may do on the way to that gate.

**Measure.** *Leading:* the share of pipeline failures triaged without paging a human, taken from the pipeline logs. *Lagging:* delivery and operational metrics, which the pipeline and the deployment tooling already emit, read against the incident tracker. Read both: fewer pages with unchanged operational metrics means the triage is closing tickets, not the incidents.
