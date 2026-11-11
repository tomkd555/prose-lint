# How a Japanese text holds together

The material the flow layer and the reader in Step 3a work from. The other
references name wordings to take out. This one names what a paragraph carries
between and around its wordings: the ending that says what a sentence is, the
words that join one sentence to the next, the uneven weight of its sentences,
the writer's distance from the reader, the word that ties a sentence to the
last, and how much one sentence holds. A rewrite that clears every hit and
drops these leaves a list of bare statements, each correct, which reads as
written by no one.

Section 1 gives the measurements behind that claim. Section 2 names the six
things a text keeps, with the grounds for each. Section 3 holds the questions
the reader asks of every paragraph. Section 4 is the table `scripts/flow.py`
was set on, with the measurements of 1.12.0 on everyday business documents
and on documents of ministries and public bodies, and section 5 lists the
sources. Every source was fetched on
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
   scored 96.9, "natural"; its sentences ran 30 characters on average and
   held 0.68 joints each. A report Claude wrote with this plugin's hooks on
   (48 sentences) held 0.46 joints a sentence; 54 % of its sentences joined
   nothing around them, and none ended in a judgement or a request. The human-written documents of section 4 hold 0.75 to 1.63
   joints a sentence.

Measured for 1.12.0, on the skill as it stood at 1.11.0, on two sets of
documents. The skill's default style is `business`, so the first set leads:
43 documents that companies and JPCERT/CC put out in 2021, press releases,
engineering blog posts and security alerts (section 4.5). The second is 35
documents of ministries and public bodies from 2009 to 2022 (sections 4.2 to
4.4). What both sets show is stated as a finding; what only the second shows
is named as such.

4. **A draft has the shape before any rule touches it.** Six of the business
   documents were reduced to notes in English: every fact, figure and name as
   a keyword item, with the cause, the contrast or the certainty the source
   states kept as a tag. Claude then wrote each document again in Japanese
   from its notes, with no rule in force and without sight of the original.
   Read by `flow.py`, every one of the six drafts holds more sentences (33.5
   against 44.5 at the median) and shorter ones (73.8 characters against
   51.4). Sentences of 100 characters or more fall from 19.5 % to 2.1 %, those
   under 30 rise from 5.6 % to 15.9 %, and the joints in a sentence fall from
   1.61 to 1.04, each in all six pairs. Sentences that open with a connective
   fall in five of the six (15.3 % against 7.9 %). Eight of the administrative
   documents, written again from notes in Japanese, moved the same way on
   every one of these figures (section 4.3). Five more documents written from
   a brief of three lines and no notes (an incident report, a proposal, a
   design note, a progress report, an explainer for staff) run shorter still:
   a mean of 33 to 47 characters, no sentence of 100, and 0.59 to 0.97 joints.
5. **Two figures did not carry over.** In the administrative pairs the drafts
   opened a sentence on a topic of its own twice as often as the originals
   and held fewer parentheses. In the business pairs neither moved (22.4 %
   against 24.8 %, and 10.0 % against 9.1 %): a press release opens a third of
   its own sentences on 「当社は、」 or 「本ソリューションは、」. `flow.py` prints the
   two figures and marks neither.
6. **The layers flag the human text more than the draft.** The mechanical
   layers (textlint, the general and translationese registers, `koyobun.py`)
   ran over the six business pairs, one sentence to a paragraph. 70.7 % of the
   208 human sentences drew a hit and 47.2 % of the 305 draft sentences; a
   human sentence drew 1.56 hits by rule and a draft sentence 0.71.
   `sentence-length` fired on 19.7 % of the human sentences and 4.6 % of the
   drafts', `clause_chain` on 26.0 % and 9.8 %, `etc` on 19.2 % and 6.2 %.
   Over all 43 business documents 64.2 % of the 1,291 sentences drew a hit,
   17.2 % under a rule SKILL.md says to fix, and 37 of the 43 hold a finding
   the write hook blocks on. The administrative set gives the same picture
   (section 4.4), and there the naturalness score read originals and drafts
   alike, 97.9 and 97.85 at the median.
7. **The drafts change the words too.** Every one of the six business drafts
   holds fewer katakana words than its original (31.1 to 1,000 characters
   against 29.3). The originals' ユーザー (four times in one notice) came back
   as 利用者, コンテンツ as 内容 and 題材, ブロックされず as 遮断されず, and
   ポイント as 点. One draft went the other way and wrote トランスペアレント
   five times where the press release has 透過的. The design note written from
   a brief says キャッシュに当たらない for a cache miss beside its own
   ヒット率, 「2で拾えないもの」 for cases a step fails to catch, 「既存Redisに
   同居できます」 and 「対応表をRedisに持ちます」. The translationese reference
   takes these up (its section 3.1).

So a hit under the length, chain and comma rules is, on these texts, more
often a mark of a person's sentence than of a defect, and a ledger cleared of
those hits has moved toward the draft. Sections 2.5 and 2.6 name what the
originals keep that the drafts lose.

The causes, by the stage of a run where each sits:

