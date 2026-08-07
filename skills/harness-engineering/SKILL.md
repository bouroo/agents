---
name: harness-engineering
description: "Harness-engineering norms across the THINK-ACT-PROVE-GROW loop: repo-as-record, split instructions, WIP=1, three-layer termination (L1/L2/L3), mutation testing, adversarial judging, and error budgets. Use when configuring agent controls, verifying work constraints, or establishing reliability patterns."
---

# Harness Engineering

A strong model still fails when the closed-loop system around it is weak. The harness constrains behavior, preserves context, defeats premature victory, verifies with executable evidence, and makes runtime observable across the loop.

> **Override.** A project-level harness spec that explicitly supersedes this skill wins.

**Stance:** "done" is the most common lie an agent tells. Verification is observed evidence, not narrated confidence; a gate that can fail is worth ten reminders that cannot.

**Right-size, don't overengineer.** Every control below exists because a real failure once demanded it -- not because every job needs all of them. Refuse the **Average Answer Trap** (high-complexity controls as defaults) and the **Kirby Effect** (a component that encodes a model-limitation bet and turns into dead weight as models improve). Dial every control to the job; add one only when a failure demands it. See [right-sizing](references/right-sizing.md).

**Modes:**
- **Build mode** -- design/extend a harness: walk the lifecycle, emit gates, handoff artifacts, failure-mode controls. Sequential.
- **Review mode** -- grade a transcript or live run against the Failure-Mode Control Map and the judge fraud rubric. Sequential.

## THINK -- guides steer before you act

1. **Repo-as-record, not conversation memory.** Restart from files; state, decisions, evidence live on disk under `.agents/`. Conversation is a cache that resets.
2. **Split instructions from learning.** Instruction memory (human directives -- AGENTS.md, build docs) stays stable and predictable; learning memory (agent-accumulated corrections) lives in its own files. Never write corrections into instruction files. ([memory-engineering](../memory-engineering/SKILL.md).)
3. **Guides beat reminders; encode standards as deterministic gates, not prose.** A gate requires a clear pass condition, an actionable failure message naming the next action, and an owner (the harness, not agent memory). "Remember to verify" loses to a gate that fails when verification is absent.

## ACT -- surgical execution

1. **WIP = 1.** Finish and verify one unit before starting the next.
2. **Right tool by capability, built-in first; handle failures cleanly.** Route by capability not name; prefer the built-in Read/Grep/Glob/Edit/Write over bash for file and string operations (AGENTS.md §2); fail gracefully -- handle tool/MCP errors explicitly with retries or fallbacks; never swallow an error.
3. **Separate reasoning from deterministic computation.** Arithmetic, parsing, validation, scheduling belong in tested code, never in model reasoning.

## PROVE -- three-layer termination, mutation, judging

**Three-layer verification (L1/L2/L3), dialed to complexity:**
- **L1 static** -- lint, type-check, format. Every source change.
- **L2 runtime** -- tests run; app starts; critical paths execute. When the change runs.
- **L3 end-to-end** -- one path crosses real boundaries. When the change crosses one (`n/a` allowed with a one-line reason).

Executable evidence (command + exit code + actual output) for every done claim -- never a narrated pass. See [verification theater](references/verification-theater.md).

**Mutation testing probe:** introduce a single semantic defect (flip a boolean, shift a bound, drop a guard); run the suite and require it to FAIL; revert and confirm it PASSES. A suite that cannot catch a deliberate defect is theater.

**Adversarial judge:** treat a "done" report as claims; re-run at least one; hunt frauds; issue one verdict (VERIFIED / VERIFIED WITH CAVEATS / REFUTED). ([judge command](../../commands/cmd-judge.md).)

**Hard verify bound:** on the **3rd failed cycle** on the same issue, STOP. Do not start a 4th attempt. ([coder](../../agents/coder.md).)

## GROW -- self-improving harness

A recurring failure is a **harness problem, not a prompt problem.** Prompt tweaks smooth edges temporarily; durable reliability comes from updating the surrounding system.

1. **Catalog failure modes** in `.agents/plans/{slug}/retro.md`.
2. **Convert findings into gates** -- a deterministic check that makes repeating the failure impossible.
3. **Refine the Failure-Mode Control Map** across sessions (below).
4. **Manage error budgets** -- track failure frequency per category; when a budget is exceeded, halt to upgrade sensors/guides.

## Failure-Mode Control Map (GROW)

| Failure mode | Looks like | Primary fix | Artifact |
|---|---|---|---|
| Tool-routing drift | `cat`/`grep`/`find` in bash instead of Read/Grep/Glob | Built-in tools first; bash for commands only | AGENTS.md §2 |
| Verification theater | "tests pass" without output | Require captured evidence; mutation probe | L1/L2/L3 gate |
| Scope creep / spec betrayal | edits outside SCOPE | SCOPE-bound handoff; `INTENT:` gate | [code-craft](../code-craft/SKILL.md) |
| Context rot / premature victory | "done" on stale memory | Repo-as-record; checkpoint every turn | `state.json` |
| Negotiated verdict | "mostly works" | One verdict; adversarial judge | judge command |
| Fragile startup | fresh checkout fails | standard startup check | L1 static gate |
| Recurring failure (>= 2 units) | same class repeats | halt; upgrade harness controls | `retro.md` |

## Hard constraints

Clean exit (startup + verification pass; speculative edits reverted). No secret leakage. Executable evidence required for "done".

## References

- [right-sizing](references/right-sizing.md) -- the two-axis dial.
- [verification-theater](references/verification-theater.md) -- the mutation-testing protocol and theater audit.
- [agent-computer-interface](references/agent-computer-interface.md) -- tool & MCP design checklist; also how slash commands receive `$ARGUMENTS` portably across hosts.
- [composition-patterns](references/composition-patterns.md) -- delegation topology menu.
- [code-craft](../code-craft/SKILL.md) | [memory-engineering](../memory-engineering/SKILL.md) | [spec-driven-development](../spec-driven-development/SKILL.md)
