"""bizreport.py - the tables of the business-document measurement, as Markdown on stdout.

    FLOW_PY=<skill dir>/scripts/flow.py python3 bizreport.py     (run in the corpus directory)

Reads flow2/, words-human.json, words-gen.json, sent/, sent6/, gensent/ and their -layers.json files,
as report.py does for the administrative set.
"""
import json, re, statistics as st, subprocess, os
from collections import Counter, defaultdict
JA_BLOCKING = {"ja-no-redundant-expression", "ja-no-abusage", "ja-no-successive-word", "no-doubled-conjunctive-particle-ga","no-double-negative-ja", "no-dropping-the-ra", "no-dropping-i", "no-insert-dropping-sa", "no-filler", "no-mix-dearu-desumasu","prefer-tari-tari", "ja-keishikimeishi", "ja-hiragana-hojodoushi", "ja-hiragana-daimeishi", "ja-hiragana-fukushi", "prh"}
JA_ADVISORY = {"no-doubled-joshi", "no-doubled-conjunction", "sentence-length", "max-ten", "max-kanji-continuous-len","no-ai-hype-expressions", "ai-tech-writing-guideline", "no-ai-words", "no-synonyms", "ja-no-weak-phrase"}
GROUPS = {'Press releases (日立, 富士通, NEC, 楽天, ソフトバンク, NRI; 2021)': ('hi', 'fj', 'nec', 'rk', 'sb', 'nri'), 'Engineering blog posts (サイボウズ, 2021-12)': ('cb',), 'Security alerts (JPCERT/CC, 2021)': ('jc',)}
PAIR = ['hi_1005', 'nec_20211007_01', 'cb_6', 'cb_1', 'jc_49', 'rk_1206_01']
g = lambda v: f'{v:g}'
P = lambda t, x: json.load(open(f'flow2/{t}_{x}.json'))['profile']
DOCS = sorted(f[2:-5] for f in os.listdir('flow2') if f.startswith('h_'))
W = json.load(open('words-human.json')); WG = json.load(open('words-gen.json'))
keys = [('mean_chars','Mean length'),('long_pct','100 characters or more %'),('short_pct','Under 30 characters %'),('connective_pct','Connective openers %'),('topic_open_pct','Topic openers %'),('paren_pct','Parenthesis %'),('joints_per_sentence','Joints per sentence'),('lone_pct','Lone %')]
print(f'## A. flow.py and words.py over {len(DOCS)} business documents (range, median in parentheses)\n')
print('| Kind | Documents | Sentences | ' + ' | '.join(l for _, l in keys) + ' | Katakana words per 1,000 characters |'); print('|' + ' --- |' * (len(keys) + 4))
def row(name, ds):
    ps = [P('h', x) for x in ds]
    cells = [f'{g(min(p[k] for p in ps))}-{g(max(p[k] for p in ps))} ({g(round(st.median(p[k] for p in ps),2))})' for k, _ in keys]
    kat = [W[x]['katakana_per_1000'] for x in ds]
    print(f'| {name} | {len(ds)} | {sum(p["sentences"] for p in ps)} | ' + ' | '.join(cells) + f' | {g(min(kat))}-{g(max(kat))} ({g(round(st.median(kat),1))}) |')
for name, pres in GROUPS.items(): row(name, [x for x in DOCS if x.split('_')[0] in pres])
row('All', DOCS)
print('\nMarked flat:', [x for x in DOCS if P('h', x)['flat']])
print('\n## B. Six documents and drafts written from English notes of them (original > draft)\n')
keysb = [('sentences','Sentences')] + keys[:1] + [('length_cv','Length CV')] + keys[1:3] + [('plain_pct','Plain endings %')] + keys[3:]
print('| Figure | ' + ' | '.join(PAIR) + ' | Median | Draft lower / higher |'); print('|' + ' --- |' * (len(PAIR) + 3))
for k, l in keysb:
    hv = [P('h', x)[k] for x in PAIR]; gv = [P('g', x)[k] for x in PAIR]
    print(f'| {l} | ' + ' | '.join(f'{g(a)} > {g(b)}' for a, b in zip(hv, gv)) + f' | {g(round(st.median(hv),2))} > {g(round(st.median(gv),2))} | {sum(b<a for a,b in zip(hv,gv))} / {sum(b>a for a,b in zip(hv,gv))} |')
for k, l in (('katakana_per_1000', 'Katakana words per 1,000 characters'), ('lone_kanji_per_1000', 'One-kanji nouns standing alone per 1,000 characters')):
    hv = [W[x][k] for x in PAIR]; gv = [WG[x][k] for x in PAIR]
    print(f'| {l} | ' + ' | '.join(f'{g(a)} > {g(b)}' for a, b in zip(hv, gv)) + f' | {g(round(st.median(hv),2))} > {g(round(st.median(gv),2))} | {sum(b<a for a,b in zip(hv,gv))} / {sum(b>a for a,b in zip(hv,gv))} |')
