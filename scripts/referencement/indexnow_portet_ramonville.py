# -*- coding: utf-8 -*-
"""
IndexNow pour Portet et Ramonville, APRÈS le déploiement : la clé doit
répondre en ligne (https://HOTE/CLE.txt), puis toutes les URL du sitemap EN
LIGNE sont soumises (un changement de numéro touche chaque page). Les URL
partent en JSON, jamais en argument de ligne de commande (MSYS réécrivait
les chemins en « /… » en chemins Windows : 422).
Usage : python indexnow_portet_ramonville.py [portet] [ramonville]
"""
import json, re, ssl, sys, time, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
SITES = {
    'portet': ('boxing-center-portet.fr', '449dd4577a864d941394bcad4f682a9d'),
    'ramonville': ('mmatoulouse.com', 'dce5c925c3d8ce0daae1354521003d04'),
}
ctx = ssl.create_default_context()


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'indexnow-verif'}), timeout=25, context=ctx).read().decode('utf-8', 'replace')


for nom in (sys.argv[1:] or list(SITES)):
    hote, cle = SITES[nom]
    for _ in range(40):
        try:
            if get(f'https://{hote}/{cle}.txt').strip() == cle:
                break
        except Exception:
            pass
        time.sleep(15)
    else:
        print(f'✗ {nom} : clé absente en ligne, rien soumis')
        continue
    urls = sorted(set(re.findall(r'<loc>\s*(https://[^<\s]+)\s*</loc>', get(f'https://{hote}/sitemap.xml'))))
    urls = [u for u in urls if u.startswith(f'https://{hote}/') and not re.search(r'\.(jpe?g|png|webp|avif)$', u)]
    corps = json.dumps({'host': hote, 'key': cle, 'keyLocation': f'https://{hote}/{cle}.txt', 'urlList': urls}).encode()
    req = urllib.request.Request('https://api.indexnow.org/indexnow', data=corps, method='POST',
                                 headers={'Content-Type': 'application/json; charset=utf-8'})
    try:
        r = urllib.request.urlopen(req, timeout=30, context=ctx)
        print(f'{nom:11s} {len(urls)} URL → HTTP {r.status}')
    except urllib.error.HTTPError as e:
        print(f'{nom:11s} {len(urls)} URL → HTTP {e.code} {e.read()[:160]!r}')
