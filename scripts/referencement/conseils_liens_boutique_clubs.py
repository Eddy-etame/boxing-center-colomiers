# -*- coding: utf-8 -*-
"""
Les conseils de Portet et de Ramonville mènent aux pages de tête de la boutique (03/10/2026).

Même constat que pour les sept sites de proximité (conseils_liens_boutique.py) : leurs liens vers
boutique-de-boxe.com visaient des rayons et des guides, jamais « Matériel de boxe » ni une page
par boxe. Ce script ajoute une phrase, écrite pour ce club-là, à la fin d'un paragraphe existant ;
rien n'est réécrit. Il se relance sans rien doubler. (Blagnac : voir blagnac_conseils.py, qui
porte ses liens dans les sections.)

Après : le build du site (generate-conseils.mjs à Portet, generer-conseils.mjs à Ramonville),
puis conseils_doublons.py — 0 phrase partagée.
"""
import io, os, sys
sys.stdout.reconfigure(encoding='utf-8')
R = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center')
B = 'https://www.boutique-de-boxe.com'


def lien(chemin, ancre):
    return '<a href=\\"%s%s\\" target=\\"_blank\\" rel=\\"noopener\\">%s</a>' % (B, chemin, ancre)


AJOUTS = [
    (os.path.join('Portet', 'boxing-center-portet', 'src', 'conseils.json'), 'le guide des protections</a> dit laquelle sert à quoi.',
     ' Et pour voir le premier sac d’un seul coup, ' + lien('/materiel-boxe-debutant/', 'le matériel de boxe pour débutant') + ' de Boutique de Boxe ne garde que les pièces du début.'),
    (os.path.join('Portet', 'boxing-center-portet', 'src', 'conseils.json'), 'le tableau du matériel de sport de combat</a>.',
     ' Pour comparer les budgets, du premier cours à la compétition, la même boutique tient ' + lien('/materiel-boxe/', 'un tableau du matériel de boxe par niveau') + '.'),
    (os.path.join('Deployment', 'bc-ramonville', 'src', 'conseils-pages.json'), 'si tu enchaînes les deux cours, un seul sac suffit.',
     ' Pour le sol, Boutique de Boxe a réuni rashguards, shorts et spats dans ' + lien('/equipement-jjb/', 'l’équipement de JJB et de grappling') + '.'),
    (os.path.join('Deployment', 'bc-ramonville', 'src', 'conseils-pages.json'), 'le protège-dents arrive avec le premier travail à deux.',
     ' Des premières bandes au casque, la suite est rangée par niveau dans ' + lien('/materiel-boxe/', 'le matériel de boxe') + ' de Boutique de Boxe.'),
    # 2ᵉ tour (03/10) : les pages du cahier des charges qu'aucun site ne liait encore
    (os.path.join('Portet', 'boxing-center-portet', 'src', 'conseils.json'), 'nt d’acheter un casque : elle dépend de la discipline et de la compétition.',
     ' Casques, protège-tibias et coquilles d’enfant se comparent dans ' + lien('/protections-boxe/', 'les protections de boxe') + ' de Boutique de Boxe.'),
    (os.path.join('Deployment', 'bc-ramonville', 'src', 'conseils-pages.json'), 'ort est la première pièce d’équipement d’une boxeuse, avant même les gants.',
     ' Brassières, leggings et shorts sont réunis dans ' + lien('/textile-boxe/', 'le textile de boxe') + ' de Boutique de Boxe.'),
]

faits = 0
for f, fin, phrase in AJOUTS:
    chemin = os.path.join(R, f)
    s = io.open(chemin, encoding='utf-8', newline='').read()
    if phrase in s:
        print('déjà posé :', f, '|', fin[-40:])
        continue
    assert s.count(fin + '"') == 1, (f, fin, s.count(fin + '"'))
    s = s.replace(fin + '"', fin + phrase + '"')
    io.open(chemin, 'w', encoding='utf-8', newline='').write(s)
    faits += 1
    print('posé :', f, '|', fin[-40:])
print(faits, 'phrase(s) ajoutée(s)')
