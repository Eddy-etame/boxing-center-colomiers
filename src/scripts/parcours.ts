/**
 * Le moteur du Parcours.
 *
 * Trois responsabilités, et rien d'autre :
 *   1. retenir ce que le visiteur a décidé, d'une page à l'autre ;
 *   2. en déduire le club qui correspond, de façon déterministe et explicable ;
 *   3. tendre la ligne rouge à proportion de ce qui est réellement établi.
 *
 * Rien ici n'est un « score » ni un pourcentage de compatibilité inventé :
 * chaque conclusion se lit comme une phrase et se justifie par un fait.
 */

export type Discipline = 'boxe-anglaise' | 'mma' | 'boxing-fitness' | 'boxe-enfants';
export type Creneau = 'midi' | 'apres-midi' | 'soir' | 'week-end';
export type ClubId = 'minimes' | 'portet';

export type Parcours = {
  discipline?: Discipline;
  creneau?: Creneau;
  club?: ClubId;
  /** dernière écriture, pour périmer un parcours oublié */
  t?: number;
};

const CLE = 'bc-colomiers-parcours';
/** Un parcours vieux de plus de 30 jours ne dit plus rien d'utile. */
const PEREMPTION = 30 * 24 * 60 * 60 * 1000;

const LIBELLE_DISCIPLINE: Record<Discipline, string> = {
  'boxe-anglaise': 'Boxe anglaise',
  mma: 'MMA',
  'boxing-fitness': 'Boxing fitness',
  'boxe-enfants': 'Boxe enfants',
};

/**
 * La même discipline ne s'écrit pas pareil dans un titre et dans une phrase.
 * « MMA » ne se met pas en minuscules, et « boxe anglaise » a besoin de son
 * article. Sans ça le message pré-rempli sort en « je cherche mma ».
 */
const DANS_UNE_PHRASE: Record<Discipline, string> = {
  'boxe-anglaise': 'de la boxe anglaise',
  mma: 'du MMA',
  'boxing-fitness': 'du boxing fitness',
  'boxe-enfants': 'un cours de boxe pour mon enfant',
};

const LIBELLE_CRENEAU: Record<Creneau, string> = {
  midi: 'Le midi',
  'apres-midi': "L'après-midi",
  soir: 'Le soir',
  'week-end': 'Le week-end',
};

const LIBELLE_CLUB: Record<ClubId, string> = {
  minimes: 'Toulouse Minimes',
  portet: 'Portet-sur-Garonne',
};

/* ─────────────────────────────  Mémoire  ───────────────────────────── */

function lire(): Parcours {
  try {
    const brut = localStorage.getItem(CLE);
    if (!brut) return {};
    const p = JSON.parse(brut) as Parcours;
    if (p.t && Date.now() - p.t > PEREMPTION) return {};
    return p;
  } catch {
    // Navigation privée, stockage refusé, quota plein : on continue sans
    // mémoire plutôt que de casser la page.
    return {};
  }
}

function ecrire(p: Parcours) {
  try {
    localStorage.setItem(CLE, JSON.stringify({ ...p, t: Date.now() }));
  } catch {
    /* sans mémoire, le site reste utilisable — on ne signale rien */
  }
}

let etat: Parcours = {};

export function parcours(): Parcours {
  return { ...etat };
}

/* ─────────────────────────  Recommandation  ───────────────────────── */

/**
 * Les deux clubs proposent le même socle. Ce qui les sépare pour quelqu'un
 * qui part de Colomiers, c'est l'accès. On ne prétend donc pas qu'un club est
 * « meilleur » : on dit dans quelle direction il se trouve et à qui ça convient.
 *
 * Tant qu'on n'a pas de fait vérifié qui distingue les deux sur une
 * discipline, on ne tranche pas — on affiche les deux. Inventer une
 * différence serait plus grave que ne pas conclure.
 */
