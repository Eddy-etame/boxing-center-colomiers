# -*- coding: utf-8 -*-
"""
Pousse le lot « pages de commune » : pull --rebase d'abord, aucune
signature ni trailer, un message par site. S'arrête au premier conflit.
Usage : python pousser_communes.py [site…]
"""
import os, sys, subprocess
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment')
LOI = " Loi commune §13.17 : on ne réécrit qu'une page qui ne tient aucun rang."
GARDE = " H1, recherches de la légende, URL et photos inchangés."
MESSAGES = {
    'lunion': "Pages de commune : leur propre micro-copie (Saint-Jean, Rouffiac-Tolosan), et la légende dit enfin que le club "
              "publie le Muay Thai." + GARDE + LOI,
    'castelginest': "Pages de commune : leur propre micro-copie et leurs propres réponses de légende (elles étaient celles de L'Union "
                    "mot pour mot) ; descriptions de cours réécrites." + GARDE + LOI,
    'cugnaux': "Pages de commune : leur propre micro-copie et leurs propres réponses de légende (elles étaient celles de "
               "Tournefeuille) ; descriptions de cours réécrites (elles étaient celles de Muret). Fait corrigé : Portet n'a pas "
               "« la seule cage du réseau », c'est la plus proche de Cugnaux." + GARDE + LOI,
    'tournefeuille': "Pages de commune : leur propre micro-copie (Fonsorbes, Plaisance-du-Touch). Faits corrigés : Portet n'a pas "
                     "« la seule cage du réseau », ni Saint-Cyprien « la seule boxe thaï » (États-Unis publie le Muay Thai) ; "
                     "ce sont les plus proches de Tournefeuille." + GARDE + LOI,
    'muret': "Fait corrigé : Portet n'a pas « la seule cage du réseau » (États-Unis a une cage, Ramonville un octogone) ; "
             "c'est la cage du réseau la plus proche de Muret." + LOI,
    'labege': "Loi commune §13.17 : la page Saint-Orens tient la page 1 de Google, ses textes restent tels quels.",
    'colomiers': "Loi commune §13.17 : mesurer avant de réécrire ; script de retouche des pages de commune versé dans scripts/referencement.",
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
