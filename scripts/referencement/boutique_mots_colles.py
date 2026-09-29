# -*- coding: utf-8 -*-
"""Boutique de Boxe, 29/09 — un blanc entre les éléments écrits bout à bout.

L'extrait Google de /materiel-mma/ lisait « Protège-dentsCasques de boxe
Protège-tibias », et le logo se lisait « BOUTIQUEDE BOXE. » sur chacune des
1 189 pages. En JSX, deux éléments frères sur deux lignes, ou produits par un
.map(), sont rendus sans aucun blanc : le CSS les espace à l'écran, le texte
que lit un moteur les colle.

Prouvé AVANT d'écrire ce code, dans un vrai navigateur, sur la production :
les mêmes blancs insérés entre les mêmes éléments (84 sur l'accueil, 195 sur
une catégorie, 91 sur une fiche produit), capture pleine page avant/après,
bureau et téléphone : hauteur inchangée, 0 pixel différent. Aucun texte ne
change ; seuls des blancs s'ajoutent.

Laissés volontairement de côté : l'illustration « 14 oz » (décorative), le
comparateur et le bandeau tournant de l'accueil (interactifs), et « modèle »
+ « s » qui DOIT se coller en « modèles ».

Rejouable : un fichier déjà traité est sauté."""
import io, re, sys

R = r"C:/Users/Mommy Jayce/Desktop/Boxing Center/Deployment/boutique-de-boxe/site/"

HELPER = """import { Children, type ReactNode } from 'react';

/* Un blanc entre des éléments frères écrits bout à bout (29/09).
   En JSX, deux éléments sur deux lignes, ou produits par un .map(), sont
   rendus sans aucun blanc. À l'écran le CSS les espace ; le texte que lit un
   moteur les colle : l'extrait Google de /materiel-mma/ disait « Protège-dents
   Casques de boxe » en un seul mot. Un blanc seul entre deux enfants d'une
   boîte flex ou grid n'est pas rendu, et entre deux blocs il est absorbé :
   rien ne bouge à l'écran (prouvé : 0 pixel changé, bureau et téléphone). */
export function spaced(nodes: ReactNode): ReactNode[] {
  const out: ReactNode[] = [];
  Children.toArray(nodes).forEach((n, i) => {
    if (i) out.push(' ');
    out.push(n);
  });
  return out;
}
"""

SP = "{' '}"


def lire(f):
    return io.open(R + f, encoding="utf-8", newline="").read()


def ecrire(f, s):
    io.open(R + f, "w", encoding="utf-8", newline="").write(s)


def remplace(s, a, b, n, quoi):
    # Certains fichiers mêlent CRLF et LF d'un bloc à l'autre : on essaie le
    # motif tel quel (LF), puis en CRLF, et on garde la forme qui correspond.
    for aa, bb in ((a, b), (a.replace("\n", "\r\n"), b.replace("\n", "\r\n"))):
        if s.count(aa) == n:
            return s.replace(aa, bb)
    raise AssertionError((quoi, "attendu %d, trouvé %d (LF) / %d (CRLF)" % (n, s.count(a), s.count(a.replace("\n", "\r\n")))))


def importe(s, ligne):
    """Pose l'import juste après le dernier import de tête. Ligne par ligne,
    chacune avec SA fin de ligne : certains fichiers de la boutique mêlent CRLF
    et LF, et un découpage sur une seule fin de ligne a posé l'import au milieu
    du code (29/09, app/marques/[brand]/page.tsx)."""
    if ligne.strip() in s:
        return s
    L = s.splitlines(keepends=True)
    imps = [i for i, l in enumerate(L[:80]) if l.startswith("import ")]
    assert imps, "aucun import de tête"
    k = imps[-1]
    # un import sur plusieurs lignes : aller jusqu'à sa ligne « from … ; »
    while not L[k].rstrip().endswith(";"):
        k += 1
    fin = L[k][len(L[k].rstrip("\r\n")):] or "\n"
    L.insert(k + 1, ligne + fin)
    return "".join(L)


