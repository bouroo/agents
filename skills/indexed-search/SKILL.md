---
name: indexed-search
description: "Use when a search is slow or repeated, when a tree has tens of thousands of files, when a miss must be trusted as absence, when a search returns nothing and the agent is about to retry it, when the same concept is being searched again under a different flag or spelling, or when the agent is unsure which search flag to pass — even if the user only complains that grep keeps timing out or that the search found nothing. Applies the search discipline: one query, one concept, held until the miss is established, structured output parsed from stdout in the same call. Probes for a trigram-indexed tool, drives its index and serve lifecycle, and falls back to ripgrep then the built-in Grep without installing anything. Not for a single known-string lookup in a small tree, and not for making an application query faster (quality owns performance)."
license: Apache-2.0
---

# Indexed search

A trigram index turns O(total bytes) scans into candidate-file lookups — up to an order of magnitude faster on large repos — but only if its lifecycle is managed. Probe first, fall back when the tool is absent, never install: the doctrine ships dependency-free, and a skill that requires a build step is broken on the next host.

## 1. Probe the host

```bash
command -v tgrep && tgrep --version
```

Present -> drive it (§4-§5). Absent -> `command -v rg` and use ripgrep with the flag map (§6). rg absent too -> the built-in Grep tool. Do not install, build, or download anything to obtain an index; note the chosen engine in your report.

## 2. Search discipline

A search that returns nothing is a miss, not a defect. The measured failure was mechanical: one concept re-searched 34 times under different flags, 21 calls passing `-r` in recursive position so the flag ate the pattern and the output was rewritten while the call still looked like a hit.

- **One query, one concept.** Re-searching one concept under a different flag, path, or spelling is a new query, not new evidence. Fix one canonical form and hold it until the miss is established. A concept searched 34 ways is 34 facts about the flags, not 34 facts about the code.
- **A miss is a miss.** Change the query — the concept, its scope, its spelling — never the tool's flags. Coaxing a result with a differently-spelled flag is the trap: a flag's meaning can differ by spelling, and the output can be rewritten silently while the call still looks like a hit. When a query legitimately must vary, vary one axis at a time and record which.
- **The flag trap, concretely.** In ripgrep and tgrep alike, `-r` is `--replace` and takes a value: `rg -rn PATTERN` is `--replace n PATTERN`, so the pattern is consumed as the replacement text and the output comes back rewritten (exit 0, no error). `-n` is line numbers, and recursion is the default. Use `rg -n PATTERN` for line numbers, `rg -rn` never. Check the running engine's `--help` before trusting any flag spelling — this table included.
- **Structured output goes to stdout, in the same call.** For machine-readable output, parse the command's stdout where it is produced; do not write a temp file and read it back in a later call. One call, one artifact: `rg --json PATTERN` piped into the parser that consumes it, not into a file.
- **Termination.** A search claim cites command + exit code. A miss (exit 1) is evidence of absence only against a fresh index or a `--no-index` scan — a negative from a stale index is the classic false-anchor: it looks like proof nothing exists while the index never saw the file. When a verdict hinges on absence, re-run `--no-index`.

## 3. When the index earns its keep

- **Earns it:** repo of ten thousand files or more, or repeated searches inside one session — the index amortizes after a handful of queries.
- **Skips it:** one-off lookups in a small tree — the probe-and-serve ceremony costs more than the scan; go straight to Grep/rg.
- **Bypasses it:** edits made moments ago must be seen now — the index is a snapshot. Search `--no-index` (full scan) or rebuild; the file watcher repairs missed changes lazily, not on demand.

## 4. Lifecycle (per session)

```bash
tgrep index .            # once; also `tgrep serve .` builds if missing
tgrep serve . &          # once per session: watches changes, serves clients
tgrep status .           # reachability + build completion — NOT freshness
```

- Server died or status is stale -> restart it. Keep `--index-path`, `--exclude`, and ignore flags **identical** across `index`/`serve`/search, or you query a different corpus than you indexed.
- Bulk file generation (migrations, vendoring, checkouts) -> rebuild or search `--no-index`.
- No way to keep a background process alive across turns -> skip `serve`; index once, rebuild after edits, and say so in the report.
- `.tgrep/` is tool-managed state: confirm the host repo ignores it (`git check-ignore .tgrep`); if untracked-and-unignored, add it to `.gitignore` — a committed index is repo pollution.

## 5. Search mechanics

```bash
tgrep -- "fn parse_config" .        # `--` always: patterns starting with `-` misparse as flags
tgrep -F -- "Vec<Option<T>>" .      # literals (braces, generics, pasted text) -> -F
tgrep -t rust -g '*.rs' -- "pat" .  # scope first; `-l` for filename triage before full hits
tgrep --json -- "pat" .             # one JSON object per line — parse it, don't eyeball it
tgrep --vimgrep -- "pat" .          # file:line:col:text for jump-to-location
tgrep -q -- "pat" . && echo HIT     # exit 0 match / 1 none / 2 error — probe, don't narrate
```

- Flags that silently degrade to a full scan: `--hidden`, `--no-ignore`, `--text`, single-file paths. Use only when that is the intent.
- Unsupported rg-style flags **error loudly**, never silently ignored — flag surfaces drift between versions, so trust `tgrep --help` on the running version over any table (including this one).

## 6. Fallback ladder

| Engine | Mapping |
| --- | --- |
| ripgrep | near-identical surface: `-F -t -g -l -c -A/-B/-C --json` all carry over; drop `--no-index`, `--index-path`, `--stats`, `serve`/`status` |
| Grep tool | built-in path/string search; lose type filters and JSON — accept, and scope with explicit globs |
