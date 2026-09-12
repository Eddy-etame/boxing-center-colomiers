/**
 * CONTENU ÉDITORIAL des pages disciplines — Castelginest.
 *
 * Ces pages visent le même club que celles de L'Union (Boxing Center Toulouse
 * États-Unis). Écrites avec les mêmes phrases, Google les replie l'une sur
 * l'autre et n'en classe qu'une : c'est ce qui arrivait, 82 à 91 % de phrases
 * communes. Chaque page est donc écrite ici depuis Castelginest — la ligne 60,
 * la seconde route par le 15, le collège — et chaque discipline y est prise
 * par d'autres facettes que sur le site frère. Un fait reste un fait : les
 * noms de cours, les âges, les surfaces viennent de clubmma.fr (relevé du
 * 2026-09-10).
 *
 * Deux règles de la loi commune s'appliquent ligne à ligne : aucune figure de
 * style, et aucune réponse qui s'ouvre sur une négation. Aucune heure, aucun
 * prix, aucune durée de trajet : le planning et Tisséo font foi.
 */
import type { MediaSlug } from './medias';
import type { PageDiscipline } from './offres';

export type Bloc = { titre: string; texte: string };

export type Contenu = {
  id: PageDiscipline;
  h1: string;
  chapeau: string;
  photoHero: MediaSlug;
  photoSecondaire: MediaSlug;
  promesse: string;
  blocs: readonly Bloc[];
  seance: readonly string[];
  faq: readonly Bloc[];
};

