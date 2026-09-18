# Python adapter

Python's baseline is declared in packaging metadata, not by whichever interpreter happens to be on PATH — a `python3` of 3.14 tells you nothing about what the project supports.

Implements [modernize-coding](../../SKILL.md) for Python.

## 1. Detect the baseline

1. **Declared** — `requires-python` in `pyproject.toml` `[project]` (PEP 621), or `python_requires` in `setup.cfg`/`setup.py`. This is the ceiling: a syntax or stdlib feature newer than it is a break, not a modernization.
2. **Runtime** — `.python-version`, `.tool-versions`, tox/nox envlist, or a CI matrix. These usually pin what CI actually tests.
3. **Running** — `python3 -V`. Only tells you what can be *run* locally.

Absent any declaration, say so explicitly rather than assuming the newest — an undeclared floor is itself a finding.

## 2. Rewrite existing code

- **`ruff`** — the practical default. Its `UP` (pyupgrade) rules are **in the default rule set** and are auto-fixable:
  `ruff check --diff .` → review → `ruff check --fix .`
  `--diff` is the dry-run: it prints the patch without writing, which is exactly the diff-first discipline the parent skill requires.
- **`pyupgrade`** — the original tool for the same rewrites, targeting an explicit floor via a flag: `pyupgrade --py311-plus $(git ls-files '*.py')`. Use the flag matching the project's `requires-python`; running it without one assumes the oldest and rewrites too little.
- **`black`** — formatting only. It is not a modernization tool; do not count it as one.

Order matters: let the fixer rewrite, then format, then verify.

## 3. Write current from the start

Each "Needs" below is anchored to the CPython documentation's own version note for that entry (`Added in version X.Y`), or to the what's-new page that announced the PEP — see [verify](verify.md) to re-derive any of them.

### Typing

| Instead of | Write | Needs |
|---|---|---|
| `from typing import List, Dict` | `list[...]`, `dict[...]` (PEP 585) | 3.9 |
| `typing.Optional[X]` | `X \| None` (PEP 604) | 3.10 |
| `typing.Union[A, B]` | `A \| B` | 3.10 |
| `TypeVar("T")` + separate `Generic[T]` | `def f[T](x: T)` / `class C[T]` (PEP 695) | 3.12 |
| `@typing.overload`-adjacent runtime override without a marker | `typing.override` | 3.12 |
| a `TypeVar` bound to the enclosing class | `typing.Self` | 3.11 |
| `Callable` from `typing` | `collections.abc.Callable` | 3.9 |

### Syntax

| Instead of | Write | Needs |
|---|---|---|
| `"literal".lstrip(prefix)` for a known prefix | `str.removeprefix` / `str.removesuffix` | 3.9 |
| manual `try/except` fan-out over a group | `except*` (PEP 654) | 3.11 |
| `dict(a, **b)` to merge | `a \| b` (PEP 584) | 3.9 |
| `%`-formatting or `.format()` | f-strings | 3.6 |

### Standard library

| Instead of | Write | Needs |
|---|---|---|
| `@lru_cache(maxsize=None)` | `@functools.cache` | 3.9 |
| `@lru_cache()` default (now 128) | `@lru_cache` unchanged, or `functools.cache` | 3.8 |
| manual `zip(it, it[1:])` pairs | `itertools.pairwise` | 3.10 |
| manual chunking loop over a sequence | `itertools.batched` | 3.12 |
| `os.path` string work where a path object reads better | `pathlib.Path` | 3.4 |
| manual `os.walk` for a path tree | `Path.walk` | 3.12 |
| `re.match(r"...")` for `startswith` intent | `str.startswith` / `Path.is_relative_to` | 3.9 |
| `pytz` | `zoneinfo` | 3.9 |
| a hand-rolled topological sort | `graphlib.TopologicalSorter` | 3.9 |
| `toml` / `tomli` to read config | `tomllib` | 3.11 |
| `asyncio.gather` with manual cancellation/error handling | `asyncio.TaskGroup` | 3.11 |

`Path.is_relative_to` (3.9) is also the correct replacement for the common `str(path).startswith(str(base))` bug — which is not merely dated but wrong on prefixes like `/data` vs `/database`.

## 4. Verify

`ruff check .` → `python -m compileall -q <pkg>` (catches syntax errors the linter may not) → the project's type checker if any (`mypy` / `pyright`) → `pytest`. If `requires-python` is lower than the interpreter you ran under, the tests prove nothing about the floor — check with the oldest supported interpreter, or say you did not.

**Termination:** a clean diff with a failing test run is not done (§7 of the manifesto).
