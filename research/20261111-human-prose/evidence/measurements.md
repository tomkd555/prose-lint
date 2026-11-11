# Measurements of 1.12.0 on administrative documents

The second set of the measurement. The first, business documents, is in
`measurements-business.md`. `flow.py` no longer marks the share of topic
openers, so its count of `flatter` figures is now out of 10.

Output of `tools/report.py` on 2026-11-11, over the corpus of `corpus.md` and
the eight drafts of `method.md`. The ids in the tables are those of
`corpus.md`. The prose around these figures is in sections 1 and 4 of
`plugins/prose-lint/skills/prose-lint/references/flow-japanese.md`.

## A. flow.py over 35 human documents, by kind (range, median in parentheses)

| Kind | Docs | Sentences | Mean length | Length CV | 100+ chars % | Under 30 chars % | Plain endings % | Connective openers % | Topic openers % | Parenthesis % | Joints | Lone % | Judge % |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| white | 5 | 54-253 (112) | 79.3-99.7 (80.3) | 0.46-0.49 (0.47) | 21.7-38.9 (29.6) | 0-7.4 (1.8) | 61.4-97.3 (77.9) | 21.4-41.8 (27.8) | 9-19.6 (11.9) | 33.9-47 (38.6) | 1.42-2.12 (1.79) | 6.9-15.2 (11.1) | 0-5.1 (1.6) |
| notice | 4 | 34-92 (46.5) | 85.7-97 (90.3) | 0.48-0.58 (0.52) | 32.6-37.7 (36.4) | 2.2-18.9 (2.7) | 9.8-35 (19.85) | 9.4-40.2 (18.8) | 6.5-35 (16.35) | 13-30 (22) | 1.23-2.24 (1.58) | 7.5-24.5 (9.85) | 0-2.5 (0) |
| speech | 4 | 78-145 (116.5) | 60.6-65.7 (64.6) | 0.38-0.45 (0.41) | 8-14.9 (9) | 6.2-10.7 (8.95) | 81-82.1 (81.75) | 23.1-39.3 (26.6) | 9.7-16.1 (14.7) | 5-13.8 (11.75) | 1.24-2.06 (1.62) | 5.5-14.3 (11.1) | 5.4-14.9 (12.3) |
| column | 15 | 18-45 (28) | 47.7-87.5 (62.9) | 0.34-0.62 (0.46) | 0-33.3 (9.1) | 0-23.1 (9.4) | 42.3-96.6 (84.1) | 13.3-37.5 (27.3) | 4.5-36.4 (20.5) | 3-43.8 (19.2) | 1-2.33 (1.52) | 2.6-25 (15.6) | 0-31.6 (8.9) |
| pr | 3 | 57-117 (72) | 35.5-48.2 (38.9) | 0.45-0.63 (0.48) | 0-2.6 (1.4) | 17.5-43.6 (33.3) | 59.8-70.8 (68.4) | 5.1-16.7 (12.3) | 14.5-24.6 (22.2) | 5.1-22.8 (19.4) | 1.04-1.23 (1.23) | 25-36.8 (35) | 1.8-6.9 (3.4) |
| guide | 2 | 17-19 (18) | 48.8-75.6 (62.2) | 0.32-0.35 (0.33) | 0-21.1 (10.55) | 0-5.9 (2.95) | 100-100 (100) | 17.6-26.3 (21.95) | 10.5-17.6 (14.05) | 5.9-21.1 (13.5) | 1.12-1.74 (1.43) | 15.8-41.2 (28.5) | 0-0 (0) |
| report | 2 | 84-346 (215) | 64.5-108 (86.25) | 0.65-0.65 (0.65) | 19-46.5 (32.75) | 9.8-16.7 (13.25) | 66.2-85.7 (75.95) | 15.5-24.6 (20.05) | 22.6-25.1 (23.85) | 21.1-41.7 (31.4) | 1.25-3.47 (2.36) | 13.6-27.4 (20.5) | 3.6-11.3 (7.5) |
| all | 35 | 17-346 (44) | 35.5-108 (65.7) | 0.32-0.65 (0.47) | 0-46.5 (14.9) | 0-43.6 (9.1) | 9.8-100 (81.8) | 5.1-41.8 (24.6) | 4.5-36.4 (16.1) | 3-47 (21.1) | 1-3.47 (1.56) | 2.6-41.2 (13.6) | 0-31.6 (4.8) |

