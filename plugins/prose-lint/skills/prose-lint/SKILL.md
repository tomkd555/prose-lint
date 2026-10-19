---
name: prose-lint
description: >-
  Runs the wording linters on a file or pasted text and picks the ones the text's language calls for. For Japanese: a style settled first (genre, reader, 文体 and where the words come from, or style=<name> from a calling skill) that every rewrite is written to; a reader in a fresh context that finds translationese from a sourced reference; a register of 13 translationese forms; textlint with the technical-writing, JTF and AI-writing presets, the kana rules of 内閣訓令 and い抜き・さ入れ・フィラー; a register of rejected wordings; natural-japanese's lint with its naturalness score; a sudachipy morphology lint for 公用文作成の考え方 and house rules; and an academic mode for papers, theses and reports. For English: textlint, the register's negation row, and vale with proselint, ai-tells and three house rules. Triggers on 「textlint かけて」「lint して」「lint 回して」「校正して」「表記チェック」「vale かけて」「否定形を消して」「否定で定義した文を直して」「AI っぽさを消して」「論文調にして」「論文向けの表現に直して」「レポートの文体にして」「学術的な表現に」「口語表現を直して」「翻訳調を直して」「直訳っぽい」「翻訳っぽい」「英語の直訳になっている」, "run textlint", "lint this file", "proofread this", "check this English draft", "does this read as AI-written". Use it whenever the user names a linter or asks for a wording check on a document.
---

# Prose lint

Runs the linters over one text on demand, settles which config the text's
language calls for, and rules on every hit. Read `{SKILL_DIR}` below as the
absolute path of this skill's directory, and `{HOME}` as `$PROSE_LINT_HOME`, or
`~/.prose-lint` when that is unset.

## Step 0 - setup

`{HOME}/textlint/node_modules`, `{HOME}/vale/styles/proselint` and
`{HOME}/vale/styles/ai-tells` hold the installed linters. When any is missing,
run once:

```
uv run python {SKILL_DIR}/scripts/setup.py
```

It needs `npm` for textlint and `vale` on PATH for the vale packages, and
reports a missing tool as `skip`. A layer whose tool is missing is reported as
skipped in the final report; the other layers still run. The Japanese
morphology and natural-japanese layers need `uv` and the natural-japanese
plugin (`/plugin marketplace add coji/natural-japanese`, then
`/plugin install natural-japanese@natural-japanese`); `uv run {SKILL_DIR}/scripts/koyobun.py --nj-dir`
prints the directory it found, written `{NJ}` below.

## Step 1 - settle the target

A path in the request is the target. Pasted text goes to a `.md` file in a
temporary directory first, because textlint, vale and the scripts all read
files.

With no path given and no file in play from the conversation, ask which text to
lint.

## Step 2 - route by script

Hiragana over 10% of the non-whitespace body means Japanese, otherwise English:

```
uv run python -c "import re,sys;t=open(sys.argv[1],encoding='utf-8').read();b=len(re.sub(r'\s','',t));print('ja' if len(re.findall('[ぁ-ゟ]',t))*10>b else 'en')" <file>
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

### The reader

The translationese that survives the other layers sits where no regex reaches.
A word gets picked as the dictionary match of an English one: 提供する for
*provide* in 「MWCは製品発表以外にも多くのことを提供する」, where Japanese says
「多くの見どころがある」. A frame gets built in English order:
「この機能はユーザーにデータ出力を可能にします」 for a feature that lets users
export data. The same word is right in its own sense elsewhere, and the
human-written documents the reference measured use the commonest surface forms
too (において in 47 of 83), so the decision needs the sentence and the document
around it.

Launch one agent, `model: opus`, in a fresh context. Its prompt carries:

- the purpose in one line: find every sentence of one Japanese document that
  reads as translated from English, or whose 文体 or words do not fit the
  document's style, and propose a rewrite for each;
- the document's absolute path and the style line from Step 2;
- the absolute path of `{SKILL_DIR}/references/translationese-japanese.md`,
  with "read it first and use its marker ids";
- the absolute path in `$PROSE_LINT_PATTERNS`, when that names a file: the
  user's own notes on wordings they rejected, read after the reference;
- the output shape, one finding per line:
  `<line> | <marker id> | "<sentence>" | <rewrite> | <reason>`, the reason
  in one sentence;
- "report every finding, no severity filter";
- the scope: notation, kana, sentence length and the register's wordings belong
  to the other layers;
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
{HOME}/textlint/node_modules/.bin/textlint --config {HOME}/textlint/.textlintrc.json <file>
```

