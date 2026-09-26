# -*- coding: utf-8 -*-
"""26/09 — Le plan du site répond 200 à l'apex aussi, plus jamais 308.

Search Console d'Eddy, 26/09 : « Impossible de récupérer le sitemap » sur
Colomiers, Cugnaux, Castelginest (et la boutique). Mesuré : les adresses
soumises étaient l'apex (sans www) ; l'apex répondait 308 → www ; la Search
Console refuse un plan du site qui redirige. À l'adresse www, les sept plans
sont sains (200, application/xml). Les trois sites à zéro dans Google sont
exactement ceux dont le plan n'a jamais pu être lu.

Correctif : la redirection apex → www épargne /sitemap.xml. Tout le reste du
site redirige comme avant ; le plan est servi tel quel aux deux adresses, ce
qu'un domaine vérifié dans la Search Console (sc-domain:) autorise.

Usage : python satellites_sitemap_apex.py [site …]   (défaut : les sept)
Rejouable : un fichier déjà patché est sauté."""
import io, json, sys

BASE = r"C:/Users/Mommy Jayce/Desktop/Boxing Center/Deployment/boxing-center-"
TOUS = ["colomiers", "muret", "cugnaux", "tournefeuille", "labege", "lunion", "castelginest"]
SITES = sys.argv[1:] or TOUS

for site in SITES:
    p = BASE + site + "/vercel.json"
    s = io.open(p, encoding="utf-8", newline="").read()
    apex = "boxingcenter-%s.fr" % site
    if "(?!sitemap" in s:
        print("déjà fait      ", site)
        continue
    # La règle de l'apex : source "/:path*" + has host = apex + destination www/:path*
    a = ('      "source": "/:path*",\n'
         '      "has": [\n'
         '        {\n'
         '          "type": "host",\n'
         '          "value": "%s"\n'
         '        }\n'
         '      ],\n'
         '      "destination": "https://www.%s/:path*",' % (apex, apex))
    b = ('      "source": "/((?!sitemap\\\\.xml$).*)",\n'
         '      "has": [\n'
         '        {\n'
         '          "type": "host",\n'
         '          "value": "%s"\n'
         '        }\n'
         '      ],\n'
         '      "destination": "https://www.%s/$1",' % (apex, apex))
    crlf = "\r\n" in s
    if crlf:
        a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    n = s.count(a)
    assert n == 1, (site, "règle apex introuvable ou multiple", n)
    s2 = s.replace(a, b)
    json.loads(s2)  # le JSON reste valide (les antislashs sont bien doublés)
    io.open(p, "w", encoding="utf-8", newline="").write(s2)
    print("patché         ", site)
