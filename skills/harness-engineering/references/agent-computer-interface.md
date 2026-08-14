# Agent-Computer Interface (ACI) Tool & MCP Design

> Load on demand. The short pointer lives in `AGENTS.md` §2 (tool routing) and [harness-engineering](../SKILL.md) Cross-References; this file is the design checklist for when you *build* a tool, slash command, or MCP rather than merely call one.

The model is only as good as the interface it drives. Invest in the agent-computer interface (ACI) the effort you would give a human-facing one: a tool a model misuses is a tool whose spec failed, not a model that failed.

**Scope.** This covers *designing* tools and MCPs. Picking which *existing* capability to call is routing. See `AGENTS.md` §2. Right-sizing the *verification* a tool's output triggers is [right-sizing](./right-sizing.md).

---

## Stance

A tool is a contract, not a convenience wrapper. Every argument the model must guess at, every output field it must reverse-engineer, every overlapping responsibility between two tools is a failure mode you built in on purpose. The goal is the smallest, most self-evident contract that makes correct use the path of least resistance and misuse harder than correct use.

## Design checklist

- **Self-contained.** A caller holding only the tool's description can use it correctly. No tribal context, no "you also need to know." State the input shape, the output shape, and the side effects in the spec itself.
- **Non-overlapping.** Two tools must not answer the same call. If `search_code` and `find_symbol` both return matches for a name, the model is forced to guess; either merge them or draw a boundary the spec states ("string vs. symbol," "broad vs. precise"). One capability, one tool.
- **Poka-yoke arguments make misuse harder than correct use.**
  - Require **absolute paths**, never relative. A model mid-context loses the cwd; an absolute path cannot be silently wrong.
  - Prefer **typed enums** over free strings where the value set is closed (`"strict" | "loose"` beats `string`).
  - Make an argument **required** when ambiguity is the failure mode; optional only when the default is genuinely always-safe.
  - Accept the **most constrained shape** that still works (a structured object over a prose blob).
- **Token-efficient returns.** Return the decision, not the dump. Surface structure first counts, paths, headers, a summary and gate large bodies behind pagination or a follow-up call. A tool that returns 4,000 lines "to be safe" forces the model to re-read noise every turn and rots the context window context rot, `AGENTS.md` §8.
- **Complete spec contents.** One-line purpose; input shape with edge cases (empty, missing, very large); output shape; at least one worked example; and explicit **boundaries** what the tool will *not* do. Writing the spec is writing a docstring for a careful junior developer who has no other documentation.
- **Minimal formatting overhead.** Keep the description close to natural prose the model has seen at scale. Avoid gimmicks the model must parse mandatory line-counting, custom escaping schemes, positional flags dressed as tokens. Cognitive overhead spent decoding the format is overhead spent not solving the task.

## Command inputs passing arguments to a slash command

Commands ship as flat `<name>.md` files surfaced as slash commands by the hosts that support them. A command author writes one input contract that works on every host no per-host copy, no host-only frontmatter.

**The portable channel is `$ARGUMENTS`.** Every supported host substitutes it with the raw text the caller appended after the command name (`/review src/auth` -> `$ARGUMENTS` is `src/auth`). It is the only token with that property, so it is the only token that belongs in a command body.

| Token / field                 | portable? | why |
| ----------------------------- | :-------: | --- |
| `$ARGUMENTS` (all args)       |   yes     | every host substitutes it; when absent from the body, a host appends `ARGUMENTS: <value>` so the model still sees it |
| `$ARGUMENTS[N]` / `$N` index   |   no      | only some hosts substitute it, and the index origin differs across hosts (0-based vs. 1-based). A value silently shifts |
| `$name` named placeholder     |   no      | host-only; needs an `arguments:` list that not all hosts read |
| `argument-hint:` (command)     |   yes\*    | cosmetic autocomplete hint; Claude reads it, every other host ignores the unknown key |
| `argument-hint:` / `arguments:` (skill) | no | not in the Agent Skills spec frontmatter set; fails packaging on hosted markets and the API |

