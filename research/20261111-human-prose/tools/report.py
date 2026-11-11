"""report.py - the tables of the 1.12.0 measurement, as Markdown on stdout.

    python3 report.py        (run in the corpus directory)

Reads, from the current directory: flow2/h_<id>.json and flow2/g_<id>.json (flow.py --json of each
human document and each draft), sent/ and gensent/ (one sentence to a paragraph, from sentsplit.py),
sent-layers.json and gensent-layers.json (layers_fast.py over those), layers-human.json and
layers-gen.json (layers.py over the documents as files), human/ and gen/ (the Markdown files).
"""
import json, re, sys, statistics as st
from collections import Counter, defaultdict
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
from kinds import KINDS, KIND_OF
JA_BLOCKING = {"ja-no-redundant-expression", "ja-no-abusage", "ja-no-successive-word", "no-doubled-conjunctive-particle-ga","no-double-negative-ja", "no-dropping-the-ra", "no-dropping-i", "no-insert-dropping-sa", "no-filler", "no-mix-dearu-desumasu","prefer-tari-tari", "ja-keishikimeishi", "ja-hiragana-hojodoushi", "ja-hiragana-daimeishi", "ja-hiragana-fukushi", "prh"}
JA_ADVISORY = {"no-doubled-joshi", "no-doubled-conjunction", "sentence-length", "max-ten", "max-kanji-continuous-len","no-ai-hype-expressions", "ai-tech-writing-guideline", "no-ai-words", "no-synonyms", "ja-no-weak-phrase"}
PAIR = ['w7', 'w4', 'n13', 'r4', 's_070', 'k4', 'm3', 'p4']
DOCS = list(KIND_OF)
P = lambda t, x: json.load(open(f'flow2/{t}_{x}.json'))['profile']
g = lambda v: f'{v:g}'
print(f'## A. flow.py over {len(DOCS)} human documents, by kind (range, median in parentheses)\n')
keys = [('sentences','Sentences'),('mean_chars','Mean length'),('length_cv','Length CV'),('long_pct','100+ chars %'),('short_pct','Under 30 chars %'),('plain_pct','Plain endings %'),('connective_pct','Connective openers %'),('topic_open_pct','Topic openers %'),('paren_pct','Parenthesis %'),('joints_per_sentence','Joints'),('lone_pct','Lone %')]
print('| Kind | Docs | ' + ' | '.join(l for _, l in keys) + ' | Judge % |'); print('|' + ' --- |' * (len(keys) + 3))
allp = {x: P('h', x) for x in DOCS}
for kind, ds in KINDS.items():
    ps = [allp[x] for x in ds]
    row = [f'{g(min(p[k] for p in ps))}-{g(max(p[k] for p in ps))} ({g(round(st.median(p[k] for p in ps),2))})' for k, _ in keys]
    j = [p['ending_pct']['judge'] for p in ps]
    print(f'| {kind} | {len(ds)} | ' + ' | '.join(row) + f' | {g(min(j))}-{g(max(j))} ({g(round(st.median(j),1))}) |')
row = [f'{g(min(p[k] for p in allp.values()))}-{g(max(p[k] for p in allp.values()))} ({g(round(st.median(p[k] for p in allp.values()),2))})' for k, _ in keys]
j = [p['ending_pct']['judge'] for p in allp.values()]
print(f'| all | {len(DOCS)} | ' + ' | '.join(row) + f' | {g(min(j))}-{g(max(j))} ({g(round(st.median(j),1))}) |')
tot = sum(p['sentences'] for p in allp.values())
print(f'\nBody sentences: {tot}. Marked flat: {[x for x,p in allp.items() if p["flat"]]}')
for k, l in keys:
    v = [p[k] for p in allp.values()]; q = st.quantiles(v, n=4)
    print(f'- {l}: quartiles {q[0]:.1f} / {q[1]:.1f} / {q[2]:.1f}')
print('\n## B. Eight documents and the drafts written from their notes (human > draft)\n')
print('| Figure | ' + ' | '.join(PAIR) + ' | Median | Drafts lower / higher |'); print('|' + ' --- |' * (len(PAIR) + 3))
for k, l in keys:
    hv = [P('h', x)[k] for x in PAIR]; gv = [P('g', x)[k] for x in PAIR]
    print(f'| {l} | ' + ' | '.join(f'{g(a)} > {g(b)}' for a, b in zip(hv, gv)) + f' | {g(round(st.median(hv),2))} > {g(round(st.median(gv),2))} | {sum(b<a for a,b in zip(hv,gv))} / {sum(b>a for a,b in zip(hv,gv))} |')
def sentlevel(layerfile, sdir, x):
    r = json.load(open(layerfile))[x]
    n = sum(1 for l in open(f'{sdir}/{x}.md', encoding='utf-8') if l.strip())
    by = defaultdict(set); fixl = set(); hookl = set()
    for m in r['textlint'][0]['messages']:
        rid = m['ruleId'].rsplit('/', 1)[-1]
        if rid in JA_BLOCKING: by['textlint ' + rid].add(m['line']); fixl.add(m['line']); hookl.add(m['line'])
        elif rid in JA_ADVISORY: by['textlint ' + rid].add(m['line'])
    for h in r['reg_general'].get('hits', []):
        by['register: ' + h['instead'][:12]].add(h['line']); fixl.add(h['line']); hookl.add(h['line'])
    for h in r['reg_translationese'].get('hits', []):
        by['translationese ' + (h.get('group') or '')].add(h['line'])
        if 'Rewrite' in (h.get('group') or ''): fixl.add(h['line'])
    for f in r['koyobun'].get('findings', []):
        by['koyobun ' + f['check']].add(f['line'])
        if f['check'] in ('nominal_ending', 'sasete_itadaku'): fixl.add(f['line'])
    al = set().union(*by.values()) if by else set()
    return n, len(al), len(fixl), len(hookl), sum(len(v) for v in by.values()), {k: len(v) for k, v in by.items()}