Body sentences: 2513. Marked flat: []
- Sentences: quartiles 26.0 / 44.0 / 92.0
- Mean length: quartiles 60.6 / 65.7 / 80.3
- Length CV: quartiles 0.4 / 0.5 / 0.5
- 100+ chars %: quartiles 7.7 / 14.9 / 31.2
- Under 30 chars %: quartiles 4.5 / 9.1 / 17.5
- Plain endings %: quartiles 61.4 / 81.8 / 85.7
- Connective openers %: quartiles 17.6 / 24.6 / 28.6
- Topic openers %: quartiles 11.5 / 16.1 / 24.6
- Parenthesis %: quartiles 11.1 / 21.1 / 35.2
- Joints: quartiles 1.2 / 1.6 / 1.8
- Lone %: quartiles 10.8 / 13.6 / 18.2

## B. Eight documents and the drafts written from their notes (human > draft)

| Figure | w7 | w4 | n13 | r4 | s_070 | k4 | m3 | p4 | Median | Drafts lower / higher |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Sentences | 54 > 103 | 83 > 116 | 40 > 58 | 78 > 99 | 39 > 53 | 24 > 39 | 72 > 70 | 17 > 24 | 47 > 64 | 1 / 7 |
| Mean length | 99.7 > 53.4 | 80.3 > 53.3 | 91.5 > 62.3 | 60.6 > 46.6 | 62.8 > 44.5 | 70 > 41.3 | 38.9 > 39.1 | 48.8 > 39.9 | 66.4 > 45.55 | 7 / 1 |
| Length CV | 0.47 > 0.41 | 0.47 > 0.32 | 0.53 > 0.46 | 0.45 > 0.36 | 0.34 > 0.37 | 0.53 > 0.41 | 0.48 > 0.36 | 0.35 > 0.36 | 0.47 > 0.36 | 6 / 2 |
| 100+ chars % | 38.9 > 4.9 | 21.7 > 0.9 | 37.5 > 6.9 | 9 > 0 | 7.7 > 0 | 33.3 > 0 | 1.4 > 0 | 0 > 0 | 15.35 > 0 | 7 / 0 |
| Under 30 chars % | 0 > 11.7 | 0 > 5.2 | 2.5 > 10.3 | 10.3 > 16.2 | 0 > 20.8 | 16.7 > 23.1 | 33.3 > 27.1 | 5.9 > 20.8 | 4.2 > 18.5 | 1 / 7 |
| Plain endings % | 77.8 > 93.2 | 94 > 91.4 | 35 > 51.7 | 82.1 > 81.8 | 87.2 > 86.8 | 50 > 66.7 | 70.8 > 88.6 | 100 > 83.3 | 79.95 > 85.05 | 4 / 4 |
| Connective openers % | 27.8 > 15.5 | 22.9 > 10.3 | 20 > 10.3 | 28.2 > 24.2 | 28.2 > 5.7 | 37.5 > 15.4 | 16.7 > 8.6 | 17.6 > 20.8 | 25.35 > 12.85 | 7 / 1 |
| Topic openers % | 9.3 > 25.2 | 15.7 > 31 | 35 > 32.8 | 15.4 > 21.2 | 20.5 > 41.5 | 8.3 > 10.3 | 22.2 > 32.9 | 17.6 > 33.3 | 16.65 > 31.9 | 1 / 7 |
| Parenthesis % | 35.2 > 30.1 | 38.6 > 26.7 | 30 > 20.7 | 12.8 > 11.1 | 15.4 > 5.7 | 16.7 > 7.7 | 19.4 > 10 | 5.9 > 12.5 | 18.05 > 11.8 | 7 / 1 |
| Joints | 1.76 > 0.79 | 2.01 > 1.22 | 1.7 > 1.33 | 2.06 > 1.63 | 1.56 > 1.3 | 2.33 > 0.97 | 1.04 > 0.87 | 1.12 > 0.83 | 1.73 > 1.09 | 8 / 0 |
| Lone % | 11.1 > 33 | 10.8 > 23.3 | 7.5 > 22.4 | 11.5 > 12.1 | 2.6 > 24.5 | 4.2 > 20.5 | 25 > 27.1 | 41.2 > 37.5 | 10.95 > 23.9 | 1 / 7 |

## C. Sentences the mechanical layers flag (textlint, the general and translationese registers, koyobun.py; one sentence to a paragraph)