| Stage | Cause |
| --- | --- |
| The draft | Written from the same notes with no rule in force, Claude's sentences already run to one or two clauses of 40 to 60 characters (item 4). The rules that follow were set against long sentences and so pull the same way. |
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

A body that has to grade certainty the same way across many reports fixes the
grades in writing. Every accident report of 運輸安全委員会 opens with the
scale its analysis uses: 「① 断定できる場合・・・「認められる」 ② 断定できない
が、ほぼ間違いない場合・・・「推定される」 ③ 可能性が高い場合・・・
「考えられる」 ④ 可能性がある場合・・・「可能性が考えられる」「可能性があると
考えられる」」 〔運輸安全〕. Exemplar 2.6 shows the four grades at work in one
analysis. A rewrite that moves a sentence from one grade to another has
changed the finding.

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
it. The particle も does part of the same work: it marks its sentence as one
more case of what the last one said. A quarter of the sentences in the white
papers, speeches and columns of section 4.2 hold it, and the drafts of
section 4.3 hold it less often than their originals in 7 of the 8 pairs
(21.6 % against 16.3 %; counted by the script named in section 4).

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
variation of 0.4 to 0.65; the memo of section 1 ran 30. A study of
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

Business documents put figures on this. Over the 43 of section 4.5 the mean
sentence runs from 38 to 103 characters by document, 74 at the median: 78 in
the press releases, 66 in the security alerts, 51 in the engineering blog
posts. A sentence of 100 characters or more makes up 19 % of a document at the
median, 22 % in the press releases and 3 % in the blog posts; a sentence under
30 characters makes up 8 %. The 35 administrative documents of section 4.2 run
to 66 at the median and 15 %. The long sentences are where a ground, a
concession or a condition sits beside the claim it bears on. The drafts of
section 1, item 4, hold next to none of them.

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

### 2.5 The word that ties a sentence to the last

Section 2.2 gives the grounds for a tie. This section gives what a draft does
to one. In the business documents of section 4.5, 13 % of the sentences open
with a connective at the median, and half of the documents sit between 8 %
and 20 %; the six drafts hold half as many as their originals (15.3 % against
7.9 %). A security alert and its draft show where they go. The alert writes
「…攻撃者にアカウント情報が詐取されます。また、詐取されたアカウント情報は、
別のフィッシングメールを送るための踏み台として攻撃者に悪用され、…」 and
opens its next paragraph 「こうした状況から、被害の拡大を防ぐため、…」
〔JPCERT〕. The draft written from the notes of the same passage has
「窃取されたアカウント情報は、…」 and 「被害の拡大を防ぐため、本文書では、…」:
また and こうした状況から are gone, and nothing stands in their place.

How a sentence opens otherwise follows the kind of document. A press release
opens a third of its sentences on its own subject (「当社は、」「本ソリューション
は、」)
and an engineer's blog post a fifth, so the share of such openings is no
finding on its own (section 1, item 5).

What follows for a rewrite:

- A rewrite keeps the tie a sentence opened on. A sentence that began with a
  connective or a demonstrative still does after the fix.
- A sentence cut in two gives the second half an opening that points back, as
  section 2.2 says.
- Naming the subject is a fix for a sentence whose subject the reader cannot
  recover, and for no other. The `subject-first` marker of the translationese
  reference names the opposite failure.

### 2.6 One statement, one sentence

A person writing from knowledge puts a thing and what is said of it in one
sentence. The drafts of section 1, item 4, spread the same content over a
third more sentences, in ways that can each be seen in a pair.

- **A purpose or a ground made into a sentence of its own.** The alert writes
  「攻撃者は、Webメールサービスのアカウント情報の詐取を目的として、サービス
  事業者になりすましたメールを送り、メールの受信者をフィッシングサイトに誘導
  します。」 〔JPCERT〕. Its draft writes 「攻撃者の目的は、Webメールサービスの
  アカウント情報を窃取することです。そのために、サービス提供者を装ったメール
  を送り、受信者をフィッシングサイトに誘導します。」 The first sentence is the
  English frame "the attacker's goal is to…", and the reader waits for the
  second to learn what happens.
- **A course of events cut at each step.** A company's notice tells the review
  and its end in one sentence: 「…公正取引委員会は…違反の疑いがあるとして審査を
  継続していましたが、当社が申し出た改善措置の実施を確認したうえで、本件の
  審査を終了することが発表されましたのでお知らせします。」 〔楽天〕. Its draft
  stops after 「…審査を続けてきました。」 and starts again with 「このたび、…」.
- **A sentence the notes never held.** Two drafts put a count in front of
  items the original simply lists: 「方針の内容は次の三つです。第一に、…」 and
  「oVice を選んだ理由は4つあります。まず、…」. The second draft was free to
  keep the list, wrote it as prose, and added 「ただ、このやり方にはいくつかの
  課題がありました。」 before it. The 建議 asks for the content itself at
  the head: 「文書の結論は、できれば最初の段落で示しておく。最後まで読まないと
  何を言おうとしているか分からないような書き方は避ける。」 〔公用文〕 Ⅲ-4 イ.
  People announce too, in the kinds of text that take it: an engineer's blog
  post says 「そこで今回は、…について紹介していきます。」 So an announcement in
  the text as it was given is no finding. One that a rewrite brought in is.

