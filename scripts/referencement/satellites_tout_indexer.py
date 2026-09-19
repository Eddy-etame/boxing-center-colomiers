# -*- coding: utf-8 -*-
"""19/09 — TOUTES LES PAGES DOIVENT ENTRER DANS GOOGLE (Eddy).

Trois défauts mesurés le 19/09, corrigés ici sur les 7 sites de proximité :

1. 42 pages en `index: false` depuis le 12/09 (premiere-seance, ta-seance,
   nos-clubs, contact, mentions-legales, confidentialite). Elles sortaient du
   plan du site ET recevaient `noindex`. Eddy, 19/09 : « there should be a rule
   when we get into production […] they should go straight to index, not no
   index anymore. » On les ouvre. Le texte ne change pas.
   EXCEPTION, et c'est la seule : `merci` (confirmation d'envoi du formulaire)
   et `introuvable` (la page 404). Indexer une 404 est un défaut, pas un gain.

2. Les pages de commune (/saint-jean/, /fonsorbes/, /seysses/…) reçoivent 2 à 4
   liens internes quand toute autre page en reçoit 13 à 16. `ROUTES_COMMUNES`
   existait dans le registre et n'était lue NULLE PART. Elles entrent dans le
   pied de page : présentes sur chaque page du site, donc au niveau des
   disciplines (choix d'Eddy).

3. Le pied de page listait en TEXTE MORT des communes qui ont leur propre page
   (Saint-Jean sur L'Union, Castanet et Saint-Orens sur Labège, Launaguet et
   Saint-Alban sur Castelginest…). Elles deviennent des liens.

Rejouable : chaque fichier déjà traité est sauté."""
import io, re

BASE = r"C:/Users/Mommy Jayce/Desktop/Boxing Center/Deployment/boxing-center-"
SITES = ["colomiers", "muret", "cugnaux", "tournefeuille", "labege", "lunion", "castelginest"]
# Les seules pages qui restent hors de Google, et pourquoi.
HORS = {"merci", "introuvable"}


def lire(p):
    return io.open(p, encoding="utf-8", newline="").read()


def ecrire(p, s):
    io.open(p, "w", encoding="utf-8", newline="").write(s)


def une(s, a, b, quoi):
    if "\r\n" in s:
        a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    n = s.count(a)
    assert n == 1, (quoi, n)
    return s.replace(a, b)


for site in SITES:
    R = BASE + site + "/"

    # ── 1. le registre : on ouvre tout sauf merci et introuvable ────────────
    p = R + "src/data/routes.ts"
    s = lire(p)
    # chaque entrée de ROUTES est un bloc « { … }, » ; on repère l'id du bloc
    # qui porte le index: false, et on l'ouvre si ce n'est pas merci/introuvable.
    ouvertes = []
    def ouvre(m):
        bloc = m.group(0)
        ident = re.search(r"id: '([^']+)'", bloc)
        if not ident or ident.group(1) in HORS or "index: false" not in bloc:
            return bloc
        ouvertes.append(ident.group(1))
        return bloc.replace("index: false", "index: true")
    s2 = re.sub(r"(?s)\{\s*\n\s*id: '[^']+',.*?\n  \},", ouvre, s)
    if ouvertes:
        ecrire(p, s2)
        print("%-14s ouvertes : %s" % (site, ", ".join(ouvertes)))
    else:
        print("%-14s registre déjà ouvert" % site)

    # ── 2 et 3. le pied de page ────────────────────────────────────────────
    p = R + "src/components/PiedDePage.astro"
    s = lire(p)
    # Tournefeuille IMPORTAIT ROUTES_COMMUNES sans jamais s'en servir : on
    # teste l'usage réel, pas la présence du nom.
    if "ROUTES_COMMUNES.map" in s:
        continue
    if site == "colomiers":
        continue  # Colomiers n'a pas de pages de commune

    if "ROUTES_COMMUNES" not in s:
        s = une(s, "route } from '../data/routes';", "ROUTES_COMMUNES, route } from '../data/routes';", "import " + site)

    # 2. les pages de commune dans la colonne « Le site » : elles sont alors
    #    liées depuis chaque page du site, comme les disciplines.
    s = une(s,
            """          <li><a class="lien" href={route('premiere-seance').chemin}>Première séance, débutants</a></li>
        </ul>
      </nav>""",
            """          <li><a class="lien" href={route('premiere-seance').chemin}>Première séance, débutants</a></li>
          {/* Les pages de commune étaient publiées mais liées 2 fois en tout
              (mesuré le 19/09) : aucune n'entrait dans Google. Ici, elles sont
              liées depuis chaque page du site, comme les disciplines. */}
          {ROUTES_COMMUNES.map((r) => (
            <li><a class="lien" href={r.chemin}>{r.nav}</a></li>
          ))}
        </ul>
      </nav>""", "communes " + site)

    # 3. une commune limitrophe qui a sa page devient un lien.
    s = une(s,
            """            <span class={c.note ? 'pied__commune pied__commune--cle' : 'pied__commune'} title={c.note}>{c.nom}</span>""",
            """            {ROUTES_COMMUNES.find((r) => r.nav === c.nom)
              ? <a class="lien pied__commune" href={ROUTES_COMMUNES.find((r) => r.nav === c.nom)!.chemin} title={c.note}>{c.nom}</a>
              : <span class={c.note ? 'pied__commune pied__commune--cle' : 'pied__commune'} title={c.note}>{c.nom}</span>}""",
            "limitrophes " + site)
    ecrire(p, s)
    print("%-14s pied : communes liées" % site)
