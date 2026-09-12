/**
 * REGISTRE DES ROUTES — une page = une question humaine distincte.
 *
 * Aucune URL n'est écrite en dur ailleurs dans le projet : on passe par
 * `route('mma')`. Renommer une page ne casse alors rien.
 *
 * Le titre et la description vivent ici parce qu'ils font partie de
 * l'architecture de recherche, pas de la mise en page.
 */

import { HORAIRES } from './verite';

export type RouteId =
  | 'accueil'
  | 'boxe-anglaise'
  | 'mma'
  | 'boxing-fitness'
  | 'boxe-enfants'
  | 'plannings'
  | 'tarifs'
  | 'premiere-seance'
  | 'quel-club'
  | 'transports'
  | 'contact'
  | 'merci'
  | 'introuvable'
  | 'mentions-legales'
  | 'confidentialite';

export type Route = {
  id: RouteId;
  chemin: string;
  /** libellé de navigation — court, pas le titre SEO */
  nav: string;
  /** la question à laquelle la page répond, du point de vue du visiteur */
  question: string;
  titre: string;
  description: string;
  /** dans la navigation principale ? */
  menu: boolean;
  /** indexable ? */
  index: boolean;
  /** page mise en avant dans la barre, hors liste ordinaire */
  promo?: true;
};

