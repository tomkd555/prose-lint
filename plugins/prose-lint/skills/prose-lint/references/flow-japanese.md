# How a Japanese text holds together

The material the flow layer and the reader in Step 3a work from. The other
references name wordings to take out. This one names what a paragraph carries
between and around its wordings: the ending that says what a sentence is, the
words that join one sentence to the next, the uneven weight of its sentences,
and the writer's distance from the reader. A rewrite that clears every hit and
drops these leaves a list of bare statements, each correct, which reads as
written by no one.

Section 1 gives the measurements behind that claim. Section 2 names the four
things a text keeps, with the grounds for each. Section 3 holds the questions
the reader asks of every paragraph. Section 4 is the table `scripts/flow.py`
was set on, and section 5 lists the sources. Every source was fetched on
2026-11-11 and each quotation checked against the fetched page or PDF. Each
carries its source's short name in 〔〕, and section 5 gives the URL.

## 1. Why a rewrite goes flat

Measured for 1.11.0, on the skill as it stood at 1.10.0.

1. **The layers flag the sentences the skill holds up as good.** The mechanical
   layers (textlint, the three registers, `koyobun.py`) ran over the 74
   sentences of `exemplars-japanese.md`, one sentence to a paragraph. 45 of
   the 74 drew a hit, and 19 drew one under a rule SKILL.md said to fix. Among
   them: 「互いの言いたいことが…決して珍しいことではありません。」 and
   「コミュニケーションにはいつでも通用するような正解があるわけではない。」 under
   the negation row, 「これは、…可能性を示唆している。」 under
   `ja-no-weak-phrase`, 「…だけを聞いているのではなく，ペンを貸してほしい，
   といった意味でしょう。」 under the negation row, `clause_chain` and
   `comma_chain` together. The reader and natural-japanese's lint were left
   out of this count.
2. **A run moves a human text toward flat.** The 1.10.0 skill ran once over a
   column by 文化庁国語課 from 2014 (ぶんかる 「言葉のQ&A」 001). It rewrote 11
   of the 35 body sentences and split 5 of them in two. `flow.py --before`
   reads the result: 28 profiled sentences became 33, their mean length fell
   from 47.6 characters to 39.6, the joints in a sentence from 1.71 to 1.30,
   and the share of plain endings rose from 60.7 % to 69.7 %. Six of the eight
   figures moved flatter. The run cut 「このように」 as a stock phrase, dropped
   the column's explicit denial 「薄笑いを浮かべているという意味はなく」 for a
   positive sentence that no longer says it, and turned 「…80ポイントで，最も
   差が小さいのは…45ポイントでした。」 into two sentences that both end
   でした. The naturalness score of the untouched column was 99.6.
3. **No layer saw flatness.** A memo Claude drafted with no rule in force
   scored 96.9, "natural"; its body sentences ran 31 characters on average
   and held 0.78 joints each. A report Claude wrote with this plugin's hooks
   on (59 sentences, list items counted) held 0.41 joints a sentence; 59 % of
   its sentences joined nothing around them, and none ended in a judgement or
   a request. The human-written documents of section 4 hold 0.75 to 1.63
   joints a sentence.

The causes, by the stage of a run where each sits:

| Stage | Cause |
| --- | --- |
| The target | "Good" was defined as the absence of hits: the score is 100 minus deductions. The `business` exemplars are a council report's opening, its survey figures and a definition, with no passage in which a writer weighs a choice. |
| Detection | Every rule names a wording to remove or avoid, and each reads one sentence. Nothing reads what a sentence does in its paragraph, and nothing counted joins or endings. |
| The ruling | The default was to fix. A kept hit needs a stated reason and a fix needs none, so the cheaper ruling is the rewrite, and with this many layers most sentences draw some hit. |
| The rewrite | One sentence at a time, each against its own hits. The usual directions are to cut a clause off, state plainly, name the subject and drop the negative: each lowers the count of joins or endings a little. |
| Verification | The second read looked for the same defects in the rewritten sentences. Nothing compared the paragraph before and after. |
| The hooks | The same rules block a write or a reply while Claude drafts, so the draft is shaped by what it must avoid before the skill ever runs. |

## 2. What a text keeps

### 2.1 The ending says what the sentence is

A Japanese sentence states its content and then, at its end, how the writer
holds that content. A paragraph of human prose mixes kinds of sentence, and
its endings differ because the kinds differ. `flow.py` sorts endings into
these classes:

