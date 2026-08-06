# Mermaid: storage form, the newline rule, and proof

The short doctrine lives in [SKILL.md](../SKILL.md); this file is the macro form, the syntax trap that is the mirror image of PlantUML's, and the prove-it-renders loop.

## Why a macro, not a fence

A ` ```mermaid ` fence authored as `content_format: "markdown"` renders as **literal source text** -- Confluence's markdown path has no mermaid renderer. Use the native **storage format** `mermaid` macro (set `content_format: "storage"`), exactly as PlantUML uses `plantumlcloud`. The macro body is the **raw, uncompressed** mermaid source in a CDATA `plain-text-body` -- there is no `plantumlcloud`-style compression to get right.

```xml
<ac:structured-macro ac:name="mermaid" ac:schema-version="1">
  <ac:plain-text-body><![CDATA[flowchart TD
    Client([Client]) --> API[adapter API]
    API --> Upstream[(Upstream API)]
    Upstream --> DB[(DB)]]]></ac:plain-text-body>
</ac:structured-macro>
```

The `mermaid_macro(body)` helper in [storage-format.md](./storage-format.md) wraps a body in this template and splits any literal `]]>` in the source. The md->storage converter emits it for a ` ```mermaid ` fence.

## The newline rule (opposite of PlantUML)

Mermaid parses one statement per **real newline**. A sequence/flow diagram whose statements are joined onto one line is a syntax error or renders as one node. This is the **mirror image** of the PlantUML sequence-message trap ([plantuml.md](./plantuml.md) `Error line N`):

```
# BROKEN -- one line; mermaid sees a single malformed statement
sequenceDiagram\nClient->>API: GET /cart\nAPI->>Upstream: lookup\nAPI-->>Client: 200
```

```
# CORRECT -- one statement per real newline
sequenceDiagram
  Client->>API: GET /cart
  API->>Upstream: lookup
  Upstream-->>API: row
  API-->>Client: 200
```

**Rule:** never `.replace("\n", "\\n")` (or otherwise join) a mermaid body before publishing. Keep real newlines. This is the single most common mermaid rendering failure on a wiki page.

## Proof (uncompressed, so trivial)

PlantUML proof needs a decode of the compressed `data` param. Mermaid needs none -- the source is stored verbatim in the CDATA body:

1. Publish the page (`content_format: "storage"`, body contains the macro above).
2. `confluence_get_page` the page storage body back.
3. Assert the returned `mermaid` macro body is **byte-identical** to what you wrote (real newlines preserved), and that the statement count is unchanged.

`body.view` is NOT proof -- it returns a macro render stub, not the rendered diagram. As with PlantUML, only the decoded/round-tripped storage body is.

## Confirm the macro name on the instance

`ac:name="mermaid"` is the **native Cloud** mermaid macro. A third-party "Mermaid Diagrams for Confluence" app installs a different macro name (commonly `mermaid-cloud` or a vendor key). On first use against an instance, publish a one-statement probe, fetch the storage body back, and read the macro name the instance stored -- then use that name. If the instance stores an unknown macro, the page renders the raw source; that probe failure is the signal, same as a PlantUML plugin that returns a trivial SVG.

## Notes

- Mermaid renders server-side in the macro on Cloud; there is no client `mermaid.js` dependency to satisfy on the page.
- Theme/direction keywords (`flowchart TD`, `sequenceDiagram`, `classDiagram`) are stable across the renderer versions Cloud ships; omit exotic theme directives that a server plugin may not support.
