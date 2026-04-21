---
name: naming-conventions
description: Language-agnostic naming conventions for writing clear, predictable, and maintainable code.
---
# Naming Conventions

Language-agnostic naming conventions for writing clear, predictable, and maintainable code.

## 1. Consistent Casing
- **Standard rules**: Adhere to the project's idiomatic casing conventions (e.g., camelCase for variables, PascalCase for types). Do not mix snake_case and camelCase arbitrarily.
- **Acronyms and Initialisms**: Keep acronyms consistently cased within identifiers (e.g., `apiKey` or `APIKey`, but not `ApiKey`). This also applies to `ID` (e.g., `userID`, not `userId`).

## 2. Identifier Clarity
- **Scope-dependent length**: The larger the scope of a variable, the more descriptive its name should be. Single-letter names are acceptable only in very small, localized scopes (like short loop counters).
- **Avoid type inclusion**: Do not include the data type in the variable name (e.g., use `score`, not `scoreInt`; use `name`, not `nameString`), unless distinguishing between a parsed and unparsed version of the same value.
- **ASCII only**: Stick to standard ASCII characters. Avoid using obscure symbols or non-English letters.

## 3. Avoid Naming Clashes
- **Language keywords**: Never use names that clash with built-in language keywords, base types, or widely used standard library modules.

## 4. Module and Package Naming
- **Short and descriptive**: Module or package names should be short, easy to type, and typically a single lowercase word (e.g., `orders`, `auth`).
- **Avoid catch-alls**: Do not use vague names like `utils`, `helpers`, `common`, or `types`. Break them down into specific, focused modules (e.g., `formatting`, `validation`).

## 5. Prevent "Chatter"
- **Avoid redundancy**: Do not repeat the module or class name in its functions or methods.
  - *Bad*: `customer.NewCustomer()`, `customer.CustomerAddress`
  - *Good*: `customer.New()`, `customer.Address`
- **Method names**: Keep method names concise based on their host object. Use `token.Validate()` rather than `token.ValidateToken()`.

## 6. Interface Naming
- **Behavior-based**: Interfaces with a single primary behavior should often be named after that action (e.g., `Reader`, `Writer`, `Authenticator`). Avoid suffixing everything generically with `Interface` unless strictly mandated by framework conventions.

## 7. Large Project Naming
- **Establish conventions early**: Define project-wide naming conventions before scaling. Document agreed-upon patterns for module prefixes, abbreviations, and compound names.
- **Avoid cross-module collisions**: In large projects, ensure names don't clash across modules. Use namespace prefixes only when disambiguation is genuinely needed.
- **Consistency over brevity**: When the same concept appears across modules, use identical naming. Don't mix `getUser`, `fetchUser`, and `retrieveUser` for the same operation.