What follows for a rewrite:

- A split is made at a change of topic (section 2.3) and for no other reason.
  A purpose, a ground or a step of one course of events stays a clause of the
  sentence it belongs to.
- A list in the text stays a list. A rewrite that turns items into prose adds
  the counting and the ordering words the list did without.
- No rewrite adds a sentence the text did not have: one that announces,
  counts or sums up what the text says (以下では…, …は次の三つです, このように
  …と言える). The text's own sentences of that kind stay.

## 3. Questions for the reader

Asked of every paragraph of two or more sentences of running text. A list
item that holds two or more sentences is such a paragraph; an item of one
short sentence or a phrase, a table, a quotation and code stay out. Each has a YES or NO answer, and a YES is
a finding, reported with the line the paragraph starts on, its first sentence
and the whole paragraph rewritten. A rewrite uses only what the paragraph and
its neighbours already say. Where the fix would need something the text lacks,
report the question for the author and no rewrite. Like section 3.4 of the
translationese reference, this section quotes no defect.

**`flow-join`** - Read each sentence with the one before it and say how the
two are related: cause, result, contrast, example, addition, order in time.
Answer YES for each pair whose relation is plain from the content while no
word in either sentence states it. Rewrite by joining the pair in one sentence
or by opening the second with the word for the relation. A paragraph need not
have every pair joined: section 2.2 gives how seldom a sentence opens with a
connective.

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

**`flow-split`** - Answer YES for each pair or run of sentences that makes
one statement between them: the first only names a thing, a purpose or a
count (〜がある, 〜の目的は〜ことである, 〜は次の三つである) and the next says
what the paragraph has to say about it, or one course of events is told a
step to a sentence. Rewrite as one sentence (section 2.6).

**`flow-cut`** - Ask only on a second read, of a paragraph that holds a
rewritten sentence. Answer YES when a sentence opens on a conclusion, a
contrast or a result that nothing before it prepares, or when a demonstrative
points at nothing in the sentence before. Report the sentence; the rewriter
holds the original and restores the tie.

On a second read, ask `flow-split` of the rewritten sentences too: a fix that
cuts one statement in two answers YES there. Report as well each sentence of the
range that only announces or sums up; the rewriter holds the original and
takes out the ones a fix added (section 2.6).

A document meant to be flat answers NO throughout: a changelog, a list of
measured values, a reference table written out as sentences.

Two rules meet at `flow-join`. natural-japanese's guide forbids adding
しかし, そのため and their kin between sentences (its §3), which guards against
a relation the rewriter invents. This reference adds a tie only where the text
fixes the relation: the clause that was cut carried it, or one sentence names
the cause, the exception or the case of the other in its own words. The clause
form the guide allows (が, ので, ため, と) comes first, and an opening word
second. Where the two rules still meet, this one stands, and the report lists
every tie a fix added so the author can strike any that says more than the
text did.

## 4. Measurements

### 4.1 The columns, the 建議 and the report (1.11.0)

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
| A memo Claude drafted with no rule in force | 22 | 29.9 | 0.44 | 54.5 | 13.6 | 0.68 | 36.4 | no |
| A report Claude wrote under the 1.10.0 hooks | 48 | 37.3 | 0.44 | 79.2 | 0.0 | 0.46 | 54.2 | yes |

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
skill's, set so that the run of section 1, item 2, is marked on six of the
eight figures 1.11.0 printed. 1.12.0 added two figures, each marked at 5
points: the share of sentences of 100 characters or more and the share under
30. It also prints the share that open on a topic of their own and the share
with a parenthesis, unmarked (section 1, item 5).

To reproduce a row, fetch the page, keep its prose paragraphs in a Markdown
file and run `scripts/flow.py --json <file>`.

### 4.2 Documents of ministries and public bodies (1.12.0)

The second set of 1.12.0. The first, business documents, is in section 4.5.

35 documents published from 2009 to 2022, fetched on 2026-11-11 and listed in
section 5: 2,513 body sentences. Each page's body was taken out by script,
with headings, paragraphs and list items kept, and a line with no full stop
(a caption, a label, navigation) dropped. The two reports are PDFs read
through `pdftotext`, so their paragraph breaks are unsure. Each cell gives the
range over the documents of its kind and, in parentheses, the median.

