/**
 * CE QUE MONTRE LA VIGNETTE DE CHAQUE PAGE — la photo de la page, le sujet,
 * le lieu, les clubs et la ligne. Lu par pages/og/ (l'image) et par le layout
 * (le JSON-LD) : l'image annoncée et l'image servie sont la même.
 */
import { CLUBS } from './verite';
import { CONTEXTE_GEO } from './mots-cles';
import { CONTENUS } from './contenus';
import { MEILLEUR } from './transports';

/** Colomiers est le point de départ, jamais une adresse de club. */
export const VILLE_SITE: string = CONTEXTE_GEO.ville;
export const CLUB_VIGNETTE: string = CLUBS.map((c) => c.nomCourt).join(' · ');
export const LIGNE_VIGNETTE: string = MEILLEUR.etapes.map((e) => e.code).join(' → ');

const SUJETS: Record<string, string> = {
  accueil: 'Club de boxe · MMA',
  'boxe-anglaise': 'Boxe anglaise',
  mma: 'Club MMA',
  'kick-boxing': 'Kick-boxing',
  'boxe-pieds-poings': 'Boxe pieds-poings',
  'boxe-thai': 'Boxe thaï · K1',
  'boxe-enfants': 'Boxe enfant',
  'boxing-fitness': 'Boxing fitness',
  'preparation-physique': 'Préparation physique',
  'premiere-seance': 'Première séance',
  'ta-seance': 'Ta séance',
  'quel-club': 'Quel club',
  transports: 'Y aller en bus',
  contact: 'Contact',
  plannings: 'Plannings',
  tarifs: 'Tarifs',
};
const DEPUIS = new Set(['transports', 'contact', 'quel-club', 'ta-seance']);

/** « BOXE ANGLAISE · PRÈS DE », « Y ALLER EN BUS · DEPUIS » : la ligne au-dessus du lieu. */
export function etiquetteDeLaRoute(id: string): string {
  return `${SUJETS[id] ?? 'Club de boxe · MMA'} · ${DEPUIS.has(id) ? 'depuis' : 'près de'}`;
}

export function photoDeLaRoute(id: string): string {
  const c = CONTENUS.find((x) => x.id === id);
  if (c) return c.photoHero;
  if (id === 'premiere-seance' || id === 'contact') return 'premiere-seance-boxe-colomiers';
  if (id === 'transports') return 'ambiance-club-boxe-colomiers';
  if (id === 'plannings' || id === 'tarifs') return 'salle-boxing-center-colomiers';
  return 'club-boxe-colomiers-boxing-center';
}

export const lieuDeLaRoute = (_id: string): string => VILLE_SITE;
