---
name: prose-lint
description: >-
  Runs the wording linters on a file or pasted text and picks the ones the text's language calls for. For Japanese: a style settled first (genre, reader, 文体 and where the words come from, or style=<name> from a calling skill) that every rewrite is written to; a reader in a fresh context that finds translationese from a sourced reference and judges each sentence against exemplar passages of present-day Japanese for the style (公用文, a council report, a government technical guide, a review article, an incident report and award-winning papers); a flow check that counts how the sentences end and join, read by paragraph before the fixes and compared with the original after them, so a rewrite keeps how sure each sentence is and how it ties to the next; a norm check that lays the rates of ordinary forms (clause joints, connectives, demonstratives, the passive, noun-and-する verbs) beside a baseline counted from news text and marks a text that leaves them out; a register of 13 translationese forms; textlint with the technical-writing, JTF, AI-writing and AI-words presets, the kana rules of 内閣訓令 and い抜き・さ入れ・フィラー; a register of rejected wordings; natural-japanese's lint with its naturalness score; a sudachipy morphology lint for 公用文作成の考え方 and house rules; an academic mode for papers, theses and reports; and, for blog posts, essays and slide decks (a .pptx included), stop-ai-slop-jp's phrase register, its structure patterns read by the reader and its five-axis score. For English: a reader in a fresh context, textlint, the register's negation row, and vale with proselint, ai-tells and five house rules. For a translation in either direction: a script and a reader in a fresh context that compare the target with its source, and one rewrite pass. Triggers on 「textlint かけて」「lint して」「lint 回して」「校正して」「表記チェック」「vale かけて」「否定形を消して」「否定で定義した文を直して」「AI っぽさを消して」「論文調にして」「論文向けの表現に直して」「レポートの文体にして」「学術的な表現に」「口語表現を直して」「翻訳調を直して」「直訳っぽい」「翻訳っぽい」「英語の直訳になっている」「AI臭を消して」「ブログを直して」「スライドの文言を直して」「翻訳をチェックして」「訳文を確認して」「この翻訳を見て」「無機質な文章を直して」「文章が硬い」「ぶつ切りを直して」「文のつながりを見て」, "run textlint", "lint this file", "proofread this", "check this English draft", "check this translation", "does this read as AI-written". Use it whenever the user names a linter or asks for a wording check on a document.
---

# Prose lint

Runs the linters over one text on demand, settles which config the text's
language calls for, and rules on every hit. Read `{SKILL_DIR}` below as the
absolute path of this skill's directory, and `{HOME}` as `$PROSE_LINT_HOME`, or
`~/.prose-lint` when that is unset.

## Step 0 - setup

The plugin's SessionStart hook sets up the linters in the background, on the
first session after an install or an update. It fetches uv when none is on
PATH and runs `scripts/setup.py`, which copies the textlint and vale configs
and the registers to `{HOME}`, downloads vale and Node with npm under `{HOME}`
when they are not on PATH, and runs `npm install` and `vale sync`.
`{HOME}/.setup-version` names the plugin version of the last setup that
finished. When it is missing or older than this plugin, as after an install
in the running session, run the hook's script and wait for it:

```
bash {SKILL_DIR}/../../hooks/session-start.sh
```

It prints the log's path and every `skip` or `fail` line. The plugin's other
hooks (`hooks/lint.py`) run textlint and the register on each file Claude
writes, on each Japanese reply, and on plans and questions before they reach
the user; this skill runs every layer. A skill copied by
hand has no hook; run `uv run python {SKILL_DIR}/scripts/setup.py` there. A
layer whose tool is still missing is reported as skipped in the final report;
the other layers still run.

The commands below start with `prose-lint-run`, which the plugin puts on PATH:
it adds the uv, vale and Node that setup downloaded. A skill copied by hand
drops it.