export const ROUTES: readonly Route[] = [
  {
    id: 'accueil',
    chemin: '/',
    nav: 'Accueil',
    question: 'Où pratiquer la boxe ou le MMA quand on habite à Colomiers ?',
    titre: 'Club de boxe et MMA près de Colomiers | Boxing Center',
    description:
      "Club de boxe, MMA et sports de combat près de Colomiers : Boxing Center accueille les Columérins à Toulouse Minimes et Portet-sur-Garonne, " + HORAIRES.court.valeur + ".",
    menu: true,
    index: true,
  },
  {
    id: 'boxe-anglaise',
    chemin: '/boxe-anglaise/',
    nav: 'Boxe anglaise',
    question: 'À quoi ressemble un cours de boxe anglaise, et est-ce que je peux commencer ?',
    titre: 'Boxe anglaise près de Colomiers | Boxing Center',
    description:
      "Cours de boxe anglaise accessibles depuis Colomiers, débutants comme confirmés. Clubs Boxing Center à Toulouse Minimes et Portet-sur-Garonne, 6 j/7.",
    menu: true,
    index: true,
  },
  {
    id: 'mma',
    chemin: '/mma/',
    nav: 'MMA',
    question: 'Où faire du MMA quand on part de Colomiers, et comment on commence ?',
    titre: 'Club de MMA près de Colomiers | Boxing Center',
    description:
      'Club de MMA près de Colomiers : frappe, corps à corps et sol, encadrement qui construit les débutants. À Portet-sur-Garonne, avec cage, grappling et JJB.',
    menu: true,
    index: true,
  },
  {
    id: 'boxing-fitness',
    chemin: '/boxing-fitness/',
    nav: 'Boxing Fitness & Femme',
    question: 'Je veux boxer pour la forme, sans prendre de coup. C’est possible ?',
    titre: 'Boxing fitness et boxe femme — Colomiers | Boxing Center',
    description:
      "Boxing fitness et boxe femme depuis Colomiers : cardio, geste de boxe, défoulement — sans opposition ni obligation de combattre. Ouvert aux débutantes.",
    menu: true,
    index: true,
  },
  {
    id: 'boxe-enfants',
    chemin: '/boxe-enfants/',
    nav: 'Boxe enfants',
    question: 'Quelle boxe pour mon enfant, et est-ce que c’est sans danger ?',
    titre: 'Boxe enfant près de Colomiers | Boxing Center',
    description:
      "Cours de boxe enfant accessibles depuis Colomiers. Boxe éducative encadrée : le geste, le cadre, le respect. Sans mise en danger.",
    menu: true,
    index: true,
  },
  {
    id: 'plannings',
    chemin: '/plannings/',
    nav: 'Plannings',
    question: 'Quand est-ce que je peux m’entraîner, avec mes horaires à moi ?',
    titre: 'Plannings et horaires près de Colomiers | Boxing Center',
    description:
      "Les clubs Boxing Center accueillent " + HORAIRES.court.valeur + ". Trouve le créneau qui tient dans ta semaine et accède aux plannings détaillés des deux clubs.",
    menu: true,
    index: true,
  },
  {
    id: 'tarifs',
    chemin: '/tarifs/',
    nav: 'Tarifs',
    question: 'Combien ça coûte, et qu’est-ce qui est compris ?',
    titre: 'Tarifs boxe et MMA près de Colomiers | Boxing Center',
    description:
      "Ce qui est compris dans une adhésion à un club de boxe, et où consulter les tarifs à jour de Boxing Center Toulouse Minimes et Portet-sur-Garonne.",
    menu: true,
    index: true,
  },
  {
    id: 'premiere-seance',
    chemin: '/premiere-seance/',
    nav: 'Première séance',
    question: 'Je n’ai jamais fait de boxe. Qu’est-ce qui m’attend à la première séance ?',
    titre: 'Première séance de boxe près de Colomiers | Boxing Center',
    description:
      'Ce qu’il faut apporter, ce que tu vas faire, ce que tu ne feras pas : la première séance de boxe ou de MMA d’un débutant, depuis Colomiers, minute par minute.',
    menu: false,
    index: true,
  },
  {
    id: 'quel-club',
    chemin: '/quel-club/',
    nav: 'Quel club',
    question: 'Minimes ou Portet : lequel des deux clubs Boxing Center depuis Colomiers ?',
    titre: 'Quel club Boxing Center depuis Colomiers : Minimes ou Portet ?',
    description:
      'Deux clubs de boxe près de Colomiers, pas la même offre : le MMA à Portet, la boxe anglaise dans les deux. Deux réponses et on te dit lequel viser.',
    menu: false,
    index: true,
  },
  {
    id: 'transports',
    chemin: '/transports/',
    nav: 'Transports',
    question: 'Comment j’y vais si je n’ai pas de voiture ?',
    titre: 'Y aller en bus et en métro depuis Colomiers | Boxing Center',
    description:
      'La 63 finit à Compans-Caffarelli, sur le métro B : Barrière de Paris pour les Minimes, Empalot et le Linéo L5 pour Portet. Le L2 roule aussi le dimanche.',
    menu: true,
    index: true,
    promo: true,
  },
  {
    id: 'contact',
    chemin: '/contact/',
    nav: 'Contact',
    question: 'Je veux poser ma question à quelqu’un.',
    titre: 'Contact | Boxing Center depuis Colomiers',
    description:
      "Une question avant de te déplacer depuis Colomiers ? Écris-nous, on te dit quel club et quel créneau correspondent à ce que tu cherches. Téléphone : 09 39 03 67 48.",
    menu: true,
    index: true,
  },
  {
    id: 'merci',
    chemin: '/merci/',
    nav: 'Merci',
    question: 'Message envoyé.',
    titre: 'Message bien reçu | Boxing Center Colomiers',
    description: 'Ta demande est partie. On te répond rapidement.',
    menu: false,
    index: false,
  },
  {
    id: 'introuvable',
    chemin: '/404/',
    nav: 'Page introuvable',
    question: 'Cette adresse ne mène nulle part.',
    titre: 'Page introuvable | Boxing Center depuis Colomiers',
    description:
      "Cette page n'existe pas ou a changé d'adresse. Voilà les pages du site, et où joindre les deux clubs.",
    menu: false,
    index: false,
  },
  {
    id: 'mentions-legales',
    chemin: '/mentions-legales/',
    nav: 'Mentions légales',
    question: 'Qui édite ce site ?',
    titre: 'Mentions légales | Boxing Center Colomiers',
    description: 'Mentions légales du site boxingcenter-colomiers.fr.',
    menu: false,
    index: false,
  },
  {
    id: 'confidentialite',
    chemin: '/confidentialite/',
    nav: 'Confidentialité',
    question: 'Qu’est-ce que vous faites de mes données ?',
    titre: 'Politique de confidentialité | Boxing Center Colomiers',
    description: 'Ce que devient une demande envoyée depuis boxingcenter-colomiers.fr.',
    menu: false,
    index: false,
  },
] as const;

export function route(id: RouteId): Route {
  const r = ROUTES.find((x) => x.id === id);
  if (!r) throw new Error(`Route inconnue : ${id}`);
  return r;
}

export const MENU = ROUTES.filter((r) => r.menu);

/** Les entrées de navigation ordinaires, hors pages mises en avant. */
export const MENU_SIMPLE = MENU.filter((r) => !r.promo);

/** La page mise en avant, s'il y en a une. */
export const PROMO = ROUTES.find((r) => r.promo);
