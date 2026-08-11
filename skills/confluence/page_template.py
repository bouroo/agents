#!/usr/bin/env python3
"""Generator: emit a Confluence storage-format endpoint page in the canonical
endpoint-page layout: 3-col metadata table, H1 Change Log / TOC / Sequence
Diagram (plantumlcloud) / Request / Response / Field-To-Field Mapping. See
references/page-template.md.

USAGE
    from page_template import build_page, compress_plantuml
    xml = build_page(spec)            # spec is the dict shape below
    open("page.xml","w").write(xml)   # then: content_format=storage, content_file=page.xml

CLI (smoke test / demo):  python3 page_template.py demo > /tmp/demo.xml
"""
import zlib, urllib.parse as up, html as _h

# ---- PlantUML compression (verified; see references/plantuml.md) ----
_B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
_B64_MAP = {i: c for i, c in enumerate(_B64)}

def compress_plantuml(text: str) -> str:
    data = up.quote(text, safe="/-._~").encode("utf-8")
    cz = zlib.compressobj(9, zlib.DEFLATED, -15)
    raw = cz.compress(data) + cz.flush()
    out = []
    for i in range(0, len(raw), 3):
        a, b, c = raw[i], raw[i + 1] if i + 1 < len(raw) else 0, raw[i + 2] if i + 2 < len(raw) else 0
        out += [_B64_MAP[a >> 2], _B64_MAP[((a & 3) << 4) | (b >> 4)],
                _B64_MAP[((b & 15) << 2) | (c >> 6)], _B64_MAP[c & 63]]
    s = "".join(out)
    pad = (-len(raw)) % 3
    return s[: len(s) - pad] if pad else s   # strip '=' padding

# ---- markup helpers (match the example exactly) ----
def esc(s): return _h.escape(str(s), quote=False)
def inline(s):
    s = re.sub(r"`([^`]+)`", lambda m: "<code>" + esc(m.group(1)) + "</code>", str(s)) if False else esc(s)
    return s

import re
def inline(s):  # noqa: E302  (override above)
    out, last = [], 0
    for m in re.finditer(r"`([^`]+)`", str(s)):
        out.append(esc(s[last:m.start()])); out.append("<code>" + esc(m.group(1)) + "</code>"); last = m.end()
    out.append(esc(s[last:]))
    return "".join(out)

def _p(x): return f"<p>{inline(x)}</p>"

def _table(rows_html): return f'<table data-table-width="1761" data-layout="default"><tbody>{rows_html}</tbody></table>'

def hdr_table(headers):
    return "<tr>" + "".join(f'<th><p><strong>{esc(h)}</strong></p></th>' for h in headers) + "</tr>"

def data_table(headers, rows):
    """headers: list[str]; rows: list[list[cell]]. Cells are inline-rendered."""
    out = hdr_table(headers)
    for r in rows:
        out += "<tr>" + "".join(f"<td>{_p(c)}</td>" for c in r) + "</tr>"
    return _table(out)

def meta_row(label, value, highlight=True):
    label_cell = f'<td data-highlight-colour="#f4f5f7" colspan="2">{_p(label)}</td>' if highlight else f'<td colspan="2">{_p(label)}</td>'
    return f"<tr>{label_cell}<td>{_p(value)}</td></tr>"


def _meta_table(rows_html):
    """Metadata table: centered layout, auto-sized (no fixed colgroup/width)."""
    return f'<table data-layout="center"><tbody>{rows_html}</tbody></table>'


def _meta_overview_row(label, value):
    """Overview row: highlighted label cell (td) + value."""
    return (f'<tr><td colspan="2" data-highlight-colour="#f4f5f7"><p><strong>{esc(label)}</strong></p></td>'
            f'<td><p>{inline(value)}</p></td></tr>')


def _meta_th_row(label, value):
    """Metadata row: bold label in <th colspan="2"> + value in <td><p>."""
    return (f'<tr><th colspan="2"><p><strong>{esc(label)}</strong></p></th>'
            f'<td><p>{inline(value)}</p></td></tr>')


def expand_macro(title, inner_html, breakout_width=None):
    """Collapsible 'expand' macro (rich-text body holds a code block, etc.)."""
    params = [f'<ac:parameter ac:name="title">{esc(title)}</ac:parameter>']
    if breakout_width:
        params.append(f'<ac:parameter ac:name="breakoutWidth">{breakout_width}</ac:parameter>')
    return ('<ac:structured-macro ac:name="expand" ac:schema-version="1">' + "".join(params) +
            f'<ac:rich-text-body>{inner_html}</ac:rich-text-body></ac:structured-macro>')

