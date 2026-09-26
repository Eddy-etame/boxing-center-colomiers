# -*- coding: utf-8 -*-
"""LIENS DE LA FAMILLE — qui lie qui, et ce que chaque page dit aux robots.

Pour chacun des quinze domaines de la famille : les URL de son plan du site,
le robots (meta et en-tête), la canonique, les balises de vérification de
l'accueil, et chaque lien sortant vers un autre domaine de la famille
(suivi ou nofollow). En sortie : un tableau des liens entrants par domaine
(« ← NONE » = personne ne lie ce site, et un moteur ne l'atteint par aucune
page qu'il connaît — le cas de club-boxe-blagnac.fr le 26/09/2026), et un
JSON complet pour comparer d'une semaine à l'autre.

Usage :  python liens_famille.py <sortie.json>
Lecture seule ; robot déclaré ; une requête par page.
"""
import sys, re, json, html, urllib.request, urllib.error, concurrent.futures as cf
sys.stdout.reconfigure(encoding='utf-8')

OUT = sys.argv[1]
UA = {'User-Agent': 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'}
FAMILY = ['club-boxe-blagnac.fr', 'boxingcenter-colomiers.fr', 'boxingcenter-tournefeuille.fr', 'boxingcenter-cugnaux.fr',
          'boxingcenter-muret.fr', 'boxingcenter-labege.fr', 'boxingcenter-lunion.fr', 'boxingcenter-castelginest.fr',
          'boxe-toulouse.com', 'club-boxe-toulouse.com', 'mmatoulouse.com', 'clubmma.fr', 'boxing-center-portet.fr',
          'noble-art-portesien.com', 'boxingcenter.fr']


def get(u):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30)
        return r.getcode(), {k.lower(): v for k, v in r.headers.items()}, r.read().decode('utf-8', 'ignore'), r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, {}, '', u
    except Exception as e:
        return 0, {}, '', u


def host(u):
    m = re.match(r'https?://(?:www\.)?([^/:]+)', u)
    return m.group(1).lower() if m else ''


def sitemap_urls(dom):
    urls = []
    for sm in (f'https://www.{dom}/sitemap.xml', f'https://{dom}/sitemap.xml', f'https://www.{dom}/sitemap_index.xml', f'https://{dom}/sitemap-index.xml', f'https://www.{dom}/sitemap-index.xml'):
        code, _, body, _ = get(sm)
        if code == 200 and '<loc>' in body:
            locs = re.findall(r'<loc>\s*([^<\s]+)\s*</loc>', body)
            subs = [l for l in locs if l.endswith('.xml')]
            pages = [l for l in locs if not l.endswith('.xml')]
            for s in subs[:8]:
                c2, _, b2, _ = get(s)
                if c2 == 200:
                    pages += [l for l in re.findall(r'<loc>\s*([^<\s]+)\s*</loc>', b2) if not l.endswith('.xml')]
            urls = pages
            break
    return list(dict.fromkeys(urls))[:120]


def page(u):
    code, hdr, body, final = get(u)
    robots = ' '.join(re.findall(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)', body, re.I))
    canon = re.findall(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', body, re.I)
    title = re.findall(r'<title>([\s\S]*?)</title>', body, re.I)
    out = []
    for m in re.finditer(r'<a\b([^>]*)href=["\'](https?://[^"\']+)["\']([^>]*)>', body, re.I):
        h = host(m.group(2))
        attrs = (m.group(1) + m.group(3)).lower()
        if h and any(h == f or h.endswith('.' + f) for f in FAMILY):
            out.append({'to': h, 'href': m.group(2), 'nofollow': 'nofollow' in attrs})
    text = re.sub(r'\s+', ' ', html.unescape(re.sub(r'(?s)<[^>]+>', ' ', re.sub(r'(?is)<(script|style|svg)\b.*?</\1>', ' ', body))))
    return {'url': u, 'code': code, 'final': final, 'xrobots': hdr.get('x-robots-tag', ''), 'robots': robots,
            'canonical': canon[0] if canon else '', 'title': html.unescape(title[0]).strip() if title else '',
            'words': len(re.findall(r'\w+', text)), 'family_links': out}


result = {}
for dom in FAMILY:
    code, hdr, home, final = get(f'https://www.{dom}/')
    if code != 200:
        code, hdr, home, final = get(f'https://{dom}/')
    verif = re.findall(r'<meta[^>]+name=["\'](google-site-verification|msvalidate\.01|yandex-verification)["\'][^>]+content=["\']([^"\']+)', home, re.I)
    urls = sitemap_urls(dom) or [final]
    with cf.ThreadPoolExecutor(8) as ex:
        pages = list(ex.map(page, urls))
    result[dom] = {'home_code': code, 'home_final': final, 'verification_meta': verif, 'pages': pages}
    noidx = [p['url'] for p in pages if 'noindex' in (p['robots'] + p['xrobots']).lower()]
    outlinks = {}
    for p in pages:
        for l in p['family_links']:
            if l['to'].endswith(dom):
                continue
            outlinks.setdefault(l['to'], set()).add(p['url'])
    print(f"\n== {dom}  home {code} → {final}  | sitemap pages {len(urls)} | noindex {len(noidx)} | verif meta {verif or '-'}")
    for to, src in sorted(outlinks.items()):
        print(f"   → {to:30s} from {len(src)} page(s)")
    result[dom]['outlinks'] = {k: sorted(v) for k, v in outlinks.items()}

inbound = {d: {} for d in FAMILY}
for d, r in result.items():
    for to, src in r['outlinks'].items():
        key = next((f for f in FAMILY if to == f or to.endswith('.' + f)), to)
        inbound.setdefault(key, {})[d] = len(src)
print('\n=== INBOUND FROM FAMILY (pages linking) ===')
for d in FAMILY:
    print(f"{d:30s} ← {inbound.get(d) or 'NONE'}")
json.dump({'domains': result, 'inbound': inbound}, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
