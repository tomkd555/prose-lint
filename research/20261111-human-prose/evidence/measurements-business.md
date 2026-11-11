# Measurements of 1.12.0 on business documents

Output of `tools/bizreport.py` on 2026-11-11, over the corpus of
`corpus-business.md` and the six drafts of `method.md`. The ids are those of
`corpus-business.md`. The prose around these figures is in sections 1 and 4.5
of `plugins/prose-lint/skills/prose-lint/references/flow-japanese.md` and in
section 4 of `translationese-japanese.md`.

## A. flow.py and words.py over 43 business documents (range, median in parentheses)

| Kind | Documents | Sentences | Mean length | 100 characters or more % | Under 30 characters % | Connective openers % | Topic openers % | Parenthesis % | Joints per sentence | Lone % | Katakana words per 1,000 characters |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Press releases (日立, 富士通, NEC, 楽天, ソフトバンク, NRI; 2021) | 30 | 817 | 54.2-103.4 (77.75) | 10-64.7 (22.2) | 0-32.6 (8) | 4.5-28.6 (13.6) | 6.7-50 (31.55) | 6.2-55.6 (25.4) | 0.58-1.76 (1.19) | 0-50 (27.25) | 10.68-53.96 (37.5) |
| Engineering blog posts (サイボウズ, 2021-12) | 8 | 361 | 38.2-73.8 (50.95) | 0-19.4 (2.65) | 3.2-44.1 (10.55) | 5-25.8 (16.7) | 9.5-39 (18.05) | 0-10 (4.05) | 0.87-2.42 (1.41) | 9.7-35.3 (15.9) | 21.07-44.57 (25.1) |
| Security alerts (JPCERT/CC, 2021) | 5 | 113 | 58.6-77.5 (65.6) | 3.2-30.3 (10) | 5-15.2 (6.7) | 5-15.2 (7.1) | 7.1-22.6 (13.3) | 0-35.7 (24.2) | 1-1.33 (1.15) | 16.1-50 (26.7) | 22.91-47.91 (26.4) |
| All | 43 | 1291 | 38.2-103.4 (73.8) | 0-64.7 (19.4) | 0-44.1 (8.3) | 4.5-28.6 (13.3) | 6.7-50 (26.7) | 0-55.6 (20) | 0.58-2.42 (1.26) | 0-50 (26.7) | 10.68-53.96 (34.6) |

Marked flat: ['sb_20211104_01']

## B. Six documents and drafts written from English notes of them (original > draft)

