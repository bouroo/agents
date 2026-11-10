# Page updates: change logs and round markers

> Load on demand from [confluence](../SKILL.md) or [page-template](page-template.md): the change-log table, the `#changeN` round-marker discipline, the baseline diff, and the bidirectional integrity gate. Read it when a published endpoint page is being updated rather than authored for the first time.

## Change logs + round markers (page updates)
[changelog]

An update must let a reader see the delta without opening version history: a baseline
diff, then in-place `#changeN` markers, with one Change logs table per page.

### Baseline diff first

`confluence_get_page_history(page_id, version=N, convert_to_markdown=false)` returns
the full stored body of any prior version (the tool defaults `convert_to_markdown=true`
- always pass `false` for storage work; its `space` field returns "Unknown", a tool
quirk, ignore it). `confluence_get_page_diff(from_version, to_version)` answers "what
did this field look like at v5" directly — prefer it over fetching and parsing a whole
version. Walk backwards until the version's timestamp precedes the current effort's
start date; that version is the pre-change baseline.

### N is the round, not the field

- The page numbers its change rounds 1, 2, 3 … and keeps counting across publishes. A
  page with 13 recorded rounds publishes its 14th as `#change14`, and **every** marker
  that round adds in the body says `14`. Writing `#change1` on a later round is the
  defect the round-number check rejects.
- Count the earlier round rows in Change logs first: a `Continued from …` row and an
  `Initiate specification` row are not rounds. Use that count + 1.
- Put the marker in the **Field Name** cell of every row the round adds or edits, and
  at the start of any note it adds. Never mark a row the round left untouched.
- **Delete the previous round's markers** as part of the sync: a marker records that
  *this* round touched the row, not that the field is special.
- Write the marker **outside** any code span — `#change14` then the field, never
  `` `#change14` ``: markdown escapes the highlight span and the page shows raw
  `<span>` markup. The build step colours each marker per N; write plain `#change14`.
- A new version shows **current state only**: delete every struck-through row or word
  (a removed field is removed, not struck through) and every old marker.

### Change logs table (`## Change logs`, page top)

Columns exactly `Date | Update By | Description | Status`:

| **Date** | **Update By** | **Description** | **Status** |
| --- | --- | --- | --- |
| YYYY-MM-DD | @Full Name | **#change14 — <short title>**<br>what changed | |

- `Date` = the edit date; `Update By` = `@Full Name`, which needs that name's
  `accountId` in the spec's `people` map to render as a mention (a name without one
  stays plain text — omit rather than invent an id).
- New API: one row, `Initiate specification`. New version of an existing page: row 1 is
  `Continued from [<old page title>](<old page url>) — earlier changes are recorded on
  that page`, then one `**#changeN — <short title>**` row per round, `<br>` for line
  breaks.
- Revising a draft that is not yet published: add a row and bump every marker to it.

### Integrity gate (add to the publish proof)

Every `#changeN` used in the body needs a row in Change logs, and every marker a
Change logs row declares must appear in the body. A dangling ref either direction is a
publish blocker, same tier as a failed `GATE OK`.

