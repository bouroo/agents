# The Loop as Decision Flowcharts

> Load on demand. The prose lives in `AGENTS.md` (§2 intake, §4 loop, §7 verification) and [verification](../SKILL.md); this file renders the same doctrine as executable decision charts. **Follow the arrows literally**: at every diamond, read the condition against the actual situation, take exactly one outgoing edge, and do not skip a gate. A chart node with no outgoing arrow you satisfy is a stop, not a suggestion.

## 1. Master router: any ask, start to finish

```mermaid
flowchart TD
    IN["Any incoming ask"] --> TRIV{"Trivial?<br/>one file, under 10 lines,<br/>no new behavior, no searching"}
    TRIV -->|yes| DOIT["Do it, run the one obvious check (L1),<br/>report in two sentences"]
    TRIV -->|no, or unsure| FIT{"Fit gate:<br/>where does the answer live?"}
    FIT -->|"reachable source<br/>(code, doc, spec)"| SHAPE{"What shape is the ask?"}
    FIT -->|unknown but researchable| SRCH["Search / fetch the source,<br/>then classify"]
    FIT -->|"own inference only,<br/>on a load-bearing claim"| STOPASK["STOP. Ask exactly one pointed question,<br/>stating your recommended interpretation.<br/>Then wait"]
    SRCH --> SHAPE
    SHAPE -->|"question<br/>(why, what, which)"| ANSWER["Diagnose and answer.<br/>Change nothing"]
    SHAPE -->|"plan-first<br/>(ambiguous scope, irreversible,<br/>or plan requested)"| PLAN["Produce a plan with one recommendation.<br/>STOP for approval"]
    SHAPE -->|task| LOOP["Enter the loop: THINK -> ACT -> PROVE -> GROW"]
    DOIT --> OUT["Report, outcome first,<br/>honest caveats"]
    ANSWER --> OUT
    PLAN --> OUT
    LOOP --> OUT
```

## 2. THINK: bounded evidence

```mermaid
flowchart TD
    T0["ORIENT: reconstruct current state from files<br/>(the repo is the record, not conversation memory)"] --> GAT["Gather primary-source evidence<br/>in parallel: reads, searches, lookups"]
    GAT --> DEC{"Can more evidence change<br/>the next action?"}
    DEC -->|no| COMMIT["Commit to exactly one recommendation"]
    DEC -->|yes| CNT{"Two fruitless lookups already<br/>spent on this source?"}
    CNT -->|no| GAT
    CNT -->|yes| ASK2["Stop; ask exactly one pointed question<br/>with your recommended interpretation"]
    GAT --> CONTRA{"Do the three intent slots disagree?<br/>(code does X, check expects Y, spec says Z)"}
    CONTRA -->|yes| FINDING["The disagreement IS the finding.<br/>Report it; do not edit"]
    CONTRA -->|no| DEC
    COMMIT --> DW["Define DONE_WHEN + backward plan:<br/>derive the state just before done,<br/>reconstruct failure state before code"]
```

## 3. ACT: one bounded change

```mermaid
flowchart TD
    A0["Intent gate owed?<br/>behavior-changing edit"] --> INT{"INTENT: line present,<br/>X/Y/Z in agreement?"}
    INT -->|yes| EDIT["Make one bounded change, within scope"]
    INT -->|trivial| NOTE["Note the skip, edit directly"]
    INT -->|no| BACK2["Back to THINK:<br/>the disagreement is the finding"]
    EDIT --> BATCH["Dispatch independent lookups together;<br/>collapse deterministic sequences into<br/>one batched execution per turn"]
    BATCH --> CKPT["Checkpoint state to .agents/:<br/>unit id, files touched, evidence, pending gates"]
    NOTE --> CKPT
```

## 4. PROVE: two-half check with bounded retries

```mermaid
flowchart TD
    V0["Run the named done_cmd yourself"] --> H1{"Half 1: does the done criterion<br/>pass, observed (command + exit + output)?"}
    H1 -->|no| WHY{"Why did it fail?"}
    H1 -->|yes| H2{"Half 2: does the check itself catch<br/>a deliberate break (mutation probe)?"}
    H2 -->|caught| VERDICT["One verdict: VERIFIED /<br/>VERIFIED WITH CAVEATS / REFUTED"]
    H2 -->|survived a break| THEATER["Test theater. The check is the defect"]
    WHY -->|"mechanical mistake<br/>in the change"| BACK4["Back to ACT: fix the change"]
    WHY -->|"observation contradicts<br/>your understanding"| BACK2["Back to THINK: your model<br/>of the problem is wrong"]
    BACK4 --> CYC{"Third failed cycle on the<br/>same issue? Or blocked by anything<br/>outside your control?"}
    BACK2 --> CYC
    CYC -->|no| V0
    CYC -->|yes| HAND["STOP. Hand back: the attempts,<br/>the exact failure output,<br/>and your current hypothesis"]
    THEATER --> HAND
    VERDICT --> GROWQ{"Same failure class<br/>across >= 2 units?"}
```

## 5. Judge: one verdict on a done report

```mermaid
flowchart TD
    J0["Collect every claim from the report,<br/>plus owed artifact lines"] --> J1["Establish ground truth:<br/>the diff outranks the report"]
    J1 --> J2{"Re-runnable<br/>claim left?"}
    J2 -->|yes| J3["Re-run it (cap 3 per claim):<br/>capture command + exit code + output"]
    J3 --> J4{"Reproduces?"}
    J4 -->|yes| J2
    J4 -->|no| J5["Label UNVERIFIABLE;<br/>force caveats if load-bearing"]
    J2 -->|no| J6["Hunt the fraud table:<br/>diff test files first, then AUTH traces,<br/>owed lines, debris/scope creep"]
    J6 --> J7{"Fraud found?"}
    J7 -->|yes| JR["REFUTED: name the claim,<br/>show contradicting output,<br/>give smallest fix"]
    J7 -->|no| JV["Exactly one verdict:<br/>VERIFIED / VERIFIED WITH CAVEATS / REFUTED"]
```

## 6. GROW: from failure to gate

```mermaid
flowchart TD
    G1{"Did any failure<br/>recur?"} -->|yes| CAT["Catalog the failure mode<br/>in .agents/plans/{slug}/retro.md"]
    G1 -->|no| EXIT["Record the decision, exit cleanly:<br/>startup checks pass, speculative edits<br/>reverted, next action stated"]
    CAT --> GATE["Convert it into a deterministic gate<br/>(a check that fails when the failure repeats)"]
    GATE --> MAP["Update the Failure-Mode Map<br/>in verification/SKILL.md"]
    MAP --> KIRBY{"Any control that now encodes only a<br/>model limitation (Kirby bet)?"}
    KIRBY -->|yes| CUT["Cut or revisit it at the next<br/>model upgrade"]
    KIRBY -->|no| EXIT
```

## Reading rules

- **Every diamond is a stop-and-test**, not a rhetorical question. If you cannot evaluate the condition, that is a hand-back, not an assumption.
- **Loops are bounded**: THINK evidence rounds cap at 3 per source; PROVE retries cap at 3 failed cycles on one issue (the hard verify bound); judge reproduction caps at 3 per claim. No fourth attempt inside a session.
- **Contradiction routes backward, never forward**: a surprise at PROVE returns to THINK; a mechanical mistake returns to ACT. Never patch past a surprise.

## Cross-references

- [verification](../SKILL.md) the loop in prose; the dial that decides how far these charts run on a given job.
- [craft](../../craft/SKILL.md) the artifact gates (`INTENT:`, `TWINS:`, `AUTH:`, `PENDING:`).
