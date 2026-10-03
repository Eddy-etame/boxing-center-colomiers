# -*- coding: utf-8 -*-
"""
Les conseils des sept sites de proximité mènent aux pages de tête de la boutique (03/10/2026).

Constat : sur les 70 liens que les conseils du réseau envoyaient à boutique-de-boxe.com, aucun
n'allait vers « Matériel de boxe », ni vers une page de vente, ni vers une page par boxe — tous
visaient un rayon ou un guide. Les requêtes de tête n'avaient donc aucun lien venu d'ailleurs.

Ce script ajoute UNE phrase, écrite pour ce site-là, à la fin d'un paragraphe existant de
conseils/<site>.json : rien n'est réécrit, et l'ancre change d'un site à l'autre (un réseau qui
répète la même ancre ressemble à une ferme de liens). Il se relance sans rien doubler.

Après : satellites_conseils.py <site>, le build du site, conseils_doublons.py (0 phrase partagée).
"""
import io, os, sys
sys.stdout.reconfigure(encoding='utf-8')
ICI = os.path.dirname(os.path.abspath(__file__))
B = 'https://www.boutique-de-boxe.com'


def lien(chemin, ancre):
    return '<a class=\\"lien\\" href=\\"%s%s\\" rel=\\"noopener\\">%s</a>' % (B, chemin, ancre)


# (site, fin exacte du paragraphe, telle qu'elle est écrite dans le fichier, phrase ajoutée)
AJOUTS = [
    ('colomiers', 'e demande ta séance, ton gabarit et ton âge, et répond par un chiffre.',
     ' Et pour ce qui entoure les gants, la même boutique range ' + lien('/materiel-boxe/', 'tout le matériel de boxe') + ' par niveau, du premier cours au ring.'),
    ('colomiers', 'notre repère de 10 à 16 oz</a> fait le tri.',
     ' Pour voir ce que contient un premier sac complet, la boutique a sa page ' + lien('/materiel-boxe-debutant/', 'matériel de boxe débutant') + '.'),
    ('tournefeuille', 'istent en coupe anglaise et en coupe thaï — ne te trompe pas de rayon.',
     ' La liste entière, rayon par rayon, est sur la page ' + lien('/materiel-boxe-thai/', 'matériel de boxe thaï') + ' de Boutique de Boxe.'),
    ('cugnaux', 'n confort — utiles si tes chevilles sont fragiles, pas indispensables.',
     ' Boutique de Boxe a réuni ' + lien('/materiel-kick-boxing/', 'le matériel de kick-boxing') + ' sur une seule page, avec le nombre de modèles de chaque rayon.'),
    ('muret', 'première année, un gant synthétique d’entrée de gamme fait le travail.',
     ' La boutique a aussi chiffré trois sacs — débuter, s’entraîner à deux, monter sur le ring — dans son tableau du ' + lien('/materiel-boxe/', 'matériel de boxe') + '.'),
    ('muret', 'Le guide pour choisir ses protections</a> explique l’usage de chacune.',
     ' Et ' + lien('/vente-materiel-de-boxe/', 'la page de vente du matériel de boxe') + ' donne le premier prix et le prix médian de chacun des dix rayons.'),
    ('muret', 'mono après chaque séance : c’est la règle d’hygiène de tous les tapis.',
     ' Kimono, ceinture, rashguard : la boutique les a rassemblés sur sa page ' + lien('/equipement-jjb/', 'équipement JJB et grappling') + '.'),
    ('labege', 'lures aux genoux, et tient une coquille quand le coach en demande une.',
     ' Rashguards, shorts et spats sont réunis sur la page ' + lien('/equipement-jjb/', 'équipement de grappling') + ' de Boutique de Boxe.'),
    ('labege', 'la boutique Boxing Center</a>, retirée à la salle.',
     ' Et si tout le sac est à refaire, ' + lien('/materiel-boxe/', 'le rayon matériel de boxe') + ' repart des trois pièces du début.'),
    ('lunion', 'Les femmes ont leurs protections pelviennes et leurs protège-poitrine.',
     ' Gants de 16 oz, casque, coquille : Boutique de Boxe chiffre ce sac dans ' + lien('/materiel-boxe/', 'son tableau du matériel de boxe, niveau par niveau') + '.'),
    ('castelginest', 'ix médian de 66,90 € pour une paire de chaussures de boxe ou de lutte.',
     ' Gants à lacets, coquille, short : le reste d’un sac de combat est sur la page ' + lien('/materiel-boxe-competition/', 'matériel de boxe de compétition') + '.'),
    ('castelginest', 'groupe, donnent le poids, la longueur et la fixation de chaque modèle.',
     ' Un sac de frappe ne se livre qu’à domicile : ' + lien('/vente-materiel-de-boxe/', 'la page vente de matériel de boxe') + ' de la boutique en donne les conditions.'),
]

faits = 0
for site, fin, phrase in AJOUTS:
    f = os.path.join(ICI, 'conseils', site + '.json')
    s = io.open(f, encoding='utf-8', newline='').read()
    if phrase in s:
        print('déjà posé :', site, '|', fin[-40:])
        continue
    assert s.count(fin + '"') == 1, (site, fin, s.count(fin + '"'))
    s = s.replace(fin + '"', fin + phrase + '"')
    io.open(f, 'w', encoding='utf-8', newline='').write(s)
    faits += 1
    print('posé :', site, '|', fin[-40:])
print(faits, 'phrase(s) ajoutée(s)')
