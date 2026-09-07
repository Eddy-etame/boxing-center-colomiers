import { defineConfig } from 'astro/config';
import vercel from '@astrojs/vercel';

// Statique par défaut. Seul /api/contact tourne à la demande : il relaie le
// formulaire vers Inlet (JSON + preuve de travail), ce qu'un <form> natif ne
// peut pas faire seul. Tout le reste est pré-rendu.
export default defineConfig({
  site: 'https://www.boxingcenter-colomiers.fr',
  output: 'static',
  adapter: vercel(),
  trailingSlash: 'always',
  build: { format: 'directory' },
  prefetch: { prefetchAll: true, defaultStrategy: 'viewport' },
  compressHTML: true,
  redirects: {
    // Le cahier des charges §15 donne des exemples d'URL avec « colomiers »
    // répété dans le slug. Le domaine le porte déjà : on garde des URL
    // propres et on redirige les formes du cahier pour qu'elles fonctionnent.
    '/club-boxe-colomiers': '/',
    '/sport-combat-colomiers': '/',
    '/boxe-colomiers': '/',
    '/boxe-anglaise-colomiers': '/boxe-anglaise/',
    '/club-mma-colomiers': '/mma/',
    '/mma-colomiers': '/mma/',
    '/boxing-fitness-colomiers': '/boxing-fitness/',
    '/boxe-femme-colomiers': '/boxing-fitness/',
    '/boxe-enfant-colomiers': '/boxe-enfants/',
    '/boxe-enfants-colomiers': '/boxe-enfants/',
  },
});
