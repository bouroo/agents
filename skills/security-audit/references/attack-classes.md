# Attack Classes

Coverage units for a security audit, and the discipline that keeps each class from producing noise. Load with [SKILL.md](../SKILL.md).

**Choosing classes.** Map the target's entry surfaces first, then select the classes that reach them — not every class applies to every codebase. Split large targets per subsystem, and split a class further when one agent cannot hold both halves (auth bypass vs. authorization logic is the classic case).

**Every class obeys the candidate gate.** A candidate names the lower-trust principal, the input or action, the intended control, the crossed boundary, the affected principal or resource, and the concrete result. The "not a finding" lines below are that gate applied to each class.

## Injection

Trace untrusted input from entry point to sink. The sink depends on the target: SQL and HTML output, shell commands, template engines, file paths, redirects, and deserialization for web; any function that consumes caller data unvalidated for a library; command construction and path handling for a CLI; query construction and log injection for a service.

Do not stop at the direct path. Look for **stored injection** — data written safely, then read and used in a dangerous context by other code — and for injection through **keys, headers, and metadata**, not only values. Look at secondary sinks: logs, caches, search indexes, analytics.

## Access control

Go past whether a permission check exists and ask whether it checks the *right* permission, for the *right resource*, by the *right mechanism*.

- Is there a second path to the same state change that checks a weaker permission?
- Can a request-body field override what the permission intended to restrict?
- Does an endpoint authenticate but forget to authorize?
- Does one resource have several access paths with inconsistent checks?
- Do bulk, batch, export, and import operations enforce per-item permissions?

## Business logic

Standard scanners cannot find these, and they carry the highest impact. For each workflow:

- **State machine** — can a step be skipped or replayed, can the flow run backward, what does partial failure leave behind?
- **Races** — check-then-act operations that produce invalid states: double-spend, double-approve, lost updates.
- **Quantities** — negative, zero, overflow, precision loss, string/number coercion.
- **Boundary mismatch** — input to one operation bypassing a rule enforced on a different operation for the same effect.
- **Implicit trust** — data from storage, config, another component, or a plugin assumed safe because "we validated it on the way in." What if a different code path wrote it?
- **Time** — expiry, scheduling, rate windows, clock skew, timezone disagreement between components, and the exact boundary instant.
- **Defaults** — the security posture when config is missing, a flag is off, a dependency is unavailable, or a migration is half-applied.

## Feature abuse and data leakage

Legitimate features used for unintended purposes — bugs in the design, not the code.

- **Export as exfiltration** — can a low-privilege user trigger an export, snapshot, or backup containing data above their access level, deleted or draft content, or unpruned revision history?
- **Import as injection** — can an import overwrite existing data, skip normal validation, or write into collections the user cannot write directly?
- **Search as oracle** — does search reveal the existence of content the user cannot read? Do filters probe statuses, roles, or hidden fields? Does sort order leak a hidden value?
- **Enumeration** — do errors, timings, response sizes, or status codes distinguish "does not exist" from "no access"?

## Resource and file handling

Path traversal (including through symlinks, encodings, and null bytes) · SSRF (including redirects, DNS rebinding, and URL-parser differentials) · unsafe deserialization and archive extraction · temp-file handling · race conditions on file operations (TOCTOU between check and use) · memory-safety classes (buffer overflow, use-after-free, integer overflow) where the language allows them.

## Cryptography and secrets

Weak randomness for tokens, keys, or nonces · hardcoded secrets, and secrets reaching logs, errors, URLs, or client-visible responses · broken key derivation, missing HMAC verification, nonce reuse · comparison that leaks timing · misuse of a primitive (ECB, unauthenticated encryption, static IV) · **the failure path** — does a crypto error fall back to no crypto?

**Not a finding** unless a secret reaches a lower-trust reader, output, artifact, or log: a secret *reference* is not disclosure.

## Domain selection

Pick the domains the target actually speaks, and prepend that domain's discipline to the hunter's brief.

