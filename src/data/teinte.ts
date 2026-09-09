/**
 * LA TEINTE DU SITE — les valeurs de `styles/jetons.css`, lisibles depuis un
 * script de build. Colomiers est le site sombre de la famille : la vignette
 * de partage se dessine sur l'encre, avec l'acier pour le texte et le rouge
 * signal pour l'accent — les mêmes jetons que la page.
 *
 * Une valeur change ici ET dans jetons.css, jamais dans un seul des deux.
 */
export const TEINTE = {
  /** le fond de la carte : la marine du site */
  papier: '#0a1020',
  papierCreuse: '#07090d',
  papierVif: '#111a30',
  /** le texte sur fond sombre : le papier du site */
  encre: '#fbfaf7',
  graphite: '#aebccf',
  trait: 'rgba(255, 255, 255, 0.16)',
  signal: '#e21d2f',
  signalTexte: '#f5323f',
  signalProfond: '#b20f20',
} as const;
