# Grilling

> Load on demand from [delivery](../SKILL.md#grilling): the round mechanics, fact-versus-decision dispatch, and completion rule for a plan-first interview.

Interview the user until you reach shared understanding of a plan, decision, or idea — the technique behind the manifesto's plan-first intake route. Ambiguity drains through conversation, never through guessing. Map the decision space as a **design tree**: every decision branches into the decisions that hang off it; settling a node unblocks its children.

Work the tree in **rounds**. The **frontier** is every question whose prerequisites are settled — what you can ask now without guessing at answers you have not heard. Ask the whole frontier in one round: number each question, give your recommended answer, then stop and wait. A question depending on one still open belongs to a later round; each round's answers push the frontier outward, so recompute it and ask the next.

```markdown
❓ **Q1** - **<question title>**: <question body; may offer choices>

➡️ <recommended answer>

---

❓ **Q2** - **<question title>**: <question body>

➡️ <recommended answer>
```

Facts are yours, decisions are theirs. Finding a _fact_ is your job: when a frontier question needs one from the environment, dispatch a sub-agent to look it up rather than asking the user. Do not block the round on it — only questions downstream of the lookup wait; ask the rest now. Put each _decision_ to the user in the round and wait: a decision made without the user is fabricated, not resolved.

Completion: the frontier is empty when every branch is visited and nothing is left silently assumed. Then produce the plan with one recommendation and **STOP** for approval — never act on the interview's outcome on your own authority. The `intent` / `spec` / `PLAN.md` shapes carry the approval. The grilling method is adapted from [mattpocock/skills](https://github.com/mattpocock/skills) (`grilling`, MIT).
