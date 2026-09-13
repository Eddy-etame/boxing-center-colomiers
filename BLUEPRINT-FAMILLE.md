# BLUEPRINT — Famille des sites satellites Boxing Center

Version 1 · 2026-09-08 · autorité d'implémentation pour Opus.
Gabarit de référence : `boxing-center-colomiers/` (14 pages, contrôle qualité au build, formulaire Inlet, barre de parcours). Chaque site de la famille est **une copie de ce gabarit** où l'on change le registre de vérité, les mots-clés, le texte, les photos et le système visuel — jamais la mécanique.

Un brief par site vit à la racine de son dossier : `boxing-center-<ville>/BLUEPRINT.md`. Ce document est la loi commune ; le brief de site précise les faits et les exceptions.

---

## 0. Les lois que rien ne peut contredire

1. **On vend la proximité, jamais l'absence.** Le visiteur a tapé « club de boxe <ville> ». La première chose qu'il lit doit lui confirmer qu'il est au bon endroit — un club l'accueille, à proximité — pas qu'il s'est trompé. Aucune phrase du type « il n'y a pas de salle à <ville> » nulle part. Le contrôle de build refuse ces tournures (`VENTE_NEGATIVE`).
2. **On ne laisse jamais croire qu'une salle est DANS la ville satellite.** Formulations : « club de boxe à proximité de <ville> », « accessible depuis <ville> », « Boxing Center accueille les habitants de <ville> dans son club de <destination> ». Jamais « situé à <ville> ». Aucun `LocalBusiness` pour la ville satellite. Le contrôle de build refuse ces tournures (`INTERDIT`).
3. **Un fait est écrit une fois**, dans `src/data/verite.ts`, puis projeté partout : HTML, meta, JSON-LD, `llms.txt`, formulaire. Horaires, adresses, téléphones, URLs de club, disciplines : jamais en dur dans un composant. Le contrôle de build refuse une heure de fermeture écrite hors registre.
4. **Chaque fait cite sa source et sa date.** Rien n'est publié sans source (`source: 'cahier-des-charges' | 'site-club' | 'wikipedia' | 'a-verifier'`). Ce qui n'est pas vérifié s'affiche comme tel ou ne s'affiche pas. On n'invente ni temps de trajet, ni distance précise, ni prix, ni tranche d'âge.
5. **Le texte vend.** Chaque section fait défiler vers la suivante ; chaque page se termine par une action, jamais par une sortie. Beaucoup de portes vers le club : boutons vers son accueil, ses activités, ses plannings, ses tarifs, sa première séance — avec des ancres porteuses (« Voir les plannings Boxing Center Portet »), pas « en savoir plus ».
6. **L'objectif SEO est la première place, pas « bien référencé ».** Tant qu'un site de la famille n'est pas premier sur ses motifs prioritaires, l'objectif n'est pas atteint. Ça commence par construire juste à tous les niveaux — et d'abord GEO, mots-clés, métadonnées (§6).
7. **Le SEO et la barre s'appliquent à tous les niveaux et à tous les sites** : titles, descriptions, H1, alt, noms de fichiers, JSON-LD, sitemap, llms.txt, vitesse, mobile, contraste. Un site de la famille qui rate un contrôle ne part pas en ligne.
8. **La copie n'est pas un site.** Même structure, même mécanique, mais le texte de chaque site est réécrit pour sa ville, son club, ses trajets, ses faits. Le test : lire l'accueil de deux sites de la famille côte à côte — s'ils sont interchangeables, c'est raté.

---

## 1. Ce qu'on garde du gabarit Colomiers, tel quel

- Astro 5 statique + adaptateur Vercel, zéro React, zéro bibliothèque de motion. `trailingSlash: 'always'`.
- `src/data/verite.ts` (registre), `routes.ts` (titres/descriptions/nav), `mots-cles.ts` (clusters vérifiés au build), `offres.ts` (graphe club × discipline, avec sources), `medias.ts` (manifeste photo : provenance, alt, légende, cadrage).
- La **barre de parcours** (`Parcours.astro` + `scripts/parcours.ts`) : persistante sur tout le site, le rouge/l'accent se mérite, le club est **dérivé** par le moteur et jamais écrit par un composant (voir la boucle infinie corrigée dans l'historique git de Colomiers).
- Le **formulaire** : POST natif → `/api/contact` (serveur) → Inlet (JSON + preuve de travail `sha256(défi:nonce)`, via `node:crypto`) → 303 `/merci/`. Pré-rempli par le parcours. Pot de miel `_gotcha`. Marche sans JavaScript.
- `Photo.astro` (AVIF/WebP/JPEG, 4 largeurs, aperçu flou base64) et `scripts/build-images.mjs`.
- `Bascule.astro` (N&B → couleur sur de vraies paires) quand le lot photo en contient.
- `Base.astro` : JSON-LD (`WebSite`, `Organization` + `SportsActivityLocation` par club avec adresse, horaires et `sport` tiré du graphe réel, `WebPage` + `dateModified` git, `BreadcrumbList`, `FAQPage` sur questions visibles), `areaServed` = ville + communes satellites, `geo.*`, noindex hors production Vercel (`src/lib/environnement.ts`).
- `sitemap.xml.ts` (lastmod = dernier commit git de la page ou de `src/data`), `robots.txt.ts`, `llms.txt.ts`, `vercel.json` (apex → www, en-têtes, cache immuable), `scripts/indexnow.mjs`.
- `scripts/verifier.mjs`, branché sur `npm run build` : formulations interdites, vente négative, faits faux, heures en dur, liens internes, H1 unique, alt, titles/descriptions (≤ 65 / ≤ 165, uniques), canonique, JSON-LD parsable, liens sortants exigés, **mots-clés prioritaires présents dans le texte visible**.
- Les jetons `jetons.css` conscients de la polarité (`--signal-texte`, `--acier-sombre` redéfinis dans `.clair`/`.papier`), la loi de contraste (AA mesuré, pas jugé), `prefers-reduced-motion`, `forced-colors`.
- Budget : premier écran ≈ 230 ko, JavaScript < 5 ko, image LCP en AVIF ≤ 160 ko.

## 2. Ce qui change sur un site satellite (par rapport à Colomiers)

