import type { APIRoute } from 'astro';
import { ROUTES } from '../data/routes';
import { SITE } from '../data/verite';

/**
 * Le plan du site sort du registre de routes : une page ajoutée y apparaît
 * automatiquement, et une page non indexable en est exclue automatiquement.
 */
export const GET: APIRoute = () => {
  const jour = new Date().toISOString().slice(0, 10);
  const urls = ROUTES.filter((r) => r.index)
    .map(
      (r) => `  <url>
    <loc>${SITE.origine}${r.chemin}</loc>
    <lastmod>${jour}</lastmod>
    <priority>${r.id === 'accueil' ? '1.0' : '0.8'}</priority>
  </url>`
    )
    .join('\n');

  return new Response(
    `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls}
</urlset>
`,
    { headers: { 'content-type': 'application/xml; charset=utf-8' } }
  );
};
