/**
 * CONTENU ÉDITORIAL des pages disciplines.
 *
 * Ton : clair, local, rassurant, sportif, accessible, professionnel — jamais
 * agressif ni compétitif (cahier des charges §14). Tutoiement respectueux.
 * On répond avant de vendre : chaque bloc part d'une question que la personne
 * se pose vraiment, pas d'un argument qu'on veut placer.
 *
 * Aucun fait volatil ici (horaires, prix, âges) : ceux-là vivent dans
 * verite.ts et n'existent qu'à un seul endroit.
 */

import type { MediaSlug } from './medias';

export type Bloc = { titre: string; texte: string };

export type Contenu = {
  id: 'boxe-anglaise' | 'mma' | 'boxing-fitness' | 'boxe-enfants';
  h1: string;
  /** La réponse immédiate, avant tout le reste. Ce que lisent Google et les IA. */
  chapeau: string;
  photoHero: MediaSlug;
  photoSecondaire: MediaSlug;
  /**
   * La paire noir-et-blanc / couleur du même instant. Le photographe a
   * réellement pris ces images deux fois : la couleur qui arrive au scroll
   * n'est pas un filtre qu'on retire, ce sont deux vraies prises.
   * Absent = la page n'a pas de bascule.
   */
  bascule?: 'garde' | 'paos' | 'corps';
  /** ce que le visiteur gagne concrètement — sert la bande de conversion */
  promesse: string;
  /** Le corps de la page : des questions, pas des rubriques. */
  blocs: readonly Bloc[];
  /** Ce que la séance contient réellement, dans l'ordre. */
  seance: readonly string[];
  /** Questions fréquentes — vraies questions, réponses honnêtes. */
  faq: readonly Bloc[];
};

