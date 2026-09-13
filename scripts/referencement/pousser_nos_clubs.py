# -*- coding: utf-8 -*-
"""
Pousse « Nos clubs » sur les sept satellites, dans les règles de la maison :
seuls les fichiers du lot sont indexés (plus, sur Colomiers, la boîte à outils
du 13/09), aucune signature ni trailer, pull --rebase --autostash avant push,
rien de forcé — arrêt au premier conflit.

Puis, site par site, attend que /nos-clubs/ réponde 200 EN LIGNE (preuve que le
NOUVEAU déploiement est servi : la page n'existait pas avant) et seulement
alors lance « npm run indexnow ». Cela rattrape aussi le lot MCP de midi, dont
l'IndexNow n'était jamais parti (son marqueur n'était pas dans humans.txt).
Usage : python pousser_nos_clubs.py [site…]
"""
import glob, io, os, re, ssl, subprocess, sys, time, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment')
SITES = sys.argv[1:] or ['colomiers', 'muret', 'cugnaux', 'tournefeuille', 'labege', 'lunion', 'castelginest']
MESSAGE = ("feat(satellites): une page « Nos clubs » dans la navigation et le pied de page — les cinq clubs Boxing Center "
           "(Portet-sur-Garonne, Minimes, États-Unis, Saint-Cyprien, Ramonville), leur adresse et un bouton vers leur vrai site ; "
           "hors index (mêmes adresses sur les sept sites de proximité), liens suivis, vignette propre")
LOT = ['src/data/routes.ts', 'src/data/vignettes.ts', 'src/pages/nos-clubs.astro']
ctx = ssl.create_default_context()


def git(R, *args, check=True):
    r = subprocess.run(['git', *args], cwd=R, capture_output=True, text=True, encoding='utf-8')
    if check and r.returncode != 0:
        raise SystemExit(f'✗ {os.path.basename(R)} : git {" ".join(args)}\n{r.stdout}{r.stderr}')
    return r


pousses = []
for s in SITES:
    R = os.path.join(BASE, f'boxing-center-{s}')
    fichiers = list(LOT)
    if s == 'colomiers':
        fichiers += [os.path.relpath(p, R).replace('\\', '/') for p in glob.glob(os.path.join(R, 'scripts', 'referencement', '*'))
                     if os.path.isfile(p)]
    git(R, 'add', '--', *fichiers)
    if git(R, 'diff', '--cached', '--name-only').stdout.strip():
        git(R, 'commit', '-q', '-m', MESSAGE)
    elif git(R, 'rev-list', '--count', '@{u}..HEAD').stdout.strip() == '0':
        print(f'{s:13s} rien à pousser')
        continue
    git(R, 'pull', '--rebase', '--autostash', '-q')
    git(R, 'push', '-q')
    print(f'{s:13s} poussé {git(R, "rev-parse", "--short", "HEAD").stdout.strip()}')
    pousses.append(s)

for s in pousses:
    R = os.path.join(BASE, f'boxing-center-{s}')
    hote = re.search(r"const HOTE = '([^']+)'", io.open(os.path.join(R, 'scripts', 'indexnow.mjs'), encoding='utf-8').read()).group(1)
    debut, ok = time.time(), False
    while time.time() - debut < 900:
        try:
            req = urllib.request.Request(f'https://{hote}/nos-clubs/?v={int(time.time())}', headers={'User-Agent': 'verif-deploiement'})
            with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
                if r.status == 200 and 'Nos cinq clubs' in r.read().decode('utf-8', 'ignore'):
                    ok = True
                    break
        except Exception:
            pass
        time.sleep(20)
    if not ok:
        print(f'{s:13s} ✗ /nos-clubs/ pas en ligne après 15 min : IndexNow NON soumis')
        continue
    r = subprocess.run(['npm', 'run', 'indexnow'], cwd=R, capture_output=True, text=True, shell=True)
    sortie = (r.stdout + r.stderr).strip().splitlines()
    print(f'{s:13s} en ligne · IndexNow : {sortie[-1] if sortie else r.returncode}')