def pool(layerfile, sdir, docs):
    t = [0] * 5; rules = Counter(); blocked = 0
    for x in docs:
        r = sentlevel(layerfile, sdir, x)
        for i in range(5): t[i] += r[i]
        rules.update(r[5]); blocked += r[3] > 0
    return t, rules, blocked
print('\n## C. Sentences the mechanical layers flag (textlint, the general and translationese registers, koyobun.py; one sentence to a paragraph)\n')
ta, ra, ba = pool('sent-layers.json', 'sent', DOCS)
th, rh, bh = pool('sent-layers.json', 'sent', PAIR)
tg, rg, bg = pool('gensent-layers.json', 'gensent', PAIR)
print('| Text | Sentences | With any hit % | Under a rule the skill fixes % | Under a rule the hook blocks on % | Rule-sentence pairs per sentence | Documents the hook would block |'); print('|' + ' --- |' * 7)
for name, t, b, n in ((f'{len(DOCS)} human documents', ta, ba, len(DOCS)), ('the 8 human documents of B', th, bh, 8), ('their 8 drafts', tg, bg, 8)):
    print(f'| {name} | {t[0]} | {100*t[1]/t[0]:.1f} | {100*t[2]/t[0]:.1f} | {100*t[3]/t[0]:.1f} | {t[4]/t[0]:.2f} | {b} of {n} |')
print('\n| Rule | % of sentences, all human | % of sentences, the 8 human | % of sentences, their drafts |'); print('| --- | --- | --- | --- |')
for k in sorted(set(ra) | set(rg), key=lambda k: -ra[k]):
    if ra[k] / ta[0] < 0.004 and rg[k] / tg[0] < 0.004: continue
    print(f'| {k} | {100*ra[k]/ta[0]:.1f} | {100*rh[k]/th[0]:.1f} | {100*rg[k]/tg[0]:.1f} |')
def score(layerfile, x, path):
    r = json.load(open(layerfile))[x]['nj']; sev = Counter(f.get('severity') for f in r.get('findings', []))
    chars = len(re.sub(r'\s', '', open(path, encoding='utf-8').read()))
    return round(max(100 - (sev['critical'] * 8 + sev['warn'] * 4 + sev['info'] * 0.5) * (1000 / max(chars, 1000)), 20), 1)
print('\n## D. Naturalness score (natural-japanese quick tier, the reading-load lane included in the count)\n')
hs = [score('layers-human.json', x, f'human/{x}.md') for x in PAIR]; gs = [score('layers-gen.json', x, f'gen/{x}.md') for x in PAIR]
print('| | ' + ' | '.join(PAIR) + ' | Median |'); print('|' + ' --- |' * (len(PAIR) + 2))
print('| human | ' + ' | '.join(map(str, hs)) + f' | {st.median(hs)} |'); print('| draft | ' + ' | '.join(map(str, gs)) + f' | {st.median(gs)} |')
al = [score('layers-human.json', x, f'human/{x}.md') for x in DOCS]
print(f'\nAll {len(DOCS)} human documents: {min(al)} to {max(al)}, median {st.median(al)}.')
# whole-document hits per 100 sentences
d = json.load(open('layers-human.json')); cnt = Counter(); docs_with = defaultdict(set)
for x in DOCS:
    r = d[x]
    for m in r['textlint'][0]['messages']:
        rid = m['ruleId'].rsplit('/', 1)[-1]
        if rid in JA_BLOCKING | JA_ADVISORY: cnt['textlint ' + rid] += 1; docs_with['textlint ' + rid].add(x)
    for f in r['koyobun'].get('findings', []): cnt['koyobun ' + f['check']] += 1; docs_with['koyobun ' + f['check']].add(x)
    for f in r['nj'].get('findings', []): cnt['natural-japanese ' + f['category']] += 1; docs_with['natural-japanese ' + f['category']].add(x)
    for kind in ('general', 'translationese', 'slop'):
        for h in r['reg_' + kind].get('hits', []): cnt[f'register {kind}: ' + h['instead'][:14]] += 1; docs_with[f'register {kind}: ' + h['instead'][:14]].add(x)
print(f'\n## E. Hits in the {len(DOCS)} human documents as files (per 100 body sentences; documents with a hit)\n')
print('| Rule | Hits | Per 100 sentences | Documents |'); print('| --- | --- | --- | --- |')
for k, v in cnt.most_common(45): print(f'| {k} | {v} | {100*v/tot:.1f} | {len(docs_with[k])} |')
print(f'\nTotal of the rules above and the rest: {sum(cnt.values())} hits, {sum(cnt.values())/tot:.2f} per sentence.')
