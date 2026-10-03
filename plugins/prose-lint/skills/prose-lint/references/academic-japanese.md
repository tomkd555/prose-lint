# Academic register for Japanese

The rules the skill applies when a Japanese text is a paper, a thesis or a
report, and the sources each rule rests on. `assets/academic.sample.md` holds
the rules a regex can find; the rest need a reading, and the review in academic
mode works through them. Every source below was fetched and read on 2026-09-26,
and the Japanese passages are quoted as they appear there. The short names in
brackets are the keys the register rows cite; section 6 gives each one in full.

## 1. What makes Japanese read as a paper

The sources agree on six points. Each names what to change and what to write
in its place.

### 1.1 常体 in the である form

The 建議 on official writing calls the である forms the written style proper:

> 「である・であろう・であった」は書き言葉専用の文体であり、論理的に結論を導き出すような文章にふさわしい。〔公用文〕 Ⅲ-1 ウ

Every university guide read asks for 常体 and forbids mixing it with です・ます
〔東北大, 金沢大, 立教大, 神戸国際大, 名桜大 and 立命館IR〕. So do the lab guides
〔坂間, 垂水, 金森〕 and two society author guides:

> 文章は口語体で、基本的に｢である調｣で統一すること。〔土木学会E3〕

A society guide's 「口語体」 means modern written Japanese, not speech:
「口語体とは現代語の文章形式のことで，いわゆる「である体」を意味する．」〔塚本〕

「だ」 is the weaker point. 垂水 asks to avoid it; 金沢大 allows a few 「だ」
endings on a である base. The register flags sentence-final だ, だった and
だろう; keep one where the surrounding text already mixes them on purpose.

### 1.2 Written words in place of spoken ones

Most register rows are pairs of this kind. The largest inventory is 〔柏野2016〕,
a survey of 32 books and 31 papers on writing that collected 1,900 words the
literature marks as 書き言葉的 or 話し言葉的. It stresses that the line is
graded: 「話し言葉的「とても」は書き言葉的「たいへん，非常に，極めて，著しく」
の組として示されている」, while the same 「とても」 is the written partner of
「とっても，すごく」. The register therefore splits とても (a judgement row)
from すごく and とっても (fixed).

Two findings shape the rows:

- For connectives the corpus agrees with the guides. 〔馬場2018〕 measured the
  hardness of connectives in BCCWJ and matched it to 柏野's four classes (a: to
  be avoided … d: no problem in academic prose). Class a holds
  「けど，だって，でも，それで，ですから，けれど，それから，だから」; class d
  holds しかし、また、ただし、あるいは、さらに、したがって、または、なお、すなわち、
  および.
- For adverbs, the Sino-Japanese word is often the spoken one: 「全然，多分，絶対，
  全部，一番は話し言葉的であり，まったく，おそらく，〔かならず〕，すべて，もっとも
  は書き言葉的」〔柏野2016, citing 石黒 2012〕.

### 1.3 The writer stays out of the sentence

「私」 does not appear 〔立命館IR, 名桜大, 樋口, 垂水, 柏野2016〕. Write no
subject, or 「本研究では」「本稿では」; where one person must be named, write
「筆者」 〔垂水, 名桜大, 長倉〕. Some fields write 「我々」: 「論文の主語になる
言葉は、基本的には「我々」です。」〔垂水, information science〕. Keep 我々
when the text uses it consistently.

「と思う」 and 「と感じる」 go 〔金沢大, 大阪大, 関西大〕. 〔酒井・関2020〕 compared 332 student reports with papers in
three fields: the papers prefer 「と考えられる（266）」 and 「と思われる（109）」,
the reports 「と考える（330）」 and 「と思う（140）」, and 「と思う」
「読み手に対して稚拙な印象を与えかねない」. The replacement the guides give is
「と考えられる」, because it states 「合理的な判断に基づく結論」〔立教大〕.