marks = []
for x in PAIR:
    out = subprocess.run(['uv','run','-q','--no-project',os.environ['FLOW_PY'],'--before',f'human/{x}.md',f'gen/{x}.md'],capture_output=True,text=True).stdout
    marks.append(re.search(r'(\d+) of (\d+) figures', out).group(0))
print('| Figures `--before` marks flatter | ' + ' | '.join(m.split(' ')[0] for m in marks) + f' | of {marks[0].split(" ")[2]} | |')
fh = Counter(); fg = Counter(); ch = cg = 0
for x in PAIR:
    ch += W[x]['chars']; cg += WG[x]['chars']; fh.update(W[x]['frames']); fg.update(WG[x]['frames'])
print('\nSurface frames per 1,000 characters, original > draft: ' + ', '.join(f'{k} {1000*fh[k]/ch:.2f} > {1000*fg[k]/cg:.2f}' for k in fh))
fa = Counter(); ca = 0
for x in DOCS: ca += W[x]['chars']; fa.update(W[x]['frames'])
print('\nThe same frames over all the documents: ' + ', '.join(f'{k} {1000*fa[k]/ca:.2f}' for k in fa))
kc = Counter(); kd = Counter(); lk = Counter(); ld = Counter()
for x in DOCS:
    for w, n in W[x]['katakana_top']: kc[w] += n; kd[w] += 1
    for w, n in W[x]['lone_kanji_top']: lk[w] += n; ld[w] += 1
print('\nKatakana words in 6 documents or more (tokens, documents): ' + ', '.join(f'{w} ({n}, {kd[w]})' for w, n in kc.most_common(80) if kd[w] >= 6))
print('\nOne-kanji nouns standing alone, 4 times or more: ' + ', '.join(f'{w} {n}' for w, n in lk.most_common(40) if n >= 4) + f'. 語 alone: {lk["語"]}; 値 alone: {lk["値"]}.')
def sentlevel(lf, sd, docs):
    d = json.load(open(lf)); T = A = H = B = F = 0; rules = Counter(); blocked = 0
    for x in docs:
        r = d[x]; n = sum(1 for l in open(f'{sd}/{x}.md', encoding='utf-8') if l.strip()); by = defaultdict(set); bl = set(); fx = set()
        for m in r['textlint'][0]['messages']:
            rid = m['ruleId'].rsplit('/', 1)[-1]
            if rid in JA_BLOCKING: by[rid].add(m['line']); bl.add(m['line']); fx.add(m['line'])
            elif rid in JA_ADVISORY: by[rid].add(m['line'])
        for h in r['reg_general'].get('hits', []): by['register: ' + h['instead'][:12]].add(h['line']); bl.add(h['line']); fx.add(h['line'])
        for h in r['reg_translationese'].get('hits', []):
            by['translationese ' + (h.get('group') or '')].add(h['line'])
            if 'Rewrite' in (h.get('group') or ''): fx.add(h['line'])
        for f in r['koyobun'].get('findings', []):
            by[f['check']].add(f['line'])
            if f['check'] in ('nominal_ending', 'sasete_itadaku'): fx.add(f['line'])
        T += n; A += len(set().union(*by.values())) if by else 0; H += sum(len(v) for v in by.values()); B += len(bl); F += len(fx); blocked += bool(bl)
        for k, v in by.items(): rules[k] += len(v)
    return T, A, H, B, F, rules, blocked
print('\n## C. Sentences the mechanical layers flag\n')
a = sentlevel('sent-layers.json', 'sent', DOCS); h = sentlevel('sent6-layers.json', 'sent6', PAIR); d = sentlevel('gensent-layers.json', 'gensent', PAIR)
print('| Text | Sentences | With a hit % | Under a rule SKILL.md fixes % | Under a rule the write hook blocks on % | Hits by rule, per sentence | Documents the hook would block |'); print('|' + ' --- |' * 7)
for name, t, n in ((f'The {len(DOCS)} documents', a, len(DOCS)), ('The six of B', h, 6), ('Their six drafts', d, 6)):
    print(f'| {name} | {t[0]} | {100*t[1]/t[0]:.1f} | {100*t[4]/t[0]:.1f} | {100*t[3]/t[0]:.1f} | {t[2]/t[0]:.2f} | {t[6]} of {n} |')
print('\n| Rule | % of all sentences | % of the six originals | % of their drafts |'); print('| --- | --- | --- | --- |')
for k in sorted(set(a[5]) | set(d[5]), key=lambda k: -a[5][k]):
    if a[5][k] / a[0] < 0.01 and d[5][k] / d[0] < 0.01: continue
    print(f'| {k} | {100*a[5][k]/a[0]:.1f} | {100*h[5][k]/h[0]:.1f} | {100*d[5][k]/d[0]:.1f} |')