| Kind | Documents | Mean length | 100 characters or more % | Under 30 characters % | Connective openers % | Topic openers % | Parenthesis % | Joints per sentence | Lone % | Judge % |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| White-paper sections (内閣府, 環境省, 総務省, 2021) | 5 | 79.3-99.7 (80.3) | 21.7-38.9 (29.6) | 0-7.4 (1.8) | 21.4-41.8 (27.8) | 9.0-19.6 (11.9) | 33.9-47.0 (38.6) | 1.42-2.12 (1.79) | 6.9-15.2 (11.1) | 0-5.1 (1.6) |
| 通知 (文部科学省, 2013-2019) | 4 | 85.7-97.0 (90.3) | 32.6-37.7 (36.4) | 2.2-18.9 (2.7) | 9.4-40.2 (18.8) | 6.5-35.0 (16.4) | 13.0-30.0 (22.0) | 1.23-2.24 (1.58) | 7.5-24.5 (9.9) | 0-2.5 (0) |
| Speeches (日本銀行, 2021) | 4 | 60.6-65.7 (64.6) | 8.0-14.9 (9.0) | 6.2-10.7 (9.0) | 23.1-39.3 (26.6) | 9.7-16.1 (14.7) | 5.0-13.8 (11.8) | 1.24-2.06 (1.62) | 5.5-14.3 (11.1) | 5.4-14.9 (12.3) |
| Columns (統計Today, ことば研究館, 2009-2021) | 15 | 47.7-87.5 (62.9) | 0-33.3 (9.1) | 0-23.1 (9.4) | 13.3-37.5 (27.3) | 4.5-36.4 (20.5) | 3.0-43.8 (19.2) | 1.00-2.33 (1.52) | 2.6-25.0 (15.6) | 0-31.6 (8.9) |
| Magazine articles for the public (aff, 2020-2021) | 3 | 35.5-48.2 (38.9) | 0-2.6 (1.4) | 17.5-43.6 (33.3) | 5.1-16.7 (12.3) | 14.5-24.6 (22.2) | 5.1-22.8 (19.4) | 1.04-1.23 (1.23) | 25.0-36.8 (35.0) | 1.8-6.9 (3.4) |
| An alert and an explainer (国民生活センター, 気象庁, 2021-2022) | 2 | 48.8-75.6 | 0-21.1 | 0-5.9 | 17.6-26.3 | 10.5-17.6 | 5.9-21.1 | 1.12-1.74 | 15.8-41.2 | 0 |
| Reports (運輸安全委員会 2019, COCOA 2021; PDF) | 2 | 64.5-108.0 | 19.0-46.5 | 9.8-16.7 | 15.5-24.6 | 22.6-25.1 | 21.1-41.7 | 1.25-3.47 | 13.6-27.4 | 3.6-11.3 |
| All 35 | 35 | 35.5-108.0 (65.7) | 0-46.5 (14.9) | 0-43.6 (9.1) | 5.1-41.8 (24.6) | 4.5-36.4 (16.1) | 3.0-47.0 (21.1) | 1.00-3.47 (1.56) | 2.6-41.2 (13.6) | 0-31.6 (4.8) |

`flow.py` marks none of the 35 `flat`. The kinds differ as much as any text
differs from a draft: a magazine article for the public runs on short
sentences and the 通知 on long ones. So a figure is read against the row of
the document's own kind, and no single line is drawn through them.

### 4.3 Eight of them beside drafts from their notes (1.12.0)

The method is in section 1, item 4. The eight are 情報通信白書 (W1), 環境白書
(W2), the 通知 on 体罰 (N), the 2021-09 speech (S), 統計Today No.70 (C1),
ことば研究館 qa-100 (C2), aff 2020-09 (M) and the 2021-10 alert (A). Each
cell gives the original and then the draft.

