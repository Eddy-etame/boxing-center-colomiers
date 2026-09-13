# -*- coding: utf-8 -*-
"""
La vignette de /contact/ (Ramonville) imprime le numéro : quand il change
(13/09 : 09 39 03 67 48), elle est refaite, et elle seule. cartes-sociales.py
repris tel quel jusqu'à sa production, puis la seule carte « contact ».
"""
import io, os, re, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
RAMONVILLE = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment', 'bc-ramonville')
os.chdir(RAMONVILLE)
source = io.open(os.path.join('scripts', 'cartes-sociales.py'), encoding='utf-8').read()
# le script vise encore l'ancien dossier (sites/bc-ramonville) : RACINE remplacée, comme og_ramonville_nos_clubs.py
source = re.sub(r'^RACINE = .*$', lambda m: 'RACINE = ' + repr(RAMONVILLE), source, count=1, flags=re.M)
fin = source.index('# ------------------------------------------------------------------ production')
ns = {'__name__': 'cartes_ramonville'}
exec(compile(source[:fin], 'cartes-sociales.py', 'exec'), ns)
exec(compile(source[fin:source.index('print("  CARTE')], 'cartes-sociales.py (composer)', 'exec'), ns)
nom, photo, sur, titre, faits = next(c for c in ns['CARTES'] if c[0] == 'contact')
assert any('09 39 03 67 48' in x for x in faits), faits
tmp = os.path.join('scripts', 'og-src', '_contact.svg')
io.open(tmp, 'w', encoding='utf-8').write(ns['carte'](photo, sur, titre, faits))
out = '%s/%s.jpg' % (ns['SORTIE'], nom)
r = subprocess.run(['node', 'scripts/og-src/_composer.cjs', 'public/assets/img/ram/' + photo, tmp, out], capture_output=True, text=True)
os.remove(tmp)
print('  contact', out, (r.stdout or r.stderr).strip()[:90])
