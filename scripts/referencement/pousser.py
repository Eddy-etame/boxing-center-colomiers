# -*- coding: utf-8 -*-
"""
Pousse les sept dépôts, un par un, dans les règles de la maison :
pull --rebase d'abord (Eddy pousse aussi depuis son terminal), aucune
signature ni trailer (interdit absolu d'Eddy), un message par site qui dit
ce qui a changé et pourquoi. S'arrête au premier conflit : rien de forcé.

Usage : python pousser.py [site…]
"""
import os, sys, subprocess
sys.stdout.reconfigure(encoding='utf-8')
BASE = r"C:\Users\Mommy Jayce\Desktop\Boxing Center\Deployment"
SITES = sys.argv[1:] or ['colomiers', 'muret', 'cugnaux', 'tournefeuille', 'labege', 'lunion', 'castelginest']

COMMUN = (
    "Référencement : une vignette photo par page (1200×630 et carrée 1200×1200, annoncée dans le JSON-LD), "
    "des favicons carrés lisibles dans le rond de Google (ICO + PNG + apple-touch + manifest), max-image-preview:large, "
    "IndexNow sur le vrai domaine avec sa propre clé, robots.txt qui nomme les moteurs de réponse, "
    "un bloc « Réponses courtes » dans llms.txt, noindex sur les pages juridiques"
)
PROPRE = {
    'colomiers': COMMUN + ".",
    'muret': COMMUN + " et sur les pages copiées d'un site à l'autre (première séance, contact, ta séance).",
    'cugnaux': COMMUN + " et sur les pages copiées d'un site à l'autre (première séance, contact, ta séance).",
    'tournefeuille': COMMUN + " et sur les pages copiées d'un site à l'autre (première séance, contact).",
    'labege': COMMUN + " et sur les pages copiées d'un site à l'autre (première séance, contact, ta séance).",
    'lunion': COMMUN + " et sur les pages copiées d'un site à l'autre (première séance, contact, ta séance).",
    'castelginest': COMMUN + " et sur les pages copiées d'un site à l'autre. Les cinq pages de discipline sont réécrites "
                    "depuis Castelginest (ligne 60, route du 15, collège) : elles partageaient 82 à 91 % de leurs phrases avec L'Union.",
}

def git(R, *args, check=True):
    r = subprocess.run(['git', *args], cwd=R, capture_output=True, text=True, encoding='utf-8')
    if check and r.returncode != 0:
        raise SystemExit(f'✗ {os.path.basename(R)} : git {" ".join(args)}\n{r.stdout}{r.stderr}')
    return r

for s in SITES:
    R = os.path.join(BASE, f'boxing-center-{s}')
    git(R, 'add', '-A')
    if not git(R, 'status', '--porcelain').stdout.strip():
        print(f'{s:13s} rien à pousser'); continue
    git(R, 'stash')
    git(R, 'pull', '--rebase', '-q', 'origin', 'main')
    git(R, 'stash', 'pop')
    git(R, 'add', '-A')
    git(R, 'commit', '-q', '-m', PROPRE[s])
    git(R, 'push', '-q', 'origin', 'main')
    h = git(R, 'log', '-1', '--format=%h %an').stdout.strip()
    trailer = 'Co-Authored' in git(R, 'log', '-1', '--format=%B').stdout
    print(f'{s:13s} poussé {h}' + ('  ✗ TRAILER PRÉSENT' if trailer else ''))
