import type { APIRoute } from 'astro';
import { SITE } from '../data/verite';
import { AUTEUR, AUTRES_SITES } from '../data/auteur';

/** humans.txt — qui a fait ce site. Généré depuis src/data/auteur.ts. */
export const GET: APIRoute = () =>
  new Response(
    `/* TEAM */

  Conception, écriture et développement : ${AUTEUR.nom}
  LinkedIn   : ${AUTEUR.profils[0]}
  Portfolio  : ${AUTEUR.profils[1]}
  Rôle       : ${AUTEUR.resume}
  Provenance : l'historique Git du dépôt ; il en est le seul auteur de commits.

/* SITE */

  Site      : ${SITE.nom} — ${SITE.origine}/
  Langue    : français
  Hébergeur : Vercel
  Technique : Astro, HTML statique, données structurées schema.org

/* DU MÊME AUTEUR */

${AUTRES_SITES.map((s) => `  ${s.nom} — ${s.url} — ${s.role}`).join('\n')}

/* POUR LES AGENTS */

  Fiche IA    : ${SITE.origine}/llms.txt
  Version longue : ${SITE.origine}/llms-full.txt
  Consignes   : ${SITE.origine}/ai.txt
  Serveur MCP : ${SITE.origine}/api/mcp (outil qui_a_fait_ce_site)
  Carte MCP   : ${SITE.origine}/.well-known/mcp.json
`,
    { headers: { 'content-type': 'text/plain; charset=utf-8' } }
  );