| A sentence that | Ends in (敬体 in parentheses) | `flow.py` class |
| --- | --- | --- |
| reports a fact or an act | する, した, である, ている (します, しました, です) | `plain` |
| gives the reason or the meaning of what came before | のである, ためである, からだ, わけだ (のです, ためです) | `explain` |
| judges, or says how far the evidence goes | だろう, と考えられる, といえる, かもしれない, はずだ, 可能性がある, 見込みである (でしょう, と考えられます) | `judge` |
| asks, advises or commits | べきである, とよい, たい, てほしい, 必要がある, なければならない (てください, ましょう, お願いします) | `stance` |
| denies or limits | ない, わけではない, とは限らない (ません) | `negative` |
| puts the reader's question | か, だろうか (でしょうか) | `question` |

The 建議 treats the ending as the writer's stance toward the reader:
「文末を「です・ます」にするのは柔らかい表現によって読み手に対して丁寧さと
親しさを示すためであり」 〔公用文〕 Ⅲ-1. It uses the range itself: its own
sentences end 「…と考えられる。」, 「…意識するとよい。」, 「…念頭に置きたい。」
and 「…用いてよい。」 beside the plain である. It also grants the form that
shows a view as a view: 「「○○とされている」と書くと、主張や意見を客観的に
見せることができる。」 〔公用文〕 Ⅲ-3 ケ.

A university writing guide gives each ending its job. 「「である」や「であった」
は単なる断定です」; のである is used, among other times, 「それまで述べてきた
ことをまとめて結論的に言うとき」, and 「乱用すると押しつけがましい感じを
与えます。」 Of と考えられる it says the form shows that a statement is
「「合理的な判断に基づく結論」であることを明示できます。」 〔立教〕 So an
ending is chosen for what the sentence does, and のである is rationed.

Readers judge by this. In a study where people tried to tell Japanese written
by seven language models from human Japanese, "participants primarily relied
on superficial impressions based on phraseology, expression, the ends of
words, conjunctions, and punctuation marks in judgments" 〔Zaitsu2025〕. An
undergraduate thesis on a small sample of opinion essays reports the
difference itself: 「AI 生成文では出現回数が多い文末表現が偏っているのに対し、
人間執筆文ではある程度ばらつきがあるということがわかった。」 and
「個人の意見と言うより一般的な見解を述べる傾向があるのがAI 生成文の特徴で
あるといえるだろう。」 〔大西〕

The form of a judgement depends on the style. `academic` writes と考えられる
and といえる and leaves だろう and と思う out, as
`references/academic-japanese.md` sets out; `business` and `article` take the
whole range in their 文体.

In the columns of section 4, 45 % to 70 % of the sentences end plain, and in
12 of the 14 between 7.8 % and 16.7 % end in a judgement. The passage of exemplar 4.3 climbs
from ようです through のかもしれません and と考えられます to こともあるでしょう
in six sentences, and each step says how sure the writer is.

What follows for a rewrite:

- The ending follows the kind of sentence. A fact the writer checked ends
  plain. A cause the writer infers ends in と考えられる or だろう. A request
  ends as a request.
- A rewrite keeps the class of the sentence it rewrites. 「〜と考えられる」
  turned into 「〜である」 is a new claim, and natural-japanese's guide forbids
  it for the same reason (its §2, principle 10).
- A run of one ending over sentences of different kinds is the finding. A run
  over sentences of one kind, such as steps or measured values, is the
  content's own shape.
- Variety for its own sake is no fix. A 体言止め, a question or a second 文体
  put in to break a run is a device, and natural-japanese's principle 8 rules
  it out.

### 2.2 Sentences are joined

A reader takes two sentences as related, and the text either says how or
leaves the reader to guess. Japanese says it in four ways: a 接続助詞 or a
連用中止 inside the sentence (ので, が, と, ば, て, 〜し、), a connective at its
head (しかし, そのため, また, 例えば), a demonstrative that points back (この,
その, これ, こうした), and a subject left out because the last sentence gave
it.

The 建議 asks a writer to hold these back from excess, and keeps them in its
own rewrites. Under 「一文の論点は、一つにする」 it splits a sentence and opens
the second half with a tie: 「在留外国人数は、約200万人を超えている。このうち、
中長期的に在留する人が増えている。」 Under 「接続助詞や中止法を多用しない」
its rewrite still holds 「これに対しては、時期尚早との意見が多く、差し戻すべきで
あるとの方向で検討が進んだ。そのまま決定するかと思われたが、反論も出され…」:
two joints in the first sentence and a contrastive が in the second. Its
instruction for a long sentence names the connective as the tool:
「長い文は、句点や接続詞を使い、また長い修飾語・修飾節を別文に移すなどして
複数の文に区切る。」 〔公用文〕 Ⅲ-3 ア, イ, カ.

