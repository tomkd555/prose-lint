# /// script
# requires-python = ">=3.10"
# dependencies = ["python-pptx>=1.0"]
# ///
"""pptx_text.py - write the text of a PowerPoint deck to Markdown for the linters.

Each slide becomes a `## Slide <n>` section. The title is a `### ` heading,
every other paragraph of a text box or a grouped shape is a `- ` item, a table
is a Markdown table whose first row is its header row, and the speaker notes
follow under `### Notes` as plain paragraphs. A soft line break inside a
paragraph starts a new line with the same prefix, so line numbers agree across
the linters; inside a table cell, paragraphs and soft breaks join with `<br>`.
A picture leaves a `<!-- picture -->` line on its slide. Charts and SmartArt
keep their text in parts python-pptx does not read; each leaves a
`<!-- chart or SmartArt -->` line, and stderr names it with its slide.

With --flat, every paragraph of a table cell is a `- ` item instead, for
textlint: its sentence rules (max-ten, no-doubled-joshi) skip the cells of a
Markdown table, and the comment lines are left out.

Usage:
    uv run pptx_text.py [--flat] <deck.pptx> <out.md>

Prints `ja` or `en` on stdout: `ja` when kana and kanji make up over 10% of the
deck's non-whitespace text. The hiragana test of the skill's Step 2 misroutes a
deck of noun-phrase bullets, which hold little hiragana.
"""
from __future__ import annotations

import re
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE, PP_PLACEHOLDER
from pptx.shapes.picture import Picture

TITLES = {PP_PLACEHOLDER.TITLE, PP_PLACEHOLDER.CENTER_TITLE, PP_PLACEHOLDER.VERTICAL_TITLE}


def parts(text: str) -> list[str]:
    """Split a paragraph at its soft line breaks, each part with its spaces collapsed."""
    return [" ".join(t.split()) for t in text.split("\v")]


def shape_lines(shape, skipped: list[str], flat: bool = False):
    """Yield (is_title, text) for every paragraph a shape holds, groups included.

    A table is one Markdown table with is_title None, or with flat one item per
    paragraph of each cell. A picture, a chart and SmartArt leave a comment line.
    """
    try:
        kind = shape.shape_type
    except NotImplementedError:  # python-pptx names no type for a p:sp without geometry
        kind = None
    if kind == MSO_SHAPE_TYPE.GROUP:
        for child in shape.shapes:
            yield from shape_lines(child, skipped, flat)
        return
    if getattr(shape, "has_table", False) and shape.has_table and flat:
        for row in shape.table.rows:
            for cell in row.cells:
                for p in cell.text_frame.paragraphs:
                    for t in parts(p.text):
                        yield False, t
        return
    if getattr(shape, "has_table", False) and shape.has_table:
        rows = []
        for row in shape.table.rows:
            cells = ["" if c.is_spanned else "<br>".join(t for p in c.text_frame.paragraphs for t in parts(p.text) if t)
                     for c in row.cells]
            rows.append("| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |")
        rows.insert(1, "|" + " --- |" * len(shape.table.columns))
        yield None, "\n".join(rows)
        return
    if getattr(shape, "has_text_frame", False) and shape.has_text_frame:
        title = shape.is_placeholder and shape.placeholder_format.type in TITLES
        for p in shape.text_frame.paragraphs:
            for t in parts(p.text):
                yield title, t
        return
    # The comment lines stay out of the flat extract: one between two items splits
    # a list, and textlint's list rules then read two lists.
    if isinstance(shape, Picture):
        yield None, "" if flat else "<!-- picture -->"
    elif getattr(shape, "has_chart", False) and shape.has_chart or kind == MSO_SHAPE_TYPE.IGX_GRAPHIC:
        skipped.append(shape.name)
        yield None, "" if flat else "<!-- chart or SmartArt -->"


def main() -> int:
    flat = "--flat" in sys.argv[1:]
    args = [a for a in sys.argv[1:] if a != "--flat"]
    if len(args) != 2:
        print(__doc__, file=sys.stderr)
        return 1
    out, skipped = [], []
    for no, slide in enumerate(Presentation(args[0]).slides, 1):
        out.append(f"## Slide {no}\n")
        start = len(skipped)
        for shape in slide.shapes:
            for title, text in shape_lines(shape, skipped, flat):
                if text:
                    out.append(f"{text}\n" if title is None else f"### {text}\n" if title else f"- {text}\n")
        skipped[start:] = [f"slide {no} {name}" for name in skipped[start:]]
        if slide.has_notes_slide:
            notes = [t for p in slide.notes_slide.notes_text_frame.paragraphs for t in parts(p.text)]
            if any(notes):
                out.append("### Notes\n")
                out.extend(f"{n}\n" for n in notes if n)
    md = "\n".join(out)
    with open(args[1], "w", encoding="utf-8", newline="\n") as f:
        f.write(md)
    if skipped:
        print(f"pptx_text: text not read from {len(skipped)} chart or SmartArt shapes: {', '.join(skipped)}", file=sys.stderr)
    body = re.sub(r"\s|^#+ Slide \d+$|^\|( --- \|)+$", "", md, flags=re.M)
    cjk = len(re.findall(r"[぀-ヿ一-鿿]", body))
    print("ja" if cjk * 10 > len(body) else "en")
    return 0


if __name__ == "__main__":
    sys.exit(main())
