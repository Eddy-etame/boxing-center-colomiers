# -*- coding: utf-8 -*-
"""19/09 — LA RÈGLE : en production, une page se range dans Google.

Eddy, 19/09 : « there should be a rule when we get into production, when
websites actually start serving on the official paid domains, they should go
straight to index, not no index anymore. »

Le 12/09, six pages par site étaient passées en `noindex` le temps de lever des
doublons entre les sept sites. Les domaines sont partis en production sans que
personne ne les rouvre : 42 pages du réseau sont restées hors de Google pendant
une semaine, et c'est un comptage manuel qui l'a trouvé, pas le build.

Le build refuse désormais toute page de contenu laissée en `noindex`. Deux
exceptions, écrites avec leur raison : la page 404 et la confirmation d'envoi du
formulaire. Une troisième exception doit être ajoutée ici, à la main, avec sa
raison — c'est la seule façon qu'un `noindex` ne se réinstalle pas en silence.

Rejouable."""
import io

BASE = r"C:/Users/Mommy Jayce/Desktop/Boxing Center/Deployment/boxing-center-"
SITES = ["colomiers", "muret", "cugnaux", "tournefeuille", "labege", "lunion", "castelginest"]

# Le corps de la règle. `LECTURE` est injecté selon que verifier.mjs a déjà ou
# non le texte de routes.ts sous la main.
REGLE = """
/* ────────  EN PRODUCTION, UNE PAGE SE RANGE DANS GOOGLE (19/09)  ────────
   Le 12/09, six pages par site étaient passées en noindex le temps de lever
   des doublons entre les sept sites. Les domaines sont partis en production
   sans que personne ne les rouvre : 42 pages du réseau sont restées hors de
   Google une semaine, et le build n'a rien dit. Il le dit maintenant.

   Deux exceptions, et il en faut une raison pour en ajouter une troisième :
   « introuvable » est la page 404 (la ranger serait un défaut) et « merci »
   est la confirmation d'envoi du formulaire (aucun contenu propre, atteinte
   par personne d'autre que celui qui vient d'écrire). */
{
LECTURE  const SANS_INDEX_LEGITIME = new Set(['introuvable', 'merci']);
  for (const bloc of SOURCE_ROUTES.split(/\\n\\s{2}\\{\\n/).slice(1)) {
    if (!/index:\\s*false/.test(bloc)) continue;
    const idRoute = (bloc.match(/id:\\s*'([^']+)'/) || [])[1];
    const cheminRoute = (bloc.match(/chemin:\\s*'([^']+)'/) || [])[1] || '?';
    if (!idRoute || SANS_INDEX_LEGITIME.has(idRoute)) continue;
    erreurs.push(
      `src/data/routes.ts — la page « ${idRoute} » (${cheminRoute}) est en noindex. ` +
        `En production, une page de contenu se range dans Google : passe-la en ` +
        `index: true, ou déclare-la comme exception dans scripts/verifier.mjs ` +
        `avec sa raison.`
    );
  }
}

"""

LECTURE_PROPRE = "  const SOURCE_ROUTES = readFileSync(join(RACINE, 'src', 'data', 'routes.ts'), 'utf8');\n"

for site in SITES:
    p = BASE + site + "/scripts/verifier.mjs"
    s = io.open(p, encoding="utf-8", newline="").read()
    if "SANS_INDEX_LEGITIME" in s:
        print("déjà fait      ", site)
        continue
    nl = "\r\n" if "\r\n" in s else "\n"

    # Où poser la règle : juste avant l'affichage du rapport.
    ancre = "console.log(`\\n  ${toutes.length} pages analysées"
    assert s.count(ancre) == 1, (site, "ancre du rapport", s.count(ancre))

    # verifier.mjs lit déjà routes.ts sous un nom ou sous un autre ?
    deja = None
    for nom in ("routesTs", "routes", "SRC_ROUTES"):
        if ("const %s = readFileSync" % nom) in s:
            deja = nom
            break
    regle = REGLE.replace("SOURCE_ROUTES", deja or "SOURCE_ROUTES")
    regle = regle.replace("LECTURE", "" if deja else LECTURE_PROPRE)
    assert "readFileSync" in s and "RACINE" in s, (site, "readFileSync/RACINE absents")

    s = s.replace(ancre, regle.strip("\n").replace("\n", nl) + nl + nl + ancre)
    io.open(p, "w", encoding="utf-8", newline="").write(s)
    print("règle posée    %-14s (routes lu via %s)" % (site, deja or "lecture ajoutée"))
