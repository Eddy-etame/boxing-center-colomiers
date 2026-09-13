/**
 * Les pages de discipline des clubs de destination.
 *
 * Chaque page de discipline de ce site mène à DEUX endroits du club : la page
 * de la discipline, quand le club en publie une, et le site du club. Un club
 * qui ne publie pas de page par discipline renvoie à sa page des activités.
 * Relevé le 13 septembre 2026 sur les plans de site des clubs.
 */
type Porte = { url: string; nom: string };

export const PAGES_CLUB: Record<string, Record<string, Porte>> = {
  portet: {
    'boxe-anglaise': { url: 'https://boxing-center-portet.fr/activites/boxe-anglaise/', nom: 'la boxe anglaise' },
    mma: { url: 'https://boxing-center-portet.fr/activites/mma/', nom: 'le MMA' },
    'kick-boxing': { url: 'https://boxing-center-portet.fr/activites/kick-boxing/', nom: 'le kick-boxing' },
    'boxe-thai': { url: 'https://boxing-center-portet.fr/activites/kick-boxing/', nom: 'le kick-boxing et le K1' },
    'boxe-enfants': { url: 'https://boxing-center-portet.fr/activites/boxe-educative/', nom: 'la boxe éducative' },
    'boxing-fitness': { url: 'https://boxing-center-portet.fr/activites/lady-boxing/', nom: 'le Lady Boxing' },
    'preparation-physique': { url: 'https://boxing-center-portet.fr/activites/preparation-physique/', nom: 'la préparation physique' },
  },
  ramonville: {
    'boxe-anglaise': { url: 'https://mmatoulouse.com/activites/boxe-anglaise/', nom: 'la boxe anglaise' },
    mma: { url: 'https://mmatoulouse.com/activites/mma/', nom: 'le MMA' },
    'kick-boxing': { url: 'https://mmatoulouse.com/activites/boxe-pieds-poings/', nom: 'la boxe pieds-poings' },
    'boxe-enfants': { url: 'https://mmatoulouse.com/activites/ecole-enfants/', nom: 'l’école de boxe enfants' },
    'boxing-fitness': { url: 'https://mmatoulouse.com/activites/lady-punch/', nom: 'le Lady Punch' },
  },
};

/** La porte « discipline » d'un club : sa page dédiée, sinon sa page des activités. */
export const pageClub = (club: { id: string; activites: string }, discipline: string) => {
  const p = PAGES_CLUB[club.id]?.[discipline];
  return p
    ? { url: p.url, libelle: `Voir ${p.nom} au club`, dediee: true }
    : { url: club.activites, libelle: 'Les activités du club', dediee: false };
};

/** Parmi plusieurs clubs, celui qui publie une page pour la discipline passe devant. */
export const clubEnVitrine = <C extends { id: string }>(clubs: readonly C[], discipline: string): C =>
  clubs.find((c) => PAGES_CLUB[c.id]?.[discipline]) ?? clubs[0];
