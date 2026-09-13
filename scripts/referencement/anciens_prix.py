# -*- coding: utf-8 -*-
"""
Eddy, 13/09 (2) : l’ancien prix barré à côté du nouveau, partout où les deux
offres s’affichent — 400 € → 259 €, 44 € → 29 € : boutons des pages, barre,
menu, pied de page, cartes des disciplines, détail du hero, et les
aria-label qui les annoncent. Les plaques l’avaient déjà (« au lieu de … ») ;
la plaque de poche (offres.js) et le CSS sont faits à la main.
Rejouable : un prix déjà barré n’est plus reconnu par les motifs.
"""
import glob, io, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
R = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment', 'bc-ramonville')


def lire(p):
    return io.open(p, encoding='utf-8', newline='').read()


def ecrire(p, t):
    io.open(p, 'w', encoding='utf-8', newline='').write(t)


S400 = '<s class="ancien">400&nbsp;€</s> '
S44 = '<s class="ancien">44&nbsp;€</s> '
MOTIFS = [
    (re.compile('(>L’année(?: complète)? · )(259[  ]€)'), r'\1' + S400 + r'\2', 'face 259'),
    (re.compile('(>(?:Je profite de l\'offre — |Offre · |Voir l’offre · |Quatre semaines · ))(29[  ]€)'), r'\1' + S44 + r'\2', 'face 29'),
    (re.compile('(>)(259&nbsp;€ comptant)'), r'\1' + S400 + r'\2', 'détail 259'),
    (re.compile('(>)(29&nbsp;€ par personne · 4 semaines · gants)'), r'\1' + S44 + r'\2', 'détail 29'),
    (re.compile('l’année complète à 259([  ])€, ou 29([  ])€ par personne pour 4 semaines"'),
     r'l’année complète à 259\1€ au lieu de 400\1€, ou 29\2€ par personne pour 4 semaines au lieu de 44\2€"', 'aria'),
]
fichiers = glob.glob(os.path.join(R, 'src', 'pages', '**', '*.astro'), recursive=True) + \
    [os.path.join(R, 'public', 'assets', 'js', f) for f in ('site.js', 'page.js')]
tot = {}
for p in fichiers:
    t = t0 = lire(p)
    for rx, rep, nom in MOTIFS:
        t, k = rx.subn(rep, t)
        tot[nom] = tot.get(nom, 0) + k
    if t != t0:
        ecrire(p, t)
        print('  ok', os.path.relpath(p, R))
print(' ', tot)

# contrôle : aucune face d'alternance qui affiche 259 € ou 29 € sans son ancien prix
RX_FACE = re.compile(r'<span class="alt__face[^"]*"[^>]*>(.*?)</span>', re.S)
RX_PRIX = re.compile('\\b(?:259|29)(?:[  ]|&nbsp;)€')
seules = [(os.path.relpath(p, R), c[:60]) for p in fichiers for c in RX_FACE.findall(lire(p))
          if RX_PRIX.search(c) and 'ancien' not in c]
print('  faces sans ancien prix :', len(seules), seules[:5])
assert not seules
