# Java adapter

Java's baseline is declared by the build, not by the JDK you happen to run: `maven.compiler.release` / `--release` (Gradle: `java.toolchain` / `options.release`). That value is the ceiling — a construct above it will not compile where the project actually runs.

Implements [modernize-coding](../../SKILL.md) for Java.

## 1. Detect the baseline

1. **Declared**: `<maven.compiler.release>` in `pom.xml`, or `options.release` / the Java toolchain in `build.gradle(.kts)`. Read it. Absent, fall back to `maven.compiler.source`/`target`, but note the difference below — they are not equivalent.
2. **Running**: `java -version`. The JDK may be far newer than the project's floor; that tells you what *can* be built with, never what the code may use.

**Use `--release`, never `-source`/`-target`.** Verified: `javac --release 8` correctly rejects `List.of` (`cannot find symbol`) because that API postdates 8, while `-source 8 -target 8` compiles it happily — emitting a class file that claims Java 8 but references JDK 25 APIs and dies at runtime on a real Java 8 JVM. `--release` is the only flag that gates the language *and* the API surface together.

## 2. Rewrite existing code

- **`jdeprscan`** (ships with the JDK) — scan for use of deprecated APIs before touching anything:
  `jdeprscan --release <N> --for-removal .` lists only what is slated for removal. This is a report, not a fixer.
- **Error Prone** — compiler-integrated, rewrites at build time. Best wired into the build once; it then fixes continuously:
  `mvn -Derrorprone ...` with `-XepPatchChecks` + `-XepPatchLocation:IN_PLACE`, or the `error_prone_core` javac plugin.
- **OpenRewrite** — recipe-driven, the closest thing Java has to Go's `go fix`. It has an explicit `Modernize` recipe family and a **dry-run is first-class**:
  `mvn -U org.openrewrite.maven:rewrite-maven-plugin:dryRun -Drewrite.activeRecipes=org.openrewrite.java.migrate.UpgradeToJava21`
  → review the printed patch → re-run without `dryRun` to apply.
- **IDE/agent session** — `jdtls` (Eclipse JDT language server) exposes the same refactorings programmatically.

## 3. Write current from the start

Language features below are anchored by compiling each against `javac --release N` and taking the first release that accepts it. API members are anchored to the `@since` javadoc tag in the JDK's own `lib/src.zip` — Java's equivalent of Go's `GOROOT/api` (re-derivable locally).

### Language

| Instead of | Write | Needs |
|---|---|---|
| explicit local type in an obvious initializer | `var x = ...` | 10 |
| `if/else` chain returning a value | `switch` expression (`case X ->`) | 14 |
| concatenated multi-line string | text block (`"""`) | 15 |
| `if (o instanceof T) { T t = (T) o; ... }` | `if (o instanceof T t)` | 16 |
| boilerplate value class | `record` | 16 |
| `final class` + private ctor + manual subtype control | `sealed` / `permits` | 17 |
| `switch` on type with casts in each branch | pattern-matching `switch` | 21 |
| record decomposition via accessors | record patterns (`case P(int x)`) | 21 |

`default` methods on interfaces (8) and lambdas / method references / `Stream` (8) are below every plausible floor; they are not migration targets. Virtual threads (`Thread.ofVirtual`, 21) are an architectural change, not a rewrite — flag, never auto-apply.

### API

| Instead of | Write | Needs |
|---|---|---|
| `Arrays.asList(...)` for a fixed list | `List.of(...)` / `Set.of(...)` / `Map.of(...)` | 9 |
| `new ArrayList<>(other)` for a defensive copy | `List.copyOf(other)` | 10 |
| `!opt.isPresent()` | `opt.isEmpty()` | 11 |
| `optional.isPresent()` + separate `get()` | `ifPresentOrElse` / `stream()` | 9 |
| `str.trim()` for Unicode whitespace | `str.strip()` | 11 |
| `str.length() == 0` / `equals("")` | `str.isBlank()` | 11 |
| manual `new String(new char[n]).replace(...)` | `str.repeat(n)` | 11 |
| `split("\\R")` to iterate lines | `str.lines()` | 11 |
| manual indent/reindent helper | `str.indent(n)` | 12 |
| manual `Files.readAllBytes` + `new String(...)` | `Files.readString(path)` | 11 |
| manual byte comparison loop | `Files.mismatch(a, b)` | 12 |
| `.collect(Collectors.toList())` | `stream.toList()` (immutable) | 16 |
| `flatMap` with a constructed stream | `mapMulti` | 16 |
| two passes for two aggregates | `Collectors.teeing` | 12 |
| `new Thread(runnable).start()` at scale | virtual threads (`Thread.ofVirtual()`, `newVirtualThreadPerTaskExecutor()`) | 21 |
| ordered-first/last traversal with separate APIs | `SequencedCollection` / `SequencedMap` | 21 |

`String.formatted` (15) exists but `String.format` is not deprecated; treat it as optional style, not a defect.

## 4. Verify

Apply the project's own gates, escalating with the change: `mvn -q compile` (or `gradle compileJava`), then the full build, then tests. `--release` in the build already enforces the API ceiling — if the build passes, no rewrite broke the declared floor.

**Termination:** a clean diff with a failing build is not done (§7 of the manifesto).
