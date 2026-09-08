/**
 * LE GRAPHE RÉEL DES DISCIPLINES — quel club propose quoi.
 *
 * Relevé le 07/09/2026 sur les pages « activités » officielles des deux
 * clubs. Chaque ligne cite sa source.
 *
 * Pourquoi ça compte autant pour le référencement : dire « nos deux clubs
 * proposent la boxe et le MMA » est générique, invérifiable et faux. Dire
 * « le MMA se pratique à Portet, dans une cage, avec le grappling et le JJB ;
 * la boxe anglaise se pratique dans les deux » est précis, vérifiable et
 * différenciant. C'est cette précision-là qu'un moteur de réponse peut citer,
 * et c'est elle qui fait qu'une page cesse de ressembler à toutes les autres.
 *
 * Corollaire : quand une discipline n'existe que dans un club, la page de
 * cette discipline a une destination unique et donc une recommandation
 * évidente. Le moteur de proximité s'en sert.
 */

import type { Club } from './verite';

export type ClubId = Club['id'];

export type Offre = {
  club: ClubId;
  /** l'intitulé publié par le club, mot pour mot */
  intitule: string;
  /** la famille de discipline à laquelle ça se rattache sur notre site */
  famille: Famille;
  /** tranche d'âge quand le club la publie */
  ages?: string;
  /** ce qui rend cette offre concrètement singulière */
  detail?: string;
  source: string;
};

export type Famille =
  | 'boxe-anglaise'
  | 'mma'
  | 'grappling'
  | 'kick-boxing'
  | 'fitness'
  | 'femme'
  | 'enfants'
  | 'physique';

const MINIMES = 'https://boxe-toulouse.com/activites/';
const PORTET = 'https://boxing-center-portet.fr/activites/';

export const OFFRES: readonly Offre[] = [
  /* ── Toulouse Minimes ─────────────────────────────────────────────── */
  { club: 'minimes', intitule: 'Boxe Anglaise Loisir', famille: 'boxe-anglaise', detail: 'La pratique sans objectif de compétition', source: MINIMES },
  { club: 'minimes', intitule: 'Boxe Compétiteurs', famille: 'boxe-anglaise', detail: 'Le groupe qui prépare les combats', source: MINIMES },
  { club: 'minimes', intitule: 'Boxe Pieds-Poings', famille: 'kick-boxing', detail: 'Les jambes en plus des poings', source: MINIMES },
  { club: 'minimes', intitule: 'Boxe Éducative', famille: 'enfants', source: MINIMES },
  { club: 'minimes', intitule: 'Baby Boxe', famille: 'enfants', ages: '3 à 6 ans', source: MINIMES },
  { club: 'minimes', intitule: 'Boxing Lady', famille: 'femme', detail: 'Un créneau 100 % féminin', source: MINIMES },
  { club: 'minimes', intitule: 'Cardio Boxing', famille: 'fitness', detail: 'Le geste de boxe en travail cardio, sans opposition', source: MINIMES },
  { club: 'minimes', intitule: 'Cross Training', famille: 'physique', source: MINIMES },
  { club: 'minimes', intitule: 'PAOS & Pattes d’ours', famille: 'fitness', detail: 'Le travail aux pattes d’ours avec un coach', source: MINIMES },
  { club: 'minimes', intitule: 'Boxing Camp', famille: 'physique', source: MINIMES },

  /* ── Portet-sur-Garonne ───────────────────────────────────────────── */
  { club: 'portet', intitule: 'Boxe anglaise', famille: 'boxe-anglaise', source: PORTET },
  { club: 'portet', intitule: 'MMA', famille: 'mma', detail: 'Entraînement en cage', source: PORTET },
  { club: 'portet', intitule: 'Grappling & jiu-jitsu brésilien', famille: 'grappling', detail: 'Le corps à corps et le sol', source: PORTET },
  { club: 'portet', intitule: 'Kick-boxing', famille: 'kick-boxing', source: PORTET },
  { club: 'portet', intitule: 'Kick-boxing enfants/ados', famille: 'enfants', source: PORTET },
  { club: 'portet', intitule: 'Boxe éducative', famille: 'enfants', source: PORTET },
  { club: 'portet', intitule: 'Baby boxe', famille: 'enfants', source: PORTET },
  { club: 'portet', intitule: 'Lady Boxing', famille: 'femme', source: PORTET },
  { club: 'portet', intitule: 'Préparation physique', famille: 'physique', source: PORTET },
] as const;

/** Les intitulés réellement publiés par un club. */
export const offresDuClub = (club: ClubId) => OFFRES.filter((o) => o.club === club);

/** Les clubs qui proposent réellement une famille de discipline. */
export const clubsQuiProposent = (f: Famille): ClubId[] => [
  ...new Set(OFFRES.filter((o) => o.famille === f).map((o) => o.club)),
];

/** Les intitulés d'une famille, tous clubs confondus. */
export const offresDeLaFamille = (f: Famille) => OFFRES.filter((o) => o.famille === f);

/**
 * Une famille exclusive à un club donne une réponse sans ambiguïté : c'est le
 * cas du MMA et du grappling, qui n'existent qu'à Portet.
 */
export function destinationUnique(f: Famille): ClubId | null {
  const c = clubsQuiProposent(f);
  return c.length === 1 ? c[0] : null;
}

/** Familles portées par chacune des quatre pages du site. */
export const FAMILLES_PAR_PAGE: Record<string, readonly Famille[]> = {
  'boxe-anglaise': ['boxe-anglaise', 'kick-boxing'],
  mma: ['mma', 'grappling'],
  'boxing-fitness': ['fitness', 'femme', 'physique'],
  'boxe-enfants': ['enfants'],
};
