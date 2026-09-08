/**
 * MANIFESTE MÉDIA — provenance, cadrage, alt.
 *
 * Source : lot WeTransfer du 07/09/2026, salle BOXING CENTER TOULOUSE MINIMES
 * (confirmé par le cahier des charges §11).
 *
 * RÈGLE : aucune photo n'est présentée comme montrant une salle à Colomiers.
 * Les légendes disent toujours où la photo a été prise.
 *
 * `pair` : trois prises existent en double, noir et blanc ET couleur, du même
 * instant. C'est le matériau du mécanisme « la certitude colore le monde » :
 * on ne filtre pas en CSS, on montre les deux vraies photographies.
 */

export type Media = {
  /** nom de fichier SEO, sans extension */
  slug: string;
  /** fichier source dans le lot WeTransfer */
  source: string;
  /** description alternative — décrit ce qu'on voit, pas ce qu'on vend */
  alt: string;
  /** ce qu'on voit, puis le club — affiché quand la photo est un document */
  legende?: string;
  /** true si la prise est en noir et blanc */
  bw?: boolean;
  /** identifiant de paire N&B / couleur du même instant */
  pair?: string;
  /** cadrage : point d'intérêt pour les recadrages mobiles (object-position) */
  focus?: string;
};

export const LIEU_PRISE_DE_VUE = 'Boxing Center Toulouse Minimes';

