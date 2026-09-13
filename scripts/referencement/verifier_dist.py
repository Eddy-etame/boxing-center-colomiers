# -*- coding: utf-8 -*-
"""
Contrôle un build statique (dist/) : chaque page indexable a un seul H1, un
titre et une description aux bonnes longueurs, une URL canonique juste, un
JSON-LD qui se lit ; chaque <img> a un texte alternatif (vide seulement si
décorative) ; chaque lien interne mène à une page du build.
Usage : python verifier_dist.py <dossier dist> <https://domaine> [préfixe de pages à détailler]
"""
import io, json, os, re, sys
from html import unescape
sys.stdout.reconfigure(encoding='utf-8')
DIST, ORIGIN = sys.argv[1], sys.argv[2].rstrip('/')
DETAIL = sys.argv[3] if len(sys.argv) > 3 else ''

pages = {}
for racine, dossiers, fichiers in os.walk(DIST):
    rel = os.path.relpath(racine, DIST).replace(os.sep, '/')
    if rel.split('/')[0] in ('md', 'admin', '_astro', 'assets'):
        continue
    if 'index.html' in fichiers:
        chemin = '/' if rel == '.' else '/' + rel.strip('/') + '/'
        pages[chemin] = io.open(os.path.join(racine, 'index.html'), encoding='utf-8').read()

constats, titres, descs = [], {}, {}
for chemin, h in sorted(pages.items()):
    noindex = re.search(r'<meta name="robots" content="[^"]*noindex', h)
    t = unescape((re.search(r'<title>([\s\S]*?)</title>', h) or [None, ''])[1]).strip()
    d = re.search(r'<meta name="description" content="([^"]*)"', h)
    d = unescape(d.group(1)) if d else ''
    can = re.search(r'<link rel="canonical" href="([^"]*)"', h)
    h1 = len(re.findall(r'<h1[\s>]', h))
    if not noindex:
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
        alt = re.search(r'\salt(?:=(?:"([^"]*)"|([^\s>]*)))?(?=[\s/>])', tag)
        deco = 'aria-hidden="true"' in tag or 'role="presentation"' in tag
        if not alt: constats.append(f'{chemin} — <img> sans alt : {tag[:90]}')
        elif not ((alt.group(1) or alt.group(2) or '').strip()) and not deco:
            constats.append(f'{chemin} — <img> alt vide non décorative : {tag[:90]}')
    for m in re.finditer(r'href="(/[^"#?]*)"', h):
        cible = m.group(1)
        if re.search(r'\.[a-z0-9]{2,12}$', cible) or cible.startswith(('/api/', '/assets/', '/img/', '/md/', '/_astro/', '/admin')):
            continue
        cible = cible if cible.endswith('/') else cible + '/'
        if cible not in pages: constats.append(f'{chemin} — lien interne mort : {cible}')

print(f'{len(pages)} pages dans le build')
if DETAIL:
    sous = [p for p in pages if p.startswith(DETAIL) and p != DETAIL]
    print(f'pages sous {DETAIL} : {len(sous)} → {", ".join(sous)}')
    motif_liens = re.compile('href="' + re.escape(DETAIL) + '[a-z-]+/"')
    for p in sous:
        h = pages[p]
        n_titre = len(unescape(re.search(r'<title>([^<]*)', h).group(1)))
        n_h1 = len(re.findall(r'<h1[\s>]', h))
        n_img = len(re.findall(r'<img', h))
        n_ld = len(re.findall(r'ld\+json', h))
        n_liens = len(motif_liens.findall(h))
        print(f'  {p:32s} titre {n_titre} · h1 {n_h1} · img {n_img} · ld {n_ld} · liens-disc {n_liens}')
print(f'{len(constats)} constat(s)')
for c in sorted(set(constats)):
    print('  ·', c)
