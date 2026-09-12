# -*- coding: utf-8 -*-
"""
Pousse le lot « phrases partagées » : pull --rebase d'abord, aucune
signature ni trailer (interdit absolu d'Eddy), un message par site.
S'arrête au premier conflit : rien de forcé.
Usage : python pousser_reecriture.py [site…]
"""
import os, sys, subprocess
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment')
GARDE = " H1, adresses, photos et titres qui nomment la ville inchangés. Loi commune §13.16 : une phrase, un site."
MESSAGES = {
    'labege': "Pages disciplines réécrites depuis Ramonville (la 79, l'octogone de sept mètres, l'étage en accès libre, l'Innopole) : "
              "elles partageaient jusqu'à 21 phrases par page avec Tournefeuille, L'Union et Cugnaux." + GARDE,
    'lunion': "Pages disciplines réécrites depuis l'avenue des États-Unis (deux rings, cage surélevée, seize sacs, MMA jeunes 10/16) : "
              "elles partageaient jusqu'à 21 phrases par page avec Tournefeuille, Labège et Castelginest. "
              "Les âges de l'École de boxe sont les mêmes d'une page à l'autre." + GARDE,
    'muret': "Pages disciplines : les phrases reprises de Colomiers réécrites (boxe anglaise, MMA, boxe enfant, boxing fitness), "
             "et la phrase doublée de la FAQ « pas en forme » corrigée." + GARDE,
    'cugnaux': "Pages disciplines : les 41 phrases partagées avec Muret, Colomiers et Tournefeuille réécrites." + GARDE,
    'tournefeuille': "Pages disciplines : les sept phrases partagées avec Colomiers et Muret réécrites." + GARDE,
    'colomiers': "Loi commune §13.16 : une phrase de discipline, un site. partage_source.py lit enfin les chaînes entre guillemets "
                 "(Muret et Cugnaux lui échappaient) ; outils de réécriture sous garde versés dans scripts/referencement.",
    'castelginest': "Loi commune §13.16 : une phrase de discipline, un site.",
}
SITES = sys.argv[1:] or list(MESSAGES)


def git(R, *args, check=True):
    r = subprocess.run(['git', *args], cwd=R, capture_output=True, text=True, encoding='utf-8')
    if check and r.returncode != 0:
        raise SystemExit(f'✗ {os.path.basename(R)} : git {" ".join(args)}\n{r.stdout}{r.stderr}')
    return r


for s in SITES:
    R = os.path.join(BASE, f'boxing-center-{s}')
    git(R, 'add', '-A')
    if not git(R, 'status', '--porcelain').stdout.strip():
        print(f'{s:13s} rien à pousser')
        continue
    git(R, 'stash')
    git(R, 'pull', '--rebase', '-q', 'origin', 'main')
    git(R, 'stash', 'pop')
    git(R, 'add', '-A')
    git(R, 'commit', '-q', '-m', MESSAGES[s])
    git(R, 'push', '-q', 'origin', 'main')
    h = git(R, 'log', '-1', '--format=%h %an').stdout.strip()
    corps = git(R, 'log', '-1', '--format=%B').stdout
    alerte = '  ✗ TRAILER PRÉSENT' if ('Co-Authored' in corps or 'Claude' in corps) else ''
    print(f'{s:13s} poussé {h}{alerte}')