export const MEDIAS = [
  {
    slug: 'materiel-boxe-colomiers-boxing-center',
    source: 'DSC_2932.jpg',
    alt: "Gants de boxe et casque de protection posés sur un sac de sport dans le vestiaire du club.",
    legende: 'Le matériel du club. Boxing Center Toulouse Minimes.',
    focus: '50% 45%',
  },
  {
    slug: 'cours-boxe-colomiers-sac-de-frappe',
    source: 'DSC_2964.jpg',
    alt: "Un pratiquant en sweat rouge frappe un sac lourd pendant un entraînement de boxe.",
    legende: 'Travail au sac. Boxing Center Toulouse Minimes.',
    focus: '55% 40%',
  },
  {
    slug: 'club-boxe-colomiers-boxing-center',
    source: 'DSC_2969.jpg',
    alt: "Un boxeur travaille sur un sac Boxing Center dans la salle d'entraînement.",
    legende: 'La salle. Boxing Center Toulouse Minimes.',
    bw: true,
    focus: '60% 45%',
  },
  {
    slug: 'encadrement-coach-boxe-colomiers',
    source: 'DSC_2979.jpg',
    alt: "Un coach ajuste les gants d'un boxeur casqué avant de monter sur le ring.",
    legende: "L'encadrement avant la montée sur le ring. Boxing Center Toulouse Minimes.",
    bw: true,
    focus: '45% 40%',
  },
  {
    slug: 'boxe-anglaise-colomiers-technique',
    source: 'DSC_3054.jpg',
    alt: "Un boxeur en garde face à un coach qui tient les pattes d'ours, dans le ring.",
    legende: 'Travail technique aux pattes d’ours. Boxing Center Toulouse Minimes.',
    focus: '55% 35%',
  },
  {
    slug: 'cours-collectifs-boxe-colomiers',
    source: 'DSC_3078.jpg',
    alt: "Vue large de la salle pendant un cours collectif : plusieurs pratiquants autour et sur le ring.",
    legende: 'Cours collectif. Boxing Center Toulouse Minimes.',
    focus: '50% 50%',
  },
  {
    slug: 'preparation-physique-boxe-colomiers',
    source: 'DSC_3081.jpg',
    alt: "Un pratiquant fait de la corde à sauter pendant l'échauffement, au centre de la salle.",
    legende: 'Échauffement à la corde. Boxing Center Toulouse Minimes.',
    focus: '45% 40%',
  },
  {
    slug: 'salle-boxing-center-colomiers',
    source: 'DSC_3095.jpg',
    alt: "Un pratiquant de dos face au ring Boxing Center, dans la salle d'entraînement.",
    legende: 'Face au ring. Boxing Center Toulouse Minimes.',
    focus: '50% 40%',
  },
  {
    slug: 'ring-boxe-colomiers-boxing-center',
    source: 'DSC_3100.jpg',
    alt: "Le ring de la salle vu de l'extérieur des cordes, pendant un entraînement.",
    legende: 'Le ring. Boxing Center Toulouse Minimes.',
    focus: '55% 50%',
  },
  {
    slug: 'sparring-boxe-colomiers',
    source: 'DSC_3117.jpg',
    alt: "Deux boxeurs casqués en opposition contrôlée pendant une séance de sparring.",
    legende: 'Sparring encadré. Boxing Center Toulouse Minimes.',
    focus: '50% 35%',
  },
  {
    slug: 'bandage-mains-boxe-colomiers-debutant',
    source: 'DSC_3131.jpg',
    alt: "Un pratiquant enroule les bandes autour des mains d'un autre avant l'entraînement.",
    legende: 'Les bandes, avant tout le reste. Boxing Center Toulouse Minimes.',
    focus: '55% 45%',
  },
  {
    slug: 'sport-combat-colomiers-sac-frappe',
    source: 'DSC_3167.jpg',
    alt: "Un pratiquant frappe un sac lourd, poings gantés, dans la salle d'entraînement.",
    legende: 'Travail au sac. Boxing Center Toulouse Minimes.',
    focus: '40% 40%',
  },
  {
    slug: 'boxe-colomiers-garde-nb',
    source: 'DSC_3174-2.jpg',
    alt: "Un boxeur en garde haute pendant un exercice, en noir et blanc.",
    bw: true,
    pair: 'garde',
    focus: '50% 35%',
  },
  {
    slug: 'boxe-colomiers-garde',
    source: 'DSC_3174.jpg',
    alt: "Un boxeur en garde haute pendant un exercice, gants verts.",
    legende: 'La garde. Boxing Center Toulouse Minimes.',
    pair: 'garde',
    focus: '50% 35%',
  },
  {
    slug: 'ambiance-club-boxe-colomiers',
    source: 'DSC_3215.jpg',
    alt: "Un boxeur s'entraîne dans le ring pendant que d'autres pratiquants observent depuis le bord.",
    legende: 'Le club pendant un entraînement. Boxing Center Toulouse Minimes.',
    focus: '50% 45%',
  },
  {
    slug: 'deplacement-boxe-anglaise-colomiers',
    source: 'DSC_3218.jpg',
    alt: "Un boxeur travaille ses déplacements dans le ring, appui sur la jambe arrière.",
    legende: 'Travail des appuis. Boxing Center Toulouse Minimes.',
    focus: '50% 45%',
  },
  {
    slug: 'coach-boxe-colomiers-paos',
    source: 'DSC_3256.jpg',
    alt: "Un coach tient les pattes d'ours face à un boxeur, en noir et blanc.",
    legende: 'Aux pattes d’ours avec le coach. Boxing Center Toulouse Minimes.',
    bw: true,
    focus: '55% 40%',
  },
  {
    slug: 'mma-colomiers-boxing-center',
    source: 'DSC_3264.jpg',
    alt: "Un pratiquant enchaîne des frappes sur les pattes d'ours tenues par un coach, dans le ring.",
    legende: 'Enchaînements aux pattes d’ours. Boxing Center Toulouse Minimes.',
    focus: '55% 40%',
  },
  {
    slug: 'boxing-fitness-colomiers-nb',
    source: 'DSC_3265.jpg',
    alt: "Un boxeur travaille aux pattes d'ours devant la fresque murale du club, en noir et blanc.",
    bw: true,
    pair: 'paos',
    focus: '55% 40%',
  },
  {
    slug: 'boxing-fitness-colomiers',
    source: 'DSC_3267.jpg',
    alt: "Un boxeur travaille aux pattes d'ours devant la fresque murale du club, gants verts.",
    legende: 'Devant la fresque du club. Boxing Center Toulouse Minimes.',
    pair: 'paos',
    focus: '55% 40%',
  },
  {
    slug: 'premiere-seance-boxe-colomiers',
    source: 'DSC_3273.jpg',
    alt: "Un coach prépare les gants d'un pratiquant dans le ring, avant le début du travail.",
    legende: 'Avant la première séance. Boxing Center Toulouse Minimes.',
    focus: '50% 40%',
  },
  {
    slug: 'cours-boxe-colomiers-encadrement',
    source: 'DSC_3296.jpg',
    alt: "Un coach et un boxeur face à face pendant un exercice aux pattes d'ours, vue large.",
    focus: '55% 45%',
  },
  {
    slug: 'cours-boxe-colomiers-encadrement-2',
    source: 'DSC_3299.jpg',
    alt: "Un coach avance sur un boxeur qui riposte pendant un exercice aux pattes d'ours.",
    legende: 'Le coach met la pression, le boxeur répond. Boxing Center Toulouse Minimes.',
    focus: '55% 45%',
  },
  {
    slug: 'travail-au-corps-boxe-colomiers-nb',
    source: 'DSC_3309-2.jpg',
    alt: "Deux pratiquants au corps à corps pendant un exercice, en noir et blanc.",
    bw: true,
    pair: 'corps',
    focus: '50% 40%',
  },
  {
    slug: 'travail-au-corps-boxe-colomiers',
    source: 'DSC_3309.jpg',
    alt: "Deux pratiquants au corps à corps pendant un exercice, gants verts.",
    legende: 'Travail au corps. Boxing Center Toulouse Minimes.',
    pair: 'corps',
    focus: '50% 40%',
  },
] as const satisfies readonly Media[];

export type MediaSlug = (typeof MEDIAS)[number]['slug'];

const INDEX = new Map(MEDIAS.map((m) => [m.slug, m as Media]));

export function media(slug: MediaSlug): Media {
  const m = INDEX.get(slug);
  if (!m) throw new Error(`Média inconnu : ${slug}`);
  return m;
}

/** Les trois paires noir-et-blanc / couleur du même instant. */
export const PAIRES = ['garde', 'paos', 'corps'] as const;

export function paire(nom: (typeof PAIRES)[number]) {
  const both = MEDIAS.filter((m) => 'pair' in m && m.pair === nom) as Media[];
  const nb = both.find((m) => m.bw);
  const couleur = both.find((m) => !m.bw);
  if (!nb || !couleur) throw new Error(`Paire incomplète : ${nom}`);
  return { nb, couleur };
}
