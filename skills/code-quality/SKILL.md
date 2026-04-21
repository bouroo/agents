---
name: code-quality
description: Language-agnostic code quality principles for writing, reviewing, and refactoring code. Focus on readability, maintainability, and safety.
---
# Code Quality Guidelines

Language-agnostic code quality principles for writing, reviewing, and refactoring code. Focus on readability, maintainability, and safety.

## 1. Modular Architecture
- **Write libraries, not just programs**: Design reusable components with clear boundaries.
- **Isolate entry points**: The main entry point should only parse configurations, handle setup/teardown, and inject dependencies.

## 2. Test Everything
- **Dogfooding**: Write tests to use your own APIs and discover awkward design choices.
- **Comprehensive testing**: Focus on unit tests for small behaviors and integration tests for end-to-end scenarios.

## 3. Write Code for Reading
- **Minimize cognitive load**: Flatten nested logic, extract complex paperwork into smaller functions.
- **Glanceability**: Ask yourself if a reviewer can understand what the code does by reading it line-by-line.

## 4. Be Safe by Default
- **Always valid states**: Ensure objects and data structures are initialized in a valid state.
- **Useful defaults**: Make the zero or default value of a type useful and safe.
- **Named constants**: Avoid magic numbers or strings; use named constants to prevent typos.

## 5. Structured Error Handling
- **Wrap errors**: Add contextual information to errors instead of flattening them into generic strings.
- **Sentinel errors**: Use defined error values or types so callers can match and handle specific failure conditions gracefully.
- **Don't ignore errors**: Never silently swallow errors. Handle them or return them.

## 6. Avoid Mutable Global State
- **Prevent data races**: Do not use module-level or global mutable variables.
- **Encapsulation**: Encapsulate state within objects and pass them explicitly, or use proper synchronization mechanisms.

## 7. Manage Concurrency Carefully
- **Structured concurrency**: Ensure that all asynchronous tasks or threads terminate cleanly before their parent scope exits.
- **Avoid leaks**: Tie asynchronous operations to cancellation contexts or timeouts.
- **Directional data flow**: When using channels or queues, clearly define producers and consumers to avoid deadlocks.

## 8. Decouple Code from Environment
- **Inject configurations**: Do not hardcode environmental paths or read environment variables deep inside your logic. Pass them down.
- **No storage assumptions**: Do not assume the local disk is writable or permanent.

## 9. Design for Errors
- **Graceful degradation**: Anticipate failures and handle them safely rather than crashing the program.
- **Fail fast on internal bugs**: Reserve fatal crashes only for unrecoverable internal logic errors, not user inputs or network issues.

## 10. Log Actionable Information
- **No logorrhea**: Do not spam logs with trivia. Log only actionable errors that need fixing.
- **Structured logging**: Emit machine-readable formats (e.g., JSON) instead of plain text.
- **Data privacy**: Never log secrets, credentials, or sensitive personal data.

## 11. Large Project Quality
- **Review module boundaries**: Ensure each module exposes a clear contract. Changes within a module should not break consumers.
- **Actionable errors at every layer**: Error messages must indicate what failed and why, not just "error occurred." Include operation identifiers for tracing.
- **Log context for tracing**: Include request/operation identifiers in log entries to trace behavior across module boundaries.