# ── 0. l'aide partagée ──────────────────────────────────────────────────────
try:
    lire("lib/spaced.ts")
    print("déjà là         lib/spaced.ts")
except FileNotFoundError:
    ecrire("lib/spaced.ts", HELPER)
    print("créé            lib/spaced.ts")

# ── 1. shop-shell.tsx : logo, bandeau, navigation, pied de page ────────────
f = "components/shop-shell.tsx"
s = lire(f)
if "spaced(" not in s:
    s = remplace(s, "BOUTIQUE<span>DE BOXE.</span>", "BOUTIQUE" + SP + "<span>DE BOXE.</span>", 1, "logo")
    s = remplace(s, "COMMANDE D’ESSAI SANS PAIEMENT\n", "COMMANDE D’ESSAI SANS PAIEMENT" + SP + "\n", 1, "bandeau")
    for lien in ['<a href="/materiel-boxe/">Boxe anglaise</a>\n          <a href="/materiel-mma/">MMA</a>',
                 ]:
        pass
    s = remplace(s,
        """          <a href="/materiel-boxe/">Boxe anglaise</a>
          <a href="/materiel-mma/">MMA</a>
          <a href="/boutique-arts-martiaux/">Arts martiaux</a>
          <a href="/guides/" onClick={() => setMenu(false)}>""",
        """          <a href="/materiel-boxe/">Boxe anglaise</a>{' '}
          <a href="/materiel-mma/">MMA</a>{' '}
          <a href="/boutique-arts-martiaux/">Arts martiaux</a>{' '}
          <a href="/guides/" onClick={() => setMenu(false)}>""", 1, "nav principale")
    # raccourcis du pied : numéro | contenu, titre | précision, et entre les liens
    s = remplace(s, """            </span>
            <span>
              <strong>""", """            </span>{' '}
            <span>
              <strong>""", 3, "raccourcis : numéro/contenu")
    s = re.sub(r"(<strong>[^<]+</strong>)(\r?\n\s+<small>)", lambda m: m.group(1) + SP + m.group(2), s)
    s = remplace(s, """          </a>
          <a className="footer-route" href=""", """          </a>{' '}
          <a className="footer-route" href=""", 2, "raccourcis : entre liens")
    # grille du pied : la liste des familles, puis les liens écrits un par un
    s = remplace(s, """          {categories
            .filter((c) =>""", """          {spaced(categories
            .filter((c) =>""", 1, "familles : ouverture")
    s = remplace(s, """                {c.name}
              </a>
            ))}
        </nav>""", """                {c.name}
              </a>
            )))}
        </nav>""", 1, "familles : fermeture")
    debut = s.index('<nav aria-labelledby="footer-practice">')
    fin = s.index('<details className="footer-directory">')
    bloc = s[debut:fin]
    bloc2 = re.sub(r"(</a>)(\r?\n\s+<a )", lambda m: m.group(1) + SP + m.group(2), bloc)
    assert bloc2.count(SP) - bloc.count(SP) == 11, ("pied : liens un par un", bloc2.count(SP) - bloc.count(SP))
    s = s[:debut] + bloc2 + s[fin:]
    # recherches par équipement
    s = remplace(s, "{QUERY_MAP.map((q) => (", "{spaced(QUERY_MAP.map((q) => (", 1, "recherches : ouverture")
    s = remplace(s, """              {q.query}
            </a>
          ))}""", """              {q.query}
            </a>
          )))}""", 1, "recherches : fermeture")
    # bas de page
    s = remplace(s, """        <MotionControl />
        <span>© {new Date().getFullYear()} Boutique de Boxe</span>
        <nav aria-label="Informations légales">
          <a href="/mentions-legales/">Mentions légales</a>
          <a href="/conditions-generales-de-vente/">CGV</a>
          <a href="/confidentialite/">Confidentialité</a>
          <CookiesButton />""", """        <MotionControl />{' '}
        <span>© {new Date().getFullYear()} Boutique de Boxe</span>{' '}
        <nav aria-label="Informations légales">
          <a href="/mentions-legales/">Mentions légales</a>{' '}
          <a href="/conditions-generales-de-vente/">CGV</a>{' '}
          <a href="/confidentialite/">Confidentialité</a>{' '}
          <CookiesButton />""", 1, "bas de page")
    s = importe(s, "import { spaced } from '@/lib/spaced';")
    ecrire(f, s)
    print("patché          " + f)
