# -*- coding: utf-8 -*-
"""Les cinq dernières phrases partagées hors titres-mots-clés (Castelginest et Tournefeuille gardent les leurs)."""
import io, os, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment')
R = {
    'lunion': [
        ("'Trois groupes : 3/6 ans, 7/11 ans et 12/16 ans, au planning de la salle Boxe.",
         "'L’École de boxe réunit trois groupes, 3/6, 7/11 et 12/16 ans, au planning de la salle Boxe."),
        ("'Échauffement au rameur ou au vélo',",
         "'Rameur ou vélo pour chauffer',"),
        ("titre: 'Il faut acheter des protège-tibias ?',",
         "titre: 'Protège-tibias : à acheter tout de suite ?',"),
        ("'Une tenue de sport et une bouteille d’eau suffisent pour découvrir. Si ton enfant accroche,",
         "'Pour découvrir, prévois une tenue de sport et une bouteille d’eau. Si ton enfant accroche,"),
    ],
    'labege': [
        ("'Corde, puis mobilité des hanches et des chevilles',",
         "'Corde, puis hanches et chevilles déliées',"),
    ],
}
for site, paires in R.items():
    p = os.path.join(BASE, 'boxing-center-' + site, 'src', 'data', 'contenus.ts')
    crlf = b'\r\n' in io.open(p, 'rb').read()
    t = io.open(p, encoding='utf-8').read()
    fautes = [f'{t.count(v)}× « {v[:60]} »' for v, _ in paires if t.count(v) != 1]
    if fautes:
        print(site, ': RIEN ÉCRIT', *fautes, sep='\n  ')
        continue
    for v, n in paires:
        t = t.replace(v, n)
    io.open(p, 'w', encoding='utf-8', newline='\r\n' if crlf else '\n').write(t)
    print(site, ':', len(paires), 'retouches écrites')
