# -*- coding: utf-8 -*-
"""
L'audit des demandes du patron, par script — pas par agents.

Pour chaque site : chaque motif (ville + communes) est-il couvert ? où ?
Les pages communes existent-elles, sont-elles indexables, liées, dans le
sitemap ? Les sorties vers le club (accueil, plannings, tarifs) pointent-elles
le bon domaine ? Quels téléphones et mails le build porte-t-il ?
"""
import io, re, sys, html, os, glob, unicodedata, json
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"C:\Users\Mommy Jayce\Desktop\Boxing Center\Deployment"
COMPLETS = ['boxe {v}', 'club de boxe {v}', 'boxe anglaise {v}', 'club MMA {v}', 'salle MMA {v}',
            'sport de combat {v}', 'club boxe thaï {v}', 'club kick boxing {v}', 'boxe pieds poings {v}']
MURET = COMPLETS[:6]
SITES = [
  dict(id='muret', ville='Muret', motifs=MURET, communes=[], clubs=['boxing-center-portet.fr']),
  dict(id='cugnaux', ville='Cugnaux', motifs=COMPLETS, communes=['Villeneuve-Tolosane', 'Frouzins', 'Seysses'], clubs=['boxing-center-portet.fr']),
  dict(id='tournefeuille', ville='Tournefeuille', motifs=COMPLETS, communes=['Fonsorbes', 'Plaisance-du-Touch'], clubs=['boxing-center-portet.fr', 'club-boxe-toulouse.com']),
  dict(id='labege', ville='Labège', motifs=COMPLETS, communes=['Saint-Orens', 'Castanet-Tolosan'], clubs=['mmatoulouse.com']),
  dict(id='lunion', ville="L'Union", motifs=COMPLETS, communes=['Saint-Jean', 'Rouffiac-Tolosan'], clubs=['clubmma.fr']),
  dict(id='castelginest', ville='Castelginest', motifs=COMPLETS, communes=['Saint-Alban', 'Fenouillet', 'Aucamville', 'Launaguet'], clubs=['clubmma.fr']),
]
LIAISONS = r"(?:\s+\S+){0,4}\s+"

