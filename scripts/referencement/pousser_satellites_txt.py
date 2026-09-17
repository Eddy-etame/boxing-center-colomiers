# -*- coding: utf-8 -*-
"""
Pousse le lot « fichiers IA hors du plan du site + X-Robots-Tag: noindex » sur
les sept satellites, dans les règles de la maison : seuls les fichiers du lot
sont indexés (plus, sur Colomiers, la boîte à outils), aucune signature, pull
--rebase --autostash avant push, rien de forcé — arrêt au premier conflit.

Puis, site par site : attend que le plan du site EN LIGNE ne liste plus aucun
.txt (preuve que le nouveau déploiement est servi) et que /llms.txt réponde
avec X-Robots-Tag: noindex, et seulement alors lance « npm run indexnow ».
Usage : python pousser_satellites_txt.py [site…]
"""
import glob, io, os, re, ssl, subprocess, sys, time, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment')
SITES = sys.argv[1:] or ['colomiers', 'muret', 'cugnaux', 'tournefeuille', 'labege', 'lunion', 'castelginest']
MESSAGE = ("seo(satellites): les fichiers pour les IA (llms.txt, llms-full.txt, humans.txt, ai.txt) sortent du plan du site "
           "et reçoivent X-Robots-Tag: noindex — Google les explorait comme des pages et les rangeait en « non indexée » ; "
           "les IA les lisent toujours")
LOT = ['vercel.json', 'src/pages/sitemap.xml.ts']
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
            v = int(time.time())
            plan = urllib.request.urlopen(urllib.request.Request(f'https://{hote}/sitemap.xml?v={v}', headers={'User-Agent': 'verif-deploiement'}), timeout=20, context=ctx).read().decode('utf-8', 'ignore')
            r = urllib.request.urlopen(urllib.request.Request(f'https://{hote}/llms.txt?v={v}', headers={'User-Agent': 'verif-deploiement'}), timeout=20, context=ctx)
            if '.txt' not in plan and 'noindex' in (r.headers.get('X-Robots-Tag') or '').lower():
                ok = True
                break
        except Exception:
            pass
        time.sleep(20)
    if not ok:
        print(f'{s:13s} ✗ nouveau déploiement pas en ligne après 15 min : IndexNow NON soumis')
        continue
    r = subprocess.run(['npm', 'run', 'indexnow'], cwd=R, capture_output=True, text=True, shell=True)
    sortie = (r.stdout + r.stderr).strip().splitlines()
    print(f'{s:13s} en ligne (plan sans .txt, llms noindex) · {sortie[-1] if sortie else r.returncode}')
