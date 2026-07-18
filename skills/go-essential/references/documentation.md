# Documentation - Depth

Loaded on demand from [go-essential](../SKILL.md) §12. The short rules live there; this file is
the why, the worked code, and the templates.

Documentation is a first-class deliverable. Write for the reader who has never seen this
codebase - the next maintainer, the new hire, or an AI agent scanning the project cold.

## Writing Principles

Apply to every piece of documentation you write or review.

**Concision** - write the shortest version that carries the idea. Remove ornament and hollow
transitions. Never drop facts, warnings, or user-requested depth.

**Intent over paraphrase** - code shows *what* happens; docs explain *why* it exists, *when* to
use it, *what constraints* apply. A comment that only restates the signature wastes the reader's
time.

**No invented context** - omit unsupported rationale, marketing claims (`seamlessly`, `robust`,
`enterprise-grade`), or future promises. Leave gaps visible rather than filling with speculation.

**Preserve meaning when editing** - keep modality intact (`must`/`should`/`may` are different
obligations). Preserve conditions, warnings, required actions. A cleaner sentence that changes
obligations is wrong.

**Anti-patterns to remove on sight:**

- Pure-paraphrase comments that start with the name but add nothing (godoc requires the name as
  prefix - what it forbids is stopping there).
- Signature restatement.
- Marketing vocabulary.
- Groundless future claims (`future extensibility`, `easy to scale`).
- Hollow transitions (`it's worth noting that`, `in conclusion`).
- Template padding that adds no information.

## Doc Comments

Every exported identifier has a doc comment. The comment starts with the name and a verb phrase.

```go
// CalculateDiscount computes the final price after applying tiered discounts.
// Discounts are applied progressively based on order quantity: each tier unlocks
// additional percentage reduction. Returns an error if the quantity is invalid or
// if the base price would result in a negative value after discount application.
//
// Parameters:
//   - basePrice: The original price before any discounts (must be non-negative)
//   - quantity: The number of units ordered (must be positive)
//   - tiers: Discount tiers sorted by minimum quantity threshold
//
// Returns the final discounted price rounded to 2 decimal places.
// Returns ErrInvalidPrice if basePrice is negative.
// Returns ErrInvalidQuantity if quantity is zero or negative.
//
// Example:
//
//	tiers := []DiscountTier{
//	    {MinQuantity: 10, PercentOff: 5},
//	    {MinQuantity: 50, PercentOff: 15},
//	}
//	final, err := CalculateDiscount(100.00, 75, tiers)
func CalculateDiscount(basePrice float64, quantity int, tiers []DiscountTier) (float64, error) {
    // ...
}
```

**Rules:**

- **Name starts the comment.** `CalculateDiscount` - not `This function` or `// calculates`.
- **Explain why, when, and constraints** - not what the code already shows.
- **Name the sentinel errors returned.** `// Returns ErrInvalidPrice if basePrice is negative.`
- **Parameters block** when non-trivial; use `//   - name: description` (two-space indent, dash).
- **Example block** uses indented Go code (one tab inside the comment).

### Package Comments

A package has exactly one package comment, on exactly one file. Convention: a `doc.go` file
holding only the package comment when it's long.

```go
// Package discount computes progressive discounts on orders.
//
// The package supports tiered pricing, quantity-based rebates, and bulk deals.
// Configure via Tiers; call CalculateDiscount to compute a final price.
//
// Example:
//
//	tiers := []discount.Tier{{MinQuantity: 10, PercentOff: 5}}
//	final, err := discount.Calculate(100.0, 25, tiers)
package discount
```

### Deprecation and Bug Markers

```go
// Deprecated: Use NewClient instead; NewClientWithTimeout sets no defaults and is unsafe.
// Will be removed in v3.0.0.
func NewClientWithTimeout(...) *Client { ... }

// BUG(bob): Calculate does not handle quantity > math.MaxInt32 correctly.
// See issue #123.
```

`gopls` and linters surface `// Deprecated:` markers at every callsite with a strikethrough.

## Example Test Functions

