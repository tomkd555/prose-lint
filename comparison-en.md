## 1. Answer

Nothing found can replace prose-lint as a whole. No candidate covers both Japanese and English, settles a style before rewriting, runs a fresh-context translationese reader, or keeps a user-grown register. The closest partial matches each replace at most one layer:
- **takusaotome ai-text-humanizer**: a Japanese regex detector with a 0-100 score.
- **ai-kousei**: 23 cited Japanese regex rules with profiles.
- **sloptrim**: 71 English patterns and a 0-100 score through Claude Code hooks.

Updates matter more than additions:
- `koyobun.py` accepts any `sudachipy>=0.6.8`, and sudachipy 0.7.0 brings a new dictionary binary format and API changes.
- Vale 3.24 and later silently turns off parts of ai-tells v1.37.0. The fixes exist on ai-tells `main` only, and the README asks only for "vale 3.x".
- natural-japanese moved from the tested 1.6.0 to 1.6.4 and added a reading-load category that SKILL.md does not list.

The one addition worth trying is **slopless**, an English-only textlint preset that fits the existing English textlint layer. It should go in only after the same false-positive measurement that was run on ai-tells.

## 2. Dependency updates

| Dependency | Pinned | Latest (date) | What changed | Action |
|---|---|---|---|---|
| sudachipy (+ sudachidict-core) | `sudachipy>=0.6.8`, `sudachidict-core>=20240409` in `scripts/koyobun.py` and `scripts/test_koyobun.py` (no upper bound) | 0.7.0 (2026-09-24); sudachidict-core/full 20261015 (2026-10-15) | Release notes on WorksApplications/sudachi.rs: new dictionary binary format V1 (system and user dictionaries must both be updated), API changes, and "Please pin the exact version when using this series" | **hold**: cap at `<0.7`, then run `test_koyobun.py` under 0.7.0 before lifting the cap. It is unverified whether sudachidict 20261015 uses the V1 format. Inference: an unbounded `>=` in inline script metadata lets uv resolve 0.7.0 on a fresh environment. |
| vale | README: "vale 3.x"; locally installed 3.17.1 | v3.25.1 (2026-10-22) | 3.24.0 added `vale test`. Per ai-tells #88, 3.24 changed the caret to match at paragraph start only and changed `%` handling. The sentence-initial adverbs in `ConclusionMarkers` (active in prose-lint) and `FormalTransitions` (already off) now fire only at paragraph start. | **hold** below 3.24 until ai-tells releases #88, and state the range in the README |
| ai-tells (vale package) | bare name in `assets/vale/.vale.ini` `Packages = proselint, ai-tells`, so `vale sync` takes the latest release | v1.37.0 (2026-09-15) | v1.32 to v1.37 added NegatedPair, CoordinatedReveal, FigurativeShape, ConsequenceClause/ConsequenceParticiple, a BareNames extension and FigurativeWorth. FigurativeWorth and ConsequenceClause are level error. After the release, #88 (Vale 3.24 repairs) and #89 (per-rule `vale test` cases) are unreleased. | **bump and re-measure** at the next release that contains #88 |
| natural-japanese | README: "tested with 1.6.0" | v1.6.4 (2026-10-28) | Changes by release:<br>• 1.6.0 shipped `newfacts.py`.<br>• 1.6.1 added `calques.py`.<br>• 1.6.2 runs `calques.py` and `newfacts.py` in quick mode.<br>• 1.6.3 stops rewriting everyday loanwords and renames the paragraph-sheet header from 段落ごとの確かめ to 段落ごとの確認.<br>• 1.6.4 adds a `sentence_in_paren` category to `lint.py --reading-load`.<br>Effect on prose-lint:<br>• `textcore.py`: one docstring line changed.<br>• The JSON findings of the main AI-smell lane are unchanged. | **bump**: update the tested version and add `sentence_in_paren` to the reading-load list in SKILL.md |
| sudachi-synonyms-dictionary | `^20.0.0` | 20.0.0 (2026-10-18) | Quarterly data refresh. Each release is a new major (17 to 20 in 2026), so `^` will not pick up 21. | **bump** by hand at each major; no-synonyms hit sets can shift |
| textlint-rule-prh | `^6.1.1` | 6.1.1 (2026-10-16) | The runtime dependency moved from prh ^5.4.4 to prh ^6.1.0, a major engine bump. The prh v6 notes show no change to matching (not verified). | **re-measure**: rerun the guard tests of `prh/koyobun-kana.yml` (their location was not checked) |
| @textlint-ja/textlint-rule-preset-ai-writing | `^1.7.0`; installed 1.7.0 | 1.7.0 (2026-05-13) | Nothing new after the pin | none |
| textlint | `^15.8.0` | 15.8.0 (2026-08-01) | MCP server on SDK v2, gh formatter grouping, chalk replaced by `styleText()`; no lint behaviour change | none |
| textlint-rule-preset-ja-technical-writing, preset-jtf-style, filter-rule-comments | `^12.0.2`, `^3.0.3`, `^1.3.0` | equal to the pins | Dependency bumps only | none |
| no-dropping-i, no-filler, no-insert-dropping-sa, no-synonyms, plugin-html, ja-hiragana-*, ja-keishikimeishi, no-start-duplicated-conjunction, prefer-tari-tari | pinned at latest | 2017-12-24 to 2024-11-19 | No releases; maintenance is stale | **hold** (watch for archiving; archive status not checked) |
| proselint (vale package) | bare name | v0.3.4 (2024-06-09) | The repo moved from errata-ai/proselint to vale-cli/proselint (BSD-3-Clause); last commit 2025-09-08; stale. The standalone proselint 0.16.0 is a separate project that prose-lint does not use. | **hold** |

