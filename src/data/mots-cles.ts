/**
 * REGISTRE DES MOTS-CLÉS — le territoire de recherche, page par page.
 *
 * Principe directeur : **plus de pertinence Colomiers PAR page, pas plus de
 * pages Colomiers.** Fabriquer /club-boxe-colomiers/, /boxe-colomiers/,
 * /sport-combat-colomiers/ à côté des routes existantes nous rapprocherait du
 * schéma de page satellite que Google sanctionne explicitement. On garde les
 * huit pages du cahier des charges, plus deux pages d'intention distinctes
 * (/premiere-seance/, /quel-club/) qui répondent à des questions qu'aucune
 * autre page ne peut porter sans se diluer — et on rend chacune beaucoup plus
 * dense et beaucoup plus spécifique.
 *
 * Deuxième principe : un mot-clé n'entre dans une page que s'il correspond à
 * une question qu'on y traite réellement. Un mur de « Colomiers » répété est
 * une sur-optimisation, et le cahier des charges §4 l'interdit lui-même
 * (« de manière naturelle, sans sur-optimisation excessive »).
 *
 * Le contrôle qualité vérifie que chaque page couvre effectivement ses
 * mots-clés prioritaires dans son texte visible. Une page qui perd son
 * territoire fait échouer le build.
 */

import type { RouteId } from './routes';

export type Cluster = {
  page: RouteId;
  /** Les expressions que la page DOIT porter. Vérifiées au build. */
  prioritaires: readonly string[];
  /** Les expressions qu'elle gagne à porter, sans obligation. */
  secondaires: readonly string[];
};

/* ─────────────────────  LE TERRITOIRE GÉOGRAPHIQUE  ───────────────────── */

/**
 * Le cahier des charges §1 vise « les prospects situés à Colomiers ET dans
 * les communes voisines ». Ces communes sont un territoire de recherche
 * entier — quelqu'un de Cornebarrieu ou de Pibrac cherche exactement la même
 * chose, avec le même trajet, et ne tape pas « Colomiers ».
 *
 * Tournefeuille, Plaisance-du-Touch et Cugnaux en sont sorties le 2026-09-09 :
 * elles ont chacune leur propre site dans la famille, et deux sites qui visent
 * la même commune se prennent des places l'un à l'autre.
 *
 * On ne fabrique pas une page par commune : ce serait l'usine à pages-villes.
 * On les nomme dans le contenu de l'accueil, là où c'est utile au lecteur,
 * et dans `areaServed` des données structurées, là où c'est utile au robot.
 */
export type Commune = { nom: string; cp: string; situation: string };

export const COMMUNES_VOISINES: readonly Commune[] = [
  { nom: 'Blagnac', cp: '31700', situation: 'au nord-est, vers l’aéroport' },
  { nom: 'Cornebarrieu', cp: '31700', situation: 'au nord' },
  { nom: 'Pibrac', cp: '31820', situation: 'à l’ouest' },
  { nom: 'Léguevin', cp: '31490', situation: 'à l’ouest, après Pibrac' },
  { nom: 'Brax', cp: '31490', situation: 'à l’ouest' },
  { nom: 'Mondonville', cp: '31700', situation: 'au nord' },
  { nom: 'Aussonne', cp: '31840', situation: 'au nord' },
] as const;

/** Le vocabulaire géographique que le site doit établir naturellement. */
export const CONTEXTE_GEO = {
  ville: 'Colomiers',
  codePostal: '31770',
  departement: 'Haute-Garonne',
  numeroDepartement: '31',
  secteur: 'ouest toulousain',
  agglomeration: 'agglomération toulousaine',
  gentile: 'Columérins',
} as const;

/* ─────────────────────────  LES CLUSTERS  ───────────────────────── */

