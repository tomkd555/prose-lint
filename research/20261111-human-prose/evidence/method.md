# How the eight drafts were made

Each of the eight documents went through two agents, each in a fresh context.

1. **Notes.** One agent read the document and wrote notes: the headings as
   they stand, and under each a list of keyword items. Its prompt:

   > The notes are what a writer would hold before drafting the document: its
   > content with the prose taken away. Keep every heading of the source, in
   > order. Under each heading, bullet items. Each item is a noun phrase or a
   > keyword line, never a full sentence: no です/ます/である endings, no
   > 接続詞, no 接続助詞 joining clauses. Keep every fact, number, date, name,
   > term, quoted phrase and example of the source. Leave nothing out and add
   > nothing. Where the source states a relation between two items, tag it at
   > the head of the item: [原因], [結果], [対比], [条件], [例], [根拠],
   > [経緯]. Where the source gives a judgement, a request or a limit, tag it
   > [判断・確信高], [判断・確信中], [判断・確信低], [依頼], [義務], [限定],
   > and for a statement of plain fact use no tag. Do not copy any run of more
   > than 15 characters from the source, except names, terms, titles and
   > quotations inside 「」.

2. **Draft.** A second agent, which never saw the document, wrote it from the
   notes. Its prompt named the kind of document, the reader, the 文体 of the
   original and a length within about 10 % of the original's, and said:

   > 見出しはメモのとおりに使う。本文は箇条書きにせず文章で書く。メモにある
   > 事実・数値・名称はすべて使い、メモにない事実は足さない。タグ自体は本文に
   > 書かない。

No rule of this skill was in force for either agent: the plugin's hooks were
not installed in the session, and neither prompt named the skill, a linter or
the comparison.

Limits of the design:

- Eight pairs, and one model wrote every draft.
- The notes keep each relation and each grade of certainty as a tag, so the
  drafts were told what joins what. A draft from thinner notes would hold
  fewer joins still; the design measures the shape of the prose, with the
  content held equal.
- The originals are administrative prose. The set holds no blog post and no
  slide deck, so the `article` and `slides` styles rest on the columns and the
  magazine articles alone.
