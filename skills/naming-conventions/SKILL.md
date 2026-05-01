---
name: naming-conventions
description: Language-agnostic naming conventions for writing clear, predictable, and maintainable code.
---

# Naming Conventions

## General Principles

- Names should reveal intent. A reader should understand purpose without comments.
- Avoid abbreviations except widely accepted ones (`id`, `url`, `http`, `sql`).
- Use consistent naming across the entire codebase — don't mix styles.

## Variable Names

| Context | Convention | Example |
|---------|-----------|---------|
| Loop counter | Single letter | `i`, `j`, `k` |
| Error | `err` | `err`, `connErr` |
| Boolean | `is`/`has`/`can`/`should` prefix | `isValid`, `hasPermission` |
| Collection | Plural | `users`, `items`, `results` |
| Map/dict | `keyToValue` | `idToName`, `tokenToUser` |
| Buffer | `buf` | `readBuf`, `writeBuf` |
| Context | `ctx` | `ctx`, `requestCtx` |

## Function/Method Names

- Use verb phrases: `calculateTotal`, `validateInput`, `parseResponse`
- Booleans: `isValid`, `hasPermission`, `canRetry`
- Getters: `getName` or `name()` depending on language convention
- Setters: `setName` or `withName` for builder pattern
- Constructors: `NewType`, `createType`, or language convention

## Type/Class Names

- Use noun phrases: `UserService`, `BillingEngine`, `TokenValidator`
- Avoid generic names: `Manager`, `Handler`, `Helper`, `Util`
- Interfaces: describe behavior — `Reader`, `Writer`, `Stringer`; or prefix `I` if language requires

## Constants

- Named constants, never magic values: `MaxRetries`, `DefaultTimeout`
- Use language enum/iota patterns when values are related
- Group related constants together

## File and Package Names

- Lowercase, no underscores or hyphens: `userservice`, `billing`
- Package name should be a single word describing the domain
- Test files: `*_test`, `*.test`, `*.spec` per language convention

## Anti-patterns

- Naming based on implementation: `HashMapWrapper` → name by purpose
- Over-abbreviation: `usrMgmtSvc` → `userService`
- Numbered variables: `result1`, `result2` → `activeUsers`, `inactiveUsers`
- Scope-shadowing: same name at different scopes
