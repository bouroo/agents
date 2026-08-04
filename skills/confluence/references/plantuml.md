# PlantUML: compression, decode, and the `\n` trap

The short doctrine lives in [SKILL.md](../SKILL.md); this file is the verified algorithm (encode + decode) and the syntax regression.

## The compression algorithm (verified)

Reverse-engineered from a hand-built page's stored `data` param: it decodes/inflates cleanly and a re-encode round-trips. The `plantumlcloud` macro's `data` param is produced by:

1. **`%`-encode** the PlantUML source, keeping RFC-3986 unreserved `- . _ ~` and `/` literal (Python `urllib.parse.quote(text, safe="/-._~")`). Note `/` stays literal; space → `%20`.
2. **Raw DEFLATE** the UTF-8 bytes -- `zlib.compressobj(9, zlib.DEFLATED, -15)` (negative wbits = no zlib header/footer).
3. **Base64** with the standard `A-Za-z0-9+/` alphabet, **strip trailing `=` padding**.

Pure-stdlib encoder:

```python
import urllib.parse as up, zlib

_B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
_B64_MAP = {i: c for i, c in enumerate(_B64)}

def _encode64(b: bytes) -> str:
    out = []
    for i in range(0, len(b), 3):
        b1 = b[i]; b2 = b[i+1] if i+1 < len(b) else 0; b3 = b[i+2] if i+2 < len(b) else 0
        out.append(_B64_MAP[b1 >> 2])
        out.append(_B64_MAP[((b1 & 0x3) << 4) | (b2 >> 4)])
        out.append(_B64_MAP[((b2 & 0xF) << 2) | (b3 >> 6)])
        out.append(_B64_MAP[b3 & 0x3F])
    s = "".join(out)
    pad = (-len(b)) % 3
    return s[: len(s) - pad] if pad else s          # drop '=' padding

def compress_plantuml(text: str) -> str:
    data = up.quote(text, safe="/-._~").encode("utf-8")
    cz = zlib.compressobj(9, zlib.DEFLATED, -15)
    return _encode64(cz.compress(data) + cz.flush())
```

Pure-stdlib **decoder** (inverse -- use to verify/inspect a published diagram):

```python
import urllib.parse as up, zlib

_B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
_DM = {c: i for i, c in enumerate(_B64)}

def decompress_plantuml(data: str) -> str:
    s = data.rstrip("=")
    out = bytearray()
    for i in range(0, len(s), 4):
        g = [_DM[c] for c in s[i:i+4]]
        while len(g) < 4: g.append(0)
        out.append((g[0] << 2) | (g[1] >> 4))
        out.append(((g[1] & 0xF) << 4) | (g[2] >> 2))
        out.append(((g[2] & 0x3) << 6) | g[3])
    raw = bytes(out[: len(s) * 6 // 8])
    return up.unquote(zlib.decompressobj(-15).decompress(raw).decode("utf-8"))
```

`plantuml_macro` wraps the compressed string:

```python
def plantuml_macro(source: str, filename: str) -> str:
    return (f'<ac:structured-macro ac:name="plantumlcloud">'
            f'<ac:parameter ac:name="filename">{filename}</ac:parameter>'
            f'<ac:parameter ac:name="data">{compress_plantuml(source)}</ac:parameter>'
            f'<ac:parameter ac:name="compressed">true</ac:parameter>'
            f'<ac:parameter ac:name="revision">1</ac:parameter>'
            f'</ac:structured-macro>')
```

## Validate with the real engine (PROVE, never trust `body.view`)

`body.view` returns a JS stub for `plantumlcloud`; it cannot tell you whether the diagram renders. Validate the decoded source.

**⚠ `-check` is unreliable in this environment** (Java 25 + plantuml.jar): it prints
`Error line 1 in file: …` / exits non-zero even for diagrams that render
perfectly -- confirmed against already-published pages that render correctly on
Confluence. **Do not trust `-check`.** The authoritative proof is to **render to
SVG and inspect the text labels**:

```bash
# one-time: engine + Graphviz (component/package diagrams need `dot`)
[ -f /tmp/plantuml.jar ] || curl -sL "https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar" -o /tmp/plantuml.jar
brew install graphviz        # only if diagrams use component/package/activity

# 1. decode the page's `data` (or use your own source) -> /tmp/d.puml
python3 -c "from page_template import compress_plantuml; import zlib,urllib.parse as up; \
 d=open('/tmp/data.txt').read(); B='A-Za-z0-9+/'; ..."   # (use decompress_plantuml from this file)

# 2. render to SVG -- THIS is the proof
java -jar /tmp/plantuml.jar -tsvg /tmp/d.puml -o /tmp/out    # exit 0 + non-trivial .svg = renders
```

Then verify the SVG is a real diagram, not a placeholder:

```python
svg = open("/tmp/out/d.svg").read()
labels = [t for t in re.findall(r"<text[^>]*>(.*?)</text>", svg, re.S) if t.strip()]
ok = svg.count("<text") > 0 and not any(m in svg for m in ["DescriptionError","errorV2","Syntax"])
# expect your participant/actor names among `labels`
```

A missing/trivial SVG, or `viewBox` ~`0 0 0 0`, or an error-marker string, means the
diagram is broken -- fix before pushing. A real SVG with your labels present is proof.

## The `\n` syntax trap (the regression)

A sequence-diagram message that spans a **real newline** is a syntax error (`Error line N`). This happens when a converter helpfully turns a literal `\n` (backslash-n) inside a message into a real newline:

```
# BROKEN -- line 2 is a syntax error
Caller -> Adapter: POST /api/v1/cart/get
(headerReq.reqID, headerReq.id)
```

PlantUML renders the **two-character escape `\n`** as a display line break when it stays inside a **single source line**:

```
# CORRECT -- one line; \n is a visual break
Caller -> Adapter: POST /api/v1/cart/get\n(headerReq.reqID, headerReq.id)
```

**Rule:** never `.replace("\\n", "\n")` a plantuml body before compressing. Keep `\n` literal inside the message line. Validate by rendering to SVG after any transformation (see above -- `-check` is unreliable).

## Notes

- `!theme plain` and other theme directives are optional and may differ by server/plugin version; omit if a diagram fails to render on the plugin but passes locally.
- This compression is the **mxgraph Confluence PlantUML plugin** format (addon `com.mxgraph.confluence.plugins.plantuml`), NOT the public `plantuml.com/server` text-encoding (which uses the `-_` alphabet). They are different encodings -- don't mix them.
