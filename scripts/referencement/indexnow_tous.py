# -*- coding: utf-8 -*-
"""
IndexNow, pour les sept domaines, UNIQUEMENT quand la clé est en ligne.

Pour chaque site : lit HOTE et CLE dans scripts/indexnow.mjs, attend que
https://HOTE/CLE.txt réponde 200 avec la clé (le déploiement Vercel est
fini), puis lance « npm run indexnow ». Un site dont la clé n'est pas en
ligne après le délai est signalé, jamais soumis à l'aveugle.
"""
import io, os, re, sys, time, subprocess, urllib.request, ssl
sys.stdout.reconfigure(encoding='utf-8')
BASE = r"C:\Users\Mommy Jayce\Desktop\Boxing Center\Deployment"
SITES = sys.argv[1:] or ['colomiers', 'muret', 'cugnaux', 'tournefeuille', 'labege', 'lunion', 'castelginest']
ctx = ssl.create_default_context()
DELAI = 600

for s in SITES:
    R = os.path.join(BASE, f'boxing-center-{s}')
    t = io.open(os.path.join(R, 'scripts', 'indexnow.mjs'), encoding='utf-8').read()
    hote = re.search(r"const HOTE = '([^']+)'", t).group(1)
    cle = re.search(r"const CLE = '([^']+)'", t).group(1)
    url = f'https://{hote}/{cle}.txt'
    debut, ok = time.time(), False
    while time.time() - debut < DELAI:
        try:
            corps = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'indexnow-verif'}), timeout=20, context=ctx).read().decode().strip()
            if corps == cle:
                ok = True
                break
        except Exception:
            pass
        time.sleep(15)
    if not ok:
        print(f'✗ {s:13s} clé absente en ligne après {DELAI}s : {url}')
        continue
    r = subprocess.run(['npm', 'run', 'indexnow'], cwd=R, capture_output=True, text=True, shell=True)
    print(f'{s:13s} {(r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else r.returncode}')
