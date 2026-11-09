# Plays — Maintain

> Load on demand from [delivery](../SKILL.md): the practices that detect a breached control band, close the loop into a new intent, and bring findings back through the same gates.

## Stage 6 — Maintain

### Closing the loop

**What changes.** The loop closes. A trigger invokes the agent with no person in the invocation path, and what it finds re-enters the pipeline as `intent.md`. A continuously running monitoring agent could, off the back of a bug ticket being raised, create an `intent.md` and flow through the requirements, plan, build, test, and review phases. Maintain runs headless, with an independent confidence gate between stages — a deterministic check or an adversarial reviewing agent — deciding whether the previous stage's output continues or escalates to a human.

**Getting started.** The `intent.md` format that gives the loop a structured output to restart. The agent accelerated change request reviews, the pre-action checks as approval gates, and a rollback path for the pipeline (which the highest autonomy tier invokes). Infrastructure: a metrics store the detection script can query, read access to the repository, a way to run the agent non-interactively, or an agent service that receives notifications.

**Steps.**

1. The service owner or platform engineer picks one metric with a stable rolling baseline, such as test failure rate, post-deploy error rate, or change request cycle time.
2. They write the detection script — typically mean and standard deviation over a rolling window with rules that catch slow drift as well as spikes. The script is version controlled and unit tested, and detection stays entirely deterministic, with no model involved in deciding that something happened.
3. Response tiers are defined in version-controlled config. At one deviation the script only logs; at two it invokes the agent read-only to diagnose; at three the agent may act, though only by opening a change request into the review gate or triggering a pre-approved runbook.
4. The trigger layer can be a scheduled workflow, a notification from the existing monitoring stack, or a timer inside the network. The agent runs stateless, either as a non-interactive step on a pipeline runner or as a service in a sandboxed container. Because the run is stateless and non-interactive, a loop can begin and end without anyone starting it.
5. The agent writes its diagnosis as `intent.md` in the Plan format, covering the anomaly and its evidence, a proposed outcome, the affected systems, and any open questions. From there the finding goes through the pipeline like anything else.
6. The service owner or on-call engineer triages the queue, routing product-facing findings to the product owner: fix now, schedule, or dismiss. Dismissals tune the bands and help reduce noise.
7. When a fix ships, add an eval for the incident, so such issues are protected against going forwards.

**The detection order.** The sequence matters and is not compressible: **detection decides the tier, and only then is the agent invoked.** A detector that watches a control band — a rolling baseline and its breach rules — is deterministic and owns the decision that something happened and how bad it is. The tier it selects then sets what the agent may do: **log** it, **diagnose it read-only**, or **propose** through the review gate. The agent never decides its own tier, and a tier is never widened by the agent that runs inside it. The finding re-enters as a new **intent artifact** in the Plan format, so the loop starts again at Plan rather than inside a stage.

**The tier configuration's neutral shape.** The band and the tiers live in one version-controlled file, so the configuration that grants the agent its powers is the configuration a reviewer reads:

```yaml
metric: test_failure_rate
baseline: rolling_30d
rules: standard_deviation_bands
tiers:
  1sigma: { action: log }
  2sigma: { action: diagnose,
            tools: "read, search, non-mutating commands" }
  3sigma: { action: propose,
            routes: [change_request, runbook:rollback_deploy] }
```

Each tier names an **action** and nothing else: `log` writes the breach to the log and stops; `diagnose` adds read-only tools and produces a diagnosis; `propose` adds the routes into the review gate. A tier that names an action outside that set is a tier the agent has been given a promotion it did not earn.

**Governance.** *What is enforced:* the tier boundaries come from version-controlled config, and the permissions and organization-managed settings deny the agent production access beyond the tier it was given. The detection script decides the tier before the agent is invoked, so the agent cannot widen its own scope. *What the evidence is:* the breach record — the metric, the band, the tier, and the timestamp — plus the finding's intent artifact. *Where it is logged:* invocations, findings, and triage decisions are logged with a timestamp. *Who approves:* a service owner triages and approves findings, resulting changes go through the normal review gate, and the runbooks the agent may trigger were approved in advance.

**Measure.** *Leading:* time from band breach to an `intent.md` in the triage queue, against the old time from incident to post-mortem action; the detection script's log has the breach timestamp and the tier. *Lagging:* the share of findings that become merged fixes — triage queue against actual change request history — and repeat incidents of the same class, which should fall as the fixes add cases to the eval suite. Read both: a faster detection-to-queue time with no more merged fixes means the queue is filling, not that the loop closes.

**Worked examples.**