| Point | Colomiers | Satellite |
|---|---|---|
| Destinations | deux clubs, le moteur choisit | **un** club (sauf Tournefeuille : deux). Le moteur n'a plus de choix de club à faire |
| Question du moteur | « quel club ? » | **« quelle séance ? »** : discipline × créneau → l'intitulé réel du club + le créneau + un fait sur la salle, puis redirection vers la page du club |
| Barre de parcours | Départ → discipline → créneau → **club** | Départ → discipline → créneau → **séance** (le club est acquis dès le départ ; l'accent se tend sur le *quand*) |
| Nav Plannings / Tarifs | pages internes qui renvoient | **liens externes directs** vers les pages réelles du club (`rel="noopener"`, ↗). Les pages internes `/plannings/` et `/tarifs/` sont **supprimées** |
| `/quel-club/` | page moteur | devient `/ta-seance/` (mono-destination) ; Tournefeuille garde `/quel-club/` |
| Communes voisines | une section + FAQ + `areaServed` | **une page par commune satellite** (§4) + section + FAQ + `areaServed` |
| Palette | encre + os + acier + rouge sémantique | **le système visuel du site** (§7) — jamais celui de Colomiers ni d'un club |
| Fait sur la salle | — | un « fun fact » vérifié par club, affiché dans le résultat du moteur et en accueil (600 m² et une cage à Portet ; 1 200 m², deux rings, 16 sacs, « la plus grande salle de France » à États-Unis ; 300 m² à ciel ouvert à Ramonville ; métro A à 4 min à Saint-Cyprien) |

## 3. Structure des pages d'un satellite

```
/                         accueil — 11 sections (H01 hero, H02 proximité, H03 moteur « ta séance », H04 disciplines,
                          H05 bascule/photo, H06 le club de destination (fiche : adresse, tel, accès, fait), H07 première
                          séance, H08 horaires/amplitude, H09 questions locales, H10 le secteur (communes), H11 convergence)
/boxe-anglaise/           4 pages disciplines — ALIGNÉES SUR L'OFFRE RÉELLE DU CLUB DE DESTINATION (§5) :
/mma/                     Portet → boxe anglaise · MMA (+grappling/JJB) · kick-boxing/pieds-poings · enfants
/kick-boxing/             Saint-Cyprien → boxe anglaise · K1/kick · Muay Thaï · femme/fitness
/boxe-enfants/            Ramonville → boxe · MMA/grappling · pieds-poings · enfants (Baby boxe 3/6)
                          États-Unis → boxe · MMA/grappling/JJB · kick & Muay Thaï · enfants/jeunes
                          (les slugs suivent les disciplines réelles ; « boxing-fitness » n'existe que si le club publie une offre femme/fitness)
/preparation-physique/    UNIQUEMENT pour les sites vers États-Unis (L'Union, Castelginest) — décision Eddy 2026-09-08 : Hyrox, cross-training, musculation & cardio sont publiés par le club ; « salle de sport » est un cluster à part
/premiere-seance/         la première séance, minute par minute — avec les conditions réelles du club (10 € à Saint-Cyprien et États-Unis, séance offerte…) SEULEMENT si vérifiées
/ta-seance/               l'adresse à part entière du moteur (Tournefeuille : /quel-club/)
/<commune-satellite>/     une page par commune imposée (§4)
/contact/  /merci/        formulaire Inlet, pré-rempli
/mentions-legales/  /confidentialite/  /404
robots.txt  sitemap.xml  llms.txt  /api/contact
```

Navigation principale : Accueil · les 4 disciplines · **Plannings ↗** · **Tarifs ↗** · Contact. Pied de page : le club (adresse, tel, site, activités, première séance), les disciplines (ancres porteuses), « Pour décider » (ta séance, première séance), les communes, mentions.

Redirections 301 depuis les formes d'URL à mots-clés (`/club-boxe-<ville>`, `/club-mma-<ville>`, `/boxe-thai-<ville>`…) vers les pages canoniques — jamais de page à ces adresses.

## 4. Les pages par commune satellite — le contrat qui les sauve

Le brief impose une page par commune (« Cugnaux + Villeneuve-Tolosane, Frouzins, Seysses », etc.). C'est exactement le schéma « page-ville » que Google surveille comme page satellite. La règle qui les rend légitimes :

**Le test du remplacement.** Si l'on remplace le nom de la commune par un autre et que la page reste vraie, la page est une page satellite et elle sera traitée comme telle. Chaque page commune doit contenir **au moins 40 % de contenu propre à cette commune**, vérifiable :

- son code postal, sa population, son gentilé (source Wikipédia, datée) ;
- **d'où l'on part réellement** : l'axe routier qui mène au club depuis CETTE commune (A64 sortie N, D817, rocade sortie N, Linéo L3, TER gare X), sans temps de trajet inventé ;
- ses communes limitrophes (dont, souvent, la ville principale du site — c'est le lien de maillage naturel) ;
- une FAQ propre (3 questions minimum) : « depuis <commune>, quel accès ? », « <commune> ou <ville> : même club ? », « les enfants de <commune> ? » ;
- un fait local honnête (l'olivier millénaire de L'Union, l'Innopole de Labège, Ader à Muret…) — jamais décoratif : il sert à situer ;
- ses propres title / description / H1 / canonique, ses mots-clés (les 9 motifs déclinés sur la commune) vérifiés au build ;
- `areaServed` de l'`Organization` inclut la commune ; la page a son `BreadcrumbList` (Accueil › <commune>).

Ce qui est interdit sur ces pages : un texte d'accueil recopié avec le nom changé, une adresse dans la commune, un `LocalBusiness`, un temps de trajet, une distance au mètre.

Le nombre de pages communes est fixé par le brief de site. On n'en ajoute pas.

## 5. Le registre de vérité d'un satellite (`src/data/verite.ts`)

```
SITE        origine, nom (« Boxing Center — depuis <Ville> »), villeOrigine, codePostal, gentile, departement
CONTACT     téléphone et e-mail de réception du formulaire (identiques réseau sauf mention contraire)
CLUBS[]     id, nom, adresse, codePostal, ville, téléphone, site, plannings, tarifs, activites, premiereSeance,
            horaires { texte, court, ouverture, fermeture }  ← PAR CLUB (Saint-Cyprien ≠ Portet), source + date
            acces (métro/bus/sortie), faits[] (surface, ring, cage, particularités — sourcés), angle, depuisVille
OFFRES[]    intitulés RÉELS publiés par le club, famille, âges, source (page activités du club)
COMMUNES    la ville d'origine + ses communes satellites : nom, cp, gentilé, population, limitrophes, accès, fait
INTERDIT / VENTE_NEGATIVE / FAITS_FAUX   les gardes-fous, hérités
```

Horaires (tranchés par Eddy, 2026-09-08) : Portet lun–sam 10h–21h30 · Minimes lun–sam 10h–21h30 · Ramonville lun–sam 10h–21h30 · **Saint-Cyprien lun–sam 10h–21h15** (c'est ce que dit son planning : on va avec ça) · États-Unis : le site n'affiche que les horaires du comptoir (lun–ven 12h–14h / 17h–20h30) — ne pas les publier comme amplitude d'entraînement ; écrire « ouvert 6 jours sur 7 » et renvoyer au planning du club. **Les horaires sont PAR CLUB dans le registre**, jamais une valeur réseau.

URLs réelles à utiliser tel quel : Portet `/activites/ /plannings/ /tarifs/` · Saint-Cyprien `/activites/ /plannings/ /tarifs/ /seance-offerte/ /la-salle/` · Ramonville `/activites/ /plannings/ /tarifs/ /la-salle/` · États-Unis `/disciplines/ /planning/ /abonnements/ /contact/` · Minimes `/activites/ /plannings/ /tarifs/`.

## 6. SEO — la méthode, appliquée à chaque site

- **Neuf motifs par ville** (brief) : `boxe <v>` · `club de boxe <v>` · `boxe anglaise <v>` · `club MMA <v>` · `salle MMA <v>` · `sport de combat <v>` · `club boxe thaï <v>` · `club kick boxing <v>` · `boxe pieds poings <v>`. Déclinés sur chaque commune satellite. Chaque motif est porté par la page qui répond réellement à la question, pas par un mur de mots : `club de boxe / boxe / sport de combat` → accueil ; `boxe anglaise` → /boxe-anglaise/ ; `club MMA / salle MMA` → /mma/ ; `boxe thaï / kick boxing / pieds poings` → /kick-boxing/ ; chaque commune → sa page. Le registre `mots-cles.ts` déclare les prioritaires ; le build échoue s'ils manquent du texte visible.
- **Plus de pertinence par page, pas plus de pages** au-delà de celles du brief.
- Titles ≤ 60, descriptions ≤ 165, un H1, H2 structurés, fil d'Ariane visible + `BreadcrumbList`.
- **FAQ visibles** (`<details>`) sur l'accueil, les disciplines, les communes → `FAQPage`. Jamais de FAQ cachée.
- **Ce que chaque club a de singulier est le contenu le plus citable** : la cage de Portet, les 1 200 m² d'États-Unis, le ciel ouvert de Ramonville, le métro à 4 min de Saint-Cyprien. Les IA citent des faits différenciants, pas des adjectifs.
- `llms.txt` généré depuis le registre : les formulations exactes à reprendre, les adresses réelles, le graphe des disciplines, le territoire (ville + communes).
- Sitemap avec `lastmod` git ; aperçus Vercel en `noindex` ; `vercel.json` apex → www ; IndexNow après un déploiement de production uniquement.
- Liens entrants à obtenir de l'écosystème : `boxingcenter.fr` et le site du club de destination vers le satellite, avec des ancres descriptives (« Vous habitez Muret ? L'orientation Boxing Center depuis Muret »). Hors dépôt — à faire poser par Eddy.
- **Cannibalisation** : dès qu'un satellite existe, sa ville sort de la liste `COMMUNES_VOISINES` des autres sites (Tournefeuille, Plaisance-du-Touch et Cugnaux sont aujourd'hui dans celle de Colomiers → à retirer).

## 6 bis. La première place — les leviers, dans l'ordre où ils pèsent

1. **L'entité.** `Organization` Boxing Center → `SportsActivityLocation` du club avec adresse, téléphone, horaires, `sport` réel, `sameAs` vers son site ; `areaServed` = ville + communes ; jamais de `LocalBusiness` pour la ville satellite. Une entité propre est ce que Google et les moteurs de réponse relient.
2. **Le fait différenciant, visible et cité.** Cage, m², rings, métro à 4 min, ciel ouvert : dans le H2, la FAQ, le JSON-LD, `llms.txt`. Les IA citent des faits, pas des adjectifs.
3. **Les motifs dans le texte visible**, vérifiés au build — jamais dans `<meta keywords>`.
4. **Les pages communes qui passent le test du remplacement** : c'est la longue traîne locale, et c'est là qu'on est premier vite.
5. **Le maillage** : chaque satellite ↔ le club de destination ↔ `boxingcenter.fr` ↔ les satellites voisins (Launaguet : L'Union ↔ Castelginest ; Seysses : Cugnaux ↔ Muret), avec des ancres descriptives.
6. **La vitesse et le mobile** : LCP ≤ 2,5 s sur 4G, CLS 0, premier écran ≤ 250 ko.
7. **La fraîcheur honnête** : `lastmod` git, `dateModified`, contenus datés (« relevé le »).
8. **La mesure** : Search Console par site dès la mise en ligne, IndexNow après chaque production, un relevé de position par motif prioritaire chaque semaine dans `.recherche/positions-<ville>.md`. Sans relevé, « première place » est une opinion.

## 7. Le système visuel — une famille, pas six clones ni six inconnus

Loi du réseau (doc interne `_boxing-center-maquettes/README.md`) : chaque salle a **un métal, une énergie** — Minimes noir+rouge, Portet navy+argent, États-Unis navy+bronze, Saint-Cyprien clair, Ramonville nuit. Colomiers : encre + rouge sémantique. Un satellite ne prend jamais la palette d'un club ni celle d'un autre satellite.

**Décision (Eddy, 2026-09-08) — un seul système satellite, « le satellite porte la couleur de là où il t'envoie »** : un seul système satellite (structure, type, motion, tokens) décliné en quatre sous-familles selon la destination :

| Sous-famille | Fond | Texte (contraste) | Accent (contrastes mesurés le 2026-09-08, formule WCAG) |
|---|---|---|---|
| Portet | `#f3efe6` | `#1e2044` (13.6:1) | `#7a3d16` en petit texte (**7.3:1**, AA) · `#b8763a` en aplats et très gros titres seulement (3.2:1) — cuivre |
| Saint-Cyprien | `#eeeeea` | `#1e2044` (13.4:1) | `#3b3f47` en petit texte (**9.1:1**, AA) · `#9db83f` en aplats et très gros titres seulement (1.9:1) — graphite (aplats vert de fresque) |
| Ramonville | `#f4f1ea` | `#1e2044` (13.8:1) | `#2f6b3a` en petit texte (**5.7:1**, AA) · `#6fa84a` en aplats et très gros titres seulement (2.5:1) — vert gazon |
| États-Unis | `#f4f1ea` | `#1e2044` (13.8:1) | `#7d5a1e` en petit texte (**5.6:1**, AA) · `#c9a45a` en aplats et très gros titres seulement (2.1:1) — bronze |

Monde matériel qui justifie chaque accent : Portet = cuir brun des sacs, cordes rouges, murs bleus ; Saint-Cyprien = murs noirs, fresque grise, gants rose-or ; Ramonville = cage, tatamis, gazon, ciel ouvert ; États-Unis = les 1 200 m², le bronze du club. Jamais la palette d'un club lui-même. Jeton `--signal-texte` = la colonne « petit texte » ; `--signal` = l'aplat.

Toutes claires (papier/os) : c'est l'inversion de Colomiers (sombre) à structure égale, et ce qui sépare le plus la famille des sites de clubs (sombres). Risque nommé : voisinage de Saint-Cyprien « clair / Apple-Linear » — mitigé par le papier chaud, l'encre et le dessin technique, qui ne sont pas le blanc Apple.

**Décision (Eddy, 2026-09-08) : le hero-type de la famille est A — L'Éole.** Un dessin d'ingénieur qui se trace : la route <ville> → <club> cotée avec des faits réels, l'aile de l'Éole comme trait fondateur à Muret ; sur les autres sites, le même mécanisme de cotes (distance routière vérifiée, surface, horaires, nombre de disciplines, accès) dessine la route vers la destination, sans l'aile — l'aile n'appartient qu'à Muret. Détail complet : `boxing-center-colomiers/.recherche/muret.md` §6.

Typographie : **différente de Colomiers** (Archivo Black/Archivo/Space Mono lui restent). Proposition A : une grotesk d'ingénierie (Bricolage Grotesque en display) + Instrument Sans (texte) + JetBrains Mono (cotes, étiquettes), auto-hébergées via `@fontsource`. Loi de lisibilité : texte encre sur papier ≥ 12:1 ; l'accent cuivre n'est jamais du petit texte (2,2:1 sur papier) — aplats, traits, très gros titres seulement ; les petits textes en accent passent par un jeton `--signal-texte` mesuré ≥ 4,5:1.

Motion : CSS + WAAPI + SVG, `prefers-reduced-motion` conçu, rien de décoratif : la ligne se tend quand un fait s'établit. Mobile = même expérience, transformée, jamais amputée.

## 8. Images — provenance, nommage, priorité

Ordre : **le dossier WeTransfer du site** (mis en avant, hero compris) → **le stock du club de destination** (`scrapers/output_imgs/<club>`, 768×512 : vignettes et portraits de coachs uniquement) → **les non-utilisées des autres sites** (Colomiers : `cours-boxe-colomiers-sac-de-frappe`, `sparring-boxe-colomiers`, `sport-combat-colomiers-sac-frappe`, `coach-boxe-colomiers-paos`, `cours-boxe-colomiers-encadrement(-2)` — photos de **Minimes**, à légender comme telles) → `output_imgs/boxingcenter_fr` (150, à trier).

Une image de hero fait ≥ 2 000 px de large. Pas de séance photo prévue pour États-Unis : L'Union et Castelginest se construisent avec les photos du réseau (Portet pour l'un, Minimes pour l'autre, jamais les mêmes), légendées selon la règle ci-dessus. Les WhatsApp 768×1024 de Cugnaux et tout le stock 768×512 ne sont **jamais** des heros.

**Légendes (décision Eddy, 2026-09-08) : ce qu'on voit + le club de destination du site.** Toujours, quelle que soit la salle où la photo a été prise — « Travail au sac — Boxing Center Portet-sur-Garonne » sur Muret et Cugnaux, « La cage — Boxing Center Saint-Cyprien » ou « … Portet-sur-Garonne » sur Tournefeuille selon le club que la page vise, « … — Boxing Center Ramonville » sur Labège, « … — Boxing Center Toulouse États-Unis » sur L'Union et Castelginest. On n'a pas besoin de connaître la salle d'origine ; le champ `lieu` du manifeste n'existe plus. Un `alt` décrit la scène, jamais un lieu.

Nommage SEO (décision Eddy, 2026-09-08 — obligatoire, vérifié par un test) : **`<sujet>-<ville-du-site>.<ext>`**, minuscules, sans accent, le sujet = ce qu'on voit, la ville = celle du site, jamais celle de la salle. Exemples : `ring-de-boxe-muret.webp`, `sac-de-frappe-muret.webp`, `cage-mma-cugnaux.webp`, `boxe-thai-tournefeuille.webp`, `coach-boxe-labege.webp`, `boxe-enfant-lunion.webp`, `preparation-physique-castelginest.webp`. Deux photos du même sujet : `-2`, `-3` (`coach-boxe-labege-2.webp`). Pas de « boxing-center » ni de numéro dans le nom. Une photo prise à Minimes ou à Portet sur un site qui envoie ailleurs n'est pas un problème (Eddy) : le nom porte la ville du site, la légende suit la règle ci-dessus.

Manifeste `medias.ts` : slug, source, alt (ce qu'on voit), légende (ce qu'on voit + le club de destination), paires N&B/couleur si elles existent. **Aucune mention de photographe** nulle part (décision Eddy) ; les mentions légales sont **identiques à celles de Colomiers** (éditeur, établissements, hébergeur Vercel, nature du site, propriété intellectuelle, liens sortants — SIRET et directeur de publication restent à renseigner, comme sur Colomiers).

## 9. Concurrence — connaître, reprendre, dépasser

Par ville, avant d'écrire : les trois premiers résultats de « club de boxe <ville> », « MMA <ville> », « boxe thaï <ville> ». Pour chacun : ses mots-clés, ses promesses, ses preuves, ses défauts (photos, mobile, faits absents, prix cachés). Puis : reprendre chaque promesse vraie chez nous avec une preuve plus forte (un fait sourcé, une photo réelle, un accès précis), reformuler ce qu'ils disent mal, et ajouter ce qu'ils n'ont pas (le moteur, la première séance minute par minute, la page commune). Consigner dans `.recherche/concurrence-<ville>.md` (gitignoré). Pistes déjà vues : un club de boxe à Cugnaux (Wikipédia), un dojo à L'Union (2020), Colomiers Boxing Club et Maison du Fight côté Colomiers.

## 10. Produire un site — la liste, dans l'ordre

1. Copier `boxing-center-colomiers/` (sans `.git`, `node_modules`, `.vercel`, `public/photos`, `.recherche`) dans `boxing-center-<ville>/`. `git init`, remote du brief, premier commit.
2. `verite.ts` : SITE, CONTACT, le ou les CLUBS avec URLs réelles et horaires **par club**, OFFRES depuis la page activités du club (vérifiée le jour même), COMMUNES avec faits Wikipédia datés.
3. `routes.ts` : pages disciplines alignées sur l'offre réelle ; `/ta-seance/` ; une route par commune ; Plannings/Tarifs retirés des routes internes, ajoutés en liens externes dans `Entete.astro` et le pied.
4. `mots-cles.ts` : les 9 motifs × (ville + communes), répartis par page ; prioritaires vérifiés au build.
5. `contenus.ts` + pages : **réécrire** — pas adapter — l'accueil, les disciplines, la première séance, les communes. Ton : clair, local, rassurant, sportif, tutoiement respectueux. Chaque section vend et fait descendre.
6. Photos : manifeste, renommage SEO, `npm run images`, hero ≥ 2 000 px.
7. Palette et type de la sous-famille (§7) dans `jetons.css` ; hero de la direction retenue.
8. `npm run build` : zéro erreur, zéro avertissement au contrôle. Contraste mesuré. Sans JavaScript vérifié. Formulaire testé de bout en bout (message marqué TEST).
9. Push, Vercel (aperçu `noindex`), domaine, puis `npm run indexnow` après la production.
10. Retirer la ville des `COMMUNES_VOISINES` des autres sites de la famille.

## 11. Définition de « fini » pour un site

Contrôle de build à zéro · 9 motifs × communes couverts · aucune phrase interdite ni négative · aucun fait sans source · horaires du bon club · nav Plannings/Tarifs sur les vraies URLs du club · pages communes passant le test du remplacement · photos ≥ 2 000 px en hero, nommées SEO, légendées avec la vraie salle · contraste AA mesuré sur toutes les pages · premier écran ≤ 250 ko · zéro erreur console dans un onglet vierge · formulaire testé · aperçus noindex · sitemap valide.

## 12. Ouvert — à trancher par Eddy

Tranché le 2026-09-08 : hero A L'Éole · un système satellite décliné par destination · pas de séance photo, légendes en phase avec le site · Saint-Cyprien 21h15 · /preparation-physique/ sur L'Union et Castelginest · nommage `<sujet>-<ville>` · aucune mention de photographe. Restent ouverts : SIRET et directeur de publication · Cugnaux au sud-ouest (corriger la fiche) · rebuild du plugin de skills (sources mises à jour le 2026-09-08).

---

## 13. Spécification d'exécution — ce qui fait la barre, pas la copie

### 13.1 Le hero « L'Éole » — le dessin coté qui se trace
Un `<svg>` inline, aucun canvas, aucun WebGL, aucune bibliothèque.
- **La route** : une polyligne à un seul coude (un plan, pas une carte) du nœud `ORIGINE` (la ville, à gauche) au nœud `DESTINATION` (le club, à droite). Trait `--acier-sombre` 1 px ; par-dessus, le même tracé en `--signal` 1,5 px avec `stroke-dasharray` égal à sa longueur (`getTotalLength()` au montage, ou valeur figée dans le SVG) : il **se trace** en 900 ms (`--e-resolution`) au chargement, puis suit la tension de la barre de parcours (déjà câblée : `--tension`).
- **Les cotes** : 3 à 5 lignes de cote perpendiculaires (tirets aux extrémités, comme un plan d'ingénieur), étiquettes en mono (`JetBrains Mono`, `--t-micro`, `--signal-texte`). Chaque cote porte **un fait du registre, avec sa source** : distance routière (« 23 km par la route — Wikipédia »), surface (« 600 m² »), amplitude (« 10h–21h30 »), nombre de disciplines (« 9 disciplines »), accès (« A64, sortie Portet »). Les cotes se dessinent 120 ms l'une après l'autre après la route ; l'étiquette apparaît par un balayage `clip-path` gauche→droite, pas par un fondu.
- **L'aile (Muret seulement)** : la silhouette de l'aile de chauve-souris de l'Éole en un seul trait (une `<path>` de ~40 points, tracée à la main depuis une gravure libre de droits, jamais générée), dessinée en 600 ms AVANT la route, puis ramenée à 18 % d'opacité derrière elle. Sur les autres sites : pas d'aile, le nœud d'origine porte le blason typographique de la ville (nom + code postal en mono).
- **Mobile** : la route passe à la verticale (origine en haut, destination en bas), les cotes à droite ; mêmes durées ; le hero tient dans un écran de 360 px sans scroll horizontal.
- **Reduced motion** : tout est rendu à l'état final, aucune animation, aucune perte d'information.
- **Sans JavaScript** : le SVG est complet dans le HTML (état final), le texte du hero est du HTML.
- **Le texte** : H1 affirmatif (loi 1), une phrase qui nomme le club et les disciplines réelles, deux boutons (« Trouver ma séance » → `#ta-seance` ; « Le site du club » ↗). Trois faits en pied de hero (amplitude · club · niveau), déjà dans le gabarit.
- **Ce que le hero ne fait pas** : pas de photo plein écran derrière (la photo arrive en H02, sur une plaque de couleur — mécanisme akaru), pas de texte qui bouge, pas de particules, pas de compteur qui défile.

### 13.2 `/ta-seance/` — le moteur à une destination
- Deux `fieldset` de vrais boutons radio : **discipline** (une entrée par famille RÉELLEMENT publiée par le club, libellée avec l'intitulé du club : « Boxe Thaï / K1 », « Baby Boxe », « MMA ») et **créneau** (midi · après-midi · soir · samedi).
- Résultat (`aria-live="polite"`) : « Ta séance : *<intitulé du club>*, *<créneau>*, à *<club>* » + le fait du club (fun fact) + trois portes : **Voir le planning ↗** (URL réelle du club), **Ta première séance** (interne), **Poser ma question** (contact pré-rempli). Le créneau n'invente pas d'horaire : il dit « le club publie ses cours du <créneau> sur son planning » et renvoie.
- Sans JavaScript : la liste complète des familles avec intitulés réels et les trois portes.
- Barre de parcours : Départ → discipline → créneau → **séance** ; le club est acquis dès le départ et s'affiche dès la première visite ; l'accent se tend sur le *quand*. Tournefeuille : la variante à deux clubs de Colomiers, le graphe réel tranche (thaï → Saint-Cyprien, MMA → Portet).

### 13.3 Le gabarit de page commune (test du remplacement)
1. Fil d'Ariane · H1 « Club de boxe et MMA à proximité de <Commune> (<CP>) » · chapeau : le club de destination, l'accès réel depuis CETTE commune, en une phrase sourcée.
2. **Depuis <Commune>** — l'axe (route, sortie, ligne de bus/TER), les communes limitrophes (dont la ville principale du site : c'est le lien de maillage), la direction sans temps de trajet. Un fait local honnête qui situe (un pont, une gare, une zone d'activité).
3. **Ce que tu trouves à <club>** — les intitulés réels (composant partagé), le fun fact.
4. **Questions depuis <Commune>** — 3 questions propres minimum (accès ; « <Commune> ou <Ville> : même club ? » ; enfants ; horaires), `FAQPage`.
5. Conversion (composant partagé).
Interdits : recopier l'accueil avec le nom changé ; une adresse dans la commune ; un `LocalBusiness` ; un temps de trajet. Le contrôle de build vérifie les 9 motifs de la commune sur sa page et refuse une page commune dont le texte propre (hors composants partagés) fait moins de 250 mots.

### 13.4 Typographie
`@fontsource/bricolage-grotesque` (display, 700 et 800, `font-optical-sizing`), `@fontsource/instrument-sans` (texte, 400/500/600), `@fontsource/jetbrains-mono` (cotes, étiquettes, 400/700). Auto-hébergées, `font-display: swap`, préchargement des deux du premier écran. Échelle fluide reprise du gabarit (`--t-*`). Display : capitales réservées aux cotes ; les titres sont en bas-de-casse avec majuscule initiale, tracking −0,02 em. Jamais Archivo sur un satellite.

### 13.5 L'écriture — la doctrine, avec avant / après
Tutoiement respectueux · clair, local, rassurant, sportif · le fait avant l'adjectif · chaque section finit par une main tendue vers la suivante · chaque page finit par une action.
| Avant (faute) | Après (barre) |
|---|---|
| « Il n'y a pas de salle Boxing Center à Colomiers. » | « Deux clubs Boxing Center t'accueillent à proximité de Colomiers. » |
| « Voir la discipline → » | « Boxe anglaise près de Muret → » |
| « Les deux clubs proposent le MMA. » | « Le MMA se pratique à Portet, dans une cage — le club à viser depuis Muret. » |
| « À 10 minutes en voiture. » (inventé) | « Par l'A64, sortie Portet ; le club est sur la route d'Espagne. » (sourcé) |
| « Y a-t-il un club à <Ville> ? — Non. » | « Où s'entraîner quand on habite <Ville> ? — Boxing Center t'accueille à <club>, <accès>. » |
Une phrase de recherche vocale par page, dite naturellement (« je cherche un club de boxe près de Muret » devient « Si tu cherches un club de boxe près de Muret… »). Une variante orthographique par titre, les autres dans le corps.

### 13.5 bis L'ÉCRITURE — les règles qu'Eddy a dû redire, et qu'on n'a plus le droit d'oublier

Corrections données les 2026-09-08 et 09. Elles priment sur tout ce qui précède.

1. **Zéro figure de style.** Pas de métaphore, pas de comparaison, pas de
   personnification, pas de clin d'œil, pas de chute. Le style visuel reste ; les
   figures de rhétorique sortent. « La cage n'est pas un décor », « on s'entraîne
   ici depuis six mille ans », « la borne du géomètre » : à jeter.
2. **Zéro négation.** On écrit ce qui existe. Jamais « le club n'est pas à X km »,
   jamais une réponse de FAQ qui commence par « Non ». On attaque par
   l'affirmation.
3. **Le hero ne nomme JAMAIS l'autre ville en premier.** Quelqu'un qui a cliqué
   « Boxing Center <Ville> » et qui lit une autre commune dans le H1 s'en va. Le
   H1 dit : « Ton club de boxe et de MMA **à proximité de <Ville>** ». Le nom du
   club arrive plus bas, une fois la raison de rester donnée. On referme l'écart
   par la langue : *à proximité de*, *à deux pas*, *la commune voisine*.
4. **Aucun mot qui évoque une distance.** Pas de kilomètres, pas de durée de
   trajet. On dit la ligne de bus, la sortie d'autoroute, l'arrêt. Un numéro de
   ligne rapproche, un chiffre en kilomètres éloigne.
5. **Des phrases courtes, adressées au lecteur.** Sujet, verbe, complément. On
   tutoie. On donne l'information dans l'ordre où elle se pose : ce que c'est, où
   c'est, ce qui va se passer, comment on y va, ce qu'il faut apporter.
6. **Les titres de FAQ sont des questions, pas des requêtes.** « Où est le club le
   plus proche ? », pas « « club de boxe X » : où ça se passe ? ». Les expressions
   exactes vivent dans le `<title>`, la description et le corps des réponses.
7. **Ne jamais commenter le site lui-même.** Aucune phrase sur « ce site est un
   plan », « notre légende », « la planche ». Le visiteur cherche un club.
8. **Test du persona, avant de livrer.** Prendre quelqu'un qui n'a aucune raison
   d'être là, qui scrolle vite, et relire chaque écran de son point de vue :
   est-ce qu'il comprend en trois secondes, et est-ce qu'il a une raison de
   continuer ?

### 13.8 COULEUR ET MOUVEMENT — un site ne doit jamais ressembler au précédent

Décision Eddy, 2026-09-09 : la sous-famille par club de destination **ne suffit
pas**. Chaque site a sa propre teinte et sa propre signature de mouvement.

- **Couleur.** Papier, encre et accent changent d'un site à l'autre, et la teinte
  se justifie par ce qu'on voit sur les photos du site (le sol turquoise de la
  salle pour Cugnaux, le vert de la fresque pour Tournefeuille). Les contrastes
  se mesurent avant d'écrire une ligne : encre ≥ 12:1, accent texte ≥ 4,5:1 sur
  papier ET sur papier creusé. Les jetons `--nav-*` portent la barre sombre, qui
  suit donc la couleur du site.
- **Mouvement.** `--mouv-x`, `--mouv-y`, `--mouv-echelle`, `--mouv-duree`,
  `--mouv-decalage` et `--mouv-courbe` forment la signature d'un site : montée
  franche ici, glissement latéral là, arrivée en échelle ailleurs. Les
  révélations, les fondus et les délais changent. Deux sites de la famille ne
  doivent pas donner la même sensation au scroll.

### 13.6 Contrôles ajoutés au `verifier.mjs` du gabarit
- Noms de fichiers image : `^[a-z0-9-]+-(<ville>)(-[2-9])?\.(avif|webp|jpg)$` — le nom porte la ville du site, jamais « boxing-center », jamais un numéro d'origine.
- Aucun `<img>` de hero (attribut `fetchpriority="high"`) sous 2 000 px de large.
- Chaque page commune : ses 9 motifs présents, ≥ 250 mots propres.
- Nav : les liens Plannings et Tarifs pointent sur les URLs réelles du registre (`CLUBS[].plannings`, `CLUBS[].tarifs`), et répondent 200 au moment du build (une requête `HEAD` par lien, tolérance réseau : avertissement, pas erreur).
- Aucun nom de photographe dans le HTML.

### 13.7 Ce qu'un site de la famille doit pouvoir devenir
Une référence dans la banque : passer les cinq tests du portillon (incrédulité, mécanisme nommable, cohérence sur toutes les surfaces, parité mobile, performance) comme n'importe quel site capturé. Le mécanisme nommable de la famille : **la route cotée par des faits sourcés, qui se tend à mesure que la personne décide**. Si, en le regardant, on peut nommer la référence dont il vient, c'est raté.

### 13.9 CE QUE LE CSS N'A PAS LE DROIT DE SAVOIR — quatre défauts trouvés en regardant les pages
Ces quatre-là ont vécu en ligne. Chacun coûtait une section entière, et aucun n'a été attrapé par le build : ils passent tous la compilation. On les relit avant chaque livraison.

1. **Aucune règle CSS ne nomme une donnée du registre.** Les onglets d'itinéraire choisissaient leur panneau par une liste de `:has(#trajet-<id>:checked)` écrite à la main. Elle portait les identifiants de Muret : sur les quatre sites au registre différent, la page affichait ses onglets et jamais de trajet. Ces règles se génèrent depuis `ITINERAIRES`, dans un `<style is:inline set:html={…}>`. Règle générale : **si une classe ou un sélecteur contient une valeur qui vit dans un registre, la règle se génère.**
2. **Aucun nombre ne s'écrit en lettres à la main.** « Deux trajets possibles », « les neuf intitulés » : faux sur quatre sites sur six. Un nombre se compte depuis le registre et se met en lettres par une table.
3. **L'opacité ne se pose jamais sur un parent dont un enfant doit rester plein.** La pastille Transports portait `opacity: .45` sur le fil ; le point mobile, qui est son `::after`, pâlissait avec lui et disparaissait à chaque cycle. Le fil et le véhicule sont deux couches. Et une boucle qui ramène l'opacité à 0 laisse, la moitié du temps, un pictogramme incomplet : **au repos, un signe doit déjà se lire.**
4. **La marge d'ancre tient compte du geste d'entrée.** Un bloc arrive translaté de `--mouv-y` et remonte en se posant : `scroll-padding-top` vaut donc `calc(6rem + var(--mouv-y))`, sinon la cible d'une ancre finit sous la barre.

Et une cinquième, d'écriture : **une réponse ne s'ouvre jamais sur une négation.** Ni « Non. », ni « Pas de ». Elle commence par ce qui est vrai. « Le cours accueille tous les âges d'adultes » remplace « Non, ce n'est pas réservé aux jeunes ».

### 13.10 LA PASSE PERSONA — ce qu'elle a trouvé, et ce qu'elle vérifie désormais
La passe se fait **sur le HTML livré**, aux trois largeurs — 1440, 1150 et 390 — et jamais sur le code source. Ce que le build accepte n'est pas ce qu'un visiteur voit.

Les trois défauts qu'elle a sortis le 2026-09-09, tous invisibles au build :
1. **La barre poussait la page.** Neuf entrées, la pastille et le téléphone demandaient 1 405 px dans une grille de 1 344 : au-dessus de 68rem, le téléphone sortait du conteneur et le document glissait de 20 px vers la droite. Règle : **l'espacement de barre se resserre avec la largeur, la barre porte `overflow-x: clip`, et la liste de liens n'apparaît qu'à partir de la largeur où elle tient en entier.**
2. **Le seuil du bouton menu doit être exactement celui de la liste.** Relever l'un sans l'autre ouvre une bande de largeurs sans aucune navigation. Un seuil, deux règles, jamais deux valeurs.
3. **Un arrêt de bus faux.** Cugnaux envoyait à « Route d'Espagne », qui est l'arrêt de Toulouse — huit arrêts au nord du club. L'arrêt du 61 route d'Espagne à Portet s'appelle **« Jean Jaurès »**, sur les trois sites qui y mènent. Règle : **un nom d'arrêt se relève sur la fiche de ligne, et il est le même sur tous les sites qui visent le même club.**

Ce que la passe mesure, à chaque livraison : contraste calculé de chaque nœud de texte contre son fond réel · cible de pointage sous 24 px (44 px sur téléphone) · débordement horizontal du document · bloc resté invisible après l'entrée · image sans `alt` ou sans dimensions · lien sans texte ou au libellé opaque · mesure de ligne au-delà de 92 caractères · titre ou `h1` dupliqué entre deux pages · saut de niveau de titre · lien interne mort · figure de style et formule creuse dans le texte visible.

### 13.11 CE QUE LE HATER A SORTI EN LISANT LES PAGES — et les deux règles de barre
La passe du 2026-09-09 s'est faite **sur l'expérience** — sept accueils lus comme un visiteur venu de Google, sur téléphone — et non sur le code. Ce qu'elle a trouvé, et ce qui est désormais loi :

**Sur le texte**
1. **Le héros ouvre la porte du club.** Sur les sept sites, le premier lien vers le club arrivait en section 2, après 60 à 316 mots. La séance d'essai est dans le héros, devant le moteur. Un site qui garde sans convertir est à moitié fait.
2. **Sept H1, cinq formulations du cahier des charges, aucun héros pareil.** *club de boxe proche de X* · *cours de boxe accessibles depuis X* · *club de MMA près de X* · *sports de combat à proximité de X* · *Boxing Center accueille les habitants de X dans ses clubs de…*. Chaque site en porte une dans son H1, le sujet et la formule changent d'un site à l'autre, et les quatre autres descendent dans ses sections. La cinquième nomme les villes des clubs : elle ne va qu'au site dont les deux clubs sont l'argument.
3. **Répéter, oui — recopier, jamais.** Un fait revient sous une forme nouvelle, attaché à une chose nouvelle : le chiffre dans le héros, la sensation dans « la salle », la preuve dans la FAQ. Six fois la même phrase, c'est du remplissage.
4. **Un décompte s'écrit depuis le registre ou ne s'écrit pas.** « Les neuf disciplines » vivait sur un site qui en publie quatorze — trente-quatre fois, cinq sites.
5. **Le bloc « la première fois » affirme.** « Tu frappes, et c'est tout » remplace « Tu ne combats pas ». Planter « humilié » pour dire qu'on ne le sera pas, c'est le planter.

**Sur la barre**
6. **Un calque fixe ne vit jamais dans un ancêtre filtré ou rogné.** `backdrop-filter` fait du header le bloc conteneur de tout `position: fixed` qu'il contient ; `overflow-x: clip` le rogne alors à la hauteur de la barre. Le panneau du menu est un frère du header, jamais son enfant.
7. **La barre mesure si elle tient, elle ne le devine pas.** Sept barres, sept longueurs de liste (811 px à Muret, 873 à Castelginest) : aucun seuil en rem ne convient à toutes. Au chargement et au redimensionnement, la barre compare la largeur de son contenu à celle de sa boîte ; si ça déborde, la liste cède au bouton menu. Le seuil CSS reste le plancher sans script. Et `min-width: 0` sur une liste dont les liens ne passent pas à la ligne ne fait que remplacer un débordement par un chevauchement.

### 13.12 UN SITE = L'ORDRE DE SES PROPRES QUESTIONS — la méthode, prouvée deux fois
Castelginest puis Muret ont été refaits selon la même méthode, et les deux pages ne se ressemblent pas. C'est le test : si l'ordre des sections de deux sites est le même, l'un des deux ment sur ses questions.

1. **L'ordre des sections est l'ordre des questions du visiteur**, telles qu'elles lui viennent quand il arrive de Google sur son téléphone. Quand il n'a plus de question, la page s'arrête. À Castelginest, « c'est où » et « j'y vais comment » sont deux questions (une adresse à Toulouse, deux bus et un métro) : deux sections. À Muret, un seul bus dépose dans la rue du club : une seule question, une seule section, qui s'ouvre avant 1,2 écran.
2. **Le dessin du héros vit sous le titre qu'il illustre.** Dans le héros, il coûtait un écran avant le premier mot sur le club. Il devient un composant (`LigneSoixante.astro`, `PlanEole.astro`) rendu dans sa section, en demi-écran sur téléphone. Le héros tient en moins d'un écran : H1, la promesse qui nomme le club, une ligne de cotes, deux boutons — la séance d'essai et l'ancre vers le dessin.
3. **Chaque section se referme sur une porte du club dont le libellé n'a pas encore servi.** Dix portes par page, dix libellés.
4. **Aucun titre de section n'est un titre d'un autre site de la famille.** La liste des titres pris est dans les commentaires d'en-tête de chaque `index.astro`.
5. **L'arrêt du club de Portet est « Jean Jaurès », sur la route d'Espagne — sur tous les sites.** Depuis Portet Gare SNCF, c'est le premier arrêt de la L5. « Route d'Espagne » est un arrêt de Toulouse, huit arrêts trop loin : il a été écrit deux fois (Cugnaux, Muret), et deux fois corrigé.
6. **Jamais une regex avec échappement à travers un script Python collé dans le shell.** `\b` y devient un caractère de retour arrière invisible, le motif ne matche jamais, et rien ne le signale. Une comparaison (`o.intitule === 'MMA'`), ou l'outil d'édition, jamais un heredoc.

### 13.13 — Tournefeuille refait, et ce que la lecture des fichiers frères a sorti (2026-09-10)

**La méthode, troisième preuve.** L'accueil de Tournefeuille suit l'ordre de ses propres questions : la thèse (héros, deux portes — la boxe thaï réserve à Saint-Cyprien, le MMA à Portet, le club lu dans `destinationUnique()` et jamais choisi) → la règle avec ses deux pièces (02, `#regle`, l'aiguillage sous son titre : 0,54 écran à 390 px) → le reste du planning et le tableau où la colonne vide désigne le club (03, `#cours`, familles partagées calculées par `clubsQuiProposent`) → le moteur (04) → le trajet, qui EST le choix de club (05) → le premier jour, le même sur les deux branches (06) → le cas par cas (07) → la règle tenue depuis Plaisance et Fonsorbes (08) → réserver chez le club de sa discipline (09). Neuf titres, aucun sur un autre site. Les portes « planning » et « appeler » suivent le club retenu par `[data-lien-club]` + `data-href-<club>` ; sans script, tout reste à Saint-Cyprien, le club desservi par le métro.

**Ce que la lecture ligne par ligne a sorti — et que ni le portillon ni la passe persona ne voyaient :**
- `transports.astro` de Tournefeuille portait les questions de Cugnaux (la 85, la 321, Frouzins) — visibles ET dans le JSON-LD FAQ. Réécrit depuis `itineraire()` et `CLUBS`.
- `llms.txt.ts` de Cugnaux était celui de Muret mot pour mot (« habitants de Muret », « 23 km par la route », Clément Ader). Réécrit depuis `SITE`, `DESTINATION`, `VILLE.figure`.
- `llms.txt.ts` de Castelginest et de L'Union citaient « la zone de Labège-Innopole » et « un étage de musculation… 22 cours par semaine » (Ramonville). Retirés.
- Les commentaires de code parlant de Muret dans les cinq autres sites (Seance, PiedDePage, ta-seance, premiere-seance) : à nettoyer site par site.

**Règles.** (1) Un fichier copié d'un site frère se relit ligne par ligne avant le premier commit ; le nom d'une autre ville du réseau dans `src/pages` ou `src/components` est un signal, sauf s'il vient de `LIMITROPHES` ou `COMMUNES`. (2) Un `llms.txt` se projette du registre (`SITE.ville`, `SITE.gentile`, `DESTINATION`, `VILLE`) : aucune ville, aucun chiffre, aucun fait local tapé. (3) À écrire dans `verifier.mjs` : un code de ligne (« la 85 », « ligne 321 », « Linéo L5 ») cité dans une page doit exister dans `transports.ts` ou dans `VILLE.bus`.

**Deux interdits d'Eddy, posés le 2026-09-10 (voir aussi la skill baffled-bar) :**
- Aucun trailer `Co-Authored-By` dans un commit : « claude » apparaissait comme contributeur GitHub avec douze commits. Le message se termine sur sa dernière phrase utile.
- Favicons, vignettes et métadonnées jamais identiques. Constat : les sept `favicon.svg` avaient le même md5 ; l'`og:image` de chaque page était une photo de salle partagée. Mise en œuvre sur Tournefeuille, à répliquer sur les six autres : `public/favicon.svg` au signe du site (l'aiguillage), `src/data/teinte.ts` (les couleurs de `jetons.css` lisibles au build), `src/pages/og/[page].png.ts` (satori + @resvg/resvg-js, polices TTF dans `src/og/fonts/`, une vignette 1200 × 630 par route : titre avec le lieu en couleur, description, le dessin du site, les deux clubs, le domaine), `Base.astro` → `og:image = /og/{id}.png`, `og:image:width/height/alt`, `twitter:image`, `theme-color = TEINTE.papier`, `primaryImageOfPage = photo`. `personas.mjs` refuse désormais un favicon partagé entre deux sites, une page sans vignette propre, deux pages avec la même vignette.

**Outils.** Le Bash de session tronque une commande longue (vers 7 Ko) : un fichier de plus de 150 lignes s'écrit avec l'outil d'écriture, jamais par heredoc. Dans le navigateur intégré, `window.scrollTo` n'agit pas ; la molette (`scroll`) oui ; `scroll_to` par repère défile mais les blocs ne se révèlent pas toujours à temps pour la capture — mesurer au JavaScript, regarder à la molette.

### 13.14 — Les demandes du patron tenues, et ce que la journée a fixé (2026-09-10, suite)

**Les contacts décidés par le client.** Les sites qui renvoient au club de Portet (Muret, Cugnaux, et la branche Portet de Tournefeuille et de Colomiers) affichent `09 56 65 37 82` et `boxingcenterportet@gmail.com` ; tous les autres (Tournefeuille côté Saint-Cyprien, Labège, L'Union, Castelginest, Colomiers) `09 39 03 67 48` et `boxingcenter31@gmail.com`. Le numéro vit dans `CONTACT` (source `cahier-des-charges`, helper `CDC`) et dans `CLUBS[].telephone` ; les descriptions de la page contact le lisent aussi. Les anciens numéros des sites de club ne s'affichent plus nulle part. **La destination des formulaires se règle dans le tableau de bord Inlet** (inlett.vercel.app, aucune API d'administration, aucun serveur MCP) : chaque site a son `FORM_ID` dans `SITE.formulaire`, l'adresse de notification est à changer là-bas, par Eddy.

**Le club des États-Unis a son vrai site : clubmma.fr.** `site`, `activites` (/disciplines/), `plannings` (/planning/), `tarifs` (/abonnements/), horaires publiés (accès libre 10h–21h15, six jours sur sept ; les cours sur trois plannings Boxe, Fitness, MMA & Sol), et le graphe des disciplines relevé sur clubmma.fr : Boxe Anglaise, Pieds-Poings / Kick, Full Contact, Muay Thai, MMA (cage officielle, 400 m² de tatamis), Grappling, Jiu-Jitsu Brésilien, Lady Punch, Hyrox, Boxing HIIT, Cross-Training, Street Workout, Accès libre, École de boxe (3/6, 7/11, 12/16 ans), MMA jeunes (10/16 ans). « Travail au Sol » et le « groupe compétiteurs amateurs » venaient de l'ancien site : sortis. Les pages MMA (« Club MMA et grappling », « salle de MMA près de … ») et pieds-poings (« Club de kick-boxing et de boxe thaï ») sont réécrites sur L'Union et Castelginest ; la barre dit « MMA ».

**Les neuf motifs du patron, vérifiés par script.** `scratchpad/audit_patron.py` (à verser dans `boxing-center-colomiers/scripts/`) lit les six builds : chaque motif (ville et communes), la page qui le porte et la balise (title, h1, h2, h3, description, ou texte seul), les pages communes (existence, index, sitemap, lien depuis l'accueil), les sorties vers le club (domaine attendu), les téléphones et mails. Règle de lecture : un motif est couvert quand ses mots se suivent avec au plus quatre mots libres entre eux dans un titre, un H1, un H2, un H3 ou une description — les formulations « près de », « proche de », « à proximité de », « accessibles depuis » comptent. Le singulier « sport de combat » est placé une fois par site, relié à la ville (« un club de sport de combat complet, proche de X »). Les motifs « club boxe thaï » et « club kick boxing » vivent dans le H1 et le titre de la page pieds-poings de chaque site, et dans une question quand le club ne publie pas la thaï (Cugnaux, Labège : on dit ce qui est publié, et où la thaï se pratique dans le réseau).

**Vignettes et favicons, sept fois.** `scratchpad/equiper_og.py <site>` équipe un satellite en une commande (polices, `teinte.ts` lu dans `jetons.css`, l'endpoint avec LE dessin du site, `favicon.svg`, `Base.astro`) ; `equiper_colomiers.py` fait de même pour le site sombre, sur l'encre. Les sept favicons sont distincts (l'aiguillage, l'Éole, la limite, le terminus, le plan de la salle, la ligne 60, l'origine). Toute étiquette trop longue déborde : les noms de club longs se raccourcissent (`nomCourt`), les codes de ligne se posent en pastille sur le trait, le pied de carte est en 15 px avec le domaine insécable.

**La méthode, cinquième et sixième preuves.** Labège (le lieu → le trajet avec le terminus sous son titre → le secteur → le midi de l'Innopole → le moteur → la première fois → huit questions → décider ; héros 0,86 écran, plan 0,56) et L'Union (la salle avec son plan sous le titre → ce qui se pratique par espace → le moteur → le trajet → le premier jour → le cas par cas → le secteur → décider ; héros 0,87, plan 0,52). Six accueils sur sept suivent l'ordre de leurs propres questions ; Colomiers reste sur son ancien squelette, avec un H2 qui s'ouvre sur une négation à corriger.

**Le plan 5× et le Workflow.** L'audit lancé en workflow est mort au plafond de session, sept agents sur sept, 516 000 jetons, résultat vide. Sur ce compte, jamais de Workflow, même sous « ultracode » : un audit se fait par script, un chantier site par site. Le Bash de session tronque une commande longue (vers 7 Ko) et transforme les échappements d'un heredoc : les gros fichiers s'écrivent avec l'outil d'écriture, les retouches ciblées avec l'outil d'édition.

### 13.15 — Le référencement mesuré, et ce qui l'empêchait (2026-09-12)

**Ligne de base Google (gl=fr, non localisé)** : club mma l'union #4 · club mma muret #5 · club de boxe tournefeuille #6 · club de boxe labege #6 ; absents de la page 1 : club de boxe muret, boxe muret, club de boxe cugnaux, salle mma cugnaux, club de boxe castelginest, club de boxe colomiers. Toutes les pages sont indexées : le problème est le classement, pas l'indexation.

**Ce qui l'empêchait, trouvé en lisant les domaines en ligne :**
1. **IndexNow mort sur six sites.** `scripts/indexnow.mjs` avait été copié de Colomiers : HOTE = colomiers, aucun fichier de clé. Bing, et avec lui ChatGPT et Copilot, n'a jamais été prévenu. Règle : HOTE se lit dans `verite.ts`, chaque domaine a sa clé dans `public/<clé>.txt`, et on ne soumet qu'après avoir lu la clé en ligne.
2. **Les doublons entre sites.** Deux sites qui visent le même club écrits avec les mêmes phrases : Google en garde un et replie l'autre. L'Union ↔ Castelginest partageaient 59 à 66 % de leurs phrases, 82 à 91 % sur les pages de discipline ; première séance, contact et ta séance étaient copiés à 84-100 % partout. Règle : une page indexable partage moins d'un tiers de ses phrases avec un site frère (mesure `doublons.py`, liste de travail `phrases_partagees.py`) ; une page qui ne peut pas être propre à sa ville passe en noindex, follow.
3. **Le favicon servi à Google était `logo.png`**, 201 × 94, découpé en rond. Règle : pastille carrée, ronde-sûre, code de la ville (CO, MU, CU, TO, LA, LU, CA), ICO + PNG 16→512 + apple-touch + manifest, `scripts/favicons.mjs`.
4. **La vignette du résultat était une carte de texte pâle.** Google la recadre en carré au centre et l'affiche vers 100 px. Règle : la photo de la page, la teinte du site, le lieu énorme au centre ; deux formats (1200 × 630 pour les partages, 1200 × 1200 annoncé en `primaryImageOfPage`) ; `max-image-preview:large`.
5. **Colomiers répond sans www** (200 sur l'apex) : réglage Vercel Domains à faire par Eddy.

**Le plafond, dit honnêtement.** À Muret, Cugnaux et Castelginest, un vrai club est installé dans la ville, avec sa fiche Maps et ses annuaires ; un concurrent à domaine ancien publie une page par ville. La page 1 se gagne ; la première place au-dessus du club local ne se promet pas. Les leviers qui la rendent possible sortent du code : Search Console et Bing Webmaster sur les sept domaines, des liens depuis les sites des clubs vers leurs satellites, la publicité Google que Portet fait déjà, étendue aux mots-clés satellites.

**Moteurs de réponse.** ChatGPT lit l'index d'OpenAI et Bing, Claude lit Brave, Perplexity son propre robot, Gemini l'index Google. Les sept domaines répondent 200 à chacun (testé par UA) ; robots.txt les nomme ; llms.txt porte un bloc « Réponses courtes » écrit depuis le registre — les questions telles qu'on les pose, la réponse avec le nom, l'adresse et la ligne. Un résumé de trajet qui s'ouvre sur un pronom (« Elle part de la gare… ») perd son sens hors de la page : le gabarit remplace le pronom par le nom de la ligne.

**Outils.** `lot_famille.py <site>` applique le lot (vignette, favicons, layout, robots, IndexNow, noindex) ; son motif de noindex s'arrête au premier « id: » suivant — sans cette borne, un second passage avait noindexé la page transports de Muret. `audit_patron.py`, `doublons.py`, `phrases_partagees.py`, `diag_live.py`, `rang.py` (Bing et DuckDuckGo renvoient des pages de défi aux scripts : le classement se lit à la main dans Google).

### 13.16 — Une phrase, un site (2026-09-12, soir)

**Le constat.** `partage_source.py` ne lisait que les chaînes entre apostrophes simples : les contenus de Muret et de Cugnaux, écrits entre guillemets doubles, lui échappaient presque entièrement. Corrigé, il a compté 141 phrases de discipline présentes sur au moins deux sites. Muret et Cugnaux reprenaient Colomiers mot pour mot (boxe anglaise : 23 et 24 phrases ; MMA de Muret : 13). Tournefeuille, Labège et L'Union partageaient un même gabarit, jusqu'à 22 phrases par page.

**La règle.** Une phrase de discipline de six mots ou plus, ville neutralisée, n'existe que sur un site. Colomiers, l'origine, garde les siennes ; un satellite réécrit ce qu'il partage avec l'origine ; entre deux satellites, un seul réécrit. Exemptés : les titres-mots-clés (H1, questions du type « Où est la salle MMA la plus proche de X ? »), où la ville change et qui portent la requête. Une réécriture garde les ids, les H1, les photos et tout titre qui nomme la ville (`remplacer_contenus2.py` refuse d'écrire sinon), et part des faits du club : la 79 et l'octogone de sept mètres à Ramonville ; les deux rings, la cage surélevée, les seize sacs et le MMA jeunes avenue des États-Unis.

**Résultat.** 141 phrases partagées, puis 11, dont 6 titres-mots-clés ; les 5 autres réécrites. Au passage : la FAQ « pas en forme » de Muret répétait sa dernière phrase ; les âges de l'École de boxe de L'Union différaient d'une page à l'autre.

**Ce que les moteurs voient (relevé du 2026-09-12).** Les sept domaines portent déjà un code `google-site-verification` dans leur zone DNS chez OVH : la Search Console est vérifiée, reste à savoir sur quel compte Google. Brave, l'index de Claude, n'a encore aucune page des satellites : soumission à la main sur search.brave.com/submit-url, et des liens depuis des pages déjà indexées. Aucun site de club (boxingcenter.fr, boxing-center-portet.fr, clubmma.fr, mmatoulouse.com, club-boxe-toulouse.com, boxe-toulouse.com) ne pointe vers un satellite. Bing ne sort encore aucun satellite en page 1 sur « club de boxe muret » ni « club mma l'union ».

**Outils.** `partage_source.py` lit les deux styles de chaîne ; `retouches.py` remplace une phrase exacte présente une seule fois, sinon n'écrit rien ; `remplacer_contenus2.py` remplace le tableau entier sous garde. Le Bash de session réduit une double barre oblique à une seule dans un heredoc, et casse les longs blocs à apostrophes typographiques : un chemin s'écrit avec `os.path.join`, un contenu avec l'outil d'écriture.

### 13.17 — On ne fait que monter : mesurer avant de réécrire (2026-09-13)

**La règle d'Eddy.** « Si ces textes sont la raison pour laquelle le référencement est bon, on ne les modifie pas. On ne fait que monter, jamais descendre. » Avant toute réécriture, on relève quelle URL tient quel rang ; une page qui sort en page 1 sur sa requête garde ses textes, même partagés.

**Le relevé du 2026-09-13 (Google, lu par Startpage).** Google oppose un contrôle anti-robot au navigateur de session : on ne le contourne pas, on lit les mêmes résultats par Startpage. Treize requêtes « club de boxe <commune> » : une seule page de commune classée, `boxingcenter-labege.fr/saint-orens-de-gameville/` (10e). « club mma l'union » : l'accueil de L'Union (5e), pas la page MMA. « club de boxe rouffiac-tolosan » : l'accueil de L'Union (7e). Les communes de Castelginest, Cugnaux et Tournefeuille ne sont pas classées ; boxingcenter.fr, le site du réseau, sort souvent entre la 2e et la 5e place.

**Ce qui a été retouché.** Les gabarits `PageCommune.astro` de L'Union, Castelginest, Cugnaux et Tournefeuille ont chacun leur micro-copie (titres de section, chapeaux, note de carte, bloc « Décider ») ; Labège garde la sienne, parce que Saint-Orens tient la page 1. Castelginest a ses propres réponses de légende (elles étaient celles de L'Union mot pour mot) ; Cugnaux aussi (identiques à Tournefeuille). Les descriptions de cours d'`offres.ts` sont réécrites sur Castelginest et Cugnaux seulement : Muret, Labège, L'Union et Tournefeuille ont un accueil classé et gardent les leurs. Jamais touchés : le H1 « Club de boxe et MMA à proximité de … », les recherches de la légende, les URL, les photos (`communes_retouches.py` refuse d'écrire sur Labège et sur toute chaîne absente ou doublée).

**Un fait corrigé.** La légende de L'Union disait que la salle publie « la boxe pieds-poings et le full contact » et renvoyait la thaï au réseau, alors que clubmma.fr publie le Muay Thai : la réponse le dit désormais.

**Les sites de club.** Portet (`boxing-center-portet`) et Ramonville (`bc-ramonville`) portent un travail non publié daté du 2026-09-03 (40 fichiers chacun) : attribution des auteurs du site, serveur MCP, llms, robots. Rien n'y est touché sans la décision d'Eddy. Le lien discret vers les satellites se pose, le jour venu, dans le pied de page cuit au build (Portet : `seoBakePlugin` de `vite.config.ts` et `footerMarkup` de `src/layout.ts` ; Ramonville : `scripts/maillage.mjs`) — un lien injecté seulement par JavaScript n'est pas lu par Bing ni par les robots des moteurs de réponse. Minimes, États-Unis et Saint-Cyprien sont hors périmètre jusqu'à nouvel ordre d'Eddy ; Blagnac est tenu par une autre session.
