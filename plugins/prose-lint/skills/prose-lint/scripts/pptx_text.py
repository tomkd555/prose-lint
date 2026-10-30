# /// script
# requires-python = ">=3.10"
# dependencies = ["python-pptx>=1.0"]
# ///
"""pptx_text.py - write the text of a PowerPoint deck to Markdown for the linters.

Each slide becomes a `## Slide <n>` section. The title is a `### ` heading,
every other paragraph of a text box, a grouped shape or a table cell is a `- `
item, and the speaker notes follow under `### Notes` as plain paragraphs. A
soft line break inside a paragraph starts a new line with the same prefix, so
line numbers agree across the linters. Charts and SmartArt keep their text in
parts python-pptx does not read; they are counted and named on stderr.

Usage:
    uv run pptx_text.py <deck.pptx> <out.md>

Prints `ja` or `en` on stdout: `ja` when kana and kanji make up over 10% of the
deck's non-whitespace text. The hiragana test of the skill's Step 2 misroutes a
deck of noun-phrase bullets, which hold little hiragana.
"""
from __future__ import annotations

import re
import sys

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE, PP_PLACEHOLDER

TITLES = {PP_PLACEHOLDER.TITLE, PP_PLACEHOLDER.CENTER_TITLE, PP_PLACEHOLDER.VERTICAL_TITLE}


def parts(text: str) -> list[str]:
    """Split a paragraph at its soft line breaks, each part with its spaces collapsed."""
    return [" ".join(t.split()) for t in text.split("\v")]


def shape_lines(shape, skipped: list[str]):
    """Yield (is_title, text) for every paragraph a shape holds, groups and tables included."""
    if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
        for child in shape.shapes:
            yield from shape_lines(child, skipped)
        return
    if getattr(shape, "has_table", False) and shape.has_table:
        for row in shape.table.rows:
            for cell in row.cells:
                for p in cell.text_frame.paragraphs:
                    for t in parts(p.text):
                        yield False, t
        return
    if getattr(shape, "has_text_frame", False) and shape.has_text_frame:
        title = shape.is_placeholder and shape.placeholder_format.type in TITLES
        for p in shape.text_frame.paragraphs:
            for t in parts(p.text):
                yield title, t
        return
    if getattr(shape, "has_chart", False) and shape.has_chart or shape.shape_type == MSO_SHAPE_TYPE.IGX_GRAPHIC:
        skipped.append(shape.name)


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 1
    out, skipped = [], []
    for no, slide in enumerate(Presentation(sys.argv[1]).slides, 1):
        out.append(f"## Slide {no}\n")
        for shape in slide.shapes:
            for title, text in shape_lines(shape, skipped):
                if text:
                    out.append(f"### {text}\n" if title else f"- {text}\n")
        if slide.has_notes_slide:
            notes = [t for p in slide.notes_slide.notes_text_frame.paragraphs for t in parts(p.text)]
            if any(notes):
                out.append("### Notes\n")
                out.extend(f"{n}\n" for n in notes if n)
    md = "\n".join(out)
    with open(sys.argv[2], "w", encoding="utf-8", newline="\n") as f:
        f.write(md)
    if skipped:
        print(f"pptx_text: text not read from {len(skipped)} chart or SmartArt shapes: {', '.join(skipped)}", file=sys.stderr)
    body = re.sub(r"\s|^#+ Slide \d+$", "", md, flags=re.M)
    cjk = len(re.findall(r"[぀-ヿ一-鿿]", body))
    print("ja" if cjk * 10 > len(body) else "en")
    return 0


if __name__ == "__main__":
    sys.exit(main())
