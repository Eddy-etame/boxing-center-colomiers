# -*- coding: utf-8 -*-
"""
La vignette de /club-de-boxe-ramonville/ : public/assets/img/ram/og/club-de-boxe-ramonville.jpg,
1200 x 630, sur une photo qu'AUCUNE autre vignette n'utilise (le ring et la
fresque murale) — règle d'Eddy : jamais la même. Même méthode que
og_ramonville_pages.py : cartes-sociales.py repris tel quel, RACINE remplacée.
Les faits imprimés sont ceux de la page (data.js : ouverture 2019-09).
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

photo = os.path.join(RAMONVILLE, 'public', 'assets', 'img', 'ram', 'photos', 'ring-de-boxe-et-fresque-murale-boxing-center-ramonville-800.webp')
assert os.path.exists(photo), photo
svg = ns['carte'](photo, 'Boxing Center Ramonville', 'Le club de boxe', ['Depuis septembre 2019', 'Le plateau dehors · octogone de 7 m', 'Terminus du métro B'])
tmp = os.path.join(RAMONVILLE, 'scripts', 'og-src', '_club.svg')
io.open(tmp, 'w', encoding='utf-8').write(svg)
out = os.path.join(RAMONVILLE, 'public', 'assets', 'img', 'ram', 'og', 'club-de-boxe-ramonville.jpg')
r = subprocess.run(['node', os.path.join(RAMONVILLE, 'scripts', 'og-src', '_composer.cjs'), photo, tmp, out], capture_output=True, text=True, cwd=RAMONVILLE)
os.remove(tmp)
print('  club-de-boxe-ramonville', (r.stdout or r.stderr).strip()[:90])
