"""pdf2md.py - the sentences of a pdftotext file as Markdown paragraphs.

    python3 pdf2md.py <in.txt> <out.md> [<first line> <last line>]

Lines are joined until a line ends in a full stop; a blank line, a page number
or a line with no hiragana ends a paragraph. Paragraphs with no full stop are
dropped, as extract.py drops them.
"""
import re
import sys

rows = open(sys.argv[1], encoding="utf-8").read().split("\n")
if len(sys.argv) > 4:
    rows = rows[int(sys.argv[3]) - 1:int(sys.argv[4])]
paras, cur = [], ""
for row in rows:
    t = row.strip()
    if not t or re.fullmatch(r"[-－ 0-9０-９ivx]+", t) or not re.search(r"[ぁ-ゖ]", t):
        if cur:
            paras.append(cur)
        cur = ""
        continue
    t = re.sub(r"(?<=[ぁ-ゖァ-ヺ一-鿿、。，．（）「」０-９])\s+(?=[ぁ-ゖァ-ヺ一-鿿、。，．（）「」０-９])", "", t)
    indent = row.startswith(("　", "    ")) and cur.endswith("。")
    if indent:
        paras.append(cur)
        cur = ""
    cur += t
    if t.endswith("。") and len(row.rstrip()) < 0.75 * max(len(r) for r in rows if r.strip()):
        paras.append(cur)
        cur = ""
if cur:
    paras.append(cur)
paras = [re.sub(r"^[○・\s]+", "", p) for p in paras if "。" in p and len(p) >= 25]
open(sys.argv[2], "w", encoding="utf-8").write("\n\n".join(paras) + "\n")
print(sys.argv[2], len(paras), "paragraphs", sum(p.count("。") for p in paras), "sentence ends")
