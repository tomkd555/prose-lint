# How well does a surface-pattern or part-of-speech-pattern rule separate a comma splice from a list comma or an introductory-phrase comma?

Sources asked for: rule documentation, issue trackers (LanguageTool, Vale, textlint and write-good) and published studies of comma-splice or run-on detection. Figures asked for: precision or false-positive rates.

## Evidence
| Claim | Publisher | URL | Published | Grade | Quote | Corroboration |
|---|---|---|---|---|---|---|
| Parse-feature CRF comma-splice detector (Stanford parser features) averaged 0.91 precision and 0.28 recall over two learner-text test sets, with a 90% confidence filter | Lee, Yeung, Chodorow, PACLIC 28 (ACL Anthology) | https://aclanthology.org/Y14-1063.pdf | 2014 | A | "our model achieved an average of 0.91 precision and 0.28 recall in detecting comma splices" | single_source |
| Per-set results, full model: CityU 0.91 P / 0.34 R / 0.69 F0.5; Cambridge 0.91 / 0.22 / 0.55 | same | https://aclanthology.org/Y14-1063.pdf | 2014 | A | Table 3: "Full 0.91/0.34/0.69 0.91/0.22/0.55" (table row) | single_source |
| Baseline CRF using only words, POS tags, bigrams and distances to conjunctions (no parse) scored 0.75 P / 0.17 R on CityU and 0.88 P / 0.08 R on Cambridge | same | https://aclanthology.org/Y14-1063.pdf | 2014 | A | Table 3: "Baseline 0.75/0.17/0.45 0.88/0.08/0.30" (table row) | single_source |
| Microsoft Word 2013 grammar checker (rule-based, internals undisclosed) scored 0.74 P / 0.15 R on CityU and 0.90 P / 0.13 R on Cambridge | same | https://aclanthology.org/Y14-1063.pdf | 2014 | A | Table 3: "MS Word 0.74/0.15/0.41 0.90/0.13/0.41" (table row) | single_source |
| Precision on the same data varies by 0.15-0.16 between the CityU set (structurally complex sentences) and the Cambridge set (shorter, simpler) for the baseline and Word; precision is traded for recall via a threshold (full model on CityU: 0.79 P at above 0.5 R) | same | https://aclanthology.org/Y14-1063.pdf | 2014 | A | "when a threshold of 0.65 was used, the precision of the full system on the CityU set dropped to 0.79" | single_source |
| Paper's definition: a noun-phrase list with a missing conjunction is not a comma splice | same | https://aclanthology.org/Y14-1063.pdf | 2014 | A | "a list of noun phrases with a missing conjunction (e.g., "I like apples, oranges.") is not a comma splice." | single_source |
| Clause features (noun/pronoun counts, has-verb flags) were added specifically to stop flagging commas around non-restrictive clauses ("however", appositives) as splices | same | https://aclanthology.org/Y14-1063.pdf | 2014 | A | "help prevent the system from flagging the commas around non-restrictive clauses as comma splices" | single_source |
| Preprocessing strips introductory phrases (transition phrases, prepositional phrases, adverbials), properly joined coordinate and subordinate clauses, and dialogue tags before parsing | same | https://aclanthology.org/Y14-1063.pdf | 2014 | A | "we remove (1) introductory phrases at the beginning of a sentence" | single_source |
| Informal or acceptable comma use causes false positives: model flagged "Hi granny, my name is Winky." while annotators did not | same | https://aclanthology.org/Y14-1063.pdf | 2014 | A | "the system marked the sentence "Hi granny, my name is Winky." as a comma splice, the annotators did not" | single_source |
| Human annotators agree at 91% precision / 92% recall on comma-splice location; disagreements mostly on two consecutive commas around a subordinate phrase | same | https://aclanthology.org/Y14-1063.pdf | 2014 | A | "the precision is 91% and the recall is 92%" | single_source |
| Run-on correction: roCRF (uses POS and syntactic features) precision 0.83-0.89 on artificial data with 10% run-ons; roS2S precision 0.77-0.84 | Zheng et al. (Grammarly), arXiv preprint without peer review | https://arxiv.org/pdf/1809.08298 | 2018-09-21 | B | "roCRF has very high precision (0.83 <= P <= 0.89) but low recall, meaning that it does not generalize as well" | single_source |
| On naturally occurring run-ons (about 1% of sentences), precision falls: roCRF P 0.34 / R 0.27, roS2S P 0.30 / R 0.32 on RealESL; a punctuation-restoration model scored P 0.11 | same | https://arxiv.org/pdf/1809.08298 | 2018-09-21 | B | Table 4 RealESL: "roCRF 0.34 0.27 0.32", "roS2S 0.30 0.32 0.31", "Punctuator-RO 0.11 0.31 0.13" (table rows) | single_source |
| Authors attribute the Punctuators' low precision to predicting punctuation at every position, and roCRF's higher precision to POS and syntactic features restricting false positives | same | https://arxiv.org/pdf/1809.08298 | 2018-09-21 | B | "roCRF consistently has the highest precision because it is the only model to use POS and syntactic features" (paper words it as speculation) | single_source |
| Test-set base rate: only 1% of sentences in RealESL are run-ons | same | https://arxiv.org/pdf/1809.08298 | 2018-09-21 | B | "Only 1% of sentences in RealESL are run-ons, which may not be the case in other forms of ESL corpora." | single_source |
| Grammarly (research team) states a whole-sentence GEC model did not correct run-ons and that run-ons are long-distance, sentence-level errors | same | https://arxiv.org/pdf/1809.08298 | 2018-09-21 | B | "a leading GEC model (Chollampatt and Ng, 2018) does not correct any run-on sentences" | single_source |
| LanguageTool issue #719 (opened 3 Jun 2017): "I went to the park, it was sunny." is accepted as correct; no maintainer reply visible in the fetched page | LanguageTool GitHub issue tracker (user report) | https://github.com/languagetool-org/languagetool/issues/719 | 2017-06-03 | C | no quote | single_source |
| textlint-rule-max-comma counts commas per sentence only (default max 4, reports at 5 or more); documentation mentions no lists, splices or false-positive rates | textlint-rule organisation README | https://github.com/textlint-rule/textlint-rule-max-comma | unknown | B | "report an error if the sentence include 5 or more `,`" | single_source |
| Rule-writing guidance from LanguageTool: overly general patterns create false positives and lower precision | LanguageTool project docs | https://github.com/languagetool-org/languagetool-org.github.io/blob/master/how-to-avoid-mistakes-when-writing-rules.md | unknown | B | no quote (known from search snippet only, page not opened) | single_source |