Three narrower points from the same study: write the discussion in the present
tense (「と考えた」 is a report habit; 〔法政大〕 says the same), do not stack
modality (「のではないか＋と考える」), and do not write 「と考察される」, which
never occurs in the papers.

### 1.4 Fact and judgement kept apart

> 事実（である，だ）と判断（だろう，と思われる，と考えられる）をきっちり分けて書いた〔玉木〕

> どこまでが事実でどこからが推測なのかは明確である必要があります〔遊佐研〕

「と考えられる」 itself can hide whose judgement it is:
「一般的にそう考えられているのか，著者（皆さん）がそう考えたのか，他の論文著者
がそう考えたのか，があいまいである」〔見延〕. Where the view is someone else's,
write 「と考えられている（文献）」 or 「との主張がなされている（文献）」. 「と言える」
states a fact, 「「（著者が）そう主張したい」という場合には使えない」〔森畑〕.
Where the evidence settles it, write 「である」 〔室蘭工大, 森畑〕.

### 1.5 Measured claims

- Numbers over adjectives: 「なるべく定量的な表現を行うようにする」〔泉〕; 「だいたい」
  「かなり」 blur the claim 〔名大図書館〕.
- No absolutes without proof: 「完全に〜である」 and 「全く〜ない」 claim 100% and
  0% 〔室蘭工大〕; 「必ず」 likewise 〔柏野2016, citing 石黒 2012〕.
- No praise of one's own result: 「〈important〉，〈very interesting〉などの形容をする
  ことは差し控えるべきである」〔泉〕; 「誇大広告は読者 (査読者) の印象が悪く」
  〔金森〕.
- 「示す」 and 「明らか」 are strong verbs; use them only where the argument or
  data settle the point 〔白川〕.

### 1.6 Sentences finished in words

- No 体言止め in running text 〔東北大, 金沢大, 法政大, 垂水〕. koyobun's
  `nominal_ending` already finds them.
- No ？ or ！: 「！、? などの記号を使わない。」〔東北大〕. A question ends
  「〜だろうか。」 or 「〜ではないか。」 〔徳島大〕.
- Name the referent of a demonstrative: 「これを…して」→「この画像を…して」
  〔金森〕; 「指示代名詞は，特に断らない限り直前の名詞を指示する」〔見延〕.
- One term for one concept, from start to end 〔森畑, 遊佐研〕.
- Methods and results in the past tense, discussion in the present 〔富山県大,
  法政大〕.

## 2. Formal without stiff

Raising the register is not piling up kanji compounds. The same sources name
the forms that make a text heavier and no clearer; the register lists them
under 「判断が要る言い方」 and 「文語調」.

- A kanji verb in place of a native one does raise the register: 「決める →
  決定（する）」「性質が変わる → 性質が変化する」, with the caveat
  「分かりやすさ、親しみやすさを妨げるおそれがあることに留意する」〔公用文〕 Ⅱ-8 ウ.
  Use it where the kanji verb is more precise, not everywhere.
- 文語調 is not formality: 「公用文には、一定の格式が求められるが、そのために文語調
  を用いることは避ける」; 「べく」「べし」 are not used, and 「するべき」 is written
  「すべき」 〔公用文〕 Ⅲ-1 エ・オ.
- 「推定することができる」→「推定できる」, 「補正を行った」→「補正した」,
  「しかしながら」→「しかし」 〔奥村〕. 〔室蘭工大〕 keeps 「ことができる」 where the
  sentence is about possibility or ability.
- 「～において」「～については」 are to be kept few 〔松尾〕, and 「における」 often
  reads better as 「の」 〔奥村〕. These are too common in good papers for a
  register row; count them in the review instead, and thin out a paragraph that
  leans on them.
- 「のである」 overused reads as pushy: 「乱用すると押しつけがましい感じを与えます」
  〔立教大〕.
- A stiff connective on every sentence (それゆえ, ゆえに, よって) reads as
  forced 〔白川〕. Use one where the logic turns.

## 3. Where the sources disagree

Rule on these by the field and the target journal; say which reading you took.

