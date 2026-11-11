# How the drafts were made

Three kinds of draft stand behind the tables. No rule of this skill was in
force for any of them: the plugin's hooks were not installed in the session,
and no prompt named the skill, a linter or the comparison.

## A. Eight administrative documents, from notes in Japanese

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

## B. Six business documents, from notes in English

The same two steps, with the notes written in English. The notes agent was
told to write every common noun and technical term in English, the words the
source writes in katakana included, and to keep only proper names in their
own script. The drafting agent got the same kind of prompt as in A (the kind
of document, the reader, です・ます, a length near the original's), with
「見出しはメモの見出しを日本語にして使う」. So each word of the draft is the
drafter's own choice, which is what the comparison of katakana words needs.
One prompt, for the 楽天 notice, asked for running prose throughout; the
others allowed a list where the notes list items.

## C. Five business documents, from a brief

One agent each, with a brief of three lines and leave to supply the details:

- an incident report: a login failure of about two hours, caused by a
  certificate left to expire;
- a proposal to a manager: moving sales tracking from a spreadsheet to one of
  two customer-management tools;
- a design note for developers: adding a cache to a slow internal search;
- a progress report: a core-system replacement, a week behind, with the
  cut-over date held;
- an explainer for staff: two-step sign-in on every company PC.

These have no original to stand beside. They show what Claude writes when the
content is its own.

## Limits of the design

- Fourteen pairs and five free drafts, and one model wrote every draft.
- The business set is what companies publish. Mail, minutes and reports
  written inside a company are not in it.
- The notes keep each relation and each grade of certainty as a tag, so the
  drafts were told what joins what. A draft from thinner notes would hold
  fewer joins still; the design measures the shape of the prose, with the
  content held equal.
- Neither set holds a personal blog post or a slide deck, so the `article`
  and `slides` styles rest on the columns and the magazine articles of the
  administrative set alone.
