"""Build the submission .docx on the Apart template from report/draft.md (and the appendix files it includes).

    python tools/build_docx.py "../Copy of Apart Research hackathon submission template.docx"

Writes report/submission.docx. The template's title block keeps its look: the title, one author, "With Apart Research"
and the abstract box. Everything after the guidance box is replaced by the draft from "## 1. Introduction" on.
`<!-- include: file.md -->` lines in the draft pull an appendix file in (its own top heading dropped, others demoted).
Needs only the standard library.
"""

from __future__ import annotations

import os
import re
import struct
import sys
import zipfile
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = os.path.join(HERE, "report")
FONT = "Arial"  # the template's default font; its sample text used Old Standard TT, which reads poorly in body text
TEMPLATE_FONT = "Old Standard TT"
MONO = "Courier New"
TEXT_W = 9360  # 6.5 in in DXA
FIG_WIDTH_IN = {"fig1_remedy_ladder.png": 3.7, "fig2_cross_model.png": 3.8, "fig3_ratchet.png": 5.6,
                "figA1_adherence_dose.png": 6.0}
BULLET_NUM, ORDERED_ABSTRACT = 3, 5  # template numbering: numId 3 is "-" bullets, abstractNum 5 is "1."

rels: list[str] = []  # extra relationships for document.xml.rels
media: list[tuple[str, str]] = []  # (zip path, source path)
new_nums: list[int] = []
_ids = {"rel": 100, "num": 100, "pic": 1}


def rid(kind_xml: str) -> str:
    r = f"rId{_ids['rel']}"
    _ids["rel"] += 1
    rels.append(kind_xml.replace("{rid}", r))
    return r


# ---------- inline text ----------

TOKEN = re.compile(r"(`[^`]+`)|(\[[^\]]+\]\([^)\s]+\))|(https?://[^\s<>()]*[^\s<>().,;:])|(\\[*_#|\[\]`])|(\*\*)|(\*)")


def rpr(b=False, i=False, mono=False, sz=None, color=None, u=False) -> str:
    f = MONO if mono else FONT
    out = f'<w:rFonts w:ascii="{f}" w:cs="{f}" w:eastAsia="{f}" w:hAnsi="{f}"/>'
    if b:
        out += '<w:b w:val="1"/><w:bCs w:val="1"/>'
    if i:
        out += '<w:i w:val="1"/><w:iCs w:val="1"/>'
    if color:
        out += f'<w:color w:val="{color}"/>'
    if sz:
        out += f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
    if u:
        out += '<w:u w:val="single"/>'
    return f"<w:rPr>{out}</w:rPr>"


def run(text: str, **kw) -> str:
    return f'<w:r>{rpr(**kw)}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'


def link(text: str, url: str, **kw) -> str:
    r = rid('<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" '
            f'Target="{escape(url, {chr(34): "&quot;"})}" TargetMode="External"/>')
    kw = {**kw, "color": "1155CC", "u": True}
    return f'<w:hyperlink r:id="{r}">{run(text, **kw)}</w:hyperlink>'


def inline(text: str, sz=None, b=False, i=False, color=None) -> str:
    toks = []
    pos = 0
    for m in TOKEN.finditer(text):
        if m.start() > pos:
            toks.append(("t", text[pos:m.start()]))
        code, md_link, url, esc, s2, s1 = m.groups()
        if code:
            toks.append(("code", code[1:-1]))
        elif md_link:
            t, u = re.match(r"\[([^\]]+)\]\(([^)]+)\)", md_link).groups()
            toks.append(("link", t, u))
        elif url:
            toks.append(("link", url, url))
        elif esc:
            toks.append(("t", esc[1]))
        else:
            toks.append(("s2" if s2 else "s1", m.group(0)))
        pos = m.end()
    if pos < len(text):
        toks.append(("t", text[pos:]))
    for kind in ("s2", "s1"):  # an unpaired marker is literal text
        idx = [k for k, t in enumerate(toks) if t[0] == kind]
        if len(idx) % 2:
            toks[idx[-1]] = ("t", toks[idx[-1]][1])
    out, bold, ital = [], b, i
    for t in toks:
        if t[0] == "s2":
            bold = not bold
        elif t[0] == "s1":
            ital = not ital
        elif t[0] == "t":
            out.append(run(t[1], b=bold, i=ital, sz=sz, color=color))
        elif t[0] == "code":
            out.append(run(t[1], b=bold, i=ital, mono=True, sz=(sz or 22) - 3))
        else:
            out.append(link(t[1], t[2], b=bold, i=ital, sz=sz))
    return "".join(out)