**HTTP, web, and identity** — sessions, JWT, OAuth/OIDC, SAML, recovery, MFA, passkeys, API keys, mTLS, custom HTTP parsers, reverse proxies.
> Framing and cache findings need *two* interpretations of the same request or key — name both components and the exact normalized value on each side. For every credential, find signature verification and every binding its role requires: issuer, audience, origin, session, principal, resource, assurance, expiry. `Host`, `Forwarded`, `Origin`, `Referer`, redirect targets, and request-derived URLs are trust decisions — trace each to the identity it affects. A missing header, cookie attribute, MFA prompt, or rate limit is **not** a finding alone; require an accepted invalid request, cross-principal impact, an assurance downgrade, or credential disclosure.

**Client-side and browser** — SPAs, extensions, webviews, service workers, cross-window messaging, DOM rendering.
> A candidate needs a controllable source *and* an executing or disclosing sink. Impact must reach a victim's session, another origin, or shared persistence — self-injection and disclosure of the attacker's own data are **not** findings. Framework escaping, same-origin policy, CSP, and `noopener` defaults are real controls; verify them before assigning impact.

**AI, LLM, and agents** — chatbots, RAG, persistent memory, tool-calling loops, prompt assembly, model-controlled actions.
> Prompt injection alone is **not** a finding. Require a code-level boundary failure: content reaching another principal's context, invoking authority the requester lacks, disclosing data they cannot read, or driving a sink they cannot reach. Model output, memory, tool descriptions, and MCP responses are untrusted inputs — point to the code that grants authority or feeds a sink. A guardrail prompt is not a control; count only deterministic checks, resource-scoped authorization, isolation, and constrained credentials.

**Cloud and deployment** — IAM, infrastructure as code, containers, service mesh, serverless, ingress, object storage.
> Do not infer live exposure from a manifest alone: establish which environment consumes it, what overlays modify it, and whether the path is active. Map each workload identity to specific operations and resources; broad policy is a finding only when lower-trust input reaches an unauthorized action. Only count a control whose configuration *and* attachment are both visible.

**Supply chain and release** — dependency resolution, generated inputs, CI, signing, promotion, updates, plugins.
> A dependency pin is not a finding without a path by which lower-trust input reaches the unpinned resolution. Build and release steps run with authority; ask who can change what the pipeline consumes.

**Protocols, RPC, and messaging** — gRPC, GraphQL transports, Protobuf/Thrift, custom protocols, queues, brokers, webhooks, streaming RPC.
> Establish which side enforces which invariant, and what each does with a malformed message. A serializer is not a validator.

**Data isolation and lifecycle** — multi-tenant stores, caches and search, object links, analytics, export, backup, migration, deletion, retention, restore.
> Trace the tenant or account key from the request to every store, cache, index, and export that answers it. Deletion and retention are boundaries too: what survives a delete, and who can still read it?

**Desktop, mobile, and local IPC** — native apps, deep links, webview bridges, exported components, privileged helpers, local daemons, sockets.
> A local boundary is still a boundary: any process on the host may be the lower-trust principal. Verify that the privilege gap between a helper and its caller is actually enforced, not assumed from the absent attacker.

**Resource exhaustion and availability** — untrusted work consuming shared CPU, memory, disk, connections, workers, queues, quotas, or paid spend.
> Name the shared resource, the bound that should cap it, and what one caller can deny to another. Do not test availability against a live or shared process.

## Anti-patterns

1. A checklist deviation presented as a vulnerability.
2. Defense-in-depth advice with no reachable boundary violation.
3. Testing a live or shared environment where a bounded local check would do.
4. Guessing proxy, provider, browser, identity, or deployment behavior absent from the source.
5. Counting intended authority or self-impact as a cross-boundary result.
6. Reporting a parser or runtime effect stronger than what was observed.
7. Assigning severity to a `needs_validation` record.
8. Presenting scanner output as a confirmed finding.
