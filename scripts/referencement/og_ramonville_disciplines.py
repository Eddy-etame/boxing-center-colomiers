# -*- coding: utf-8 -*-
"""
Les huit vignettes des pages de discipline de Ramonville
(public/assets/img/ram/og/disciplines/<slug>.jpg, 1200 x 630).

On ne redessine rien : on reprend TELS QUELS la typographie (glyphes Chakra
Petch convertis en chemins), le voile, le losange, la ligne de faits et la
signature de scripts/cartes-sociales.py, le générateur de cartes du site.
Seul son chemin RACINE, périmé (sites\\bc-ramonville), est remplacé.
Le texte de chaque carte vient de src/disciplines-pages.json (clé « og »).
Usage : python og_ramonville_disciplines.py
"""
import io, json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')

RAMONVILLE = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment', 'bc-ramonville')
source = io.open(os.path.join(RAMONVILLE, 'scripts', 'cartes-sociales.py'), encoding='utf-8').read()

debut_cartes = source.index('# ------------------------------------------------------------------ les cartes')
tete = re.sub(r'^RACINE = .*$', lambda m: 'RACINE = ' + repr(RAMONVILLE), source[:debut_cartes], count=1, flags=re.M)
ns = {'__name__': 'cartes_ramonville'}
exec(compile(tete, 'cartes-sociales.py (tête)', 'exec'), ns)
i, j = source.index('def carte('), source.index('# ------------------------------------------------------------------ production')
exec(compile(source[i:j], 'cartes-sociales.py (carte)', 'exec'), ns)

pages = json.load(io.open(os.path.join(RAMONVILLE, 'src', 'disciplines-pages.json'), encoding='utf-8'))['pages']
sortie = os.path.join(RAMONVILLE, 'public', 'assets', 'img', 'ram', 'og', 'disciplines')
os.makedirs(sortie, exist_ok=True)
composer = os.path.join(RAMONVILLE, 'scripts', 'og-src', '_composer.cjs')

for cle, p in pages.items():
    og = p['og']
    photo = os.path.join(RAMONVILLE, 'public', *p['photo']['src'].strip('/').split('/'))
    svg = ns['carte'](photo, og['sur'], og['titre'], og['faits'])
    tmp = os.path.join(RAMONVILLE, 'scripts', 'og-src', f'_disc_{p["slug"]}.svg')
    io.open(tmp, 'w', encoding='utf-8').write(svg)
    out = os.path.join(sortie, f'{p["slug"]}.jpg')
    r = subprocess.run(['node', composer, photo, tmp, out], capture_output=True, text=True, cwd=RAMONVILLE)
    os.remove(tmp)
    print(f'  {p["slug"]:20s} {(r.stdout or r.stderr).strip()[:80]}')
