/**
 * Date de dernière modification réelle d'une page.
 *
 * Un `lastmod` égal à la date du build ment à Google : il dit que tout a
 * changé à chaque déploiement, et Google finit par ne plus le croire. On
 * lit donc la date du dernier commit qui a touché la page — ou les données
 * dont elle dépend (src/data), puisqu'un horaire ou une adresse qui change
 * modifie bien la page.
 *
 * Quand git n'est pas disponible ou que l'historique est tronqué (clone
 * superficiel), on retombe sur la date du build : moins précis, jamais faux
 * dans le mauvais sens.
 */
import { execSync } from 'node:child_process';
import { existsSync } from 'node:fs';

const cache = new Map<string, string>();

function dateGit(chemin: string): string | null {
  if (!existsSync(chemin)) return null;
  try {
    const iso = execSync(`git log -1 --format=%cI -- "${chemin}"`, {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
    }).trim();
    return iso || null;
  } catch {
    return null;
  }
}

const AUJOURDHUI = new Date().toISOString();

/** Date ISO de la dernière modification d'une page, données comprises. */
export function derniereModification(fichierPage: string): string {
  if (cache.has(fichierPage)) return cache.get(fichierPage)!;
  const candidates = [dateGit(fichierPage), dateGit('src/data')].filter(Boolean) as string[];
  const date = candidates.length ? candidates.sort().at(-1)! : AUJOURDHUI;
  cache.set(fichierPage, date);
  return date;
}

/** Le fichier source d'une route, pour en lire la date. */
export function fichierDeRoute(chemin: string): string {
  if (chemin === '/') return 'src/pages/index.astro';
  return `src/pages/${chemin.replace(/^\/|\/$/g, '')}.astro`;
}
