/**
 * REGISTRE DES TRANSPORTS — les itinéraires qui déposent au club.
 *
 * La règle, et elle est stricte : une ligne n'entre ici que si elle fait
 * avancer un Columérin jusqu'à la porte d'un des deux clubs. Une ligne qui
 * dessert le secteur sans y mener n'a rien à faire sur cette page.
 *
 * Sur ce site, le choix d'itinéraire EST le choix de club : la 63 et le métro
 * B mènent aux Minimes en deux étapes ; la même 63, le même métro B et le
 * Linéo L5 mènent à Portet.
 *
 * Chaque étape a été relevée sur la fiche horaire Tisséo de sa ligne, le
 * 2026-09-09 :
 *   63  Compans-Caffarelli ⇄ Tournefeuille Lycée — dessert Colomiers
 *       Ramassiers Gare SNCF, Esplanade des Ramassiers, Caulet et Fontaine.
 *       Son terminus est une station du métro B. Du lundi au samedi.
 *   L2  Arènes ⇄ Colomiers Lycée International — dessert Colomiers Gare SNCF
 *       et la Médiathèque Pavillon Blanc. Tous les jours, un bus toutes les
 *       9 à 12 minutes. Son terminus est une station du métro A.
 *   L5  Empalot ⇄ Portet Gare SNCF — longe la route d'Espagne et marque
 *       l'arrêt « Jean Jaurès », à Portet. Tous les jours.
 *
 * Ce qu'on n'écrit JAMAIS ici : un horaire, une durée de trajet. Chaque étape
 * porte le lien vers sa page officielle : c'est Tisséo qui dit quand, ce site
 * dit quoi.
 */

export type Mode = 'bus' | 'metro' | 'train';

export type Etape = {
  mode: Mode;
  code: string;
  de: string;
  a: string;
  precision?: string;
  jours: string;
  href: string;
};

export type Itineraire = {
  id: string;
  onglet: string;
  titre: string;
  resume: string;
  mode: Mode;
  /** le club au bout de ce trajet */
  club: 'minimes' | 'portet';
  etapes: readonly Etape[];
  meilleur?: true;
};

export const RESEAU = {
  nom: 'Tisséo',
  site: 'https://www.tisseo.fr/',
  itineraire: 'https://www.tisseo.fr/se-deplacer/itineraires',
} as const;

export const LIBELLE_MODE: Record<Mode, string> = {
  bus: 'Bus',
  metro: 'Métro',
  train: 'Train',
};

/** L'arrêt d'arrivée du meilleur trajet, et ce qu'il a de remarquable. */
export const ARRIVEE = {
  arret: 'Barrière de Paris',
  rue: 'rue de Fenouillet',
  phrase:
    'Le métro B s’arrête à Barrière de Paris. C’est la station la plus proche du club, au 12 rue de Fenouillet.',
} as const;

const LIGNE_63: Etape = {
  mode: 'bus',
  code: '63',
  de: 'Colomiers Ramassiers Gare SNCF',
  a: 'Compans-Caffarelli',
  precision: 'terminus de la ligne, et station du métro B',
  jours: 'du lundi au samedi',
  href: 'https://www.tisseo.fr/nos-mobilites/transports-en-commun/ligne-63',
};

/** Le titre de la page, ligne par ligne. La dernière porte l'accent. */
export const TITRE = [
  'La 63 finit au métro.',
  'Le métro B fait le reste.',
  'Deux étapes, et tu y es.',
] as const;

/** Le chapeau : ce que fait le meilleur trajet, en une phrase. */
export const CHAPEAU =
  'La 63 traverse Colomiers et finit à Compans-Caffarelli, qui est une station du métro B. Tu y prends le métro et tu descends à Barrière de Paris : le club des Minimes est au 12 rue de Fenouillet. Pour Portet, c’est le même début, et le Linéo L5 termine le trajet route d’Espagne.';

