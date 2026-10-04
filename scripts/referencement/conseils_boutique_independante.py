# -*- coding: utf-8 -*-
"""
Eddy, 03/10/2026 : Boutique de Boxe est une boutique à part, « something apart from Boxing Center »,
pas la boutique des clubs. Les conseils des clubs la présentaient comme « la boutique de matériel du
groupe » : quinze tournures, ici retirées ou remplacées par une description neutre, différente d'un
site à l'autre (une phrase, un site). Rejouable : une tournure déjà retirée n'est plus cherchée.

Après : satellites_conseils.py <site>, les builds, conseils_doublons.py (0 phrase partagée).
"""
import io, os, sys
sys.stdout.reconfigure(encoding='utf-8')
BC = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center')
C = os.path.join(BC, 'Deployment', 'boxing-center-colomiers', 'scripts', 'referencement', 'conseils')

REMPLACEMENTS = [
    (os.path.join(BC, 'Portet', 'boxing-center-portet', 'src', 'conseils.json'),
     'bandes de boxe de Boutique de Boxe</a>, la boutique de matériel du groupe, indiquent',
     'bandes de boxe de Boutique de Boxe</a>, boutique en ligne de matériel de combat, indiquent'),
    (os.path.join(BC, 'Deployment', 'bc-ramonville', 'src', 'conseils-pages.json'),
     'Les gants de MMA de Boutique de Boxe</a>, la boutique de matériel du groupe, sont triés',
     'Les gants de MMA de Boutique de Boxe</a>, une boutique en ligne spécialisée, sont triés'),
    (os.path.join(C, 'tournefeuille.json'), 'Boutique de Boxe, la boutique en ligne du groupe, compare', 'Boutique de Boxe, boutique en ligne de matériel de boxe, compare'),
    (os.path.join(C, 'tournefeuille.json'), 'de Boutique de Boxe, la boutique de matériel du groupe, affichent', 'de Boutique de Boxe affichent'),
    (os.path.join(C, 'muret.json'), 'de Boutique de Boxe</a>, la boutique de matériel du groupe, les gants', 'de Boutique de Boxe</a>, boutique de matériel de sports de combat, les gants'),
    (os.path.join(C, 'muret.json'), 'Les kimonos de Boutique de Boxe</a>, la boutique de matériel du groupe, donnent', 'Les kimonos de Boutique de Boxe</a> donnent'),
    (os.path.join(C, 'lunion.json'), 'Chez Boutique de Boxe, la boutique de matériel du groupe, <a', 'Chez Boutique de Boxe, <a'),
    (os.path.join(C, 'lunion.json'), 'Les cordes à sauter de Boutique de Boxe</a>, la boutique de matériel du groupe, sont', 'Les cordes à sauter de Boutique de Boxe</a> sont'),
    (os.path.join(C, 'labege.json'), 'le guide de Boutique de Boxe, la boutique de matériel du groupe, évite', 'le guide de Boutique de Boxe, évite'),
    (os.path.join(C, 'cugnaux.json'), 'de Boutique de Boxe, la boutique de matériel du groupe, part de', 'de Boutique de Boxe part de'),
    (os.path.join(C, 'cugnaux.json'), 'Boutique de Boxe, la boutique en ligne du groupe, passe', 'Boutique de Boxe, boutique spécialisée en ligne, passe'),
    (os.path.join(C, 'colomiers.json'), 'de Boutique de Boxe, la boutique de matériel du groupe, apprend', 'de Boutique de Boxe apprend'),
    (os.path.join(C, 'colomiers.json'), 'Chez Boutique de Boxe, la boutique en ligne du groupe, <a', 'Chez Boutique de Boxe, boutique de matériel en ligne, <a'),
    (os.path.join(C, 'castelginest.json'), 'de Boutique de Boxe, la boutique de matériel du groupe, vont', 'de Boutique de Boxe vont'),
    (os.path.join(C, 'castelginest.json'), 'de Boutique de Boxe, la boutique de matériel du groupe, donnent', 'de Boutique de Boxe donnent'),
]

faits = 0
for f, ancien, neuf in REMPLACEMENTS:
    s = io.open(f, encoding='utf-8', newline='').read()
    if ancien not in s:
        print('absent (déjà fait ?) :', os.path.basename(f), '|', ancien[:50])
        continue
    assert s.count(ancien) == 1, (f, ancien)
    s = s.replace(ancien, neuf)
    io.open(f, 'w', encoding='utf-8', newline='').write(s)
    faits += 1
reste = 0
for f in {r[0] for r in REMPLACEMENTS}:
    reste += io.open(f, encoding='utf-8').read().count('du groupe')
print(faits, 'tournure(s) retirée(s) ;', reste, '« du groupe » restant(s)')