def meta_table(spec):
    """3-col metadata table matching the canonical endpoint-page layout: centered,
    fixed colgroup, bold <th colspan="2"> labels, <p>-wrapped values."""
    md = spec["metadata"]
    rows = _meta_overview_row("Overview", spec["overview"])
    rows += _meta_th_row("Layer", md.get("layer", "adapter"))
    rows += _meta_th_row("Microservice", md.get("microservice", "adapter"))
    rows += _meta_th_row("Authentication Level", md.get("auth", ""))
    rows += _meta_th_row("Dependency overview", "")  # section divider label
    rows += _meta_th_row("Inbound component", spec.get("inbound", ""))
    rows += _meta_th_row("Outbound component", spec["outbound"])
    rows += _meta_th_row("Expose to Mobile", md.get("expose_to_mobile", "N"))
    rows += _meta_th_row("Access token required", md.get("access_token_required", "N"))
    rows += _meta_th_row("Language", md.get("language", "Golang"))
    rows += _meta_th_row("JIRA", md.get("jira", ""))
    return _meta_table(rows)

def code_macro(body, language="none", wide=False):
    safe = body.replace("]]>", "]]]]><![CDATA[>")
    params = [f'<ac:parameter ac:name="language">{esc(language)}</ac:parameter>']
    if wide:
        params += ['<ac:parameter ac:name="breakoutMode">wide</ac:parameter>',
                   '<ac:parameter ac:name="breakoutWidth">4000</ac:parameter>',
                   '<ac:parameter ac:name="wrap">true</ac:parameter>']
    return ('<ac:structured-macro ac:name="code">' + "".join(params) +
            f'<ac:plain-text-body><![CDATA[{safe}]]></ac:plain-text-body></ac:structured-macro>')

def plantuml_macro(source, filename):
    return ('<ac:structured-macro ac:name="plantumlcloud">'
            f'<ac:parameter ac:name="filename">{esc(filename)}</ac:parameter>'
            f'<ac:parameter ac:name="data">{compress_plantuml(source)}</ac:parameter>'
            '<ac:parameter ac:name="compressed">true</ac:parameter>'
            '<ac:parameter ac:name="revision">1</ac:parameter></ac:structured-macro>')

FIELD_HDR = ["Field Name", "Data Type", "Mandatory (M) /Optional (O) /Conditional (C)", "Description", "Remark"]
STATUS_HDR = ["HTTP Code", "Custom Status Code", "Scenario", "Status Description"]
MAP_HDR = ["Input/ Output", "Field Name", "Type", "Mandatory (M) /Optional (O) /Conditional (C)", "Source Field", "Remarks"]

def build_page(spec) -> str:
    """spec keys: title, overview, inbound, outbound, metadata{}, changelog[[Date,By,Desc,Status]],
    sequence(str), logic[list], request_fields[[5]], sample_request(str, lang default json),
    response_fields[[5]], sample_200(str), sample_err(str), status_rows[[4]],
    upstream_name(str), mapping_rows[[5]], svg_filename(opt)."""
    parts = []
    # Canonical layout: no leading H1 title (page title carries it);
    # top-level sections are H1. See references/page-template.md.
    parts.append(meta_table(spec))
    # Change Log
    parts.append("<h1>Change Log</h1>")
    parts.append(data_table(["Date", "Updated By", "Description", "Status"], spec["changelog"]))
    # Table of Contents
    parts.append("<h1>Table of Contents</h1>")
    parts.append('<ac:structured-macro ac:name="toc"><ac:parameter ac:name="minLevel">1</ac:parameter><ac:parameter ac:name="maxLevel">3</ac:parameter></ac:structured-macro>')
    # Sequence diagram: rendered plantumlcloud macro + raw source collapsed in an expand
    parts.append("<h1>Sequence Diagram</h1>")
    svg = spec.get("svg_filename") or (spec["title"].split("/")[-1].strip().lower().replace(" ", "-").replace("/", "-") + ".svg")
    parts.append(plantuml_macro(spec["sequence"], svg))
    parts.append(expand_macro("Raw sequence diagram source", code_macro(spec["sequence"], language="none", wide=False)))
    # Logic
    if spec.get("logic"):
        parts.append("<h1>Logic</h1>")
        items = "".join(f"<li>{_p(s)}</li>" for s in spec["logic"])
        parts.append(f"<ol>{items}</ol>")
    # Request
    parts.append("<h1>Request</h1>")
    if spec.get("request_header_fields"):
        parts.append("<h2>Request Header Schema</h2>")
        parts.append(data_table(FIELD_HDR, spec["request_header_fields"]))
    parts.append("<h2>Request Body Schema</h2>")
    parts.append(data_table(FIELD_HDR, spec["request_fields"]))
    parts.append("<h2>Example Request</h2>")
    parts.append(code_macro(spec["sample_request"], language=spec.get("sample_request_lang", "json"), wide=True))
    # Response
    parts.append("<h1>Response</h1>")
    parts.append("<h2>Custom HTTP Response Code</h2>")
    parts.append(data_table(STATUS_HDR, spec["status_rows"]))
    parts.append("<h2>Response Schema</h2>")
    parts.append(data_table(FIELD_HDR, spec["response_fields"]))
    parts.append("<h2>Example Response</h2>")
    parts.append(_table(hdr_table(["Case HTTP 200 Success"])))
    parts.append(code_macro(spec["sample_200"], language="json", wide=True))
    if spec.get("sample_400"):
        parts.append(_table(hdr_table(["Case HTTP 400 Bad Request"])))
        parts.append(code_macro(spec["sample_400"], language="json", wide=False))
    if spec.get("sample_err"):
        parts.append(_table(hdr_table([spec.get("error_case_title", "Case HTTP 409 Business Error")])))
        parts.append(code_macro(spec["sample_err"], language="json", wide=False))
    if spec.get("sample_500"):
        parts.append(_table(hdr_table(["Case HTTP 500 System Error"])))
        parts.append(code_macro(spec["sample_500"], language="json", wide=False))
    # Field to Field Mapping
    parts.append("<h1>Field-To-Field Mapping</h1>")
    parts.append(f'<h2>Field Mapping when calling to {esc(spec["upstream_name"])}</h2>')
    parts.append(data_table(MAP_HDR, spec["mapping_rows"]))
    return "\n".join(parts)