natural-japanese (https://github.com/coji/natural-japanese, MIT, coji) ships
in `{SKILL_DIR}/vendor/natural-japanese`. `{NJ}` below is its `scripts`
directory. Its `SKILL.md` is renamed `guide.md` there, so Claude Code does not
load it as a second skill; natural-japanese's `SKILL.md` below, and a mention
of `SKILL.md` in its own files, mean that file.

## Step 1 - settle the target

The target is the path in the request, or else the file the conversation is
working on. With neither, ask which text to lint. Pasted text goes to a `.md`
file in a temporary directory first, because textlint, vale and the scripts
all read files.

A request that hands over a source and its translation, or asks for a
translation, goes to Step 3c first. The target is the translation, and Step 2
routes it after that step.

A PowerPoint file goes to a `.md` file in a temporary directory too:

```
prose-lint-run uv run {SKILL_DIR}/scripts/pptx_text.py <deck.pptx> <tmp>/deck.md
prose-lint-run uv run {SKILL_DIR}/scripts/pptx_text.py --flat <deck.pptx> <tmp>/deck-flat.md
```

Each slide becomes a `## Slide <n>` section. The title placeholder gives one
`### ` heading per paragraph or line break; a title drawn in a text box is a
`- ` item. Every other paragraph and line break of a shape or a group is a `- `
item, each table a Markdown table whose first row becomes its header row, and
the speaker notes follow under `### Notes`. A picture leaves a
`<!-- picture -->` line on its slide, and a chart or SmartArt a
`<!-- chart or SmartArt -->` line. `deck-flat.md` writes each paragraph of a
table cell as a `- ` item instead and leaves the comment lines out, for textlint
alone: textlint's sentence rules skip the cells of a Markdown table, and a
comment line between two items splits a list for its list rules. The script names on stderr, by slide, each
chart or SmartArt whose text it could not read; say so in the report. It prints
`ja` or `en`, and that settles Step 2 for the deck.

The layers run on that file, every fix is applied to it, and the second runs
read it. The report gives each finding and each rewrite by its slide. The deck
itself stays as it is, because a text edit through python-pptx drops the run
formatting.

## Step 2 - route by script

A deck takes the language `pptx_text.py` printed in Step 1. For any other
file, hiragana over 10% of the non-whitespace body means Japanese, otherwise
English:

```
prose-lint-run uv run python -c "import re,sys;t=open(sys.argv[1],encoding='utf-8').read();b=len(re.sub(r'\s','',t));print('ja' if len(re.findall('[ぁ-ゟ]',t))*10>b else 'en')" <file>
```

It counts hiragana alone on purpose: the Japanese an English document quotes is
terminology - kanji and katakana, almost no hiragana - so an English document
holding a dozen Japanese terms still routes to English.

A mixed document runs once, under its majority language. Findings that land on a
quotation in the other language get dropped.

A Japanese text also runs in **academic mode** in two cases. The user asks for
the register of a paper, thesis or report: 論文調, 論文向け, レポートの文体,
学術的な表現 or 口語表現を直して. Or the text is plainly one: a 参考文献 or
引用文献 section together with 本研究, 本稿 or 本論文 in the body. The report
says which of the two put the run in academic mode. Academic mode adds one
step to 3a and changes some rulings; the other layers run as usual.

A Japanese text also gets a **style** before any layer runs: what the document
is and who reads it, its 文体, and where its words come from. The reader in
Step 3a judges the text against it, and every rewrite is written to it. A
calling skill can name it with `style=<name>`; otherwise settle it from the
request, the file name, the headings and the text, and state it in one line at
the head of the report (「style: business - 設計書、読み手は開発者、常体、IT の
用語はカタカナ」).

| Style | Signals | 文体 | Words |
| --- | --- | --- | --- |
| `business`, the default | 設計書, 仕様書, 手順書, 報告書, 計画書, 議事録, README, a work email | the one most body sentences end in | the reader's field terms in the form the field writes them: an engineer's katakana term (スクリーンショット, コンポーネント, デプロイ) over a 漢語 rendering; a 漢語 predicate where the sentence carries weight |
| `paper` | `style=paper` from a calling skill: a business document for print or hand-over | 常体 in the である form throughout | as `business` |
| `official` | 通知, 規程, 要綱, a notice from an organisation to the public | the one most body sentences end in | the words of 公用文, and 外来語 only where the reader knows them |
| `academic` | the academic-mode signals above | 常体 in the である form | the academic register |
| `article` | a blog post, note, essay or column for a general reader | the one most body sentences end in | everyday 和語 over 漢語; a field term only where the reader knows it |
| `slides` | a `.pptx`, a Marp or reveal.js deck, a slide outline, スライド or 発表資料 | 体言止め in titles and bullets; the 文体 most full sentences end in | as `business` for a business deck, as `article` for a talk to the public |

The `article` and `slides` styles also run the stop-ai-slop-jp layer in Step
3a.

`{SKILL_DIR}/references/exemplars-japanese.md` quotes present-day Japanese
that institutions and award committees hold up as well written: 公用文 for
`official`, a council report, a government technical guide, a review
article and an incident report for `business`, award-winning papers for
`academic`, and writing for the general public for `article`, and the
business or public group for `slides`. Passages 2.4, 2.5, 4.3 and 4.4 show a
writer weighing a choice or a cause, with the endings and the joins that
carry it. Its section 0 names the groups each style reads. Each passage names its source and the features to take from it.

A sentence off the style's 文体 is a finding. In `paper` a です・ます sentence
gets rewritten; in the others the minority 文体 does, unless a quotation or a
direct address explains it. In `article` the spoken-register rows of the
register stay where the text is casual by design.

## Step 3a - Japanese

Launch the reader first, in the background, then run the mechanical layers
while it reads; the review comes last. Each layer reports suspicions; the
ruling on each hit is yours and goes in the report. Start fixing once the
reader has returned and the review is done: the reader reads the file as it
stands, and a sentence fixed for one layer's hit gets rewritten again for the
next. With the whole ledger in hand, each sentence is rewritten once in the
main pass, against all its hits.

Before the first Edit, copy the file to `<tmp>/original.md`. The flow check
after the fixes compares the two.

A hit names a wording. The sentence around it also does a job in its
paragraph: it says how sure the writer is, gives a reason, sets a limit, or
ties the next sentence to the last. Every layer below takes wordings out, and
no layer before 1.11.0 looked at what went out with them, so a run could clear
its ledger and leave a list of bare statements. Three measurements for 1.11.0
are in `{SKILL_DIR}/references/flow-japanese.md`, section 1. The mechanical
layers flagged 45 of the 74 sentences in this skill's own exemplar passages,
19 of them under a rule this file said to fix. A report written under this
plugin's hooks held 0.46 clause joints a sentence, where the human-written
documents measured hold 0.75 to 1.63. And the naturalness score read 96.9 on a
memo whose sentences ran 30 characters on average. So a ruling of "fix" means
this: take the wording out and keep the job, as "Writing a fix" sets out.
Where a layer leaves a hit to judgement, a sentence that reads well and does
its job is kept, with that as the reason. Where a layer says a hit is fixed
or rewritten, that ruling stands, and the fix keeps the job.

### The reader

The other layers match surface forms. The translationese they leave lies in
word senses and sentence frames, which only a reading finds. A word gets
picked as the dictionary match of an English one: 提供する for *provide* in 「MWCは製品発表以外にも多くのことを提供する」, where Japanese says
「多くの見どころがある」. A frame gets built in English order:
「この機能はユーザーにデータ出力を可能にします」 for a feature that lets users
export data. The same word is right in its own sense elsewhere, and the
human-written documents the reference measured use the commonest surface forms
too (において in 47 of 83), so the decision needs the sentence and the document
around it.

Launch one agent, `model: opus`, in a fresh context. Its prompt carries:

- the purpose in one line: find every sentence of one Japanese document whose
  meaning a reader cannot recover, that reads as translated from English, or
  whose 文体 or words do not fit the document's style, every title that names
  its subject by no word or leaves out the result its text states, every
  table header that needs another header or a cell to name its column, and
  every paragraph whose sentences stand side by side with nothing to join
  them, and propose a rewrite for each;
- the document's absolute path and the style line from Step 2;
- the absolute path of `{SKILL_DIR}/references/translationese-japanese.md`,
  with "read it first, answer the questions of its section 3.4 for every
  sentence and those of section 3.5 for every heading, slide title and table,
  and use its marker ids";
- the absolute path of `{SKILL_DIR}/references/exemplars-japanese.md`, with
  "read section 0 and the groups it names for the style, and compare each
  sentence with how those passages open and end their sentences, which words
  they choose and how they join. A sentence that differs from the passages
  in shape alone, and reads well, is no finding";
- the absolute path of `{SKILL_DIR}/references/flow-japanese.md`, with "read
  it after the exemplars and ask the questions of its section 3 of every
  paragraph of two or more sentences of running text, a list item of two or
  more sentences included. Mark each finding with
  its `flow-` id, give the line the paragraph starts on, quote its first
  sentence, and write the rewrite as the whole paragraph, made only of what
  the paragraph and its neighbours already say";
- for `article` and `slides`, the absolute paths of
  `{SKILL_DIR}/references/stop-ai-slop-jp/rules.md` and of `structures.md`,
  `examples.md` and `phrases.md` beside it, with "read them after the
  reference. Find every pattern of structures.md except §4-5 and §4-6, and
  the points of the rules' quick check under 構造レベル, 文・段落レベル and
  強度と立場, except the one on uniform sentence endings. From phrases.md, find
  the words it limits to a metaphorical use (装置, インフラ, 設計, 接続) and
  full proper names repeated (§3). Mark each finding `slop-<section>`
  (`slop-1-1` for false agency), `slop-rule-<n>` for a core rule or
  `slop-phrases-<section>`. Close with five lines, one per axis of the rules'
  採点 section: `score | <axis> | <1-10> | <grounds in one sentence>`";
- the absolute path in `$PROSE_LINT_PATTERNS`, when that names a file: the
  user's own notes on wordings they rejected, read after the reference;
- the output shape, one finding per line:
  `<line> | <marker id> | "<sentence>" | <rewrite> | <reason>`, the reason
  in one sentence;
- "report every finding, no severity filter";
- the scope: notation, kana, sentence length and the register's wordings belong
  to the other layers, and a verbatim quotation is left as it stands;
- English as the output language, with Japanese quoted verbatim.

It withholds who wrote the text, the task it served, any reason a wording was
chosen, the lint results and any expected finding. A reader handed those reads
the intent into each sentence and passes the English frame it sits in.

Its findings join the ledger and are ruled on like any other hit.

The reader reads a document in full on its first run in a session, and again
when the document changed outside the session. On a later run over a
document it has already read, such as a revised draft, it takes the second
read's form (end of "Writing a fix") over the passages changed since that
run.

### textlint

```
prose-lint-run {HOME}/textlint/node_modules/.bin/textlint --config {HOME}/textlint/.textlintrc.json <file>
```

For a deck, `<file>` is `<tmp>/deck-flat.md` from Step 1; its findings are
fixed in `deck.md`, slide by slide. textlint exits 1 when it finds anything, so
read the output and ignore the exit code. The findings fall in three tiers by
rule id:

- Blocking - fix these:
  `ja-no-redundant-expression`, `ja-no-abusage`,
  `ja-no-successive-word`, `no-doubled-conjunctive-particle-ga`,
  `no-double-negative-ja`, `no-dropping-the-ra`, `@textlint-ja/no-dropping-i`,
  `@textlint-ja/no-insert-dropping-sa`, `@textlint-ja/no-filler`,
  `no-mix-dearu-desumasu`, `prefer-tari-tari` (a たり with no partner:
  rewrite with the pair, 読んだり書いたりする, or without たり), and the kana rules: `ja-keishikimeishi`,
  `ja-hiragana-hojodoushi`, `ja-hiragana-daimeishi`, `ja-hiragana-fukushi`
  and `prh`. The four hiragana rules and prh together restate 「公用文における
  漢字使用等について」(平成22年内閣訓令第1号) 別紙. prh carries the
  conjunctions, auxiliaries and the fixed phrases of its item キ. Those
  phrases include 但し, 出来る, 様に, 通り and 致します. Each prh message names
  the item it comes from. The fukushi dictionary is the rule's own minus the five words the
  訓令 keeps in kanji (更に, 既に, 最も, 僅か, 若しくは). A kana rule firing on
  a proper noun, a legal term or a quotation is kept, with that reason.
  `ja-no-redundant-expression` runs without its 〜を行う dictionary; the
  reader judges the light verb (`light-verb` in the reference).
- Advisory - each needs judgement: `no-doubled-joshi`, `no-doubled-conjunction`,
  `sentence-length` (90 characters), `max-ten`, `max-kanji-continuous-len`,
  `no-ai-hype-expressions`, `ai-tech-writing-guideline`, `ai-words-ja/no-ai-words`,
  `@textlint-ja/no-synonyms` and `ja-no-weak-phrase`. `ja-no-weak-phrase`
  reports かもしれない, と思う and their kin, and was a blocking rule up to
  1.10.0. A hedge on something the writer knows or decides gets stated
  plainly (「実施したいと思います」 becomes 「実施します」). A hedge that reports
  how far the evidence goes stays, in the written form the style takes
  (と考えられる, 可能性がある, 見込みである): cut it and a guess reads as a fact.
  The rule fired on 「可能性を示唆している」 in an award-winning paper among the
  exemplars. A `sentence-length` hit on a sentence that reads in one pass,
  its clauses in the order things happened, stays: the 建議 sets a point at
  which to check a sentence and no cap (`flow-japanese.md`, section 2.3). `no-ai-words` reports words generated Japanese
  overuses: a figurative verb (走る, 焼く, 見張る) gets the literal one, and a
  term the document's field uses in its literal sense (検査, 照合) stays. A particle repeated in a plain list holds; the
  conjunctive が repeated in one sentence gets fixed. The two AI-writing rules
  also fire on a negated 完全には and on 必要があります. `no-synonyms` reports
  two spellings of one word in the document (ユーザー and ユーザ, アプリ and
  アプリケーション); settle on the spelling the field uses, and keep a pair
  that names two things, such as a company and its group. Fix the ones that
  hold and say why the others stay.
- Notation - every other rule: punctuation, spacing, numerals. Leave them alone
  unless the user asks for notation.

### The register

```
prose-lint-run uv run {SKILL_DIR}/scripts/register.py <file>
```

The register is a Markdown table, or a CSV with the header `Pattern,Instead,Why`,
of rejected wordings: `$PROSE_LINT_REGISTER`, else `{HOME}/vocabulary.md`, else
the sample in `assets/`. A CSV headed `Pattern,Instead,Except` lists plain words
matched as written, and its `Except` column gives the exception shown with each
hit; `register.py`'s docstring has the rules. A plain word that holds kana
or kanji is matched on morpheme boundaries, read with sudachipy: the row 語
matches 「この語は」 and leaves 語った alone, 置き leaves 位置 and 置き換える,
旅 leaves 旅行, and a verb row written as its stem (述べ) matches every form
of that verb. Measured for 1.12.0 with one user's register of 344 rows:
substring matching flagged 92.5 % of 400 news articles, and the boundary test
dropped 16.4 % of the hits on news text held out of the baseline, each of the
sampled ones a different word. A word used in its literal sense still
matches (請求 in 請求書, 事故 in 交通事故), so a row for a figurative use
needs its `Except` text, and the ruling stays with the reader of the hit. The script prints
which one it read. The sample carries twelve rows in three groups.

- Definition by negation, two rows. The Japanese row on `ではない` also covers
  `でない`, `じゃない`, `に当たらない`, `該当しない` and `非該当`; the English
  row covers `not X but Y`, `X, not Y`, `rather than`, `instead of` and
  `not applicable`. Two forms stay: quoted text, and a verb plainly negated.
  Every other hit gets rewritten: say what the thing is; where the sentence
  draws a boundary, name what falls inside it; where it corrects a wrong idea,
  state the right one and leave the wrong one out. Write the sentence a
  business document would carry, in the words of the text around it; a
  template sentence reads as translation. The positive sentence has to say
  the same thing with the same force, from what the text already holds. Two
  more forms stay for that reason, each with the reason in the report: a
  negation that limits the text's own claim, where the positive form would
  claim more or less (「いつでも通用するような正解があるわけではない。しかし、
  より望ましい方法は、きっとあるはずである。」 in the exemplars), and a negation
  whose positive form needs a fact, a plan or a promise the text lacks. In the
  1.10.0 run on a memo, 「移行そのものの判断は含みません」 came out as
  「移行そのもののご判断は改めてお願いします」, a request the memo never made.
- The spoken register, four rows: なので and だから at a sentence start, 一番
  before an adjective, ほぼ全部. Rewrite in a formal document; a quotation or
  a deliberately casual text keeps them.
- The stock phrases of generated Japanese, six rows. Each is on a pattern that
  natural-japanese's catalogue lists but its lint leaves to the eye:
  - hearsay with no source (と言われています, とされています, という声もあります)
  - breadth adjectives that stand in for a list (様々な, 多様な, 幅広い)
  - outcomes named by an abstract noun (を実現, に寄与, シームレス, 最適化)
  - an intention softened with と思います
  - the closing ぜひ〜してみてください
  - the opening 今回は〜について紹介します

  Rewrite each as the row says: name the source or own the claim, list the
  items, say what changes, say it plainly, delete the boilerplate. A hit
  inside a quotation stays. Where the text holds no source, no items or no
  outcome to put in the phrase's place, the phrase stays and the gap goes in
  the report as a question for the author; cutting it would leave a barer
  claim than the writer made.

The regex matches surface forms only. The `negated_predicate` id of the
morphology lint below lists every sentence whose final predicate is negated.
Read each one and rewrite the ones whose whole content is a denial:
「〜とは限らない」, 「〜するわけがない」, 「〜を含まない」, 「〜せず」 or
「〜しない」 used to define a thing or to draw its boundary, and a clause that
names only what something lacks. The two forms that stay under the negation
row stay here too. The other rows are handled as the register
says: kept when the wording fits the context and the reason is stated, otherwise
rewritten.

### The translationese register

```
prose-lint-run uv run {SKILL_DIR}/scripts/register.py --translationese <file>
```

The register is `$PROSE_LINT_TRANSLATIONESE_REGISTER`, else
`{HOME}/translationese.md`, else `assets/translationese.sample.md`. Its rows
are the forms from the reference that a regex can find. Each rests on a
published source and was measured against 83 human-written documents:
business, technical, essays and slides. The rows fall in two groups:

- Rewrite, seven rows, each matching at most 2 of the 83 human documents:
  - 彼, 彼女 and 彼ら
  - a feature or product made the agent (この機能は〜を可能にします)
  - これは〜を示す
  - 値を持つ
  - に存在する before a noun
  - および／または
  - されるように設定され

  Rewrite each to the style; the row's `Why` names any exception.
- Read in context, six rows that human writers use in some kinds of document:
  - が可能です
  - することにより
  - を可能にする
  - あなた
  - 私たち
  - the em dash

  Rule each by the style and the sentence.

A span that a row of each group matches (この機能は〜を可能にします) is one
finding, ruled under the Rewrite row. The bracket at the end of each `Why`
names the sources; keep it in the report.

### stop-ai-slop-jp (`article` and `slides`)

```
prose-lint-run uv run {SKILL_DIR}/scripts/register.py --slop <file>
```

stop-ai-slop-jp (https://github.com/iKora128/stop-ai-slop-jp, MIT, Daichi
Nagashima) is a guide to the tells of AI-written Japanese in blog posts and
essays. Its files sit in `{SKILL_DIR}/references/stop-ai-slop-jp/`. `rules.md`
is its `SKILL.md`: the core rules, the quick check, the five-axis score and
the fix order. `phrases.md`, `structures.md` and `examples.md` are its
references; a link in `rules.md` to `references/<file>` means the file beside
it. The layer runs on the `article` and `slides` styles and on no other.

The register is `$PROSE_LINT_SLOP_REGISTER`, else `{HOME}/slop.md`, else
`assets/slop.sample.md`: 31 rows restating `phrases.md` and the symbol rules
13 and 14 of `rules.md`. Each hit carries its group in brackets.

- `[Rewrite]`, 10 rows. Rewrite each hit.
- `[Count]`, 12 rows: ordinary words that become a tell by repetition. Count
  the hits per article or per paragraph as the row's `Why` says, and rewrite
  once the count reaches it.
- `[Read in context]`, 9 rows: forms human writers also use. Rule each by the
  sentence.

The rows were measured on technical books and Wikipedia; blog posts and
essays were not in the measurement, so read each hit with that in mind.

The reader covers what a regex cannot find: the sections of `structures.md`,
the quick-check points that need a reading, and the metaphor-only words of
`phrases.md`. Rule its `slop-` findings with the others. A span that rows of
two registers match, such as the em dash, is one finding, ruled under the
stricter group.

Where this layer meets another, the rulings go this way:

- `structures.md` §4-5 (mixed sentence endings) and §4-6 (kept fillers and
  typos) yield to the style's 文体 and to textlint's blocking rules. The
  reader leaves them out, and no rewrite adds a filler, a typo or a second
  文体. The flow layer carries what §4-5 is after inside one 文体: endings
  that follow what each sentence does.
- `rules.md` rule 4 asks for hearsay marked as hearsay (らしい, と聞いた). In
  `article` and `slides` it takes the place of the hearsay row's "言い切る"
  branch: name the source where there is one, and mark hearsay as hearsay
  where there is none.
- In `slides`, 体言止め in a `### ` title or a `- ` item is the medium's form;
  the morphology lint reads a deck's `- ` items as body text and leaves
  `nominal_ending` silent on them. Rule 9's uneven
  rhythm reads per slide body; the notes read as prose.
- The first person, the 毒 and the uneven rhythm of rules 5, 6 and 9 serve an
  article. A business deck keeps the writer's stance and drops the rest; say
  so in the report.
- Rules 2 and 5 and the first step of the fix order ask for a stance and for
  people, numbers and failures the writer knows. A rewrite never adds a fact,
  a number, an anecdote or an opinion the text lacks. Put each such finding in
  the report as a question for the author.

The fix order of `rules.md` (stance, false agency, structure templates, words
and phrases, then symbols) settles which hit leads when one sentence carries
several, and the order of the layer's findings in the report. Each sentence is
still rewritten once, in the main pass.

### natural-japanese lint

```
prose-lint-run uv run {NJ}/lint.py --genre business --reading-load --json <file> > <tmp>/nj-1.json
prose-lint-run uv run python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));d.pop('paragraphs',None);print(json.dumps(d,ensure_ascii=False))" <tmp>/nj-1.json
```

`--genre business` selects natural-japanese's business profile, which mainly
switches off detectors that misfire on bullet-heavy business documents. The
JSON goes to a temporary file so it serves twice: it is the ledger the report
rules on, and the baseline for the second run below.
Read it through the second command, which prints it without the `paragraphs`
key. From natural-japanese 1.6.0 that key copies every paragraph of the
document as the worksheet for that skill's own paragraph check, and it makes
up most of the file. Two lanes come out.

- The AI-smell lane: banned phrases and translationese, uniform sentence length,
  the 体言止め rate, paragraph-opening conjunctions and lexical variety. Judge each
  hit by the fix its own message gives and by §3 of natural-japanese's
  `SKILL.md` (「既存の文書を直すとき」). A `forbidden_phrase` hit on a
  connective that opens a paragraph's closing sentence (このように, 以上の
  ように) is cut only where the sentence still reads as the conclusion
  without it. That file runs to about 45 KB, so read
  the section once, before ruling on the lane, from its heading to the next
  `## ` heading. The lane's antithesis detector counts `ではなく` and
  `だけでなく…も` across the document, fires at three occurrences, and sets the
  severity by their share of all sentences.
