# -*- coding: utf-8 -*-
"""
Remplace le tableau CONTENUS d'un site par un bloc réécrit, en refusant
d'écrire si ce qui porte le référencement bouge : ids, h1, photos, et
tout titre (bloc ou FAQ) qui nomme la ville. Garde la fin de ligne du fichier.
Usage : python remplacer_contenus2.py <site> <bloc.ts> <Ville>
"""
import io, os, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment')
site, bloc, ville = sys.argv[1], sys.argv[2], sys.argv[3]
p = os.path.join(BASE, 'boxing-center-' + site, 'src', 'data', 'contenus.ts')
crlf = b'\r\n' in io.open(p, 'rb').read()
t = io.open(p, encoding='utf-8').read()
neuf = io.open(bloc, encoding='utf-8').read().strip()
debut = t.index('export const CONTENUS')
fin = t.index('] as const;', debut) + len('] as const;')
ancien = t[debut:fin]


def lignes(s, cle):
    return [l.strip() for l in s.splitlines() if l.strip().startswith(cle)]


for cle in ("id: '", "h1: '", "photoHero: '", "photoSecondaire: '"):
    a, n = lignes(ancien, cle), lignes(neuf, cle)
    assert a == n, cle + ' différent :\n' + '\n'.join(a) + '\n---\n' + '\n'.join(n)
porteurs = [l for l in lignes(ancien, 'titre: ') if ville in l]
restants = lignes(neuf, 'titre: ')
perdus = [l for l in porteurs if l not in restants]
assert not perdus, 'titres qui nomment la ville perdus : ' + repr(perdus)
q = chr(39)
for l in neuf.splitlines():
    if l.count(q) % 2:
        raise SystemExit('apostrophe droite dans une chaîne : ' + l[:90])
t = t[:debut] + neuf + t[fin:]
io.open(p, 'w', encoding='utf-8', newline='\r\n' if crlf else '\n').write(t)
print(site, ': CONTENUS remplacé —', len(lignes(neuf, "id: '")), 'pages ; ids, h1, photos et',
      len(porteurs), 'titres qui nomment la ville intacts')