# ---- demo / self-test (generic placeholder content; no real service data) ----
_DEMO = {
    "title": "POST - /v1/example-resource/get",
    "overview": "Example adapter endpoint: fetch a resource by id from an upstream service and "
                "return it in the standard envelope. Illustrative only.",
    "inbound": "internal callers (BFF / orchestrator)",
    "outbound": "External Service: Example Upstream API",
    "metadata": {"jira": ""},
    "changelog": [["2026-08-04", "Author", "Initial template example.", "Initial"]],
    "sequence": "@startuml\nTitle adapter API - example - POST /v1/example-resource/get\nhide footbox\n"
                "actor Requester as requester #85E3FF\nbox \"adapter MS\" #DFFDFF\n"
                "entity \"adapter\" as adapter #85E3FF\nendbox\nbox \"Upstream\" #F7E5EC\n"
                "entity \"Upstream\" as upstream #FB9EBB\nendbox\n"
                "requester -> adapter : POST /v1/example-resource/get (content.id)\n"
                "adapter -> upstream : GET /resources/{id}\nupstream --> adapter : 200 resource\n"
                "adapter --> requester : HTTP 200 statusCd 0000\n@enduml",
    "logic": ["Validate content.id present (else HTTP 400 bad request).",
              "Fetch {resource.baseURL}/resources/{id} via the configured HTTP client.",
              "Map the upstream response into the standard envelope (statusCd 0000 on success)."],
    "request_fields": [["content.id", "String", "M", "Resource identifier.", ""]],
    "sample_request": '{\n  "headerReq": { "reqID": "req-1" },\n  "content": { "id": "ex-001" }\n}',
    "response_fields": [["content.resultCode", "String", "M", "Upstream result code.", "0000 on success."],
                        ["content.data", "Object", "M", "Resource object, verbatim.", ""]],
    "sample_200": '{\n  "headerResp": { "statusCd": "0000", "statusDesc": "success" },\n  "content": { "resultCode": "0000", "data": { "id": "ex-001" } }\n}',
    "sample_err": '{\n  "headerResp": { "statusCd": "E4091", "statusDesc": "upstream business error: not found" }\n}',
    "status_rows": [["200", "0000", "success", "Resource found."],
                    ["400", "0001", "bad request", "content.id missing/invalid."],
                    ["409", "E4091", "business error", "Non-success upstream result."]],
    "upstream_name": "Example Upstream API",
    "mapping_rows": [["I", "{id} (URL path)", "String", "M", "req.content.id", "Direct."],
                     ["O", "content (body)", "Object", "M", "upstream response", "Verbatim, no re-shaping.", ""]],
}

if __name__ == "__main__" and __import__("sys").argv[-1] == "demo":
    print(build_page(_DEMO))