- The reading-load lane (`--reading-load`): a sentence over 90 characters, a
  buried enumeration, a kanji run, a double negative, a chain of の. From
  natural-japanese 1.6.4 it also flags a sentence inside parentheses
  (`sentence_in_paren`). Judge each
  hit against the nine checks of 「読みやすさの点検」 in §5 of the same file,
  read once and applied in order from the first. A split sentence that grows
  longer is a correct result.

Three more pieces of natural-japanese come in here.

- **The naturalness score.** From the JSON, count the AI-smell findings by
  severity and apply the formula and bands from natural-japanese's
  `references/diagnose.md` (by coji). This skill leaves the reading-load lane
  out of the count. Deduction = (critical×8 + warn×4 + info×0.5) ×
  (1000 / max(characters, 1000)); score = max(100 − deduction, 20). The bands
  are 90+ natural, 70–89 light, 50–69 needs work, under 50 heavy. Put the score
  and the band at the head of the report as a one-line summary, and say that it
  is the quick tier of that skill's diagnosis, with no judgement adjustment.
  The score varies between runs, so read it as a direction.
  Under 100 characters of body the score is skipped.
- **The skeleton.** For a document with headings and over about 3,000
  characters, run `prose-lint-run uv run {NJ}/outline.py <file>` and read the headings and
  paragraph leads it prints in one pass. Check three things: the line of
  argument follows from the headings alone, each heading states a message, and
  no two sections repeat one template. Those findings join the ledger.
