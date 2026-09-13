# -*- coding: utf-8 -*-
"""
Audit SEO / GEO des sorties de build (ce que Google et les IA lisent vraiment) :
Ramonville (dist), Portet (dist), les 7 satellites (.vercel/output/static).
Par page : titre, description, canonical, robots, og:image, H1, JSON-LD,
images (alt absent, alt générique, alt en double, dimensions). Entre pages et
entre sites : titres, descriptions et vignettes en double (règle d'Eddy :
jamais la même). Sortie : .research/suivi/audit-seo.md + résumé à l'écran.
"""
import collections, glob, html, io, json, os, re, sys
from html.parser import HTMLParser
sys.stdout.reconfigure(encoding='utf-8')
BC = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center')
SITES = {'ramonville': os.path.join(BC, 'Deployment', 'bc-ramonville', 'dist'),
         'portet': os.path.join(BC, 'Portet', 'boxing-center-portet', 'dist')}
for s in ['colomiers', 'muret', 'cugnaux', 'tournefeuille', 'labege', 'lunion', 'castelginest']:
    SITES[s] = os.path.join(BC, 'Deployment', f'boxing-center-{s}', '.vercel', 'output', 'static')
IGNORE = re.compile(r'[\\/](admin|api|_astro|assets|md|evals)[\\/]|404')
GENERIQUE = re.compile(r'^(image|photo|img|picture|logo|icon|icône|visuel|illustration|banner|bannière)[\s\d_-]*$', re.I)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self.in_title, self.in_h1, self.in_ld = '', False, False, False
        self.meta, self.links, self.h1, self.imgs, self.ld = {}, {}, [], [], []
        self._buf = ''

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == 'title': self.in_title = True
        elif tag == 'meta':
            k = a.get('name') or a.get('property')
            if k: self.meta[k.lower()] = a.get('content', '')
        elif tag == 'link' and a.get('rel'):
            self.links[a['rel'].lower()] = a.get('href', '')
        elif tag == 'h1': self.in_h1 = True; self.h1.append('')
        elif tag == 'img': self.imgs.append(a)
        elif tag == 'script' and a.get('type') == 'application/ld+json': self.in_ld = True; self._buf = ''

    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
        elif tag == 'h1': self.in_h1 = False
        elif tag == 'script' and self.in_ld:
            self.in_ld = False
            try:
                d = json.loads(self._buf)
                for x in (d if isinstance(d, list) else d.get('@graph', [d])):
                    t = x.get('@type') if isinstance(x, dict) else None
                    self.ld += t if isinstance(t, list) else [t] if t else []
            except Exception:
                self.ld.append('JSON-LD INVALIDE')

    def handle_data(self, d):
        if self.in_title: self.title += d
        if self.in_h1 and self.h1: self.h1[-1] += d
        if self.in_ld: self._buf += d


rapport, resume = ['# Audit SEO / GEO — sorties de build\n'], collections.Counter()
tous_titres, toutes_desc, toutes_og = collections.defaultdict(list), collections.defaultdict(list), collections.defaultdict(list)
for site, racine in SITES.items():
    if not os.path.isdir(racine):
        rapport.append(f'\n## {site} — build absent ({racine})\n'); continue
    pages = [p for p in glob.glob(os.path.join(racine, '**', 'index.html'), recursive=True) if not IGNORE.search(p[len(racine):])]
    rapport.append(f'\n## {site} — {len(pages)} pages\n')
    for p in sorted(pages):
        url = '/' + os.path.relpath(os.path.dirname(p), racine).replace('\\', '/').replace('.', '').strip('/')
        url = url if url.endswith('/') else url + '/'
        P = Page(); P.feed(io.open(p, encoding='utf-8', errors='replace').read())
        t, d = html.unescape(P.title.strip()), P.meta.get('description', '').strip()
        og = P.meta.get('og:image', '')
        pb = []
        if not t: pb.append('titre absent')
        elif len(t) > 65: pb.append(f'titre {len(t)} car.')
        elif len(t) < 25: pb.append(f'titre court ({len(t)})')
        if not d: pb.append('description absente')
        elif len(d) > 165: pb.append(f'description {len(d)} car.')
        elif len(d) < 70: pb.append(f'description courte ({len(d)})')
        if 'canonical' not in P.links: pb.append('canonical absente')
        if 'noindex' in P.meta.get('robots', ''): pb.append('noindex')
        if not og: pb.append('og:image absente')
        if len(P.h1) != 1: pb.append(f'{len(P.h1)} H1')
        if not P.ld: pb.append('aucun JSON-LD')
        if 'JSON-LD INVALIDE' in P.ld: pb.append('JSON-LD invalide')
        sans_alt = [i.get('src', '')[-40:] for i in P.imgs if 'alt' not in i]
        gen = [i.get('alt') for i in P.imgs if i.get('alt') and GENERIQUE.match(i['alt'].strip())]
        alts = [i.get('alt', '').strip() for i in P.imgs if i.get('alt', '').strip()]
        doublons = [a for a, n in collections.Counter(alts).items() if n > 1]
        sans_dim = [i.get('src', '')[-40:] for i in P.imgs if not (i.get('width') and i.get('height'))]
        if sans_alt: pb.append(f'{len(sans_alt)} img sans alt {sans_alt[:3]}')
        if gen: pb.append(f'alt générique {gen[:3]}')
        if doublons: pb.append(f'alt en double {[x[:40] for x in doublons[:2]]}')
        if sans_dim: pb.append(f'{len(sans_dim)} img sans dimensions')
        for x in pb: resume[f'{site}: ' + re.sub(r"[\d\[].*", '', x).strip()] += 1
        tous_titres[t].append(f'{site}{url}'); toutes_desc[d].append(f'{site}{url}')
        if og: toutes_og[og.split('?')[0].split('/')[-1] + '@' + site if False else og.split('?')[0]].append(f'{site}{url}')
        rapport.append(f'- `{url}` — {len(t)}/{len(d)} car. · H1 {len(P.h1)} · LD {sorted(set(P.ld))[:4]}' + (f' — **{" · ".join(pb)}**' if pb else ' — ok'))

rapport.append('\n## Doublons\n')
for nom, tab in (('titre', tous_titres), ('description', toutes_desc), ('og:image', toutes_og)):
    for k, v in tab.items():
        if k and len(v) > 1:
            rapport.append(f'- {nom} en double ({len(v)}) : {v[:6]} — « {k[:80]} »')
            resume[f'doublon {nom}'] += 1
out = os.path.join(BC, '.research', 'suivi', 'audit-seo.md')
io.open(out, 'w', encoding='utf-8').write('\n'.join(rapport))
print(out)
for k, v in sorted(resume.items()):
    print(f'  {v:4d}  {k}')