The council's 2018 report gives the same pair of acts, cut and then join:
「余計な情報を落として一文を簡潔にし，接続詞等で結ぶことによって，より意味の
取りやすい言い方を工夫できます。」 〔分かり合う〕 p. 43. A reading experiment
states what a connective does: 「接続詞には後文が前文に対して持っている接続
関係を読み手に予告する機能がある」, a view it reports from earlier linguists,
and finds the cost of leaving one out highest for contrast and for cause:
"Without these connectives, the inter-sentential situations may impose much
information processing load on readers" 〔伊藤1991〕. natural-japanese's guide
makes the point from the other side: a list of items loses 「だから」 and
「しかし」, and the reader has to supply them (its §2, principle 3).

Most joins sit inside the sentence, and a connective heads a minority of
sentences. 石黒 counted the sentences that open with one: 25.5 % in papers,
13.3 % in essays, 12.2 % in newspaper editorials, and concludes
「書き言葉ではせいぜい10％前後、もっとも多い論文でも全体の４分の１にしか
接続詞はつきません。」 〔石黒2009〕 The columns of section 4 give 3 % to 26 %. A
rewrite that opens every sentence with そのため or また has traded one
uniform shape for another, and 石黒 names that failure too:
「一つか二つの決まった接続詞しか使えないために、単調で読みにくくなっている
文章」.

What follows for a rewrite:

- A split keeps the tie. The clause that ended in が, ので or ため stated a
  relation; the sentence cut off from it opens with the word that states the
  same relation (しかし、 そのため、 このうち、), or the sentence stays whole.
  The relation was in the original, so this adds no content.
- A join the text already states can be written in. Two sentences one of
  which gives the cause of the other become one sentence with ので or ため,
  or the second opens with そのため. Where the relation is the rewriter's
  guess, the sentences stay apart and the question goes to the author.
- A stock connective cut as a tell (このように, また at every paragraph head)
  leaves the paragraph it closed or opened. Read the paragraph after the cut:
  where the reader now meets a conclusion with nothing to mark it, the tie
  stays or another word carries it.
- A subject the last sentence gave can stay unsaid. The 建議 limits this at
  the point where the reader would lose it: 「日本語の文では、主語が省略される
  ことがあるが、それによって誤解が生じることもある。」 〔公用文〕 Ⅲ-3 オ.
  Naming the same subject at the head of every sentence is the
  `subject-first` marker of the translationese reference.

### 2.3 Length is uneven, and so is weight

The 建議 sets no cap on a sentence: 「単に長い短いが問題になるわけではないが、
一文を短くすることによって、読み取りにくい文にすることを防ぐことができる。」
「適当な長さは一概に決められないが、50～60 字ほどになってきたら読みにくく
なっていないか意識するとよい。」 〔公用文〕 Ⅲ-3 ア. Fifty to sixty characters
is where to check, and the test is whether the sentence still reads. The mean
in the documents of section 4 is 41 to 55 characters with a coefficient of
variation of 0.4 to 0.65; the memo of section 1 ran 31. A study of
literary texts found the same of generated Japanese: 「LLM テキストの方が文長の
ばらつきが低い，つまり，LLM は同じ長さの文を生成する傾向があると言える．」
〔岩本2026〕

A sentence per clause puts every fact at the same height. A subordinate clause
says which fact is the ground and which is the point (「費用は増えませんが、
属人化は残ります」), and a writer who thinks a point matters gives it more
room. natural-japanese's guide calls this 濃淡: a document in which every
section has the same thickness hides which part matters (its §1).

The 2018 report adds the limit on cutting: 「もちろん，文を短くするからと
いって，必要な情報を落とすことがないように気を付けましょう。」 〔分かり合う〕
p. 43.

What follows for a rewrite:

- A sentence over the length line that reads in one pass, its clauses in the
  order things happened, stays.
- A sentence is split where its topic changes, as the 建議 says (「論点が変わる
  ときには、文を区切った方が読み取りやすい。」), and left whole where one
  thought runs through it.
- A rewrite leaves the paragraph's proportions alone: the long sentence that
  carried the main point stays the long one.

### 2.4 The writer stands somewhere