- **The second run.** It runs with the second read (end of "Writing a fix"),
  after the fixes are applied: lint.py again with the same options plus
  `--baseline <tmp>/nj-1.json`, into `<tmp>/nj-2.json`, read through the
  second command above with `<tmp>/nj-2.json` as its argument. Keep `--json`:
  the text output ends with the paragraph worksheet and asks for every
  paragraph to be written out. lint.py sorts findings into resolved, new and
  persisting; a `new` finding is a fix that introduced a fresh smell, and it
  goes into the final pass. The report states the three counts.

### 公用文 morphology lint

```
prose-lint-run uv run {SKILL_DIR}/scripts/koyobun.py <file>
```

This script checks rules that turn on parts of speech, which no surface-string
linter sees. Four come from 「公用文作成の考え方」 (文化審議会建議, 2022-01-07,
https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/93650001_01.html);
the rules below paraphrase its items. Five are house rules of this skill,
marked as such, and five more, below them, read table headers and slide titles;
each names the source it leans on where it has one. It tokenises
with sudachipy, on the same sentence split and Markdown mask lint.py uses, and
reports one line per suspicion. Each id carries its rule and its ruling:

- `passive` (Ⅲ-3 ケ, use the passive sparingly): れる/られる after a verb. The
  form is shared with 可能, 尊敬 and 自発, so read each hit. Rewrite when the
  agent is known and the active sentence reads naturally; keep a passive whose
  agent is unknown or beside the point.
