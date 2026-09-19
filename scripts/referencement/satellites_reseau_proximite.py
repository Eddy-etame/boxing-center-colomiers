# -*- coding: utf-8 -*-
"""19/09 — Les sept sites de proximité se relient entre eux.

Mesuré le 19/09 : Colomiers, Cugnaux et Castelginest ont 0 page dans Google ;
Muret 10, Labège 4, Tournefeuille 3, L'Union 1. Aucun satellite ne liait un
autre satellite : Google n'arrivait aux trois absents par aucune page qu'il
explore déjà. Chaque pied de page relie donc son site aux six autres.

- src/data/verite.ts  : RESEAU_PROXIMITE (les sept sites)
- PiedDePage.astro    : « Tu pars d'une autre commune » + six liens « Boxing
                        Center près de <ville> » (le site courant est filtré)
Rejouable. Langage de proximité uniquement, aucun texte existant ne change."""
import io, sys

BASE = r"C:/Users/Mommy Jayce/Desktop/Boxing Center/Deployment/boxing-center-"
SITES = ["colomiers", "muret", "cugnaux", "tournefeuille", "labege", "lunion", "castelginest"]

REGISTRE = """
/* ─────────────────────────  LES SITES DE PROXIMITÉ  ───────────────────────── */
/**
 * Les sept sites Boxing Center « depuis ta commune ». Le pied de page relie
 * chacun aux six autres : le visiteur qui part d'une autre commune trouve le
 * site écrit pour lui, et les moteurs vont de l'un à l'autre.
 */
export const RESEAU_PROXIMITE: readonly { ville: string; url: string }[] = [
  { ville: 'Colomiers', url: 'https://www.boxingcenter-colomiers.fr/' },
  { ville: 'Tournefeuille', url: 'https://www.boxingcenter-tournefeuille.fr/' },
  { ville: 'Cugnaux', url: 'https://www.boxingcenter-cugnaux.fr/' },
  { ville: 'Muret', url: 'https://www.boxingcenter-muret.fr/' },
  { ville: 'Labège', url: 'https://www.boxingcenter-labege.fr/' },
  { ville: 'L’Union', url: 'https://www.boxingcenter-lunion.fr/' },
  { ville: 'Castelginest', url: 'https://www.boxingcenter-castelginest.fr/' },
];
"""

# Gabarit partagé (six sites) : dans le bloc « secteur », après la note.
BLOC_PARTAGE = """      {NOTE_SECTEUR && <p class="pied__note">{NOTE_SECTEUR}</p>}

      {/* Les six autres sites de proximité : celui qui part d'une autre commune
            trouve le site écrit pour lui. */}
      <p class="mono pied__cle pied__cle--2">Tu pars d’une autre commune</p>
      <p class="pied__communes pied__reseau">
        {RESEAU_PROXIMITE.filter((s) => !s.url.startsWith(SITE.origine)).map((s, i) => (
          <>
            {i > 0 && <span aria-hidden="true"> · </span>}
            <a class="lien" href={s.url}>Boxing Center près de {s.ville}</a>
          </>
        ))}
      </p>"""

# Colomiers (gabarit propre) : un sixième bloc dans la grille — 3 + 3 au lieu de 4 + 1.
BLOC_COLOMIERS = """      <nav aria-label="Les autres sites de proximité">
        <p class="mono pied__cle">Tu pars d’une autre commune</p>
        <ul>
          {RESEAU_PROXIMITE.filter((s) => !s.url.startsWith(SITE.origine)).map((s) => (
            <li><a class="lien" href={s.url}>Boxing Center près de {s.ville}</a></li>
          ))}
        </ul>
      </nav>
    </div>

    <div class="pied__bas">"""


def lire(p):
    return io.open(p, encoding="utf-8", newline="").read()


def ecrire(p, s):
    io.open(p, "w", encoding="utf-8", newline="").write(s)


def une(s, a, b, quoi):
    crlf = "\r\n" in s
    if crlf:
        a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    n = s.count(a)
    assert n == 1, (quoi, n)
    return s.replace(a, b)


for site in SITES:
    racine = BASE + site + "/"
    # 1. le registre
    p = racine + "src/data/verite.ts"
    s = lire(p)
    if "RESEAU_PROXIMITE" not in s:
        nl = "\r\n" if "\r\n" in s else "\n"
        s = s.rstrip("\r\n") + nl + REGISTRE.replace("\n", nl)
        ecrire(p, s)
    # 2. le pied de page
    p = racine + "src/components/PiedDePage.astro"
    s = lire(p)
    if "RESEAU_PROXIMITE" in s:
        print("déjà fait", site)
        continue
    if site == "colomiers":
        s = une(s, "import { CLUBS, CONTACT, HORAIRES, DISCIPLINES, SITE } from '../data/verite';",
                "import { CLUBS, CONTACT, HORAIRES, DISCIPLINES, SITE, RESEAU_PROXIMITE } from '../data/verite';", "import colomiers")
        s = une(s, "    </div>\n\n    <div class=\"pied__bas\">", BLOC_COLOMIERS, "bloc colomiers")
        # six blocs : trois colonnes, deux rangées pleines (quatre colonnes laissaient « Légal » seul)
        s = une(s, "    grid-template-columns: repeat(4, 1fr);\n    gap: var(--e-6);",
                "    grid-template-columns: repeat(3, 1fr);\n    gap: var(--e-6);", "grille colomiers")
    else:
        # la liste importée varie d'un site à l'autre (Tournefeuille importe aussi CLUBS)
        s = une(s, "NOTE_SECTEUR } from '../data/verite';", "NOTE_SECTEUR, RESEAU_PROXIMITE } from '../data/verite';", "import " + site)
        s = une(s, "      {NOTE_SECTEUR && <p class=\"pied__note\">{NOTE_SECTEUR}</p>}", BLOC_PARTAGE, "bloc " + site)
    ecrire(p, s)
    print("ok", site)