textlint exits 1 when it finds anything, so read the output and ignore the exit
code. The findings fall in three tiers by rule id:

- Blocking - fix these: `no-ai-hype-expressions`, `ai-tech-writing-guideline`,
  `ja-no-weak-phrase`, `ja-no-redundant-expression`, `ja-no-abusage`,
  `ja-no-successive-word`, `no-doubled-conjunctive-particle-ga`,
  `no-double-negative-ja`, `no-dropping-the-ra`, `@textlint-ja/no-dropping-i`,
  `@textlint-ja/no-insert-dropping-sa`, `@textlint-ja/no-filler`,
  `no-mix-dearu-desumasu`, and the kana rules: `ja-keishikimeishi`,
  `ja-hiragana-hojodoushi`, `ja-hiragana-daimeishi`, `ja-hiragana-fukushi`
  and `prh`. The four hiragana rules and prh together restate 「公用文における
  漢字使用等について」(平成22年内閣訓令第1号) 別紙. prh carries the
  conjunctions, auxiliaries and the fixed phrases of its item キ. Those
  phrases include 但し, 出来る, 様に, 通り and 致します. Each prh message names
  the item it comes from. The fukushi dictionary is the rule's own minus the five words the
  訓令 keeps in kanji (更に, 既に, 最も, 僅か, 若しくは). A kana rule firing on
  a proper noun, a legal term or a quotation is kept, with that reason.
- Advisory - each needs judgement: `no-doubled-joshi`, `no-doubled-conjunction`,
  `sentence-length` (90 characters), `max-ten`, `max-kanji-continuous-len`. A
  particle repeated in a plain list holds; the conjunctive が repeated in one
  sentence gets fixed. Fix the ones that hold and say why the others stay.
- Notation - every other rule: punctuation, spacing, numerals. Leave them alone
  unless the user asks for notation.

### The register

```
uv run {SKILL_DIR}/scripts/register.py <file>
```

The register is a Markdown table of rejected wordings: `$PROSE_LINT_REGISTER`,
else `{HOME}/vocabulary.md`, else the sample in `assets/`. The script prints
which one it read. The sample carries twelve rows in three groups.

- Definition by negation, two rows. The Japanese row on `ではない` also covers
  `でない`, `じゃない`, `に当たらない`, `該当しない` and `非該当`; the English
  row covers `not X but Y`, `X, not Y`, `rather than`, `instead of` and
  `not applicable`. Two forms stay: quoted text, and a verb plainly negated.
  Every other hit gets rewritten: say what the thing is; where the sentence
  draws a boundary, name what falls inside it; where it corrects a wrong idea,
  state the right one and leave the wrong one out. Write the sentence a
  business document would carry, in the words of the text around it; a
  template sentence reads as translation.
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
  inside a quotation stays.

The regex reaches the surface forms only. The `negated_predicate` id of the
morphology lint below lists every sentence whose final predicate is negated;
read each one and rewrite the ones whose whole content is a denial:
「〜とは限らない」, 「〜するわけがない」, 「〜を含まない」, 「〜せず」 or
「〜しない」 used to define a thing or to draw its boundary, and a clause that
names only what something lacks. The other rows are handled as the register
says: kept when the wording fits the context and the reason is stated, otherwise
rewritten.

### The translationese register