else:
    print("déjà fait       " + f)

# ── 2. shop-interactions.tsx : carte produit, catalogue, fiche ──────────────
f = "components/shop-interactions.tsx"
s = lire(f)
if "spaced(" not in s:
    s = remplace(s, """        </span>
        <span className="product-status">""", """        </span>{' '}
        <span className="product-status">""", 1, "carte : numéro/famille")
    s = remplace(s, "        <span>{p.brand}</span>\n", "        <span>{p.brand}</span>{' '}\n", 1, "carte : marque/tailles")
    s = remplace(s, """        </strong>
        <span>prix prévu</span>""", """        </strong>{' '}
        <span>prix prévu</span>""", 1, "carte : prix")
    s = remplace(s, """        </span>
        <span>EN VENTE BIENTÔT</span>""", """        </span>{' '}
        <span>EN VENTE BIENTÔT</span>""", 1, "compteur")
    s = remplace(s, "{pageWindow(page, Math.ceil(count / 36)).map(", "{spaced(pageWindow(page, Math.ceil(count / 36)).map(", 1, "pagination : ouverture")
    s = remplace(s, """                  </span>
                ),
              )}
            </nav>""", """                  </span>
                ),
              ))}
            </nav>""", 1, "pagination : fermeture")
    s = remplace(s, """            Caractéristiques détaillées
          </span>
          <span>""", """            Caractéristiques détaillées
          </span>{' '}
          <span>""", 1, "assurances")
    s = importe(s, "import { spaced } from '@/lib/spaced';")
    ecrire(f, s)
    print("patché          " + f)
else:
    print("déjà fait       " + f)

# ── 3. menus de sous-familles (trois gabarits) ──────────────────────────────
for f, a, b, a2, b2 in [
    ("components/facet-page.tsx",
     "        {siblings.slice(0, 12).map((x) => (", "        {spaced(siblings.slice(0, 12).map((x) => (",
     "          <a key={x.path} href={x.path}>{x.name}</a>\n        ))}", "          <a key={x.path} href={x.path}>{x.name}</a>\n        )))}"),
    ("app/[...slug]/page.tsx",
     "          {siblings.map((x) => (", "          {spaced(siblings.map((x) => (",
     "            <a key={x.slug} href={'/' + x.slug + '/'}>{x.name}</a>\n          ))}", "            <a key={x.slug} href={'/' + x.slug + '/'}>{x.name}</a>\n          )))}"),
    ("app/marques/[brand]/page.tsx",
     "          {b.families.map((f) => {", "          {spaced(b.families.map((f) => {",
     "            ) : null;\n          })}", "            ) : null;\n          }))}"),
]:
    s = lire(f)
    if "spaced(" in s:
        print("déjà fait       " + f)
        continue
    s = remplace(s, a, b, 1, f + " ouverture")
    s = remplace(s, a2, b2, 1, f + " fermeture")
    if f == "components/facet-page.tsx":
        # le lien vers la famille, écrit à la main avant la liste
        s = re.sub(r"(<nav className=\"subfamily-links\"[^>]*>\r?\n\s+<a href=\{f\.parent\.path\}>.*?</a>)", lambda m: m.group(1) + SP, s, count=1, flags=re.S)
    if f == "app/[...slug]/page.tsx":
        s = remplace(s, "{parent && <a href={'/' + parent.slug + '/'}>Toute la famille : {parent.name}</a>}",
                     "{parent && <><a href={'/' + parent.slug + '/'}>Toute la famille : {parent.name}</a>{' '}</>}", 1, "famille parente")
        # fiche produit : l'étiquette et sa valeur
        for lab in ["Discipline", "Niveau conseillé", "Famille"]:
            s = remplace(s, "<div><span>%s</span>{" % lab if lab != "Famille" else "<div><span>Famille</span><a",
                         ("<div><span>%s</span>{' '}{" % lab) if lab != "Famille" else "<div><span>Famille</span>{' '}<a", 1, "faits : " + lab)
        s = remplace(s, "                  <span>Marque</span>\n", "                  <span>Marque</span>{' '}\n", 1, "faits : marque")
        s = remplace(s, "<div><span>{p.referenceLabel || 'Référence'}</span>{p.reference}</div>",
                     "<div><span>{p.referenceLabel || 'Référence'}</span>{' '}{p.reference}</div>", 1, "faits : référence")
    s = importe(s, "import { spaced } from '@/lib/spaced';")
    ecrire(f, s)
    print("patché          " + f)