| Figure | W1 | W2 | N | S | C1 | C2 | M | A | Median | Draft lower / higher |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Sentences | 54 > 103 | 83 > 116 | 40 > 58 | 78 > 99 | 39 > 53 | 24 > 39 | 72 > 70 | 17 > 24 | 47 > 64 | 1 / 7 |
| Mean length | 99.7 > 53.4 | 80.3 > 53.3 | 91.5 > 62.3 | 60.6 > 46.6 | 62.8 > 44.5 | 70.0 > 41.3 | 38.9 > 39.1 | 48.8 > 39.9 | 66.4 > 45.6 | 7 / 1 |
| Length CV | 0.47 > 0.41 | 0.47 > 0.32 | 0.53 > 0.46 | 0.45 > 0.36 | 0.34 > 0.37 | 0.53 > 0.41 | 0.48 > 0.36 | 0.35 > 0.36 | 0.47 > 0.36 | 6 / 2 |
| 100 characters or more % | 38.9 > 4.9 | 21.7 > 0.9 | 37.5 > 6.9 | 9.0 > 0 | 7.7 > 0 | 33.3 > 0 | 1.4 > 0 | 0 > 0 | 15.4 > 0 | 7 / 0 |
| Under 30 characters % | 0 > 11.7 | 0 > 5.2 | 2.5 > 10.3 | 10.3 > 16.2 | 0 > 20.8 | 16.7 > 23.1 | 33.3 > 27.1 | 5.9 > 20.8 | 4.2 > 18.5 | 1 / 7 |
| Plain endings % | 77.8 > 93.2 | 94.0 > 91.4 | 35.0 > 51.7 | 82.1 > 81.8 | 87.2 > 86.8 | 50.0 > 66.7 | 70.8 > 88.6 | 100 > 83.3 | 80.0 > 85.1 | 4 / 4 |
| Connective openers % | 27.8 > 15.5 | 22.9 > 10.3 | 20.0 > 10.3 | 28.2 > 24.2 | 28.2 > 5.7 | 37.5 > 15.4 | 16.7 > 8.6 | 17.6 > 20.8 | 25.4 > 12.9 | 7 / 1 |
| Topic openers % | 9.3 > 25.2 | 15.7 > 31.0 | 35.0 > 32.8 | 15.4 > 21.2 | 20.5 > 41.5 | 8.3 > 10.3 | 22.2 > 32.9 | 17.6 > 33.3 | 16.7 > 31.9 | 1 / 7 |
| Parenthesis % | 35.2 > 30.1 | 38.6 > 26.7 | 30.0 > 20.7 | 12.8 > 11.1 | 15.4 > 5.7 | 16.7 > 7.7 | 19.4 > 10.0 | 5.9 > 12.5 | 18.1 > 11.8 | 7 / 1 |
| Joints per sentence | 1.76 > 0.79 | 2.01 > 1.22 | 1.70 > 1.33 | 2.06 > 1.63 | 1.56 > 1.30 | 2.33 > 0.97 | 1.04 > 0.87 | 1.12 > 0.83 | 1.73 > 1.09 | 8 / 0 |
| Lone % | 11.1 > 33.0 | 10.8 > 23.3 | 7.5 > 22.4 | 11.5 > 12.1 | 2.6 > 24.5 | 4.2 > 20.5 | 25.0 > 27.1 | 41.2 > 37.5 | 11.0 > 23.9 | 1 / 7 |
| Figures `--before` marks flatter, of 10 | 9 | 8 | 9 | 7 | 7 | 10 | 4 | 4 | | |

`flow.py` marks none of the eight drafts `flat`: the line of 40 % and 0.6
catches a text written under the old hooks and lets a plain draft through.
The comparison with an original is what shows the shape, which is why the
run copies the file before its first Edit. The share of plain endings and of
judgements moved in no one direction, since the notes carried each source's
certainty as a tag.

### 4.4 What the mechanical layers flag in the same texts (1.12.0)

textlint, the general register, the translationese register and `koyobun.py`
over each text set one sentence to a paragraph. A sentence counts once per
rule.

| Text | Sentences | With a hit % | Under a rule SKILL.md fixes % | Under a rule the write hook blocks on % | Hits by rule, per sentence |
| --- | --- | --- | --- | --- | --- |
| The 35 documents | 2,513 | 79.2 | 23.3 | 12.2 | 2.25 |
| The eight of 4.3 | 407 | 77.4 | 12.8 | 9.1 | 2.02 |
| Their eight drafts | 562 | 60.3 | 6.2 | 6.0 | 1.01 |

| Rule | % of the 2,513 sentences | % of the 407 | % of the drafts' 562 |
| --- | --- | --- | --- |
| `passive` | 32.9 | 32.9 | 24.6 |
| `sentence-length` | 27.9 | 24.1 | 3.7 |
| `clause_chain` | 26.7 | 25.8 | 12.5 |
| `etc` | 24.6 | 24.6 | 16.2 |
| `comma_chain` | 19.1 | 19.7 | 7.5 |
| `max-ten` | 18.3 | 17.4 | 2.7 |
| `max-kanji-continuous-len` | 14.0 | 10.3 | 6.9 |
| `ga_conjunction` | 10.5 | 10.3 | 3.0 |
| `no-doubled-joshi` | 4.8 | 3.7 | 2.0 |
| `ja-no-weak-phrase` | 3.7 | 2.0 | 0.5 |
| `ai-tech-writing-guideline` | 3.5 | 2.2 | 2.1 |
| `negated_predicate` | 3.3 | 4.7 | 6.4 |
| the register's negation row | 3.3 | 2.0 | 1.6 |
| `ja-no-successive-word` | 2.9 | 1.0 | 0.5 |
| `no-ai-words` | 2.6 | 4.4 | 2.7 |

33 of the 35 documents hold a finding of the tier the write hook blocks on,
and 6 of the 8 drafts. The naturalness score, by the formula in SKILL.md,
runs from 93.1 to 100 over the 35 (median 98.1); for the eight it is 97.1 to 98.7 (median 97.9) and
for their drafts 92.4 to 99.3 (median 97.85). `nominal_ending` is left out of
the table: the PDF extracts and the captions of the magazine articles inflate
it.

One long sentence is reported up to four times. natural-japanese's
reading-load lane returned `sentence_too_long` 676 times on the 35 documents
(26.9 per 100 sentences) beside textlint's `sentence-length` at 717, and
`kanji_run` 393 times beside `max-kanji-continuous-len` at 480; `clause_chain`
and `comma_chain` then fire on the same sentences.

