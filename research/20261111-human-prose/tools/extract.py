# /// script
# requires-python = ">=3.10"
# dependencies = ["beautifulsoup4>=4.12", "lxml>=5"]
# ///
"""extract.py - the body prose of a saved HTML page as Markdown.

    uv run extract.py <page.html> <out.md> [--select <css>] [--drop <css>]

Headings become # lines, <p> a paragraph, <li> a `- ` item, a table one
`<!-- table -->` line. The text is the page's own: nothing is retyped.
"""
import argparse
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

DROP = "script,style,nav,header,footer,noscript,form,aside,figure,iframe,sup"
BLOCK = {"p", "div", "li", "ul", "ol", "dl", "dt", "dd", "table", "blockquote", "section", "article",
         "h1", "h2", "h3", "h4", "h5", "h6", "br", "tr", "td", "th", "pre", "hr"}


def text_of(node) -> str:
    return re.sub(r"[ \t\r\n　\xa0]+", " ", node.get_text()).strip()


def walk(node, out):
    for child in node.children:
        if isinstance(child, NavigableString):
            t = re.sub(r"\s+", " ", str(child)).strip()
            if t:
                out.append(("p", t))
            continue
        if not isinstance(child, Tag):
            continue
        name = child.name.lower()
        if re.fullmatch(r"h[1-6]", name):
            t = text_of(child)
            if t:
                out.append(("h" + name[1], t))
        elif name == "table":
            out.append(("table", ""))
        elif name in ("ul", "ol"):
            for li in child.find_all("li", recursive=False):
                sub = li.find(["ul", "ol"])
                if sub:
                    sub.extract()
                t = text_of(li)
                if t:
                    out.append(("li", t))
                if sub:
                    walk(BeautifulSoup(f"<div>{sub}</div>", "lxml").div, out)
        elif name == "p" or (name in ("dd", "dt", "blockquote") and not child.find(list(BLOCK - {"br"}))):
            # a <br> inside a paragraph is a line break of the same paragraph on these sites
            parts = re.split(r"<br\s*/?>\s*(?:(?:<br\s*/?>\s*)+|(?=(?:&nbsp;|\u3000|\xa0)))", child.decode_contents())
            for part in parts:
                t = text_of(BeautifulSoup(part, "lxml"))
                if t:
                    out.append(("p", t))
        elif child.find(list(BLOCK - {"br"})):
            walk(child, out)
        else:
            parts = re.split(r"<br\s*/?>\s*(?:(?:<br\s*/?>\s*)+|(?=(?:&nbsp;|\u3000|\xa0)))", child.decode_contents())
            for part in parts:
                t = text_of(BeautifulSoup(part, "lxml"))
                if t:
                    out.append(("p", t))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("out")
    ap.add_argument("--select", default="")
    ap.add_argument("--drop", default="")
    a = ap.parse_args()
    raw = Path(a.page).read_bytes()
    m = re.search(rb"charset=[\"']?([\w-]+)", raw[:4000], re.I)
    enc = m.group(1).decode() if m else "utf-8"
    if enc.lower() in ("shift_jis", "sjis", "x-sjis"):
        enc = "cp932"
    soup = BeautifulSoup(raw.decode(enc, "replace"), "lxml")
    for sel in (DROP + ("," + a.drop if a.drop else "")).split(","):
        for n in soup.select(sel.strip()):
            n.decompose()
    if a.select:
        roots = soup.select(a.select)
    else:
        # the smallest element that holds 80 % of the page's sentence ends
        total = soup.body.get_text().count("。")
        best = soup.body
        for el in soup.body.find_all(["div", "main", "article", "section", "td"]):
            t = el.get_text()
            if t.count("。") >= 0.8 * total and len(t) < len(best.get_text()):
                best = el
        roots = [best]
    if not roots:
        print(f"no match for {a.select}", file=sys.stderr)
        return 1
    out = []
    for r in roots:
        walk(r, out)
    lines, prev = [], None
    for kind, t in out:
        if kind.startswith("h"):
            lines += ["", "#" * int(kind[1]) + " " + t, ""]
        elif kind == "li":
            if prev != "li":
                lines.append("")
            lines.append("- " + t)
        elif kind == "table":
            lines += ["", "<!-- table -->", ""]
        elif "。" in t:
            lines += ["", t]  # a line with no full stop is a label, a caption or navigation
        else:
            continue
        prev = kind
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip() + "\n"
    Path(a.out).write_text(text, encoding="utf-8")
    body = re.sub(r"\s", "", text)
    print(f"{a.out}: {len(body)} chars, {len(re.findall('[。．]', text))} sentence ends")
    return 0


if __name__ == "__main__":
    sys.exit(main())
