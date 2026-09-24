# Re-deriving the Python table

CPython's documentation carries the version in structured form, so the Python table is re-derivable locally after a docs update — no recall.

## The anchor: each entry's own `Added in version` note

Every documented entry has a stable HTML id, and the version note sits inside that entry's block. Run:

```bash
curl -sSL https://docs.python.org/3/library/functools.html -o f.html
python3 - <<'PY'
import re, pathlib
raw = pathlib.Path("f.html").read_text()
NOTE = re.compile(r'class="[^"]*versionmodified[^"]*"[^>]*>\s*((?:Added|New) in version (\d+\.\d+))')
i = raw.find('id="functools.cache"')      # anchor to THIS entry, not the page
print(NOTE.search(raw, i).group(2))        # -> 3.9
PY
```

For PEPs and syntax the library pages do not cover, the introducing page is the **what's-new** that announces the PEP. Run:

```bash
curl -sS https://docs.python.org/3/whatsnew/3.9.html | grep -o 'PEP 584[^<]*'
# -> "PEP 584, union operators added to dict"
```

## Two traps that produced wrong answers here

Both were hit and corrected while building this table — they are the reason the method is spelled out rather than shown as a single grep.

1. **Windowing over flattened prose.** Taking "the first `in version X.Y` within N characters after the symbol" picks up the *next* entry's note. This reported `dict | dict` as 3.8 (it is 3.9 — PEP 584) and `typing.override` as 3.11 (it is 3.12). Anchor to the entry's `id="..."`, then search forward from there.
2. **Keyword-scanning what's-new.** The *first* page that *mentions* a feature is not the one that *introduced* it (e.g. `functools.cache` appears in pages later than 3.9). Use the note, or the page that announces the PEP — never a bare keyword hit.

## Runtime availability is necessary, not sufficient

An `import` succeeding proves a feature exists in the interpreter you ran, not the version that introduced it. Run:

```bash
python3 -c "import functools; functools.cache; print('present on', __import__('sys').version.split()[0])"
```

Pair that with the docs anchor: runtime confirms the feature works here; the version note says since when. Neither alone is the claim.