`Example_xxx` test functions are executable documentation - they render under godoc and are
verified by `go test`. Drift between docs and code becomes a build failure, not a stale comment.

```go
func ExampleCalculateDiscount() {
    tiers := []DiscountTier{
        {MinQuantity: 10, PercentOff: 5},
        {MinQuantity: 50, PercentOff: 15},
    }
    final, _ := CalculateDiscount(100.0, 75, tiers)
    fmt.Printf("%.2f\n", final)
    // Output: 85.00
}
```

The `// Output:` comment is the assertion. If the function's stdout doesn't match exactly, the
test fails. Use `// Unordered output:` for non-deterministic ordering.

## Go Playground Demos

For libraries, link a runnable demo in the doc comment:

```go
// Play: https://go.dev/play/p/abc123XYZ
```

pkg.go.dev renders this as a "Run" button. Use the [Go Playground](https://go.dev/play/) to
create and share URLs.

## README

Follow a stable section order:

1. **Title** - project name as `# heading`.
2. **Badges** - shields.io pictograms (Go version, license, CI, coverage, Go Report Card, Go
   Reference).
3. **Summary** - 1-2 sentences explaining what the project does.
4. **Demo** - code snippet, GIF, screenshot, or video showing the project in action.
5. **Getting Started** - installation + minimal working example.
6. **Features / Specification** - detailed feature list or specification.
7. **Contributing** - link to CONTRIBUTING.md or inline if short.
8. **Contributors** - thank contributors (badge or list).
9. **License** - license name + link.

Common Go project badges:

```markdown
[![Go Version](https://img.shields.io/github/go-mod/go-version/{owner}/{repo})](https://go.dev/)
[![License](https://img.shields.io/github/license/{owner}/{repo})](./LICENSE)
[![Build Status](https://img.shields.io/github/actions/workflow/status/{owner}/{repo}/test.yml?branch=main)](https://github.com/{owner}/{repo}/actions)
[![Go Report Card](https://goreportcard.com/badge/github.com/{owner}/{repo})](https://goreportcard.com/report/github.com/{owner}/{repo})
[![Go Reference](https://pkg.go.dev/badge/github.com/{owner}/{repo}.svg)](https://pkg.go.dev/github.com/{owner}/{repo})
```

## CONTRIBUTING.md

Get a new contributor to a working build in under 10 minutes. If setup takes longer, fix the
process (Makefile, docker-compose, devcontainer) - don't document the pain.

Required sections:

- Prerequisites (Go version, OS notes).
- Clone and build.
- Run the tests.
- PR process (style, signoff, branch naming).

## CHANGELOG

Follow [Keep a Changelog](https://keepachangelog.com/) format or use GitHub Releases.

```markdown
## [1.2.0] - 2026-07-18
### Added
- Tiered discount calculation with configurable thresholds.
### Changed
- `Calculate` now returns `(float64, error)` instead of panicking on bad input.
### Deprecated
- `NewClientWithTimeout` - use `NewClient` with the `WithTimeout` option.
### Fixed
- Integer overflow on `quantity > math.MaxInt32`.
```

Each entry answers *what changed for the reader*. Internal refactors without user-visible impact
belong in commit history, not the changelog. Don't inflate a fixed edge case into a broad
"reliability improvement" claim.

## API Documentation

| API Style    | Format      | Tool                                         |
| ------------ | ----------- | -------------------------------------------- |
| REST/HTTP    | OpenAPI 3.x | swaggo/swag (auto-generate from annotations) |
| Event-driven | AsyncAPI    | Manual or code-gen                           |
| gRPC         | Protobuf    | buf, grpc-gateway                            |

Prefer auto-generation from code annotations when possible. Hand-maintained docs drift.

## llms.txt

An `llms.txt` at the repo root gives LLMs and AI coding tools a structured overview of the
project:

- Project name and one-line summary.
- Key entry points (`cmd/`, main package, public API).
- Architectural decisions.
- Pointers to deeper docs.

For libraries: also register on [pkg.go.dev](https://pkg.go.dev), Context7, DeepWiki, and
zRead for AI discoverability - even for private internal libraries, the discovery surface helps
internal tools.
