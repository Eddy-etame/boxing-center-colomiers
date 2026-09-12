# -*- coding: utf-8 -*-
"""
Le classement réel, requête par requête, sur les moteurs qu'on peut lire
sans contourner quoi que ce soit : Bing (qui nourrit ChatGPT, Copilot et
DuckDuckGo) et DuckDuckGo HTML. Google se lit à la main, dans le navigateur.

Usage : python rang.py [bing|ddg] [site…]
Lecture seule, une requête toutes les quelques secondes. Si un moteur
renvoie un défi (captcha), on s'arrête : rien n'est contourné.
"""
import sys, re, time, html, urllib.request, urllib.parse, ssl, json, os
sys.stdout.reconfigure(encoding='utf-8')

MOTEUR = sys.argv[1] if len(sys.argv) > 1 else 'bing'
FILTRE = sys.argv[2:]
VILLES = {
  'muret': ['Muret'],
  'cugnaux': ['Cugnaux', 'Villeneuve-Tolosane', 'Frouzins', 'Seysses'],
  'tournefeuille': ['Tournefeuille', 'Plaisance-du-Touch', 'Fonsorbes'],
  'labege': ['Labège', 'Saint-Orens', 'Castanet-Tolosan'],
  'lunion': ["L'Union", 'Saint-Jean', 'Rouffiac-Tolosan'],
  'castelginest': ['Castelginest', 'Saint-Alban', 'Fenouillet', 'Aucamville', 'Launaguet'],
  'colomiers': ['Colomiers'],
}
MOTIFS = ['club de boxe {v}', 'boxe {v}', 'club mma {v}', 'salle mma {v}', 'boxe anglaise {v}', 'sport de combat {v}', 'club boxe thai {v}', 'kick boxing {v}']
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36'
ctx = ssl.create_default_context()

def cherche(q):
    if MOTEUR == 'bing':
        url = 'https://www.bing.com/search?' + urllib.parse.urlencode({'q': q, 'cc': 'FR', 'setlang': 'fr', 'count': '50'})
    else:
        url = 'https://html.duckduckgo.com/html/?' + urllib.parse.urlencode({'q': q, 'kl': 'fr-fr'})
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'fr-FR,fr;q=0.9'})
    body = urllib.request.urlopen(req, timeout=30, context=ctx).read().decode('utf-8', 'ignore')
    if re.search(r'captcha|unusual traffic|anomaly', body, re.I) and 'b_algo' not in body and 'result__a' not in body:
        raise RuntimeError('défi du moteur — arrêt')
    if MOTEUR == 'bing':
        liens = re.findall(r'<li class="b_algo"[\s\S]*?<a[^>]+href="(https?://[^"]+)"', body)
    else:
        liens = [urllib.parse.unquote(m) for m in re.findall(r'class="result__a" href="[^"]*?uddg=([^"&]+)', body)]
    vus, res = set(), []
    for l in liens:
        d = urllib.parse.urlparse(html.unescape(l)).netloc.replace('www.', '')
        if d and d not in vus:
            vus.add(d); res.append(d)
    return res

sortie = {}
for site, villes in VILLES.items():
    if FILTRE and site not in FILTRE: continue
    dom = f'boxingcenter-{site}.fr'
    print(f'\n══════ {dom} ({MOTEUR})')
    for v in villes:
        for m in (MOTIFS if v == villes[0] else MOTIFS[:3]):
            q = m.format(v=v)
            try:
                r = cherche(q)
            except Exception as e:
                print(f'  {q:40s} ERREUR {e}'); sortie[q] = None
                if 'défi' in str(e): sys.exit(1)
                continue
            pos = next((i + 1 for i, d in enumerate(r) if d == dom), None)
            autres = [d for d in r if d.startswith('boxingcenter-') and d != dom]
            sortie[q] = pos
            print(f'  {q:40s} {("#" + str(pos)) if pos else "—":>4}  sur {len(r):2d} · devant : {", ".join(r[:max(0,(pos or 4)-1)][:4])}' + (f' · frères : {autres}' if autres else ''))
            time.sleep(2.5)
json.dump(sortie, open(os.path.join(os.path.dirname(__file__), f'rang_{MOTEUR}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
