# TypeScript / JS adapter

Two baselines, and they answer different questions. `tsconfig.json` `target`/`lib` governs what the *type system and emitter* allow; `package.json` `engines.node` governs what the *runtime* actually has. A project can happily compile `Array.prototype.toSorted` and still crash on Node 18.

Implements [modernize-coding](../../SKILL.md) for TypeScript and JavaScript.

## 1. Detect the baseline

1. **`tsconfig.json` `compilerOptions.target`** — controls which features the compiler **downlevels** and sets the default `lib`. Values: `ES5`, `ES2015` (`ES6` alias), `ES2016`–`ES2024`, `ESNext` (case-insensitive; `ESNext` means "newest the installed TypeScript supports", not a fixed standard).
2. **`compilerOptions.lib`** — controls which **type declarations** are available. Independent of `target`: `target: "ES5"` with `lib: ["ES2024"]` emits old syntax while type-checking modern APIs. **`target` provides no runtime polyfills** — it changes emitted syntax only.
3. **`package.json` `engines.node`** and any `browserslist` — the real runtime floor, and the one that decides whether a modern API is *safe*, not merely compilable.
4. **TypeScript version** (a devDependency) — some syntax is TS-only and has no JS-target equivalent.

A modern `target` with an old `engines.node` is the single most common trap here: the code compiles, the types pass, and it crashes in production. Check both before calling anything modern.

## 2. Rewrite existing code

- **`tsc`** — **reports, it does not rewrite source.** `tsc --noEmit` type-checks; it will not modernize anything. Do not treat it as a fixer.
- **ESLint `--fix`** — rewrites source for fixable rules. Dry-run first:
  `eslint --fix-dry-run .` prints what it would change without writing; then `eslint --fix .`. Rules that modernize (`prefer-const`, `no-var`, `prefer-arrow-callback`, `prefer-template`, `no-useless-concat`, `prefer-object-spread`, `prefer-optional-chaining`, `prefer-nullish-coalescing`, `logical-assignment-operators`) come from `eslint:recommended` plus `typescript-eslint`.
- **`jscodeshift`** — the codemod runner, for rewrites ESLint has no rule for. You supply a transform; it applies it across many files:
  `npx jscodeshift -t <transform.js> <path> --dry --print` (dry-run and print) → drop `--dry --print` to write. The registry at [codemod.com](https://codemod.com) carries published transforms for common migrations.
- **`ts-morph`** — programmatic, for one-off project-specific rewrites where a codemod would be overkill.

Order: codemod the structure, `eslint --fix` the idiom, then format.

## 3. Write current from the start

Edition years below are from TC39's own finished-proposals table (the year the proposal reached stage 4 / shipped in that year's spec) — see [verify](verify.md) to re-derive them.

### Syntax

| Instead of | Write | Needs |
|---|---|---|
| `var` | `const` (default) / `let` (when reassigned) | ES2015 |
| `function () {}` as a callback | arrow function | ES2015 |
| `"a" + b + "c"` | template literal `` `a${b}c` `` | ES2015 |
| `arguments` in a non-arrow function | rest parameters `...args` | ES2015 |
| `.concat()` / `.apply()` for spreading | spread `[...a, ...b]` / `f(...args)` | ES2015 |
| `Object.assign({}, a, b)` | object spread `{ ...a, ...b }` | ES2018 |
| `x && x.y && x.y.z` | optional chaining `x?.y?.z` | ES2020 |
| `x !== null && x !== undefined ? x : d` | nullish coalescing `x ?? d` | ES2020 |
| `if (!x) x = d` | `x ??= d` / `||=` / `&&=` | ES2021 |
| `Object.prototype.hasOwnProperty.call(o, k)` | `Object.hasOwn(o, k)` | ES2022 |
| `delete obj[k]` then re-add to immutably remove | rest destructuring `const { [k]: _, ...rest } = obj` | ES2018 |
| a `try { } catch { }` around a `switch` for exhaustiveness | `satisfies` / exhaustive `switch` with `never` | TS 4.9 |

### Runtime API (check `engines.node` before using)

| Instead of | Write | Needs |
|---|---|---|
| `arr[arr.length - 1]` | `arr.at(-1)` | ES2022 |
| manual reverse-index loop to find from the end | `arr.findLast()` / `findLastIndex()` | ES2023 |
| `[...arr].sort()` to sort immutably | `arr.toSorted()` | ES2023 |
| `[...arr].reverse()` | `arr.toReversed()` | ES2023 |
| `arr.map((v, i) => i === n ? x : v)` | `arr.with(n, x)` | ES2023 |
| `arr.filter(...)` + `splice` to delete immutably | `arr.toSpliced()` | ES2023 |
| `JSON.parse(JSON.stringify(o))` to deep-clone | `structuredClone(o)` | Node 17+ / all modern browsers (WHATWG, **not** ECMAScript) |
| `lodash.get` for a guarded path read | optional chaining | ES2020 |
| a `class` with `_private` naming convention | `#private` fields | ES2022 |
| a module-level `await` wrapper IIFE | top-level `await` (ESM only) | ES2022 |

**`structuredClone` is not ECMAScript** — it comes from the WHATWG HTML spec, so its floor is a runtime version, not an edition. It also cannot clone functions, DOM nodes, or class prototypes, and it throws on those; it is not a drop-in for every `JSON.parse(JSON.stringify(...))`.

## 4. Verify

`tsc --noEmit` → `eslint .` → the bundler/build → `npm test` (or the repo's runner). Then the step the tooling cannot do for you: confirm every modern API used is available at the declared `engines.node`. `npx browserslist` / `npx caniuse` help; when unsure, state the assumption rather than claiming it verified.

**Termination:** a clean diff with a failing build is not done (§7 of the manifesto).
