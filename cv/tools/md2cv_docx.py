#!/usr/bin/env python3
"""Render a CV markdown file to a neutral, unbranded .docx.

Purpose-built for the CV in this folder. Parses only the constructs that file
uses, so the markdown stays the single source of truth and the docx is
regenerated rather than hand-edited.

Design is deliberately sober: single column, no photo, no sidebar, no
competency ratings, one restrained accent used only on section headings.
Carries no employer branding of any kind.

Usage: python3 md2cv_docx.py <input.md> <output.docx>
"""

import re
import sys
import zipfile
from datetime import datetime, timezone

ACCENT = "1F3864"   # dark navy, section headings
BODY = "1A1A1A"     # near black, body text
MUTED = "595959"    # mid grey, meta lines
RULE = "BFBFBF"     # light grey, heading rules

BODY_FONT = "Calibri"
HEAD_FONT = "Cambria"

# ---------------------------------------------------------------- xml helpers


def esc(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def runs_from(text):
    """Split inline **bold** into (text, bold) pairs."""
    out = []
    for i, chunk in enumerate(re.split(r"\*\*", text)):
        if chunk:
            out.append((chunk, i % 2 == 1))
    return out


def run_xml(text, bold, size, color, font=BODY_FONT, italic=False):
    props = [f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:cs="{font}"/>']
    if bold:
        props.append("<w:b/>")
    if italic:
        props.append("<w:i/>")
    props.append(f'<w:color w:val="{color}"/>')
    props.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    return (
        f"<w:r><w:rPr>{''.join(props)}</w:rPr>"
        f'<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'
    )


def para(runs, before=0, after=80, style=None, indent=None,
         numbered=False, rule=False, keep_next=False, line=228):
    # CT_PPr enforces child order: pStyle, keepNext, keepLines, numPr, pBdr,
    # spacing, ind. Emitting out of order fails XSD validation.
    props = []
    if style:
        props.append(f'<w:pStyle w:val="{style}"/>')
    if keep_next:
        props.append("<w:keepNext/><w:keepLines/>")
    if numbered:
        props.append('<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>')
    if rule:
        props.append(
            '<w:pBdr><w:bottom w:val="single" w:sz="4" w:space="4" '
            f'w:color="{RULE}"/></w:pBdr>'
        )
    props.append(
        f'<w:spacing w:before="{before}" w:after="{after}" '
        f'w:line="{line}" w:lineRule="auto"/>'
    )
    if indent:
        props.append(f'<w:ind w:left="{indent}" w:hanging="180"/>')
    pr = f"<w:pPr>{''.join(props)}</w:pPr>"
    return f"<w:p>{pr}{''.join(runs)}</w:p>"


# ------------------------------------------------------------------- parsing


def parse(md_text):
    """Return a list of (kind, payload) blocks."""
    lines = md_text.split("\n")
    blocks = []
    i = 0
    seen_name = False
    table = None

    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        i += 1

        if not line:
            continue

        # markdown table
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) or c == "" for c in cells):
                continue  # separator or empty header row
            if table is None:
                table = []
                blocks.append(("table", table))
            table.append(cells)
            continue
        table = None

        if line.startswith("# "):
            blocks.append(("name", line[2:].strip()))
            seen_name = True
            continue

        if line.startswith("## "):
            blocks.append(("h2", line[3:].strip()))
            continue

        if line.startswith("### "):
            blocks.append(("role", line[4:].strip()))
            continue

        if line.startswith("- "):
            blocks.append(("bullet", line[2:].strip()))
            continue

        if line.startswith("---"):
            continue

        # the bolded title line straight after the name, then the contact line
        if seen_name and len(blocks) == 1 and line.startswith("**"):
            blocks.append(("subtitle", line.strip("*").strip()))
            continue
        if len(blocks) == 2 and blocks[1][0] == "subtitle":
            blocks.append(("contact", line))
            continue

        # employer line directly under a role heading
        if blocks and blocks[-1][0] == "role" and line.startswith("**"):
            blocks.append(("meta", re.sub(r"\*\*", "", line)))
            continue

        # "**Label.** body" competency paragraph
        m = re.match(r"^\*\*(.+?)\*\*\s*(.*)$", line)
        if m and m.group(2):
            blocks.append(("kv", (m.group(1), m.group(2))))
            continue

        blocks.append(("para", line))

    return blocks


# ------------------------------------------------------------------ document


def build_body(blocks):
    out = []
    for kind, payload in blocks:
        if kind == "name":
            out.append(para(
                [run_xml(payload, True, 36, BODY, HEAD_FONT)],
                after=0, line=228))

        elif kind == "subtitle":
            out.append(para(
                [run_xml(payload, False, 22, ACCENT, HEAD_FONT)],
                before=40, after=40))

        elif kind == "contact":
            out.append(para(
                [run_xml(payload, False, 16, MUTED)],
                after=150))

        elif kind == "h2":
            out.append(para(
                [run_xml(payload.upper(), True, 18, ACCENT, HEAD_FONT)],
                before=170, after=70, rule=True, keep_next=True))

        elif kind == "role":
            out.append(para(
                [run_xml(payload, True, 20, BODY, HEAD_FONT)],
                before=130, after=0, keep_next=True))

        elif kind == "meta":
            out.append(para(
                [run_xml(payload, False, 16, MUTED)],
                after=80, keep_next=True))

        elif kind == "bullet":
            runs = [run_xml(t, b, 18, BODY) for t, b in runs_from(payload)]
            out.append(para(runs, after=40, numbered=True, indent=284))

        elif kind == "kv":
            label, rest = payload
            runs = [run_xml(label, True, 18, BODY)]
            runs += [run_xml(t, b, 18, BODY) for t, b in runs_from(" " + rest)]
            out.append(para(runs, after=50))

        elif kind == "para":
            runs = [run_xml(t, b, 18, BODY) for t, b in runs_from(payload)]
            out.append(para(runs, after=70))

        elif kind == "table":
            out.append(build_table(payload))

    return "".join(out)