export const CONTENUS: readonly Contenu[] = [
  {
    id: 'boxe-anglaise',
    h1: 'Boxe anglaise près de Castelginest, sur deux rings de compétition',
    chapeau:
      'Depuis Castelginest, la boxe anglaise se pratique au 388 avenue des États-Unis, dans l’espace Boxe du club : 400 m², deux rings de compétition, du tapis autour. Le club l’écrit sur sa page des disciplines : sans réservation, tous niveaux, coachs diplômés.',
    photoHero: 'boxe-anglaise-castelginest',
    photoSecondaire: 'encadrement-boxe-castelginest',
    promesse: 'La garde, les jambes, puis les poings : la boxe anglaise dans l’ordre où elle s’apprend.',
    blocs: [
      {
        titre: 'La garde vient avant le coup',
        texte:
          'Les mains à hauteur du menton, les coudes près du corps, le menton rentré. Les premières semaines, le coach corrige surtout ça : une garde qui tient pendant tout un round permet ensuite de frapper sans s’ouvrir.',
      },
      {
        titre: 'Les jambes font la moitié du travail',
        texte:
          'Le pas chassé, le pivot, la sortie en diagonale. Sur un ring de compétition, on apprend à régler la distance avec les pieds avant de la régler avec les bras. C’est ce travail qui fatigue le plus au début, et c’est lui qui fait progresser le plus vite.',
      },
      {
        titre: 'Une séance se compte en rounds',
        texte:
          'Le cours alterne l’effort et la récupération, comme un combat. Le souffle se construit ainsi, round après round, au sac, à la corde et aux pattes d’ours avec un coach. L’opposition reste un choix : tu la découvres quand le coach et toi le décidez.',
      },
      {
        titre: 'Du 60 jusqu’au ring',
        texte:
          'Le 60 s’arrête six fois à Castelginest, de l’École jusqu’à Pont Vieil, puis finit à Trois Cocus. Une station de métro B jusqu’à La Vache, et le 59 s’arrête à « États-Unis Fondeyre », l’arrêt du club. En voiture, la D820 puis le périphérique, sortie 33b « Lalande ».',
      },
    ],
    seance: [
      'Corde et déplacements, pour chauffer les chevilles et le souffle',
      'La garde et le pas, travaillés à vide face au coach',
      'Un enchaînement de deux ou trois coups, décomposé puis accéléré',
      'Rounds au sac, puis aux pattes d’ours avec le coach',
      'Gainage, puis étirements du dos et des épaules',
    ],
    faq: [
      {
        titre: 'Où faire de la boxe anglaise près de Castelginest ?',
        texte:
          'Au 388 avenue des États-Unis, à Toulouse, dans l’espace Boxe de Boxing Center : 400 m² et deux rings de compétition. Depuis Castelginest, le 60, une station de métro B, puis le 59.',
      },
      {
        titre: 'Mon ado sort du collège de Castelginest : il y a un groupe pour lui ?',
        texte:
          'Oui : l’école de boxe du club a un groupe 12/16 ans au planning de la salle Boxe, à côté des groupes 3/6 et 7/11 ans.',
      },
      {
        titre: 'Faut-il réserver son cours ?',
        texte:
          'Le club indique « sans réservation » sur sa page des disciplines : tu viens au créneau publié sur le planning Boxe. Pour une toute première fois, la séance d’essai se réserve sur son site.',
      },
      {
        titre: 'Boxe anglaise ou full contact ?',
        texte:
          'La boxe anglaise se pratique aux poings seuls. Le full contact, nouveau dans l’espace Boxe, ajoute les jambes, avec des coups portés au-dessus de la ceinture. Beaucoup commencent par les poings et ajoutent les jambes ensuite.',
      },
    ],
  },
  {
    id: 'mma',
    h1: 'Club MMA près de Castelginest : une cage officielle et 400 m² de tatamis',
    chapeau:
      'Le MMA réunit la boxe debout, les projections et le sol. Depuis Castelginest, il se pratique au 388 avenue des États-Unis, dans la salle MMA du club : une cage surélevée officielle, 400 m² de tatamis, des protections murales. Les cours s’adressent aux débutants comme aux confirmés, et un créneau MMA jeunes 10/16 ans figure au planning.',
    photoHero: 'sparring-boxe-castelginest',
    photoSecondaire: 'ring-de-boxe-castelginest',
    promesse: 'Debout, en projection, au sol : le MMA se construit dans cet ordre, dans une vraie cage.',
    blocs: [
      {
        titre: 'Une salle MMA à proximité de Castelginest',
        texte:
          'La salle MMA est l’un des trois espaces de 400 m² du club. La cage y est surélevée et officielle, les murs sont protégés, et des panneaux de séparation permettent de travailler le cage control sans occuper toute la cage.',
      },
      {
        titre: 'Le cours suit l’ordre du combat',
        texte:
          'On commence debout, avec les coups de la boxe et du Muay Thai, puis on travaille la projection, puis le sol. Un débutant apprend d’abord à tomber et à se relever, avant d’apprendre à amener l’autre au sol.',
      },
      {
        titre: 'Grappling et jiu-jitsu brésilien',
        texte:
          'Deux cours publiés à part au planning de la salle MMA, où le sol se travaille sans frappe : contrôles, renversements, soumissions. Beaucoup de pratiquants de MMA les suivent en plus de leur cours, pour le travail au sol.',
      },
      {
        titre: 'La seconde route : le 15',
        texte:
          'Depuis Castelginest, le 60 rejoint le métro à Trois Cocus. La première route continue d’une station jusqu’à La Vache, où le 59 prend le relais. La seconde descend de deux stations jusqu’à Barrière de Paris, où le 15 finit sa ligne à « États-Unis Fondeyre », du lundi au samedi.',
      },
    ],
    seance: [
      'Échauffement au sol : roulades, sorties de hanche, relevés',
      'Debout : un enchaînement pieds-poings, travaillé à deux',
      'Une projection, décomposée, puis la chute qui va avec',
      'Au sol : une position, et la façon d’en sortir',
      'Mise en situation encadrée contre la paroi de la cage',
    ],
    faq: [
      {
        titre: 'Où est le club de MMA le plus proche de Castelginest ?',
        texte:
          'Au 388 avenue des États-Unis, à Toulouse : Boxing Center y a une cage surélevée officielle et 400 m² de tatamis. Depuis Castelginest, le 60, le métro B, puis le 59 ou le 15.',
      },
      {
        titre: 'À partir de quel âge pour le MMA ?',
        texte:
          'Le club publie un créneau MMA jeunes 10/16 ans au planning de la salle MMA. Les cours adultes accueillent les débutants comme les confirmés.',
      },
      {
        titre: 'Il faut savoir boxer avant de faire du MMA ?',
        texte:
          'Tu peux commencer directement : le cours reprend les bases debout à chaque séance. Certains ajoutent un cours de boxe anglaise ou de pieds-poings dans l’espace Boxe, à côté.',
      },
      {
        titre: 'Quelle tenue pour le premier cours ?',
        texte:
          'Une tenue de sport près du corps, sans fermeture ni bijou, et une bouteille d’eau. Pour les protections, le club t’indique quoi prendre après la séance d’essai.',
      },
    ],
  },
  {
    id: 'boxe-pieds-poings',
    h1: 'Kick-boxing, boxe thaï et boxe pieds-poings près de Castelginest',
    chapeau:
      'Au planning de la salle Boxe, le club publie « Pieds-Poings / Kick ». Sur sa page des disciplines, il présente aussi le Muay Thai, la boxe thaïlandaise, et le full contact, nouveau dans l’espace Boxe. Depuis Castelginest, les trois se pratiquent au 388 avenue des États-Unis, sur deux rings de compétition.',
    photoHero: 'sac-de-frappe-castelginest',
    photoSecondaire: 'club-boxe-castelginest',
    promesse: 'Chaque règlement ajoute des coups : les jambes au kick-boxing, les coudes et les genoux au Muay Thai.',
    blocs: [
      {
        titre: 'Le club de kick-boxing le plus proche de Castelginest',
        texte:
          'Le kick-boxing ajoute les coups de pied aux coups de poing, en garde haute. Au club, il figure au planning de la salle Boxe sous le nom « Pieds-Poings / Kick », à côté de la boxe anglaise et de l’école de boxe.',
      },
      {
        titre: 'Un club de boxe thaï près de Castelginest',
        texte:
          'Le club présente le Muay Thai comme l’art des huit membres : les poings, les pieds, les coudes, les genoux, avec le clinch et les projections. C’est la discipline la plus exigeante pour les jambes et le gainage.',
      },
      {
        titre: 'Le full contact vise le haut du corps',
        texte:
          'Dans ce règlement, les coups de pied visent le haut du corps, jamais les jambes. Il vient d’arriver dans l’espace Boxe du club, et il se travaille avec les mêmes bases que le kick-boxing : la garde, l’appui, la distance.',
      },
      {
        titre: 'Les hanches et les tibias travaillent',
        texte:
          'Un coup de pied part de la hanche et se porte avec le tibia. Les premières séances insistent sur la mobilité, l’équilibre sur une jambe et le retour en garde. La souplesse vient avec les étirements de fin de cours.',
      },
    ],
    seance: [
      'Corde, puis mobilité des hanches et des chevilles',
      'Un coup de pied, travaillé lentement, puis enchaîné derrière un direct',
      'Rounds au sac, poings et jambes',
      'Pattes d’ours et paos avec le coach, pour la précision',
      'Gainage, et étirements longs des jambes',
    ],
    faq: [
      {
        titre: 'Où faire du kick-boxing près de Castelginest ?',
        texte:
          'Au 388 avenue des États-Unis, dans l’espace Boxe : le cours s’appelle « Pieds-Poings / Kick » au planning. Depuis Castelginest, le 60 jusqu’au métro, puis le 59.',
      },
      {
        titre: 'Et la boxe thaï ?',
        texte:
          'Le club la publie sous le nom « Muay Thai (Boxe Thaïlandaise) ». Ses créneaux figurent sur les plannings, à consulter sur le site du club.',
      },
      {
        titre: 'Je commence à trente ou quarante ans, c’est possible ?',
        texte:
          'Oui : le club accueille tous les niveaux, et le coach adapte les exercices. La plupart des adultes commencent au sac et aux paos, et l’opposition vient plus tard, s’ils la veulent.',
      },
      {
        titre: 'Quel matériel pour les jambes ?',
        texte:
          'Pour découvrir, une tenue de sport suffit. Si tu continues, des protège-tibias et des gants : le club te dira quels modèles prendre.',
      },
    ],
  },
  {
    id: 'boxe-enfants',
    h1: 'Boxe enfant près de Castelginest : l’école de boxe, de 3 à 16 ans',
    chapeau:
      'L’école de boxe du club accueille trois groupes : 3/6 ans, 7/11 ans et 12/16 ans, au planning de la salle Boxe. Dans la salle MMA, un créneau MMA jeunes réunit les 10/16 ans. Tout se passe au 388 avenue des États-Unis, en touché contrôlé.',
    photoHero: 'entrainement-boxe-castelginest',
    photoSecondaire: 'garde-boxe-castelginest',
    promesse: 'Un groupe par âge, une règle pour tous : on touche, on contrôle, on s’arrête au signal.',
    blocs: [
      {
        titre: 'Trois âges, trois façons de travailler',
        texte:
          'Chez les 3/6 ans, la boxe passe par le jeu : l’équilibre, la coordination, la distance. Chez les 7/11 ans, les gestes se précisent. Chez les 12/16 ans, le travail ressemble à celui des adultes, avec plus de technique et de souffle.',
      },
      {
        titre: 'Le MMA jeunes, à partir de 10 ans',
        texte:
          'Le club publie un créneau MMA jeunes 10/16 ans dans la salle MMA, sur les tatamis. Les jeunes y travaillent la chute, les contrôles et les bases debout.',
      },
      {
        titre: 'Le touché contrôlé, expliqué aux parents',
        texte:
          'Les enfants touchent la cible sans appuyer le coup. Le coach arrête l’exercice au signal, et l’enfant apprend à doser avant d’apprendre à frapper fort. Les protections sont adaptées à la taille.',
      },
      {
        titre: 'Depuis Castelginest, pour un parent',
        texte:
          'Le 60 part de Castelginest et rejoint le métro à Trois Cocus ; une station plus loin, le 59 dessert l’avenue des États-Unis. En voiture, la D820 puis le périphérique, sortie 33b « Lalande ».',
      },
    ],
    seance: [
      'Échauffement en jeu : attraper, esquiver, réagir au signal',
      'La garde et la distance, montrées puis imitées',
      'Un geste simple, répété et corrigé enfant par enfant',
      'Travail aux pattes d’ours, en touché contrôlé',
      'Retour au calme, et le récapitulatif du coach',
    ],
    faq: [
      {
        titre: 'Dès quel âge mon enfant peut-il commencer ?',
        texte:
          'L’école de boxe du club commence avec le groupe 3/6 ans. Pour le MMA, le créneau jeunes accueille les 10/16 ans.',
      },
      {
        titre: 'Mon enfant va-t-il recevoir des coups ?',
        texte:
          'Le travail se fait en touché contrôlé : la cible est effleurée, le geste est dosé, et le coach arrête au signal. Les protections sont adaptées à l’âge.',
      },
      {
        titre: 'Boxe ou MMA pour un enfant de 11 ans ?',
        texte:
          'Les deux existent pour cet âge : le groupe 7/11 ans de l’école de boxe, et le MMA jeunes à partir de 10 ans. Une séance d’essai dans chacun permet de choisir avec lui.',
      },
      {
        titre: 'Que met-il dans son sac ?',
        texte:
          'Une tenue de sport, une bouteille d’eau et des chaussures propres pour la salle. Pour les gants, le club indique quoi prendre après les premières séances.',
      },
    ],
  },
  {
    id: 'preparation-physique',
    h1: 'Préparation physique près de Castelginest : Hyrox, cross-training et seize sacs',
    chapeau:
      'Le troisième espace du club, 400 m², est consacré à la condition physique : seize sacs de frappe, une cage de street workout, la musculation et le cardio. Au planning Fitness, le club publie l’Hyrox, le Boxing HIIT, le Cross-Training et le Lady Punch. L’accès libre est ouvert six jours sur sept aux membres.',
    photoHero: 'preparation-physique-castelginest',
    photoSecondaire: 'sac-de-frappe-castelginest',
    promesse: 'La condition physique d’un boxeur, travaillée au sac, à la barre et au chrono.',
    blocs: [
      {
        titre: 'Seize sacs pour un groupe entier',
        texte:
          'Avec seize sacs de frappe dans le même espace, tout un groupe travaille en même temps. Le Boxing HIIT les utilise en circuit : des séries courtes et intenses, sans adversaire.',
      },
      {
        titre: 'Lady Punch, entre femmes',
        texte:
          'Le cours Boxing Lady du club est exclusivement féminin et sans opposition. Il figure au planning Fitness sous le nom « Lady Punch ».',
      },
      {
        titre: 'Hyrox et cross-training',
        texte:
          'L’Hyrox prépare au format de course en salle, en cours mixtes, du débutant au confirmé. Le cross-training combine haltérophilie, gymnastique et cardio.',
      },
      {
        titre: 'La cage de street workout',
        texte:
          'Tractions, dips et gainage au poids du corps : la cage de street workout est en accès libre, avec la musculation et le cardio, six jours sur sept pour les membres.',
      },
    ],
    seance: [
      'Échauffement au rameur ou au vélo',
      'Circuit au sac : séries courtes, récupération courte',
      'Renforcement au poids du corps dans la cage de street workout',
      'Un bloc de charges, la technique d’abord',
      'Étirements et respiration pour finir',
    ],
    faq: [
      {
        titre: 'Où faire de la préparation physique près de Castelginest ?',
        texte:
          'Au 388 avenue des États-Unis : le club consacre un espace de 400 m² à la condition physique. Depuis Castelginest, le 60, une station de métro B, puis le 59.',
      },
      {
        titre: 'Le Lady Punch, c’est quoi ?',
        texte:
          'Le nom du cours Boxing Lady au planning Fitness : exclusivement féminin, sans opposition.',
      },
      {
        titre: 'Je peux m’entraîner en dehors des cours ?',
        texte:
          'Oui : l’accès libre est ouvert aux membres six jours sur sept, pour la musculation, le cardio, le cross-training et le street workout. Les conditions dépendent de l’abonnement, sur le site du club.',
      },
      {
        titre: 'L’Hyrox, pour un débutant ?',
        texte:
          'Le club indique des cours mixtes, du débutant au confirmé. Le coach adapte les charges et les distances.',
      },
    ],
  },
] as const;

export const contenu = (id: PageDiscipline): Contenu => {
  const c = CONTENUS.find((x) => x.id === id);
  if (!c) throw new Error(`Contenu inconnu : ${id}`);
  return c;
};
