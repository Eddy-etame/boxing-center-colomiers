# -*- coding: utf-8 -*-
"""
Les vignettes de /conseils/ sur Ramonville : l'index
(public/assets/img/ram/og/conseils.jpg) et une par article
(public/assets/img/ram/og/conseils/<slug>.jpg), 1200 x 630.

Chaque carte a sa photo — règle d'Eddy : jamais la même vignette. Le texte
et la photo viennent de src/conseils-pages.json (clé « og », et « photo »).
Même méthode que og_ramonville_disciplines.py : la typographie, le voile et
la signature de scripts/cartes-sociales.py sont repris tels quels.
Usage : python og_ramonville_conseils.py
"""
import io, json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')

RAMONVILLE = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment', 'bc-ramonville')
source = io.open(os.path.join(RAMONVILLE, 'scripts', 'cartes-sociales.py'), encoding='utf-8').read()
debut = source.index('# ------------------------------------------------------------------ les cartes')
tete = re.sub(r'^RACINE = .*$', lambda m: 'RACINE = ' + repr(RAMONVILLE), source[:debut], count=1, flags=re.M)
ns = {'__name__': 'cartes_ramonville'}
exec(compile(tete, 'cartes-sociales.py (tête)', 'exec'), ns)
i, j = source.index('def carte('), source.index('# ------------------------------------------------------------------ production')
exec(compile(source[i:j], 'cartes-sociales.py (carte)', 'exec'), ns)

data = json.load(io.open(os.path.join(RAMONVILLE, 'src', 'conseils-pages.json'), encoding='utf-8'))
og_dir = os.path.join(RAMONVILLE, 'public', 'assets', 'img', 'ram', 'og')
os.makedirs(os.path.join(og_dir, 'conseils'), exist_ok=True)
composer = os.path.join(RAMONVILLE, 'scripts', 'og-src', '_composer.cjs')

cartes = [('conseils', os.path.join('public', 'assets', 'img', 'ram', *data['index']['photo'].split('/')), data['index']['og'], os.path.join(og_dir, 'conseils.jpg'))]
for a in data['articles']:
    cartes.append((a['slug'], os.path.join('public', *a['photo']['src'].strip('/').split('/')), a['og'], os.path.join(og_dir, 'conseils', a['slug'] + '.jpg')))

photos = [c[1] for c in cartes]
assert len(set(photos)) == len(photos), 'deux vignettes partagent une photo'
for nom, rel, og, out in cartes:
    photo = os.path.join(RAMONVILLE, rel)
    assert os.path.exists(photo), photo
    svg = ns['carte'](photo, og['sur'], og['titre'], og['faits'])
    tmp = os.path.join(RAMONVILLE, 'scripts', 'og-src', '_conseil_%s.svg' % nom)
    io.open(tmp, 'w', encoding='utf-8').write(svg)
    r = subprocess.run(['node', composer, photo, tmp, out], capture_output=True, text=True, cwd=RAMONVILLE)
    os.remove(tmp)
    print('  %-28s %s' % (nom, (r.stdout or r.stderr).strip()[:80]))
