# Tools of the 1.12.0 measurement

The scripts that produced sections 1 and 4 of
`plugins/prose-lint/skills/prose-lint/references/flow-japanese.md`. They read a
corpus kept outside the repository; `../evidence/corpus-business.md` and
`../evidence/corpus.md` list its 43 and 35 documents with their URLs.

| Script | Does |
| --- | --- |
| `extract.py` | Takes the body of a saved HTML page out as Markdown: headings, paragraphs, list items. A line with no full stop is dropped. Nothing is retyped. |
| `pdf2md.py` | Joins the lines of a `pdftotext` file into paragraphs of sentences. |
| `kinds.py` | The document ids by kind. |
| `layers.py` | Runs `flow.py`, `koyobun.py`, the three registers, textlint and natural-japanese's lint over each file and writes one JSON. |
| `sentsplit.py` | Writes each document one body sentence to a paragraph, as `flow.py` reads its sentences. |
| `layers_fast.py` | Runs textlint, two registers and `koyobun.py` over those files. |
| `features.py` | Counts what `flow.py` leaves out: the kinds of opening, も, stance adverbs, paragraph sizes. |
| `report.py` | Prints the tables of the administrative set from the JSON files of the others. |
| `words.py` | Counts katakana words, one-kanji nouns standing alone and the surface forms the translationese reference names. |
| `bizreport.py` | Prints the tables of the business set. |

Order of a run, in a corpus directory with `raw/` holding the saved pages:

```
uv run extract.py raw/<id>.html human/<id>.md        # per page
python3 layers.py <skill dir> layers-human.json human/*.md
uv run sentsplit.py <skill dir>/scripts sent human/*.md
python3 layers_fast.py <skill dir> sent-layers.json sent/*.md
uv run <skill dir>/scripts/flow.py --json human/<id>.md > flow2/h_<id>.json   # per file
python3 report.py
```

The drafts go through the same steps into `gen/`, `gensent/`, `layers-gen.json`,
`gensent-layers.json` and `flow2/g_<id>.json`. `../evidence/method.md` says how
they were made.
