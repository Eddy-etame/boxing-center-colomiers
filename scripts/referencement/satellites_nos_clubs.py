# -*- coding: utf-8 -*-
"""
« Nos clubs » sur les 7 sites de proximité (Eddy, 13/09 : une page dans la
navigation de chaque site, les 5 salles avec le lien vers leur vrai site — pas
les sites de proximité).

Tout passe par le registre : la route (navigation, pied de page, vignette) +
l'étiquette de vignette + la page. La route est `index: false` : les adresses
des cinq clubs sont les mêmes d'un site à l'autre, et la famille a déjà mis
hors index les pages qui se ressemblaient à 84–100 % (contact, première séance,
ta séance — 12/09). Hors index, mais liens suivis : le visiteur et les robots
vont aux cinq vrais sites. Aucune tournure négative, aucune « salle à <ville> ».
Rejouable ; fins de ligne du dépôt conservées.
"""
import io, os, sys
sys.stdout.reconfigure(encoding='utf-8')
DEP = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment')
VILLES = {'colomiers': 'Colomiers', 'muret': 'Muret', 'cugnaux': 'Cugnaux', 'tournefeuille': 'Tournefeuille',
          'labege': 'Labège', 'lunion': 'L’Union', 'castelginest': 'Castelginest'}
SITES = sys.argv[1:] or list(VILLES)

PAGE = """---
/**
 * NOS CLUBS (Eddy, 13/09) — les cinq clubs Boxing Center, chacun vers SON
 * site. Page de navigation : les adresses sont les mêmes sur les sept sites
 * de proximité, elle reste donc hors index (route `index: false`) — ses liens
 * vers les cinq clubs, eux, sont suivis.
 */
import Base from '../layouts/Base.astro';
import { CONTACT } from '../data/verite';
import { route } from '../data/routes';
import { VILLE_SITE } from '../data/vignettes';

const RESEAU = [
  { nom: 'Boxing Center Portet-sur-Garonne', lieu: 'Route d’Espagne', adresse: "61 route d'Espagne, 31120 Portet-sur-Garonne", site: 'https://boxing-center-portet.fr/' },
  { nom: 'Boxing Center Toulouse Minimes', lieu: 'Quartier Minimes', adresse: '12 rue de Fenouillet, 31200 Toulouse', site: 'https://boxe-toulouse.com/' },
  { nom: 'Boxing Center Toulouse États-Unis', lieu: 'Avenue des États-Unis', adresse: '388 avenue des États-Unis, 31200 Toulouse', site: 'https://clubmma.fr/' },
  { nom: 'Boxing Center Toulouse Saint-Cyprien', lieu: 'Rive gauche', adresse: '11 rue Sainte-Lucie, 31300 Toulouse', site: 'https://club-boxe-toulouse.com/' },
  { nom: 'Boxing Center Ramonville', lieu: 'Terminus du métro B', adresse: '33 rue des Ormes, 31520 Ramonville-Saint-Agne', site: 'https://mmatoulouse.com/' },
];
---

<Base page="nos-clubs">
  <section class="section tete" aria-labelledby="t-clubs">
    <div class="enveloppe tete__inner">
      <nav class="fil mono" aria-label="Fil d’Ariane">
        <a href="/">Accueil</a><span aria-hidden="true">/</span>
        <span aria-current="page">Nos clubs</span>
      </nav>
      <h1 id="t-clubs">Nos cinq clubs, accessibles depuis {VILLE_SITE}</h1>
      <p class="tete__chapeau">
        Cinq adresses du réseau Boxing Center autour de Toulouse. Chacune a son site,
        ses plannings, ses tarifs et ses coachs&nbsp;: choisis celle qui tombe sur ton
        trajet — un clic et tu y es.
      </p>
    </div>
  </section>

  <section class="section reseau" aria-label="Les cinq clubs Boxing Center">
    <div class="enveloppe">
      <div class="reseau__grille">
        {RESEAU.map((c) => (
          <article class="rclub">
            <p class="rclub__lieu mono">{c.lieu}</p>
            <h2 class="rclub__nom"><a href={c.site} rel="noopener">{c.nom}</a></h2>
            <p class="rclub__adresse">{c.adresse}</p>
            <a class="bouton rclub__site" href={c.site} rel="noopener"><span>Le site du club</span><span class="fleche" aria-hidden="true">↗</span></a>
          </article>
        ))}
      </div>
    </div>
  </section>

  <section class="section conversion" aria-labelledby="t-viser">
    <div class="enveloppe conversion__inner">
      <p class="numero-section mono"><span>Lequel viser</span></p>
      <h2 id="t-viser">Lequel viser depuis {VILLE_SITE}&nbsp;?</h2>
      <p class="lead conversion__texte">
        Donne-nous ta discipline et ton créneau&nbsp;: on te répond avec le club qui
        colle vraiment à ta semaine.
      </p>
      <div class="conversion__actions">
        <a class="bouton bouton--signal" href={route('contact').chemin}><span>Poser ma question</span><span class="fleche" aria-hidden="true">→</span></a>
        <a class="bouton" href={`tel:${CONTACT.telephoneLien.valeur}`}><span>{CONTACT.telephone.valeur}</span><span class="fleche" aria-hidden="true">↗</span></a>
      </div>
    </div>
  </section>
</Base>

<style>
  .tete__inner { max-width: 60rem; }
  .fil { display: flex; gap: var(--e-2); margin-bottom: var(--e-5); }
  .fil a { color: var(--acier-sombre); text-decoration: none; }
  .fil a:hover { color: var(--signal-texte); }
  .fil span[aria-current] { color: var(--acier); }
  .tete h1 { max-width: 20ch; margin-bottom: var(--e-5); }
  .tete__chapeau { max-width: 60ch; padding-left: var(--e-5); border-left: 2px solid var(--signal); font-size: var(--t-lead); line-height: 1.5; color: var(--acier); }

  /* Cinq cartes, jamais une seule sur sa rangée : 2 + 3 sur grand écran,
     2 + 2 + une pleine largeur sur tablette, une colonne sur téléphone. */
  .reseau__grille { display: grid; grid-template-columns: repeat(6, 1fr); gap: var(--e-5); }
  .rclub { grid-column: span 2; display: grid; align-content: start; gap: var(--e-3); padding: var(--e-6); border: 1px solid var(--trait); border-radius: var(--rayon-1); }
  .rclub:nth-child(-n + 2) { grid-column: span 3; }
  @media (max-width: 60rem) {
    .reseau__grille { grid-template-columns: 1fr 1fr; }
    .rclub, .rclub:nth-child(-n + 2) { grid-column: span 1; }
    .rclub:last-child { grid-column: span 2; }
  }
  @media (max-width: 36rem) {
    .reseau__grille { grid-template-columns: 1fr; }
    .rclub:last-child { grid-column: span 1; }
  }
  .rclub__lieu { color: var(--signal-texte); font-size: var(--t-petit); letter-spacing: 0.08em; text-transform: uppercase; }
  .rclub__nom { font-size: var(--t-h3); line-height: 1.15; }
  .rclub__nom a { color: inherit; text-decoration: none; }
  .rclub__nom a:hover { color: var(--signal-texte); }
  .rclub__adresse { color: var(--texte-faible); font-size: var(--t-petit); }
  .rclub__site { justify-self: start; margin-top: var(--e-2); }

  .conversion { background: var(--marine); }
  .conversion__inner { max-width: 46rem; }
  .conversion h2 { max-width: 24ch; margin-bottom: var(--e-5); }
  .conversion__texte { max-width: 50ch; color: var(--acier); }
  .conversion__actions { display: flex; flex-wrap: wrap; gap: var(--e-3); margin-top: var(--e-7); }
</style>
"""


