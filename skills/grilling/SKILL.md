---
name: grilling
description: "Interview the user in numbered frontier rounds to reach shared understanding of a plan or decision, mapping choices as a design tree. Use when scope is ambiguous, an action is irreversible or outward-facing, a plan is requested, or the user asks to be grilled."
---

# Grilling

Interview the user relentlessly until you reach shared understanding of a plan, decision, or idea. This is the technique behind the manifesto's plan-first intake route (§2): ambiguity drains through conversation, never through guessing.

> **Override.** A project-level planning process that explicitly supersedes this skill wins.

## The design tree

Map the decision space as a **design tree**: every decision branches into the decisions that hang off it. Settling a node unblocks its children; the interview walks the tree, not a flat question list.

## Rounds and the frontier

Work the tree in **rounds**. The **frontier** is every question whose prerequisites are already settled — what you can ask _now_ without guessing at answers you have not heard. Ask the whole frontier in one round: number each question, give your recommended answer, then stop and wait. A question whose answer depends on one still open this round belongs to a _later_ round. Each round's answers reshape the tree: settled decisions push the frontier outward. Recompute it and ask the next round.

Format a round like so:

```markdown
❓ **Q1** - **<question title>**: <question body; may be several paragraphs, may offer choices>

➡️ <recommended answer>

---

❓ **Q2** - **<question title>**: <question body>

➡️ <recommended answer>
```

## Facts are yours; decisions are theirs

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (code, files, tools), dispatch a sub-agent to look it up — never ask the user for anything you could find yourself. Do not block on it: a running lookup is an unsettled prerequisite, so only the questions downstream of it wait for the result; ask the rest of the frontier now. The _decisions_ are the user's: put each to them in the round, and wait.

## Completion

The interview is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Then produce the plan with one recommendation and **STOP** for approval — never act on the interview's outcome on your own authority (§2).

## Common mistakes

| Mistake | Fix |
| --- | --- |
| One question at a time | Ask the whole settled frontier as one numbered round |
| Asking what you could look up | Dispatch a sub-agent for facts; only decisions reach the user |
| Blocking the round on a running lookup | Only questions downstream of the lookup wait |
| A question downstream of one still open | Move it to a later round |
| Answering your own questions | A decision made without the user is fabricated, not resolved |
| Acting when the questions run out | Frontier empty -> one-recommendation plan, then STOP for approval |

## Cross-references

- [wayfinder](../wayfinder/SKILL.md) runs this method across sessions: its Grilling tickets resolve one decision each; its frontier is the map's takeable tickets, not this session's open questions.
- [domain-modeling](../domain-modeling/SKILL.md) pins fuzzy terms to canonical ones mid-interview and keeps the resulting language in `CONTEXT.md`.

Adapted from [mattpocock/skills](https://github.com/mattpocock/skills) (`grilling`, MIT).