Among the findings of the tier the hook blocks on, read one by one on the 35
documents: `ja-no-successive-word` fired 88 times, on doubled brackets
(「（G-MIS））」), on 「一つ一つ」 and on 「○○して」; `no-filler` on the え of
「えのきたけ」; `prh` on 「緊急の日程」 as 日程 for 日ほど; `ja-hiragana-fukushi`
on 「正しく処理される」 as まさしく. `no-ai-words` fired on 検査, 事故, 経路
and 入口 in their plain senses.

### 4.5 Everyday business documents (1.12.0)

43 documents published in 2021 and fetched on 2026-11-11 (section 5): 30
press releases of six companies, 8 posts of a company's engineering blog and
5 security alerts of JPCERT/CC, 1,291 body sentences. They are what a company
publishes; mail, minutes and reports written inside a company are not public
and are not in the set. The bodies were taken out as in section 4.2.

| Kind | Documents | Sentences | Mean length | 100 characters or more % | Under 30 characters % | Connective openers % | Topic openers % | Parenthesis % | Joints per sentence | Lone % | Katakana words per 1,000 characters |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Press releases (日立, 富士通, NEC, 楽天, ソフトバンク, NRI) | 30 | 817 | 54.2-103.4 (77.8) | 10.0-64.7 (22.2) | 0-32.6 (8.0) | 4.5-28.6 (13.6) | 6.7-50.0 (31.6) | 6.2-55.6 (25.4) | 0.58-1.76 (1.19) | 0-50.0 (27.3) | 10.7-54.0 (37.5) |
| Engineering blog posts (サイボウズ, 2021-12) | 8 | 361 | 38.2-73.8 (51.0) | 0-19.4 (2.7) | 3.2-44.1 (10.6) | 5.0-25.8 (16.7) | 9.5-39.0 (18.1) | 0-10.0 (4.1) | 0.87-2.42 (1.41) | 9.7-35.3 (15.9) | 21.1-44.6 (25.1) |
| Security alerts (JPCERT/CC) | 5 | 113 | 58.6-77.5 (65.6) | 3.2-30.3 (10.0) | 5.0-15.2 (6.7) | 5.0-15.2 (7.1) | 7.1-22.6 (13.3) | 0-35.7 (24.2) | 1.00-1.33 (1.15) | 16.1-50.0 (26.7) | 22.9-47.9 (26.4) |
| All 43 | 43 | 1,291 | 38.2-103.4 (73.8) | 0-64.7 (19.4) | 0-44.1 (8.3) | 4.5-28.6 (13.3) | 6.7-50.0 (26.7) | 0-55.6 (20.0) | 0.58-2.42 (1.26) | 0-50.0 (26.7) | 10.7-54.0 (34.6) |

`flow.py` marks one of the 43 `flat`, a press release that is mostly a list
of event dates. Beside the administrative set, these documents open fewer
sentences with a connective (13 % against 25 %), tie fewer sentences to the
ones around them (27 % lone against 14 %) and hold fewer joints (1.26 against
1.56). The line that marks a document `flat` sits well below all of this,
and a figure is read against the row of the document's own kind.

Six of the documents beside drafts written from notes in English (section 1,
item 4): a 日立 press release (P1), an NEC press release (P2), two blog posts
(B1, B2), an alert (A) and a 楽天 notice (N). Each cell gives the original and
then the draft.

| Figure | P1 | P2 | B1 | B2 | A | N | Median | Draft lower / higher |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Sentences | 36 > 48 | 24 > 41 | 36 > 78 | 63 > 72 | 31 > 40 | 18 > 26 | 33.5 > 44.5 | 0 / 6 |
| Mean length | 81.2 > 62.7 | 97.0 > 59.8 | 69.5 > 35.6 | 49.7 > 41.2 | 58.6 > 46.0 | 78.0 > 56.8 | 73.8 > 51.4 | 6 / 0 |
| Length CV | 0.55 > 0.44 | 0.31 > 0.41 | 0.40 > 0.37 | 0.36 > 0.40 | 0.35 > 0.32 | 0.45 > 0.49 | 0.38 > 0.41 | 3 / 3 |
| 100 characters or more % | 27.8 > 4.2 | 33.3 > 9.8 | 16.7 > 0 | 1.6 > 0 | 3.2 > 0 | 22.2 > 7.7 | 19.5 > 2.1 | 6 / 0 |
| Under 30 characters % | 5.6 > 12.5 | 0 > 2.4 | 5.6 > 35.9 | 11.1 > 25.0 | 6.5 > 12.5 | 5.6 > 19.2 | 5.6 > 15.9 | 0 / 6 |
| Plain endings % | 88.9 > 95.8 | 83.3 > 95.1 | 83.3 > 89.7 | 93.7 > 90.3 | 83.9 > 87.5 | 72.2 > 88.5 | 83.6 > 90.0 | 1 / 5 |
| Connective openers % | 13.9 > 6.2 | 25.0 > 14.6 | 16.7 > 23.1 | 19.0 > 8.3 | 9.7 > 7.5 | 5.6 > 3.8 | 15.3 > 7.9 | 5 / 1 |
| Topic openers % | 22.2 > 41.7 | 29.2 > 36.6 | 16.7 > 15.4 | 9.5 > 26.4 | 22.6 > 22.5 | 33.3 > 23.1 | 22.4 > 24.8 | 3 / 3 |
| Parenthesis % | 16.7 > 16.7 | 45.8 > 34.1 | 0 > 1.3 | 3.2 > 1.4 | 0 > 0 | 55.6 > 42.3 | 10.0 > 9.1 | 3 / 1 |
| Joints per sentence | 0.97 > 0.81 | 1.67 > 1.07 | 2.19 > 0.88 | 1.56 > 1.38 | 1.29 > 1.02 | 1.67 > 1.23 | 1.61 > 1.04 | 6 / 0 |
| Lone % | 36.1 > 27.1 | 0 > 29.3 | 13.9 > 23.1 | 15.9 > 20.8 | 16.1 > 25.0 | 33.3 > 19.2 | 16.0 > 24.1 | 2 / 4 |
| Katakana words per 1,000 characters | 47.9 > 42.9 | 31.3 > 30.6 | 30.8 > 28.1 | 21.1 > 20.2 | 47.9 > 46.7 | 10.7 > 6.8 | 31.1 > 29.3 | 6 / 0 |
| Figures `--before` marks flatter, of 10 | 8 | 8 | 8 | 4 | 5 | 6 | | |

