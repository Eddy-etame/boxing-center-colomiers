# -*- coding: utf-8 -*-
"""
Les pages de conseil, vues en ligne comme Googlebot les voit : chaque page
répond 200, se range (index, follow), porte son adresse canonique, sa vignette
répond 200 en JPEG, et le plan du site la déclare. On vérifie après
déploiement, sur le domaine réel — jamais sur la foi du build.

Usage : python conseils_en_ligne.py            (tous les sites)
        python conseils_en_ligne.py muret      (un seul)
"""
import io, json, os, re, ssl, sys, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
ICI = os.path.dirname(os.path.abspath(__file__))
UA = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
ctx = ssl.create_default_context()

SITES = {
    'portet': ('https://boxing-center-portet.fr', ['/conseils/', '/conseils/equipement-boxe-debutant/', '/conseils/equipement-boxe-enfant/']),
    'ramonville': ('https://mmatoulouse.com', ['/conseils/', '/conseils/equipement-mma-debutant/', '/conseils/equipement-boxe-femme/']),
    'blagnac': ('https://www.club-boxe-blagnac.fr', ['/gants-de-boxe-enfant/', '/sac-de-sport-boxe/']),
}
for s in ('colomiers', 'tournefeuille', 'cugnaux', 'muret', 'labege', 'lunion', 'castelginest'):
    d = json.load(io.open(os.path.join(ICI, 'conseils', s + '.json'), encoding='utf-8'))
    SITES[s] = ('https://www.boxingcenter-%s.fr' % s, ['/conseils/'] + ['/conseils/%s/' % a['id'] for a in d['articles']])


def get(url):
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=30, context=ctx)
        return r.status, r.headers.get('content-type', ''), r.read()
    except urllib.error.HTTPError as e:
        return e.code, '', b''
    except Exception as e:
        return 0, str(e)[:60], b''


fautes = 0
for site in (sys.argv[1:] or list(SITES)):
    base, chemins = SITES[site]
    _, _, plan = get(base + '/sitemap.xml')
    plan = plan.decode('utf-8', 'replace')
    for c in chemins:
        code, _, corps = get(base + c)
        h = corps.decode('utf-8', 'replace')
        canon = (re.search(r'<link rel="canonical" href="([^"]+)"', h) or [None, ''])[1]
        robots = (re.search(r'<meta name="robots" content="([^"]+)"', h) or [None, ''])[1]
        og = (re.search(r'<meta property="og:image" content="([^"]+)"', h) or [None, ''])[1]
        ocode, otype, _ = get(og) if og else (0, '', b'')
        boutique = len(set(re.findall(r'href="(https://www\.boutique-de-boxe\.com/[^"]*)"', h)))
        ok = (code == 200 and canon == base + c and robots.replace(' ', '').startswith('index,follow') and ocode == 200 and 'jpeg' in otype and (base + c) in plan)
        fautes += 0 if ok else 1
        print('%s %-13s %-42s %s · canon %s · %s · vignette %s · plan %s · %d lien(s) boutique' % (
            '✓' if ok else '✗', site, c, code, 'ok' if canon == base + c else canon or 'absent',
            'index' if robots.replace(' ', '').startswith('index,follow') else robots or 'robots absent',
            ocode, 'oui' if (base + c) in plan else 'NON', boutique))
print('\n%d défaut(s)' % fautes)
sys.exit(1 if fautes else 0)
