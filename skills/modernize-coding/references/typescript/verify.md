# Re-deriving the TS/JS edition table

Unlike Go and Java, this ecosystem ships no local machine-readable index — MDN's specification table now links only the *current* edition draft (every page reports "ECMAScript 2027"), so it cannot date a feature. The authoritative, regenerable anchor is TC39's own finished-proposals list.

## The anchor: TC39's publication year

A proposal reaching stage 4 is included in that year's spec. The list states the year per proposal. Run:

```bash
curl -sSL https://raw.githubusercontent.com/tc39/proposals/main/finished-proposals.md -o finished.md
```

```python
import re, pathlib
t = pathlib.Path("finished.md").read_text()
rows = [ln for ln in t.splitlines() if re.match(r"^\|\s*\[", ln)]
for r in rows:
    cells = [c.strip() for c in r.strip().strip("|").split("|")]   # 5 cells
    name = re.sub(r"^\[([^\]]+)\]\[[^\]]*\]$", r"\1", cells[0])     # strip the link markup
    year = re.sub(r"\D", "", cells[-1])                            # last cell = year
    if "Optional Chaining" in name:
        print(name, "->", year)                                    # -> 2020
```

Years this yields for the guide's table: Optional Chaining **2020**, Nullish Coalescing **2020**, Logical Assignment **2021**, `.at()` **2022**, Accessible `Object.hasOwn` **2022**, Change Array by Copy (`toSorted`/`toReversed`/`with`/`toSpliced`) **2023**, find-from-last **2023**.

## Trap: the row shape

`cells[0]` is `[Optional Chaining][chaining]` — a Markdown reference link. Stripping `[` and `]` naively leaves `Optional Chaining][chaining` (or, with an over-eager character class, the empty string). Match the whole link with `^\[([^\]]+)\]\[[^\]]*\]$` and take group 1. Getting this wrong produces a silent empty result rather than an error — the failure mode to watch for.

## Traps specific to this ecosystem

1. **`structuredClone` is not ECMAScript.** It is defined by the WHATWG HTML spec, so no edition year applies; its floor is a runtime version (Node 17+, and the browsers that shipped it). Do not file it under an ES year.
2. **`target` is not a runtime guarantee.** `tsconfig` `target: "ES2024"` emits modern syntax but ships no polyfill. The safe-use floor is `package.json` `engines.node` / `browserslist`, which TC39's table says nothing about. Verify the API exists at that floor separately.
3. **MDN's spec table is not an anchor.** It links the live draft. If you need a per-feature source, prefer the proposal's own repo README, which records the stage-4 date.

## Runtime check (availability, not provenance)

Run:

```bash
node -e "console.log(typeof [].toSorted, typeof Object.hasOwn, typeof structuredClone)"
```

This proves the feature exists in the Node you ran — not that it exists at the project's declared floor, and not when it was introduced. Pair it with the TC39 year and the `engines.node` floor; no single one of the three is the claim.
