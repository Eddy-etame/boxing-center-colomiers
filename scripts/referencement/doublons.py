# -*- coding: utf-8 -*-
"""
Le risque « pages satellites » (doorway) mesuré : pour chaque paire de sites,
la part de phrases visibles identiques une fois la ville neutralisée. Google
filtre les quasi-doublons entre domaines d'un même propriétaire ; un site dont
les pages sont à 60 % la copie d'un frère n'est pas classé, il est replié.
"""
import io, re, os, sys, glob, html, itertools
sys.stdout.reconfigure(encoding='utf-8')
BASE = r"C:\Users\Mommy Jayce\Desktop\Boxing Center\Deployment"
SITES = {'colomiers': 'Colomiers', 'muret': 'Muret', 'cugnaux': 'Cugnaux', 'tournefeuille': 'Tournefeuille',
         'labege': 'Labège', 'lunion': 'L’Union', 'castelginest': 'Castelginest'}
GENTILES = ['Columérins', 'Muretains', 'Cugnalais', 'Tournefeuillais', 'Labégeois', 'Unionais', 'Castelginestois']

def texte(h):
    h = re.sub(r'<(script|style|noscript|svg|template|header|footer|nav)[\s\S]*?</\1>', ' ', h)
    h = re.sub(r'<[^>]+>', '\n', h)
    return html.unescape(h)

def phrases(t, ville):
    t = t.replace(ville, 'VILLE')
    for g in GENTILES: t = t.replace(g, 'GENTILE')
    t = re.sub(r'\b\d{5}\b', 'CP', t)
    out = set()
    for p in re.split(r'(?<=[.!?:;])\s+|\n+', t):
        p = re.sub(r'\s+', ' ', p).strip().lower()
        if len(p.split()) >= 6: out.add(p)
    return out

corpus = {}
for s, ville in SITES.items():
    dist = os.path.join(BASE, f'boxing-center-{s}', '.vercel', 'output', 'static')
    ph = {}
    for f in glob.glob(os.path.join(dist, '**', 'index.html'), recursive=True):
        route = '/' + os.path.relpath(os.path.dirname(f), dist).replace('\\', '/').strip('.')
        h = io.open(f, encoding='utf-8', errors='ignore').read()
        if 'noindex' in h: continue
        r = route.replace('//', '/')
        r = r if r.endswith('/') else r + '/'
        ph[r] = phrases(texte(h), ville)
    corpus[s] = ph

print('Part des phrases de A que l’on retrouve mot pour mot chez B (ville neutralisée), toutes pages indexables :\n')
tout = {s: set().union(*ph.values()) for s, ph in corpus.items()}
print(' ' * 14 + ''.join(f'{b[:8]:>10}' for b in SITES))
for a in SITES:
    ligne = f'{a:14s}'
    for b in SITES:
        ligne += f'{"":>10}' if a == b else f'{100 * len(tout[a] & tout[b]) / max(1, len(tout[a])):9.0f}%'
    print(ligne)

print('\nPar page type (A = muret vs chaque frère) — les pages les plus copiées :')
for page in sorted(set().union(*[set(c) for c in corpus.values()]), key=lambda x: (x.count('/'), x)):
    ligne = f'  {page:22s}'
    for s in SITES:
        if page not in corpus[s]: ligne += f'{"-":>9}'; continue
        autres = set().union(*[corpus[o].get(page, set()) for o in SITES if o != s])
        a = corpus[s][page]
        ligne += f'{100 * len(a & autres) / max(1, len(a)):8.0f}%'
    print(ligne)
print('  ' + ' ' * 22 + ''.join(f'{s[:8]:>9}' for s in SITES))
