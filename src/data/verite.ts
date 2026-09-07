/**
 * REGISTRE DE VÉRITÉ — la seule source de faits du site.
 *
 * Chaque fait est écrit ici UNE fois, puis projeté dans le HTML, les
 * métadonnées, le JSON-LD, le formulaire et les recommandations.
 * Aucun composant n'a le droit d'écrire un horaire, un téléphone ou une
 * adresse en dur.
 *
 * `source` dit d'où vient le fait. Rien n'est publié sans source.
 */

export type Source = 'cahier-des-charges' | 'site-reseau' | 'a-verifier';

export type Fait<T> = {
  valeur: T;
  source: Source;
  /** date de dernière vérification, ISO */
  verifie: string;
};

const CDC = (v: string) => ({ valeur: v, source: 'cahier-des-charges' as const, verifie: '2026-09-07' });

/* ─────────────────────────────  IDENTITÉ  ───────────────────────────── */

export const SITE = {
  /** Le domaine de production. */
  origine: 'https://www.boxingcenter-colomiers.fr',
  nom: 'Boxing Center — depuis Colomiers',
  nomCourt: 'Boxing Center Colomiers',
  langue: 'fr-FR',
  /**
   * IMPORTANT — ce site ne représente PAS une salle physique à Colomiers.
   * Colomiers est le point de départ du visiteur, jamais une adresse de club.
   */
  villeOrigine: 'Colomiers',
  departement: 'Haute-Garonne',
} as const;

/* ─────────────────────────────  CONTACT  ───────────────────────────── */

export const CONTACT = {
  telephone: CDC('05 62 24 46 82'),
  /** format tel: pour les liens */
  telephoneLien: CDC('+33562244682'),
  email: CDC('bc.combat31@gmail.com'),
} as const;

/* ─────────────────────────────  HORAIRES  ───────────────────────────── */

export const HORAIRES = {
  /** Cahier des charges §8 et §10. */
  texte: CDC('6 jours sur 7, de 10h à 21h15'),
  ouverture: CDC('10:00'),
  fermeture: CDC('21:15'),
  joursParSemaine: 6,
  /** Les arguments que le cahier des charges §10 demande de porter. */
  arguments: [
    'Grande amplitude horaire',
    'Tu viens quand tu peux',
    'Compatible avec un travail, des études, une famille',
    'Un rythme régulier reste tenable',
  ],
} as const;

/* ─────────────────────────────  LES CLUBS  ───────────────────────────── */

export type Club = {
  id: 'minimes' | 'portet';
  nom: string;
  nomCourt: string;
  ville: string;
  /** site officiel du club — cahier des charges §9 */
  site: string;
  /** ce que le club apporte à quelqu'un qui part de Colomiers */
  angle: string;
  /** direction depuis Colomiers, en langage humain, sans distance inventée */
  depuisColomiers: string;
};

export const CLUBS: readonly Club[] = [
  {
    id: 'minimes',
    nom: 'Boxing Center Toulouse Minimes',
    nomCourt: 'Toulouse Minimes',
    ville: 'Toulouse',
    site: 'https://boxe-toulouse.com/',
    angle: "Le club urbain, dans Toulouse, sur l'axe nord — le plus direct quand tu rentres du travail.",
    depuisColomiers: "En allant vers Toulouse, direction nord-est.",
  },
  {
    id: 'portet',
    nom: 'Boxing Center Portet-sur-Garonne',
    nomCourt: 'Portet-sur-Garonne',
    ville: 'Portet-sur-Garonne',
    site: 'https://boxing-center-portet.fr/',
    angle: "Le club au sud de l'agglomération, facile d'accès en voiture et à se garer.",
    depuisColomiers: "En descendant vers le sud de l'agglomération toulousaine.",
  },
] as const;

export const club = (id: Club['id']): Club => {
  const c = CLUBS.find((x) => x.id === id);
  if (!c) throw new Error(`Club inconnu : ${id}`);
  return c;
};

/* ─────────────────────────────  DISCIPLINES  ───────────────────────────── */

export type Discipline = {
  id: 'boxe-anglaise' | 'mma' | 'boxing-fitness' | 'boxe-enfants';
  nom: string;
  /** l'intitulé tel qu'un visiteur le formule, pas tel qu'un club le nomme */
  question: string;
  /** phrase courte qui répond avant de vendre */
  reponse: string;
  route: string;
  /** mots-clés du cahier des charges §4 que cette page doit porter */
  motsCles: readonly string[];
};

export const DISCIPLINES: readonly Discipline[] = [
  {
    id: 'boxe-anglaise',
    nom: 'Boxe anglaise',
    question: 'Je veux apprendre à boxer.',
    reponse:
      "Poings uniquement, déplacements, garde, lecture de l'adversaire. C'est la discipline la plus simple à commencer et la plus longue à maîtriser.",
    route: '/boxe-anglaise/',
    motsCles: ['boxe anglaise Colomiers', 'club de boxe Colomiers', 'cours de boxe Colomiers'],
  },
  {
    id: 'mma',
    nom: 'MMA',
    question: 'Je veux du MMA, du complet.',
    reponse:
      'Frappe debout, corps à corps, sol. La discipline la plus complète, et celle où un encadrement sérieux compte le plus.',
    route: '/mma/',
    motsCles: ['club MMA Colomiers', 'MMA Colomiers', 'club MMA près de Colomiers'],
  },
  {
    id: 'boxing-fitness',
    nom: 'Boxing Fitness & Femme',
    question: 'Je veux me remettre en forme, sans combattre.',
    reponse:
      "Le geste de boxe, le cardio, le défoulement — sans opposition. Tu ne prends pas de coup, et tu n'as rien à prouver à personne.",
    route: '/boxing-fitness/',
    motsCles: ['boxing fitness Colomiers', 'boxe femme Colomiers'],
  },
  {
    id: 'boxe-enfants',
    nom: 'Boxe enfants',
    question: 'Je cherche quelque chose pour mon enfant.',
    reponse:
      'Boxe éducative : le geste, le cadre, le respect de l’autre. Pas de mise en danger, un encadrement qui fait autorité.',
    route: '/boxe-enfants/',
    motsCles: ['boxe enfant Colomiers', 'cours de boxe enfant Colomiers'],
  },
] as const;

export const discipline = (id: Discipline['id']): Discipline => {
  const d = DISCIPLINES.find((x) => x.id === id);
  if (!d) throw new Error(`Discipline inconnue : ${id}`);
  return d;
};

/* ─────────────────────────  CE QU'ON NE DIT PAS  ───────────────────────── */

/**
 * Formulations interdites. Le cahier des charges §2 l'exige explicitement :
 * ne jamais laisser croire qu'une salle Boxing Center est à Colomiers.
 * Un test de build vérifie qu'aucune de ces chaînes n'apparaît dans le HTML.
 */
export const INTERDIT: readonly string[] = [
  'salle de Colomiers',
  'notre salle à Colomiers',
  'notre club à Colomiers',
  'Boxing Center Colomiers vous accueille',
  'venez à notre salle de Colomiers',
  'situé à Colomiers',
  'située à Colomiers',
  'basé à Colomiers',
];

/**
 * Formulations à privilégier — cahier des charges §2, mot pour mot.
 */
export const FORMULATIONS = [
  'club de boxe proche de Colomiers',
  'cours de boxe accessibles depuis Colomiers',
  'club de MMA près de Colomiers',
  'sports de combat à proximité de Colomiers',
] as const;
