# Re-deriving the Java version table

The claims in the Java guide are re-derivable from the local JDK — no network, no recall. The scripts below are the method, not a snapshot: **run** them after a JDK upgrade and reconcile any drift.

## API members — the JDK's own `@since` tags

Java's equivalent of Go's `GOROOT/api`: the JDK ships its full source in `lib/src.zip`, and every public member carries an `@since` javadoc tag. Run:

```python
import re, zipfile
SRC = "<JAVA_HOME>/lib/src.zip"
z = zipfile.ZipFile(SRC)
src = z.read("java.base/java/lang/String.java").decode("utf-8", "replace")
m = re.search(r"public\s+String\s+strip\(\)", src)
print(re.findall(r"@since\s+([0-9.]+)", src[:m.start()])[-1])   # -> 11
```

**Anchor to the declaration, not the file.** Taking the file's *last* `@since` is wrong for classes that gained members later: `HttpClient.java`'s last tag is 21 (a later method), while the type itself is 11. Always search the text *before* the matched declaration.

## Language features — compile against `--release`

`@since` covers APIs, not syntax. For language changes the anchor is `javac` itself: `--release N` enforces the language level *and* the API surface, so a snippet that fails at N and compiles at N+1 proves the feature landed at N+1. Run:

```python
import pathlib, subprocess, tempfile
def compiles(src, release):
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d, "T.java"); p.write_text(src)
        return subprocess.run(["javac", "--release", str(release), "-d", d, str(p)],
                              capture_output=True).returncode == 0
# min release = first N where this compiles
compiles("record T(int x) {}", 16)
```

## Trap: `-source`/`-target` are not substitutes for `--release`

Verified against `List.of` (a Java 9 API):

- `javac --release 8` → `error: cannot find symbol` ✓ correct
- `javac -source 8 -target 8` → compiles, emits a class file that runs on JDK 8 and fails at runtime ✗

The second produces a build that appears to target Java 8 but silently links JDK 25 APIs. A project using `-source`/`-target` cannot trust its own floor — flagging that is often the highest-value finding.
