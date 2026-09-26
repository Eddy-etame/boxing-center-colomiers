# -*- coding: utf-8 -*-
"""26/09 — Le plan du site répond 200 à l'apex aussi, plus jamais 308.

Search Console d'Eddy, 26/09 : « Impossible de récupérer le sitemap » sur
Colomiers, Cugnaux, Castelginest (et la boutique). Mesuré : les adresses
soumises étaient l'apex (sans www) ; l'apex répondait 308 → www ; la Search
Console refuse un plan du site qui redirige. À l'adresse www, les sept plans
sont sains (200, application/xml). Les trois sites à zéro dans Google sont
exactement ceux dont le plan n'a jamais pu être lu.

Deux correctifs dans vercel.json :
1. La redirection apex → www épargne /sitemap.xml : le plan est servi tel quel
   aux deux adresses, ce qu'un domaine vérifié dans la Search Console
   (sc-domain:) autorise. Tout le reste redirige comme avant.
2. Trouvé en passant : sur cinq sites (Cugnaux, Tournefeuille, Labège,
   L'Union, Castelginest), la règle nommait l'hôte de MURET — un reste de
   copier-coller. Règle morte : leur redirection vivante vient du tableau de
   bord Vercel. On la remet au bon hôte, pour qu'elle tienne le jour où le
   tableau de bord change.

Usage : python satellites_sitemap_apex.py [site …]   (défaut : les sept)
Rejouable : un fichier déjà patché est sauté."""
import io, json, re, sys

BASE = r"C:/Users/Mommy Jayce/Desktop/Boxing Center/Deployment/boxing-center-"
TOUS = ["colomiers", "muret", "cugnaux", "tournefeuille", "labege", "lunion", "castelginest"]
SITES = sys.argv[1:] or TOUS

# La règle apex, telle qu'elle est écrite sur les sept sites (hôte variable).
REGLE = re.compile(
    r'(      "source": ")/:path\*(",\n'
    r'      "has": \[\n'
    r'        \{\n'
    r'          "type": "host",\n'
    r'          "value": ")boxingcenter-([a-z]+)\.fr("\n'
    r'        \}\n'
    r'      \],\n'
    r'      "destination": "https://www\.)boxingcenter-([a-z]+)\.fr/:path\*(",)'
)

for site in SITES:
    p = BASE + site + "/vercel.json"
    s = io.open(p, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    t = s.replace("\r\n", "\n") if crlf else s
    if "(?!sitemap" in t:
        print("déjà fait      ", site)
        continue
    m = REGLE.search(t)
    assert m, (site, "règle apex introuvable")
    assert len(REGLE.findall(t)) == 1, (site, "plusieurs règles apex")
    mauvais = m.group(3) != site or m.group(5) != site
    neuf = (m.group(1) + "/((?!sitemap\\\\.xml$).*)" + m.group(2)
            + "boxingcenter-%s.fr" % site + m.group(4)
            + "boxingcenter-%s.fr/$1" % site + m.group(6))
    t2 = t[:m.start()] + neuf + t[m.end():]
    json.loads(t2)  # le JSON reste valide, antislashs compris
    io.open(p, "w", encoding="utf-8", newline="").write(t2.replace("\n", "\r\n") if crlf else t2)
    print("patché         ", site, "· hôte corrigé (nommait %s)" % m.group(3) if mauvais else "")
