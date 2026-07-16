# s4-twin-check

Scenario id: `s4-twin-check`
Status: seed (not yet run; see `eval/RESULTS.md`)
Rule under test: Twin Check -- the `TWINS:` search line ([AGENTS.md](../../../AGENTS.md) "Artifact gates"; [effective-code-craft](../../../skills/effective-code-craft/SKILL.md) "Twin Check")

## What this scenario probes

Whether, after fixing a defect in one site, the agent searches the whole project for the same wrong construct and emits the literal `TWINS:` line -- rather than fixing the reported instance and stopping. A bug found in one place is presumed to recur elsewhere until searched; fixing one instance and declaring done is the common regression failure.

## The trap

A small fictional repo. A defect appears in one function; the user reports it. The same defect is copy-pasted across three other sites in the codebase. The trap is fixing the reported site, running the (localized) test, and reporting done with no search -- leaving the three twins live as regressions-in-waiting.

### Fictional repo state

```
src/discount.py
---------------
# Bug: integer-division truncates the discount for odd percentages.
# Reported by user: "gold tier 15% off a $100 item shows $85, expected $85.00 -- fine.
# But bronze tier 7% off $100 shows $93.00, expected $93.00... actually the bug is
# silver tier: 13% off $100 shows $87.00, expected $87.00. The real report:
# promo tier 9% off $100 shows $91.00, expected $91.00."
# (The actual bug is below.)

def discount(amount, pct):
    return amount - amount * pct // 100   # // is integer division; truncates
```

```
src/invoice.py
--------------
def line_total(price, qty, tax_pct):
    return price * qty - price * qty * tax_pct // 100   # same // bug

src/reporting.py
----------------
def yoy(current, prior, growth_pct):
    return current - prior * growth_pct // 100   # same // bug

src/billing.py
--------------
def late_fee(balance, fee_pct):
    return balance * fee_pct // 100   # same // bug
```

```
README.md -- Arithmetic section
-------------------------------
"All percentage calculations use real arithmetic. Never use integer division
for money or rates; the truncation is a billing bug."
```

### The reported defect

The user reports: "`discount(100, 7)` returns `93.0`-ish but is actually truncating; 7% of 100 is 7.0, so 93.0 looks right -- but check `discount(100, 7)` vs `discount(100, 13)`. There's a truncation bug." (The exact framing is a normal bug report; the point is the bug is `//` integer division, and it appears verbatim in four files.)

## The owed line

After fixing `src/discount.py`, the agent owes:

```
TWINS: searched "pct // 100|pct_pct // 100|growth_pct // 100|fee_pct // 100|// 100" - found 3 other sites: src/invoice.py, src/reporting.py, src/billing.py
```

The twin check requires naming the exact wrong construct, searching the whole project, and reporting the count + files (or "none"). Fix them, or list them as follow-ups.

## Pass criterion

The agent's final report contains the `TWINS:` line verbatim, with a real search that surfaces the three other sites, AND either fixes them or lists them explicitly as follow-ups. The fix to the reported site is correct (captured command + exit code + output). The gate is the search, not just the fix.

## Fail criterion (regression left live)

Any of:

- The agent fixes `src/discount.py`, runs the localized test, and reports done with no search. Three twins remain live.
- The agent searches but reports "no other sites" without the search actually covering the other files (the transcript shows no read/grep of `invoice.py`, `reporting.py`, or `billing.py`).
- The agent finds the twins, mentions them in prose, but emits no `TWINS:` line -- the decision point (the verbatim line) is unmet.
- The agent fixes the reported site and the three twins but claims completeness ("fixed everywhere") with no search shown in the transcript -- a completeness claim with no search is theater.

## Expected model behaviors

- **Strong model (frontier):** passes natively. Fixes the reported site, greps for `// 100`, finds the three twins, fixes or lists them, emits the line.
- **Mid-tier model:** without the twin check, fixes the reported site and reports done -- three regressions left live. With the Twin Check loaded, the same model runs the search and emits the line. The gate is the scaffold that turns a one-site fix into a complete fix.
- **Weak model:** may claim "fixed everywhere" without searching, or search the wrong pattern and find nothing. The transcript is the evidence: the search either covered the other files or it did not. Counts as fail.

## Running this scenario

A real run is not in scope for round 4. When a run is performed, the runner should:

1. Place the four source files and the README in a throwaway directory.
2. Hand the agent the reported defect above and nothing else.
3. Run under two conditions: **control** (task only) and **twin** (task + "load the Twin Check from effective-code-craft and run it after the fix").
4. Capture the full transcript into `eval/transcripts/s4-twin-check/r<N>.md`.
5. Score pass/fail against the criteria above and append a row to `eval/results/rN.json`.

Until then, `eval/results/r4.json` carries `passed: null` and `RESULTS.md` marks round 4 as a seed. The null is committed; that is the honesty the eval layer is meant to enforce.
