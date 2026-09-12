# -*- coding: utf-8 -*-
"""
Phrases de discipline partagées d'un site à l'autre, lues dans les SOURCES
(src/data/contenus.ts), ville et gentilé neutralisés. Ne dépend d'aucun
build : sert de liste de travail pendant que les builds tournent.
"""
import io, re, sys
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')
BASE = r"C:\Users\Mommy Jayce\Desktop\Boxing Center\Deployment"
SITES = {'muret': 'Muret', 'cugnaux': 'Cugnaux', 'tournefeuille': 'Tournefeuille', 'labege': 'Labège',
         'lunion': 'L’Union', 'castelginest': 'Castelginest', 'colomiers': 'Colomiers'}
GENT = ['Muretains', 'Cugnalais', 'Tournefeuillais', 'Labégeois', 'Unionais', 'Castelginestois', 'Columérins']
CHAINE = re.compile(r"'((?:[^'\\]|\\.)*)'")
PAGE = re.compile(r"\n    id: '([a-z-]+)',([\s\S]*?)(?=\n    id: '|\n\] as const)")

par = defaultdict(set)
for s, v in SITES.items():
    t = io.open(rf'{BASE}\boxing-center-{s}\src\data\contenus.ts', encoding='utf-8').read()
    for m in PAGE.finditer(t):
        page, corps = m.group(1), m.group(2).replace(v, 'VILLE')
        for g in GENT: corps = corps.replace(g, 'GENTILE')
        for txt in CHAINE.findall(corps):
            for p in re.split(r'(?<=[.!?:;])\s+', txt):
                p = p.strip().lower()
                if len(p.split()) >= 6:
                    par[p].add((s, page))

compte = defaultdict(lambda: defaultdict(int))
total = defaultdict(lambda: defaultdict(int))
for p, ou in par.items():
    sites = {s for s, _ in ou}
    for s, pg in ou:
        total[s][pg] += 1
        if len(sites) >= 2: compte[s][pg] += 1
print('Par site et par page : phrases partagées avec un autre site / phrases de la page')
for s in SITES:
    print(f'  {s:13s}', ' · '.join(f'{pg} {compte[s][pg]}/{total[s][pg]}' for pg in sorted(total[s], key=lambda x: -compte[s][x])))
print('\nPartagées par au moins deux sites :')
for p, ou in sorted(par.items(), key=lambda x: (-len({s for s, _ in x[1]}), sorted(x[1])[0])):
    sites = sorted({s for s, _ in ou})
    if len(sites) >= 2:
        pages = sorted({pg for _, pg in ou})
        print(f'  [{len(sites)}] {p[:130]}\n        {", ".join(sites)} · {", ".join(pages)}')
