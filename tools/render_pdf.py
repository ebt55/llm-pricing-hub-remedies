"""Render report/draft.md to report/draft.pdf (a page-count and layout preview; the submission uses the Apart template).

    python tools/render_pdf.py            # needs the `markdown` package (pip install markdown) and Microsoft Edge

Styled close to the Apart Google Docs template: Letter size, 1-inch margins, 11pt Arial. Prints the page count of the
main text (up to References) and of the whole file.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

import markdown

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = os.path.join(HERE, "report")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
CSS = """
@page { size: Letter; margin: 1in; }
body { font-family: Arial, Helvetica, sans-serif; font-size: 11pt; line-height: 1.35; color: #111; }
h1 { font-size: 17pt; margin: 0 0 4pt; } h2 { font-size: 13pt; margin: 14pt 0 4pt; } h3 { font-size: 11.5pt; margin: 10pt 0 3pt; }
p, li { margin: 3pt 0; } ul, ol { margin: 2pt 0 4pt 18pt; padding: 0; }
table { border-collapse: collapse; margin: 6pt 0; font-size: 9.5pt; } th, td { border: 1px solid #bbb; padding: 2pt 5pt; }
img { width: 100%; display: block; margin: 6pt auto 0; } img[alt="Figure 1"], img[alt="Figure 2"] { width: 62%; } img[alt="Figure 3"] { width: 86%; } code { font-size: 9.5pt; }
"""


def render(md_path: str, pdf_path: str) -> int:
    with open(md_path, encoding="utf-8") as f:
        text = f.read()
    body = markdown.markdown(text, extensions=["tables"])
    html_path = pdf_path.replace(".pdf", ".html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>")
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf_path}", "file:///" + html_path.replace(os.sep, "/")],
                   check=True, capture_output=True)
    with open(pdf_path, "rb") as f:
        return len(re.findall(rb"/Type\s*/Page[^s]", f.read()))


if __name__ == "__main__":
    src = os.path.join(REPORT, "draft.md")
    with open(src, encoding="utf-8") as f:
        full = f.read()
    main = full[:full.index("## References")]
    tmp = os.path.join(REPORT, "_main_only.md")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(main)
    n_main = render(tmp, os.path.join(REPORT, "_main_only.pdf"))
    n_all = render(src, os.path.join(REPORT, "draft.pdf"))
    for x in ("_main_only.md", "_main_only.html", "_main_only.pdf"):
        os.remove(os.path.join(REPORT, x))
    print(f"main text (title to Limitations): {n_main} pages; whole draft incl. references and appendix list: {n_all} pages")
    sys.exit(0)