```
uv run {SKILL_DIR}/scripts/register.py --translationese <file>
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

### natural-japanese lint

```
uv run {NJ}/lint.py --genre business --reading-load --json <file> > <tmp>/nj-1.json
uv run python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));d.pop('paragraphs',None);print(json.dumps(d,ensure_ascii=False))" <tmp>/nj-1.json
```

`--genre business` selects natural-japanese's business profile, which mainly
switches off detectors that misfire on bullet-heavy business documents. The JSON goes to a temporary file so it serves twice: it is
the ledger the report rules on, and the baseline for the second run below.
Read it through the second command, which prints it without the `paragraphs`
key. From natural-japanese 1.6.0 that key copies every paragraph of the
document as the worksheet for that skill's own paragraph check, and it makes
up most of the file. Two lanes come out.

- The AI-smell lane: banned phrases and translationese, uniform sentence length,
  the 体言止め rate, paragraph-opening conjunctions and lexical variety. Judge each
  hit by the fix its own message gives and by §3 of natural-japanese's
  `SKILL.md` (「既存の文書を直すとき」). That file runs to about 45 KB, so read
  the section once, before ruling on the lane, from its heading to the next
  `## ` heading. The lane's antithesis detector counts `ではなく` and
  `だけでなく…も` across the document, fires at three occurrences, and sets the
  severity by their share of all sentences.
- The reading-load lane (`--reading-load`): a sentence over 90 characters, a
  buried enumeration, a kanji run, a double negative, a chain of の. Judge each
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
  characters, run `uv run {NJ}/outline.py <file>` and read the headings and
  paragraph leads it prints in one pass: whether the line of argument holds from
  headings alone, whether each heading is a message, and whether sections repeat
  one template. Those findings join the ledger.
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
uv run {SKILL_DIR}/scripts/koyobun.py <file>
```

This script checks rules that turn on parts of speech, which no surface-string
linter sees. Four come from 「公用文作成の考え方」 (文化審議会建議, 2022-01-07,
https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/93650001_01.html);
the rules below paraphrase its items. Six are house rules of this skill,
marked as such, three of them leaning on an item of the 建議. It tokenises
with sudachipy, on the same sentence split and Markdown mask lint.py uses, and
reports one line per suspicion. Each id carries its rule and its ruling:

- `passive` (Ⅲ-3 ケ, use the passive sparingly): れる/られる after a verb. The
  form is shared with 可能, 尊敬 and 自発, so read each hit. Rewrite when the
  agent is known and the active sentence reads naturally; keep a passive whose
  agent is unknown or beside the point.
- `clause_chain` (Ⅲ-3 カ, avoid long chains of conjunctive particles and
  continuative forms): three or more 接続助詞 or 連用中止 in one sentence; the
  threshold of three is this skill's. Split at the joint where the topic
  changes.
- `comma_chain` (house rule, after Ⅲ-3 カ): two or more 読点 in one sentence
  that each close a clause, after a 接続助詞 or a 連用中止
  (「要件を確認し、設計を進めて、実装に着手する」). 「，」 and 「,」 count as
  読点; について、 に対して、 として、 and their kin work as particles and
  stay out of the count, as does a 読点 after a topic, a conjunction or an
  item of a noun list. Fixed: give each clause its own sentence, or a list
  when the clauses are parallel. A hit inside a quotation stays.
- `kanji_suru` (Ⅱ-8, limit verbs made of one kanji and する): a verb of that
  shape. The 建議 gives 模する, 擬する, 賭する and 滅する as examples. Its
  rewrites are 似せる, なぞらえる, 賭ける and 滅ぼす. This skill exempts 関する,
  対する and 際する, which work as particles. Rewrite with a native verb or a
  two-kanji compound; a legal term of art stays.
- `etc` (Ⅱ-5 イ, use 等 and など with care): every occurrence. The 建議 asks
  the writer to have the full content in mind and to put representative,
  typical items before 「等」「など」; check that each occurrence does.
- `ga_conjunction` (house rule, after Ⅲ-3 カ): every が used as a 接続助詞,
  with the words before it. The 建議 asks the writer not to string clauses on
  接続助詞; this check lists each が so that the ones that join two clauses
  with no contrast (「説明しますが、」, 「検討したが、」 before a result) get
  cut into two sentences or rewritten with ので or ため. A が that marks a real
  contrast stays, and the report says so.
- `tari_single` (house rule): a sentence with one たり and no partner.
  Standard usage pairs it (読んだり書いたりする); rewrite with the pair, or
  without たり (読むなどして). A たり that closes a list on purpose stays.
- `sasete_itadaku` (house rule, after Ⅱ-6 ウ): させていただく. The 建議 asks
  for 敬語 to be used as needed and not piled up; させていただく asks the reader's
  leave, so it stays only where leave is being asked. Elsewhere write します or
  いたします.
- `nominal_ending` (house rule: 体言止め only in headings and list items, after
  JTF 日本語標準スタイルガイド 1.1.2 and 1.1.3): a body sentence whose last content
  word is a noun. Headings, list items, tables and quotes are masked, so every
  hit is in running text; finish the sentence with a predicate. A label before
  a colon or a table-like paragraph laid out on purpose stays.
- `negated_predicate` (house rule: say what a thing is): the final predicate
  carries ない, ぬ or ません. This is the mechanised form of the second reading
  the register section asks for.

`--json` gives the same findings for the ledger.

### Academic mode

Only in academic mode. Read `{SKILL_DIR}/references/academic-japanese.md` first:
it gives each rule, the passage it rests on and the sources' disagreements. Then
run:

```
uv run {SKILL_DIR}/scripts/register.py --academic <file>
uv run {SKILL_DIR}/scripts/koyobun.py --academic <file>
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

