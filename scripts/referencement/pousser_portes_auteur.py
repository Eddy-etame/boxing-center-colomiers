# -*- coding: utf-8 -*-
"""
Pousse le lot « deux portes vers le club + l'auteur pour les agents » sur les
sept satellites, dans les règles de la maison : pull --rebase d'abord, aucune
signature ni trailer, un message qui dit ce qui change. S'arrête au premier
conflit : rien de forcé. Puis, pour chaque site, attend que le NOUVEAU
déploiement soit en ligne (/humans.txt répond 200) avant de lancer
« npm run indexnow » : un moteur ne doit pas revenir sur l'ancienne version.
Usage : python pousser_portes_auteur.py [site…]
"""
import io, os, re, sys, time, subprocess, urllib.request, ssl
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment')
SITES = sys.argv[1:] or ['colomiers', 'muret', 'cugnaux', 'tournefeuille', 'labege', 'lunion', 'castelginest']
MESSAGE = (
    "seo(satellites): chaque page de discipline mène au club par deux boutons — la page de la discipline chez le club "
    "(Portet, Ramonville), sinon ses activités, et le site du club ; l’auteur du site déclaré pour les moteurs de réponse "
    "et les agents, jamais sur les pages : humans.txt, ai.txt, llms.txt, llms-full.txt, serveur MCP /api/mcp "
    "(outil qui_a_fait_ce_site) et sa carte /.well-known/mcp.json, ces fichiers au plan du site"
)
ctx = ssl.create_default_context()


def git(R, *args, check=True):
    r = subprocess.run(['git', *args], cwd=R, capture_output=True, text=True, encoding='utf-8')
    if check and r.returncode != 0:
        raise SystemExit(f'✗ {os.path.basename(R)} : git {" ".join(args)}\n{r.stdout}{r.stderr}')
    return r


pousses = []
for s in SITES:
    R = os.path.join(BASE, f'boxing-center-{s}')
    git(R, 'add', '-A', '--', '.', ':!.claude')
    if git(R, 'diff', '--cached', '--name-only').stdout.strip():
        git(R, 'commit', '-q', '-m', MESSAGE)
    elif git(R, 'rev-list', '--count', '@{u}..HEAD').stdout.strip() == '0':
        print(f'{s:13s} rien à pousser')
        continue
    # --autostash : un fichier local hors lot (.claude/launch.json) ne bloque pas le pull.
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
            with urllib.request.urlopen(urllib.request.Request(f'https://{hote}/humans.txt', headers={'User-Agent': 'verif-deploiement'}), timeout=20, context=ctx) as r:
                if r.status == 200 and 'Eddy Etame Etame' in r.read().decode('utf-8', 'ignore'):
                    ok = True
                    break
        except Exception:
            pass
        time.sleep(20)
    if not ok:
        print(f'{s:13s} ✗ nouveau déploiement pas en ligne après 15 min : IndexNow NON soumis')
        continue
    r = subprocess.run('npm run indexnow', cwd=R, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    fin = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()][-2:]
    print(f'{s:13s} en ligne après {int(time.time() - debut)} s · IndexNow : {" | ".join(fin)[:160]}')