export const CONTENUS: readonly Contenu[] = [
  {
    id: 'boxe-anglaise',
    bascule: 'garde',
    promesse:
      "Apprendre à boxer pour de vrai, encadré, sans avoir à prouver quoi que ce soit à personne.",
    h1: 'Cours de boxe anglaise à proximité de Colomiers, débutants et confirmés',
    chapeau:
      "La boxe anglaise se pratique aux poings, avec des gants, dans un cadre encadré. Aucun niveau n'est demandé pour commencer. Les deux clubs Boxing Center accessibles depuis Colomiers la proposent : Toulouse Minimes distingue un groupe loisir et un groupe compétiteurs et publie aussi la boxe pieds-poings ; Portet-sur-Garonne propose la boxe anglaise et le kick-boxing. Ouverts 6 jours sur 7, de 10h à 21h15.",
    photoHero: 'boxe-anglaise-colomiers-technique',
    photoSecondaire: 'deplacement-boxe-anglaise-colomiers',
    blocs: [
      {
        titre: 'C’est quoi, concrètement, la boxe anglaise',
        texte:
          "Uniquement les poings. Pas de pied, pas de genou, pas de sol. Ce qui paraît une limite est en réalité ce qui rend la discipline si dense : quand on ne dispose que de quatre coups, tout se joue dans les déplacements, la distance, la garde et la lecture de l’autre. C’est un sport de placement bien plus que de puissance, et c’est exactement pour ça qu’une personne qui n’a jamais fait de sport peut y progresser vite.",
      },
      {
        titre: 'Est-ce que je vais prendre des coups dès le premier jour',
        texte:
          "Non. L’opposition n’est pas le point de départ, c’est une étape qui arrive plus tard, et seulement pour ceux qui la souhaitent. Un débutant travaille au sac, à la corde, aux pattes d’ours avec un coach, et sur le déplacement à vide. Beaucoup de pratiquants s’entraînent des mois sans jamais faire d’opposition — et progressent énormément.",
      },
      {
        titre: 'Ce que ça change dans une semaine ordinaire',
        texte:
          "Deux séances par semaine suffisent à sentir une différence en un mois : sur le souffle d’abord, sur la posture ensuite, sur la façon de gérer la fatigue enfin. La boxe a ceci de particulier qu’elle occupe complètement la tête : il est très difficile de penser à sa journée de travail pendant un round au sac. Beaucoup viennent au départ pour la forme et restent pour cette raison-là.",
      },
      {
        titre: 'Depuis Colomiers, quel club viser',
        texte:
          "Les deux clubs Boxing Center proposent la boxe anglaise avec un encadrement diplômé. Le vrai critère n’est pas la discipline, c’est ton trajet : Toulouse Minimes est sur l’axe nord-est, pratique en sortie de journée ; Portet-sur-Garonne est au sud de l’agglomération, plus simple d’accès en voiture et pour se garer. Ce qui tient sur la durée, c’est le club où tu iras même les soirs où tu n’en as pas envie.",
      },
    ],
    seance: [
      'Échauffement : corde, mobilité, déplacements à vide',
      'Technique : un geste, décomposé, répété lentement puis en rythme',
      'Sac ou pattes d’ours : l’application du geste, avec correction du coach',
      'Renforcement : gainage, abdominaux, travail au poids du corps',
      'Retour au calme et étirements',
    ],
    faq: [
      {
        titre: 'Il me faut du matériel pour la première séance ?',
        texte:
          "Une tenue de sport, une bouteille d’eau, et c’est tout pour découvrir. Pour les gants et les bandes, demande directement au club : les conditions de prêt sont propres à chaque salle et c’est le club qui a l’information à jour.",
      },
      {
        titre: 'J’ai plus de 40 ans, c’est trop tard ?',
        texte:
          "Non. La boxe se pratique à l’intensité qu’on lui donne. Un coach adapte le volume et l’intensité au pratiquant qu’il a devant lui, et la salle accueille des profils très différents dans la même séance.",
      },
      {
        titre: 'Je suis vraiment pas en forme. Je vais être ridicule ?',
        texte:
          "Tout le monde a été le débutant essoufflé du fond de la salle. C’est même la situation la plus banale d’un club de boxe : personne ne regarde, tout le monde est occupé à sa propre séance.",
      },
    ],
  },

  {
    id: 'mma',
    bascule: 'corps',
    promesse:
      "La discipline la plus complète, construite étape par étape, même en partant de zéro.",
    h1: 'Club de MMA à proximité de Colomiers : cap sur Portet-sur-Garonne',
    chapeau:
      "Le MMA combine la frappe debout, le corps à corps et le travail au sol. Dans le réseau Boxing Center, c’est à Portet-sur-Garonne que le MMA se pratique, avec le grappling, le jiu-jitsu brésilien et le kick-boxing, dans une salle équipée d’une cage. C’est donc le club de MMA à retenir depuis Colomiers, ouvert 6 jours sur 7 de 10h à 21h15, et il accueille les débutants.",
    photoHero: 'mma-colomiers-boxing-center',
    photoSecondaire: 'travail-au-corps-boxe-colomiers',
    blocs: [
      {
        titre: 'Pourquoi le MMA fait peur, et pourquoi c’est un malentendu',
        texte:
          "L’image publique du MMA vient des combats professionnels : une cage, deux athlètes préparés, et une intensité qui n’a rien à voir avec un entraînement. Un cours de MMA en club, c’est autre chose : de la technique décomposée, des répétitions à vitesse lente, du travail de placement, et une progression par étapes. Ce qu’on voit à la télévision est le sommet d’une pyramide dont la base est un cours d’apprentissage tout à fait ordinaire.",
      },
      {
        titre: 'Les trois zones à apprendre, et dans quel ordre',
        texte:
          "Le MMA se décompose en trois distances. Debout, c’est la frappe : poings, pieds, genoux, avec la même logique de distance et de garde qu’en boxe. Au corps à corps, c’est le clinch et les projections : le travail de déséquilibre. Au sol, c’est le contrôle, les positions et les soumissions. Un débutant n’attaque pas les trois de front — on construit une zone après l’autre.",
      },
      {
        titre: 'Ce qu’il faut vraiment pour commencer',
        texte:
          "Pas de niveau, pas de condition physique préalable, pas d’expérience d’un autre sport de combat. Ce qu’il faut, c’est accepter de mal faire pendant plusieurs semaines. Le MMA est la discipline où la sensation d’incompétence dure le plus longtemps, parce qu’il y a le plus de choses à intégrer — et c’est aussi celle où les progrès sont les plus visibles une fois le cap passé.",
      },
      {
        titre: 'Quel club de MMA viser depuis Colomiers',
        texte:
          "Boxing Center Portet-sur-Garonne. C’est le club du réseau qui publie le MMA, et il ne le publie pas seul : le grappling, le jiu-jitsu brésilien et le kick-boxing y figurent aussi, avec une cage pour le travail spécifique. Depuis Colomiers, c’est la descente vers le sud de l’agglomération, sur la route d’Espagne, avec du stationnement simple. Toulouse Minimes, l’autre club accessible depuis Colomiers, est orienté boxe anglaise — loisir, compétition et pieds-poings : c’est là qu’il faut aller si c’est la boxe qui t’intéresse.",
      },
      {
        titre: 'MMA, grappling, JJB : quelle différence',
        texte:
          "Le grappling, c’est la lutte et les soumissions sans frappe, en short et rashguard. Le jiu-jitsu brésilien travaille le même terrain avec le kimono et un système de ceintures. Le MMA réunit les deux et y ajoute la frappe debout. Beaucoup de pratiquants commencent par le grappling parce qu’on n’y prend aucun coup : c’est une porte d’entrée très sûre vers le MMA, et Portet propose les deux.",
      },
      {
        titre: 'Un club sérieux, ça se reconnaît à quoi',
        texte:
          "À l’encadrement, et à rien d’autre. Un cours de MMA sans coach qui corrige, sans progression, sans règles claires sur l’intensité, c’est du risque inutile. C’est le point à vérifier avant de choisir un club — pas le matériel, pas la décoration, pas la taille de la salle.",
      },
    ],
    seance: [
      'Échauffement articulaire complet : le MMA sollicite tout le corps',
      'Technique debout : frappe, distance, déplacement',
      'Technique au sol ou clinch selon le cycle en cours',
      'Mise en situation contrôlée, à intensité réduite',
      'Renforcement spécifique et retour au calme',
    ],
    faq: [
      {
        titre: 'Est-ce que je vais me battre au premier cours ?',
        texte:
          "Non. Une première séance sert à apprendre à tomber, à se placer et à répéter des gestes lentement. L’opposition, même souple, arrive une fois les bases posées.",
      },
      {
        titre: 'Je viens de la boxe, est-ce que ça m’aide ?',
        texte:
          "Beaucoup, sur la partie debout. Il te restera le corps à corps et le sol à construire, ce qui prend du temps mais part d’une bonne base de distance et de garde.",
      },
      {
        titre: 'Quelles disciplines exactement sont proposées par club ?',
        texte:
          "L’offre exacte peut évoluer d’un club à l’autre et d’une saison à l’autre. Consulte directement le site du club visé, ou écris-nous : on te répond avec l’information à jour plutôt qu’avec une liste approximative.",
      },
    ],
  },

  {
    id: 'boxing-fitness',
    bascule: 'paos',
    promesse:
      "Le cardio et le défoulement de la boxe, sans opposition et sans obligation de combattre.",
    h1: 'Boxing fitness, cardio boxing et boxe femme à proximité de Colomiers',
    chapeau:
      "Le boxing fitness reprend les gestes de la boxe — frappe, déplacement, garde — sans aucune opposition. Les deux clubs Boxing Center accessibles depuis Colomiers le proposent : Cardio Boxing et Boxing Lady, créneau 100 % féminin, à Toulouse Minimes ; Lady Boxing et préparation physique à Portet-sur-Garonne. Une pratique de cardio et de remise en forme, ouverte à toutes et à tous.",
    photoHero: 'boxing-fitness-colomiers',
    photoSecondaire: 'preparation-physique-boxe-colomiers',
    blocs: [
      {
        titre: 'La différence, en une phrase',
        texte:
          "En boxe, il y a quelqu’un en face. En boxing fitness, il y a un sac, un coach avec des pattes d’ours, ou simplement le vide. Le geste est le même, l’intensité est la même, la dépense est la même — l’opposition en moins. C’est cette seule différence qui fait que beaucoup de gens franchissent la porte d’un club de boxe alors qu’ils ne l’auraient jamais fait autrement.",
      },
      {
        titre: 'Pourquoi ça marche mieux qu’une salle de sport classique',
        texte:
          "Parce qu’on ne compte pas les répétitions. Un round dure trois minutes, il y a un objectif technique, un coach qui donne le rythme, et la tête est occupée du début à la fin. La séance passe. C’est le contraire d’un tapis de course où chaque minute se voit. Sur la durée, c’est cette différence-là qui fait qu’on continue.",
      },
      {
        titre: 'Pour les femmes qui hésitent à pousser la porte',
        texte:
          "L’appréhension est réelle et elle est légitime : un club de boxe a une réputation d’endroit masculin et fermé. Dans les faits, les cours de boxing fitness sont fréquentés par un public très mixte, et l’encadrement est le même pour tout le monde. Personne ne teste personne. Si l’idée d’arriver seule est ce qui bloque, dis-le dans ton message : on te répondra en te disant précisément quel créneau et quel club conviennent le mieux pour une première fois.",
      },
      {
        titre: 'Et si je veux basculer vers la boxe plus tard',
        texte:
          "C’est exactement le chemin que beaucoup prennent. Le boxing fitness construit le geste, le souffle et la confiance ; passer ensuite sur un cours de boxe anglaise devient une simple continuation. Il n’y a pas de mur entre les deux, et rien ne t’oblige jamais à franchir cette étape.",
      },
    ],
    seance: [
      'Échauffement cardio : corde, déplacements, mobilité',
      'Apprentissage ou rappel du geste de la séance',
      'Rounds au sac : le cœur de la séance, en intervalles',
      'Circuit de renforcement au poids du corps',
      'Étirements et retour au calme',
    ],
    faq: [
      {
        titre: 'Je ne veux vraiment jamais faire d’opposition. C’est possible ?',
        texte:
          'Oui. Le boxing fitness est conçu sans opposition. Personne ne te poussera à en faire, ni au premier cours ni au centième.',
      },
      {
        titre: 'Il faut être en forme pour commencer ?',
        texte:
          "Non — c’est le sens même de la discipline. L’intensité se règle : tu frappes moins vite, tu récupères plus longtemps, et tu suis la séance à ton rythme.",
      },
      {
        titre: 'Est-ce que c’est un cours réservé aux femmes ?',
        texte:
          'Cela dépend des créneaux et des clubs. Pour connaître l’offre exacte du club qui t’intéresse, consulte son site ou écris-nous.',
      },
    ],
  },

  {
    id: 'boxe-enfants',
    promesse:
      "Un cadre qui apprend le geste, la maîtrise et le respect — et ça se voit hors de la salle.",
    h1: 'Boxe enfant à proximité de Colomiers : Baby Boxe et boxe éducative',
    chapeau:
      "La boxe éducative apprend le geste, la distance et le respect de l'adversaire, sans mise en danger. C'est un cadre, pas un ring. Les deux clubs Boxing Center accessibles depuis Colomiers proposent la Baby Boxe — dès 3 ans à Toulouse Minimes — et la boxe éducative ; Portet-sur-Garonne ajoute un créneau kick-boxing enfants et ados. Encadrement diplômé dans les deux cas.",
    photoHero: 'cours-collectifs-boxe-colomiers',
    photoSecondaire: 'encadrement-coach-boxe-colomiers',
    blocs: [
      {
        titre: 'La question que tous les parents posent en premier',
        texte:
          "« Est-ce qu’il va prendre des coups ? » La réponse est non. La boxe éducative est une pratique codifiée dans laquelle la puissance est proscrite : on touche, on ne frappe pas. L’objectif pédagogique est le contrôle — savoir s’arrêter, doser, respecter la distance et l’intégrité de l’autre. Un enfant qui frappe fort en boxe éducative est corrigé, pas encouragé.",
      },
      {
        titre: 'Ce que la boxe apprend, en dehors de la boxe',
        texte:
          "Se tenir droit. Regarder quelqu’un en face. Attendre son tour. Accepter une correction sans le prendre pour soi. Recommencer un geste raté vingt fois. Serrer la main de celui d’en face à la fin. Ce sont ces choses-là que les parents constatent en premier, souvent avant tout progrès technique — et elles se transportent hors de la salle.",
      },
      {
        titre: 'Pour l’enfant trop timide, pour l’enfant trop énergique',
        texte:
          "Les deux profils y trouvent leur compte, pour des raisons opposées. L’enfant réservé y gagne une confiance qui ne dépend de personne d’autre que lui. L’enfant qui déborde d’énergie trouve un cadre où cette énergie a enfin une destination et des règles. C’est le même cours, et il fonctionne dans les deux sens.",
      },
      {
        titre: 'Ce qu’il faut vérifier avant d’inscrire',
        texte:
          "Les tranches d’âge exactes, les créneaux et les conditions d’inscription sont propres à chaque club et évoluent d’une saison à l’autre. Ne te fie pas à une information générale : consulte le site du club visé, ou écris-nous en précisant l’âge de ton enfant — on te répondra avec ce qui existe réellement pour lui.",
      },
    ],
    seance: [
      'Échauffement sous forme de jeu : déplacements, réactivité',
      'Apprentissage technique : un geste, décomposé et répété',
      'Exercices à deux, sous contrôle permanent du coach',
      'Jeux d’opposition codifiés, sans puissance',
      'Retour au calme et salut',
    ],
    faq: [
      {
        titre: 'À partir de quel âge ?',
        texte:
          'Les tranches d’âge varient selon les clubs et les saisons. Écris-nous avec l’âge de ton enfant, ou consulte directement le site du club : c’est la seule information fiable.',
      },
      {
        titre: 'Est-ce que ça rend les enfants violents ?',
        texte:
          "L’effet observé est l’inverse. La boxe éducative enseigne d’abord à se contenir : un enfant qui apprend à contrôler un geste apprend aussi à ne pas l’utiliser. Le cadre, l’autorité du coach et le salut de fin de séance font partie de l’apprentissage.",
      },
      {
        titre: 'Mon enfant peut essayer avant de s’inscrire ?',
        texte:
          'Les conditions d’essai relèvent de chaque club. Pose la question directement au club visé, ou passe par notre formulaire et on te met en relation.',
      },
    ],
  },
] as const;

export function contenu(id: Contenu['id']): Contenu {
  const c = CONTENUS.find((x) => x.id === id);
  if (!c) throw new Error(`Contenu inconnu : ${id}`);
  return c;
}