# ── 4. accueil : la liste des familles et l'index par discipline ────────────
f = "components/home.tsx"
s = lire(f)
if "spaced(" not in s:
    i = s.index('<div className="equipment-rows">')
    j = s.index("</div>", s.index("})}", i))
    bloc = s[i:j]
    ouv = re.search(r"\{(\s*)([A-Za-z_][\w.]*[\s\S]*?\.map\(\(c, i\) => \{)", bloc)
    assert ouv, "familles accueil : ouverture introuvable"
    bloc2 = bloc[:ouv.start()] + "{spaced(" + bloc[ouv.start() + 1:]
    k = bloc2.rindex("})}")
    bloc2 = bloc2[:k] + "}))}" + bloc2[k + 3:]
    s = s[:i] + bloc2 + s[j:]
    i = s.index('<nav className="practice-index"')
    j = s.index("</nav>", i)
    bloc = s[i:j]
    bloc2 = re.sub(r"(</span>|</a>)(\r?\n\s+<a )", lambda m: m.group(1) + SP + m.group(2), bloc)
    assert bloc2 != bloc, "index par discipline : rien trouvé"
    s = s[:i] + bloc2 + s[j:]
    s = importe(s, "import { spaced } from '@/lib/spaced';")
    ecrire(f, s)
    print("patché          " + f)
else:
    print("déjà fait       " + f)

# ── 5. les deux autres menus du même genre (manqués au premier passage :
#       le script ne traitait que la première occurrence par fichier) ────────
for f, a, b in [
    ("app/marques/[brand]/page.tsx",
     """          <a href="/marques/">Toutes les marques</a>
          {others.map((x) => (
            <a key={x.slug} href={'/marques/' + x.slug + '/'}>
              {x.name}
            </a>
          ))}""",
     """          <a href="/marques/">Toutes les marques</a>{' '}
          {spaced(others.map((x) => (
            <a key={x.slug} href={'/marques/' + x.slug + '/'}>
              {x.name}
            </a>
          )))}"""),
    ("app/[...slug]/page.tsx",
     """              {subs.map((x) => (
                <a key={x.slug} href={'/' + x.slug + '/'}>{x.name}</a>
              ))}""",
     """              {spaced(subs.map((x) => (
                <a key={x.slug} href={'/' + x.slug + '/'}>{x.name}</a>
              )))}"""),
]:
    s2 = lire(f)
    # la PREMIÈRE ligne du remplacement n'existe qu'une fois patché (la 2e
    # existait déjà : faux « déjà fait » sur le menu Sous-familles, 29/09)
    if b.split("\n")[0].strip() in s2:
        print("déjà fait       " + f + " (2e menu)")
        continue
    s2 = remplace(s2, a, b, 1, f + " (2e menu)")
    ecrire(f, s2)
    print("patché          " + f + " (2e menu)")
