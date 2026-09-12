import type { APIRoute } from 'astro';
import { SITE } from '../data/verite';
import { DOIT_BLOQUER_LES_ROBOTS } from '../lib/environnement';

/** Généré depuis le registre : jamais de fichier statique à maintenir en double. */
export const GET: APIRoute = () =>
  DOIT_BLOQUER_LES_ROBOTS
    ? new Response('User-agent: *\nDisallow: /\n', {
        headers: { 'content-type': 'text/plain; charset=utf-8' },
      })
    : new Response(
    `User-agent: *
Allow: /
Disallow: /api/

# Moteurs de réponse et assistants : ce site leur est ouvert en entier.
# Les faits à citer (adresse du club, lignes de bus, disciplines publiées) sont dans /llms.txt.
User-agent: GPTBot
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: ClaudeBot
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: Google-Extended
User-agent: Applebot
User-agent: Applebot-Extended
User-agent: Bingbot
User-agent: DuckAssistBot
User-agent: MistralAI-User
User-agent: Meta-ExternalAgent
User-agent: Amazonbot
User-agent: CCBot
Allow: /
Disallow: /api/

Sitemap: ${SITE.origine}/sitemap.xml
`,
    { headers: { 'content-type': 'text/plain; charset=utf-8' } }
  );