export const CLUSTERS: readonly Cluster[] = [
  {
    page: 'accueil',
    prioritaires: [
      'club de boxe',
      'Colomiers',
      'MMA',
      'sports de combat',
      'Haute-Garonne',
    ],
    secondaires: [
      'club de boxe à Colomiers',
      'club de boxe près de Colomiers',
      'boxe Colomiers',
      'club MMA Colomiers',
      'club MMA près de Colomiers',
      'sport de combat Colomiers',
      'cours de boxe Colomiers',
      'salle de boxe près de Colomiers',
      'boxe anglaise Colomiers',
      'boxing fitness Colomiers',
      'boxe enfant Colomiers',
      'boxe débutant Colomiers',
      '31770',
      'ouest toulousain',
      'agglomération toulousaine',
      'Blagnac',
      'Cornebarrieu',
      'Pibrac',
    ],
  },
  {
    page: 'boxe-anglaise',
    prioritaires: ['boxe anglaise', 'Colomiers', 'débutant'],
    secondaires: [
      'boxe anglaise Colomiers',
      'cours de boxe Colomiers',
      'club de boxe Colomiers',
      'boxe loisir',
      'boxe compétition',
      'boxe pieds-poings',
      'kick-boxing',
      'boxe débutant Colomiers',
      'apprendre à boxer',
      'cours de boxe adulte',
    ],
  },
  {
    page: 'mma',
    prioritaires: ['MMA', 'Colomiers', 'grappling', 'Portet-sur-Garonne'],
    secondaires: [
      'club MMA Colomiers',
      'cours MMA Colomiers',
      'MMA débutant Colomiers',
      'club MMA près de Colomiers',
      'grappling Colomiers',
      'jiu-jitsu brésilien',
      'JJB Colomiers',
      'cage MMA',
      'kick-boxing Colomiers',
      'sport de combat Colomiers',
    ],
  },
  {
    page: 'boxing-fitness',
    prioritaires: ['boxing fitness', 'Colomiers', 'cardio boxing', 'femme'],
    secondaires: [
      'boxing fitness Colomiers',
      'cardio boxing Colomiers',
      'boxe femme Colomiers',
      'Boxing Lady',
      'Lady Boxing',
      'boxe sans combat',
      'boxe sans opposition',
      'remise en forme',
      'reprendre le sport',
      'préparation physique',
      'cross training',
    ],
  },
  {
    page: 'boxe-enfants',
    prioritaires: ['boxe enfant', 'Colomiers', 'boxe éducative', 'Baby Boxe'],
    secondaires: [
      'boxe enfant Colomiers',
      'cours de boxe enfant Colomiers',
      'Baby Boxe Colomiers',
      'boxe éducative Colomiers',
      'boxe ado Colomiers',
      'sport de combat enfant',
      'boxe 3 ans',
      'boxe adolescent',
      'kick-boxing enfants',
    ],
  },
  {
    page: 'plannings',
    prioritaires: ['planning', 'horaires', 'Colomiers', 'créneau'],
    secondaires: [
      'planning boxe Colomiers',
      'horaires boxe Colomiers',
      'planning MMA Colomiers',
      'horaires club de boxe',
      'cours du soir',
      'cours le midi',
      'boxe le samedi',
    ],
  },
  {
    page: 'tarifs',
    prioritaires: ['tarif', 'Colomiers', 'adhésion'],
    secondaires: [
      'tarif boxe Colomiers',
      'prix club de boxe Colomiers',
      'prix MMA Colomiers',
      'combien coûte la boxe',
      'abonnement boxe',
      'licence',
      'cours d’essai',
    ],
  },
  {
    page: 'premiere-seance',
    prioritaires: ['première séance', 'Colomiers', 'débutant', 'essai'],
    secondaires: [
      'première séance boxe Colomiers',
      'cours d’essai boxe Colomiers',
      'boxe débutant Colomiers',
      'commencer la boxe',
      'essayer le MMA',
      'séance découverte',
      'jamais fait de boxe',
      'cours de boxe débutant',
    ],
  },
  {
    page: 'quel-club',
    prioritaires: ['Minimes', 'Portet', 'Colomiers', 'club'],
    secondaires: [
      'quel club de boxe Colomiers',
      'Minimes ou Portet',
      'club de boxe proche de Colomiers',
      'Boxing Center Colomiers',
      'Boxing Center Minimes',
      'Boxing Center Portet',
    ],
  },
  {
    page: 'contact',
    prioritaires: ['Colomiers', 'contact'],
    secondaires: [
      'club de boxe près de Colomiers',
      'cours d’essai boxe Colomiers',
      'première séance',
      'essayer la boxe',
      'inscription boxe Colomiers',
    ],
  },
] as const;

export const cluster = (page: RouteId): Cluster | undefined =>
  CLUSTERS.find((c) => c.page === page);
