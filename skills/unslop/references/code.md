# Code rules

Rule ids are stable (`C1`, `C2`, ...). A removed rule leaves a gap. Each rule names a residue pattern in source, tests, or interfaces, and its fix. These cover the back-end and library half of a SWE task; the UI half lives in [ui.md](ui.md).

## Placeholders and stubs

**C1. The placeholder body.** A function or method whose body is `pass`, `...`, `return None`, `return []`, `return {}`, `TODO`, or a bare `throw new Error("Not implemented")` where the task claims it works. Either the task ships the implementation or the artifact states plainly that it is a stub. A stub in a diff presented as a feature is a false claim.

**C2. The signature that promises more than the body.** A function named `calculate_total` that returns a constant, or a getter that ignores its argument. The name is the contract; if the body does not honour it, rename or implement.

**C3. The sample data that shipped.** `John Doe`, `foo@bar.com`, `555-0123`, `test_user`, `aaa.bbb`, `lorem ipsum`, `example.com` standing in for real values in a fixture, a config default, or a seed file. Real-looking data (`anna.kowalski@example.org`, a plausible id) reads as intentional; `foo` reads as residue. Three outcomes, in order: if the real source is already in scope (a field the caller passes, a fixture the repo carries), read from it; if the value is a fixture, replace it with plausible data; if no source exists anywhere, the value is *missing work* and goes to the build queue as `PENDING:` — never invent the source, and never leave the placeholder shipping as if it were data.

**C4. The mock that mirrors the implementation.** A fake whose methods return what the production code returns, so the test passes without exercising anything. The fake asserts nothing; it is theatre.

**C5. The not-yet file.** A reference to a module, route, table, or config key that does not exist. Search the tree for each one before shipping.

## Over-generation

**C6. The abstraction with one caller.** An interface, factory, registry, or generic wrapper that only one implementation uses. The `quality` skill's simplicity rule owns the verdict; this rule names the shape to look for.

**C7. The flag nobody sets.** A feature flag, config key, environment variable, or setting whose only value in the repository is the default. A knob with one position is not configuration.

**C8. The layer that only forwards.** A wrapper, facade, or "service" whose method calls one other method and returns the result unchanged.

**C9. The validation of something already valid.** A null check on a value the type system guarantees is not null, or a guard the caller cannot bypass. Defensive code at a boundary is right; defensive code everywhere is residue.

**C10. The exception hierarchy with no catcher.** Custom exception classes nobody catches, or a catch block that swallows every error type identically.

**C11. The retry, timeout, or circuit breaker nobody configured.** A resilience wrapper at its default settings, carrying a policy no one chose: three attempts, one second, on every call path.

## Comments and documentation in code

**C12. The narration comment.** A comment that restates the next line: `# increment the counter` above `counter++`. Per the `quality` skill's comment rule, a comment earns its place only by stating a non-derivable why.

**C13. The swallowed error.** `catch (e) { }`, `except Exception: pass`, or a `_ = err` that discards the cause. Never swallow an error; wrap it with context and propagate it.

**C14. The comment that narrates the change.** "Updated to use the new API", "Refactored for clarity", "Added error handling". These describe the diff, not the code, and they rot on the next edit.

**C15. The commented-out block.** Dead code kept as a comment. It is unmaintained source that no compiler checks; delete it, and let the history keep it.

**C16. The docstring that repeats the signature.** `"""Returns the user."""` above `def get_user(...)`. State the contract the signature cannot carry: the precondition, the postcondition, or the failure mode.

**C17. The file header that says nothing.** A banner naming the project, the author, or the framework, above the license header the project already has.

## Naming and structure

**C18. The vague name.** `data`, `info`, `temp`, `result`, `value`, `item`, `obj`, `utils`, `helpers`, `common`, `stuff` as a type, field, or module name. Name the domain, not the container. A job-named class is not vague here: C25 asks for exactly that, so `PaymentProcessor` and `OrderManager` stand. Only a bare `Processor`, or a generic prefix like `DataManager`, is residue.

**C19. The duplicated block.** The same logic in two places, differing by one line. Copy-paste-with-edits is the strongest duplication smell; the `TWINS:` gate in the `quality` skill owns the fix.

**C20. The layer that is only a pass-through.** A module that adds a name to another module without adding behaviour, so the reader pays a hop for nothing.

**C21. The default that hides a bug.** A zero value, empty list, or `nil` returned to mean "not computed yet", which the caller cannot distinguish from a real result. Make the absence explicit in the type.

**C22. The magic value.** A bare number or string whose meaning is not in the name: `if status == 3`, `timeout=30`. Name it or cite where it comes from.

**C23. The inconsistent vocabulary.** The same domain entity named three ways across the layers (`user`, `account`, `customer`), so a reader has to map them. One term, chosen from the project's own glossary.

**C24. The over-generalized name.** `process`, `handle`, `execute`, `run` on a function that does one specific thing. `retry_payment` beats `process_transaction`.

**C25. The abstraction noun.** A class or module named after a concept instead of a job: `PaymentProcessor`, `DataValidator`, `OrderManager`. Name the job it does for the caller.

## Data and interfaces

**C26. The stringly typed contract.** A status, type, or role carried as a free string where an enum, union, or constant set already exists in the project.

**C27. The unbounded field.** A field, parameter, or column with no maximum, no validation, and no stated unit, where the value reaches a database, a queue, or an external API.

**C28. The error shape that differs per endpoint.** Two handlers returning `{error}` and `{message}` for the same failure class. One error shape, one place that builds it.

**C29. The API that leaks the storage.** A response carrying an internal column, a database id, or a field the client cannot act on.

**C30. The pagination that does not paginate.** An endpoint promising `limit`/`offset` and returning the whole table.

**C31. The test that asserts the mock.** A test whose assertion reads back the value the fake was given, so it fails only if the fake changes. Assert the observable behaviour, not the wiring.

**C32. The test with no failure mode.** A test covering only the happy path of a function that can fail. Cover the error and boundary paths, per the `quality` skill's craft rule.

**C33. The snapshot that snapshots the bug.** An approved snapshot containing the wrong value, which turns the defect into the expected output.

## The claim in code

**C34. The comment that promises a guarantee.** "This is thread-safe", "Guaranteed to be idempotent", "No partial writes". A guarantee stated in a comment and not enforced by a test or a type is a claim with no referent; enforce it or delete it.

**C35. The metric with no definition.** A counter or field named `duration_ms`, `score`, or `quality` whose unit, range, or meaning is not stated. Define it where it is produced.

**C36. The benchmark in the comment.** "10x faster" in a comment or a doc, with no command, no baseline, and no date. Per the `quality` skill's performance rule, an optimization claim cites command, output, and delta; a bare multiplier is residue.

**C37. The catch that only re-raises.** A `try` whose `except` re-raises the same exception it caught, or returns the value it already had. It adds a frame without adding behaviour; delete it and let the exception propagate. A catch that wraps or annotates the cause is not this rule, it is C13's fix.

**C38. The catch-all that catches nothing specific.** `except Exception` around a call that raises specific types. Catch what the code can actually handle, and let the rest propagate.
