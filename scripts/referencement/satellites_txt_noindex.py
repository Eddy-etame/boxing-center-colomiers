# -*- coding: utf-8 -*-
"""
Satellites (7), 17/09 : les quatre fichiers pour les IA (llms.txt, llms-full.txt,
humans.txt, ai.txt) sortent du plan du site et reçoivent X-Robots-Tag: noindex.
Google les rangeait en « Explorée, actuellement non indexée » (vu sur Minimes
et Ramonville) : ce sont des fichiers pour les moteurs de réponse, pas des
pages de recherche. Les IA les lisent toujours (robots.txt les autorise).
Rejouable.
"""
import io, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment')
SITES = sys.argv[1:] or ['colomiers', 'muret', 'cugnaux', 'tournefeuille', 'labege', 'lunion', 'castelginest']
TXT = ['/llms.txt', '/llms-full.txt', '/humans.txt', '/ai.txt']
BLOC_AVANT = """  /* Les fichiers pour les moteurs de réponse : la fiche du site, sa version
     complète, l'équipe et les consignes aux agents. */
  const fichiers = ['/llms.txt', '/llms-full.txt', '/humans.txt', '/ai.txt']
    .map((c) => `  <url>\n    <loc>${SITE.origine}${c}</loc>\n    <priority>0.3</priority>\n  </url>`)
    .join('\n');

"""
for s in SITES:
    R = os.path.join(BASE, f'boxing-center-{s}')
    p = os.path.join(R, 'src', 'pages', 'sitemap.xml.ts')
    t = io.open(p, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in t else '\n'
    avant = BLOC_AVANT.replace('\n', nl)
    if avant in t:
        t = t.replace(avant, ('  /* Les fichiers pour les IA (llms, humans, ai) ne sont PAS dans le plan du\n'
                              '     site : Google les explorait comme des pages et les rangeait en « non\n'
                              '     indexée ». Ils reçoivent X-Robots-Tag: noindex (vercel.json). */\n').replace('\n', nl))
        t = t.replace(nl + '${fichiers}' + nl, nl)
        assert 'fichiers' not in t.replace('Les fichiers pour', ''), s
        io.open(p, 'w', encoding='utf-8', newline='').write(t)
        print(f'  {s:13s} sitemap : txt retirés')
    else:
        print(f'  {s:13s} sitemap : déjà fait' if '${fichiers}' not in t else f'  {s:13s} sitemap : MOTIF INTROUVABLE')
    v = os.path.join(R, 'vercel.json')
    j = json.load(io.open(v, encoding='utf-8'))
    deja = {h['source'] for h in j.get('headers', [])}
    ajout = 0
    for c in TXT:
        if c not in deja:
            j.setdefault('headers', []).append({'source': c, 'headers': [{'key': 'X-Robots-Tag', 'value': 'noindex'}]})
            ajout += 1
    if ajout:
        io.open(v, 'w', encoding='utf-8', newline='\n').write(json.dumps(j, ensure_ascii=False, indent=2) + '\n')
    print(f'  {s:13s} vercel.json : {ajout} règle(s) ajoutée(s)')