## 3. Candidates

### Japanese

| Name | URL | What it does | Maintenance | Relation to prose-lint | Recommendation | Reason |
|---|---|---|---|---|---|---|
| ai-kousei | https://github.com/AidenLee0011/ai-kousei | Regex-only, 23 rules, each citing 公用文, JTF or textlint presets. Profiles commit/report/agent/customer. Reports findings and does not rewrite. Ships an MCP server and a git hook. The 77-rule selftest spans 6 languages. | active (last commit 2026-08-25) | duplicate of the register + morphology layers; the profiles are new | watch | Its own README says it falls short of textlint's coverage. The PyPI and npm installs return 404; only git works (old npm name `buntai-lint` 0.4.0 has no MCP). |
| textlint-rule-preset-ai-words-ja 1.2.1 | https://registry.npmjs.org/textlint-rule-preset-ai-words-ja | 53-entry AI-word list. An `allows` option suppresses chosen words. A second rule, `no-short-topic-comma`, flags a short topic plus a comma at the start of a sentence. | active | duplicate of the register's stock-phrase rows; `no-short-topic-comma` is new coverage | watch | `allows` weakens the README's reason for leaving it out (everyday words). A fix to `no-short-topic-comma` merged 2026-09-24 is unreleased. Measure against the 83 human documents before adopting. |
| textlint-rule-ja-hiraku 1.4.0 | https://registry.npmjs.org/textlint-rule-ja-hiraku | Opens kanji to kana; per-part-of-speech and per-word toggles | active | duplicate of the kana layer (4 hiragana rules + prh) | reject | 及び, 更に and 既に are opened by default (dictionaries unchanged since 2023-12-16). Toggles would only rebuild what prh already does. |
| textlint-rule-ja-ten-maru 1.0.0 | https://github.com/314systems/textlint-rule-ja-ten-maru | Unifies 読点 and 句点 | active | notation only | reject | Outside the wording layers |
| Shodo CLI 1.1.0 | https://pypi.org/project/shodo/ | Hosted proofreading through `shodo lint`; needs an account and token | stale (CLI last push 2024-11-15) | weaker than the textlint layer | reject | Sends text to a service; no 公用文 or AI-text checks seen |
| luft.co.jp AI Japanese Text Check | https://www.luft.co.jp/cgi/ai-ja-text-check.php | Web form, 15+ statistical items, three 0-100 scores | unknown | weaker than the natural-japanese score | reject | No CLI or API; the page calls its results reference values |
| ANLP 2026 B9-17 (林, 相澤) | https://www.anlp.jp/proceedings/annual_meeting/2026/pdf_dir/B9-17.pdf | Paper: identifies the source LLM of Japanese text at 98.2% (3 API models) and 93.0% (6 open models); Appendix A lists phrases per model | n/a | possible source for register rows | watch | No code or word list released; the Japanese glyphs did not render, so the phrase findings are unverified |

### English

