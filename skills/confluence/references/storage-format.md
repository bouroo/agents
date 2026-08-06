# Storage format: macros, conversion, validation

The short doctrine lives in [SKILL.md](../SKILL.md); this file is the macro templates, a markdown→storage converter, and the validate-before-publish loop.

## Why not markdown

Markdown pages (`content_format: "markdown"`) render fenced code blocks as plain `<pre class="highlight"><code class="language-…">` -- no code panel, no real highlighting -- and PlantUML fences as **literal `@startuml…@enduml` text** that never renders. Hand-built pages use **native storage format** so the macros render:

- `<ac:structured-macro ac:name="code">` → a syntax-highlighted code panel.
- `<ac:structured-macro ac:name="plantumlcloud">` → a server-side rendered diagram (see [plantuml.md](./plantuml.md)).

Set `content_format: "storage"` on create/update.

## Macro templates

**Code block** (use `language: none` for plain text):

```xml
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">bash</ac:parameter>
  <ac:plain-text-body><![CDATA[curl -X POST http://localhost:1323/api/v1/cart/get]]></ac:plain-text-body>
</ac:structured-macro>
```

If the body contains `]]>`, split the CDATA: `]]></ac:plain-text-body><ac:plain-text-body><![CDATA[>` -- simpler: `body.replace("]]>", "]]]]><![CDATA[>")`.

**PlantUML diagram** (`data` = compressed source per [plantuml.md](./plantuml.md)):

```xml
<ac:structured-macro ac:name="plantumlcloud">
  <ac:parameter ac:name="filename">diagram-name.svg</ac:parameter>
  <ac:parameter ac:name="data">{COMPRESSED}</ac:parameter>
  <ac:parameter ac:name="compressed">true</ac:parameter>
  <ac:parameter ac:name="revision">1</ac:parameter>
</ac:structured-macro>
```

**Mermaid diagram** (raw source in a plain-text body -- no compression; see [mermaid.md](./mermaid.md)):

```xml
<ac:structured-macro ac:name="mermaid" ac:schema-version="1">
  <ac:plain-text-body><![CDATA[flowchart TD
    Client([Client]) --> API[adapter API]
    API --> Upstream[(Upstream API)]
    Upstream --> DB[(DB)]]]></ac:plain-text-body>
</ac:structured-macro>
```

The macro name is the native Cloud mermaid macro. A third-party "Mermaid for Confluence" app installs a different macro name (`mermaid-cloud`, etc.) -- confirm the name against the instance on first use (see [mermaid.md](./mermaid.md)). Mermaid source needs **real newlines** between statements (the opposite of PlantUML sequence messages), so never join its lines.

**Page link** (links to another page by exact title):

```xml
<ac:link>
  <ri:page ri:content-title="adapter-mbf-ais - POST /api/v1/cart/get"/>
  <ac:plain-text-link-body><![CDATA[POST /api/v1/cart/get]]></ac:plain-text-link-body>
</ac:link>
```

**Children macro** (auto-list child pages -- keep on a landing page):

```xml
<ac:structured-macro ac:name="children" ac:schema-version="2" data-layout="default">
  <ac:parameter ac:name="allChildren">true</ac:parameter>
</ac:structured-macro>
```

## Headings / tables / lists (storage XHTML)

- `<h1>`…`<h6>` for headings (escape inline content).
- Tables: `<table><tbody><tr><th>…</th></tr><tr><td>…</td></tr>…</tbody></table>`.
- `<ol>`/`<ul>` + `<li>`; `<p>` for paragraphs; `<br/>` for hard breaks.
- Inline code: `<code>…</code>`; escape `&`/`<`/`>`.
- Every table row must have the same cell count as its header, or Confluence misrenders -- validate (see below).

## Markdown → storage converter (Python, stdlib only)

A converter that turns fenced code blocks into `code` macros, PlantUML fences into `plantumlcloud` macros (using `compress_plantuml` from [plantuml.md](./plantuml.md)), Mermaid fences into `mermaid` macros (see [mermaid.md](./mermaid.md)), and markdown tables/headings/lists into storage XHTML. (This block uses
`~~~` fences because its regex matches ```` ``` ````, which would close a
` ``` ` fence early.)