\* `argument-hint:` is allowed **only on commands** (it is behaviorally inert; unknown frontmatter is ignored by hosts that do not recognize it, and commands are not Agent-Skills-spec artifacts). On skills it is a spec-breaking field. `arguments:` (which wires `$name` substitution) is behaviorally functional and banned everywhere hosts that do not substitute `$name` leave the token in the prompt verbatim.

Positional indexing is **not portable** even where two hosts implement it, because the index origin differs (0-based on one host, 1-based on another): `$1` means the second argument on one host and the first on another. Use it only in a command documented as single-host, never in the shared core.

**No behaviorally host-specific frontmatter in the core.** `arguments:` (wires `$name` substitution) is functional and not portable; the repo's `G18` gate rejects it on every invokable surface. `argument-hint:` and `arguments:` are not in the Agent Skills spec frontmatter set (`name, description, license, compatibility, metadata, allowed-tools`), so `G18` rejects them on **skills**; `G5` rejects `arguments:` on commands but permits `argument-hint:` there. Hint text belongs in the `description` and the body's input section; `argument-hint:` only echoes the input shape for autocomplete, it must never carry the contract.

**Structured options ride inside `$ARGUMENTS`.** When a command takes flags or named options, the body declares the option grammar and the command parses `$ARGUMENTS` itself it does not ask the host to parse. This keeps one contract across hosts:

```
## Inputs
- `$ARGUMENTS` (optional): a target area, plus any of these flags (any order, `key=value`):
  - `--strict`      fail on warnings, not just errors (default: off)
  - `--focus=<area>` narrow the run to one system or path
  - `--since=<ref>`  only consider changes after this git ref
- If empty, <documented default>.
```

Declare the same grammar whether the caller writes `/verify --strict --focus=auth` or `/verify auth --strict`. Parsing is the command's job; the host only forwards the string.

**Authoring rules:**

- Put `$ARGUMENTS` in an `## Inputs` section near the top, with the default behavior when it is empty. If the body never references `$ARGUMENTS`, hosts that support argument appending still hand the text to the model but the contract is implicit. Make it explicit so the next host does not silently drop it.
- Optionally echo the input shape as `argument-hint:` on a command (e.g. `argument-hint: "[target] [--against=<ref>]"`) for hosts whose autocomplete shows it. It is a mirror of the Inputs section, never a substitute for it, and commands-only never on a skill.
- One command, one positional shape. If a command needs two distinct positional values, split it or move the second into a named option rather than relying on `$1`/`$2`.
- Keep the option set small and closed. Free-form flags multiply misuse surface; prefer one required target plus a few well-named toggles.
- Default to the safe, no-argument behavior. A command invoked with empty `$ARGUMENTS` must do something useful and non-destructive (review the current diff, verify the whole tree), never error or block waiting for input it never named.

## The feedback loop

A tool's spec is a hypothesis about how the model will use it. Validate it the way you validate code:

1. **Watch real usage.** Run the tool through representative turns; log where the model passes the wrong argument, the wrong shape, or calls the wrong sibling tool.
2. **Repeated misuse is a spec bug, not a model bug.** If the model reliably misuses an argument, fix the argument rename it, constrain its type, make it required, or fold it into another tool. Do not add a prose warning and ship.
3. **Convert recurring misuse into a gate.** A misuse you cannot design out becomes a deterministic check (a validator, a type constraint, a pre-flight assertion). This is the [Failure-Mode -> Control Map](../SKILL.md) applied to interfaces: the control lives in the harness, not in a reminder.

> **Kirby check.** A poka-yoke constraint that exists only because the current model cannot read a flat description is a bet against model improvement. Revisit each constraint when a stronger model arrives; yesterday's guardrail is tomorrow's dead weight (see [right-sizing](./right-sizing.md)).

---

## Cross-References

- [harness-engineering](../SKILL.md) (Failure-Mode -> Control Map), where recurring tool misuse becomes a deterministic gate.
- [Right-sizing the harness](./right-sizing.md). The Average Answer Trap and the Kirby Effect; applies to interface constraints too.
- [composition-patterns](./composition-patterns.md). How designed tools compose into delegation topologies.