The 建議 opens on this: 「公用文は、伝えたいことを一方的に書き連ねるものでは
ない。」「一方向の情報発信であっても、書き言葉によるコミュニケーションとして
捉えるとよい。」 It names distance as something words set: 「言葉にも相手との
距離を表す機能があり、敬意と親しさのバランスをとるよう考えながら書くことで
適度な距離感になる。傾向として、和語より漢語、動詞的表現より名詞的表現で、
対象が客観化されて距離感が大きくなりやすい。」 〔公用文〕 The 2018 report says
what the reader feels when it is missing: 「言葉には，気持ちが反映されます。
気持ちのない言葉は，時として軽く，また冷たく感じられます。」 〔分かり合う〕
p. 47. Its checklist for accuracy asks the writer to mark what is fact and what
is inference: 「事実と意見とを区別し，推論や推測に際しては裏付けの有無を明示
している。」 〔分かり合う〕 p. 18.

A text reads as written by someone when it shows which statements are the
writer's own view, how sure the writer is, and what the writer wants of the
reader. Each of these sits in a form some rule of this skill reports: a hedge,
a が that concedes, a negative that limits a claim, 私たち, と思います, an
adverb such as きっと or おそらく. A rule that reports the form is right to ask
whether it earns its place. The answer is a reading of the sentence, and it is
"stays" whenever the form is doing the job this section names.

What follows for a rewrite:

- A view stays marked as a view, and a recommendation as a recommendation
  (担当としては B 案を推します).
- A word is replaced for a defect in it. A plain word that reads well is left
  alone: 頼る beside 依存する in one memo names no second thing, and
  natural-japanese's guide rules out the swap (「意味の分かる言葉を、好みで
  言い換えない」, its §3). One term per concept applies to terms.
- A rewrite brings in no fact, plan or promise the text lacks, in any layer.

## 3. Questions for the reader

Asked of every paragraph of two or more sentences of running text. Lists,
tables, quotations and code stay out. Each has a YES or NO answer, and a YES is
a finding, reported with the line the paragraph starts on, its first sentence
and the whole paragraph rewritten. A rewrite uses only what the paragraph and
its neighbours already say. Where the fix would need something the text lacks,
report the question for the author and no rewrite. Like section 3.4 of the
translationese reference, this section quotes no defect.

**`flow-join`** - Read each sentence with the one before it and say how the
two are related: cause, result, contrast, example, addition, order in time.
Answer YES when the relation is plain from the content and no word in either
sentence states it, for two or more pairs in the paragraph. Rewrite by joining
the pair in one sentence or by opening the second with the word for the
relation.

**`flow-ending`** - Name what each sentence does: reports a fact, gives a
reason, judges, asks or advises, limits. Answer YES when three or more
sentences in a row end in the same form while they do different things, so
that a judgement or a reason reads as one more fact. Rewrite each with the
ending of what it is (section 2.1), in the style's 文体, and keep how sure the
text is: an ending is changed to show a kind the content already has.

**`flow-weight`** - Find the sentence that carries the paragraph's point.
Answer YES when no sentence does, because every sentence is one clause of
about the same length and none is grounded on another. Rewrite by making the
ground a clause of the sentence it supports. A paragraph of steps or of
parallel facts answers NO.

**`flow-named`** - Answer YES when the same subject or the same long noun
phrase heads three or more sentences in a row where the previous sentence
already gave it. Rewrite with the subject left out, or with a demonstrative,
wherever the reader still recovers it at once.

**`flow-cut`** - Ask only on a second read, of a paragraph that holds a
rewritten sentence. Answer YES when a sentence opens on a conclusion, a
contrast or a result that nothing before it prepares, or when a demonstrative
points at nothing in the sentence before. Report the sentence; the rewriter
holds the original and restores the tie.

A document meant to be flat answers NO throughout: a changelog, a list of
measured values, a reference table written out as sentences.

## 4. Measurements

`flow.py` over human-written Japanese and over text from section 1, on
2026-11-11. The columns are the prose paragraphs of each page, with dictionary
entries and quotations from novels left out. The two PDFs are sentences of 25
to 220 characters taken from each page's text, so their paragraph breaks are
lost and the last column is left blank for them.

