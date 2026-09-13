# -*- coding: utf-8 -*-
"""
Contrôle le build de Portet (dist/) : chaque page a un seul H1, un titre et
une description aux bonnes longueurs, une URL canonique juste, un JSON-LD
qui se lit ; chaque <img> a un texte alternatif (vide seulement si décorative) ;
chaque lien interne mène à une page du build ; les cartes de discipline sont
des liens. Usage : python verifier_portet_dist.py
"""
import io, json, os, re, sys
from html import unescape
sys.stdout.reconfigure(encoding='utf-8')
DIST = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Portet', 'boxing-center-portet', 'dist')
ORIGIN = 'https://boxing-center-portet.fr'

pages = {}
for racine, _, fichiers in os.walk(DIST):
    if 'index.html' in fichiers and os.sep + 'md' not in racine:
        chemin = '/' + os.path.relpath(racine, DIST).replace(os.sep, '/').strip('./') + '/'
        chemin = chemin.replace('//', '/')
        pages[chemin] = io.open(os.path.join(racine, 'index.html'), encoding='utf-8').read()

constats = []
titres, descs = {}, {}
for chemin, h in sorted(pages.items()):
    t = unescape((re.search(r'<title>([\s\S]*?)</title>', h) or [None, ''])[1]).strip()
    d = re.search(r'<meta name="description" content="([^"]*)"', h)
    d = unescape(d.group(1)) if d else ''
    can = re.search(r'<link rel="canonical" href="([^"]*)"', h)
    h1 = len(re.findall(r'<h1[\s>]', h))
    if h1 != 1: constats.append(f'{chemin} — {h1} <h1>')
    if not t or len(t) > 65: constats.append(f'{chemin} — titre de {len(t)} car.')
    if not d or len(d) > 165: constats.append(f'{chemin} — description de {len(d)} car.')
    if t in titres: constats.append(f'{chemin} — même titre que {titres[t]}')
    titres.setdefault(t, chemin)
    if d and d in descs: constats.append(f'{chemin} — même description que {descs[d]}')
    if d: descs.setdefault(d, chemin)
    if chemin != '/404/' and (not can or can.group(1) != ORIGIN + chemin):
        constats.append(f'{chemin} — canonical : {can.group(1) if can else "absente"}')
    for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>([\s\S]*?)</script>', h):
        try: json.loads(m.group(1))
        except Exception as ex: constats.append(f'{chemin} — JSON-LD illisible : {ex}')
    for m in re.finditer(r'<img\b[^>]*>', h):
        tag = m.group(0)
        alt = re.search(r'\salt(="([^"]*)")?[\s/>]', tag)
        deco = 'aria-hidden="true"' in tag
        if not alt: constats.append(f'{chemin} — <img> sans alt : {tag[:90]}')
        elif not (alt.group(2) or '').strip() and not deco: constats.append(f'{chemin} — <img> alt vide non décorative : {tag[:90]}')
    for m in re.finditer(r'href="(/[^"#?]*)"', h):
        cible = m.group(1)
        if re.search(r'\.[a-z0-9]{2,5}$', cible) or cible.startswith(('/api/', '/assets/', '/img/', '/md/')): continue
        cible = cible if cible.endswith('/') else cible + '/'
        if cible not in pages: constats.append(f'{chemin} — lien interne mort : {cible}')

accueil = pages.get('/', '')
act = pages.get('/activites/', '')
liens_reel = re.findall(r'<a class="reel__frame" href="(/activites/[a-z-]+/)"', accueil)
liens_act = re.findall(r'<a class="disc disc--img" href="(/activites/[a-z-]+/)"', act)
print(f'{len(pages)} pages dans le build')
print(f'cartes-liens : accueil {len(liens_reel)} (bandeau) · activités {len(liens_act)}')
print(f'pages de discipline : {len([p for p in pages if p.startswith("/activites/") and p != "/activites/"])}')
print(f'{len(constats)} constat(s)')
for c in sorted(set(constats)):
    print('  ·', c)