| Point | One side | Other side | Default in this skill |
| --- | --- | --- | --- |
| 「と思われる」 | Avoid 〔室蘭工大, 森畑, 坂間, 大手前〕 | Fine with no subject 〔白川, 法政大〕; frequent in literature papers 〔向坂2024〕 | Judgement row. Keep with no subject and a stated ground; otherwise 「と考えられる」 or 「である」 |
| 「と考える」 | Implies 「私」 〔向坂2024 citing 石黒 2012〕 | The usual form in literature papers 〔向坂2024〕 | Not flagged; the review checks that the ground is given |
| 「我々」 | Avoid 〔樋口, 立命館IR〕 | The norm 〔垂水〕 | Not flagged |
| 「〜ていく」 | 「見ていく」 is spoken 〔室蘭工大〕 | 「論じていく」 fits a thesis 〔白川〕 | Not flagged |
| 文中の「なので」「だから」 | Replace 〔金沢大, 室蘭工大〕 | Fine inside one sentence 〔白川〕 | Judgement row |
| 「かもしれない」 | textlint's `ja-no-weak-phrase` flags it | The 〇 form in 〔東北大〕 | Fix as textlint says when the claim has data behind it; keep when the text states a real uncertainty |
| 及び・更に | Write in kana 〔金森, 塚本〕 | Kanji per 内閣訓令 | The 訓令, unless the journal says otherwise |

## 4. Journal and field conventions

A journal's author guide wins over this file and over the 訓令 rules.

- Some journals ask for 「，」 and 「．」: 「日本語の句読点はカンマ（，）とピリオド
  （．）を使用し，“、”や“。”は使用しません．」〔人工知能学会〕; 土木学会 asks the
  same. Punctuation stays in textlint's notation tier; change it only when the
  user names the journal or asks.
- 常用漢字 and 現代仮名遣い are required in 〔人工知能学会〕 and 〔塚本〕.
- Abbreviations are written out at first use: 文科省 → 文部科学省, with
  「（以下、文科省）」 allowed after it 〔東北大〕.

## 5. Not bundled

- `textlint-rule-preset-ja-engineering-paper` (kn1cht, MIT): its prh dictionary
  deletes 「非常に」「極めて」 outright and rewrites 又は, 基に and 挙げる against
  the 訓令, and it forces 「，．」. Its register ideas are cited as
  〔ja-engineering-paper〕; the preset itself is left out.
- 『語の文体値データ』 (NINJAL; 〔馬場2022〕) scores the hardness of thousands of
  words from corpus frequencies, and 柏野's KAKEN 20K00655 built a register
  database of 2,791 words. Either could replace hand-written rows with a
  scored lexicon; neither is bundled.

## 6. Sources

Accessed 2026-09-26.

### Public guidance