| Text | Sentences | With any hit % | Under a rule the skill fixes % | Under a rule the hook blocks on % | Rule-sentence pairs per sentence | Documents the hook would block |
| --- | --- | --- | --- | --- | --- | --- |
| 35 human documents | 2513 | 79.2 | 23.3 | 12.2 | 2.25 | 33 of 35 |
| the 8 human documents of B | 407 | 77.4 | 12.8 | 9.1 | 2.02 | 8 of 8 |
| their 8 drafts | 562 | 60.3 | 6.2 | 6.0 | 1.01 | 6 of 8 |

| Rule | % of sentences, all human | % of sentences, the 8 human | % of sentences, their drafts |
| --- | --- | --- | --- |
| koyobun passive | 32.9 | 32.9 | 24.6 |
| textlint sentence-length | 27.9 | 24.1 | 3.7 |
| koyobun clause_chain | 26.7 | 25.8 | 12.5 |
| koyobun etc | 24.6 | 24.6 | 16.2 |
| koyobun comma_chain | 19.1 | 19.7 | 7.5 |
| textlint max-ten | 18.3 | 17.4 | 2.7 |
| koyobun nominal_ending | 14.2 | 3.9 | 0.2 |
| textlint max-kanji-continuous-len | 14.0 | 10.3 | 6.9 |
| koyobun ga_conjunction | 10.5 | 10.3 | 3.0 |
| textlint no-doubled-joshi | 4.8 | 3.7 | 2.0 |
| textlint ja-no-weak-phrase | 3.7 | 2.0 | 0.5 |
| textlint ai-tech-writing-guideline | 3.5 | 2.2 | 2.1 |
| koyobun negated_predicate | 3.3 | 4.7 | 6.4 |
| register: 何であるかを書く。範囲を | 3.3 | 2.0 | 1.6 |
| textlint ja-no-successive-word | 2.9 | 1.0 | 0.5 |
| textlint no-ai-words | 2.6 | 4.4 | 2.7 |
| koyobun kanji_suru | 2.3 | 2.2 | 1.4 |
| translationese Read in context | 1.4 | 2.9 | 0.5 |
| textlint no-synonyms | 1.2 | 1.7 | 1.2 |
| textlint ja-no-redundant-expression | 1.1 | 0.7 | 0.5 |
| register: 何と何があるのかを挙げる | 1.1 | 1.5 | 0.4 |
| textlint no-ai-hype-expressions | 0.8 | 0.5 | 0.4 |
| textlint ja-hiragana-fukushi | 0.8 | 1.0 | 0.9 |
| textlint no-doubled-conjunctive-particle-ga | 0.7 | 0.0 | 0.0 |
| textlint prh | 0.5 | 0.0 | 0.0 |
| register: 何がどう変わるのかを動詞 | 0.5 | 0.7 | 0.2 |
| register: 誰が言ったのかを書く。出 | 0.4 | 0.5 | 0.4 |
| textlint no-mix-dearu-desumasu | 0.2 | 1.0 | 1.6 |

## D. Naturalness score (the AI-smell lane of natural-japanese's lint, by the formula in SKILL.md)

| | w7 | w4 | n13 | r4 | s_070 | k4 | m3 | p4 | Median |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| human | 98.5 | 98.1 | 97.9 | 98.7 | 97.9 | 97.1 | 97.5 | 97.2 | 97.9 |
| draft | 99.2 | 99.3 | 96.6 | 98.7 | 98.2 | 92.4 | 97.5 | 96.9 | 97.85 |

All 35 human documents: 93.1 to 100.0, median 98.1.

## E. Hits in the 35 human documents as files (per 100 body sentences; documents with a hit)