- `clause_chain` (Ⅲ-3 カ, avoid long chains of conjunctive particles and
  continuative forms): three or more 接続助詞 or 連用中止 in one sentence; the
  threshold of three is this skill's. Read each hit. A sentence whose clauses
  follow one line of thought in order, and that reads in one pass, stays. One
  that changes topic part-way is split at that joint, and the tie the joint
  carried goes into the new sentence as its opening word (このうち、 そのため、
  しかし). The 建議's own rewrites do both: 「このうち、中長期的に在留する人が
  増えている。」 opens the second sentence of its split, and its rewrite under
  カ still holds 「意見が多く、…検討が進んだ。」 and a contrastive が.
- `comma_chain` (house rule, after Ⅲ-3 カ): two or more 読点 in one sentence
  that each close a clause, after a 接続助詞 or a 連用中止
  (「要件を確認し、設計を進めて、実装に着手する」). 「，」 and 「,」 count as
  読点; について、 に対して、 として、 and their kin work as particles and
  stay out of the count, as does a 読点 after a topic, a conjunction or an
  item of a noun list. Ruled as `clause_chain` is: split where the topic
  changes and carry the tie over, set parallel clauses out as a list, and
  keep a sentence that tells a sequence or a cause in one pass. A sentence
  per clause, each ending alike, is the flat text `flow.py` reports. A hit
  inside a quotation stays.
- `kanji_suru` (Ⅱ-8, limit verbs made of one kanji and する): a verb of that
  shape. The 建議 gives 模する, 擬する, 賭する and 滅する as examples. Its
  rewrites are 似せる, なぞらえる, 賭ける and 滅ぼす. This skill exempts 関する,
  対する and 際する, which work as particles. Rewrite with a native verb or a
  two-kanji compound; a legal term of art stays. So does a verb in everyday
  written use whose two-kanji rendering would be the stiffer word, such as
  適する, 反する, 属する, 要する, 有する and 達する; the list is this skill's.
  The check fired on 相反する and 適している in an award-winning paper.
- `etc` (Ⅱ-5 イ, use 等 and など with care): every occurrence. The 建議 asks
  the writer to have the full content in mind and to put representative,
  typical items before 「等」「など」; check that each occurrence does.
- `ga_conjunction` (house rule, after Ⅲ-3 カ): every が used as a 接続助詞,
  with the words before it. The 建議 asks the writer not to overuse 接続助詞. Some が join two clauses with no contrast, as in 「説明しますが、」 or
  「検討したが、」 before a result; cut each of those into two sentences, or
  rewrite it with ので or ため. A が that marks a real
  contrast or a concession stays, and the report says so: 「費用は増えませんが、
  属人化は残ります」 says in one sentence what two would leave the reader to
  join.
- `sasete_itadaku` (house rule, after Ⅱ-6 ウ): させていただく. The 建議 asks
  for 敬語 to be used as needed and not piled up; させていただく asks the reader's
  leave, so it stays only where leave is being asked. Elsewhere write します or
  いたします.
- `nominal_ending` (house rule: 体言止め only in headings and list items, after
  JTF 日本語標準スタイルガイド 1.1.2 and 1.1.3): a body sentence whose last content
  word is a noun. Headings, list items, tables and quotes are masked, so every
  hit is in running text; finish the sentence with a predicate. A label before
  a colon or a table-like paragraph laid out on purpose stays. In a deck
  extract the script reads the `- ` items as body text for the other checks,
  and this one stays silent on them.
- `negated_predicate` (house rule: say what a thing is): the final predicate
  carries ない, ぬ or ません. This is the mechanised form of the second reading
  the register section asks for.

Five more ids read what the checks above mask: the header row of each Markdown
table, and the titles of a deck extract from Step 1. The reader's section 3.5
questions cover the cases these leave out. No false-positive rate has been
measured on labelled documents for these five; rule on each hit before
rewriting.

- `table_deixis` (after the Microsoft and WordPress style guides on table
  headers): a column header that opens with a demonstrative or a referring
  word, such as その, これ, 上記, 当該 or 同. A header names its column on its
  own, since a cell is read by its header. Rewrite with the noun the word points
  at. その他 as a category, and これまで and これから as times, stay.
- `table_particle` (same grounds): a column header that ends in が, を, に or の
  and runs on into its cells. End it with the noun for what the column holds.
- `title_symbol` (after 「公用文作成の考え方」 Ⅲ-2 on 標題): a slide title with no
  Japanese word, no Latin word of four letters and no lower-case word of three,
  such as a matrix symbol or an abbreviation alone; the thresholds are this
  skill's. Name the subject in words; the symbol may follow.
- `title_lines` (after Garner and Alley 2013, two-line headlines, and the 建議's
  one-line 標題): a slide title over two lines in the extract. Keep the subject
  and the point in the title and move the rest to the body. The formal name of
  a report on its cover stays, since the writer cannot change it; this
  exception is this skill's.
- `title_only` (after the 建議's 主題と文書の性格): a slide that holds only its
  title and at most a page number, where the title is a sentence (a 読点, or a
  predicate at its end) with no word for its role from this skill's list (課題,
  例題, 問題, 目標, まとめ, 要点, 目次, 結論) and no line of thanks. A picture,
  a chart or a table on the slide counts as its body, so a sentence headline
  over a figure stays. State the role, or move the sentence to the body and put
  its point in the title. A section slide titled with a noun phrase stays out
  of the check.

`--json` gives the same findings for the ledger.

### Flow

```
prose-lint-run uv run {SKILL_DIR}/scripts/flow.py <file>
```

For a deck, `<file>` is `<tmp>/deck.md`. This layer counts what the others
leave out of the ledger: how the body sentences end, how they join, and how
their lengths vary. A list item that holds two or more sentences, or one
sentence of 60 characters or more, is read as a paragraph; the other layers
mask it. `{SKILL_DIR}/references/flow-japanese.md` gives the
grounds and the measurements. The script prints a profile and two kinds of
passage:

- `ending_run`: three or more sentences in a row, in one paragraph, with the
  same final form (ます, でした, である). Read the paragraph. Where the
  sentences differ in kind (a fact, its reason, a judgement, a request) and
  the endings hide it, each takes the ending of what it is, as section 2.1 of
  the reference lists them, inside the style's 文体. A list of steps or of
  measured values is uniform by nature and stays. No rewrite adds a 体言止め,
  a question or a second 文体 to break a run.
- `lone_run`: three or more sentences in a row with no opening connective,
  no demonstrative and no clause joint. Read the paragraph. Where the text
  itself states the cause, the contrast, the condition or the order between
  two of them, join them: one sentence with ので, が or と, or an opening
  word (そのため、 しかし、 このうち、). Where the relation is a guess, the
  sentences stay apart and the question goes to the author.

The profile's `flat` line marks a document of 12 body sentences or more in
which 40 % or more of the sentences are lone and a sentence holds 0.6 joints
or fewer. Put the profile in the report beside the naturalness score, which
reads none of this. The reader's `flow-` findings cover the same ground by
reading, and the two are ruled together, paragraph by paragraph. Every flow
fix is made of what the text already says.