export const ITINERAIRES: readonly Itineraire[] = [
  {
    id: 'minimes',
    onglet: 'La 63, puis le métro B',
    titre: 'De Colomiers aux Minimes, en deux étapes.',
    resume:
      'La 63 dessert Colomiers Ramassiers, Caulet et Fontaine, puis finit à Compans-Caffarelli — son terminus est une station du métro B. Tu prends le métro dans le sens du nord et tu descends à Barrière de Paris. Le club est au 12 rue de Fenouillet.',
    mode: 'bus',
    club: 'minimes',
    meilleur: true,
    etapes: [
      LIGNE_63,
      {
        mode: 'metro',
        code: 'B',
        de: 'Compans-Caffarelli',
        a: 'Barrière de Paris',
        precision: 'la station la plus proche de la rue de Fenouillet',
        jours: 'sept jours sur sept',
        href: 'https://www.tisseo.fr/nos-mobilites/transports-en-commun/ligne-b',
      },
    ],
  },
  {
    id: 'portet',
    onglet: 'La 63, le métro B, le L5',
    titre: 'De Colomiers à Portet, pour le MMA et la cage.',
    resume:
      'Même départ : la 63 jusqu’à Compans-Caffarelli. Le métro B descend cette fois vers le sud, jusqu’à Empalot, où démarre le Linéo L5. Ce Linéo longe la route d’Espagne et marque l’arrêt « Jean Jaurès » : le club est au 61. C’est le trajet à connaître pour le MMA, le grappling et la cage.',
    mode: 'bus',
    club: 'portet',
    etapes: [
      LIGNE_63,
      {
        mode: 'metro',
        code: 'B',
        de: 'Compans-Caffarelli',
        a: 'Empalot',
        precision: 'le Linéo L5 démarre à cette station',
        jours: 'sept jours sur sept',
        href: 'https://www.tisseo.fr/nos-mobilites/transports-en-commun/ligne-b',
      },
      {
        mode: 'bus',
        code: 'L5',
        de: 'Empalot',
        a: 'Jean Jaurès',
        precision: 'sur la route d’Espagne, à Portet-sur-Garonne',
        jours: 'tous les jours',
        href: 'https://www.tisseo.fr/nos-mobilites/transports-en-commun/ligne-l5',
      },
    ],
  },
  {
    id: 'lineo',
    onglet: 'Le L2, tous les jours',
    titre: 'Le dimanche, et depuis le centre de Colomiers.',
    resume:
      'Le Linéo L2 part de Colomiers Lycée International, passe par la Médiathèque Pavillon Blanc et Colomiers Gare SNCF, et finit aux Arènes. Il roule tous les jours, avec un bus toutes les neuf à douze minutes aux heures de pointe. Le métro A y démarre, et le métro B prend le relais à Jean Jaurès.',
    mode: 'bus',
    club: 'minimes',
    etapes: [
      {
        mode: 'bus',
        code: 'L2',
        de: 'Colomiers Gare SNCF',
        a: 'Arènes',
        precision: 'terminus du Linéo, correspondance métro, tram et train',
        jours: 'tous les jours',
        href: 'https://www.tisseo.fr/nos-mobilites/transports-en-commun/ligne-l2',
      },
      {
        mode: 'metro',
        code: 'A',
        de: 'Arènes',
        a: 'Jean Jaurès',
        precision: 'la correspondance avec le métro B',
        jours: 'sept jours sur sept',
        href: 'https://www.tisseo.fr/nos-mobilites/transports-en-commun/ligne-a',
      },
      {
        mode: 'metro',
        code: 'B',
        de: 'Jean Jaurès',
        a: 'Barrière de Paris',
        precision: 'la station la plus proche de la rue de Fenouillet',
        jours: 'sept jours sur sept',
        href: 'https://www.tisseo.fr/nos-mobilites/transports-en-commun/ligne-b',
      },
    ],
  },
];

export const itineraire = (id: string) => {
  const i = ITINERAIRES.find((x) => x.id === id);
  if (!i) throw new Error(`Itinéraire inconnu : ${id}`);
  return i;
};

/** L'itinéraire qui mène à un club donné. */
export const itineraireDuClub = (club: string) => ITINERAIRES.find((i) => i.club === club);

export const MEILLEUR = ITINERAIRES.find((i) => i.meilleur) ?? ITINERAIRES[0];

export const RESUME = 'La 63 jusqu’au métro B, puis Barrière de Paris';

export type Depart = { depuis: string; itineraire: string; texte: string };

export const DEPARTS: readonly Depart[] = [
  {
    depuis: 'Colomiers Ramassiers',
    itineraire: 'minimes',
    texte:
      'La 63 démarre le trajet ici et finit à Compans-Caffarelli. Le métro B monte vers le nord, et Barrière de Paris est la station du club.',
  },
  {
    depuis: 'Le centre de Colomiers',
    itineraire: 'lineo',
    texte:
      'Le Linéo L2 passe à la Médiathèque Pavillon Blanc et à Colomiers Gare SNCF, puis finit aux Arènes. C’est la ligne qui roule aussi le dimanche.',
  },
  {
    depuis: 'Vers le MMA et la cage',
    itineraire: 'portet',
    texte:
      'La cage est à Portet. Même 63, même métro B, mais vers le sud jusqu’à Empalot, puis le Linéo L5 sur la route d’Espagne.',
  },
];

export const AVERTISSEMENT =
  'Tisséo publie les horaires, les fréquences et les arrêts, et les met à jour à chaque saison. Cette page te dit quelles lignes prendre ; Tisséo te dit à quelle heure elles passent.';