- When the test failure rate breaches the third tier, the agent quarantines the flaky test or opens a revert change request, and the review gate decides.
- When the post-deploy error rate breaches the third tier with a deployment in the window, the agent triggers the existing rollback pipeline.
- When change request cycle time trips a drift rule, the agent writes a report for engineering leadership, which shows the harness works for process metrics as well as production ones.

### Recurring codebase scans

**What changes.** A security scan is a point-in-time statement about a codebase under a particular model, and both halves go stale: the code changes every week, and each model generation finds vulnerabilities the previous one missed. The AI-native answer is to run the scan on a schedule, without a human in the invocation path, and send what it finds through the same gates as any other change.

**Getting started.** The review gate and the pre-action checks as approval gates, so findings go through review like any other change, and the `intent.md` format for findings too large for a single change. Infrastructure: a hosted scanning service, or a scheduled job running the agent non-interactively against each repository.

**Steps.**

1. The security lead connects the repositories and organizes them into projects by repository, service, or team, so ownership of findings is clear from the start.
2. Run a first full scan of the most critical repositories, including ones scanned before by other tools or earlier models. Treat the first scan as the baseline; it will likely surface findings in code that was considered clean.
3. Set a schedule per project. Weekly is a sensible default for actively developed services; scope scans to a directory or branch where a repository is large or mixed.
4. Triage findings with the confidence rating in hand. Dismiss with a reason, so the dismissal is recorded and the same finding does not return as new on the next run.
5. For a bounded finding, open the suggested patch, review it, and send it through the review gate like any other change. The agent that proposed the fix has no route to approve it.
6. For anything wider than one patch, such as an architectural weakness or a pattern repeated across services, write it up as `intent.md` in the Plan format and start it at Plan.
7. When a fix is released to production, add an eval for the vulnerability class to the suite, so the configuration that steers the agent is tested against that class from then on.
8. Export findings to the organization's existing tracker and audit systems, where auditors already expect them.

**Governance.** *What is enforced:* the scan runs under the organization's administrative controls — which repositories are connected, who holds a scan seat, and the spend limit are all set centrally — and every fix reaches production through the review gate and branch protection rather than from the scan itself. *What the evidence is:* every finding's validation result and confidence rating, and every dismissal's reason, so the scan history is an audit record of what was found, fixed, and consciously accepted. *Where it is logged:* the organization's tracker and audit systems, alongside the change request history of the fixes. *Who approves:* the code owner reviewing each fix; the security lead owns the dismissal reasons.

**Measure.** *Leading:* share of connected repositories on a schedule, and time from a finding being reported to its patch entering the review gate, read from the scan history and the change request metadata. *Lagging:* vulnerabilities found by the scheduled scan set against those found in production or by external report, from the incident tracker; and the trend in findings per scan on repositories that have been through several runs, which should fall as fixes and evals accumulate. Read both: a faster route to the review gate with a flat finding count means the scanner is finding the same things faster, not that the codebase is safer.

### Incidents arriving from anywhere

**What changes.** Incidents can arrive through channels other than a monitoring system — a ticket, a message on an incident channel, an external report. The agent can be a member of those channels under its own identity, so each new incident gets a first responder and the response itself becomes part of the loop and the memory for future incidents.

**Getting started.** A channel the agent can be reached on, and the incident categories it may answer without a human. Infrastructure: the same tool operations the closing-the-loop play uses, so the agent can verify a metric is back at baseline.

**Steps.**

1. The agent answers under its own identity, so the request, the diagnosis, the human authorization, and the fix all stay where the incident was handled — the channel history is the audit trail.
2. Anyone in the channel can guide and action the response: hypotheses are tested in real time, and the conversation keeps the institutional knowledge.
3. The agent verifies through its tool operations that the metric is back at baseline, and confirms it in the thread rather than asserting it.
4. The post-mortem is written to a version-controlled lessons file that future investigations can read.
5. Work is triaged the same way as any other: a small, well-bounded fix arrives as a change request through the review gate, and anything larger is written up as `intent.md` for Plan, at which point the loop starts feeding itself.

**Governance.** *What is enforced:* the agent acts under its own identity and never grants itself the authorization a human owns, and a fix reaches production through the review gate rather than from the channel. *What the evidence is:* the request, the diagnosis, the human authorization, and the fix, all in the channel where the incident was handled. *Where it is logged:* the channel history and the version-controlled lessons file. *Who approves:* the on-call engineer or incident commander for the response; the code owner for the fix.

**Measure.** *Leading:* time from the first message to a diagnosed cause with a verified baseline, read from the channel history. *Lagging:* the share of channel-borne incidents that become merged fixes against the incident tracker, and repeat incidents of the same class, which should fall as the fixes add cases to the eval suite. Read both: faster diagnosis with fewer merged fixes means the diagnosis is not leading to a fix, which is a triage problem rather than a detection one.
