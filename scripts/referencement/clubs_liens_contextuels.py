# -*- coding: utf-8 -*-
"""19/09 — Un lien DANS LE TEXTE vers les sites de proximité, sur les pages
« club de boxe » de Portet et de Ramonville (section « Venir au club »).

Pourquoi : Colomiers, Cugnaux et Castelginest ont 0 page dans Google (mesuré le
19/09). Un lien dans un paragraphe d'une page explorée pèse plus qu'une ligne
de pied de page. Chaque club ne cite que les communes dont le site de
proximité le désigne comme destination : Portet ← Muret, Cugnaux,
Tournefeuille, Colomiers ; Ramonville ← Labège.
Rejouable. N'ajoute qu'une phrase ; aucun texte existant ne change."""
import io

def patch(p, a, b, marque):
    s = io.open(p, encoding="utf-8", newline="").read()
    if marque in s:
        print("déjà fait", p.split("/")[-1]); return
    if "\r\n" in s:
        a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert s.count(a) == 1, (p, s.count(a))
    io.open(p, "w", encoding="utf-8", newline="").write(s.replace(a, b))
    print("ok", p.split("/")[-1])

# Portet : après le paragraphe des cinq clubs.
patch("C:/Users/Mommy Jayce/Desktop/Boxing Center/Portet/boxing-center-portet/scripts/generate-club.mjs",
      """<a href="/partenaires/">les partenaires du club</a>.</p>
      </div>""",
      """<a href="/partenaires/">les partenaires du club</a>.</p>
        <p>Tu pars de Muret, de Cugnaux, de Tournefeuille ou de Colomiers ? Chaque commune a son site, avec le trajet jusqu’au club : ${DEPUIS.map(([v, u]) => `<a href="${u}">Boxing Center près de ${e(v)}</a>`).join(", ")}.</p>
      </div>""", "DEPUIS.map")
patch("C:/Users/Mommy Jayce/Desktop/Boxing Center/Portet/boxing-center-portet/scripts/generate-club.mjs",
      "const GABARIT = readFileSync(",
      """/* Les sites de proximité qui désignent Portet comme club : un lien dans le texte,
   en plus de la ligne du pied de page. */
const DEPUIS = [
  ["Muret", "https://www.boxingcenter-muret.fr/"],
  ["Cugnaux", "https://www.boxingcenter-cugnaux.fr/"],
  ["Tournefeuille", "https://www.boxingcenter-tournefeuille.fr/"],
  ["Colomiers", "https://www.boxingcenter-colomiers.fr/"],
];
const GABARIT = readFileSync(""", "const DEPUIS")

# Ramonville : après le paragraphe des horaires.
patch("C:/Users/Mommy Jayce/Desktop/Boxing Center/Deployment/bc-ramonville/scripts/generer-club-de-boxe.mjs",
      """<a href="/plannings/">les horaires de chaque cours</a>.</p>
        </div>""",
      """<a href="/plannings/">les horaires de chaque cours</a>.</p>
          <p>Tu pars de Labège ? Le trajet jusqu’au club est détaillé sur <a href="https://www.boxingcenter-labege.fr/">Boxing Center près de Labège</a>.</p>
        </div>""", "boxingcenter-labege.fr")
