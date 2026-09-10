---
name: indexed-search
description: "Fast repeated search over large repositories via a trigram-indexed tool: probe the host for tgrep and drive its index/serve lifecycle when present, fall back to ripgrep, then the built-in Grep. Use for search-heavy sessions, big-tree sweeps, or when the user names tgrep."
---

# Indexed search

A trigram index turns O(total bytes) scans into candidate-file lookups — up to an order of magnitude faster on large repos — but only if the lifecycle is managed. Probe first, degrade gracefully, never install: the doctrine ships dependency-free, and a skill that requires a build step is a broken skill on the next host.

## 1. Probe the host

```bash
command -v tgrep && tgrep --version
```

Present -> drive it (§3-§4). Absent -> `command -v rg` and use ripgrep with the flag map (§5). rg absent too -> the built-in Grep tool. Do not install, build, or download anything to obtain an index; note the chosen engine in your report.

## 2. When the index earns its keep

- **Earns it:** repo of ten thousand files or more, or repeated searches inside one session — the index amortizes after a handful of queries.
- **Skips it:** one-off lookups in a small tree — the probe-and-serve ceremony costs more than the scan; go straight to Grep/rg.
- **Bypasses it:** edits made moments ago must be seen now — the index is a snapshot. Search `--no-index` (full scan) or rebuild; the file watcher repairs missed changes lazily, not on demand.

## 3. Lifecycle (per session)

```bash
tgrep index .            # once; also `tgrep serve .` builds if missing
tgrep serve . &          # once per session: watches changes, serves clients
tgrep status .           # reachability + build completion — NOT freshness
```

- Server died or status is stale -> restart it. Keep `--index-path`, `--exclude`, and ignore flags **identical** across `index`/`serve`/search, or you query a different corpus than you indexed.
- Bulk file generation (migrations, vendoring, checkouts) -> rebuild or search `--no-index`.
- No way to keep a background process alive across turns -> skip `serve`; index once, rebuild after edits, and say so in the report.
- `.tgrep/` is tool-managed state: confirm the host repo ignores it (`git check-ignore .tgrep`); if untracked-and-unignored, add it to `.gitignore` — a committed index is repo pollution.

## 4. Search mechanics

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

## 5. Fallback ladder

| Engine | Mapping |
| --- | --- |
| ripgrep | near-identical surface: `-F -t -g -l -c -A/-B/-C --json` all carry over; drop `--no-index`, `--index-path`, `--stats`, `serve`/`status` |
| Grep tool | built-in path/string search; lose type filters and JSON — accept, and scope with explicit globs |

**Termination:** a search claim cites command + exit code. A **miss (exit 1) is evidence of absence only against a fresh index or a `--no-index` scan** — a negative from a stale index is the classic false-anchor: it looks like proof nothing exists while the index simply never saw the file. When a verdict hinges on absence, re-run `--no-index`.