Two cases make this layer lead the run: the document is marked `flat`, or the
request is about how the text reads as a whole (無機質, 硬い, ぶつ切り,
つながり, 流れ). Then the runs the script lists are a starting point only.
Read every paragraph and every list item of two or more sentences against the
questions of section 3 of the reference, in the main context as well as in the
reader, and rule on each: a rewrite of the paragraph, or the reason it stays
as it is, such as a list of independent facts. A document still marked `flat`
after the fixes is reported as such, with the paragraphs that stayed and why.

A tie is added only where the text fixes the relation, in the clause form
first (が, ので, ため, と) and as an opening word second. natural-japanese's
guide forbids adding しかし and そのため between sentences; where the two meet,
section 3 of the reference says how this layer rules, and the report lists
every tie a fix added. A が or a ので that a flow fix writes shows up in the
second pass as `ga_conjunction`, and a joined sentence can pass 90
characters; each is kept under those rules as a contrast, or as a sentence
that reads in one pass.

### Norm

```
prose-lint-run uv run {SKILL_DIR}/scripts/norm.py <file>
```

For a deck, `<file>` is `<tmp>/deck.md`. Every layer above names a form to
take out, so a text can clear them all by leaving ordinary Japanese out: the
が and ので that join clauses, the connective that opens a sentence, the
demonstrative, the passive, the verb made of a noun and する. This layer
counts those forms with sudachipy and lays each rate beside the same rate in
a baseline of human-written text. The shipped baseline,
`assets/norm-baseline.json`, was counted from the 1,405 articles of Japanese
Wikinews (CC BY 4.0) that run to 10 sentences or more. It holds rates and no
text.

Six rates are marked, each on the side a text moves to when those forms are
left out: `joints`, `glue` (conjunctive が, opening connectives and
demonstratives together), `sahen` and `length` when they fall under the value
95 % of the baseline documents reach, `negative_end` and `colon` when they
pass the value 95 % of them stay under. Two or more marks make the text
`off`. Measured for 1.12.0 with a baseline built from half of those articles:
4.9 % of the 695 articles held out were marked `off`, 4.6 % of 109 science
news articles edited by a public agency, 1.7 % of 59 sections of a government
white paper, none of 27 human-written business and technical documents, and
93.9 % of 297 replies Claude wrote under this plugin's hooks. Web news
written in short sentences sits further from the baseline: 27.3 % of 982
articles of the livedoor news corpus were marked. In those replies が joined
clauses 6 times in 1,000 sentences, where news text holds 81 to 94.

A text marked `off` is read again by paragraph, with the flow layer's
questions: join what the text itself relates, receive the sentence before
with この or その where it is the topic, write the verb the field writes
(確認する, 修正する), and let a passive stand where the agent is unknown or
beside the point. Every such fix is made of what the text already says. A
list of steps or of measured values is short and unjoined by nature and
stays. A document under 10 sentences gets its rates and no marks.

To hold a text to another standard, build a baseline from documents you hold,
one document a file:

```
prose-lint-run uv run {SKILL_DIR}/scripts/norm.py --build {HOME}/norm-baseline.json --name "<label>" [--plain] <folder>
```

`{HOME}/norm-baseline.json`, or the file `$PROSE_LINT_NORM_BASELINE` names,
then takes the shipped baseline's place. A folder of NHK or newspaper
articles the user saved, or newspaper data licensed for research, makes the
baseline the user's own standard; 20 documents of 10 sentences or more are
the least a baseline takes.

### Academic mode

Only in academic mode. Read `{SKILL_DIR}/references/academic-japanese.md` first:
it gives each rule, the passage it rests on and the sources' disagreements. Then
run:

```
prose-lint-run uv run {SKILL_DIR}/scripts/register.py --academic <file>
prose-lint-run uv run {SKILL_DIR}/scripts/koyobun.py --academic <file>
```

The academic register is `$PROSE_LINT_ACADEMIC_REGISTER`, else
`{HOME}/academic.md`, else `assets/academic.sample.md`. Its rows fall in seven
groups; the Why of each hit ends with the sources in 〔〕, which the report
keeps.

- Fixed - six groups:
  - 文体と文末: です・ます、だ、じゃ、んだ、ちゃう、？！
  - 接続の言葉: でも、けど、それで、正直
  - 程度と量の副詞: すごく、ちょっと、いっぱい、全然、多分、一番
  - 指示の言葉と名詞: こんな、とか、みたい、私、今回は、卒論
  - 述語と判断の示し方: と思う、と考えた、てみた、ないといけない、ないで、図を見ると
  - 文語調: ごとく、べく、するべき

  Rewrite each with the row's Instead, in the words of the text around it. A
  hit inside a quotation, a term of art or a corpus example stays, with that
  reason.
- Advisory - 判断が要る言い方, eight rows:
  - 文中の なので/だから
  - とても
  - 完全に/必ず
  - と思われる
  - ことが分かる
  - することができる
  - を行う
  - しかしながら

  The sources split on these or keep them in some uses; section 3 of the
  reference says how to rule. Fix the ones that hold and say why the others
  stay.

`koyobun.py --academic` adds two ids to the fourteen above: `tte` (って as a
particle) and `tara` (the conditional たら/だら), both fixed. Rewrite って as
は, とは or と/という, and たら as と, ば or 場合.

Academic mode changes these rulings in the other layers:

- `passive`: 「と考えられる」「と思われる」「と見られる」 are 自発 and stay; they
  are the forms the register itself recommends.
- The general register's breadth row (様々な): the academic rows give 様々な
  and 種々の as the written form of いろんな. List the items when the text can;
  otherwise the word stays, with that reason. A paper's statement of its
  contribution keeps に寄与 when it names what changes.
- `ja-no-weak-phrase` on かもしれない and the kana rules: as section 3 and 4
  of the reference say. A journal's author guide, when the user names one, wins
  over every rule here, punctuation and kana included.

Raise the register and keep the prose plain. Use the plainest written form
the row offers. Keep the text's native verbs unless the kanji verb is more
precise, and write において, それゆえ and よって only where the sentence needs
them (reference, section 2). The
`academic` group of the exemplars shows the level to aim at.

### The review

Review the text from the read that settled the style in Step 2, for the
points that need a reader: each paragraph serves the document's purpose, terms
stay the same from start to end, and the conclusion comes first. A term is a
word the field or the document defines. Where the document writes one term
two ways, the form it uses more often stays; the style's word column governs
the words a rewrite brings in.

In academic mode, read also for the points of the reference's sections 1.3 to
1.6 and 2 that need a reader:

- fact and judgement kept apart, with the ground of each judgement given and
  another author's view attributed;
- claims measured by numbers, with the writer's own result stated without
  praise;
- each demonstrative with a named referent, and one term per concept;
- methods and results in the past tense, and discussion in the present;
- において, のである and the stiff connectives used where a sentence needs
  them; a paragraph that leans on them gets thinned.

### Writing a fix

The unit of a fix is the paragraph. Before rewriting a sentence, read its
paragraph and note three things the rewrite keeps, from section 2 of
`{SKILL_DIR}/references/flow-japanese.md`:

- what the sentence is: a fact, a reason, a judgement, a request or a limit,
  and how sure the text is of it. The rewrite ends in the same kind. A hedge
  that says how far the evidence goes stays a hedge, and a plain statement
  stays plain;
