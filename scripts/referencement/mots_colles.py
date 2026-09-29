# -*- coding: utf-8 -*-
"""Mots collés : ce qu'un moteur lit quand deux éléments en ligne se touchent.

Le 29/09, l'extrait Google de /materiel-mma/ sur boutique-de-boxe.com disait
« Protège-dentsCasques de boxeProtège-tibias » : les liens d'un menu écrits
bout à bout, sans blanc. À l'écran, le CSS les sépare ; dans le texte que lit
un moteur, ils se collent.

Ce script lit une page comme un moteur : les éléments de bloc (div, li, p,
h1…) séparent le texte ; les éléments en ligne (a, span, strong…) non. Il
signale chaque jonction où deux mots se touchent sans blanc, avec le conteneur
le plus proche qui porte une classe — c'est lui qu'il faut corriger.

Usage : python mots_colles.py <url> [<url> …]"""
import sys, urllib.request
from html.parser import HTMLParser

BLOCS = set("""address article aside blockquote body br dd details dialog div dl dt fieldset
figcaption figure footer form h1 h2 h3 h4 h5 h6 header hr html li main nav ol p pre section
summary table tbody td tfoot th thead tr ul option select label button""".split())
IGNORE = {"script", "style", "svg", "noscript", "template", "head", "title"}
VIDES = {"br", "hr", "img", "input", "meta", "link", "source", "wbr", "area", "col", "embed", "track"}


class Lecteur(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pile = []          # (tag, classe)
        self.ignore = 0
        self.dernier = ""       # dernier caractère de texte émis
        self.coupure = True     # un bloc vient de s'ouvrir/fermer : pas de collage possible
        self.jonctions = {}

    def conteneur(self):
        for tag, cls in reversed(self.pile):
            if cls:
                return "%s.%s" % (tag, cls.split()[0])
        return "?"

    def handle_starttag(self, tag, attrs):
        if tag in IGNORE:
            self.ignore += 1
        if tag in BLOCS:
            self.coupure = True
        if tag not in VIDES:
            self.pile.append((tag, dict(attrs).get("class", "")))

    def handle_endtag(self, tag):
        if tag in IGNORE:
            self.ignore = max(0, self.ignore - 1)
        if tag in BLOCS:
            self.coupure = True
        for i in range(len(self.pile) - 1, -1, -1):
            if self.pile[i][0] == tag:
                del self.pile[i:]
                break

    def handle_data(self, d):
        if self.ignore or not d:
            return
        if d.strip() == "":
            self.dernier = " "
            return
        premier = d[0]
        if (not self.coupure and self.dernier and not self.dernier.isspace()
                and self.dernier.isalnum() and premier.isalnum()):
            c = self.conteneur()
            self.jonctions.setdefault(c, []).append(d.strip()[:24])
        self.dernier = d[-1]
        self.coupure = False


UA = {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
total = 0
for url in sys.argv[1:]:
    h = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read().decode("utf-8", "ignore")
    L = Lecteur()
    L.feed(h)
    n = sum(len(v) for v in L.jonctions.values())
    total += n
    print("%s — %d jonction(s) collée(s)" % (url, n))
    for c, ex in sorted(L.jonctions.items(), key=lambda x: -len(x[1])):
        print("   %4d  %-40s ex. « …%s »" % (len(ex), c, ex[0]))
print("\ntotal : %d" % total)