The layers over the same texts, counted as in section 4.4:

| Text | Sentences | With a hit % | Under a rule SKILL.md fixes % | Under a rule the write hook blocks on % | Hits by rule, per sentence |
| --- | --- | --- | --- | --- | --- |
| The 43 documents | 1,291 | 64.2 | 17.2 | 11.4 | 1.37 |
| The six originals | 208 | 70.7 | 16.8 | 12.0 | 1.56 |
| Their six drafts | 305 | 47.2 | 5.2 | 5.2 | 0.71 |

| Rule | % of the 1,291 sentences | % of the 208 | % of the drafts' 305 |
| --- | --- | --- | --- |
| `sentence-length` | 23.5 | 19.7 | 4.6 |
| `passive` | 20.2 | 22.6 | 17.4 |
| `clause_chain` | 15.5 | 26.0 | 9.8 |
| `etc` | 15.3 | 19.2 | 6.2 |
| `comma_chain` | 9.1 | 9.6 | 5.6 |
| `max-ten` | 5.8 | 5.8 | 2.0 |
| `max-kanji-continuous-len` | 5.3 | 7.2 | 4.3 |
| the translationese register, read in context | 4.4 | 3.4 | 1.0 |
| the register's row on を実現, に寄与, 最適化 | 3.0 | 2.9 | 1.3 |
| `ga_conjunction` | 2.7 | 5.8 | 2.0 |
| `negated_predicate` | 2.3 | 1.4 | 3.3 |
| `no-ai-words` | 1.7 | 1.4 | 1.0 |
| the register's negation row | 1.4 | 0.5 | 1.6 |

37 of the 43 documents hold a finding of the tier the write hook blocks on.
`no-ai-words` fired 29 times on the 43 documents, 23 of them on 検査 in its
plain sense.

The surface forms the translationese reference names are the business
writer's own. To 1,000 characters the 43 documents hold において 1.18 times,
によって or により 0.94, を行う 0.86 and ことができる 0.79; the six drafts hold
fewer of each than their originals (において 0.92 against 0.07, を行う 1.21
against 0.41). No document holds 彼, 彼女 or 彼ら.

The scripts that took the page bodies out, counted what `flow.py` leaves out
(も, the kinds of opening, katakana words, the surface forms) and made these
tables are in the repository under `research/20261111-human-prose/tools`.

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
- 〔運輸安全〕 運輸安全委員会. 「鉄道事故調査報告書 RA2019-2 Ⅰ 東海旅客鉄道株式会社 飯田線 元善光寺駅～伊那上郷駅間 踏切障害事故」, 平成31年3月28日, 「本報告書本文中に用いる分析の結果を表す用語の取扱いについて」 and 「３ 分析」. https://www.mlit.go.jp/jtsb/railway/rep-acci/RA2019-2-1.pdf
- 〔JPCERT〕 JPCERT/CC. 「Webメールサービスのアカウントを標的としたフィッシングに関する注意喚起」 (JPCERT-AT-2021-0049), 2021-11. https://www.jpcert.or.jp/at/2021/at210049.html
- 〔楽天〕 楽天グループ株式会社. 「「楽天市場」における「共通の送料込みライン」導入にかかる 公正取引委員会による審査終了に関するお知らせ」, 2021-12-06. https://corp.rakuten.co.jp/news/press/2021/1206_01.html

The 35 documents of section 4.2, all fetched on 2026-11-11:

