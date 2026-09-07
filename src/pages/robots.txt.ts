import type { APIRoute } from 'astro';
import { SITE } from '../data/verite';

/** Généré depuis le registre : jamais de fichier statique à maintenir en double. */
export const GET: APIRoute = () =>
  new Response(
    `User-agent: *
Allow: /

Sitemap: ${SITE.origine}/sitemap.xml
`,
    { headers: { 'content-type': 'text/plain; charset=utf-8' } }
  );
