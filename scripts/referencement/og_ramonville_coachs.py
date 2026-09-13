# -*- coding: utf-8 -*-
"""
Les vignettes des pages de coach de Ramonville
(public/assets/img/ram/og/coachs/<slug>.jpg, 1200 x 630) : une par page,
jamais la même (règle d'Eddy). Même méthode que og_ramonville_disciplines.py :
on reprend TELS QUELS la typographie, le voile, le losange, la ligne de faits
et la signature de scripts/cartes-sociales.py ; seul son chemin RACINE est
remplacé. Le texte vient de src/coachs-pages.json (clé « og »), la photo est le
portrait officiel du coach.
Usage : python og_ramonville_coachs.py
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

PORTRAITS = {'jerome': 'coach-jerome.webp', 'sonia': 'coach-sonia.webp', 'hicham': 'coach-hicham.webp',
             'farouk': 'coach-farouk.webp', 'valentin-guth': 'coach-valentin.webp'}
pages = json.load(io.open(os.path.join(RAMONVILLE, 'src', 'coachs-pages.json'), encoding='utf-8'))['pages']
sortie = os.path.join(RAMONVILLE, 'public', 'assets', 'img', 'ram', 'og', 'coachs')
os.makedirs(sortie, exist_ok=True)
composer = os.path.join(RAMONVILLE, 'scripts', 'og-src', '_composer.cjs')

for nom, p in pages.items():
    og = p['og']
    photo = os.path.join(RAMONVILLE, 'public', 'assets', 'img', 'ram', PORTRAITS[p['slug']])
    assert os.path.exists(photo), f'portrait absent : {photo}'
    svg = ns['carte'](photo, og['sur'], og['titre'], og['faits'])
    tmp = os.path.join(RAMONVILLE, 'scripts', 'og-src', f'_coach_{p["slug"]}.svg')
    io.open(tmp, 'w', encoding='utf-8').write(svg)
    out = os.path.join(sortie, f'{p["slug"]}.jpg')
    r = subprocess.run(['node', composer, photo, tmp, out], capture_output=True, text=True, cwd=RAMONVILLE)
    os.remove(tmp)
    print(f'  {p["slug"]:16s} {(r.stdout or r.stderr).strip()[:80]}')