def lire(p):
    return io.open(p, encoding='utf-8', newline='').read()


def ecrire(p, t):
    io.open(p, 'w', encoding='utf-8', newline='').write(t)


for s in SITES:
    R = os.path.join(DEP, f'boxing-center-{s}')
    ville = VILLES[s]
    # 1. le registre des routes
    p = os.path.join(R, 'src', 'data', 'routes.ts')
    t = lire(p)
    nl = '\r\n' if '\r\n' in t else '\n'
    if "'nos-clubs'" not in t:
        a = f"  | 'contact'{nl}"
        assert t.count(a) == 1, (s, 'union')
        t = t.replace(a, f"  | 'nos-clubs'{nl}" + a)
        b = f"  {{{nl}    id: 'contact',"
        assert t.count(b) == 1, (s, 'route contact')
        entree = nl.join([
            "  {",
            "    id: 'nos-clubs',",
            "    chemin: '/nos-clubs/',",
            "    nav: 'Nos clubs',",
            "    question: 'Où sont les cinq clubs Boxing Center, et quel est le site de chacun ?',",
            f"    titre: 'Nos 5 clubs de boxe près de {ville} | Boxing Center',",
            "    description:",
            f"      'Portet-sur-Garonne, Minimes, États-Unis, Saint-Cyprien et Ramonville : les cinq clubs Boxing Center autour de {ville}, leur adresse et le lien vers leur site.',",
            "    menu: true,",
            "    // hors index : mêmes adresses sur les sept sites de proximité ; liens suivis",
            "    index: false,",
            "  },",
        ]) + nl
        t = t.replace(b, entree + b)
        ecrire(p, t)
    # 2. l'étiquette de la vignette
    p = os.path.join(R, 'src', 'data', 'vignettes.ts')
    t = lire(p)
    nl2 = '\r\n' if '\r\n' in t else '\n'
    if "'nos-clubs'" not in t:
        a = "  contact: 'Contact',"
        assert t.count(a) == 1, (s, 'sujets')
        t = t.replace(a, "  'nos-clubs': 'Nos 5 clubs'," + nl2 + a)
        ecrire(p, t)
    # 3. la page
    p = os.path.join(R, 'src', 'pages', 'nos-clubs.astro')
    ecrire(p, PAGE.replace('\n', nl))
    print(f'  ok {s} ({ville})')