- how it joins its neighbours: the が, ので or ため it holds, the connective
  or the demonstrative it opens with, the subject it leaves to the sentence
  before. A sentence cut in two keeps the tie as the opening word of the
  second (このうち、 そのため、 しかし); a stock connective that closed a
  paragraph is cut only where the paragraph still reads as closed;
- its place in the paragraph: the long sentence that carries the point stays
  the long one, and a ground stays a clause of the sentence it supports.

Change what the finding names and leave the other words as they are. A plain
word that reads well stays; one term per concept applies to terms, and two
ordinary verbs for one act are no finding. No rewrite, in any layer, brings in
a fact, a plan, a promise or an opinion the text lacks. Where the fix would
need one, the sentence stays and the question goes in the report.

Every rewrite, from any layer, is written to the style from Step 2:

1. Settle what the sentence asserts and who acts in it: a person, or the program
   doing what a program does. A state is written as a state. Then build the
   sentence from that in Japanese order. Swapping one word inside an English
   frame leaves the frame.
2. Take each word from the first source that has it: the term the document
   already uses for the same thing; the reader's field term in the form the
   field writes it; a plain word whose dictionary entry lists the sense you
   mean. Look up each content word the rewrite brings in, unless the document
   already uses it in the same sense, in Weblio 国語辞書
   (`https://www.weblio.jp/content/<word>`), and confirm the sense before
   using it. One lookup per word serves the whole run.
3. End the sentence in the style's 文体.
4. Read the rewrite with the sentence before and after it: the topic carries
   on, the connective still holds, and the term matches the one the document
   uses for the same thing.
5. A row's `Instead` and the reference's before/after pairs give the
   direction. The exemplar groups that section 0 of
   `references/exemplars-japanese.md` names for the style give the frame: how
   their sentences open and end, which words they choose, and how they join.
   Read those groups once per run, before the first rewrite. The words come from the
   text around the hit. One replacement pasted at every hit is a template, and
   a template reads as translation.

Apply the fixes in one pass once every hit is ruled: one Edit per paragraph
that contains a fix. A paragraph with two or more fixes, or with a sentence
split or joined, is written again as a whole and read once from its first
sentence to its last before the Edit. Each Edit can set off the session's write hooks, so one
Edit per hit multiplies their output by the number of hits.

Once the fixes are in, run the flow check against the copy from before the
first Edit:

```
prose-lint-run uv run {SKILL_DIR}/scripts/flow.py --before <tmp>/original.md <file>
```

It prints each figure for both texts and marks the ones that moved `flatter`:
more sentences, shorter ones, more plain endings, fewer joints. For each mark,
find the rewrites behind it and lay each beside its paragraph in
`<tmp>/original.md`. A rewrite that dropped a tie, turned a judgement into a
bare statement, or cut one thought into sentences that end alike is corrected
in the final pass from the original's own words. A mark that the fixes had to
cause, such as a 190-character sentence split at its change of topic, stays,
with that reason. The script also lists the `ending_run` and `lone_run`
passages of the fixed file; rule on those that hold a rewritten sentence.

Then run natural-japanese's second run and launch the
reader once more, fresh, on the fixed file. The reader's prompt carries the
first read's items with the scope narrowed: the line ranges of the paragraphs
that contain a rewritten sentence, the line of each rewritten sentence, "read
only these ranges, with offset and limit", and "report on the sentences at
those lines only", and "ask the questions of section 3 of the flow
reference, `flow-cut` included, of each paragraph in these ranges". Merge
ranges under 10 lines apart; once they cover half the
file, drop the ranges and let the reader read the file in full. The prompt
still withholds the original wording and the reason for each change. Rule on
both results together and apply what holds in one final pass; that pass
closes the run.

## Step 3b - English

Settle the style first, as in Step 2: what the document is, who reads it and
where its words come from. State it in one line at the head of the report
(`style: technical - a README, read by developers`). Then the reader, the
mechanical layers and the review. Fix once all are in, one Edit per paragraph
that contains a fix, as in "Writing a fix".

### The reader

Launch one agent, `model: opus`, in a fresh context, in the background, before
the mechanical layers. Its prompt carries:

- the purpose in one line: find every English sentence of one document that
  fails in meaning or carries the shape of a Japanese draft, and propose a
  rewrite for each;
- the document's absolute path and the style line;
- the absolute path of `{SKILL_DIR}/references/english-reader.md`, with "read it
  first, answer its sentence checks for every sentence and its title and table
  checks for every heading, slide title and table";
- the output shape, one finding per line:
  `<line> | <check id> | "<sentence>" | <rewrite> | <reason>`, the reason in one
  sentence;
- "report every finding, no severity filter";
- the scope: what vale reports belongs to the other layers, and a verbatim
  quotation is left as it stands.

It withholds who wrote the text, the task it served and the lint results. After
the fixes, launch it once more over the paragraphs that changed, as the Japanese
reader's second read does, and rule on what it returns in one final pass.

### textlint

```
prose-lint-run {HOME}/textlint/node_modules/.bin/textlint --config {HOME}/textlint/.textlintrc.en.json <file>
```

For a deck, `<file>` is `<tmp>/deck-flat.md` from Step 1, as in Step 3a. The
English config covers duplicated conjunctions at the start of consecutive
sentences and two Markdown-shape rules of the AI-writing preset. `no-ai-list-formatting`
reports a bullet that opens with a bold label and a colon, and an emoji
bullet. `no-ai-emphasis-patterns` reports bold inside a heading, and an emoji
before a bold label. Those two report in Japanese; restate the finding in
English in the report. All of these are fixed when they hold.

### vale

```
prose-lint-run vale --config {HOME}/vale/.vale.ini <file>
```

vale stops with E201 on front matter whose YAML is invalid, and it lints nothing.
On E201, blank the front matter and pipe the text in:

```
prose-lint-run uv run {SKILL_DIR}/scripts/register.py --blank-front-matter <file> | prose-lint-run vale --config {HOME}/vale/.vale.ini --ext=.md
```

Four styles run:

- proselint: clichés, redundancy, corporate speak, jargon and hedging, plus
  vale's own `Vale.Repetition` for a word typed twice.
