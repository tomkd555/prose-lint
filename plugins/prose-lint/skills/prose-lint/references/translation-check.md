# Comparing a translation with its source

The material the comparing agent in Step 3c works from. It covers English to Japanese and Japanese
to English. A fluent target can hide a change of meaning, so this step reads source and target
side by side and proposes no wording.

## Why the comparison stands apart from the rewrite

Three findings set the shape of Step 3c.

- One generic refinement pass gives the best result. Across eight language directions, en-ja among
  them, "most gains come from self-refinement", "with the best results achieved after a single step
  of self-refinement" 〔Wu2025〕.
- Refinement moves text toward the refiner's own wording: "a projection toward the refiner's
  preferred distribution rather than targeted error repair" 〔Refine2026〕.
- An LLM judge marks candidates, and the session rules on each one. No study found in the survey
  of 2026-11-08 measured span-level agreement for Japanese and English.

So the comparison answers questions, and the rewrite is one pass over the answers.

## The questions

Ask each question of every section, source and target open. Accuracy is the one category of the
JTF guideline that needs both texts 〔JTF2018〕. Terminology follows MQM's definition, which includes
"the correct, normative equivalent of the corresponding term in the source text" 〔MQM〕. MQM's
Accuracy holds addition, mistranslation and omission; the mistranslation rows below split out the
forms found in real English to Japanese pairs. Each answer of YES is one finding.

| id | Family | Question |
| --- | --- | --- |
| `shift-omission` | Accuracy | Does the source state something the target leaves out, such as a qualifier, a scope or a reason? |
| `shift-addition` | Accuracy | Does the target state something the source does not? |
| `shift-attachment` | Accuracy | Does a modifier or an argument attach to something else in the target? |
| `shift-modality` | Accuracy | Does the certainty or obligation differ, such as "may" stated as fact, or a recommendation stated as a requirement? |
| `shift-negation` | Accuracy | Does the target deny something else, or something more or less, than the source denies? |
| `shift-count` | Accuracy | Does a count or a singular reading differ, such as "a single study" written with no number? |
| `shift-sense` | Accuracy | Does the target give a word a meaning the source word lacks here? |
| `term` | Terminology | Is one source term given two target terms, or a term the glossary fixes given another? |

Leave style and fluency out: the layers of Step 3a or 3b read the target afterwards.

## Severity

Take the severity from the JTF guideline's definitions:

- Critical: 「翻訳成果物の使用が不適当となるエラー。」
- Major: 「翻訳成果物の理解しやすさや使いやすさに影響を与えうるエラー。」
- Minor: 「翻訳成果物の理解しやすさや使いやすさに大きな影響を与えないエラー。」

## Output

One finding per line:

`<source line> | <target line> | <id> | <severity> | "<source text>" | "<target sentence>" | <what differs, in one sentence>`

The target sentence is quoted whole. The line states the difference and leaves the wording to the
rewrite. Report every finding, with no severity filter.

## Sources

- 〔Wu2025〕 Wu, Aycock and Monz, "Please Translate Again: Two Simple Experiments on Whether
  Human-Like Reasoning Helps Translation", EMNLP 2025. https://arxiv.org/abs/2506.04521
- 〔Refine2026〕 "What Does LLM Refinement Actually Improve? A Systematic Study on Document-Level
  Literary Translation", ACL 2026. https://aclanthology.org/2026.acl-long.268.pdf
- 〔JTF2018〕 日本翻訳連盟, JTF 翻訳品質評価ガイドライン 第1版, 2018-11-15.
  https://www.jtf.jp/pdf/jtf_translation_quality_guidelines_v1.pdf
- 〔MQM〕 The MQM error typology. https://themqm.org/error-types-2/typology/