# ---------- blocks ----------

def para(content: str, style=None, jc=None, ind=None, after=80, before=0, line=259, num=None, keep_next=False,
         shade=None, page_break=False) -> str:
    p = ""
    if style:
        p += f'<w:pStyle w:val="{style}"/>'
    if keep_next:
        p += '<w:keepNext w:val="1"/>'
    if page_break:
        p += '<w:pageBreakBefore w:val="1"/>'
    if num:
        p += f'<w:numPr><w:ilvl w:val="{num[1]}"/><w:numId w:val="{num[0]}"/></w:numPr>'
    if shade:
        p += f'<w:shd w:fill="{shade}" w:val="clear"/>'
    p += f'<w:spacing w:before="{before}" w:after="{after}" w:line="{line}" w:lineRule="auto"/>'
    if ind:
        p += "<w:ind " + " ".join(f'w:{k}="{v}"' for k, v in ind.items()) + "/>"
    if jc:
        p += f'<w:jc w:val="{jc}"/>'
    return f"<w:p><w:pPr>{p}</w:pPr>{content}</w:p>"


HEAD = {2: dict(style="Heading2", sz=28, before=280, after=80), 3: dict(style="Heading3", sz=24, before=180, after=60),
        4: dict(style="Heading4", sz=22, before=140, after=40)}


def heading(level: int, text: str, page_break=False) -> str:
    h = HEAD[min(max(level, 2), 4)]
    return para(inline(text, sz=h["sz"], b=True, color="000000"), style=h["style"], before=h["before"], after=h["after"], line=240,
                keep_next=True, page_break=page_break)


def table(rows: list[list[str]]) -> str:
    plain = lambda c: re.sub(r"[*`\\]", "", c)
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]
    # body cells set the width; a long header may wrap onto two lines
    weight = [min(max(max([len(plain(r[j])) for r in rows[1:]] + [0.55 * len(plain(rows[0][j]))]), 5), 48)
              for j in range(ncol)]
    widths = [int(TEXT_W * w / sum(weight)) for w in weight]
    widths[-1] = TEXT_W - sum(widths[:-1])
    border = "".join(f'<w:{s} w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
                     for s in ("top", "left", "bottom", "right", "insideH", "insideV"))
    out = (f'<w:tbl><w:tblPr><w:tblW w:w="{TEXT_W}" w:type="dxa"/><w:jc w:val="center"/><w:tblBorders>{border}</w:tblBorders>'
           '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:top w:w="20" w:type="dxa"/><w:left w:w="70" w:type="dxa"/>'
           '<w:bottom w:w="20" w:type="dxa"/><w:right w:w="70" w:type="dxa"/></w:tblCellMar></w:tblPr><w:tblGrid>'
           + "".join(f'<w:gridCol w:w="{w}"/>' for w in widths) + "</w:tblGrid>")
    for k, r in enumerate(rows):
        out += "<w:tr>" + ('<w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>' if k == 0 else "<w:trPr><w:cantSplit/></w:trPr>")
        for j, c in enumerate(r):
            shd = '<w:shd w:val="clear" w:color="auto" w:fill="F2F2F2"/>' if k == 0 else ""
            out += (f'<w:tc><w:tcPr><w:tcW w:w="{widths[j]}" w:type="dxa"/>{shd}</w:tcPr>'
                    + para(inline(c.strip(), sz=18, b=(k == 0)), after=0, line=240) + "</w:tc>")
        out += "</w:tr>"
    return out + "</w:tbl>" + para("", after=60, line=240)


def image(alt: str, src: str) -> str:
    path = os.path.join(REPORT, src)
    with open(path, "rb") as f:
        head = f.read(24)
    w_px, h_px = struct.unpack(">II", head[16:24])
    name = os.path.basename(src)
    cx = int(FIG_WIDTH_IN.get(name, 6.0) * 914400)
    cy = int(cx * h_px / w_px)
    media.append((f"word/media/{name}", path))
    r = rid('<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
            f'Target="media/{name}"/>')
    n = _ids["pic"]
    _ids["pic"] += 1
    drawing = (f'<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
               f'<wp:docPr id="{n}" name="Picture {n}" descr="{escape(alt)}"/><wp:cNvGraphicFramePr>'
               '<a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
               '</wp:cNvGraphicFramePr><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
               '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
               '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
               f'<pic:nvPicPr><pic:cNvPr id="{n}" name="{name}"/><pic:cNvPicPr/></pic:nvPicPr>'
               f'<pic:blipFill><a:blip r:embed="{r}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
               f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
               '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic>'
               '</wp:inline></w:drawing></w:r>')
    return para(drawing, jc="center", after=40, before=80, line=240, keep_next=True)