`koyobun.py --academic` adds two ids to the ten above: `tte` (って as a
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

Raise the register without stiffening it. Use the plainest written form the
row offers; do not turn native verbs into kanji compounds wholesale, add
において, or string それゆえ and よって through a paragraph (reference, section
2).

### The review

Review the text from the read that settled the style in Step 2, for what no
script decides: whether each paragraph serves the document's purpose, whether terms stay consistent from start to end, and
whether the conclusion comes first.

In academic mode, read also for the points of the reference's sections 1.3 to
1.6 and 2 that no regex finds: fact and judgement kept apart, with the ground
of each judgement given and another author's view attributed; claims measured
by numbers, with no praise of one's own result; each demonstrative with a
named referent; one term per concept; methods and results in the past tense
and discussion in the present; no paragraph leaning on において, のである or a
stiff connective in every sentence.

### Writing a fix

Every rewrite, from any layer, is written to the style from Step 2:

1. Settle what the sentence asserts and who acts in it: a person, or the program
   doing what a program does. A state is written as a state. Then build the
   sentence from that in Japanese order. Swapping one word inside an English
   frame leaves the frame.
2. Take each word from the first source that has it: the term the document
   already uses for the same thing; the reader's field term in the form the
   field writes it; a plain word whose dictionary entry lists the sense you
   mean. Look up each content word the rewrite brings in, unless the document
   already uses it for the same thing, in Weblio 国語辞書
   (`https://www.weblio.jp/content/<word>`), and confirm the
   sense before using it. One lookup per word serves the whole run.
3. End the sentence in the style's 文体.
4. Read the rewrite with the sentence before and after it: the topic carries
   on, the connective still holds, and the term matches the one the document
   uses for the same thing.
5. A row's `Instead` and the reference's before/after pairs give the
   direction; the words come from the text around the hit. One replacement
   pasted at every hit is a template, and a template reads as translation.

Apply the fixes in one pass once every hit is ruled: one Edit per paragraph
that contains a fix. Each Edit can set off the session's write hooks, so one
Edit per hit multiplies their output by the number of hits.

Once the fixes are in, run natural-japanese's second run and launch the
reader once more, fresh, on the fixed file. The reader's prompt carries the
first read's items with the scope narrowed: the line ranges of the paragraphs
that contain a rewritten sentence, the line of each rewritten sentence, "read
only these ranges, with offset and limit", and "report on the sentences at
those lines only". Merge ranges under 10 lines apart; once they cover half the
file, drop the ranges and let the reader read the file in full. The prompt
still withholds the original wording and the reason for each change. Rule on
both results together and apply what holds in one final pass; that pass
closes the run.

## Step 3b - English

Three mechanical layers, then the review. Fix once all four are in, one Edit
per paragraph that contains a fix, as in "Writing a fix".

### textlint

```
{HOME}/textlint/node_modules/.bin/textlint --config {HOME}/textlint/.textlintrc.en.json <file>
```

The English config covers write-good, terminology, a 40-word sentence cap and
duplicated conjunctions at the start of consecutive sentences. It also runs
two Markdown-shape rules of the AI-writing preset. `no-ai-list-formatting`
reports a bullet that opens with a bold label and a colon, and an emoji
bullet. `no-ai-emphasis-patterns` reports bold inside a heading, and an emoji
before a bold label. Those two report in Japanese; restate the finding in
English in the report. All of these are fixed when they hold.

### vale

```
vale --config {HOME}/vale/.vale.ini <file>
```

Three styles run:

- proselint: redundancy, corporate speak, jargon and hedging.
- `ai-tells` (https://github.com/tbhb/vale-ai-tells): the signs of LLM-written
  English.
- `AISigns`: three house rules shipped in `assets/vale/styles/AISigns` for
  what ai-tells leaves out. `AISigns.Chatbot` reports the model talking about
  itself or a token pasted from a chat interface. `AISigns.Emoji` reports an
  emoji in a heading or list item. `AISigns.CommaCount` reports five or more
  commas in one sentence.

vale exits 1 on any finding. Every ai-tells rule is `error`, so the tier comes
from the message's opening words, which name the family:

- Fixed - the families that name a stock phrase, a filler or a chat artefact:
  - `AI closing`
  - `AI opening`
  - `AI sycophancy`
  - `AI hedge`
  - `AI stacked hedge`
  - `AI conclusion`
  - `AI vague attribution`
  - `AI copula dodge`
  - `AI participial padding`
  - `AI transition`
  - `AI overused word`
  - `AI vocabulary`
  - `AI cliché`
  - `AI puffery`
  - every `AI ... heading`
  - `AI structure announcement`
  - `AI metacommentary`
  - `AI restatement`
  - `AI empty modifier`
  - `AI intensifier`
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
  - `AI formalism`
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
  - every `AI ... metaphor`
  - `AI figurative noun`
  - `AI punctuation`: an em dash is a sign only when a paragraph holds three
    or more; a capital after a colon is a style choice
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
  - `AI emphasis`
  - `AI explainer lead`
  - `AI idiom`
  - `AI incomplete comparison`
  - `AI nominalization`
  - `AI point verdict`
  - `AI possession verb`
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
`ShipOveruse`) are switched off in the shipped `.vale.ini`.

### The register

Run `register.py` on the file. Its English negation row is the only linter
that carries the rule on definition by negation; the Japanese rows find nothing
in English text. Rewrite each hit the same way as in Step 3a.

### The review

With the `elements-of-style:writing-clearly-and-concisely` skill installed
(https://github.com/obra/the-elements-of-style), invoke it for the judgement
layer; without it, read for needless words, passive voice that hides the actor,
and vague nouns yourself. Then read once for the signs no regex catches:

- clauses joined by a comma alone (a comma splice, which the comma count
  passes at one or two commas)
- three items where two or four were the truth
- a paragraph that opens with a claim and closes with its restatement
- headings that all take the same shape
- a document that agrees with the reader
- a synonym cycled to avoid repeating a name

## Reporting

- **Report every finding as fixed, or as kept with a stated reason.** A hit is a
  suspicion, and the reason a wording stays is part of the report.
- **Never rewrite the user's text silently, and never mass-apply the lint
  output.** A run over a long document produces more hits than problems, and
  applying them wholesale flattens prose the user wrote deliberately. `textlint
  --fix` is off the table for the same reason.
- For Japanese, open with the style line, then the naturalness score and its
  band, then the ledger by layer with the reader's findings as one layer, then
  the second run's resolved / new / persisting counts and what the second read
  of the rewrites returned. In
  academic mode, add a line under the score: that the run was in academic mode
  and why, and the academic register's hit count before and after the fixes;
  the academic ledger comes after the register's, with each hit's sources. A score
  alone says nothing about the register hits, so it never replaces the ledger.
- For English, open with one line: the count of ai-tells, `AISigns.Chatbot`
  and `AISigns.Emoji` hits and the count per 1,000 words. Both come from the
  vale run before the fixes: `vale --output line` piped to a count of lines
  holding `ai-tells`, `AISigns.Chatbot` or `AISigns.Emoji`, over `wc -w`. It
  is a direction, like the naturalness score, and never
  replaces the ledger. After the fixes, run vale again and state the count
  that remains.
- Name every layer that was skipped and the tool it lacked.
- Report in Markdown in the reply.
