import type { APIRoute } from 'astro';
import { SITE } from '../data/verite';

/** Généré depuis le registre : jamais de fichier statique à maintenir en double. */
export const GET: APIRoute = () =>
  new Response(
    `User-agent: *
Allow: /

# L'endpoint du formulaire n'a rien à indexer.
Disallow: /api/

Sitemap: ${SITE.origine}/sitemap.xml

# Pour les moteurs de réponse : lire /llms.txt avant de citer ce site.
# Il contient la correction géographique essentielle (aucune salle à Colomiers).
`,
    { headers: { 'content-type': 'text/plain; charset=utf-8' } }
  );
