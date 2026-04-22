---
name: naming-conventions
description: Language-agnostic naming conventions for writing clear, predictable, and maintainable code.
---
# Naming Conventions

Language-agnostic naming conventions for writing clear, predictable, and maintainable code.

## 1. Consistent Casing
- **Follow project conventions**: Adhere to the project's established casing style (e.g., camelCase for identifiers, PascalCase for types). Do not mix styles arbitrarily.
- **Acronyms and Initialisms**: Keep acronyms consistently cased within identifiers (e.g., `apiKey` or `APIKey`, but not `ApiKey`). Apply this consistently to all multi-letter abbreviations (e.g., `userID`, not `userId`).

## 2. Identifier Clarity
- **Scope-dependent length**: The larger the scope of an identifier, the more descriptive its name should be. Single-letter names are acceptable only in very small, localized scopes (like loop counters).
- **Don't encode type in names**: Avoid including data types in identifier names (e.g., use `score`, not `scoreInt`; use `name`, not `nameString`), unless distinguishing between a parsed and unparsed version of the same value.
- **ASCII only**: Stick to standard ASCII characters. Avoid using obscure symbols or non-English letters.

## 3. Avoid Naming Clashes
- **Reserved words**: Never use names that clash with built-in keywords, base types, or widely used standard library components.

## 4. Module and Package Naming
- **Short and descriptive**: Module or package names should be short, easy to type, and typically a single word. Use concrete nouns (e.g., `orders`, `auth`).
- **Avoid catch-alls**: Do not use vague names like `utils`, `helpers`, `common`, or `types`. Break them down into specific, focused modules (e.g., `formatting`, `validation`).

## 5. Prevent Redundancy
- **Don't repeat the module name**: Avoid repeating the module or type name in its members.
  - *Bad*: `customer.CreateCustomer()` inside the `customer` module — the module context already indicates the type.
  - *Good*: `customer.Create()` inside the `customer` module — concise names that rely on module context.
- **Concise method names**: Keep method names concise based on their host type. Use `token.Validate()` rather than `token.ValidateToken()`.

## 6. Interface Naming
- **Behavior-based**: Interfaces that describe a single primary behavior should often be named after that action (e.g., `Reader`, `Writer`, `Authenticator`). Avoid generically suffixing with `Interface` unless mandated by framework conventions.

## 7. Large Project Naming
- **Establish conventions early**: Define project-wide naming conventions before scaling. Document agreed-upon patterns for module prefixes, abbreviations, and compound names.
- **Avoid cross-module collisions**: In large projects, ensure names don't clash across modules. Use namespace prefixes only when disambiguation is genuinely needed.
- **Consistency over brevity**: When the same concept appears across modules, use identical naming. Don't mix different verbs for the same operation (e.g., avoid using `getUser`, `fetchUser`, and `retrieveUser` interchangeably).