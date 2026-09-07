/**
 * REGISTRE DES ROUTES — une page = une question humaine distincte.
 *
 * Aucune URL n'est écrite en dur ailleurs dans le projet : on passe par
 * `route('mma')`. Renommer une page ne casse alors rien.
 *
 * Le titre et la description vivent ici parce qu'ils font partie de
 * l'architecture de recherche, pas de la mise en page.
 */

export type RouteId =
  | 'accueil'
  | 'boxe-anglaise'
  | 'mma'
  | 'boxing-fitness'
  | 'boxe-enfants'
  | 'plannings'
  | 'tarifs'
  | 'contact'
  | 'merci'
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
};

export const ROUTES: readonly Route[] = [
  {
    id: 'accueil',
    chemin: '/',
    nav: 'Accueil',
    question: 'Où pratiquer la boxe ou le MMA quand on habite à Colomiers ?',
    titre: 'Club de boxe et MMA près de Colomiers | Boxing Center',
    description:
      "Tu habites Colomiers et tu cherches un club de boxe, de MMA ou de sport de combat ? Boxing Center accueille les Columérins dans ses clubs de Toulouse Minimes et Portet-sur-Garonne, 6 jours sur 7 de 10h à 21h15.",
    menu: true,
    index: true,
  },
  {
    id: 'boxe-anglaise',
    chemin: '/boxe-anglaise/',
    nav: 'Boxe anglaise',
    question: 'À quoi ressemble un cours de boxe anglaise, et est-ce que je peux commencer ?',
    titre: 'Boxe anglaise près de Colomiers — cours débutants et confirmés | Boxing Center',
    description:
      "Cours de boxe anglaise accessibles depuis Colomiers, pour débutants comme pour confirmés. Encadrement diplômé, matériel prêté à l'essai, clubs Boxing Center à Toulouse Minimes et Portet-sur-Garonne.",
    menu: true,
    index: true,
  },
  {
    id: 'mma',
    chemin: '/mma/',
    nav: 'MMA',
    question: 'Où faire du MMA quand on part de Colomiers, et comment on commence ?',
    titre: 'Club de MMA près de Colomiers — cours tous niveaux | Boxing Center',
    description:
      'Tu cherches un club de MMA près de Colomiers ? Boxing Center propose le MMA à Toulouse Minimes et Portet-sur-Garonne : frappe, corps à corps, sol, avec un encadrement qui construit les débutants.',
    menu: true,
    index: true,
  },
  {
    id: 'boxing-fitness',
    chemin: '/boxing-fitness/',
    nav: 'Boxing Fitness & Femme',
    question: 'Je veux boxer pour la forme, sans prendre de coup. C’est possible ?',
    titre: 'Boxing fitness et boxe femme près de Colomiers | Boxing Center',
    description:
      "Boxing fitness accessible depuis Colomiers : cardio, geste de boxe, défoulement, sans opposition ni obligation de combattre. Un cadre pensé pour les débutantes et les débutants.",
    menu: true,
    index: true,
  },
  {
    id: 'boxe-enfants',
    chemin: '/boxe-enfants/',
    nav: 'Boxe enfants',
    question: 'Quelle boxe pour mon enfant, et est-ce que c’est sans danger ?',
    titre: 'Boxe enfant près de Colomiers — boxe éducative encadrée | Boxing Center',
    description:
      "Cours de boxe enfant accessibles depuis Colomiers. Boxe éducative : le geste, le cadre, le respect. Encadrement diplômé aux clubs Boxing Center de Toulouse Minimes et Portet-sur-Garonne.",
    menu: true,
    index: true,
  },
  {
    id: 'plannings',
    chemin: '/plannings/',
    nav: 'Plannings',
    question: 'Quand est-ce que je peux m’entraîner, avec mes horaires à moi ?',
    titre: 'Plannings et horaires des cours près de Colomiers | Boxing Center',
    description:
      "Les clubs Boxing Center accueillent 6 jours sur 7, de 10h à 21h15. Retrouve les créneaux qui collent à tes journées et accède aux plannings détaillés de Toulouse Minimes et Portet-sur-Garonne.",
    menu: true,
    index: true,
  },
  {
    id: 'tarifs',
    chemin: '/tarifs/',
    nav: 'Tarifs',
    question: 'Combien ça coûte, et qu’est-ce qui est compris ?',
    titre: 'Tarifs des cours de boxe et MMA près de Colomiers | Boxing Center',
    description:
      "Ce que coûte la pratique de la boxe ou du MMA depuis Colomiers, ce qui est compris dans une adhésion, et où consulter les tarifs à jour des clubs Boxing Center Toulouse Minimes et Portet-sur-Garonne.",
    menu: true,
    index: true,
  },
  {
    id: 'contact',
    chemin: '/contact/',
    nav: 'Contact',
    question: 'Je veux poser ma question à quelqu’un.',
    titre: 'Contact — poser sa question avant de venir | Boxing Center Colomiers',
    description:
      "Une question avant de te déplacer depuis Colomiers ? Écris-nous, on te dit quel club et quel créneau correspondent à ce que tu cherches. Téléphone : 05 62 24 46 82.",
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
    id: 'mentions-legales',
    chemin: '/mentions-legales/',
    nav: 'Mentions légales',
    question: 'Qui édite ce site ?',
    titre: 'Mentions légales | Boxing Center Colomiers',
    description: 'Mentions légales du site boxingcenter-colomiers.fr.',
    menu: false,
    index: true,
  },
  {
    id: 'confidentialite',
    chemin: '/confidentialite/',
    nav: 'Confidentialité',
    question: 'Qu’est-ce que vous faites de mes données ?',
    titre: 'Politique de confidentialité | Boxing Center Colomiers',
    description: 'Ce que devient une demande envoyée depuis boxingcenter-colomiers.fr.',
    menu: false,
    index: true,
  },
] as const;

export function route(id: RouteId): Route {
  const r = ROUTES.find((x) => x.id === id);
  if (!r) throw new Error(`Route inconnue : ${id}`);
  return r;
}

export const MENU = ROUTES.filter((r) => r.menu);
