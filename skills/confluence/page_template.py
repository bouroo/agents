#!/usr/bin/env python3
"""Generator: emit a Confluence storage-format endpoint page that matches the
hand-built example `adapter-mbf-ais - POST /api/v1/cart/get` (page 6082560274,
/wiki/x/EoGMagE) byte-for-byte in structure. See references/page-template.md.

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

def meta_table(spec):
    """3-col highlighted metadata table. spec['overview'] is the intro paragraph."""
    rows = meta_row("Overview", spec["overview"])
    md = spec["metadata"]
    rows += meta_row("Layer", md.get("layer", "Adapter Microservice"))
    rows += meta_row("Microservice", md.get("microservice", "adapter-mbf-ais"))
    rows += meta_row("Authentication Level", md.get("auth",
              "- (no caller-auth check in v1; trust boundary at network/gateway edge)"))
    rows += meta_row("Dependency overview", "")  # section divider label
    rows += meta_row("Inbound component", spec.get("inbound", "bff-mobile-mbf (and other internal callers)"))
    rows += meta_row("Outbound component", spec["outbound"])
    rows += meta_row("Expose to Mobile", md.get("expose_to_mobile", "N"))
    rows += meta_row("Access token required", md.get("access_token_required", "N"))
    rows += meta_row("Language", md.get("language", "Golang"))
    rows += meta_row("JIRA", md.get("jira", ""))
    return _table(rows)

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

FIELD_HDR = ["Field Name", "Datatype", "Mandatory  M/C/O", "Description", "Remark"]
STATUS_HDR = ["HTTP Code", "Custom Status Code", "Status Description", "Scenario"]
MAP_HDR = ["Input / Output", "Target", "Source", "Mapping Logic", "Remark"]

def build_page(spec) -> str:
    """spec keys: title, overview, inbound, outbound, metadata{}, changelog[[Date,By,Desc,Status]],
    sequence(str), logic[list], request_fields[[5]], sample_request(str, lang default json),
    response_fields[[5]], sample_200(str), sample_err(str), status_rows[[4]],
    upstream_name(str), mapping_rows[[5]], svg_filename(opt)."""
    parts = []
    parts.append(f"<h1>{esc(spec['title'])}</h1>")
    parts.append(meta_table(spec))
    # Change logs
    parts.append("<h2>Change logs</h2>")
    parts.append(data_table(["Date", "Update By", "Description", "Status"], spec["changelog"]))
    # TOC (optional macro)
    parts.append("<h2>Table of Contents</h2>")
    parts.append('<ac:structured-macro ac:name="toc"><ac:parameter ac:name="maxLevel">3</ac:parameter></ac:structured-macro>')
    # Sequence diagram: rendered macro + raw source code block (wide, language none)
    parts.append("<h2>Sequence diagram</h2>")
    svg = spec.get("svg_filename") or (spec["title"].split("/")[-1].strip().lower().replace(" ", "-").replace("/", "-") + ".svg")
    parts.append(plantuml_macro(spec["sequence"], svg))
    parts.append(code_macro(spec["sequence"], language="none", wide=True))
    # Logic
    parts.append("<h2>Logic</h2>")
    items = "".join(f"<li>{_p(s)}</li>" for s in spec["logic"])
    parts.append(f"<ol>{items}</ol>")
    # Request
    parts.append("<h2>Request</h2>")
    parts.append("<h3>Request Body</h3>")
    parts.append(data_table(FIELD_HDR, spec["request_fields"]))
    parts.append("<h3>Sample request</h3>")
    parts.append(code_macro(spec["sample_request"], language=spec.get("sample_request_lang", "json"), wide=True))
    # Response
    parts.append("<h2>Response</h2>")
    parts.append("<h3>Response Body</h3>")
    parts.append(data_table(FIELD_HDR, spec["response_fields"]))
    parts.append("<h3>Sample response</h3>")
    parts.append(_table(hdr_table(["HTTP 200 - Success"])))
    parts.append(code_macro(spec["sample_200"], language="json", wide=True))
    if spec.get("sample_err"):
        parts.append(_table(hdr_table(["HTTP 409 - Business error"])))
        parts.append(code_macro(spec["sample_err"], language="json", wide=False))
    # Status Code
    parts.append("<h2>Status Code</h2>")
    parts.append(data_table(STATUS_HDR, spec["status_rows"]))
    # Field to Field Mapping
    parts.append("<h2>Field to Field Mapping</h2>")
    parts.append(f"<h3>When calling the upstream {esc(spec['upstream_name'])}</h3>")
    parts.append(data_table(MAP_HDR, spec["mapping_rows"]))
    return "\n".join(parts)


# ---- demo / self-test ----
_DEMO = {
    "title": "adapter-mbf-ais - POST /api/v1/cart/get",
    "overview": "Adapter API to fetch an AIS cart by id, loan application id, or selection token. "
                "Wraps the upstream GET /v1/carts/{id}?type=<type> call in the standard envelope.",
    "inbound": "bff-mobile-mbf (and other internal callers)",
    "outbound": "External Service: AIS Cart API (via AIS ESB, OAuth2 client_credentials) -- cart-api.md §2",
    "metadata": {"jira": ""},
    "changelog": [["2026-08-04", "Kawin.V", "Initial -- matches dev implementation", "Initial"]],
    "sequence": "@startuml\nparticipant Caller\nparticipant \"adapter-mbf-ais\" as Adapter\n"
                "participant \"AIS Cart API\" as AIS\nCaller -> Adapter: POST /api/v1/cart/get\\n(content.type, content.id)\n"
                "Adapter -> AIS: GET /v1/carts/{id}?type=<type>\nAIS -> Adapter: 200, cart\n"
                "Adapter -> Caller: HTTP 200, statusCd 0000\n@enduml",
    "logic": ["Validate content.type (id|loan-app-id|selection-token) and content.id present (else HTTP 422 AIS4001).",
              "Obtain AIS OAuth2 token via TokenManager (else HTTP 500 AIS5003).",
              "GET {cart.baseURL}/v1/carts/{id}?type=<type>; return upstream body verbatim (resultCode 20000 → 0000)."],
    "request_fields": [["content.type", "Enum", "M", "Which identifier content.id is.", "id / loan-app-id / selection-token."],
                       ["content.id", "String", "M", "Cart UUID / loan app id / selection token.", ""]],
    "sample_request": '{\n  "headerReq": { "reqID": "req-1" },\n  "content": { "type": "id", "id": "50d80b8b-…" }\n}',
    "response_fields": [["content.resultCode", "String", "M", "Upstream result code.", "20000 on success."],
                        ["content.data", "Object", "M", "Full cart object, verbatim.", ""]],
    "sample_200": '{\n  "headerResp": { "statusCd": "0000", "statusDesc": "success" },\n  "content": { "resultCode": "20000", "data": { "id": "50d80b8b-…" } }\n}',
    "sample_err": '{\n  "headerResp": { "statusCd": "AIS4091", "statusDesc": "upstream cart business error: Not found" }\n}',
    "status_rows": [["200", "0000", "success", "Cart found; resultCode 20000."],
                    ["422", "AIS4001", "<field> is required", "type|id missing/invalid."],
                    ["409", "AIS4091", "upstream cart business error: …", "Non-20000 resultCode."]],
    "upstream_name": "AIS Cart API",
    "mapping_rows": [["I", "{id} (URL path)", "req.content.id", "", ""],
                     ["I", "type (query)", "req.content.type", "", ""],
                     ["O", "content (body)", "upstream response", "Verbatim, no re-shaping.", ""]],
}

if __name__ == "__main__" and __import__("sys").argv[-1] == "demo":
    print(build_page(_DEMO))
