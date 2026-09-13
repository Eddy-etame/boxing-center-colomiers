# -*- coding: utf-8 -*-
"""
Deux faux « seul du réseau » corrigés :
  · Portet n'a pas la seule cage : États-Unis a une cage officielle surélevée,
    Ramonville un octogone de sept mètres. Depuis Muret, Cugnaux, Tournefeuille
    et leurs communes, c'est en revanche la cage du réseau la plus proche.
  · Saint-Cyprien n'est pas le seul à publier la boxe thaï : États-Unis publie
    le Muay Thai. Depuis Tournefeuille, c'est le club thaï le plus proche.
Chaque ancienne chaîne doit exister une fois, sinon rien n'est écrit pour ce fichier.
Usage : python verite_cage.py
"""
import io, os, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment')

R = {
    ('muret', 'data/contenus.ts'): [
        ("promesse: 'La seule cage du réseau, et un apprentissage par étapes, même en partant de zéro.'",
         "promesse: 'La cage la plus proche de Muret, et un apprentissage par étapes, même en partant de zéro.'"),
        ("Portet-sur-Garonne a la seule cage du réseau Boxing Center.",
         "Depuis Muret, la cage du réseau Boxing Center la plus proche est à Portet-sur-Garonne."),
    ],
    ('muret', 'data/verite.ts'): [
        ("singularite: 'Le seul club du réseau avec une cage MMA.',",
         "singularite: 'Une cage MMA, un ring et un mur de sacs sur 600 m², au sud-ouest de Toulouse.',"),
    ],
    ('cugnaux', 'components/PageCommune.astro'): [
        ("`Seule cage du réseau Boxing Center, c’est là que s’entraîne le MMA. Grappling",
         "`Le MMA s’entraîne dans la cage du club, la plus proche de ${c.nom} dans le réseau. Grappling"),
    ],
    ('cugnaux', 'data/contenus.ts'): [
        ("c'est le seul club du réseau équipé d'une cage, et l'entraînement s'y fait dedans.",
         "c'est la cage du réseau la plus proche de Cugnaux, et l'entraînement s'y fait dedans."),
        ("Boxing Center Portet-sur-Garonne est le seul club du réseau à en avoir une, ce qui fait de la commune voisine de Cugnaux l'adresse la plus proche pour s'y entraîner.",
         "Boxing Center Portet-sur-Garonne en a une, dans la commune voisine : c'est la cage du réseau la plus proche de Cugnaux."),
        ("C'est la seule cage du réseau Boxing Center, et l'entraînement de MMA s'y déroule dedans, pas à côté.",
         "C'est la cage du réseau Boxing Center la plus proche de Cugnaux, et l'entraînement de MMA s'y déroule dedans, pas à côté."),
    ],
    ('cugnaux', 'data/verite.ts'): [
        ("singularite: 'Le seul club du réseau avec une cage MMA.',",
         "singularite: 'Un ring, une cage MMA et un mur de sacs sur 600 m², de l’autre côté de la route d’Espagne.',"),
    ],
    ('tournefeuille', 'components/PageCommune.astro'): [
        ("`Le MMA s’entraîne dans la cage du club — la seule du réseau Boxing Center. Le grappling",
         "`Le MMA s’entraîne dans la cage de Portet-sur-Garonne, la plus proche de ${c.nom} dans le réseau. Le grappling"),
    ],
    ('tournefeuille', 'data/contenus.ts'): [
        ("C’est le seul club du réseau qui publie la Boxe Thaï / K1.",
         "Le club publie la Boxe Thaï / K1, et c’est le plus proche de Tournefeuille à le faire."),
        ("c’est le seul club du réseau avec une cage, et l’entraînement se fait dedans.",
         "c’est la cage du réseau la plus proche de Tournefeuille, et l’entraînement se fait dedans."),
        ("Portet-sur-Garonne est le seul club du réseau à en avoir une.",
         "Depuis Tournefeuille, la plus proche du réseau est à Portet-sur-Garonne."),
        ("C’est la seule cage du réseau Boxing Center, et l’entraînement de MMA s’y déroule dedans.",
         "C’est la cage du réseau Boxing Center la plus proche de Tournefeuille, et l’entraînement de MMA s’y déroule dedans."),
    ],
    ('tournefeuille', 'data/verite.ts'): [
        ("et c’est le seul du réseau à publier la Boxe Thaï et le K1.",
         "et il publie la Boxe Thaï et le K1."),
        ("singularite: 'Le seul club du réseau avec une cage MMA, et le seul à publier le grappling.',",
         "singularite: 'Une cage MMA, un ring et le grappling, sur 600 m² au bord de la route d’Espagne.',"),
        ("600 m², un ring, et la seule cage MMA du réseau.",
         "600 m², un ring et une cage MMA."),
    ],
}

for (site, rel), paires in R.items():
    p = os.path.join(BASE, 'boxing-center-' + site, 'src', *rel.split('/'))
    crlf = b'\r\n' in io.open(p, 'rb').read()
    t = io.open(p, encoding='utf-8').read()
    fautes = [f'{t.count(v)}× « {v[:70]} »' for v, _ in paires if t.count(v) != 1]
    if fautes:
        print(f'{site:13s} {rel} : RIEN ÉCRIT', *fautes, sep='\n    ')
        continue
    for v, n in paires:
        t = t.replace(v, n)
    io.open(p, 'w', encoding='utf-8', newline='\r\n' if crlf else '\n').write(t)
    print(f'{site:13s} {rel} : {len(paires)} correction(s)')
