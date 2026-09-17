# -*- coding: utf-8 -*-
"""
Contrôle EN LIGNE des neuf sites (Eddy, 13/09 : « check all the nine projects…
make sure everything is at baffled bar »). Ce que voient Google, les IA et les
visiteurs, pas les fichiers du disque.

Par site : robots.txt, sitemap.xml, llms.txt ; chaque page du plan en 200 ;
chaque lien interne en 200 ; chaque lien externe joignable (les réseaux sociaux
qui refusent les robots sont notés « non vérifiable », pas en panne) ; la
vignette og:image en 200 ; aucun ancien numéro (05 62 24 46 82, 06 87 90 02 16).
Sortie : .research/suivi/audit-live.md + résumé à l'écran.
"""
import concurrent.futures as cf, io, os, re, ssl, sys, urllib.error, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
SITES = {'portet': 'https://boxing-center-portet.fr', 'ramonville': 'https://mmatoulouse.com'}
for s in ['colomiers', 'muret', 'cugnaux', 'tournefeuille', 'labege', 'lunion', 'castelginest']:
    SITES[s] = f'https://www.boxingcenter-{s}.fr'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'}
ctx = ssl.create_default_context()
SEP = r'[\s. -]?'
ANCIENS = re.compile(r'0?5' + SEP + r'62' + SEP + r'24' + SEP + r'46' + SEP + r'82|0?6' + SEP + r'87' + SEP + r'90' + SEP + r'02' + SEP + r'16|33562244682|33687900216')
SOCIAUX = re.compile(r'instagram\.com|facebook\.com|tiktok\.com|linkedin\.com|youtube\.com|x\.com|twitter\.com|wa\.me|whatsapp')
cache = {}


def get(url):
    if url in cache:
        return cache[url]
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25, context=ctx) as r:
            type_ = r.headers.get('content-type', '')
            corps = r.read().decode('utf-8', 'replace') if 'html' in type_ or 'xml' in type_ or 'text' in type_ else ''
            res = (r.status, r.geturl(), corps)
    except urllib.error.HTTPError as e:
        res = (e.code, url, '')
    except Exception as e:
        res = (0, url, str(e)[:90])
    cache[url] = res
    return res


def meme_site(a, b):
    h = lambda u: urllib.parse.urlparse(u).netloc.replace('www.', '')
    return h(a) == h(b)


rapport, resume = ['# Contrôle en ligne des neuf sites\n'], {}
externes = {}
for nom, base in SITES.items():
    lignes, pb = [], []
    for f in ('robots.txt', 'sitemap.xml', 'llms.txt'):
        st = get(f'{base}/{f}')[0]
        if st != 200:
            pb.append(f'/{f} → {st}')
    sm = get(f'{base}/sitemap.xml')[2]
    pages = sorted(set(u for u in re.findall(r'<loc>\s*([^<\s]+)\s*</loc>', sm)
                       if meme_site(u, base) and not re.search(r'\.(jpe?g|png|webp|avif)$', u)))
    with cf.ThreadPoolExecutor(10) as ex:
        res_pages = dict(zip(pages, ex.map(get, pages)))
    internes = set()
    for u, (st, fin, corps) in res_pages.items():
        if st != 200:
            pb.append(f'page {u} → {st}')
            continue
        if ANCIENS.search(corps):
            pb.append(f'ANCIEN NUMÉRO sur {u} : « {ANCIENS.search(corps).group(0)} »')
        og = re.search(r'property="og:image"\s+content="([^"]+)"', corps)
        if not og:
            pb.append(f'og:image absente sur {u}')
        else:
            internes.add(og.group(1))
        for href in re.findall(r'href="([^"#]+)"', corps):
            if href.startswith(('mailto:', 'tel:', 'javascript:', 'sms:', 'data:')):
                continue
            abs_ = urllib.parse.urljoin(u, href)
            if not abs_.startswith('http'):
                continue
            if meme_site(abs_, base):
                internes.add(abs_)
            else:
                externes.setdefault(abs_, set()).add(nom)
    with cf.ThreadPoolExecutor(10) as ex:
        res_int = dict(zip(sorted(internes), ex.map(get, sorted(internes))))
    casses = [(u, r[0]) for u, r in res_int.items() if r[0] != 200]
    for u, st in casses:
        pb.append(f'lien interne cassé {u} → {st}')
    resume[nom] = (len(pages), len(internes), len(pb))
    rapport.append(f'\n## {nom} — {len(pages)} pages, {len(internes)} liens internes vérifiés\n')
    rapport += [f'- {x}' for x in pb] or ['- rien à signaler']

# les liens externes, une fois chacun
with cf.ThreadPoolExecutor(10) as ex:
    res_ext = dict(zip(sorted(externes), ex.map(get, sorted(externes))))
rapport.append('\n## Liens externes\n')
ko = 0
for u, (st, fin, _) in sorted(res_ext.items()):
    if st == 200:
        continue
    etiquette = 'non vérifiable (refuse les robots)' if SOCIAUX.search(u) and st in (0, 400, 403, 429, 999) else 'EN PANNE'
    if etiquette == 'EN PANNE':
        ko += 1
    rapport.append(f'- {etiquette} {u} → {st} (sur : {", ".join(sorted(externes[u]))})')
out = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', '.research', 'suivi', 'audit-live.md')
io.open(out, 'w', encoding='utf-8').write('\n'.join(rapport))
print(out)
for nom, (p, i, n) in resume.items():
    print(f'  {nom:14s} {p:3d} pages · {i:4d} liens internes · {n} problème(s)')
print(f'  liens externes : {len(res_ext)} vérifiés, {ko} en panne')
