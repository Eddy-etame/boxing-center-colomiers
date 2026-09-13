# -*- coding: utf-8 -*-
"""
Audit SEO en ligne d'un site : lit robots.txt, le sitemap, llms.txt, puis
chaque page du sitemap, et relève ce que voient Google et les moteurs de
réponse. Aucun écrit, aucune soumission.
Usage : python diag_club.py https://domaine.fr [https://autre.fr …]
"""
import io, json, re, ssl, sys, urllib.request, urllib.error
from html import unescape
sys.stdout.reconfigure(encoding='utf-8')
CTX = ssl.create_default_context()
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36'


def get(url, ua=UA):
    req = urllib.request.Request(url, headers={'User-Agent': ua, 'Accept-Language': 'fr-FR'})
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=25) as r:
            return r.status, r.geturl(), dict(r.headers), r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, url, dict(e.headers or {}), ''
    except Exception as e:
        return 0, url, {}, str(e)


def meta(h, attr, val):
    m = re.search(r'<meta[^>]+' + attr + r'=["\']' + re.escape(val) + r'["\'][^>]*>', h, re.I)
    if not m:
        return None
    c = re.search(r'content=["\']([^"\']*)', m.group(0), re.I)
    return unescape(c.group(1)) if c else ''


def lien(h, rel):
    for m in re.finditer(r'<link[^>]+>', h, re.I):
        t = m.group(0)
        if re.search(r'rel=["\'][^"\']*\b' + re.escape(rel) + r'\b', t, re.I):
            hr = re.search(r'href=["\']([^"\']*)', t, re.I)
            return hr.group(1) if hr else ''
    return None


def texte(h):
    h = re.sub(r'<(script|style|noscript|svg|template)[\s\S]*?</\1>', ' ', h, flags=re.I)
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', ' ', h))).strip()


def jsonld_types(h):
    types = []
    for m in re.finditer(r'<script[^>]+application/ld\+json[^>]*>([\s\S]*?)</script>', h, re.I):
        try:
            d = json.loads(m.group(1))
        except Exception:
            types.append('JSON-LD INVALIDE')
            continue
        pile = [d]
        while pile:
            x = pile.pop()
            if isinstance(x, list):
                pile.extend(x)
            elif isinstance(x, dict):
                t = x.get('@type')
                if t:
                    types.extend(t if isinstance(t, list) else [t])
                pile.extend(v for v in x.values() if isinstance(v, (dict, list)))
    return sorted(set(types))


def auditer(base):
    base = base.rstrip('/')
    print(f'\n════════ {base}')
    s, fin, hd, _ = get(base + '/')
    print(f'  accueil : {s} → {fin}')
    for variante in (base.replace('https://www.', 'https://') if '://www.' in base else base.replace('https://', 'https://www.'),
                     base.replace('https://', 'http://')):
        s2, fin2, _, _ = get(variante + '/')
        print(f'  {variante} → {s2} {fin2}')
    s, _, _, robots = get(base + '/robots.txt')
    sitemaps = re.findall(r'(?im)^sitemap:\s*(\S+)', robots)
    agents = re.findall(r'(?im)^user-agent:\s*(\S+)', robots)
    print(f'  robots.txt : {s} · {len(agents)} groupes ({", ".join(agents[:8])}{"…" if len(agents) > 8 else ""}) · sitemaps : {sitemaps or "AUCUN"}')
    if re.search(r'(?im)^user-agent:\s*\*\s*$[\s\S]*?^disallow:\s*/\s*$', robots):
        print('  ✗ robots.txt : Disallow: / sous User-agent: *')
    for f in ('/llms.txt', '/llms-full.txt', '/ai.txt', '/.well-known/mcp.json', '/site.webmanifest', '/favicon.ico'):
        s, _, hd2, corps = get(base + f)
        print(f'  {f:22s} {s} {len(corps)} o')
    urls = []
    for sm in (sitemaps or [base + '/sitemap.xml']):
        s, _, _, x = get(sm)
        locs = re.findall(r'<loc>\s*([^<\s]+)\s*</loc>', x)
        enfants = [l for l in locs if l.endswith('.xml')]
        for e in enfants:
            _, _, _, xe = get(e)
            urls += [l for l in re.findall(r'<loc>\s*([^<\s]+)\s*</loc>', xe) if not l.endswith('.xml')]
        urls += [l for l in locs if not l.endswith('.xml')]
    urls = list(dict.fromkeys(urls))
    print(f'  sitemap : {len(urls)} URL')
    titres, descs, ogs, constats = {}, {}, {}, []
    for u in urls[:60]:
        s, fin, hd, h = get(u)
        chemin = re.sub(r'^https?://[^/]+', '', u) or '/'
        if s != 200:
            constats.append(f'{chemin} — HTTP {s}')
            continue
        t = unescape((re.search(r'<title[^>]*>([\s\S]*?)</title>', h, re.I) or [None, ''])[1]).strip()
        d = meta(h, 'name', 'description') or ''
        rb = (meta(h, 'name', 'robots') or '') + ' ' + hd.get('X-Robots-Tag', hd.get('x-robots-tag', ''))
        can = lien(h, 'canonical')
        og = meta(h, 'property', 'og:image')
        h1 = re.findall(r'<h1[^>]*>([\s\S]*?)</h1>', h, re.I)
        types = jsonld_types(h)
        mots = len(texte(h).split())
        sans_alt = len([i for i in re.findall(r'<img\b[^>]*>', h, re.I) if not re.search(r'\salt=', i)])
        lang = (re.search(r'<html[^>]*lang=["\']([^"\']+)', h, re.I) or [None, '?'])[1]
        print(f'  {chemin[:34]:34s} t{len(t):3d} d{len(d):3d} h1:{len(h1)} mots:{mots:5d} ld:{",".join(types)[:60]}')
        if not t: constats.append(f'{chemin} — sans <title>')
        elif len(t) > 65: constats.append(f'{chemin} — titre de {len(t)} car. (tronqué dans Google) : « {t[:70]} »')
        if t in titres: constats.append(f'{chemin} — même titre que {titres[t]}')
        titres.setdefault(t, chemin)
        if not d: constats.append(f'{chemin} — sans meta description')
        elif len(d) > 165: constats.append(f'{chemin} — description de {len(d)} car.')
        elif len(d) < 70: constats.append(f'{chemin} — description courte ({len(d)} car.)')
        if d and d in descs: constats.append(f'{chemin} — même description que {descs[d]}')
        if d: descs.setdefault(d, chemin)
        if 'noindex' in rb.lower(): constats.append(f'{chemin} — NOINDEX ({rb.strip()})')
        if can is None: constats.append(f'{chemin} — sans canonical')
        elif can.rstrip('/') != u.rstrip('/') and can.rstrip('/') != fin.rstrip('/'):
            constats.append(f'{chemin} — canonical ailleurs : {can}')
        if not og: constats.append(f'{chemin} — sans og:image')
        elif og in ogs: constats.append(f'{chemin} — même og:image que {ogs[og]}')
        if og: ogs.setdefault(og, chemin)
        if len(h1) != 1: constats.append(f'{chemin} — {len(h1)} <h1>')
        if not types: constats.append(f'{chemin} — aucun JSON-LD')
        if sans_alt: constats.append(f'{chemin} — {sans_alt} <img> sans alt')
        if mots < 250: constats.append(f'{chemin} — {mots} mots seulement')
        if lang[:2] != 'fr': constats.append(f'{chemin} — lang="{lang}"')
    print(f'  ── {len(constats)} constat(s)')
    for c in constats:
        print('   ·', c)


for b in sys.argv[1:]:
    auditer(b)
