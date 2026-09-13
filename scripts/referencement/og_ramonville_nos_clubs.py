# -*- coding: utf-8 -*-
"""
La vignette de /nos-clubs/ (Ramonville) : public/assets/img/ram/og/nos-clubs.jpg,
1200 x 630, propre à la page (règle d'Eddy : jamais la même). Même méthode que
og_ramonville_coachs.py : cartes-sociales.py repris tel quel, RACINE remplacée.
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

photo = os.path.join(RAMONVILLE, 'public', 'assets', 'img', 'ram', 'photos', 'octogone-cours-vu-d-en-haut-boxing-center-ramonville-800.webp')
assert os.path.exists(photo), photo
svg = ns['carte'](photo, 'Le réseau Boxing Center', 'Nos 5 clubs', ['Ramonville · Portet · Minimes', 'Saint-Cyprien · États-Unis', 'Une offre Saison, cinq clubs'])
tmp = os.path.join(RAMONVILLE, 'scripts', 'og-src', '_nos_clubs.svg')
io.open(tmp, 'w', encoding='utf-8').write(svg)
out = os.path.join(RAMONVILLE, 'public', 'assets', 'img', 'ram', 'og', 'nos-clubs.jpg')
r = subprocess.run(['node', os.path.join(RAMONVILLE, 'scripts', 'og-src', '_composer.cjs'), photo, tmp, out], capture_output=True, text=True, cwd=RAMONVILLE)
os.remove(tmp)
print('  nos-clubs', (r.stdout or r.stderr).strip()[:80])