## Falsifier
| Query | What came back | Does it change the answer |
|---|---|---|
| "rule-based comma splice checker high precision no parser regular expression POS tags evaluation false positive rate" (plus 2 more rule-based queries and a github.com/vale.sh/forum.languagetool.org sweep) | No published precision figure for a regex or POS-only comma-splice rule. Closest items: Lee et al.'s POS-only baseline (P 0.75 and 0.88 but recall 0.08-0.17, trained CRF, not hand rules) and MS Word's rule-based checker (P 0.74 / 0.90, recall 0.13-0.15). Nothing was found in Vale, proselint, write-good or textlint trackers about comma-splice rules. | No. No pattern-based detector reported with high precision on ordinary prose was found. The two sub-0.90 precision cases above come with recall of 0.17 or lower and were measured on learner text, not ordinary prose. Absence from the trackers is a search result, not proof that no such rule exists. |

## Search log
| Query | Facet | Sources adopted |
|---|---|---|
| LanguageTool comma splice rule false positives issue | practice | LanguageTool issue #719; LanguageTool rule-writing guide |
| comma splice detection run-on sentence automatic detection precision recall | data | Lee et al. 2014; Zheng et al. 2018 |
| textlint rule comma splice OR "run-on" OR "max-comma" English | definition | textlint-rule-max-comma |
| Vale style comma splice rule regex proselint write-good "comma splice" | practice | none (only generic grammar pages) |
| rule-based comma splice detector part-of-speech patterns high precision evaluation | falsifier | none new |
| rule-based comma splice checker high precision no parser regular expression POS tags evaluation false positive rate | falsifier | none new |
| comma splice rule Vale OR proselint OR write-good OR textlint github issue (allowed_domains github.com, vale.sh, forum.languagetool.org) | practice (primary sweep) | none; only unrelated Vale adoption issues |

## Gaps
- No Vale, proselint or write-good issue or documentation on comma-splice detection was found (two queries, including a github.com/vale.sh/forum.languagetool.org sweep). Reading the Vale styles' rule files directly would settle it.
- LanguageTool's own comma-splice-related rule (if any) and its measured false-positive rate were not found; the forum thread "Advice on reducing these false positives?" and the rule list at community.languagetool.org were not opened.
- No study scores a hand-written regex or POS-pattern rule on lists versus introductory phrases; evidence is limited to a trained CRF with POS-only features and MS Word. Both studies use learner English, not ordinary prose; ordinary-prose precision is unmeasured.
- Scholarly floor: one peer-reviewed paper plus one preprint; only 2 independent sources with figures. Both figure sets are single_source each. The LanguageTool rule-writing guide row rests on a search snippet, not an opened page.
- Several quotes for tabular figures are table rows, not sentences; textlint README and LanguageTool issue have no date.