| Figure | hi_1005 | nec_20211007_01 | cb_6 | cb_1 | jc_49 | rk_1206_01 | Median | Draft lower / higher |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Sentences | 36 > 48 | 24 > 41 | 36 > 78 | 63 > 72 | 31 > 40 | 18 > 26 | 33.5 > 44.5 | 0 / 6 |
| Mean length | 81.2 > 62.7 | 97 > 59.8 | 69.5 > 35.6 | 49.7 > 41.2 | 58.6 > 46 | 78 > 56.8 | 73.75 > 51.4 | 6 / 0 |
| Length CV | 0.55 > 0.44 | 0.31 > 0.41 | 0.4 > 0.37 | 0.36 > 0.4 | 0.35 > 0.32 | 0.45 > 0.49 | 0.38 > 0.41 | 3 / 3 |
| 100 characters or more % | 27.8 > 4.2 | 33.3 > 9.8 | 16.7 > 0 | 1.6 > 0 | 3.2 > 0 | 22.2 > 7.7 | 19.45 > 2.1 | 6 / 0 |
| Under 30 characters % | 5.6 > 12.5 | 0 > 2.4 | 5.6 > 35.9 | 11.1 > 25 | 6.5 > 12.5 | 5.6 > 19.2 | 5.6 > 15.85 | 0 / 6 |
| Plain endings % | 88.9 > 95.8 | 83.3 > 95.1 | 83.3 > 89.7 | 93.7 > 90.3 | 83.9 > 87.5 | 72.2 > 88.5 | 83.6 > 90 | 1 / 5 |
| Connective openers % | 13.9 > 6.2 | 25 > 14.6 | 16.7 > 23.1 | 19 > 8.3 | 9.7 > 7.5 | 5.6 > 3.8 | 15.3 > 7.9 | 5 / 1 |
| Topic openers % | 22.2 > 41.7 | 29.2 > 36.6 | 16.7 > 15.4 | 9.5 > 26.4 | 22.6 > 22.5 | 33.3 > 23.1 | 22.4 > 24.75 | 3 / 3 |
| Parenthesis % | 16.7 > 16.7 | 45.8 > 34.1 | 0 > 1.3 | 3.2 > 1.4 | 0 > 0 | 55.6 > 42.3 | 9.95 > 9.05 | 3 / 1 |
| Joints per sentence | 0.97 > 0.81 | 1.67 > 1.07 | 2.19 > 0.88 | 1.56 > 1.38 | 1.29 > 1.02 | 1.67 > 1.23 | 1.61 > 1.04 | 6 / 0 |
| Lone % | 36.1 > 27.1 | 0 > 29.3 | 13.9 > 23.1 | 15.9 > 20.8 | 16.1 > 25 | 33.3 > 19.2 | 16 > 24.05 | 2 / 4 |
| Katakana words per 1,000 characters | 47.88 > 42.87 | 31.34 > 30.57 | 30.78 > 28.11 | 21.09 > 20.2 | 47.91 > 46.74 | 10.68 > 6.78 | 31.06 > 29.34 | 6 / 0 |
| One-kanji nouns standing alone per 1,000 characters | 1.03 > 0.66 | 0.43 > 0.41 | 1.6 > 2.88 | 1.6 > 3.03 | 1.65 > 1.63 | 1.42 > 4.07 | 1.51 > 2.25 | 3 / 3 |
| Figures `--before` marks flatter, of 10 | 8 | 8 | 8 | 4 | 5 | 6 | | |

Surface frames per 1,000 characters, original > draft: 可能にする 0.28 > 0.14, ことができる 0.64 > 0.14, を提供する 0.07 > 0.14, を持つ 0.00 > 0.00, を行う 1.21 > 0.41, において 0.92 > 0.07, に関する 1.06 > 0.55, のための 0.00 > 0.07, これら/それら 0.14 > 0.28, 彼/彼女/彼ら 0.00 > 0.00, によって/により 1.21 > 0.69, することで 0.57 > 0.14, ための 0.21 > 0.55

The same frames over all the documents: 可能にする 0.09, ことができる 0.79, を提供する 0.35, を持つ 0.26, を行う 0.86, において 1.18, に関する 0.36, のための 0.04, これら/それら 0.18, 彼/彼女/彼ら 0.00, によって/により 0.94, することで 0.53, ための 0.25

Katakana words in 6 documents or more (tokens, documents): データ (108, 16), サービス (84, 24), システム (72, 16), ソリューション (48, 11), チーム (47, 9), メンバー (38, 8), ユーザー (33, 8), ソフトバンク (32, 6), ソフトウェア (26, 9), セキュリティ (23, 7), イノベーション (22, 7), アプリケーション (21, 7), インフラ (19, 10), デジタル (18, 9), サイト (17, 7), ビジネス (16, 6), アプリ (15, 6), グローバル (14, 6), オンライン (13, 8), グループ (12, 6), サポート (11, 7), コスト (11, 6), ニーズ (10, 7)

One-kanji nouns standing alone, 4 times or more: 声 18, 場 14, 夏 11, 形 8, 金 8, 国 8, 今 7, 例 7, 別 6, 水 5, 話 4, 気 4, 体 4, 共 4. 語 alone: 0; 値 alone: 1.

## C. Sentences the mechanical layers flag

| Text | Sentences | With a hit % | Under a rule SKILL.md fixes % | Under a rule the write hook blocks on % | Hits by rule, per sentence | Documents the hook would block |
| --- | --- | --- | --- | --- | --- | --- |
| The 43 documents | 1291 | 64.2 | 17.2 | 11.4 | 1.37 | 37 of 43 |
| The six of B | 208 | 70.7 | 16.8 | 12.0 | 1.56 | 5 of 6 |
| Their six drafts | 305 | 47.2 | 5.2 | 5.2 | 0.71 | 5 of 6 |

