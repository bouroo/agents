# CONTEXT.md Format

## Structure

Most repos have a single context: one `CONTEXT.md` at the repo root.

```md
# {Context Name}

{One or two sentences: what this context is and why it exists.}

## Language

**Order**:
{One or two sentences defining the term}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

## Rules

- **Be opinionated.** When several words exist for one concept, pick the best and list the rest under `_Avoid_`.
- **Keep definitions tight.** One or two sentences; define what the term IS, not what it does.
- **Context-specific terms only.** General programming concepts (timeouts, error types, utility patterns) do not belong, however heavily the project uses them. Ask: unique to this context, or general? Only the former.
- **Group under subheadings** when natural clusters emerge; one cohesive area can stay a flat list.

## Multi-context repos

A `CONTEXT-MAP.md` at the repo root lists the contexts, where each lives, and how they relate:

```md
# Context Map

## Contexts

- **Ordering** (./src/ordering/CONTEXT.md): receives and tracks customer orders
- **Billing** (./src/billing/CONTEXT.md): generates invoices and processes payments
- **Fulfillment** (./src/fulfillment/CONTEXT.md): manages warehouse picking and shipping

## Relationships

- **Ordering -> Fulfillment**: Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking
- **Fulfillment -> Billing**: Fulfillment emits `ShipmentDispatched` events; Billing consumes them to generate invoices
- **Ordering <-> Billing**: shared types for `CustomerId` and `Money`
```

Which structure applies: `CONTEXT-MAP.md` present -> read it to find the contexts; only a root `CONTEXT.md` -> single context; neither -> create the root `CONTEXT.md` lazily when the first term resolves. In a multi-context repo, infer which context the topic touches; ask only if genuinely unclear.

Distilled from [mattpocock/skills](https://github.com/mattpocock/skills) (`domain-modeling/CONTEXT-FORMAT.md`, MIT).
