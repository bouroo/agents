# Common Mistakes

> Load on demand from [delivery](../SKILL.md): the failure modes the four faces prevent, each paired with its fix.

| Mistake | Fix |
| --- | --- |
| Running the stages as a waterfall | Re-enter on evidence; `Test -> Build` and `Operate -> Intent` are canonical back-edges |
| Exiting a stage on "the agent finished" | Exit on the stage's check — the artifact plus its evidence |
| The implementer approving its own work | Split the seats; approval is a different actor from authorship |
| Verifying in the author's context | Re-derive in a fresh context; a report is testimony, not evidence |
| Adding a seat for every org role | Collapse into the seven; a duplicated seat is ceremony |
| Treating evals as verification | Evals test the process across runs; verification tests one unit of work |
| Mixing intent, spec, and plan into one document | One artifact per stage; each is a checkpoint the next resumes from |
| A spec with no Unresolved decisions | List what is open; a settled-looking spec hid the decisions |
| Execution progress leaking into PLAN.md | It belongs in the sibling STATUS.md |
| A WP with no verify command | Size it until it names one, or split it |
| A DONE_WHEN item that cannot name its command | Rewrite it as a check, or it is not terminal |
| `Phase` / `step` / bare `Pn` tokens | One vocabulary: `WPn` |
| One question at a time in a grilling round | Ask the whole settled frontier as one numbered round |
| Asking what you could look up | Dispatch a sub-agent for facts; only decisions reach the user |
| Acting when the questions run out | Frontier empty -> one-recommendation plan, then STOP for approval |
| Pre-slicing fog into ticket-sized pieces | Graduate one patch at a time as the frontier reaches it |
| An agent answering its own HITL ticket | Resolve HITL only through live exchange; a self-answer is fabricated |
| Charting past the destination | Rule it out of scope; it returns only if the destination is redrawn |