def code(lines: list[str]) -> str:
    runs = '<w:r><w:br/></w:r>'.join(run(l, mono=True, sz=16) for l in lines)
    return para(runs, shade="F3F3F3", ind={"left": 120, "right": 120}, after=120, line=228)


def expand_includes(md: str) -> str:
    def sub(m):
        txt = open(os.path.join(REPORT, m.group(1)), encoding="utf-8").read()
        out = []
        for line in txt.splitlines():
            if re.match(r"# ", line):
                continue  # the appendix letter heading is already in the draft
            h = re.match(r"(#{2,5}) (.*)", line)
            out.append(f"#### {h.group(2)}" if h else line)
        return "\n".join(out)
    md = re.sub(r"<!-- include: (\S+) -->\n\*[^\n]*\*\n", lambda m: sub(m) + "\n", md)
    return md


def body(md: str) -> str:
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    lines = md.splitlines()
    out, i = [], 0
    list_num = None  # numId of the open list (None if no list is open)
    para_buf: list[str] = []

    def flush():
        if para_buf:
            out.append(para(inline(" ".join(s.strip() for s in para_buf))))
            para_buf.clear()

    while i < len(lines):
        line = lines[i]
        li = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", line)
        if not line.strip():
            flush()
            i += 1
            continue
        if line.startswith("```"):
            flush()
            j = i + 1
            while not lines[j].startswith("```"):
                j += 1
            out.append(code(lines[i + 1:j]))
            list_num, i = None, j + 1
            continue
        h = re.match(r"^(#{1,6}) (.*)$", line)
        if h:
            flush()
            text = h.group(2)
            out.append(heading(len(h.group(1)), text, page_break=(text == "Appendix")))
            list_num, i = None, i + 1
            continue
        if line.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = lines[i].strip().strip("|").split("|")
                if not all(re.fullmatch(r"\s*:?-+:?\s*", c) for c in cells):
                    rows.append(cells)
                i += 1
            out.append(table(rows))
            list_num = None
            continue
        img = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", line)
        if img:
            flush()
            out.append(image(img.group(1), img.group(2)))
            list_num, i = None, i + 1
            continue
        if li:
            flush()
            level = min(len(li.group(1)) // 2, 1)
            ordered = li.group(2)[0].isdigit()
            if list_num is None or (level == 0 and ordered != (list_num != BULLET_NUM)):
                if ordered:
                    list_num = _ids["num"]
                    _ids["num"] += 1
                    new_nums.append(list_num)
                else:
                    list_num = BULLET_NUM
            text = li.group(3)
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r"^(\s*)([-*]|\d+\.)\s+|^[#|!]", lines[i]):
                text += " " + lines[i].strip()  # lazy continuation
                i += 1
            out.append(para(inline(text), num=(list_num, level), after=40,
                            ind={"left": 720 + 360 * level, "hanging": 360}))
            continue
        if line.startswith("  ") and list_num is not None:
            flush()
            out.append(para(inline(line.strip()), ind={"left": 720}))
            i += 1
            continue
        list_num = None
        para_buf.append(line)
        i += 1
    flush()
    return "".join(out)


# ---------- template surgery ----------

def top_level_spans(xml: str, start: int, end: int) -> list[tuple[int, int, str]]:
    spans, i = [], start
    while i < end:
        j = xml.find("<w:", i)
        if j < 0 or j >= end:
            break
        tag = re.match(r"<w:(\w+)", xml[j:]).group(1)
        if tag == "p":
            k = xml.index("</w:p>", j) + 6
        elif tag == "tbl":
            depth, k = 0, j
            for m in re.finditer(r"<w:tbl>|</w:tbl>", xml[j:]):
                depth += 1 if m.group(0) == "<w:tbl>" else -1
                if depth == 0:
                    k = j + m.end()
                    break
        elif tag == "sectPr":
            k = xml.index("</w:sectPr>", j) + 11
        else:
            raise ValueError(tag)
        spans.append((j, k, tag))
        i = k
    return spans


