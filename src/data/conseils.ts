/**
 * LES CONSEILS — le texte des articles sur le matériel (/conseils/).
 *
 * Écrit pour ce site, et pour lui seul : aucune phrase d'ici n'existe sur un
 * autre site du réseau. Chaque conseil part de ce que les clubs publient
 * (src/data/offres.ts) et renvoie, depuis son texte, vers la boutique de
 * matériel du groupe, vers les pages du site et vers le club. Le titre et la
 * description de chaque page vivent dans le registre des routes.
 *
 * Les prix cités portent leur date ; « maj » est la date de la dernière
 * relecture du conseil, affichée sur la page.
 */

export type ConseilId = 'poids-gants-de-boxe' | 'materiel-cardio-boxing';

export type Conseil = {
  id: ConseilId;
  /** l'étiquette de la carte, sur l'index */
  carte: string;
  h1: string;
  /** la réponse, en deux phrases qui se lisent seules */
  chapeau: string;
  resume: string;
  photo: string;
  /** la ligne de la vignette de partage */
  sujet: string;
  publie: string;
  maj: string;
  sections: readonly { sur: string; h2: string; paras: readonly string[] }[];
  tableau?: { sur: string; h2: string; entetes: readonly string[]; lignes: readonly (readonly string[])[]; note: string };
  faq: readonly { titre: string; texte: string }[];
};

export const INDEX_CONSEILS = {
  h1: 'Le matériel de boxe, expliqué avant d’acheter.',
  chapeau: 'Deux questions reviennent chez celles et ceux qui partent de Colomiers pour s’entraîner : quel poids de gants choisir, et que faut-il pour un cours sans opposition. Chaque conseil y répond, chiffres à l’appui.',
  photo: 'sport-combat-colomiers-sac-frappe',
  sujet: 'Conseils matériel · depuis',
  finH2: 'Le plus simple reste d’essayer une séance.',
  finTexte: 'Tu viens en tenue de sport à Toulouse Minimes ou à Portet-sur-Garonne, tu poses tes questions au coach, et tu achètes ensuite — en sachant quoi.',
} as const;

export const LIBELLES = {
  sommaire: 'Dans ce conseil',
  maj: 'Mis à jour le',
  questionsSur: 'Questions',
  questionsH2: 'Ce que les Columérins nous demandent.',
  autresSur: 'À lire aussi',
  autresH2: 'L’autre conseil, pour compléter ton sac.',
  lire: 'Lire le conseil',
  tous: 'Tous les conseils matériel',
  finH2: 'Le gant se choisit mieux après une séance.',
  finTexte: 'Viens d’abord essayer à Toulouse Minimes ou à Portet-sur-Garonne : le coach voit ta main, ton gabarit et ton cours, et te dit quoi acheter.',
  finBouton: { texte: 'La première séance', route: 'premiere-seance' },
  finContact: 'Poser ma question',
} as const;

