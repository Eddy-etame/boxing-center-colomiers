/**
 * LE MOUVEMENT — un seul moteur pour tout le site.
 *
 * Trois règles, et rien d'autre :
 *
 * 1. Rien n'arrive posé. Chaque bloc d'une section entre en montant, décalé
 *    de son voisin — c'est la feuille qu'on pose sur la table, la même
 *    grammaire que le hero.
 * 2. Ça se rejoue. Si on remonte au-dessus d'un bloc puis qu'on redescend, il
 *    rejoue son entrée : une page qu'on parcourt deux fois n'est pas une page
 *    morte à la deuxième. En revanche, on ne rejoue jamais un bloc qu'on vient
 *    de dépasser vers le bas — sinon la remontée devient un clignotement.
 * 3. On ne balise pas à la main. Le script trouve lui-même les blocs de chaque
 *    section : ajouter une section, c'est hériter du mouvement sans y penser.
 *
 * `prefers-reduced-motion` n'est pas une amputation : tout est rendu à l'état
 * final, immédiatement, sans perte d'information. Sans JavaScript non plus.
 */

const REDUIT = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

/** Les sections qui gèrent elles-mêmes leur chorégraphie. */
const EXCLUES = '.hero, [data-sans-scene]';

/**
 * Découpe une section en blocs animables.
 *
 * On descend d'un niveau quand l'enveloppe n'a qu'un seul enfant qui est
 * lui-même une grille : sinon toute la section monterait d'un bloc, et le
 * décalage — qui est tout l'intérêt — n'existerait pas.
 */
function blocsDe(section: HTMLElement): HTMLElement[] {
  const enveloppes = [...section.querySelectorAll<HTMLElement>(':scope > .enveloppe')];
  const sortie: HTMLElement[] = [];

  for (const env of enveloppes) {
    let enfants = [...env.children] as HTMLElement[];
    if (enfants.length === 1 && enfants[0].children.length > 1) {
      enfants = [...enfants[0].children] as HTMLElement[];
    }
    sortie.push(...enfants);
  }
  return sortie;
}

function preparer(): HTMLElement[] {
  const cibles: HTMLElement[] = [];

  for (const section of document.querySelectorAll<HTMLElement>('main .section')) {
    if (section.matches(EXCLUES)) continue;
    const blocs = blocsDe(section);
    blocs.forEach((b, i) => {
      // Un élément déjà chorégraphié garde sa propre cadence.
      if (b.classList.contains('reveler') || b.classList.contains('bloc-scene')) return;
      b.classList.add('bloc-scene');
      b.style.setProperty('--i', String(i));
      cibles.push(b);
    });
  }

  // Les éléments balisés à la main : listes, cartes, photos.
  for (const e of document.querySelectorAll<HTMLElement>('.reveler, [data-calque]')) {
    cibles.push(e);
  }
  return cibles;
}

/** Tout montrer, tout de suite. Le repli de dernier recours. */
const revelerTout = (cibles: HTMLElement[]) => cibles.forEach((c) => c.classList.add('vu'));

export function demarrerMouvement() {
  const cibles = preparer();
  if (!cibles.length) return;

  if (REDUIT() || typeof IntersectionObserver === 'undefined') {
    revelerTout(cibles);
    return;
  }

  let obs: IntersectionObserver;
  try {
    obs = new IntersectionObserver(
      (entrees) => {
        for (const e of entrees) {
          if (e.isIntersecting) {
            e.target.classList.add('vu');
            continue;
          }
          // On ne réarme que par le bas : sortir par le haut, c'est avoir lu.
          if (e.boundingClientRect.top > 0) e.target.classList.remove('vu');
        }
      },
      { rootMargin: '0px 0px -8% 0px', threshold: 0 }
    );
    cibles.forEach((c) => obs.observe(c));
  } catch {
    revelerTout(cibles);
    return;
  }

  /**
   * LE FILET. Un bloc en attente est un bloc invisible : si l'observateur ne
   * s'exécute pas — onglet ouvert en arrière-plan, rendu suspendu, moteur
   * exotique — personne ne doit se retrouver devant une page blanche. On
   * recalcule donc à la main, une fois, ce qui est à l'écran, et on le montre.
   * Le calcul de rectangle fonctionne là où l'observateur ne tourne pas.
   */
  const filet = () => {
    for (const c of cibles) {
      if (c.classList.contains('vu')) continue;
      const r = c.getBoundingClientRect();
      if (r.top < innerHeight && r.bottom > 0) c.classList.add('vu');
    }
  };
  setTimeout(filet, 1400);
  addEventListener('pageshow', () => setTimeout(filet, 200));
}