| Name | URL | What it does | Maintenance | Relation to prose-lint | Recommendation | Reason |
|---|---|---|---|---|---|---|
| slopless 0.2.42 | https://github.com/berelevant-ai/slopless | English-only textlint preset plus CLI; 51 deterministic rules in 7 families (narrative family off by default); optional Jev checks call the TypeSafe API | active (release 2026-10-23, 338 stars, MIT) | partly duplicates ai-tells; fits the English textlint layer | adopt as layer, after measurement | Same engine as the existing layer. Jev must stay off because it sends text out. Needs the Go blog / Rust book false-positive run that ai-tells had. |
| unslopify 0.4.1 | https://github.com/youngfreezy/unslopify | Deterministic audit (formula, substance, wording, structure plus mechanical checks), `--fix`, `--brief`, a SKILL.md rewrite loop | active | duplicate of ai-tells + register | watch | Unreleased 0.4.2 makes dashes always fail; `--fix` conflicts with the no-autofix rule |
| dslop 0.2.2 | https://github.com/aaazzam/dslop | Rust binary on PyPI; pattern rules plus sentence-length CV, kurtosis and word-frequency dispersion; detect only | active by the 12-month rule (last commit 2026-04-24) | the rhythm metrics are new coverage for English (inference: prose-lint measures rhythm only for Japanese, through natural-japanese) | watch | Small (6 stars) and quiet for six months |
| llm-slop-detector 0.11.0 | https://github.com/mandakan/llm-slop-detector | VS Code, CLI and browser extensions; about 40 core rules and 14 packs including `claudeisms`; MCP server | active | duplicate of ai-tells | watch | `claudeisms` overlaps `AISigns.Chatbot`. The "500+ patterns" claim and the `npx llm-slop-detector` bin are unverified. |
| ammil-industries/vale-signs-of-ai-writing | https://github.com/ammil-industries/vale-signs-of-ai-writing | Vale port of Wikipedia's "Signs of AI writing" | active (rules NegativeParallelisms and StandInEndings 2026-10-22, unreleased) | duplicate of ai-tells | reject | Already left out in the README; CC BY-SA 4.0 |
| krishnasunkam/vale-ai-tells (`AiTells`) | https://github.com/krishnasunkam/vale-ai-tells | 17 rules, 6 at error; on the Vale hub as `AiTells` | active (v1.0.0 2026-08-25) | duplicate of ai-tells | reject | Name clash only; its style name differs, so it cannot be pulled in by mistake |
| wsc | https://github.com/theserverlessdev/wsc | 8 detectors, 98 words + 83 phrases + 12 structures; CLI, MCP, Action | active | duplicate of ai-tells | reject | Adds nothing ai-tells lacks for this use |
| SignsOfAI.Cli 0.8.1 | https://github.com/peopleworks/SignsofAI | .NET 0-100 scorer; some checks call a server | active | duplicate of ai-tells + score | reject | Needs a .NET install; partly online |
| Harper v3.0.0 | https://github.com/Automattic/harper | Grammar and spelling | active (Apache-2.0) | different job | reject | Unchanged since the September survey |

### Claude Code ecosystem

