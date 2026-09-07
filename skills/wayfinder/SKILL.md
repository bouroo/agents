---
name: wayfinder
description: "Plan an effort too big for one agent session as a shared map of decision tickets on the issue tracker, then resolve one ticket per session until the route to the destination is clear. Use when a loose idea is wrapped in fog, when planning itself exceeds one session, or when work must survive across sessions and agents."
---

# Wayfinder

A loose idea arrives, too big for one agent session, wrapped in fog: the way from here to the destination is not visible yet. Wayfinding is about finding the way, not charging at the destination. This skill charts the effort as a **map** on the issue tracker, then works its **decision tickets** — questions whose resolution is a decision, not build slices to execute — one at a time until the route is clear: nothing left to decide before someone goes and does the thing.

The destination varies per effort, and naming it is the first act of charting because it shapes every ticket: a spec to hand off and iterate on, a set of decisions locked before build planning starts, or a change made in place, like a data-structure migration. The map is domain-agnostic — engineering work, course content, whatever fits the shape.

## Plan, don't do

Wayfinder is **planning** by default: each ticket resolves a decision, and the map is done when the way is clear. The urge to just do the work is usually the signal you have reached the edge of the map and it is time to hand off. An effort can override this in its **Notes**, carrying execution into the map itself; absent that, produce decisions, not deliverables.

## Refer by name

Every map ticket is an issue, so it has a **name**: its title. In everything a human reads — narration, the map's decisions-so-far — refer to it by name, never by a bare id, number, or slug. A wall of `#42, #43, #44` is illegible; names read at a glance. Ids and URLs do not vanish: the name wraps its link, and they ride inside the name, never stand in for it.

## The map

The map is a single issue on the repo's issue tracker, labelled `wayfinder:map` — the canonical artifact of the effort. Tickets are child issues of the map. The map is an **index, not a store**: it lists decisions made and points at the tickets that hold the detail; a decision lives in exactly one place, its ticket, so the map never restates it, only gists it with a link.

**Where the map, child tickets, blocking, and frontier queries physically live is tracker-specific.** The tracker should have been provided; if none was, default to a local markdown tracker (one file per issue in a directory under the repo, labels in frontmatter, blocking as `Blocked-by:` lines) and say so.

### Map body

The whole map at low resolution, loaded once per session. Open tickets are not listed: they are child issues, found by query.

```markdown
## Destination

<the end of the map: the spec, decision, or change this effort is finding
the way to. One or two lines; every session orients against this first.>

## Notes

<domain constraints; skills sessions should consult; standing preferences;
any override of "plan, don't do">

## Decisions so far

<!-- index: one line per closed ticket, enough to judge relevance;
     the ticket name wraps its link, then zoom into the ticket for detail -->

- <closed ticket title>: <one-line gist of the answer>

## Not yet specified

<!-- fog: in-scope questions not sharp enough to ticket yet;
     graduates to tickets as the frontier advances -->

## Out of scope

<!-- work consciously ruled out of this effort; closed, never graduates -->
```

### Tickets

Each ticket is a child issue of the map; its body is a question, sized so one agent session can resolve it:

```markdown
## Question

<the decision or investigation this ticket resolves>
```

Each ticket carries a `wayfinder:<type>` label (below). A session **claims** a ticket by assigning itself **first**, before any work: an open, unassigned ticket is unclaimed, so concurrent sessions skip it. Blocking uses the tracker's native dependency relationship when it has one — it renders the frontier visually, so a human sees what is takeable without opening the map; fall back to `Blocked-by:` lines only when it does not. A ticket is **unblocked** when every ticket blocking it is closed; the **frontier** is the open, unblocked, unclaimed children — the edge of the known. The answer is not part of the body; it is recorded on resolution. Assets created while resolving link to the ticket; never paste them in.

### Ticket types

Every ticket is either **HITL** (human in the loop, worked _with_ the human) or **AFK** (the agent drives it alone). A HITL ticket resolves only through live exchange; the agent never stands in for the human's side — answering your own grilling questions is the planning equivalent of fabricating evidence, and breaks the same gate as self-granted `AUTH:`.

