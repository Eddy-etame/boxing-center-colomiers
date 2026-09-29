# -*- coding: utf-8 -*-
"""26/09 — Blagnac : les pages légales entrent dans Google, et le build le garde.

Règle d'Eddy (19/09) : « when websites actually start serving on the official
paid domains, they should go straight to index, not no index anymore. » Les
sept satellites l'appliquent depuis le 19/09. Blagnac non : ses mentions
légales et sa confidentialité étaient en `noindex,follow`, hors du plan du
site, et scripts/audit-build.mjs FAISAIT ÉCHOUER le build si quelqu'un les
rouvrait — le contrôle défendait l'inverse de la règle.

Vérifié avant d'ouvrir : les deux pages sont réelles (1 321 et 1 023 mots,
éditeur nommé, aucun texte de brouillon — les deux « placeholder » trouvés
sont des sélecteurs CSS).

Ce qui change :
- BaseLayout.astro : le robots ne dépend plus de LOW_VALUE_PAGES ; seule la
  prop `noindex` (la 404) garde une page hors de l'index.
- sitemap.xml.ts : les pages légales ne sont plus filtrées du plan.
- audit-build.mjs : la branche qui exigeait `noindex,follow` pour les pages
  légales disparaît — elles passent par le contrôle commun (index + canonique
  exacte) ; et un contrôle neuf exige que chaque page légale soit dans le plan.
- LOW_VALUE_PAGES garde son rôle sémantique dans schema.ts (« page qui parle de
  l'éditeur, pas de la boxe »), qui n'a rien à voir avec l'indexation.

Rejouable."""
import io, sys

R = r"C:/Users/Mommy Jayce/Desktop/Boxing Center/Deployment/club-de-boxe-blagnac/"


def patch(f, pairs, marque):
    p = R + f
    s = io.open(p, encoding="utf-8", newline="").read()
    if marque in s:
        print("déjà fait     ", f)
        return
    crlf = "\r\n" in s
    for a, b in pairs:
        if crlf:
            a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
        n = s.count(a)
        assert n == 1, (f, a[:70], n)
        s = s.replace(a, b)
    io.open(p, "w", encoding="utf-8", newline="").write(s)
    print("patché        ", f)


patch("src/layouts/BaseLayout.astro", [
    ("""/* Three answers: locked/404 → noindex,nofollow; legal pages → noindex,follow
   (reachable, followed, not indexed); everything else → index. */
const lowValue = (LOW_VALUE_PAGES as readonly string[]).includes(pathname);
const robots = !SITE.indexable
  ? 'noindex,nofollow,noarchive,nosnippet'
  : noindex || lowValue
    ? 'noindex,follow'""",
     """/* Deux réponses (26/09) : site verrouillé → noindex,nofollow ; la 404 (prop
   `noindex`) → noindex,follow ; TOUT le reste → index, pages légales comprises.
   Règle d'Eddy : en production, une page de contenu se range dans Google. */
const robots = !SITE.indexable
  ? 'noindex,nofollow,noarchive,nosnippet'
  : noindex
    ? 'noindex,follow'"""),
], "Règle d'Eddy : en production")

patch("src/pages/sitemap.xml.ts", [
    ("""    ? PUBLIC_PAGES.filter((path) => !(LOW_VALUE_PAGES as readonly string[]).includes(path)).map((path) => {""",
     """    /* Toutes les pages publiques, pages légales comprises (26/09, règle d'Eddy). */
    ? PUBLIC_PAGES.map((path) => {"""),
], "pages légales comprises (26/09")

patch("scripts/audit-build.mjs", [
    ("""    } else if (LOW_VALUE.includes(relative(dist, file).split('\\\\').join('/'))) {
      assert(/name="robots"\\s+content="noindex,follow"/i.test(html), `${relative(dist, file)}: legal page must be noindex,follow.`);
      assert(!sitemap.includes('/' + relative(dist, file).split('\\\\').join('/').replace('index.html', '') + '<'), `${relative(dist, file)}: legal page must stay out of the sitemap.`);
    } else {""",
     """    } else {
      /* 26/09 — règle d'Eddy : en production, une page de contenu se range dans
         Google. Les pages légales passent par le contrôle commun (index +
         canonique exacte) et doivent figurer dans le plan du site. */
      if (LOW_VALUE.includes(relative(dist, file).split('\\\\').join('/'))) {
        assert(sitemap.includes('/' + relative(dist, file).split('\\\\').join('/').replace('index.html', '') + '<'), `${relative(dist, file)}: legal page must be in the sitemap (production pages are indexed).`);
      }"""),
], "règle d'Eddy : en production")

# LOW_VALUE_PAGES n'est plus importé par le gabarit ni par le plan : on retire
# l'import devenu mort pour qu'astro check reste propre.
for f, a, b in [
    ("src/layouts/BaseLayout.astro", "import { SITE, LOW_VALUE_PAGES, absoluteUrl } from '@/data/site';",
     "import { SITE, absoluteUrl } from '@/data/site';"),
]:
    p = R + f
    s = io.open(p, encoding="utf-8", newline="").read()
    if a in s and "LOW_VALUE_PAGES" not in s.replace(a, ""):
        io.open(p, "w", encoding="utf-8", newline="").write(s.replace(a, b))
        print("import nettoyé", f)

p = R + "src/pages/sitemap.xml.ts"
s = io.open(p, encoding="utf-8", newline="").read()
reste = s.count("LOW_VALUE_PAGES")
imp = [l for l in s.splitlines() if "import" in l and "LOW_VALUE_PAGES" in l]
if reste == 1 and imp:
    l = imp[0]
    neuf = l.replace("LOW_VALUE_PAGES, ", "").replace(", LOW_VALUE_PAGES", "")
    io.open(p, "w", encoding="utf-8", newline="").write(s.replace(l, neuf))
    print("import nettoyé src/pages/sitemap.xml.ts")