| Rule | % of all sentences | % of the six originals | % of their drafts |
| --- | --- | --- | --- |
| sentence-length | 23.5 | 19.7 | 4.6 |
| passive | 20.2 | 22.6 | 17.4 |
| clause_chain | 15.5 | 26.0 | 9.8 |
| etc | 15.3 | 19.2 | 6.2 |
| comma_chain | 9.1 | 9.6 | 5.6 |
| max-ten | 5.8 | 5.8 | 2.0 |
| nominal_ending | 5.7 | 4.8 | 0.0 |
| max-kanji-continuous-len | 5.3 | 7.2 | 4.3 |
| translationese Read in context | 4.4 | 3.4 | 1.0 |
| no-doubled-joshi | 3.6 | 5.3 | 4.3 |
| register: 何がどう変わるのかを動詞 | 3.0 | 2.9 | 1.3 |
| ga_conjunction | 2.7 | 5.8 | 2.0 |
| negated_predicate | 2.3 | 1.4 | 3.3 |
| kanji_suru | 2.3 | 1.9 | 1.0 |
| ja-no-redundant-expression | 2.2 | 1.0 | 0.3 |
| ai-tech-writing-guideline | 2.1 | 1.4 | 0.7 |
| no-ai-words | 1.7 | 1.4 | 1.0 |
| no-ai-hype-expressions | 1.6 | 1.0 | 0.7 |
| prh | 1.6 | 3.4 | 0.0 |
| no-synonyms | 1.5 | 1.4 | 0.3 |
| register: 何と何があるのかを挙げる | 1.5 | 1.0 | 1.0 |
| ja-no-weak-phrase | 1.5 | 3.4 | 2.3 |
| register: 何であるかを書く。範囲を | 1.4 | 0.5 | 1.6 |
| prefer-tari-tari | 1.0 | 2.4 | 0.0 |

## D. Words the drafts changed

Katakana words of each original that its draft does not hold, and the word
the draft wrote in its place where one was found by reading.

| Pair | In the original | In the draft |
| --- | --- | --- |
| rk_1206_01 | ユーザー (4 times) | 利用者 (4 times) |
| cb_1 | コンテンツ (4 times) | 内容, 題材 |
| jc_49 | ブロックされず | 遮断されず |
| cb_6 | 工夫したポイント | 工夫した点 |
| nec_20211007_01 | コスト, ビジネス (1 each) | not found as katakana |
| jc_49 | ケース, タイミング (1 each) | not found as katakana |
| hi_1005 | 透過的 | トランスペアレント (5 times) |
| jc_49 | 詐取, サービス事業者, かたった | 窃取, サービス提供者, 装った |

## E. Five documents written from a brief and no notes

`flow.py`, `tools/words.py` and textlint's `no-ai-words` over each.

| Document | Mean length | 100 characters or more % | Under 30 characters % | Joints per sentence | Katakana words per 1,000 characters | `no-ai-words` hits |
| --- | --- | --- | --- | --- | --- | --- |
| f1, an incident report | 33.9 | 0 | 52.2 | 0.91 | 16.7 | 疑う |
| f2, a proposal | 46.6 | 0 | 20.0 | 0.80 | 14.0 | none |
| f3, a design note | 33.1 | 0 | 26.3 | 0.61 | 30.2 | 効く |
| f4, a progress report | 34.9 | 0 | 37.9 | 0.59 | 10.9 | 突き合わせる, 漏れ |
| f5, an explainer for staff | 35.0 | 0 | 43.8 | 0.97 | 39.3 | none |

Read one by one, the design note (f3) holds figures for technical acts:
「結果の使い回しがよく効きます」, 「既存Redisに同居できます」, 「ほとんど当たら
なくなる」 and 「キャッシュに当たらないクエリ」 beside its own ヒット率, 「2で
拾えないもの」, 「対応表をRedisに持ちます」. The other four hold none that the
reading found.