- **Research** (AFK): reading documentation, third-party APIs, or local knowledge bases to surface a fact a decision waits on. Fan out per the delegation tier of [teamwork](../teamwork/SKILL.md): one scoped worker per ticket, findings back as the resolution comment.
- **Prototype** (HITL): a key "how should it look or behave" question, resolved by raising fidelity — a cheap, rough, concrete artifact to react to: an outline, a rough take, a stub, throwaway UI or logic. Link the artifact as an asset; the human's reaction is the resolution.
- **Grilling** (HITL): conversation with the human to pin down a decision — the default type whenever the open question is about intent, preference, or scope. Interview technique: [grilling](../grilling/SKILL.md); the word "frontier" travels badly between the two — wayfinder's frontier is the map's takeable tickets across sessions, grilling's is the open questions inside one session.
- **Task** (AFK): work that must happen so a decision can be made — provisioning access, moving data so its shape can be seen. This type does rather than decides, and earns its place only by unblocking a decision. Resolved when the work is done; the resolution records any facts later tickets depend on (credentials location, new URLs, row counts).

## Fog of war

The map is deliberately incomplete: don't chart what you can't yet see. Beyond the live tickets lies **fog**: decisions and investigations you can tell are coming but cannot pin down yet. Resolving a ticket clears fog ahead of it, graduating whatever is now specifiable into fresh tickets — one at a time, never in advance — until the way to the destination is clear and no tickets remain.

**Fog or ticket?** Test whether you can state the question sharply _now_, not whether you can answer it now. Sharp-but-blocked is a ticket; unstateable is fog. Don't pre-slice fog into ticket-sized pieces: one patch may graduate into several tickets, or none, once the frontier reaches it.

Fog only gathers **toward** the destination. Work beyond it is not fog but **out of scope**: it never graduates, and returns only if the destination is redrawn. When a ticket turns out to sit past the destination, close it and leave one line under **Out of scope** — the gist plus why — keeping it out of **Decisions so far**, which records the route actually walked.

## Invocation

Two modes. Either way, resolve at most **one** ticket per session — research fan-out is the exception. One session, one decision; the map carries the state, so no context has to.

### Chart the map

Invoked with a loose idea.

1. **Name the destination.** Grill the human until the destination is one or two lines — spec, decision, or change. The destination fixes scope, so it is settled first.
2. **Map the frontier, breadth-first.** Fan out across the whole space rather than deep on any one thread, surfacing open decisions and first steps takeable now. If this surfaces no fog — the way is already clear and the whole journey fits one session — there is no map to make: stop and ask the user how to proceed.
3. **Create the map** (label `wayfinder:map`): destination and notes filled in, decisions empty, fog sketched into **Not yet specified**.
4. **Create the tickets you can specify now** as child issues, then wire blocking edges in a second pass that sorts them into frontier vs blocked. Everything unstateable stays fog.
5. **Fire research fan-outs** for the research tickets just created, so findings land as resolutions while you stop.
6. **Stop.** Charting is one session's work; it hand-resolves nothing.

### Work through the map

Invoked with a map reference (URL, number, or file).

1. **Load the map** — the low-resolution body, not every ticket.
2. **Choose a ticket.** If the user named one, take it; otherwise take the first frontier ticket in order. **Claim it** by self-assigning before any work.
3. **Resolve it.** Zoom into any related closed ticket's detail on demand. When in doubt about what a decision needs, default to a grilling conversation with the human.
4. **Record the resolution**: resolution comment on the ticket, close it, append the one-line gist to **Decisions so far**.
5. **Update the map's edges**: create newly surfaced tickets, graduate fog the answer made specifiable (clearing each graduated patch from **Not yet specified** so it lives only in its ticket), rule out of scope anything the answer exposed as beyond the destination, and delete or rewire tickets the decision invalidated.
6. **Stop.** Other sessions may be working the map concurrently; trust the claim discipline, not the absence of others.

## Cross-references

- [teamwork](../teamwork/SKILL.md) the delegation tier fans research tickets out; its task ledger coordinates agents within one job, the map across sessions.
- [verification](../verification/SKILL.md) the evidence standard a task ticket owes before it may close.
- [craft](../craft/SKILL.md) decision gates (`INTENT:`, `AUTH:`) apply to what a resolution changes.
- [grilling](../grilling/SKILL.md) the interview technique behind a Grilling ticket: rounds and frontier within one session; the map is what persists across sessions.
