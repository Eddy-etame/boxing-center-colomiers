# -*- coding: utf-8 -*-
"""
Les phrases que plusieurs sites partagent mot pour mot (ville neutralisée),
sur les pages INDEXABLES seulement — ce que Google compare vraiment.
Sortie : chaque phrase partagée par au moins N sites, avec les pages où elle
vit. C'est la liste de travail de la réécriture : on attaque le haut.

Usage : python phrases_partagees.py [N=2] [site…]
"""
import io, re, os, sys, glob, html
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')
BASE = r"C:\Users\Mommy Jayce\Desktop\Boxing Center\Deployment"
SITES = {'colomiers': 'Colomiers', 'muret': 'Muret', 'cugnaux': 'Cugnaux', 'tournefeuille': 'Tournefeuille',
         'labege': 'Labège', 'lunion': 'L’Union', 'castelginest': 'Castelginest'}
GENTILES = ['Columérins', 'Muretains', 'Cugnalais', 'Tournefeuillais', 'Labégeois', 'Unionais', 'Castelginestois']
N = int(sys.argv[1]) if len(sys.argv) > 1 else 2
FILTRE = sys.argv[2:]

def texte(h):
    h = re.sub(r'<(script|style|noscript|svg|template|header|footer|nav)[\s\S]*?</\1>', ' ', h)
    h = re.sub(r'<[^>]+>', '\n', h)
    return html.unescape(h)

index = defaultdict(set)      # phrase -> {(site, page)}
for s, ville in SITES.items():
    dist = os.path.join(BASE, f'boxing-center-{s}', '.vercel', 'output', 'static')
    for f in glob.glob(os.path.join(dist, '**', 'index.html'), recursive=True):
        h = io.open(f, encoding='utf-8', errors='ignore').read()
        if re.search(r'<meta name="robots" content="noindex', h): continue
        page = '/' + os.path.relpath(os.path.dirname(f), dist).replace('\\', '/').strip('./')
        t = texte(h).replace(ville, 'VILLE')
        for g in GENTILES: t = t.replace(g, 'GENTILE')
        for p in re.split(r'(?<=[.!?:;])\s+|\n+', t):
            p = re.sub(r'\s+', ' ', p).strip()
            if len(p.split()) >= 6:
                index[p.lower()].add((s, page))

lignes = []
for p, ou in index.items():
    sites = {s for s, _ in ou}
    if len(sites) >= N and (not FILTRE or sites & set(FILTRE)):
        lignes.append((len(sites), p, sorted(ou)))
lignes.sort(key=lambda x: (-x[0], x[2][0][1], x[1]))
par_page = defaultdict(int)
for n, p, ou in lignes:
    for s, pg in ou:
        if not FILTRE or s in FILTRE: par_page[(s, pg)] += 1
print(f'{len(lignes)} phrases partagées par ≥ {N} sites (pages indexables)\n')
print('Pages les plus touchées :')
for (s, pg), c in sorted(par_page.items(), key=lambda x: -x[1])[:25]:
    print(f'  {c:3d}  {s:13s} {pg}')
print()
for n, p, ou in lignes[:160]:
    pages = sorted({pg for _, pg in ou})
    print(f'[{n}] {p[:150]}\n      {", ".join(sorted({s for s, _ in ou}))} · {", ".join(pages)}')