def plat(s):
    s = s.replace('’', ' ').replace("'", ' ').replace('‘', ' ')
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    s = re.sub(r"[^a-z0-9 ]+", ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

def variantes(mot):
    m = plat(mot)
    v = {m}
    v.add(m.replace('kick boxing', 'kick-boxing').replace('pieds poings', 'pieds-poings'))
    return v

def texte_visible(h):
    h = re.sub(r'<(script|style|noscript|svg|template)[\s\S]*?</\1>', ' ', h)
    h = re.sub(r'<[^>]+>', ' ', h)
    return re.sub(r'\s+', ' ', html.unescape(h))

def balises(h, nom):
    return [re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', m))).strip()
            for m in re.findall(rf'<{nom}[^>]*>([\s\S]*?)</{nom}>', h)]

def couvre(motif, phrase):
    """Tous les mots du motif, dans l'ordre, avec seulement des liaisons entre eux."""
    p = plat(phrase)
    for v in variantes(motif):
        mots = v.split()
        if not mots: continue
        motif_re = LIAISONS.join(re.escape(w) for w in mots)
        if re.search(r'\b' + motif_re + r'\b', p): return True
    return False

def exact(motif, phrase):
    p = plat(phrase)
    return any(re.search(r'\b' + re.escape(v) + r'\b', p) for v in variantes(motif))

def pages(dist):
    out = {}
    for f in glob.glob(os.path.join(dist, '**', 'index.html'), recursive=True):
        route = '/' + os.path.relpath(os.path.dirname(f), dist).replace('\\', '/').strip('.')
        route = route.replace('//', '/')
        if not route.endswith('/'): route += '/'
        out[route] = io.open(f, encoding='utf-8', errors='ignore').read()
    return out

rapport = {}
for s in SITES:
    dist = os.path.join(BASE, f"boxing-center-{s['id']}", '.vercel', 'output', 'static')
    P = pages(dist)
    sitemap = io.open(os.path.join(dist, 'sitemap.xml'), encoding='utf-8').read() if os.path.exists(os.path.join(dist, 'sitemap.xml')) else ''
    accueil = P.get('/', '')
    lieux = [s['ville']] + s['communes']
    res = dict(motifs=[], communes=[], clubs={}, contacts={}, alias=[])
    for lieu in lieux:
        for m in s['motifs']:
            motif = m.replace('{v}', lieu)
            meilleur = None
            for route, h in P.items():
                if '<meta name="robots" content="noindex' in h: continue
                t = balises(h, 'title'); h1 = balises(h, 'h1'); h2 = balises(h, 'h2'); h3 = balises(h, 'h3')
                desc = re.findall(r'<meta name="description" content="([^"]*)"', h)
                zones = [('title', t), ('h1', h1), ('h2', h2), ('h3', h3), ('description', desc)]
                for nom, liste in zones:
                    for ph in liste:
                        if exact(motif, ph): meilleur = (route, nom, 'exact'); break
                        if couvre(motif, ph) and (meilleur is None or meilleur[2] != 'exact'): meilleur = meilleur or (route, nom, 'couvert')
                    if meilleur and meilleur[2] == 'exact': break
                if meilleur and meilleur[2] == 'exact': break
                if meilleur is None:
                    tv = texte_visible(h)
                    if couvre(motif, tv): meilleur = (route, 'texte', 'couvert-texte')
            res['motifs'].append((motif, meilleur))
    for c in s['communes']:
        slug = plat(c).replace("'", '').replace(' ', '-')
        route = next((r for r in P if slug in r and r.count('/') == 2), None)
        if route is None:
            res['communes'].append((c, None)); continue
        h = P[route]
        res['communes'].append((c, dict(route=route, noindex='noindex' in h, sitemap=route in sitemap, lie=(f'href="{route}"' in accueil))))
    # sorties vers le club
    for route in ['/', '/mma/', '/transports/', '/contact/']:
        h = P.get(route, '')
        liens = sorted(set(re.findall(r'href="(https?://[^"]+)"', h)))
        hors = [l for l in liens if not any(d in l for d in ['tisseo', 'google', 'facebook', 'instagram', 'vercel', 'wikipedia', 'inlett', 'openstreetmap', 'w3.org', 'lio-occitanie', 'sncf', f"boxingcenter-{s['id']}"])]
        res['clubs'][route] = hors
    tout = ' '.join(P.values())
    res['contacts']['tel'] = sorted(set(re.findall(r'0\d(?: \d\d){4}', texte_visible(tout))))
    res['contacts']['mail'] = sorted(set(re.findall(r'[\w.+-]+@gmail\.com', tout)))
    res['alias'] = [r for r in P if re.search(r'^/(club|salle|boxe|mma|kick|k1|muay|grappling|sport|bus)-', r)]
    rapport[s['id']] = res

for sid, r in rapport.items():
    print(f"\n══════ {sid}")
    manques = [(m, b) for m, b in r['motifs'] if b is None]
    faibles = [(m, b) for m, b in r['motifs'] if b and b[2] == 'couvert-texte']
    print(f"  motifs : {len(r['motifs'])} · exacts {sum(1 for _, b in r['motifs'] if b and b[2]=='exact')} · couverts (titre/h1/h2/h3/desc) {sum(1 for _, b in r['motifs'] if b and b[2]=='couvert')} · texte seulement {len(faibles)} · MANQUANTS {len(manques)}")
    for m, b in r['motifs']:
        if b is None: print(f"    ✗ {m}")
    for m, b in faibles: print(f"    ~ {m} → {b[0]} (texte)")
    for c, d in r['communes']:
        print(f"  commune {c}: " + ('PAGE ABSENTE' if d is None else f"{d['route']} noindex={d['noindex']} sitemap={d['sitemap']} liée depuis accueil={d['lie']}"))
    for route, liens in r['clubs'].items():
        mauvais = [l for l in liens if not any(d in l for d in SITES[[x['id'] for x in SITES].index(sid)]['clubs'])]
        print(f"  sorties {route}: {len(liens)} lien(s) club ; hors domaine attendu : {mauvais if mauvais else 'aucun'}")
    print(f"  téléphones : {r['contacts']['tel']} · mails : {r['contacts']['mail']}")
    print(f"  alias : {len(r['alias'])} → {', '.join(r['alias'][:12])}{' …' if len(r['alias'])>12 else ''}")
