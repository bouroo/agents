---
name: code-quality
description: Code readability, quality standards, and clean code principles. Use when writing new code, refactoring, reviewing code quality, naming variables/functions, or when the user mentions code style, readability, clean code, or quality standards.
---

# Code Quality

## Style Principles (Priority Order)

1. **Clarity** — Purpose and rationale must be obvious to the *reader*. Comment the "why", not the "what". Prioritize naming, organization, and helpful commentary.
2. **Simplicity** — Simplest mechanism that works. Prefer: core language > stdlib > third-party > custom code. Avoid unnecessary abstraction.
3. **Concision** — High signal-to-noise. Eliminate repetition, extraneous syntax, opaque names, and unneeded abstraction.
4. **Maintainability** — Easy for future programmers to modify correctly. Don't hide important details. Keep predictable names. Minimize dependencies.
5. **Consistency** — Match the broader codebase. Local consistency (within file/package) matters most. When in doubt, follow existing patterns.

## Naming

- No repetition when used in context — `time.Now()` not `time.GetCurrentTime()`
- Length proportional to scope, inversely proportional to usage frequency
- Single-letter only for narrow-scope: loop vars (`i`, `j`), method receivers
- Omit types from names: `count` not `intCount`, `users` not `userList`
- Omit words clear from context
- No package/module name in exported identifiers
- Acronyms stay consistent: `APIKey` not `ApiKey`, `userID` not `userId`

```
# Bad
intCount, userSlice, httpRequest, HttpURL
# Good
count,  users,      req,         URL
```

## Readability

- Flatten cognitive load: extract complex logic into named functions
- Cyclomatic complexity < 10 per function
- Write for reading first, execution second
- Named constants over magic values (`MAX_RETRIES = 3` not bare `3`)
- Handle errors/edge cases first — early return keeps normal path unindented

```
# Bad — normal path buried
func process(data) {
  if data != nil {
    if data.isValid() {
      // 50 lines of logic here
    } else {
      return err("invalid")
    }
  } else {
    return err("nil")
  }
}

# Good — guard clauses flatten the flow
func process(data) {
  if data == nil    { return err("nil") }
  if !data.isValid() { return err("invalid") }
  // normal path, unindented
}
```

## Checklist Before Committing

- [ ] Would a new team member understand this code in 60 seconds?
- [ ] Is every abstraction pulling its weight?
- [ ] Are names clear at the call site without surrounding context?
- [ ] Does this file/package match the surrounding style?
