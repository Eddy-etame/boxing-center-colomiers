# -*- coding: utf-8 -*-
"""INVENTAIRE PAGE PAR PAGE — pourquoi telle page n'est pas indexée.

Pour chaque site : on part de l'accueil, on suit tous les liens internes, et
pour chaque page trouvée on relève ce qui décide de son indexation :

  statut · robots (meta + en-tête) · canonique (vers elle-même ?) · mots ·
  dans le plan du site ? · combien de pages du site la lient (orpheline ?) ·
  profondeur de clic depuis l'accueil

Une page n'entre pas dans Google pour une de ces raisons, dans l'ordre :
noindex → canonique ailleurs → orpheline (aucun lien interne) → trop profonde
→ trop pauvre → doublon d'une autre page. Ce script donne les cinq premières ;
les doublons sont l'affaire de doublons_blocs.py.

Usage :  python inventaire_pages.py <hôte> [<hôte> …]      (sans https://)
Sortie : un tableau par site + un fichier TSV par site dans le dossier courant.
"""
import sys, re, html, time, json
import urllib.request, urllib.error
from collections import deque

UA = {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
MAX = 200


def get(u):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30)
        return r.getcode(), dict(r.headers), r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), ""
    except Exception as e:
        return 0, {}, str(e)[:80]


def texte(h):
    h = re.sub(r"(?is)<(script|style|noscript|svg)\b.*?</\1>", " ", h)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"(?s)<[^>]+>", " ", h))).strip()


def liens(h, base, hote):
    """Les liens internes du corps de page, séparés de ceux de la barre et du pied."""
    corps = h
    for zone in ("header", "footer", "nav"):
        corps = re.sub(r"(?is)<%s\b.*?</%s>" % (zone, zone), " ", corps)
    out = {}
    for src, marque in ((corps, "corps"), (h, "toutes")):
        s = set()
        for m in re.finditer(r'(?i)<a\b[^>]*href="([^"#?]+)', src):
            u = m.group(1)
            if u.startswith("/"):
                u = "https://" + hote + u
            if not u.startswith("https://" + hote):
                continue
            if re.search(r"\.(jpg|png|webp|svg|xml|txt|pdf|ico|json)$", u, re.I):
                continue
            s.add(u if u.endswith("/") else u + "/")
        out[marque] = s
    return out


def inventaire(hote):
    racine = "https://" + hote + "/"
    _, _, sm = get(racine + "sitemap.xml")
    plan = {u if u.endswith("/") else u + "/" for u in re.findall(r"<loc>([^<]+)</loc>", sm)}

    vus, file, entrants, entrants_corps, prof = {}, deque([(racine, 0)]), {}, {}, {}
    while file and len(vus) < MAX:
        u, d = file.popleft()
        if u in vus:
            continue
        code, ent, h = get(u)
        prof[u] = d
        xr = ent.get("X-Robots-Tag", "")
        meta = re.search(r'(?i)<meta name="robots" content="([^"]*)"', h)
        can = re.search(r'(?i)<link rel="canonical" href="([^"]*)"', h)
        titre = re.search(r"(?is)<title>(.*?)</title>", h)
        vus[u] = {
            "code": code,
            "xrobots": xr,
            "robots": meta.group(1) if meta else "",
            "canonique": (can.group(1) if can else ""),
            "mots": len(texte(h).split()),
            "titre": html.unescape(titre.group(1)).strip() if titre else "",
            "plan": u in plan,
            "prof": d,
        }
        if code == 200:
            l = liens(h, u, hote)
            for v in l["toutes"]:
                entrants[v] = entrants.get(v, 0) + (1 if v != u else 0)
                if v not in vus:
                    file.append((v, d + 1))
            for v in l["corps"]:
                if v != u:
                    entrants_corps[v] = entrants_corps.get(v, 0) + 1
        time.sleep(0.05)

    for u, r in vus.items():
        r["entrants"] = entrants.get(u, 0)
        r["entrants_corps"] = entrants_corps.get(u, 0)
        r["canonique_ailleurs"] = bool(r["canonique"]) and r["canonique"].rstrip("/") + "/" != u
        bloque = "noindex" in (r["robots"] + r["xrobots"]).lower()
        r["indexable"] = r["code"] == 200 and not bloque and not r["canonique_ailleurs"]
        r["pourquoi"] = (
            "statut %s" % r["code"] if r["code"] != 200
            else "noindex" if bloque
            else "canonique → %s" % r["canonique"] if r["canonique_ailleurs"]
            else "ORPHELINE (aucun lien interne)" if r["entrants"] == 0 and u != racine
            else "hors plan du site" if not r["plan"]
            else "pauvre (%d mots)" % r["mots"] if r["mots"] < 300
            else ""
        )
    orphelines_plan = plan - set(vus)
    return vus, plan, orphelines_plan


for hote in sys.argv[1:]:
    vus, plan, hors_crawl = inventaire(hote)
    print("\n" + "=" * 100)
    print("%s — %d pages atteintes en suivant les liens · %d dans le plan du site" % (hote, len(vus), len(plan)))
    print("-" * 100)
    print("%-42s %4s %5s %4s %4s %4s %5s  %s" % ("chemin", "code", "mots", "plan", "ent.", "txt", "prof", "pourquoi pas indexable / à surveiller"))
    for u in sorted(vus):
        r = vus[u]
        print("%-42s %4s %5d %4s %4d %4d %5d  %s" % (
            u.replace("https://" + hote, "") or "/", r["code"], r["mots"],
            "oui" if r["plan"] else "NON", r["entrants"], r["entrants_corps"], r["prof"], r["pourquoi"]))
    if hors_crawl:
        print("\n  DANS LE PLAN MAIS ATTEINTE PAR AUCUN LIEN (orpheline vraie) :")
        for u in sorted(hors_crawl):
            print("   ", u)
    ok = [u for u, r in vus.items() if r["indexable"]]
    print("\n  indexables : %d / %d   ·   bloquées : %s" % (
        len(ok), len(vus), ", ".join(sorted(u.replace("https://" + hote, "") for u, r in vus.items() if not r["indexable"])) or "aucune"))
    with open("inventaire-%s.tsv" % hote.replace("www.boxingcenter-", "").replace(".fr", ""), "w", encoding="utf-8") as f:
        f.write("url\tcode\tmots\tplan\tentrants\tentrants_corps\tprof\trobots\tcanonique\tindexable\tpourquoi\ttitre\n")
        for u in sorted(vus):
            r = vus[u]
            f.write("\t".join(str(x) for x in [u, r["code"], r["mots"], r["plan"], r["entrants"], r["entrants_corps"],
                                               r["prof"], r["robots"] + "|" + r["xrobots"], r["canonique"],
                                               r["indexable"], r["pourquoi"], r["titre"]]) + "\n")
