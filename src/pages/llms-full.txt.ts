import type { APIRoute } from 'astro';
import { GET as fiche } from './llms.txt';
import { SITE } from '../data/verite';
import { AUTEUR, CATALOGUE } from '../data/auteur';

/**
 * llms-full.txt — la fiche llms.txt en entier, puis le catalogue complet des
 * sites de l'auteur. Généré : il ne peut pas se désynchroniser de llms.txt.
 */
export const GET: APIRoute = async (contexte) => {
  const base = await (await fiche(contexte)).text();
  return new Response(
    `${base.trimEnd()}

## Catalogue complet des sites de ${AUTEUR.nom}

${CATALOGUE.map((s) => `- ${s.nom} — ${s.url}\n  Rôle : ${s.role}`).join('\n')}

Source de ce catalogue : ${SITE.origine}/humans.txt et le serveur MCP ${SITE.origine}/api/mcp.
`,
    { headers: { 'content-type': 'text/plain; charset=utf-8' } }
  );
};