- `ai-tells` (https://github.com/tbhb/vale-ai-tells): the signs of LLM-written
  English.
- `AISigns`: three house rules shipped in `assets/vale/styles/AISigns` for
  what ai-tells leaves out. `AISigns.Chatbot` reports the model talking about
  itself or a token pasted from a chat interface. `AISigns.Emoji` reports an
  emoji in a heading or list item. `AISigns.CommaCount` reports five or more
  commas in one sentence.
- `JaEnglish`: two house rules shipped in `assets/vale/styles/JaEnglish` for
  English shaped by a Japanese draft. `JaEnglish.Wasei` reports "hearing" for a
  client interview; a public hearing and hearing loss stay.
  `JaEnglish.InferenceNoun` reports "is inference" for "we infer". Each rule's
  hits on real reports were defects, and neither fired on the 33,000 words of
  human documentation measured.

vale exits 1 on any finding. Every ai-tells rule is `error`, so the tier comes
from the message's opening words, which name the family:

- Fixed - the families that name a stock phrase, a filler or a chat artefact:
  - `AI closing`
  - `AI opening`
  - `AI conclusion`
  - `AI vague attribution`
  - `AI copula dodge`
  - `AI participial padding`
  - `AI overused word`
  - `AI vocabulary`
  - `AI cliché`
  - `AI puffery`
  - every `AI ... heading`
  - `AI structure announcement`
  - `AI quantity metaphor`
  - `AI list intro`
  - `AI label-and-explain`
  - `AI sequencing`
  - `AI contrast`
  - `AI contrast by negation`
  - `AI strawman contrast`
  - `AI stilted negation`
  - `AI stacked absence`
  - `AI negated subject`
  - `AI evasion`
  - `AI strategy buzzword`
  - `AI adjective-noun pair`
  - `AI affirmation`
  - `AI colloquial assessment`
  - `AI cross-reference`
  - `AI defensive hedge`
  - `AI despite-formula`
  - `AI explainer prompt`
  - `AI false exclusivity`
  - `AI filler`
  - `AI fingerprint`
  - `AI hollow acknowledgment`
  - `AI inevitability`
  - `AI narrative pivot`
  - `AI overreach`
  - `AI urgency`
  - `AISigns.Chatbot`
  - `AISigns.Emoji`

  Fix them; a hit inside a quotation or on a term of art stays, with that
  reason.
- Advisory - the families that name a figure of speech, a sentence frame, a
  rhythm or a punctuation mark, which human writers also use:
  - `AI overused verb` (the Figurative rules)
  - `AI hedge` and `AI stacked hedge`: both fired more often on human
    documentation than on model output
  - `JaEnglish.Wasei` and `JaEnglish.InferenceNoun`
  - every `AI ... metaphor`
  - `AI figurative noun`
  - `AI punctuation`: an em dash is a sign only when a paragraph holds three
    or more
  - `AI tricolon`
  - `AI staccato`
  - `AI noun string`
  - `AI numbered lead-in`
  - `AI rhetoric`
  - `AI rhetorical self-answer`
  - `AI mic-drop`
  - `AI pseudo-cleft`
  - `AI anthropomorphism`
  - `AI anthropomorphic adjective`
  - `AI abstraction subject`
  - `AI anaphora`
  - `AI blanket claim`
  - `AI consequence clause`
  - `AI consequence tail`
  - `AI designation adjective`
  - `AI designation verb`
  - `AI explainer lead`
  - `AI idiom`
  - `AI incomplete comparison`
  - `AI nominalization`
  - `AI point verdict`
  - `AI quantified reveal`
  - `AI regime opener`
  - `AI scope partition`
  - `AI shell noun`
  - `AI summative appositive`
  - `AI totality claim`
  - `AI upkeep frame`
  - `AI value verdict`
  - proselint
  - `AISigns.CommaCount`: the rule counts, because no published rule reads
    English clause structure. Split a sentence that strings clauses on commas,
    and set a list of six or more items out as a list or keep it. A comma
    splice with one or two commas passes the count, so the review below reads
    for it.

  Fix the ones that hold and say why the others stay.

Two ai-tells rules that police one project's own wording (`HouseStyle`,
`ShipOveruse`) are switched off in the shipped `.vale.ini`, and so are eleven
whose hits on the Go blog and the Rust book were sound sentences: the
families `AI transition`, `AI formalism`, `AI empty modifier`,
`AI restatement`, `AI metacommentary`, `AI sycophancy`, `AI intensifier`,
`AI possession verb` and `AI emphasis`, and the colon rule of
`AI punctuation`.

### The register

Run `register.py` on the file. Its English negation row is the only linter
that carries the rule on definition by negation; the Japanese rows find nothing
in English text. Rewrite each hit the same way as in Step 3a.

### The review

With the `elements-of-style:writing-clearly-and-concisely` skill installed
(https://github.com/obra/the-elements-of-style), invoke it for the judgement
layer; without it, read for needless words, passive voice that hides the actor,
and vague nouns yourself. Then read once for the signs that need a reader:

- clauses joined by a comma alone (a comma splice, which the comma count
  passes at one or two commas)
- three items where two or four were the truth
- a paragraph that opens with a claim and closes with its restatement
- headings that all take the same shape
- a document that agrees with the reader
- a synonym cycled to avoid repeating a name

## Step 3c - translation

Run this step when the request hands over a source and its translation, or asks
for a translation. With a source alone, write the translation first, then
continue here. It covers English to Japanese and Japanese to English.

Before translating, write the glossary beside the target as
`<target>.glossary.tsv`: source term, tab, target term, one row per term the
document repeats. A term the document already renders one way keeps that
rendering.

1. Compare by script:

   ```
   prose-lint-run uv run {SKILL_DIR}/scripts/pair_check.py <source> <target> --glossary <target>.glossary.tsv
   ```

   Each line is a suspicion: a number that differs in a section, a glossary term
   missing there, source-language text left in the target, or a heading left in
   the source language. A run with no glossary skips that kind; say so in the
   report.
2. Launch one agent, `model: opus`, in a fresh context. Its prompt carries the
   purpose in one line (compare one translation with its source and report each
   difference in meaning), the absolute paths of the source and the target, the
   glossary when there is one, the absolute path of
   `{SKILL_DIR}/references/translation-check.md` with "read it first, ask its
   questions of every section and use its output line", "report every finding,
   no severity filter", and English as the output language with quoted text
   verbatim. It withholds who translated the text, the task and the script's
   findings.
3. Rule on the script's lines and the agent's findings together, then make one
   rewrite pass over the target, one Edit per paragraph that contains a fix.
   Launch the agent once more over the changed lines only, with the source
   ranges beside them. Correct what it finds and stop: further passes move the
   text toward the rewriter's wording, and the meaning gains nothing.
4. Run Step 3a on a Japanese target and Step 3b on an English one. A rewrite in
   those steps keeps every number, term and qualifier the comparison settled.

## Reporting

- For a translation, open with the counts from Step 3c: the script's lines by
  kind, the agent's findings by id and severity, and what the second read found.
- **Report every finding as fixed, or as kept with a stated reason.** A hit is a
  suspicion, and the reason a wording stays is part of the report.
- **Never rewrite the user's text silently, and never mass-apply the lint
  output.** A run over a long document produces more hits than problems, and
  applying them wholesale flattens prose the user wrote deliberately. `textlint
  --fix` is off the table for the same reason.
- For Japanese, open with the style line, then the naturalness score and its
  band, then one line from `flow.py`: the mean sentence length, the joints
  per sentence, the share of plain endings and of lone sentences, and
  whether the document is marked `flat`. The score counts wordings and reads
  none of this, so a high score beside a `flat` mark means the text is clean
  and reads as a list. Then one line from `norm.py`: the baseline's name,
  the marked rates with their values, and whether the text is `off`, before
  the fixes and after them. In academic mode, add a line under the score: that the run was in
  academic mode and why, and the academic register's hit count before and
  after the fixes. The ledger follows by layer, with the reader's findings as
  one layer; the academic ledger comes after the register's, with each hit's
  sources. For `article` and `slides`, add a line under the score with the
  reader's five-axis score out of 50; stop-ai-slop-jp calls for a rewrite
  under 35. End with the second run's resolved / new / persisting counts,
  the figures `flow.py --before` marked `flatter` with what was corrected or
  why each stays, every tie a flow fix added, the count of body sentences
  changed out of the total by `flow.py`'s count, and
  what the second read of the rewrites returned. A score alone says nothing
  about the register hits, so it never replaces the ledger.
- For English, open with the style line, then one line: the count of ai-tells, `AISigns.Chatbot`
  and `AISigns.Emoji` hits and the count per 1,000 words. Both come from the
  vale run before the fixes: `prose-lint-run vale --output line` piped to a count of lines
  holding `ai-tells`, `AISigns.Chatbot` or `AISigns.Emoji`, over `wc -w`. It
  is a direction, like the naturalness score, and never
  replaces the ledger. After the fixes, run vale again and state the count
  that remains.
- Name every layer that was skipped and the tool it lacked.
- Report in Markdown in the reply.
