---
name: naming-conventions
description: Language-agnostic naming conventions for writing clear, predictable, and maintainable code.
version: 1.0.0
triggers:
  - writing identifier names
  - naming variables, functions, types
  - consistent naming across codebase
---

# Naming Conventions

Language-agnostic rules for writing clear, predictable names.

## Variables

| Pattern | Use For | Examples |
|---------|---------|---------|
| `err` | Error values | `err`, `connErr` |
| `ctx` | Context objects | `ctx`, `reqCtx` |
| `req`/`resp` | Request/Response pairs | `req`, `resp`, `httpResp` |
| `buf` | Byte/string buffers | `buf`, `readBuf` |
| `data` | Arbitrary byte slices | `data`, `rawData` |
| `ok` | Boolean success | `ok`, `found` |
| `i`, `j` | Loop indices | `i`, `j`, `idx` |
| `n` | Counts/sizes | `n`, `count`, `len` |

## Functions

- **Names are verbs or verb phrases**: `calculateTotal`, `validateInput`, `parseResponse`.
- **Test names are sentences**: `TestCalculateTotalReturnsZeroForEmptyCart`.
- **Boolean functions use is/has/can/should**: `isValid`, `hasPermission`, `canRetry`.

## Types/Interfaces

- **Nouns**: `Customer`, `OrderProcessor`, `PaymentGateway`.
- **Interfaces describe behavior**: `Reader`, `Formatter`, `Validator`.
- **Avoid generic names**: `Manager`, `Handler`, `Helper`, `Util`.

## Constants

- Named constants, never magic values.
- `MaxRetryCount`, `DefaultTimeout`, `StatusOK`.

## Rules

- Short names for short-lived variables (loop counters).
- Longer names for longer-lived and broader-scope variables.
- Consistent naming within the same codebase — follow existing patterns.
- No abbreviations unless universally understood (`HTTP`, `URL`, `ID`).

## Checklist

- [ ] Consistent with existing codebase conventions
- [ ] Names reveal intent without comments
- [ ] No single-letter names outside loops
- [ ] No ambiguous abbreviations
- [ ] Test names read as sentences