| Name | URL | What it does | Maintenance | Relation to prose-lint | Recommendation | Reason |
|---|---|---|---|---|---|---|
| takusaotome ai-text-humanizer | https://takusaotome.github.io/claude-skills-library/en/skills/ops/ai-text-humanizer/ | Japanese-only regex detector (`detect_ai_patterns.py`, 6 patterns, `--doc-type`), 0-100 score, three rewrite techniques; tests included | active (skill folder 2026-05-27, MIT) | possible replacement for the natural-japanese lint + score (inference: smaller pattern set) | watch | Narrower than natural-japanese, which is already integrated |
| og3-lab/ai-writing-fix 0.2.0 | https://github.com/og3-lab/ai-writing-fix | 13 genre rubrics, common AI-pattern list, `find_repeats.py` (sentence pairs with character-trigram overlap ≥0.35), two-pass editor agent | active (last commit 2026-10-14) | `find_repeats.py` is new coverage: prose-lint's own files have no scripted restatement finder (natural-japanese's lint not checked) | watch | License allows modification and business use but not redistribution, so it cannot be shipped. The test claim was measured on the chat route, not the plugin route. |
| sloptrim 0.9.6 | https://github.com/seyedehsanhadi/sloptrim | Local Python detector, 71 patterns (62 with a detector), 0-100 score; Node hooks score each saved prose file | active (Apache-2.0, about 410 stars, 2026-10-22) | possible replacement for the vale ai-tells layer (English) | watch | The strongest English alternative to ai-tells, but unmeasured against the prose-lint corpus; no Japanese fork |
| conorbronsdon/avoid-ai-writing v3.38.0 | https://github.com/conorbronsdon/avoid-ai-writing | Detect and rewrite skill; 74 pattern categories; deterministic detector of 54 types (npm `avoid-ai-writing-detector`, MCP, pre-commit) | active (2026-10-27, about 5.3k stars) | duplicate of the ai-tells layer | watch | English-calibrated; no Japanese adaptation |
| matsuikentaro1/humanizer-japanese | https://github.com/matsuikentaro1/humanizer-japanese | SKILL.md-only checklist, 33 checks in A-E plus a voice section F; derived from blader/humanizer | active by the 12-month rule (2 commits, 2026-03-23) | weaker than the reader + register | reject | No script; no LICENSE file |
| geonwoo-jeong/japanese-humanizer 0.1.0 | https://github.com/geonwoo-jeong/japanese-humanizer | Rewrites translationese and AI Japanese while keeping facts and negations; `profile-japanese-text.mjs` | active (one day, 2026-07-01, MIT) | duplicate of the reader | reject | No gain over the reader plus the exemplars |
| iKora128/stop-ai-slop-jp 0.1.1 | https://github.com/iKora128/stop-ai-slop-jp | Prompt-only; 6 structure and 8 vocabulary families, 17 example pairs | active (2026-06-11, MIT, 474 stars) | weaker than the register | watch | Possible source of register rows; each row would need the 83-document measurement |
| makotofalcon/humanizer-ja 1.0.0 | https://github.com/makotofalcon/humanizer-ja | Prompt-only fork of blader/humanizer; adds conjunction chains, kango runs and translationese katakana | active by the 12-month rule (2026-03-24) | weaker than the register + translationese register | reject | No script |
| finelagusaz/ja-writing-tools v1.0.1 | https://github.com/finelagusaz/ja-writing-tools | proofread-ja and refine-ja skills; no AI-smell checks | active (2026-10-10) | weaker than the textlint layer | reject | LLM proofreading that the textlint layer already covers mechanically; no LICENSE file |
| kousei | https://claudskills.com/skills/kousei/ | textlint proofreading with auto-fix | unknown | duplicate of the textlint layer | reject | Auto-fix is ruled out in SKILL.md "Reporting"; no repo or license named |
| Mapika/plainly | https://github.com/Mapika/plainly | PostToolUse hook on Write and Edit; scorer plus a haiku judge; CI mode | active by the 12-month rule (all commits 2026-05-23) | duplicate of the vale layer | reject | Its own README reports AUC 0.67 against 2026 frontier models (self-reported) |
| petems/unsloppify 0.1.1 | https://github.com/petems/unsloppify | CLI for dashes and banned phrases; structures are left to the LLM skill | active by the 12-month rule (2026-05-16) | weaker than ai-tells | reject | |
| HugoLopes45/llmstrip v0.3.4 | https://github.com/HugoLopes45/llmstrip | Rust, 34 rules; the README's PostToolUse hook matches `.*` and pipes every tool output to it | active by the 12-month rule (2026-03-29) | duplicate of ai-tells | reject | How much of the structural rules the binary covers is unclear |
| CrossNox/linnl 0.1.3 | https://github.com/CrossNox/linnl | Mostly LLM-judged rules; regex rules can be added | active | duplicate of the reader (English) | reject | Needs a Claude or Codex login or API key |
| blader/humanizer v3.1.0 | https://github.com/blader/humanizer | Rewrite-only, 26 patterns in sections A-F | active | weaker | reject | No detector |
| MohamedAbdallah-14/unslop 0.7.0 | https://github.com/MohamedAbdallah-14/unslop | Rewriter; its hooks inject the mode and do not lint files | active | weaker | reject | Rewrite-first; English only |

### Refuted and unreachable

- No candidate came back refuted or unreachable. Every verdict was confirmed or partial.
- Leads that could not be reached:
  - cfregly/claude-deslop: GitHub 404.
  - github.com/textlint-ja/textlint-rule-preset-ai-words-ja: 404; the real repo is p1ass/…, which was not fetched.
  - shodo.ink/api: 404; the Shodo developer docs returned 403.
  - npmjs.com page for ai-words-ja: 403; the registry JSON was used instead.

## 4. Recommended actions