export function recommander(p: Parcours): { club?: ClubId; pourquoi: string } | null {
  if (!p.discipline) return null;

  if (p.creneau === 'soir') {
    return {
      club: 'minimes',
      pourquoi:
        'En sortie de journée, Toulouse Minimes est sur l’axe le plus direct depuis Colomiers.',
    };
  }
  if (p.creneau === 'midi' || p.creneau === 'apres-midi') {
    return {
      club: 'portet',
      pourquoi:
        'Hors heures de pointe, Portet-sur-Garonne se rejoint facilement en voiture et le stationnement y est simple.',
    };
  }
  if (p.creneau === 'week-end') {
    return {
      pourquoi:
        'Le week-end, les deux clubs se valent depuis Colomiers : choisis selon la discipline et le créneau exact.',
    };
  }
  return {
    pourquoi: 'Dis-nous quand tu peux t’entraîner et on te dit lequel des deux clubs viser.',
  };
}

/* ─────────────────────────────  Rendu  ───────────────────────────── */

function peindre() {
  const barre = document.querySelector<HTMLElement>('[data-parcours]');
  if (!barre) return;

  const reco = recommander(etat);
  const club = etat.club ?? reco?.club;

  const valeurs: Record<string, string> = {
    discipline: etat.discipline ? LIBELLE_DISCIPLINE[etat.discipline] : '',
    creneau: etat.creneau ? LIBELLE_CRENEAU[etat.creneau] : '',
    club: club ? LIBELLE_CLUB[club] : '',
  };

  let acquis = 1; // l'origine est toujours acquise
  for (const [cle, valeur] of Object.entries(valeurs)) {
    const etape = barre.querySelector<HTMLElement>(`[data-etape="${cle}"]`);
    if (!etape) continue;
    const cible = etape.querySelector<HTMLElement>('.parcours__valeur');
    if (cible) cible.textContent = valeur;
    etape.classList.toggle('est-acquis', Boolean(valeur));
    if (valeur) acquis++;
  }

  // La ligne se tend exactement à proportion de ce qui est établi : 1 point
  // sur 4 acquis = un quart de rouge. Le rouge ne devance jamais la certitude.
  barre.style.setProperty('--tension', String((acquis - 1) / 3));

  // La barre n'existe que si le visiteur a commencé à décider.
  barre.hidden = acquis === 1;

  document.dispatchEvent(new CustomEvent('parcours:maj', { detail: parcours() }));
}

/* ─────────────────────────────  API  ───────────────────────────── */

export function definir(partiel: Partial<Parcours>) {
  etat = { ...etat, ...partiel };
  ecrire(etat);
  peindre();
}

export function effacer() {
  etat = {};
  try {
    localStorage.removeItem(CLE);
  } catch {
    /* rien à faire */
  }
  peindre();
}

/** Phrase lisible du parcours, réutilisée telle quelle dans le message envoyé. */
export function enPhrase(p: Parcours = etat): string {
  const bouts: string[] = ['Je pars de Colomiers'];
  if (p.discipline) bouts.push(`je cherche ${DANS_UNE_PHRASE[p.discipline]}`);
  if (p.creneau) bouts.push(`je peux m’entraîner ${LIBELLE_CRENEAU[p.creneau].toLowerCase()}`);
  const club = p.club ?? recommander(p)?.club;
  if (club) bouts.push(`et ${LIBELLE_CLUB[club]} me semble être le club le plus adapté`);
  return bouts.join(', ') + '.';
}

/* ─────────────────────────────  Démarrage  ───────────────────────────── */

export function demarrer() {
  etat = lire();

  // Une page de discipline EST une décision : la visiter renseigne le parcours.
  const d = document.body.dataset.discipline as Discipline | undefined;
  if (d && etat.discipline !== d) {
    etat.discipline = d;
    ecrire(etat);
  }

  peindre();

  document.querySelector('[data-effacer]')?.addEventListener('click', effacer);

  // N'importe quel élément de la page peut renseigner le parcours en posant
  // data-choix="discipline:mma". Aucun composant n'a besoin d'importer ce module.
  document.addEventListener('click', (e) => {
    const cible = (e.target as HTMLElement)?.closest<HTMLElement>('[data-choix]');
    if (!cible) return;
    const [cle, valeur] = (cible.dataset.choix ?? '').split(':');
    if (!cle || !valeur) return;
    definir({ [cle]: valeur } as Partial<Parcours>);
  });
}