| Key | Source |
| --- | --- |
| 公用文 | 文化審議会（建議）「公用文作成の考え方」2022-01-07. https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/93650001_01.html (PDF: https://www.bunka.go.jp/seisaku/bunkashingikai/kokugo/hokoku/pdf/93651301_01.pdf) |

### Research papers

| Key | Source |
| --- | --- |
| 柏野2016 | 柏野和佳子・田嶋明日香・平本智弥・木田真理「学術的文章作成時に留意すべき「書き言葉的」「話し言葉的」な語の文献調査」『言語処理学会第22回年次大会発表論文集』pp.1041–1044, 2016. https://www.anlp.jp/proceedings/annual_meeting/2016/pdf_dir/P18-1.pdf |
| 馬場2018 | 馬場俊臣「接続詞の文体差の計量的分析の試み―『BCCWJ図書館サブコーパスの文体情報』を用いて―」『北海道教育大学紀要（人文科学・社会科学編）』69(1), pp.1–15, 2018. https://doi.org/10.32150/00006733 |
| 馬場2022 | 馬場俊臣「「語の文体」と「文章の文体」―『語の文体値データ』を利用した「文章の文体」の推定―」『計量国語学』33(7), pp.435–450, 2022. https://www.jstage.jst.go.jp/article/mathling/33/7/33_435/_pdf/-char/ja |
| 酒井・関2020 | 酒井晴香・関玲「文末モダリティ表現に焦点を当てた大学生レポートの問題―コーパスを用いた実態調査より―」『国語科教育』88, pp.21–29, 2020. https://doi.org/10.20555/kokugoka.88.0_21 |
| 山下ほか2022 | 山下由美子・川越颯亮・小松川浩・山川広人「学生レポートの話し言葉改善を目指したオンライン型協調学習の実践研究」『リメディアル教育研究』16, pp.53–63, 2022. https://doi.org/10.18950/jade.2022.05.19.01 |
| 向坂2024 | 向坂卓也「文学論文における思考動詞の使用状況―医学・農学・工学論文における使用状況との比較を通して―」言語資源ワークショップ2024（国立国語研究所）. https://clrd.ninjal.ac.jp/lrw/lrw2024/i2_C1-paper.pdf |

### University writing guides

| Key | Source |
| --- | --- |
| 東北大 | 東北大学『東北大学レポート指南書』第5版, 2024-03-15. https://ital.ihe.tohoku.ac.jp/italwp/wp-content/uploads/2024/03/shinansyo_v5.pdf ; 『東北大学レポート指南書・別冊』2024-03-21. https://ital.ihe.tohoku.ac.jp/italwp/wp-content/uploads/2024/03/shinansyo_bessatu.pdf |
| 金沢大 | 金沢大学国際基幹教育院『レポート作成の手引き』2023-04. https://ilas.w3.kanazawa-u.ac.jp/wp-content/uploads/ReportWritingGuide.pdf |
| 立教大 | 立教大学大学教育開発・支援センター『Master of Writing』. https://www.rikkyo.ac.jp/about/activities/fd/cdshe/mknpps000001ri7e-att/MasterofWriting.pdf |
| 大阪大 | 大阪大学全学教育推進機構『阪大生のためのアカデミック・ライティング入門』第4版, 2023. https://ir.library.osaka-u.ac.jp/repo/ouka/all/71454/2023academicwriting.pdf |
| 名大図書館 | 名古屋大学附属図書館『アカデミックスキルズ』第2章「レポートの書き方」. https://nagoya.repo.nii.ac.jp/record/2002305/files/Academic_Skills_02.pdf |
| 法政大 | 法政大学教育開発・学習支援センター 学習ハンドブック「レポートの文章術」. https://www.hoseikyoiku.jp/lf/images/handbook/pdf/2020/handbook22.pdf |
| 関西大 | 関西大学ライティングラボ「期末レポートに関するルーブリック」2016. https://www.kansai-u.ac.jp/ctl/labo/images/write1_4.pdf |
| 徳島大 | 徳島大学高等教育研究センター「3-1.「文章力」を身につけよう」. https://www.tokushima-u.ac.jp/highedu/reform/sih/writing.html |
| 大手前 | 大手前学園学修サポートセンター「レポートの書き方」第4章 確認テスト（答えと解説）. https://lsc.otemae.ac.jp/documents/reports/04_answer.pdf |
| 神戸国際大 | 神戸国際大学経済学部『レポートの書き方 Ver.1.2』. https://www.kobe-kiu.ac.jp/wp-content/themes/kiu/pdf/i-01_report_guide_eco.pdf |
| 名桜大 | 名桜大学「アカデミックライティングI」講義資料. https://www.meio-u.ac.jp/support/assets/academicwriting01.pdf |
| 富山県大 | 富山県立大学『レポートの書き方』2020. https://www.pu-toyama.ac.jp/shirabasu/2020report.pdf |
| 立命館IR | 立命館大学国際関係学部「IRナビ テクニック編：論文・レポートの書き方」. https://www.ritsumei.ac.jp/ir/ir-navi/technic/technic01.html/ |

### Lab and faculty guides

| Key | Source |
| --- | --- |
| 樋口 | 樋口能士（立命館大学）「環境工学系研究室 卒業論文/修士論文 作成の手引き」2021. https://www.ritsumei.ac.jp/se/rv/higuchi/thesis/guide.html |
| 坂間 | 坂間千秋（和歌山大学）「卒論の書き方」2019. https://web.wakayama-u.ac.jp/~sakama/sotsuron/sotsuron.html |
| 垂水 | 垂水浩幸（香川大学）「卒業論文・修士論文の書き方」2017. https://stwww.eng.kagawa-u.ac.jp/~tarumi/sotsuron/howto.html |
| 室蘭工大 | 室蘭工業大学 水素機能材料学研究室, two pages of its thesis-writing rules. https://u.muroran-it.ac.jp/hydrogen/thesis_style.html ; https://u.muroran-it.ac.jp/hydrogen/thesis_express.html |
| 見延 | 見延庄士郎（北海道大学）「レポート・卒論の書き方初級編」「論文の書き方中級編」. https://geodynamics.sci.hokudai.ac.jp/poc/minobe/class/how2write_1.htm ; https://geodynamics.sci.hokudai.ac.jp/poc/minobe/class/how2write_2.htm |
| 金森 | 金森由博（筑波大学）「論文執筆のためのチェックリスト」第1.42版, 2020. https://kanamori.cs.tsukuba.ac.jp/docs/writing_paper_checklist.pdf |
| 玉木 | 玉木徹「卒論・修論チェックリスト」Qiita, 2021. https://qiita.com/tttamaki/items/f553e4cb9f4f08cc8872 |
| 森畑 | 森畑明昌（東京大学）「Tips for Preparing Thesis」. https://www.graco.c.u-tokyo.ac.jp/labs/morihata/thesis_memo.htm |
| 泉 | 泉聡志（東京大学）「論文の書き方（基本的な事項）」. https://www.fml.t.u-tokyo.ac.jp/~izumi/sotsuron/writing.htm |
| 奥村 | 奥村曉（名古屋大学）修士論文テンプレート, Writing.tex. https://github.com/akira-okumura/MasterThesisTemplate |
| 松尾 | 松尾豊（東京大学）「論文の書き方」2005. https://ymatsuo.com/information/how-to-write-paper-jp/ |
| 長倉 | 長倉ゼミ（慶應義塾大学）「論文を書く上での心構えと注意点」. http://user.keio.ac.jp/~nagakura/zemi/kokorogamae.pdf |
| 白川 | 白川晋太郎「論文・レポートを書く際に」. https://sites.google.com/view/shintaroshirakawa/%E8%AB%96%E6%96%87%E3%83%AC%E3%83%9D%E3%83%BC%E3%83%88%E3%82%92%E6%9B%B8%E3%81%8F%E9%9A%9B%E3%81%AB |
| 遊佐研 | 東北大学 Yusa-Yoshioka Laboratory「論文の書き方について」「論文べからず集」. https://web.tohoku.ac.jp/yusa/index.php/2021/how-to-write-your-article/ ; https://web.tohoku.ac.jp/yusa/index.php/2021/manuscript-dontdothis/ |

### Academic societies and tools

| Key | Source |
| --- | --- |
| 土木学会E3 | 土木学会論文集E3（特集号）執筆要領, 2022改正. https://committees.jsce.or.jp/mokuzai07/system/files/sippitu_youryou22.pdf |
| 人工知能学会 | 人工知能学会論文誌 原稿執筆案内, 2021改訂. https://www.ai-gakkai.or.jp/pdf/journal/how_to_paper.pdf |
| 塚本 | 塚本真也「技術文章の書き方 第2講」『砥粒加工学会誌』57(10), pp.673–676, 2013. https://www.jsat.or.jp/sites/default/files/2017-11/20161227155134.pdf |
| ja-engineering-paper | kn1cht, textlint-rule-preset-ja-engineering-paper 1.0.4 (MIT). https://github.com/kn1cht/textlint-rule-preset-ja-engineering-paper |