def title_block(tbl: str, title: str, subtitle: str, author: str, affil: str, abstract: str) -> str:
    tbl = tbl.replace("PROJECT TITLE", escape(title), 1)
    end_title = tbl.index("</w:p>", tbl.index(escape(title))) + 6
    sub = para(inline(subtitle, sz=20, i=True), jc="center", after=120, line=240)
    tbl = tbl[:end_title] + sub + tbl[end_title:]
    a = tbl.index("Author name 1")
    g0 = tbl.rfind("<w:tbl>", 0, a)
    g1 = tbl.index("</w:tbl>", tbl.index("Author name 6")) + len("</w:tbl>")
    who = (f'<w:r>{rpr()}<w:t xml:space="preserve">{escape(author)}</w:t><w:br w:type="textWrapping"/>'
           f'<w:t xml:space="preserve">{escape(affil)}</w:t></w:r>')
    tbl = tbl[:g0] + para(who, jc="center", after=200, line=240) + tbl[g1:]
    s = tbl.index("Summarize your project")
    box = tbl.rfind("<w:tbl>", 0, s)  # widen the abstract box from 4.9 in to 5.8 in, still centred
    tbl = (tbl[:box] + tbl[box:s].replace('w:w="7095.0"', 'w:w="8400.0"').replace('w:w="7095"', 'w:w="8400"')
           .replace('<w:tblInd w:w="780.0"', '<w:tblInd w:w="370.0"') + tbl[s:])
    s = tbl.index("Summarize your project")
    p0 = tbl.rfind("<w:p ", 0, s)
    p1 = tbl.index("</w:tc>", s)
    abs_p = para(inline(abstract), jc="both", after=120, line=240)
    return tbl[:p0] + abs_p + tbl[p1:]


def main(template: str, out_path: str):
    md = open(os.path.join(REPORT, "draft.md"), encoding="utf-8").read()
    title = re.search(r"^# (.*)$", md, flags=re.M).group(1)
    subtitle = re.search(r"^\*([^*].*[^*])\*$", md, flags=re.M).group(1)
    author, affil = re.search(r"^\*\*Author:\*\* (.*)$", md, flags=re.M).group(1).split(", ", 1)
    abstract = md.split("## Abstract", 1)[1].strip().split("\n\n", 1)[0].strip()
    main_md = expand_includes(md[md.index("## 1. Introduction"):])
    generated = body(main_md)

    zin = zipfile.ZipFile(template)
    files = {n: zin.read(n) for n in zin.namelist()}
    doc = files["word/document.xml"].decode("utf-8")
    b0 = doc.index("<w:body>") + len("<w:body>")
    b1 = doc.index("</w:body>")
    spans = top_level_spans(doc, b0, b1)
    (p0s, p0e, _), (t1s, t1e, _), (p2s, p2e, _) = spans[:3]
    sect = next(doc[s:e] for s, e, t in spans if t == "sectPr")
    new_body = (doc[p0s:p0e] + title_block(doc[t1s:t1e], title, subtitle, author, affil, abstract) + doc[p2s:p2e]
                + generated + sect)
    files["word/document.xml"] = (doc[:b0] + new_body + doc[b1:]).replace(TEMPLATE_FONT, FONT).encode("utf-8")
    for part in ("word/footnotes.xml", "word/styles.xml"):
        files[part] = files[part].decode("utf-8").replace(TEMPLATE_FONT, FONT).encode("utf-8")

    r = files["word/_rels/document.xml.rels"].decode("utf-8")
    files["word/_rels/document.xml.rels"] = r.replace("</Relationships>", "".join(rels) + "</Relationships>").encode("utf-8")
    num = files["word/numbering.xml"].decode("utf-8")
    extra = "".join(f'<w:num w:numId="{n}"><w:abstractNumId w:val="{ORDERED_ABSTRACT}"/>'
                    '<w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>' for n in new_nums)
    files["word/numbering.xml"] = num.replace("</w:numbering>", extra + "</w:numbering>").encode("utf-8")
    ct = files["[Content_Types].xml"].decode("utf-8")
    if 'Extension="png"' not in ct:
        ct = ct.replace("<Default ", '<Default ContentType="image/png" Extension="png"/><Default ', 1)
    files["[Content_Types].xml"] = ct.encode("utf-8")
    for zpath, src in media:
        files[zpath] = open(src, "rb").read()

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", files.pop("[Content_Types].xml"))
        for n, data in files.items():
            z.writestr(n, data)
    print(f"wrote {out_path}: {len(media)} figures, {sum('hyperlink' in x for x in rels)} links, {len(new_nums)} numbered lists")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else os.path.join(REPORT, "submission.docx"))