| Rule | Hits | Per 100 sentences | Documents |
| --- | --- | --- | --- |
| koyobun passive | 1120 | 44.6 | 35 |
| koyobun etc | 797 | 31.7 | 35 |
| textlint sentence-length | 717 | 28.5 | 34 |
| koyobun clause_chain | 658 | 26.2 | 35 |
| textlint max-ten | 488 | 19.4 | 27 |
| textlint max-kanji-continuous-len | 480 | 19.1 | 30 |
| koyobun comma_chain | 468 | 18.6 | 34 |
| koyobun nominal_ending | 343 | 13.6 | 16 |
| koyobun ga_conjunction | 281 | 11.2 | 30 |
| textlint no-doubled-joshi | 129 | 5.1 | 27 |
| textlint ja-no-weak-phrase | 108 | 4.3 | 15 |
| textlint ai-tech-writing-guideline | 95 | 3.8 | 19 |
| register general: 何であるかを書く。範囲を示す | 91 | 3.6 | 24 |
| textlint no-ai-words | 90 | 3.6 | 18 |
| textlint ja-no-successive-word | 88 | 3.5 | 9 |
| koyobun negated_predicate | 83 | 3.3 | 22 |
| natural-japanese forbidden_phrase | 78 | 3.1 | 23 |
| koyobun kanji_suru | 57 | 2.3 | 21 |
| register slop: 何がどう大切なのかを、理由と | 35 | 1.4 | 11 |
| register slop: 副詞を削るか、程度を数字や出 | 33 | 1.3 | 11 |
| textlint no-synonyms | 31 | 1.2 | 17 |
| textlint no-doubled-conjunction | 30 | 1.2 | 15 |
| register general: 何と何があるのかを挙げる。数 | 30 | 1.2 | 13 |
| register slop: 「と」「や」でつなぐか、箇条 | 29 | 1.2 | 11 |
| natural-japanese repeated_sentence_lead | 28 | 1.1 | 10 |
| textlint ja-no-redundant-expression | 28 | 1.1 | 18 |
| natural-japanese low_burstiness | 24 | 1.0 | 24 |
| natural-japanese translationese | 24 | 1.0 | 12 |
| textlint no-ai-hype-expressions | 23 | 0.9 | 9 |
| textlint ja-hiragana-fukushi | 20 | 0.8 | 11 |
| textlint no-doubled-conjunctive-particle-ga | 17 | 0.7 | 3 |
| natural-japanese antithesis_repetition | 15 | 0.6 | 3 |
| natural-japanese low_lexical_diversity_ttr | 14 | 0.6 | 14 |
| register translationese: 「〜できる」「〜できます」と | 14 | 0.6 | 10 |
| register slop: スペースを削る。 | 14 | 0.6 | 11 |
| register slop: ヘッジを 1 つに絞り、残り | 14 | 0.6 | 7 |
| textlint prh | 13 | 0.5 | 10 |
| register general: 何がどう変わるのかを動詞で書 | 12 | 0.5 | 8 |
| register general: 誰が言ったのかを書く。出典を | 11 | 0.4 | 7 |
| register slop: 「誰が」を立てて書き直す。 | 9 | 0.4 | 6 |
| register translationese: 省くか、組織の名前で書く。 | 9 | 0.4 | 7 |
| textlint prefer-tari-tari | 9 | 0.4 | 8 |
| register slop: 普通の日本語に戻せるなら戻す | 9 | 0.4 | 4 |
| register slop: 比喩をやめ、指しているものを | 9 | 0.4 | 4 |
| register translationese: 「〜して」「〜すると」「〜す | 8 | 0.3 | 8 |

Total of the rules above and the rest: 6771 hits, 2.69 per sentence.

## F. natural-japanese's reading-load lane on the 35 documents

| Category | Findings | Per 100 sentences | The 8 originals, per 100 | Their drafts, per 100 |
| --- | --- | --- | --- | --- |
| sentence_too_long | 676 | 26.9 | 22.6 | 3.7 |
| kanji_run | 393 | 15.6 | 12.0 | 8.4 |
| buried_list | 112 | 4.5 | 4.4 | 3.4 |
| translationese_morph | 60 | 2.4 | 2.0 | 1.4 |
| no_chain | 40 | 1.6 | 1.7 | 0.7 |
| sentence_in_paren | 39 | 1.6 | 1.0 | 0.7 |
| double_negative | 10 | 0.4 | 0.2 | 0.0 |

## G. Counts by `tools/features.py` on the eight pairs (original > draft, medians)

| Feature | Median | Drafts lower / higher |
| --- | --- | --- |
| Sentences holding the particle も % | 21.6 > 16.3 | 7 / 1 |
| Sentences opening on が as subject % | 1.9 > 6.4 | 0 / 7 |
| Paragraphs | 17 > 24 | 0 / 7 |
| Sentences with a numeral % | 28.4 > 25.2 | 7 / 0 |

Announcement sentences (以下では…, 本節では…, 今回は…紹介します, ここからは…):
four of the eight originals hold one (W2, S, C1, M) and six of the eight
drafts; the drafts of W1 and C2 hold one where the original has none.
