---
description: Generate AGENTS.md for the current project — from codebase analysis (no args) or from a brief (/generate-agents-md <brief text>)
---

# Generate AGENTS.md

Generate a comprehensive `AGENTS.md` file for the current working project. The workflow adapts based on whether a brief is provided as arguments.

**Mode detection:**

- **No arguments** (`/generate-agents-md`) → analyze the existing codebase and extract conventions, architecture, and standards.
- **With arguments** (`/generate-agents-md A Go REST API with...`) → generate AGENTS.md from the provided project brief, using codebase analysis only to complement or validate the brief.

The user's brief text is: `$ARGUMENTS`

---

## Mode A: Codebase Analysis (no `$ARGUMENTS`)

Use this mode when the project already exists and you need to extract conventions from the code itself.

### Phase 1: Discover

1. **Identify project type** — check for:
   - Language: `go.mod`, `package.json`, `Cargo.toml`, `pom.xml`, `build.gradle`, `pyproject.toml`, `requirements.txt`, `Gemfile`, `*.csproj`, `*.sln`, `mix.exs`
   - Framework: framework-specific directories and imports (React, Next.js, Django, Spring Boot, Gin, Actix, Rails, etc.)
   - Build system: Makefile, Justfile, Taskfile, scripts in `package.json`
   - Monorepo: workspaces (npm/pnpm/yarn, Go modules, Cargo workspace)
2. **Map directory structure** — read the top-level and first-level subdirectories. Identify:
   - Source code locations (`src/`, `cmd/`, `lib/`, `app/`, `internal/`, `pkg/`)
   - Test locations (`test/`, `tests/`, `__tests__/`, `*_test.go` patterns, `spec/`)
   - Configuration (`config/`, `.config/`, `configs/`)
   - Documentation (`docs/`, `doc/`)
   - Infrastructure (`deploy/`, `infra/`, `k8s/`, `terraform/`, `docker/`)
3. **Read existing agent config** — if `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursorrules`, or `.windsurfrules` already exist, read them for context. Preserve any valid existing content.

### Phase 2: Analyze Conventions

4. **Coding style** — check for:
   - Formatter config: `.prettierrc`, `.editorconfig`, `gofmt`/`goimports`, `rustfmt.toml`, `.clang-format`
   - Linter config: `.eslintrc*`, `.golangci.yml`, `ruff.toml`, `.flake8`, clippy config
   - Type checking: `tsconfig.json` strictness, mypy config
   - Import style: read 3–5 source files for import conventions
5. **Architecture patterns** — read key source files to identify:
   - Architectural style (MVC, Clean Architecture, Hexagonal, layered, microservices)
   - Common patterns (dependency injection, repository, strategy, factory)
   - Entry points (main files, route definitions, handler registration)
   - Module boundaries and dependency flow
6. **Testing conventions** — check for:
   - Test framework (Jest, pytest, Go testing, JUnit, RSpec, etc.)
   - Test directory structure (colocated vs separate)
   - Coverage requirements (coverage config, CI thresholds)
   - Test naming patterns from existing test files
7. **Error handling patterns** — read 2–3 source files to identify:
   - Error types (custom errors, error wrapping, sentinel errors)
   - Error propagation style (exceptions, Result types, error returns)
   - Logging conventions (structured vs unstructured, log levels)
8. **Security practices** — check for:
   - `.gitignore` patterns (secrets, env files)
   - Secret scanning config (`.gitsecret`, `trivy.yaml`, `snyk`)
   - Authentication/authorization patterns
   - Input validation patterns in handler/controller files

### Phase 3: Generate

9. **Write `AGENTS.md`** to the project root. Fill every section with facts discovered in Phase 1–2. Do not fabricate conventions — omit sections with no evidence.

---

## Mode B: Brief-Driven (has `$ARGUMENTS`)

Use this mode when the user provides a project description. The brief guides the AGENTS.md structure while codebase analysis (if files exist) complements it.

### Phase 1: Parse Brief

1. **Extract from the brief**:
   - Project name and purpose
   - Languages and frameworks
   - Architecture and design patterns
   - Key constraints and non-functional requirements
   - Target audience (team size, skill level)
2. **Identify tech stack** — map brief keywords to specific tools, frameworks, and conventions

### Phase 2: Analyze Codebase (if files exist)

3. **Quick scan** — if the project directory has existing source files:
   - Read project manifest (`go.mod`, `package.json`, `Cargo.toml`, etc.)
   - Map directory structure (top two levels)
   - Check for existing configs (linters, formatters, CI)
   - Read 2–3 source files to confirm or refine the brief
4. **Reconcile** — if codebase facts contradict the brief, prefer codebase evidence for technical details but preserve brief intent for aspirational/missing conventions

### Phase 3: Generate

5. **Write `AGENTS.md`** to the project root. Derive content primarily from the brief, supplemented by codebase facts where available.

---

## Output Template (both modes)

Write `AGENTS.md` with the following structure. Omit sections with no evidence (codebase mode) or no relevant brief content (brief mode).

```markdown
# {Project Name}

{One-line description.}

## Code Style

- Language(s): {languages with versions if available}
- Formatter: {tool and key settings}
- Linter: {tool and key rules}
- Indentation: {spaces/tabs, width}
- {Other discovered style conventions}

## Architecture

- Pattern: {e.g., layered, hexagonal, MVC}
- {Key structural observations: entry points, module boundaries, dependency flow}
- {Framework-specific conventions}

## Key Directories

- `{dir}/` — {purpose}

## Testing

- Framework: {test framework}
- Command: {how to run tests}
- {Coverage requirements or conventions}

## Error Handling

- {Error patterns: custom types, wrapping, propagation style}
- {Logging conventions}

## Security

- {Security practices}
- {Secret management}

## Conventions

- {Project-specific conventions with file references as evidence}
```

Append SPDD sections if the project uses spec-driven practices (has `plans/`, `spdd/`, design docs):

```markdown
## SPDD Methodology

- Spec location: {where specs/canvases live}

## Spec-Code Sync

| Change Type | Strategy |
|-------------|----------|
| New feature | Spec → Code |
| Logic correction | Spec → Code (fix spec first) |
| Bug fix | Spec → Code (fix spec first) |
| Refactoring | Code → Spec (refactor first, then sync) |
| Performance optimization | Code → Spec (optimize, update spec) |
```

---

## Phase 4: Validate (both modes)

10. **Verify the output**:
    - File exists at project root as `AGENTS.md`
    - Every statement is grounded in discovered evidence or provided brief — no hallucinated conventions
    - No placeholder text remains (no `{something}`)
    - Markdown is valid and well-structured
    - File is under 200 lines (concise is better)

## Rules

- **Evidence-based**: Every convention must be discoverable in the codebase (Mode A) or stated in the brief (Mode B). If no evidence, omit the section.
- **Preserve existing**: If `AGENTS.md` already exists, read it first. Merge new discoveries with existing content. Never delete custom sections.
- **No inline code**: Reference files by path, do not embed source code.
- **Concise**: Bullet points, not paragraphs. Under 200 lines.
- **Ask when uncertain**: If project type is ambiguous, ask the user before proceeding.
- **Respect gitignore**: Do not read files in `.gitignore` directories.
