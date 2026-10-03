# -*- coding: utf-8 -*-
"""
Les pages de tête de Boutique de Boxe, vues en production comme Googlebot les voit (03/10/2026) :
200, index, canonique = l'adresse, le titre et le H1 attendus, la vignette en PNG, la page dans le
plan du site, et le nombre de pages de la boutique qui la lient dans leur texte n'est pas mesuré
ici (audit-links.mjs le fait sur le build). On vérifie après déploiement, jamais sur la foi du build.

Usage : python boutique_en_ligne.py
"""
import re, ssl, sys, urllib.request, html
sys.stdout.reconfigure(encoding='utf-8')
B = 'https://www.boutique-de-boxe.com'
UA = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
ctx = ssl.create_default_context()

# chemin, début de titre attendu, H1 attendu
PAGES = [
    ('/materiel-boxe/', 'Matériel de boxe :', 'Matériel de boxe'),
    ('/vente-materiel-de-boxe/', 'Vente matériel de boxe', 'Vente de matériel de boxe en ligne.'),
    ('/materiel-boxe-thai/', 'Matériel de boxe thaï', 'Matériel de boxe thaï'),
    ('/materiel-kick-boxing/', 'Matériel de kick-boxing', 'Matériel de kick-boxing'),
    ('/materiel-boxe-francaise/', 'Matériel de boxe française', 'Matériel de boxe française'),
    ('/equipement-jjb/', 'Équipement JJB', 'Équipement JJB et grappling'),
    ('/materiel-boxe-debutant/', 'Matériel de boxe débutant', 'Matériel de boxe débutant'),
    ('/materiel-boxe-competition/', 'Matériel de boxe de compétition', 'Matériel de boxe de compétition'),
    ('/a-propos/', 'À propos de la boutique', 'À propos de la boutique'),
    ('/plan-du-site/', 'Plan du site', 'Le plan du site.'),
    ('/boutique-boxe/', 'Boutique boxe : matos boxe', 'Boutique boxe'),
    ('/guides/gants-de-boxe-cuir-ou-synthetique/', 'Gants de boxe en cuir ou en synthétique', 'Gants de boxe en cuir ou en synthétique : lequel choisir ?'),
    ('/guides/sac-de-frappe-suspendu-ou-sur-pied/', 'Sac de frappe suspendu ou sur pied', 'Sac de frappe suspendu ou sur pied : lequel choisir ?'),
    ('/guides/bandes-de-boxe-ou-sous-gants/', 'Bandes de boxe ou sous-gants', 'Bandes de boxe ou sous-gants : que mettre sous ses gants ?'),
    ('/guides/', 'Guides d’achat', 'Les guides d’achat.'),
    ('/sports-de-combat/', 'Sport de combat :', 'Les sports de combat, discipline par discipline.'),
    ('/les-arts-martiaux/', 'Arts martiaux :', 'Les arts martiaux, leur origine et leurs dojos.'),
]


def get(url):
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=40, context=ctx)
        return r.status, r.headers.get('content-type', ''), r.read()
    except urllib.error.HTTPError as e:
        return e.code, '', b''
    except Exception as e:
        return 0, str(e)[:60], b''


plie = lambda s: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).replace(' ', ' ').strip()
_, _, plan = get(B + '/sitemap.xml')
plan = plan.decode('utf-8', 'replace')
fautes = 0
for chemin, titre, h1 in PAGES:
    code, _, corps = get(B + chemin)
    h = corps.decode('utf-8', 'replace')
    t = plie((re.search(r'<title>([\s\S]*?)</title>', h) or [0, ''])[1])
    vu = plie((re.search(r'<h1[^>]*>([\s\S]*?)</h1>', h) or [0, ''])[1])
    canon = (re.search(r'<link rel="canonical" href="([^"]+)"', h) or [0, ''])[1]
    robots = (re.search(r'<meta name="robots" content="([^"]+)"', h) or [0, 'index, follow'])[1]
    og = html.unescape((re.search(r'<meta property="og:image" content="([^"]+)"', h) or [0, ''])[1])
    ocode, otype, _ = get(og) if og else (0, '', b'')
    ok = {
        '200': code == 200,
        'titre': t.startswith(titre.replace(' ', ' ')) or t.replace(' ', ' ').startswith(titre),
        'H1': vu.replace(' ', ' ') == h1,
        'canonique': canon == B + chemin,
        'index': 'noindex' not in robots,
        'vignette': ocode == 200 and 'png' in otype,
        'plan': (B + chemin) in plan,
    }
    rate = [k for k, v in ok.items() if not v]
    fautes += bool(rate)
    print('%s %-46s %s%s' % ('✓' if not rate else '✗', chemin, t[:62], ('   ✗ ' + ', '.join(rate) + (' (H1 vu : %s)' % vu[:60] if 'H1' in rate else '')) if rate else ''))
print('\n%d page(s) en défaut sur %d' % (fautes, len(PAGES)))
sys.exit(1 if fautes else 0)
