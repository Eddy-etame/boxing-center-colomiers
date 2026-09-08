/**
 * Ce build est-il celui du vrai domaine ?
 *
 * Vercel construit aussi des aperçus (preview) à chaque push. Ces aperçus
 * servent le site entier sur une URL *.vercel.app : s'ils sont indexables, on
 * publie du contenu dupliqué en concurrence directe avec le domaine réel,
 * et Google peut retenir la mauvaise URL comme canonique.
 *
 * La variable est lue au build, donc la valeur est figée dans le HTML : un
 * aperçu porte son noindex de façon définitive, il ne peut pas « devenir »
 * indexable par accident.
 */
const env = import.meta.env.VERCEL_ENV ?? process.env.VERCEL_ENV;

/** true uniquement sur le déploiement de production Vercel. */
export const EST_PRODUCTION = env === 'production';

/** true en local (dev / build local), où rien n'est publié. */
export const EST_LOCAL = env === undefined;

/**
 * Les robots ne doivent indexer que la production. En local on n'ajoute rien,
 * pour ne pas fausser les contrôles de build ; sur un aperçu Vercel, on
 * bloque.
 */
export const DOIT_BLOQUER_LES_ROBOTS = !EST_PRODUCTION && !EST_LOCAL;