export const CONSEILS: readonly Conseil[] = [
  {
    id: 'poids-gants-de-boxe',
    carte: 'Gants',
    h1: 'Gants de boxe : quel poids choisir, de 10 à 16 oz ?',
    chapeau: 'Le poids d’un gant suit ce que tu fais avec : 10 oz pour frapper le sac, 12 oz pour la technique en cours collectif, 14 à 16 oz dès qu’un partenaire est en face. Une once pèse 28,35 grammes : le chiffre dit combien de mousse te sépare de la cible, pas la pointure du gant.',
    resume: '10, 12, 14 ou 16 oz : le poids suit la séance, puis ton gabarit. Le repère, avec son tableau.',
    photo: 'materiel-boxe-colomiers-boxing-center',
    sujet: 'Conseil · Poids des gants',
    publie: '2026-10-02',
    maj: '2026-10-02',
    sections: [
      {
        sur: 'L’unité',
        h2: 'Une once, c’est 28 grammes de mousse.',
        paras: [
          'Un gant de 10 oz pèse environ 283 g, un gant de 16 oz environ 454 g : l’écart, c’est du rembourrage. Plus il y en a, plus le coup est amorti — pour ta main, et pour la personne que tu touches.',
          'Ce chiffre ne dit rien de la largeur du gant : deux paires de 14 oz peuvent chausser très différemment. <a class="lien" href="https://www.boutique-de-boxe.com/guides/taille-poids-gants-boxe/" rel="noopener">Le guide des tailles 10, 12, 14 et 16 oz</a> de Boutique de Boxe, la boutique de matériel du groupe, apprend à lire les deux.',
        ],
      },
      {
        sur: 'Selon la séance',
        h2: 'Le sac, la technique, le partenaire : trois poids.',
        paras: [
          'Au sac et aux pattes d’ours, 10 oz suffisent : tu frappes du matériel, et la vitesse compte. En cours collectif, avec des touches légères, 12 oz. Quand tu boxes vraiment avec quelqu’un, 14 oz en dessous de 55 kg, 16 oz pour la plupart des adultes.',
          'Si tu ne veux qu’une paire pour commencer, prends des 12 oz. Tu ajouteras <a class="lien" href="https://www.boutique-de-boxe.com/gants-de-boxe-16-oz/" rel="noopener">des gants de 16 oz</a> le jour où le coach te met en opposition.',
        ],
      },
      {
        sur: 'Selon le club',
        h2: 'À Minimes ou à Portet, demande avant d’acheter.',
        paras: [
          'Depuis Colomiers, tu t’entraînes à Toulouse Minimes ou à Portet-sur-Garonne. À Minimes, le groupe <a class="lien" href="/boxe-anglaise/">Boxe Anglaise Loisir</a> pratique sans objectif de compétition ; le groupe Boxe Compétiteurs prépare les combats, et c’est son coach qui fixe le poids du sparring.',
          'Pour le <a class="lien" href="/boxing-fitness/">Cardio Boxing</a>, sans opposition, une paire légère fait l’affaire. Les conditions de prêt de gants dépendent de chaque club : renseigne-toi avant ta <a class="lien" href="/premiere-seance/">première séance</a>. Pour acheter sur place, <a class="lien" href="https://boutique.boxingcenter.fr/materiel" rel="noopener">la boutique Boxing Center</a> prend la commande en ligne, avec retrait en salle.',
        ],
      },
      {
        sur: 'L’essai',
        h2: 'Un gant s’essaie avec les bandes aux mains.',
        paras: [
          'Enfile le gant par-dessus tes bandes et ferme le poing : les doigts touchent le fond sans se plier, le pouce se pose sans forcer, et le poignet reste droit quand tu appuies contre un mur.',
          'Tu hésites entre deux poids ? <a class="lien" href="https://www.boutique-de-boxe.com/outils/poids-de-gants/" rel="noopener">Le calculateur en onces</a> de la boutique demande ta séance, ton gabarit et ton âge, et répond par un chiffre.',
        ],
      },
      {
        sur: 'Les enfants',
        h2: 'Avant 16 ans, c’est l’âge qui décide.',
        paras: [
          'Les repères vont de 4 oz vers 5 ans à 10 oz pour un adolescent, en passant par 6 puis 8 oz. À Minimes, la Baby Boxe accueille les 3 à 6 ans : à cet âge, on joue avec la distance bien avant de parler d’onces.',
          '<a class="lien" href="/boxe-enfants/">La page boxe enfants</a> dit quel club propose quoi, tranche d’âge par tranche d’âge.',
        ],
      },
    ],
    tableau: {
      sur: 'Le tableau',
      h2: 'Le poids des gants, séance par séance.',
      entetes: ['Séance', 'Moins de 55 kg', '55 à 75 kg', 'Plus de 75 kg'],
      lignes: [
        ['Sac et pattes d’ours', '10 oz', '10 oz', '10 oz'],
        ['Technique, cours collectif', '12 oz', '12 oz', '14 oz'],
        ['Sparring avec un partenaire', '14 oz', '16 oz', '16 à 18 oz'],
      ],
      note: 'Source : <a class="lien" href="https://www.boutique-de-boxe.com/guides/quelle-taille-gants-de-boxe/" rel="noopener">« Quelle taille de gants de boxe choisir ? »</a>, Boutique de Boxe. Ce sont des repères : pour le sparring, le club a le dernier mot.',
    },
    faq: [
      {
        titre: 'Quel poids de gants pour débuter la boxe ?',
        texte: '12 oz pour un adulte qui commence en cours collectif. 10 oz si tu ne frappes que le sac, 14 ou 16 oz dès que tu boxes avec un partenaire.',
      },
      {
        titre: 'Combien pèse une once ?',
        texte: '28,35 grammes. Un gant de 12 oz pèse donc environ 340 g, et un gant de 16 oz environ 454 g.',
      },
      {
        titre: 'Les gants de 16 oz sont-ils obligatoires en sparring ?',
        texte: 'C’est le poids le plus courant pour un adulte, parce qu’il protège le partenaire. Le poids exact est fixé par le coach du club : pose-lui la question avant d’acheter.',
      },
      {
        titre: 'Peut-on garder les mêmes gants pour le sac et le sparring ?',
        texte: 'Mieux vaut deux paires. La mousse d’un gant qui frappe le sac se tasse, et elle protège moins bien un partenaire ensuite.',
      },
    ],
  },
  {
    id: 'materiel-cardio-boxing',
    carte: 'Cardio boxing',
    h1: 'Cardio boxing : le matériel qu’il faut, et rien de plus.',
    chapeau: 'Un cours de cardio boxing se pratique sans opposition : des bandes, une paire de gants légers et une corde à sauter suffisent. Casque, coquille et protège-dents ne servent que le jour où tu passes à la boxe avec partenaire.',
    resume: 'Bandes, gants légers, corde à sauter : le sac d’un cours sans opposition, pièce par pièce.',
    photo: 'coach-boxe-colomiers-paos',
    sujet: 'Conseil · Cardio boxing',
    publie: '2026-10-02',
    maj: '2026-10-02',
    sections: [
      {
        sur: 'Le cours',
        h2: 'Sans opposition, donc sans protections.',
        paras: [
          'Le Cardio Boxing de Toulouse Minimes reprend le geste de boxe en travail cardio, sans opposition : on frappe un sac ou des pattes d’ours, jamais une personne. Le même club publie un créneau Boxing Lady, 100 % féminin ; à Portet-sur-Garonne, le créneau féminin s’appelle Lady Boxing.',
          'C’est ce qui allège le sac de sport : aucune protection à acheter. <a class="lien" href="/boxing-fitness/">La page boxing fitness</a> détaille ces cours, et <a class="lien" href="https://www.boutique-de-boxe.com/guides/debuter-boxe/" rel="noopener">le guide pour débuter la boxe</a> de Boutique de Boxe reprend les bases pour la suite.',
        ],
      },
      {
        sur: 'Les mains',
        h2: 'Des bandes à toi, lavées après chaque cours.',
        paras: [
          'Même au sac, le poignet encaisse des centaines de frappes par séance. Les bandes le tiennent dans l’axe et gardent l’intérieur du gant sec : compte une paire si tu viens une fois par semaine, deux paires au-delà.',
          'Chez Boutique de Boxe, la boutique en ligne du groupe, <a class="lien" href="https://www.boutique-de-boxe.com/bandes-de-boxe/" rel="noopener">le rayon des bandes de boxe</a> les classe par longueur. Pour un cours cardio, une bande élastique se pose plus vite qu’une bande rigide.',
        ],
      },
      {
        sur: 'Les gants',
        h2: 'Légers, parce que tu frappes longtemps.',
        paras: [
          'Pour un cours où les rounds de sac s’enchaînent, 10 oz suffisent — 12 oz si tu veux une paire qui serve aussi en cours technique. Un gant plus lourd fatigue l’épaule avant la fin de la séance, et n’apporte rien quand personne n’est en face.',
          'Les clubs fixent eux-mêmes leurs conditions de prêt : pose la question à l’accueil avant d’acheter. Si tu hésites sur le poids, <a class="lien" href="/conseils/poids-gants-de-boxe/">notre repère de 10 à 16 oz</a> fait le tri.',
        ],
      },
      {
        sur: 'Les pattes d’ours',
        h2: 'Aux pattes d’ours, c’est le coach qui s’équipe.',
        paras: [
          'Minimes publie un créneau « PAOS & Pattes d’ours » : le coach tient les cibles, tu frappes. Tu n’as rien à acheter de plus que tes gants.',
          '<a class="lien" href="https://www.boutique-de-boxe.com/pattes-d-ours/" rel="noopener">Une paire de pattes d’ours</a> ne devient un achat que pour s’entraîner à deux en dehors du club — et celui qui les tient doit avoir appris à les présenter.',
        ],
      },
      {
        sur: 'Le souffle',
        h2: 'Une corde à sauter, pour les jours sans cours.',
        paras: [
          'La corde ouvre presque tous les échauffements de boxe : trois minutes de saut, une minute de repos, comme un round. <a class="lien" href="https://www.boutique-de-boxe.com/cordes-a-sauter/" rel="noopener">Une corde à sauter</a> à câble fin tourne vite ; une corde lestée fait travailler les épaules.',
          'Pour la régler, pose un pied au milieu : les poignées doivent arriver sous tes aisselles. Gants et bandes, eux, se commandent aussi à <a class="lien" href="https://boutique.boxingcenter.fr/materiel" rel="noopener">la boutique Boxing Center</a>, avec retrait en salle.',
        ],
      },
    ],
    tableau: {
      sur: 'En résumé',
      h2: 'Chaque pièce, et le moment de l’acheter.',
      entetes: ['Pièce', 'À quoi elle sert', 'Quand l’acheter'],
      lignes: [
        ['Bandes', 'Tenir le poignet, garder le gant sec', 'Dès le premier mois'],
        [
          'Gants de 10 ou 12 oz',
          'Frapper le sac et les pattes d’ours',
          'Après avoir demandé au club ce qu’il prête',
        ],
        ['Corde à sauter', 'S’échauffer, travailler le souffle chez soi', 'Quand tu veux'],
        ['Protège-dents, casque, coquille', 'Boxer avec un partenaire', 'Seulement si tu changes de cours'],
      ],
      note: 'Avant d’acheter, vérifie l’intitulé exact de ton cours sur <a class="lien" href="/plannings/">la page des plannings</a> : le matériel suit le cours, pas l’inverse.',
    },
    faq: [
      {
        titre: 'Faut-il des gants pour un cours de cardio boxing ?',
        texte: 'Oui, dès que le cours passe au sac ou aux pattes d’ours. Une paire de 10 ou 12 oz suffit ; les conditions de prêt dépendent de chaque club.',
      },
      {
        titre: 'Faut-il un protège-dents en cardio boxing ?',
        texte: 'Non : le cours se pratique sans opposition, personne ne te frappe. Il devient nécessaire si tu passes à la boxe avec partenaire.',
      },
      {
        titre: 'Quelle différence entre cardio boxing et boxe anglaise ?',
        texte: 'Le cardio boxing reprend les gestes de la boxe pour le souffle et la dépense, sans opposition. La boxe anglaise ajoute le travail avec partenaire, puis le sparring pour celles et ceux qui le veulent.',
      },
      {
        titre: 'Où faire du cardio boxing en partant de Colomiers ?',
        texte: 'À Boxing Center Toulouse Minimes, qui publie un cours de Cardio Boxing et un créneau Boxing Lady 100 % féminin. Portet-sur-Garonne propose de son côté le Lady Boxing.',
      },
    ],
  },
];

export function conseil(id: ConseilId): Conseil {
  const c = CONSEILS.find((x) => x.id === id);
  if (!c) throw new Error(`Conseil inconnu : ${id}`);
  return c;
}

/** Le sujet et la photo de la vignette d'une page de conseils — jamais ceux d'une autre page. */
export function vignetteDuConseil(id: string): { sujet: string; photo: string } | undefined {
  if (id === 'conseils') return { sujet: INDEX_CONSEILS.sujet, photo: INDEX_CONSEILS.photo };
  const c = CONSEILS.find((x) => x.id === id);
  return c && { sujet: c.sujet, photo: c.photo };
}

/** « 2 octobre 2026 », depuis une date ISO. */
export function dateFr(iso: string): string {
  const d = new Intl.DateTimeFormat('fr-FR', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' }).format(new Date(`${iso}T12:00:00Z`));
  return d.replace(/^1 /, '1er ');
}
