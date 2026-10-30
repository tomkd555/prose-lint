# Which published Vale styles ship a rule for comma splices, run-on sentences or comma-heavy sentences, and through which extension point does each work?

## Evidence
| Claim | Publisher | URL | Published | Grade | Quote | Corroboration |
|---|---|---|---|---|---|---|
| The occurrence extension point caps how often a token appears in a scope; the docs example counts commas per sentence (scope sentence, max 3, token ',') | Vale docs (vale.sh) | https://docs.vale.sh/checks/occurrence | unknown | B | "occurrence enforces the maximum or minimum number of times a particular token can appear in a given scope." | single_source |
| The occurrence docs ship a comma-cap example: "More than 3 commas!" | Vale docs (vale.sh) | https://docs.vale.sh/checks/occurrence | unknown | B | no quote (YAML example: extends: occurrence, scope: sentence, max: 3, token: ',') | single_source |
| The sequence extension point matches token sequences with part-of-speech tags and targets grammar rules; docs examples are infinitive-marker and ambiguous-pronoun rules, none for comma splices | Vale docs (vale.sh) | https://docs.vale.sh/checks/sequence | unknown | B | no quote ("support grammar-focused rules" is a fetch paraphrase) | single_source |
| The script extension point runs Tengo programs and fills a matches array with begin/end offsets | Vale docs (vale.sh) | https://docs.vale.sh/checks/script | unknown | B | "script allows for the creation of arbitrary logic-based rules using Tengo, a Go-like scripting language." (fetch transcription, not verified verbatim) | single_source |
| Microsoft style SentenceLength rule uses extends occurrence, scope sentence, max 30, token \b(\w+)\b (counts words, level suggestion) | vale-cli/errata-ai Microsoft repo | https://raw.githubusercontent.com/errata-ai/Microsoft/master/Microsoft/SentenceLength.yml | unknown | B | "Try to keep sentences short (< 30 words)." | single_source |
| Google style directory (38 files) holds no sentence-length, run-on or comma-splice rule; comma-related files are OxfordComma and Semicolons only | vale-cli Google repo | https://github.com/errata-ai/Google/tree/master/Google | unknown | B | no quote (directory listing) | single_source |
| Google Colons rule is an existence rule (token regex), scope sentence | vale-cli Google repo | https://raw.githubusercontent.com/errata-ai/Google/master/Google/Colons.yml | unknown | B | no quote | single_source |
| write-good style has 8 rule files (`Cliches, E-Prime, Illusions, Passive, So, ThereIs, TooWordy, Weasel`); none concerns commas, run-ons or sentence length | errata-ai write-good repo | https://github.com/errata-ai/write-good/tree/master/write-good | unknown | B | no quote (directory listing) | single_source |
| proselint style has 34 rule files (Airlinese ... Very); none concerns commas, run-ons or sentence length by file name | errata-ai proselint repo | https://github.com/errata-ai/proselint/tree/master/proselint | unknown | B | no quote (directory listing; file contents not opened) | single_source |
| vale-cli/Std library lists Readability.SentenceLength ("Sentences over 25 words", IBM origin) and Punctuation.OxfordComma; no run-on rule | vale-cli Std repo | https://github.com/vale-cli/Std | unknown | B | no quote | single_source |
| vale-ai-tells (tbhb) targets vocabulary and rhetorical patterns; closest punctuation rules are SemicolonUsage and ColonUsage; no comma-splice or run-on rule | tbhb/vale-ai-tells repo | https://github.com/tbhb/vale-ai-tells | unknown | B | no quote | single_source |
| Search snippets report 111 rule files in vale-ai-tells (variants krishnasunkam, theredspoon exist) | GitHub search snippet | https://github.com/tbhb/vale-ai-tells | unknown | C | no quote | single_source |
| Vale is documented as having twelve extension points, existence through script | vale.sh | https://vale.sh/features/extensible | unknown | B | no quote (search snippet) | single_source |

## Falsifier
| Query | What came back | Does it change the answer |
|---|---|---|
| Vale style "run-on" OR "comma splice" rule github yml "extends: sequence" OR "extends: script" (plus a second query on commas-per-sentence occurrence rules) | No published style with a comma-splice or run-on rule on sequence or script surfaced. Only the generic sequence and script docs and the occurrence comma-cap example came back. Directory listings of Google, write-good, proselint show no such file. Microsoft, RedHat, GitLab, alex, Joblint directories were not listed. | No change within the sampled styles; the search found nothing, which does not prove absence in unlisted styles. |

## Search log
| Query | Facet | Sources adopted |
|---|---|---|
| Vale styles comma splice run-on sentence rule write-good proselint Microsoft Google styles | definition | none (overview only) |
| Vale rule "comma splice" sequence tokens style yml | definition | none |
| Vale styles documentation extension points existence occurrence sequence metric script (vale.sh) | definition | vale.sh/features/extensible, docs.vale.sh checks |
| Vale ai-tells style GitHub AI writing patterns rules | data | tbhb/vale-ai-tells |
| Vale Google style SentenceLength Microsoft style SentenceLength rule yml occurrence max (github.com) | practice | vale-cli/Std, Microsoft |
| Vale style "run-on" OR "comma splice" ... sequence OR script | falsifier | none |
| Vale style package run-on sentences commas per sentence rule occurrence (github, vale.sh) | practice | docs.vale.sh/checks/occurrence |

## Gaps
- The directories of eight styles were not listed; only Microsoft SentenceLength was read. A listing of each would settle absence. The eight:
  - Microsoft
  - RedHat
  - GitLab
  - alex
  - Joblint
  - jdkato/fiction
  - Datadog
  - Elastic
- Contents of proselint and ai-tells rules were not opened; absence rests on file names and a README summary. Cloning the repos and grepping for "extends: sequence" and "extends: script" would settle it.
- Publication dates were not stated on any page (all unknown).
- Most key claims are single_source (each from one publisher's repo or docs); several quotes are fetch transcriptions or absent.
- Floor of 4 searches and 2 sources met in count; the independence of sources is weak because most come from vale.sh/errata-ai.
