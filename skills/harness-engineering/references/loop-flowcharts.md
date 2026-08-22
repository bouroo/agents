# The Loop as Decision Flowcharts

> Load on demand. The prose lives in `AGENTS.md` (S2 intake, S4 loop, S7 verification) and [harness-engineering](../SKILL.md); this file renders the same doctrine as executable decision charts. **Follow the arrows literally**: at every diamond, read the condition against the actual situation, take exactly one outgoing edge, and do not skip a gate. A chart node with no outgoing arrow you satisfy is a stop, not a suggestion.

ASCII only; the charts are Mermaid `flowchart TD`. Node vocabulary: gates and artifact lines (`INTENT:`, `TWINS:`, `AUTH:`, `PENDING:`), verification layers (L1/L2/L3), the mutation probe, the hard verify bound.

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
    T0["ORIENT: reconstruct current state from files<br/>(repo-as-record, not conversation memory)"] --> GAT["Gather primary-source evidence<br/>in parallel: reads, searches, lookups"]
    GAT --> DEC{"Can more evidence change<br/>the next action?"}
    DEC -->|no| COMMIT["Commit to exactly one recommendation"]
    DEC -->|yes| CNT{"Round 3 already spent<br/>on this source or strategy?"}
    CNT -->|no| GAT
    CNT -->|yes| ASK2["Two fruitless lookups on one source:<br/>stop, ask exactly one pointed question"]
    GAT --> CONTRA{"Do the three intent slots disagree?<br/>(code does X, check expects Y, spec says Z)"}
    CONTRA -->|yes| FINDING["The disagreement IS the finding.<br/>Report it; do not edit"]
    CONTRA -->|no| DEC
    COMMIT --> DW["Define DONE_WHEN:<br/>one executable check per unit"]
```

## 3. ACT: one bounded change

```mermaid
flowchart TD
    A0["Intent gate owed?<br/>behavior-changing edit"] --> INT{"INTENT: line present,<br/>X/Y/Z in agreement?"}
    INT -->|yes| EDIT["Make one bounded change, within scope"]
    INT -->|trivial| NOTE["Note the skip, edit directly"]
    INT -->|no| BACK2["Back to THINK:<br/>the disagreement is the finding"]
    EDIT --> BATCH["Dispatch independent units together;<br/>collapse deterministic sequences into<br/>one batched command"]
    BATCH --> CKPT["Checkpoint state to .agents/:<br/>unit id, files, evidence, pending gates"]
    NOTE --> CKPT
```

## 4. PROVE: two-half check with bounded retries

```mermaid
flowchart TD
    V0["Run the named done_cmd yourself"] --> H1{"Half 1: does the done criterion<br/>pass, observed (command + exit + output)?"}
    H1 -->|no| WHY{"Why did it fail?"}
    H1 -->|yes| H2{"Half 2: does the check itself catch<br/>a deliberate break (mutation probe)?"}
    H2 -->|caught| VERDICT["Report verdict: VERIFIED /<br/>VERIFIED WITH CAVEATS / REFUTED"]
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

## 5. GROW: from failure to gate

```mermaid
flowchart TD
    G1{"Did any failure<br/>recur?"} -->|yes| CAT["Catalog the failure mode<br/>in .agents/plans/{slug}/retro.md"]
    G1 -->|no| EXIT["Record the decision, exit cleanly:<br/>startup checks pass, speculative edits<br/>reverted, next action stated"]
    CAT --> GATE["Convert it into a deterministic gate<br/>(a check that fails when the failure repeats)"]
    GATE --> MAP["Update the Failure-Mode Control Map"]
    MAP --> KIRBY{"Any control that now encodes only a<br/>model limitation (Kirby bet)?"}
    KIRBY -->|yes| CUT["Cut or revisit it at the next<br/>model upgrade"]
    KIRBY -->|no| EXIT
```

## 6. Judge: one verdict on a done report

```mermaid
flowchart TD
    J0["Collect every claim from the report,<br/>plus owed artifact lines"] --> J1["Establish what changed:<br/>the diff is ground truth, not the report"]
    J1 --> J2{"Re-runnable<br/>claim left?"}
    J2 -->|yes| J3["Re-run it:<br/>capture command + exit code + output"]
    J3 --> J4{"Reproduces?"}
    J4 -->|yes| J2
    J4 -->|no| J5["Fraud table hit:<br/>file:line + smallest fix"]
    J2 -->|no| J6["Hunt the fraud table:<br/>highest-yield first"]
    J6 --> J7{"Fraud found?"}
    J7 -->|yes| J5
    J7 -->|no| JV["Exactly one verdict:<br/>VERIFIED / VERIFIED WITH CAVEATS / REFUTED"]
    J5 --> JR["REFUTED: name the claim,<br/>show the contradicting output"]
```

## Reading rules

- **Every diamond is a stop-and-test**, not a rhetorical question. If you cannot evaluate the condition, that is a hand-back, not an assumption.
- **Loops are bounded**: THINK evidence rounds cap at 3 per source; PROVE retries cap at 3 failed cycles on one issue (the hard verify bound); judge reproduction caps at 3 per claim. No fourth attempt inside a session.
- **Contradiction routes backward, never forward**: a surprise at PROVE returns to THINK; a mechanical mistake returns to ACT. Never patch past a surprise.

## Cross-References

- [harness-engineering](../SKILL.md) the loop in prose; the Failure-Mode Control Map.
- [right-sizing](./right-sizing.md) which controls these charts demand on a given job (the dial, not the map, decides).
- [verification-theater](./verification-theater.md) the two-half check in depth.
- [composition-patterns](./composition-patterns.md) the delegation topologies behind the ACT fan-out node.
- `AGENTS.md` S2 (intake and the fit gate), S4 (the loop), S7 (three-layer termination).
