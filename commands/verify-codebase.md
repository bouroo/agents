---
description: Format, lint, type-check, scan, and test the project
---

# Verify Project Workflow

Run full project verification. Execute all steps autonomously without stopping for confirmation between steps.

$ARGUMENTS

## Workflow

1. **Discover tools** — Read project config to find formatters, linters, type checkers, test runners, security scanners
2. **Format** — Run formatter (e.g., `gofmt`, `prettier`, `rustfmt`)
3. **Lint** — Run linter (e.g., `golangci-lint`, `eslint`, `clippy`)
4. **Type-check** — Run type checker if applicable (e.g., `tsc --noEmit`, `mypy`)
5. **Security scan** — Run vulnerability and security analysis (see Security Scans below)
6. **Test** — Run test suite with coverage
7. **Report** — Summarize results, list failures with suggested fixes

**Do not stop after each step.** Run all verification steps in sequence, then report.

## Security Scans

Run all applicable scans for the project's language and ecosystem. Skip tools not installed or not relevant.

### Dependency Vulnerabilities

Scan lockfiles and manifests for known CVEs:

- **Go**: `govulncheck ./...`
- **Node.js**: `npm audit` / `pnpm audit` / `yarn audit`
- **Python**: `pip-audit` or `safety check`
- **Rust**: `cargo audit`
- **Java**: `mvn org.owasp:dependency-check:check` or `snyk test`
- **Ruby**: `bundle audit check`
- **Container**: `trivy fs .` or `grype .`

### Static Security Analysis (SAST)

Run language-specific security linters if available:

- **Go**: `gosec ./...`
- **JavaScript/TypeScript**: `eslint --plugin security` (if configured) or `semgrep --config auto`
- **Python**: `bandit -r .` or `semgrep --config auto`
- **Java**: `spotbugs` with FindSecBugs plugin
- **General**: `semgrep --config auto .` (works across all languages)

### Secrets Detection

Scan for accidentally committed secrets, keys, and tokens:

- **git-secrets**: `git-secrets --scan-history` (if repo has it configured)
- **gitleaks**: `gitleaks detect --source . --no-git` or `gitleaks detect`
- **trufflehog**: `trufflehog filesystem .`
- If none installed, skip this step — do not install without explicit permission.

### Container / IaC Scanning (if applicable)

Only run if Dockerfiles, Kubernetes manifests, or Terraform files exist in the project:

- **Dockerfile**: `hadolint Dockerfile` or `trivy config .`
- **Kubernetes**: `checkov -f <manifest>` or `trivy config .`
- **Terraform**: `tfsec` or `checkov -d .`

### Handling Security Findings

- **Critical/High severity**: Report as failures. Attempt auto-fix only for dependency upgrades (`npm audit fix`, `cargo audit -f`, etc.)
- **Medium severity**: Report as warnings with suggested remediation.
- **Low/Info**: Report only in verbose mode or summarize count.
- **False positives**: Note as "likely false positive" with brief reasoning; do not auto-dismiss.

## If Arguments Provided

Use `$ARGUMENTS` as the scope (specific files, directories, or test patterns).

## Auto-Fix

If a tool supports auto-fix, run it in fix mode first, then re-verify. Apply fixes autonomously — do not ask for permission.

For security vulnerabilities, auto-fix applies to:
- Dependency upgrades via package manager audit-fix commands
- Formatting/linting issues that touch vulnerable code patterns
- Do NOT auto-fix security findings by suppressing or ignoring them

## Failure Handling

When a step fails:
1. Parse the error output
2. Identify root cause
3. Fix the issue
4. Re-run the failing step
5. After fix, re-run ALL steps to check for regressions

**Fix failures autonomously.** Only stop and report if the same failure persists after two fix attempts.

For security scan failures:
- If a CVE has a known patched version, upgrade the dependency
- If upgrading breaks compatibility, report the conflict — do not force incompatible upgrades
- If no fix is available, note it as an accepted risk with justification

## Rules

- **Execute the full workflow.** Do not stop after each step to ask whether to continue.
- Auto-fix what can be auto-fixed. Report what requires manual intervention.
- If all steps pass, say so concisely — no need for a lengthy report.
- If arguments specify a scope, only run verification within that scope.
- **Security findings are never suppressed.** Report all findings with severity and remediation guidance.