1. **Cap sudachipy.** In `scripts/koyobun.py` and `scripts/test_koyobun.py`, change the inline dependency to `sudachipy>=0.6.8,<0.7`. Then run `test_koyobun.py` under 0.7.0 with sudachidict-core 20261015 before lifting the cap.
2. **State the supported Vale range.** In `README.md` (Requirements), change "vale 3.x" to "below 3.24" until ai-tells releases #88. Optionally have `scripts/setup.py` warn on `vale --version` ≥ 3.24 (inference: setup.py does not check the version today; only a grep was run). The local install is 3.17.1, so this machine is unaffected now.
3. **Move natural-japanese to 1.6.4.**
   - Change "tested with 1.6.0" to 1.6.4 in `README.md`.
   - Add `sentence_in_paren` to the reading-load list in `SKILL.md`, under "natural-japanese lint".
   - Check whether `references/forbidden-patterns.md` changed under the six restated register rows in `assets/vocabulary.sample.md`. Not checked.
4. **Re-measure ai-tells after its next release.** Wait for the release with #88, then rerun the Go blog / Rust book versus LLM-article comparison. Include ConsequenceClause, FigurativeWorth and BareNames, which are not in the disable list. Update `assets/vale/.vale.ini`, plus the tier lists in `SKILL.md` if families change. SKILL.md already lists `AI consequence clause`, `AI point verdict` and `AI value verdict` as advisory, so the tier list knows these families. The README does not say whether the measurement included them.
5. **Trial slopless as an English textlint preset**, with Jev off, on the same corpus. Adopt it only if it beats its false-positive rate on human prose. Files: `assets/textlint/package.json`, the English config in `assets/textlint/`, `SKILL.md` Step 3b, `README.md`.
6. **Refresh "Considered and left out"** in `README.md`:
   - ai-words-ja: now has `allows` and the `no-short-topic-comma` rule; still left out pending measurement.
   - ja-hiraku: per-word toggles exist, but the defaults still open 及び, 更に and 既に.
   - Add one row each for sloptrim, avoid-ai-writing, ai-kousei and og3-lab/ai-writing-fix (no redistribution) with today's reasons.
   - Note that sudachi-synonyms-dictionary needs a manual major bump in `assets/textlint/package.json`.

## 5. Gaps

Lenses and places that found nothing or were not searched:
- **Claude Code ecosystem**: the anthropics/claude-plugins-official subdirectories were not opened. In anthropics/skills, `academy-guide` was not opened. No first-party Anthropic anti-AI-writing feature was confirmed; the claude.ai "writing styles" claim rests on a third-party blog.
- **Unopened leads**:
  - zircote/human-voice, mike-coulbourn/claude-vibes, charlesjones-dev writing-humanize, softaworks humanizer
  - gonta223/humanizer-ja
  - etincel, smellcheck, humanize-cli, deslop (JMill)
  - the Zenn article on textlint-rule-preset-ai-writing as an MCP server (prose-lint already uses that preset)
- **English**: LanguageTool was not searched. The Vale hub catalog was not fetched by the English lens and could not be parsed by the upstream lens, so other new hub packages may exist. The Juzek and Ward word list (`incl.ods`) was not fetched.
- **Japanese**: no dedicated translationese textlint rule exists. No Japanese LLM proofreading CLI was found other than Shodo. No released academic word list was found.
- **"Considered and left out" tools**: no new releases were found, but their repos were not checked one by one. The changes in textlint-rule-stop-words 5.2.0 were not read.

Claims left unverified:
- ai-tells: "39 messages reworded" and "BareNames narrowed".
- prh v6: no change to matching behaviour.
- sudachidict 20261015: whether it uses dictionary format V1.
- llm-slop-detector: "500+ patterns", and whether `npx llm-slop-detector` resolves a bin.
- llmstrip: how much of the structural rules the binary covers.
- plainly: the 0.67 AUC (self-reported).
- slopless: that it has no autofix.
- kousei: the anti-AI checklist.
- Shodo: its detection claims and the 10,000-character free tier.
- ANLP B9-17: the phrase findings.
- og3-lab: the test result (measured on the chat route, not the plugin route).
- natural-japanese: whether 1.6.4 is installed locally (the two lenses disagree).
- Whether natural-japanese's own `lint.py` caps sudachipy.

Facts checked against prose-lint's files and this machine:
- `.vale.ini` installs ai-tells and proselint by bare name.
- `package.json` pins match the table.
- `koyobun.py` has no upper bound on sudachipy.
- The local vale is 3.17.1.

Nothing was installed or run against the new versions, and no prose-lint file was edited.