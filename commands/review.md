---
description: Review code for quality, security, and performance issues
subtask: true
---

You are performing a thorough code review on the specified target.

## Target

$ARGUMENTS

## Context

Recent changes:
!`git diff --stat HEAD~1 HEAD 2>/dev/null || git diff --stat --cached 2>/dev/null || echo "No git diff available"`

Current branch:
!`git branch --show-current 2>/dev/null || echo "Not a git repo"`

## Review Checklist

Review the code against these categories, in priority order:

### Security
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication/authorization bypasses
- Sensitive data exposure (secrets in logs, hardcoded credentials)
- Unsafe deserialization or eval usage
- Missing input validation at trust boundaries

### Correctness
- Logic errors, off-by-one errors, race conditions
- Unhandled error paths or swallowed errors
- Resource leaks (unclosed files, connections, goroutines)
- Incorrect concurrency patterns

### Performance
- N+1 queries or redundant I/O in loops
- Unnecessary allocations in hot paths
- Missing indices or inefficient data structures
- Synchronous operations that should be async

### Readability
- Functions longer than 40 lines or mixing abstraction levels
- Unclear naming — does the name say what it does?
- Magic values instead of named constants
- Missing or misleading comments

### Structure
- Tight coupling that should be injected
- Environment-dependent code outside the entry point
- Duplicated logic that should be extracted
- Violations of single responsibility

## Output Format

For each issue found, report:

```
### [SEVERITY] Category: Brief title
**File**: path/to/file:line_number
**Issue**: What's wrong
**Fix**: What to change
```

Severity levels: CRITICAL > HIGH > MEDIUM > LOW > INFO

End with a summary:
- Total issues by severity
- Top 3 most important fixes
- Overall assessment (ship / fix first / needs major rework)
