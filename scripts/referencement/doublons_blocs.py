# -*- coding: utf-8 -*-
"""Quels blocs d'une page A sont repris d'une page B ? Bloc par bloc (titres,
paragraphes, items), la part de ses séquences de 5 mots qu'on retrouve dans B,
une fois le nom des villes neutralisé. Usage :
  python doublons_blocs.py <urlA> <urlB> [seuil=0.5]"""
import re, sys, html, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (audit interne Boxing Center)"}
VILLES = ["colomiers", "muret", "cugnaux", "tournefeuille", "labège", "labege", "l’union", "l'union", "castelginest",
          "muretains", "cugnalais", "castelginestois", "unionais", "columérins", "tournefeuillais", "labégeois"]


def page(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read().decode("utf-8", "ignore")


def blocs(h):
    h = re.sub(r"(?is)<(script|style|noscript|svg|header|nav|footer)\b.*?</\1>", " ", h)
    out = []
    for m in re.finditer(r"(?is)<(h1|h2|h3|p|li|dt|dd|summary|figcaption|blockquote)\b[^>]*>(.*?)</\1>", h):
        t = html.unescape(re.sub(r"(?s)<[^>]+>", " ", m.group(2)))
        t = re.sub(r"\s+", " ", t).strip()
        if len(t.split()) >= 8:
            out.append((m.group(1).lower(), t))
    return out


def neutre(t):
    t = t.lower()
    for v in VILLES:
        t = t.replace(v, "§")
    return re.findall(r"[a-zà-ÿ0-9§]+", t)


def shingles(mots, n=5):
    return {" ".join(mots[i:i + n]) for i in range(len(mots) - n + 1)}


a, b = sys.argv[1], sys.argv[2]
seuil = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
A, B = blocs(page(a)), blocs(page(b))
SB = set()
for _, t in B:
    SB |= shingles(neutre(t))
tot = dup = 0
print(f"A = {a}\nB = {b}\n")
for tag, t in A:
    s = shingles(neutre(t))
    if not s:
        continue
    part = len(s & SB) / len(s)
    mots = len(t.split())
    tot += mots
    if part >= seuil:
        dup += mots
        print(f"[{part:4.0%}] <{tag}> {mots:3d} mots · {t[:150]}")
print(f"\n{dup} mots sur {tot} dans des blocs repris à ≥ {seuil:.0%}  →  {dup / max(tot, 1):.0%} de la page")
