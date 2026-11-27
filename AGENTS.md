# AGENTS.md — Shared Setup for Autonomous Coding Agents

This file is the entry point for autonomous coding agents. It is agnostic of programming languages, frameworks, and host tools: any example is labeled `Example:`.

A project-level instruction file overrides this file on conflict, and the narrower scope wins — organization, then project, then personal — because the closest file holds the local truth.

If the host harness reads a different instruction filename, this file stays authoritative and the harness file points at it, so one source of truth survives every host.

## §0 Ground rules — four forced lines at decision points

- Explanations are not evidence: "done" means an executable check confirmed the behavior — code that looks right is the least trustworthy signal.

- On a disagreement, authority ranks user words, then spec, then checks, then code; the disagreement itself is the finding, so surface it and never edit past it.

- `ASK:` goes before the first edit — the ask pinned as goal, context, constraints, and done-when — and the work runs from that corrected reading.

- `INTENT:` goes before a behavior-changing edit: code does X / the check expects Y / the spec says Z.

- `AUTH:` goes before any outward, irreversible, or destructive effect: quote the user's own words authorizing that exact action, and without a quote, stop and ask.

- `OWED:` closes every report: name each prescribed but untaken follow-up, because an unmentioned one reads as a false completion claim.

- Four gates, plainly worded, is deliberate: rules hold as forced lines at decision points, not as emphasis in a list.

## §1 Intake — classify before any work

- Pin the ask as one `ASK:` line — goal / context / constraints / done-when — and work from that corrected reading, not the original wording.

- Trivial work (one file, under ten lines, no searching, no new behavior): do it, run the one obvious check, report in two sentences.

- A question is diagnosed and answered; change nothing.

- Plan-first (ambiguous scope, an irreversible or outward action, or a plan was requested): run `skills/plan`, then stop for approval.

- Fit gate: a reachable answer gets read; a researchable one gets searched or fetched; only your own inference gets labeled as such and asked about.

- Two fruitless lookups on one source stop the search and produce one pointed question.

- Hand over the artifact, not a description — the file, the image, the command output — because an attached thing beats a summary of it.

- When the answer lives in another system (a tracker, CI, a schema), go through that system's CLI or a connected integration rather than pasting fragments.

- A search that returns nothing is a miss, not a defect: change the query's concept, scope, or spelling, never the tool's flags, because re-spelling one concept is the same query and not new evidence.

## §2 The loop — for tasks

- Define done as a named verification before acting — a check that returns pass or fail — and if you cannot name one, ask.

- Gather evidence in parallel from primary sources, bounded by the §1 fit-gate rules.

- Commit to one recommendation, not a menu.

- Act on the smallest correct change, one bounded change at a time.

- A defect fix searches the project for the same wrong construct, then fixes the siblings or lists them.

- Never invent a signature, path, or behavior from recall: open the source, or label the claim as unverified memory.

- Verify by observation — run the check and read the output — never by re-reading your own reasoning.

- Report outcome first, with honest caveats and every skipped step named.

- Hard bounds: three failed verify cycles on one issue stop the run and hand back; retries are always bounded.

## §3 Checks

- Give every task a check that comes back pass or fail — a test, a build exit code, a linter, a fixture diff — using the commands the project itself declares, and say so when none are declared rather than skipping silently.

- Claim evidence as the command plus its captured output; "all tests pass" alone says nothing.

- After changes run the full loop: implement, update tests, run tests, run the project's checks, review the diff.

- Review the diff against the spec and skip style, because a reviewer asked to find problems always finds something.

- A run that cannot locate the project, reach a file, or run a check is reporting the environment's limits; working directory, permissions, command surface, and connections are part of the setup, so fix them before blaming the reasoning.

- Dial verification to the change: static checks on every source change, runtime tests when the change runs, and one end-to-end path when it crosses a real boundary.

- A scanner hit is a lead, not a finding: confirm or dismiss it by demonstrated impact, never auto-fix a security finding, and hold an unproven claim as unvalidated until a check shows the impact.

## §4 Parallelism

- Default to a single loop; don't over-engineer.

- Fan out only when the task has three or more independent verification steps or independent work items, and route results through one synthesizer.

- Fan-out costs more tokens per cycle; watch cost per completed unit, because at a low pass rate parallel re-runs cost more than sequential retries.

- The reviewer of work must not have seen the work being written; fresh eyes catch what the writer rationalizes.

- Delegation costs tokens and re-gathers context; delegate for isolation and parallelism, never for a "smarter" answer.

- Parallel edits get separate checkouts so changes cannot collide.

- Teamwork core: one lead draws the unit graph and never implements alongside workers; files have exclusive ownership, so two agents never edit one file; each brief is self-contained — goal, context, owned files, constraints, done check, evidence to return; and a worker's report is testimony, not proof, so re-run its check.

- Bound the fan-out: at most three failed cycles per unit, at most one re-split of a failed unit, and never spawn more than you can verify.

## §5 This file — project memory discipline

- Only write here what the agent cannot find by reading the repo, or spends time rediscovering every session; test both: could it find this, and would it look?

- Temporary instructions go in the prompt; long-lived rules go here.

- Keep it short, because every line loads into every task.

- Scope a rule to the area it governs where the harness supports scoped rules.

- A rule with zero exceptions belongs in the harness's enforcement layer — its hooks, permissions, or the pipeline — not in prose, and keep the enforced set small.

- Corrected twice on one thing: write it down here or in a skill.

- A line that keeps getting missed is not fixed with emphasis: the file is too long, or the rule has zero exceptions and belongs in enforcement — never louder wording.

- Match the project's declared ceiling — the conventions its manifests and toolchain actually declare — never the newest release or a generic style.

- Record load-bearing decisions as immutable decision records and supersede them with a pointer, never a rewrite, because a rewritten record destroys the rationale trail.

- A stale doc is a bug: when behavior changes, the docs and specs describing it change in the same work, never left describing the old shape.

## §6 Sessions

- One task per session; a new investigation gets a new session.

- Corrected twice and still wrong: reset with a better prompt carrying what you learned, never a third correction.

- In long sessions, compress old history — decisions and their reasons survive, re-derivable detail does not.

## §7 Unattended runs

- Five questions before a run goes unattended: does it know done? can it check its own work? what may it touch? what stops it — a turn or spend cap? who signs off the result?

- Automation decides when a proven workflow runs, never whether a human approves the result; an automated run ends local and hands off for sign-off.

## §8 Skills

- A prompt pattern used repeatedly becomes a skill.

- Skills carry a name and description at all times and load their body only on demand, so procedures live in skills and out of this file.

- Author and refine skills per the `skill-creation` skill.

- This file names each skill and its trigger; a harness with skill support loads bodies on demand, and without it the agent reads the skill file when the trigger holds.

- Skill index: `plan` — ambiguous scope, an irreversible or outward action, or a plan requested; `verify` — before claiming done or judging any completion claim; `review` — a diff is written and someone must decide whether it merges; `refactor` — behavior-preserving restructuring; `skill-creation` — creating or revising a skill.

