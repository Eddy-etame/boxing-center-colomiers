# -*- coding: utf-8 -*-
"""
Diagnostic EN LIGNE des sept domaines : ce que Google, Bing et les robots
d'IA reçoivent réellement. Aucune écriture, uniquement des lectures HTTP.
"""
import sys, re, json, ssl, urllib.request, urllib.error, http.client
from urllib.parse import urlparse
sys.stdout.reconfigure(encoding='utf-8')

SITES = ['colomiers', 'muret', 'cugnaux', 'tournefeuille', 'labege', 'lunion', 'castelginest']
UA = {
  'navigateur': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36',
  'Googlebot': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
  'Bingbot': 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
  'GPTBot': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.2; +https://openai.com/gptbot)',
  'OAI-SearchBot': 'Mozilla/5.0 (compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot)',
  'ClaudeBot': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; ClaudeBot/1.0; +claudebot@anthropic.com)',
  'PerplexityBot': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)',
}
ctx = ssl.create_default_context()

class PasDeRedirection(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None

def get(url, ua='navigateur', suivre=False, tete=False):
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx), *( [] if suivre else [PasDeRedirection()] ))
    req = urllib.request.Request(url, headers={'User-Agent': UA[ua], 'Accept-Language': 'fr-FR,fr;q=0.9'}, method='HEAD' if tete else 'GET')
    try:
        r = opener.open(req, timeout=25)
        return r.status, dict(r.headers), (b'' if tete else r.read()), r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), (e.read() if not tete else b''), url
    except Exception as e:
        return None, {}, str(e).encode(), url

for s in SITES:
    dom = f'boxingcenter-{s}.fr'
    www = f'https://www.{dom}/'
    print(f'\n══════ {dom}')
    # 1. redirections
    for depart in [f'http://{dom}/', f'https://{dom}/', f'http://www.{dom}/', www]:
        st, h, _, _ = get(depart)
        print(f'  {depart:48s} → {st} {h.get("Location", h.get("location", ""))}')
    st, h, body, final = get(www, suivre=True)
    html = body.decode('utf-8', 'ignore')
    canon = re.findall(r'<link rel="canonical" href="([^"]+)"', html)
    robots_meta = re.findall(r'<meta name="robots" content="([^"]+)"', html)
    print(f'  accueil : {st} · canonical={canon} · robots meta={robots_meta} · x-robots-tag={h.get("x-robots-tag") or h.get("X-Robots-Tag")} · server={h.get("server")} · age={h.get("age")} · x-vercel-cache={h.get("x-vercel-cache")}')
    TITRE = re.findall(r'<title>([^<]*)</title>', html)
    print(f'  title   : {TITRE}')
    ICONES = re.findall(r'<link rel="(?:icon|apple-touch-icon|shortcut icon|manifest)"[^>]*>', html)
    OG = re.findall(r'<meta property="og:image" content="([^"]+)"', html)
    print(f'  icons   : {ICONES}')
    print(f'  og:image: {OG} · max-image-preview: {"max-image-preview" in html}')
    lds = re.findall(r'<script type="application/ld\+json"[^>]*>([\s\S]*?)</script>', html)
    types = []
    for l in lds:
        try:
            d = json.loads(l)
            g = d.get('@graph', [d])
            types += [x.get('@type') for x in g]
        except Exception as e:
            types.append(f'JSON INVALIDE {e}')
    print(f'  json-ld : {types}')
    # 2. robots, sitemap, llms
    st, h, body, _ = get(www + 'robots.txt', suivre=True)
    print(f'  robots.txt {st} :', ' | '.join(l for l in body.decode("utf-8","ignore").splitlines() if l.strip())[:400])
    st, h, body, _ = get(www + 'sitemap.xml', suivre=True)
    locs = re.findall(r'<loc>([^<]+)</loc>', body.decode('utf-8', 'ignore'))
    print(f'  sitemap {st} : {len(locs)} URL · domaines={sorted(set(urlparse(u).netloc for u in locs))}')
    ko = []
    for u in locs:
        st2, _, _, _ = get(u, tete=True)
        if st2 != 200: ko.append((u, st2))
    print(f'  URL du sitemap en échec : {ko if ko else "aucune"}')
    st, h, body, _ = get(www + 'llms.txt', suivre=True)
    print(f'  llms.txt {st} · {len(body)} octets · content-type={h.get("content-type")}')
    for f in ['favicon.ico', 'favicon-192.png', 'apple-touch-icon.png', 'site.webmanifest', 'og/accueil.jpg', 'og/accueil-carre.jpg', 'og/accueil.png']:
        st, h, _, _ = get(www + f, tete=True)
        print(f'  /{f:22s} {st} {h.get("Content-Type", h.get("content-type",""))}')
    # 3. robots d'IA et moteurs
    ligne = []
    for ua in UA:
        st, h, body, _ = get(www, ua=ua, suivre=True)
        ligne.append(f'{ua}={st}/{len(body)//1024}Ko')
    print('  UA :', ' · '.join(ligne))
