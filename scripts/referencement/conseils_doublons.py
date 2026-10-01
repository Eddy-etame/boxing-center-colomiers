# -*- coding: utf-8 -*-
"""
« Une phrase, un site » appliqué aux articles /conseils/ de toute la famille.

Lit le HTML produit de chaque site (le <main> de /conseils/ et de chaque
article), découpe en phrases, et signale toute phrase de six mots ou plus qui
existe sur deux sites — ou deux fois sur le même site. Sept sites sont tombés à
zéro page indexée le 19/09 pour avoir partagé leurs phrases : on mesure avant
de pousser, pas après.

Usage : python conseils_doublons.py            (tous les sites trouvés)
"""
import glob, html, io, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

BC = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center')
SITES = {
    'portet': os.path.join(BC, 'Portet', 'boxing-center-portet', 'conseils'),
    'ramonville': os.path.join(BC, 'Deployment', 'bc-ramonville', 'dist', 'conseils'),
    'blagnac': os.path.join(BC, 'Deployment', 'club-de-boxe-blagnac', 'dist', 'conseils'),
}
for s in ('colomiers', 'tournefeuille', 'cugnaux', 'muret', 'labege', 'lunion', 'castelginest'):
    racine = os.path.join(BC, 'Deployment', 'boxing-center-' + s)
    for d in (os.path.join(racine, '.vercel', 'output', 'static', 'conseils'), os.path.join(racine, 'dist', 'conseils'), os.path.join(racine, 'dist', 'client', 'conseils')):
        if os.path.isdir(d):
            SITES[s] = d
            break


def phrases(fichier):
    t = io.open(fichier, encoding='utf-8').read()
    m = re.search(r'<main[\s\S]*?</main>', t)
    t = m.group(0) if m else t
    t = re.sub(r'<(script|style|svg|nav)[\s\S]*?</\1>', ' ', t)
    t = re.sub(r'</(p|h1|h2|h3|li|td|th|summary|figcaption)>', ' . ', t)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    t = re.sub(r'\s+', ' ', t)
    for ph in re.split(r'(?<=[.!?:;])\s+', t):
        mots = re.findall(r"[a-zà-ÿœ0-9]+", ph.lower())
        if len(mots) >= 6 and not ph.lower().startswith('mis à jour le'):  # la date n'est pas du texte
            yield ' '.join(mots), ph.strip()


vues = {}
total = {}
for site, dossier in SITES.items():
    fichiers = glob.glob(os.path.join(dossier, '**', 'index.html'), recursive=True)
    if not fichiers:
        continue
    total[site] = 0
    for f in fichiers:
        page = os.path.relpath(os.path.dirname(f), dossier).replace('\\', '/')
        for cle, ph in phrases(f):
            total[site] += 1
            vues.setdefault(cle, []).append((site, page, ph))

partagees = {k: v for k, v in vues.items() if len({s for s, _, _ in v}) > 1}
# la même phrase sur l'index et sur l'article d'un site est voulue (le résumé de la carte) ; deux fois sur UNE page ne l'est pas
repetees = {k: v for k, v in vues.items() if len(v) != len({(s, p) for s, p, _ in v})}

print('sites lus :', ', '.join('%s (%d phrases)' % (s, n) for s, n in total.items()))
print('phrases partagées entre sites : %d' % len(partagees))
for k, v in partagees.items():
    print('  « %s »' % v[0][2][:140])
    print('     ' + ' · '.join('%s/%s' % (s, p) for s, p, _ in v))
print('phrases répétées sur une même page : %d' % len(repetees))
for k, v in repetees.items():
    print('  « %s » — %s' % (v[0][2][:140], ' · '.join('%s/%s' % (s, p) for s, p, _ in v)))
sys.exit(1 if partagees or repetees else 0)