| Text | Sentences | Mean length | Length CV | Plain endings % | Judge % | Joints per sentence | Lone % | Flat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ぶんかる「言葉のQ&A」 001-014, 文化庁国語課, 2014-2018: range over the 14 | 35-87 | 32.0-55.0 | 0.40-0.87 | 45.2-69.7 | 0.0-16.7 | 0.75-1.63 | 13.6-52.9 | none |
| the same, median of the 14 | 54.5 | 47.2 | 0.55 | 59.8 | 11.1 | 1.29 | 21.4 | |
| 「公用文作成の考え方」 and its 解説, 2022 | 548 | 49.1 | 0.43 | 77.9 | 0.7 | 1.07 | 22.4 | |
| 「分かり合うための言語コミュニケーション（報告）」, 2018 | 1089 | 53.8 | 0.47 | 54.5 | 17.0 | 1.36 | 18.5 | |
| A memo Claude drafted with no rule in force, body sentences | 18 | 30.9 | 0.46 | 55.6 | 5.6 | 0.78 | 27.8 | no |
| A report Claude wrote under the 1.10.0 hooks, list items counted | 59 | 36.7 | 0.43 | 66.1 | 0.0 | 0.41 | 59.3 | yes |

The `flat` line of `flow.py` is 40 % lone sentences or more together with 0.6
joints a sentence or fewer, in a document of 12 body sentences or more. It
marks the last row and none of the others. One column (014) reaches 52.9 %
lone sentences, since half of it is a list of short example phrases, and holds
0.75 joints, so the two figures are read together. The line rests on these 17
human documents and 2 generated ones; it is a direction, and the reading of
section 3 decides.

The `flatter` marks of `flow.py --before` use these least changes: 5 points
for a percentage, 0.15 joints, 0.05 in the CV, 15 % in the count of sentences
and in the mean length, one sentence in the longest run. They are this
skill's, set so that the run of section 1, item 2, is marked on six figures.

To reproduce a row, fetch the page, keep its prose paragraphs in a Markdown
file and run `scripts/flow.py --json <file>`.

## 5. Sources

- 〔公用文〕 文化審議会. 「公用文作成の考え方（建議）」 and its 解説, 令和4年1月7日. https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/pdf/93651301_01.pdf
- 〔分かり合う〕 文化審議会国語分科会. 「分かり合うための言語コミュニケーション（報告）」, 平成30年3月2日. https://www.bunka.go.jp/koho_hodo_oshirase/hodohappyo/__icsFiles/afieldfile/2018/04/09/a1401904_03.pdf (measured in section 4 from the copy at https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/wakariau/pdf/r1403493_01.pdf)
- 〔立教〕 立教大学 大学教育開発・支援センター. 『Master of Writing』 「8. レポートの文章表現」, pp. 17-18. https://www.rikkyo.ac.jp/about/activities/fd/cdshe/mknpps000001ri7e-att/MoW_8.pdf
- 〔石黒2009〕 石黒圭. 「接続詞の難しさ」, 国際交流基金 『日本語教育通信』 日本語・日本語教育を研究する 第37回. https://www.jpf.go.jp/j/project/japanese/teach/tsushin/research/200908.html
- 〔伊藤1991〕 伊藤俊一・阿部純一. 「接続詞の機能と必要性」, 心理学研究 62(5), 316-323, 1991. https://www.jstage.jst.go.jp/article/jjpsy1926/62/5/62_5_316/_pdf/-char/ja (a scanned page; the quotations were read from its image)
- 〔Zaitsu2025〕 Wataru Zaitsu, Mingzhe Jin, Shunichi Ishihara, Satoru Tsuge and Mitsuyuki Inaba. "Stylometry can reveal artificial intelligence authorship, but humans struggle: A comparison of human and seven large language models in Japanese", *PLOS ONE* 20(10): e0335369, 2025. https://doi.org/10.1371/journal.pone.0335369
- 〔岩本2026〕 岩本海風・宮本友樹・内海彰. 「大規模言語モデルで生成された文学テキストの検出と有効な識別的特徴の探求」, 言語処理学会第32回年次大会 P9-11, 2026年3月. https://www.anlp.jp/proceedings/annual_meeting/2026/pdf_dir/P9-11.pdf (published without peer review; poems, lyrics and short stories)
- 〔大西〕 大西夢. 「AI生成文からみた「自然な日本語」についての研究」, 広島大学文学部 令和7年度卒業論文, pp. 34-35. https://home.hiroshima-u.ac.jp/jshira/papers/ (an undergraduate thesis on a small sample; the file is the one whose name is the thesis title)
- 文化庁国語課. 文化庁広報誌ぶんかる 連載「言葉のQ&A」 001-014, 2014-05 to 2018-07, measured in section 4. https://www.bunka.go.jp/prmagazine/rensai/kotoba/kotoba_001.html (the number in the URL runs to 014)
- coji. natural-japanese, `guide.md` §1 to §3 (MIT), in `vendor/natural-japanese`. https://github.com/coji/natural-japanese
