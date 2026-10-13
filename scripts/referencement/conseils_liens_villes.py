# -*- coding: utf-8 -*-
"""
Les conseils du réseau mènent à la page « Boutique de boxe Toulouse » de la boutique (13/10/2026).

Constat : les neuf sites de proximité et de club envoyaient 7 à 14 liens chacun à boutique-de-boxe.com,
tous vers des rayons, des guides ou des pages de tête — aucun vers une page-ville, alors que ce sont
les pages sorties de Google et que chaque club est à Toulouse ou à ses portes. Eddy (13/10) : des liens
« très discrets », jamais sur boxingcenter.fr.

Ce script ajoute UNE phrase, écrite pour ce site-là, à la fin d'un paragraphe existant : rien n'est
réécrit, l'ancre change d'un site à l'autre (neuf ancres, neuf tournures), le lien a le style des liens
déjà présents dans l'article. Il se relance sans rien doubler.

Après : satellites_conseils.py <site> et le build (sept sites) ; generate-conseils.mjs (Portet) ;
generer-conseils.mjs (Ramonville) ; conseils_doublons.py — 0 phrase partagée.
"""
import io, os, sys
sys.stdout.reconfigure(encoding='utf-8')
ICI = os.path.dirname(os.path.abspath(__file__))
R = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center')
B = 'https://www.boutique-de-boxe.com'
TOULOUSE = '/boutique-de-boxe-toulouse/'


def lien_sat(chemin, ancre):
    """Le style des liens des sept sites de proximité."""
    return '<a class=\\"lien\\" href=\\"%s%s\\" rel=\\"noopener\\">%s</a>' % (B, chemin, ancre)


def lien_club(chemin, ancre):
    """Le style des liens de Portet et de Ramonville."""
    return '<a href=\\"%s%s\\" target=\\"_blank\\" rel=\\"noopener\\">%s</a>' % (B, chemin, ancre)


# (fichier, fin exacte du paragraphe telle qu'écrite dans le fichier, phrase ajoutée)
AJOUTS = [
    (os.path.join(ICI, 'conseils', 'colomiers.json'), 'tu poses tes questions au coach, et tu achètes ensuite — en sachant quoi.',
     ' Les salles de la ville, toutes, sont sur la page ' + lien_sat(TOULOUSE, 'boutique de boxe Toulouse') + ' de Boutique de Boxe.'),
    (os.path.join(ICI, 'conseils', 'tournefeuille.json'), 'qui publie un cours Boxe Thaï / K1. Portet-sur-Garonne propose le kick-boxing.',
     ' Les lieux de Toulouse où l’on boxe sont listés avec leurs disciplines sur ' + lien_sat(TOULOUSE, 'la page Toulouse de Boutique de Boxe') + '.'),
    (os.path.join(ICI, 'conseils', 'cugnaux.json'), 'pour l’opposition, on passe en général à 14 ou 16 oz selon le gabarit.',
     ' Pour savoir où l’on boxe à Toulouse même, ' + lien_sat(TOULOUSE, 'la boutique de boxe à Toulouse') + ' recense les salles de la ville.'),
    (os.path.join(ICI, 'conseils', 'muret.json'), 'au 1er octobre 2026, commande en ligne et retrait en salle.',
     ' Toulouse a sa propre page chez la même boutique : ' + lien_sat(TOULOUSE, 'boutique de boxe Toulouse, salles et matériel') + '.'),
    (os.path.join(ICI, 'conseils', 'labege.json'), 'Prends-le à ta taille — trop grand, il perd son intérêt.',
     ' Les clubs de Toulouse où l’on pratique le grappling sont sur ' + lien_sat(TOULOUSE, 'la page Boutique de boxe Toulouse') + '.'),
    (os.path.join(ICI, 'conseils', 'lunion.json'), 'et tu demandes au club ce qu’il met à disposition. Le reste s’achète en connaissance de cause.',
     ' Et pour comparer les clubs de la ville avant de choisir, ' + lien_sat(TOULOUSE, 'Boutique de boxe Toulouse') + ' les liste, disciplines et adresses comprises.'),
    (os.path.join(ICI, 'conseils', 'castelginest.json'), 'Chaussures et sac de frappe attendront que tu saches ce que tu veux travailler.',
     ' Si tu cherches une salle plus près du centre, ' + lien_sat(TOULOUSE, 'la boutique de boxe Toulouse') + ' recense celles de la ville.'),
    (os.path.join(R, 'Portet', 'boxing-center-portet', 'src', 'conseils.json'), 'et tu ne le connais qu’après en avoir parlé avec le coach.',
     ' Les autres clubs de Toulouse, Boxing Center en tête, sont sur ' + lien_club(TOULOUSE, 'la page boutique de boxe Toulouse') + '.'),
    (os.path.join(R, 'Deployment', 'bc-ramonville', 'src', 'conseils-pages.json'), 'Pour les gants de cette première fois, pose la question à l’accueil en arrivant.',
     ' Où l’on boxe à Toulouse, salle par salle : ' + lien_club(TOULOUSE, 'boutique de boxe Toulouse') + ', chez Boutique de Boxe.'),
]

faits = 0
for f, fin, phrase in AJOUTS:
    s = io.open(f, encoding='utf-8', newline='').read()
    nom = os.path.relpath(f, R)
    if phrase in s:
        print('déjà posé :', nom)
        continue
    n = s.count(fin + '"')
    assert n == 1, (nom, fin[-50:], n)
    s = s.replace(fin + '"', fin + phrase + '"')
    io.open(f, 'w', encoding='utf-8', newline='').write(s)
    faits += 1
    print('posé :', nom, '|', fin[-40:])
print(faits, 'phrase(s) ajoutée(s)')