- 内閣府. 「令和3年度 年次経済財政報告」 第1章第1節, 第2章第1節. https://www5.cao.go.jp/j-j/wp/wp-je21/h01-01.html and `h02-01.html`
- 環境省. 「令和3年版 環境・循環型社会・生物多様性白書」 第1部第1章第1節, 第2節. https://www.env.go.jp/policy/hakusyo/r03/html/hj21010101.html and `hj21010102.html`
- 総務省. 「令和3年版 情報通信白書」 「コロナ禍における行政のデジタル活用の成果と課題」. https://www.soumu.go.jp/johotsusintokei/whitepaper/ja/r03/html/nd122110.html
- 文部科学省. 「不登校児童生徒への支援の在り方について（通知）」, 令和元年10月25日. https://www.mext.go.jp/a_menu/shotou/seitoshidou/1422155.htm
- 文部科学省. 「障害のある児童生徒等に対する早期からの一貫した支援について（通知）」, 平成25年10月4日. https://www.mext.go.jp/a_menu/shotou/tokubetu/material/1340331.htm
- 文部科学省. 「性同一性障害に係る児童生徒に対するきめ細かな対応の実施等について」, 平成27年4月30日. https://www.mext.go.jp/b_menu/houdou/27/04/1357468.htm
- 文部科学省. 「体罰の禁止及び児童生徒理解に基づく指導の徹底について（通知）」, 平成25年3月13日. https://www.mext.go.jp/a_menu/shotou/seitoshidou/1331907.htm
- 日本銀行. 講演・挨拶 2021-06-08 「最終局面を迎えたLIBOR移行対応」, 2021-07-27 「気候変動に関する日本銀行の取り組み」, 2021-09-27 「最近の金融経済情勢と金融政策運営」, 2021-12-23 「金融政策と企業行動」. https://www.boj.or.jp/about/press/koen_2021/ko210927a.htm (the others are `ko210608a`, `ko210727a` and `ko211223a`)
- 総務省統計局. 統計Today No.1, 10, 30, 50, 70, 90, 110, 130, 150, 160 and 170, 2009-01 to 2021-04. https://www.stat.go.jp/info/today/001.html (the number in the URL, three digits)
- 国立国語研究所. ことば研究館 「よくあることばの質問」 qa-01, qa-02, qa-50 and qa-100, 2015-04 to 2020-10. https://www.kotobaken.jp/qa/yokuaru/qa-01/
- 農林水産省. 広報誌 aff 2020年9月号 特集1 (1) and 2021年10月号 特集1 (1), (2). https://www.maff.go.jp/j/pr/aff/2009/spe1_01.html, https://www.maff.go.jp/j/pr/aff/2110/spe1_01.html and `spe1_02.html`
- 国民生活センター. 「「解約したはず！」「契約してない！」と思い込んでいませんか？ 予期せぬ“サブスク”の請求トラブルに注意！」, 2021-10-07. https://www.kokusen.go.jp/news/data/n-20211007_1.html
- 気象庁. 知識・解説 「キキクル（危険度分布）」, the page as of 2022-06. https://www.jma.go.jp/jma/kishou/know/bosai/riskmap.html
- 運輸安全委員会. RA2019-2 Ⅰ, as 〔運輸安全〕 above.
- COCOA不具合調査・再発防止策検討チーム（厚生労働省）. 「接触確認アプリ「COCOA」の不具合の発生経緯の調査と再発防止の検討について」, 2021-04. https://www.mhlw.go.jp/content/000769774.pdf

The 43 documents of section 4.5, all fetched on 2026-11-11:

- 株式会社日立製作所. ニュースリリース, 2021-10: the releases of the 1st, 4th, 5th, 6th, 7th, 8th, 12th and 14th. https://www.hitachi.co.jp/New/cnews/month/2021/10/1005.html (the last four digits are the month and day)
- 富士通株式会社. プレスリリース, 2021-10: numbers 1, 4, 6, 7, 8 and 11. https://pr.fujitsu.com/jp/news/2021/10/6.html
- 日本電気株式会社. プレスリリース, 2021-10: the first release of the 4th, 7th, 8th, 11th, 12th and 13th. https://jpn.nec.com/press/202110/20211007_01.html
- 楽天グループ株式会社. プレスリリース, 2021: `1026_02`, `1124_01` and `1206_01`. https://corp.rakuten.co.jp/news/press/2021/1206_01.html
- ソフトバンク株式会社. プレスリリース, 2021: `20210301_01`, `20210316_01`, `20210511_01`, `20210701_01`, `20211001_01` and `20211104_01`. https://www.softbank.jp/corp/news/press/sbkk/2021/20210316_01/
- 株式会社野村総合研究所. ニュースリリース, 2021-10-01. https://www.nri.com/jp/news/newsrelease/lst/2021/cc/1001_1
- サイボウズ株式会社. Cybozu Inside Out, eight posts of 2021-12-02 to 2021-12-22. https://blog.cybozu.io/entry/2021/12/13/160224 (the others are listed in `research/20261111-human-prose/evidence/corpus-business.md`)
- JPCERT/CC. 注意喚起 JPCERT-AT-2021-0041, 0043, 0047, 0049 and 0050. https://www.jpcert.or.jp/at/2021/at210049.html