~~~python
import re, urllib.parse, zlib

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def inline(s):
    s = re.sub(r"`([^`]+)`", lambda m: "<code>"+esc(m.group(1))+"</code>", s)
    return re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)

def code_macro(body, lang="none"):
    safe = body.replace("]]>", "]]]]><![CDATA[>")
    return (f'<ac:structured-macro ac:name="code">'
            f'<ac:parameter ac:name="language">{esc(lang)}</ac:parameter>'
            f'<ac:plain-text-body><![CDATA[{safe}]]></ac:plain-text-body>'
            f'</ac:structured-macro>')

def mermaid_macro(body):
    safe = body.replace("]]>", "]]]]><![CDATA[>")   # no compression -- source stored raw
    return ('<ac:structured-macro ac:name="mermaid" ac:schema-version="1">'
            f'<ac:plain-text-body><![CDATA[{safe}]]></ac:plain-text-body>'
            '</ac:structured-macro>')

def convert(md, slug, compress_plantuml):
    out, lines, i, n = [], md.split("\n"), 0, len(md.split("\n"))
    while i < n:
        line = lines[i]
        m = re.match(r"^```(\w*)\s*$", line)            # fenced block
        if m:
            lang = m.group(1) or "none"; body, i = [], i+1
            while i < n and not re.match(r"^```\s*$", lines[i]):
                body.append(lines[i]); i += 1
            i += 1
            body = "\n".join(body)
            if lang == "plantuml":
                out.append(plantuml_macro(body, f"{slug}.svg", compress_plantuml))  # see plantuml.md
            elif lang == "mermaid":
                out.append(mermaid_macro(body))                                    # see mermaid.md
            else:
                out.append(code_macro(body, lang))
            out.append(""); continue
        if line.startswith("|") and i+1 < n and re.match(r"^\|[- :|]+\|$", lines[i+1]):  # table
            tbl = []
            while i < n and lines[i].startswith("|"): tbl.append(lines[i]); i += 1
            out.append(table_to_xhtml(tbl)); out.append(""); continue
        hm = re.match(r"^(#{1,6})\s+(.*)$", line)       # heading
        if hm: out.append(f"<h{len(hm.group(1))}>{inline(hm.group(2))}</h{len(hm.group(1))}>"); i += 1; continue
        if re.match(r"^\d+\.\s+", line):                # ordered list
            items = []
            while i < n and re.match(r"^\d+\.\s+", lines[i]):
                items.append("<li>"+inline(re.sub(r"^\d+\.\s+","",lines[i]))+"</li>"); i += 1
            out.append("<ol>"+"".join(items)+"</ol>"); out.append(""); continue
        if line.strip() == "": i += 1; continue
        out.append("<p>"+inline(line)+"</p>"); i += 1
    return "\n".join(out)

def table_to_xhtml(md_lines):
    rows = []
    for idx, line in enumerate(md_lines):
        s = line.strip()
        if s.startswith("|"): s = s[1:]
        if s.endswith("|"): s = s[:-1]
        cells = [c.strip() for c in s.split("|")]
        if idx == 1 and all(set(c) <= set("-: ") for c in cells): continue   # separator
        rows.append(cells)
    if not rows: return ""
    h = "<table><tbody><tr>" + "".join(f"<th>{inline(c)}</th>" for c in rows[0]) + "</tr>"
    for r in rows[1:]: h += "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
    return h + "</tbody></table>"
~~~

`plantuml_macro(body, filename, compress_plantuml)` wraps `compress_plantuml(body)` in the macro template above. **Do not** `.replace("\\n","\n")` the plantuml body -- see the trap in [plantuml.md](./plantuml.md).

## Validate before publishing

1. **Table alignment** (cheap, every page): every row's cell count must equal the header's.
2. **PlantUML** (see plantuml.md): decode the `data` param → write `.puml` → `java -jar plantuml.jar -check file.puml` (exit 0). Component/package diagrams also need Graphviz (`brew install graphviz`).
3. **Mermaid** (see mermaid.md): source is uncompressed CDATA, so proof is a byte-identical round-trip of the `mermaid` macro body after fetch -- no decode step. Confirm the macro name the instance stores matches what you wrote.
4. **Round-trip after publish**: fetch the page storage body, re-read each diagram, confirm it equals what you intended. `body.view` is NOT proof (it returns a macro JS stub).
