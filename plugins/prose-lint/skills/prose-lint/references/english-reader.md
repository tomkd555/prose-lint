# Reading English

The material the reader in Step 3b works from. vale finds surface forms; these checks find sentences
that fail in meaning or carry the shape of a Japanese draft. Quotations, code and terms of art stay
out of every check; the cells of a specification table stay out of the sentence checks.

## The checks

Ask each question of every sentence. An answer of YES is a finding. Each rewrite keeps every fact,
number and citation.

| id | Question |
| --- | --- |
| `actor` | Is the subject an abstraction doing what only a person can do, such as deciding or corroborating? A program, a rule, a type or a standard doing its defined job is sound, and so is "doing so improves performance". |
| `noun-load` | Does a noun phrase need unpacking to be understood: three or more modifiers before the head, or a nominalisation as the subject of "is"? |
| `dictionary` | Is a word the dictionary match of a Japanese word, where the field or the passages below use another? "Hearing" for a client interview is one. |
| `topic-frame` | Does the sentence map word for word onto one Japanese sentence with a 〜は topic, and hold no ordinary English order? |
| `function-word` | Is the sentence ungrammatical because a "that", "for", article or subject is missing, or is a future plan written in the present tense? An optional "that" and a concise but grammatical sentence are sound. |
| `fragment` | Does a label or a clipped phrase stand where the reader needs a sentence? Headings, table cells and specification lists stay. |
| `frame` | Do three or more neighbouring sentences share one frame, or does a stock phrase recur through the document? |
| `two-senses` | Is one word used in two senses that a reader could confuse here? A term of art next to its everyday sense, with the context settling which is meant, is sound. |
| `join` | Does "and" or "while" link two facts with no stated relation? |
| `scope` | Does a claim go further than the evidence in the text? A specification's statement of what it guarantees is sound. |

Ask these of each table and each heading or slide title, read with the text under it, instead of
the sentence checks; `title-flow` once per document. An answer of YES is a finding.

| id | Question |
| --- | --- |
| `table-header` | Read with the values under it, does a column header, without another header or the text around the table, fail to name the quantity its values are, or leave out a unit the values carry? A header that points at another header ("its", "this", "the above", "same") or runs on into its cells answers YES. |
| `table-purpose` | Read with its title or the sentence before it, does the table leave unnamed the data it holds? |
| `title-subject` | Does the title name its subject by a symbol or an abbreviation alone, with no word for it in the title or the text under it? |
| `title-role` | Asked only of a slide that holds its title alone: is the title a sentence with no word that says what the slide is, such as "task" or "conclusion"? A closing slide of thanks is sound. |
| `title-message` | Asked only when the sentences under the title state a result or a claim: does the title state none of them? A slide of a table, numbers or formulas alone, with no sentence that states a result, keeps a topic title, and so does a heading the document's genre fixes, such as "Background". A rewrite keeps the title within two lines. |
| `title-flow` | Read in order, do the titles alone leave the content hard to follow, as when two titles read the same over different content, or a step of the content has no title that names it? |

## Passages

Compare each sentence with how these passages open, end and join. Each one names its actor, keeps
modifiers after the noun where they run long, and states a relation with a word for it.

Business, from a speech by Jerome Powell, 2020-08-27 (public domain):

> For the past year and a half, my colleagues and I on the Federal Open Market Committee (FOMC) have
> been conducting the first-ever public review of our monetary policy framework.

> Because the economy is always evolving, the FOMC's strategy for achieving its goals—our policy
> framework—must adapt to meet the new challenges that arise.

Public administration, from the GOV.UK Service Manual, "Writing user stories" (Open Government
Licence):

> Your user stories should include enough information for your product manager to decide how
> important the story is.

> Large user stories (ones that would take more than a few weeks to develop and test) are typically
> called epics. If possible, split a large story or epic into smaller stories that can be completed
> within an iteration.

Technical, from the Google developer documentation style guide, "Voice and tone" (CC BY 4.0):

> Consider that readers come from many different cultures and may have varying levels of ability
> reading English.

## Sources

- The table and title checks carry over section 3.5 of `translationese-japanese.md`, which quotes
  and dates each source: Microsoft Writing Style Guide, "Tables",
  https://learn.microsoft.com/en-us/style-guide/scannable-content/tables; WordPress Documentation
  Style Guide, "Tables", https://make.wordpress.org/docs/style-guide/formatting/tables/; Wei Liu,
  "Preparing better tables" (2018), https://jphe.amegroups.org/article/view/4327/html; Garner and
  Alley (2013), https://www.ijee.ie/articles/Vol29-6/23_ijee2791ns.pdf; 「公用文作成の考え方」 Ⅲ-2
  on 標題 and 見出し, https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/pdf/93651301_01.pdf
- https://www.federalreserve.gov/newsevents/speech/powell20200827a.htm
- https://www.gov.uk/service-manual/agile-delivery/writing-user-stories
- https://developers.google.com/style/tone
