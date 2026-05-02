---
name: naming-conventions
description: Language-agnostic naming conventions for writing clear, predictable, and maintainable code.
---

# Naming Conventions

## General Principles

- Names reveal intent. Understand purpose without comments.
- Avoid abbreviations except widely accepted ones (`id`, `url`, `http`, `sql`).
- Consistent naming across the entire codebase.

## Variable Names

| Context | Convention | Example |
|---------|-----------|---------|
| Loop counter | Single letter | `i`, `j`, `k` |
| Error | `err` | `err`, `connErr` |
| Boolean | `is`/`has`/`can`/`should` | `isValid`, `hasPermission` |
| Collection | Plural | `users`, `items` |
| Map/dict | `keyToValue` | `idToName` |
| Buffer | `buf` | `readBuf` |
| Context | `ctx` | `ctx`, `requestCtx` |

## Function/Method Names

- Verb phrases: `calculateTotal`, `validateInput`, `parseResponse`
- Booleans: `isValid`, `hasPermission`, `canRetry`
- Constructors: `NewType`, `createType`, or language convention

## Type/Class Names

- Noun phrases: `UserService`, `BillingEngine`, `TokenValidator`
- Avoid generic names: `Manager`, `Handler`, `Helper`, `Util`
- Interfaces: describe behavior — `Reader`, `Writer`, `Stringer`

## Constants

- Named constants, never magic values: `MaxRetries`, `DefaultTimeout`
- Group related constants using enum/iota patterns

## Anti-patterns

- Naming based on implementation (`HashMapWrapper`) → name by purpose
- Over-abbreviation (`usrMgmtSvc`) → `userService`
- Numbered variables (`result1`, `result2`) → descriptive names