def build_table(rows):
    cells_xml = []
    for row in rows:
        left = row[0] if len(row) > 0 else ""
        right = row[1] if len(row) > 1 else ""
        tcs = []
        for width, text, bold_default in ((2100, left, True), (7400, right, False)):
            runs = [
                run_xml(t, b or (bold_default and "**" not in text), 18, BODY)
                for t, b in runs_from(text)
            ] or [run_xml("", False, 18, BODY)]
            tcs.append(
                f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>'
                # CT_TcMar child order: top, left, bottom, right.
                '<w:tcMar>'
                '<w:top w:w="40" w:type="dxa"/><w:left w:w="0" w:type="dxa"/>'
                '<w:bottom w:w="40" w:type="dxa"/><w:right w:w="140" w:type="dxa"/>'
                '</w:tcMar></w:tcPr>'
                + para(runs, after=40, line=228)
                + "</w:tc>"
            )
        cells_xml.append(f"<w:tr>{''.join(tcs)}</w:tr>")

    return (
        "<w:tbl><w:tblPr>"
        '<w:tblW w:w="9500" w:type="dxa"/>'
        "<w:tblBorders>"
        + "".join(
            f'<w:{e} w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            for e in ("top", "left", "bottom", "right", "insideH", "insideV")
        )
        + "</w:tblBorders><w:tblLayout w:type="
        '"fixed"/></w:tblPr>'
        '<w:tblGrid><w:gridCol w:w="2100"/><w:gridCol w:w="7400"/></w:tblGrid>'
        + "".join(cells_xml)
        + "</w:tbl>"
    )


SECT_PR = (
    "<w:sectPr>"
    '<w:pgSz w:w="11906" w:h="16838"/>'
    '<w:pgMar w:top="907" w:right="907" w:bottom="907" w:left="907" '
    'w:header="0" w:footer="0" w:gutter="0"/>'
    "</w:sectPr>"
)

DOCUMENT = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    "<w:body>{body}{sect}</w:body></w:document>"
)

STYLES = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    "<w:docDefaults><w:rPrDefault><w:rPr>"
    f'<w:rFonts w:ascii="{BODY_FONT}" w:hAnsi="{BODY_FONT}" w:cs="{BODY_FONT}"/>'
    f'<w:color w:val="{BODY}"/><w:sz w:val="18"/><w:szCs w:val="18"/>'
    "</w:rPr></w:rPrDefault>"
    "<w:pPrDefault><w:pPr>"
    '<w:spacing w:after="80" w:line="228" w:lineRule="auto"/>'
    "</w:pPr></w:pPrDefault></w:docDefaults>"
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
    '<w:name w:val="Normal"/><w:qFormat/></w:style>'
    '<w:style w:type="numbering" w:default="1" w:styleId="NoList">'
    '<w:name w:val="No List"/></w:style>'
    "</w:styles>"
)

NUMBERING = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:abstractNum w:abstractNumId="0">'
    '<w:multiLevelType w:val="hybridMultilevel"/>'
    '<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/>'
    '<w:lvlText w:val="&#8211;"/><w:lvlJc w:val="left"/>'
    '<w:pPr><w:ind w:left="284" w:hanging="180"/></w:pPr>'
    f'<w:rPr><w:rFonts w:ascii="{BODY_FONT}" w:hAnsi="{BODY_FONT}"/>'
    f'<w:color w:val="{MUTED}"/></w:rPr></w:lvl>'
    "</w:abstractNum>"
    '<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>'
    "</w:numbering>"
)

CONTENT_TYPES = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
    '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
    '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
    '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
    "</Types>"
)

ROOT_RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
    '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
    "</Relationships>"
)

DOC_RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'
    "</Relationships>"
)

APP = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
    'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
    "<Application>Microsoft Office Word</Application>"
    "</Properties>"
)


def core_xml(title):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        f"<dc:title>{esc(title)}</dc:title>"
        f"<dc:creator>Gilles Mourgues</dc:creator>"
        f'<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>'
        f'<dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>'
        "</cp:coreProperties>"
    )


def main():
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding="utf-8") as fh:
        blocks = parse(fh.read())

    title = next((p for k, p in blocks if k == "name"), "CV")
    document = DOCUMENT.format(body=build_body(blocks), sect=SECT_PR)

    parts = {
        "[Content_Types].xml": CONTENT_TYPES,
        "_rels/.rels": ROOT_RELS,
        "word/document.xml": document,
        "word/styles.xml": STYLES,
        "word/numbering.xml": NUMBERING,
        "word/_rels/document.xml.rels": DOC_RELS,
        "docProps/core.xml": core_xml(title),
        "docProps/app.xml": APP,
    }

    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in parts.items():
            zf.writestr(name, data)

    print(f"wrote {dst} ({len(blocks)} blocks)")


if __name__ == "__main__":
    main()
