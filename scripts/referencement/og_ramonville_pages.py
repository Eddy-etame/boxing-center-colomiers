# -*- coding: utf-8 -*-
"""
Les vignettes de /about/ et /privacy/ (Ramonville) — les deux seules pages sans
image de partage (audit du 13/09). Une par page, jamais la même (règle d'Eddy),
chacune sur une photo qu'aucune autre vignette n'utilise. Même méthode que
og_ramonville_nos_clubs.py : cartes-sociales.py repris tel quel, RACINE remplacée.
Les faits imprimés sont ceux que la page /about/ écrit déjà.
"""
import io, os, re, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
RAMONVILLE = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment', 'bc-ramonville')
source = io.open(os.path.join(RAMONVILLE, 'scripts', 'cartes-sociales.py'), encoding='utf-8').read()
debut = source.index('# ------------------------------------------------------------------ les cartes')
tete = re.sub(r'^RACINE = .*$', lambda m: 'RACINE = ' + repr(RAMONVILLE), source[:debut], count=1, flags=re.M)
ns = {'__name__': 'cartes_ramonville'}
exec(compile(tete, 'cartes-sociales.py (tête)', 'exec'), ns)
i, j = source.index('def carte('), source.index('# ------------------------------------------------------------------ production')
exec(compile(source[i:j], 'cartes-sociales.py (carte)', 'exec'), ns)

PHOTOS = os.path.join(RAMONVILLE, 'public', 'assets', 'img', 'ram', 'photos')
CARTES = [
    ('about', 'coach-bras-croises-devant-l-octogone-boxing-center-ramonville-800.webp',
     'Boxing Center Ramonville', 'Le club', ['Octogone de 7 m · grand ring', '8 disciplines · 5 coachs', 'École dès 3 ans']),
    ('privacy', 'boxe-anglaise-garde-haute-boxing-center-ramonville-800.webp',
     'Boxing Center Ramonville', 'Vos données', ['Pas de compte', 'Pas de pisteur', 'Pas de mesure d’audience']),
]
for nom, photo, sur, titre, faits in CARTES:
    src = os.path.join(PHOTOS, photo)
    assert os.path.exists(src), src
    tmp = os.path.join(RAMONVILLE, 'scripts', 'og-src', f'_{nom}.svg')
    io.open(tmp, 'w', encoding='utf-8').write(ns['carte'](src, sur, titre, faits))
    out = os.path.join(RAMONVILLE, 'public', 'assets', 'img', 'ram', 'og', f'{nom}.jpg')
    r = subprocess.run(['node', os.path.join(RAMONVILLE, 'scripts', 'og-src', '_composer.cjs'), src, tmp, out], capture_output=True, text=True, cwd=RAMONVILLE)
    os.remove(tmp)
    print(' ', nom, (r.stdout or r.stderr).strip()[:90])
