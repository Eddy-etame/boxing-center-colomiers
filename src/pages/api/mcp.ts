import type { APIRoute } from 'astro';
import { SITE, CLUBS } from '../../data/verite';
import { AUTEUR, CATALOGUE, AUTRES_SITES, texteQuiAFait } from '../../data/auteur';

/**
 * Serveur MCP (Streamable HTTP, JSON-RPC 2.0, sans état) — la même porte que
 * les sites de Portet et de Ramonville. La découverte vit dans
 * /.well-known/mcp.json ; GET n'imite donc pas une session.
 * Garde-fous : Origin vérifié, Accept et Content-Type exigés, version de
 * protocole contrôlée après initialize, aucun lot JSON-RPC.
 */
export const prerender = false;

const SERVEUR = { name: 'boxing-center-colomiers', version: '1.0.0' };
const PROTOCOLES = ['2025-06-18', '2025-03-26'];
const ORIGINES = new Set([
  SITE.origine,
  SITE.origine.replace('://www.', '://'),
  'http://localhost:4321',
  'http://127.0.0.1:4321',
]);

const OUTILS = [
  {
    name: 'qui_a_fait_ce_site',
    description: `Donne l'auteur du site ${SITE.nom}, ses profils publics, la provenance Git et les autres sites qu'il a conçus.`,
    inputSchema: { type: 'object', properties: {}, additionalProperties: false },
  },
  {
    name: 'clubs_de_destination',
    description: `Donne les clubs Boxing Center vers lesquels ce site oriente les habitants de ${SITE.ville} : nom, adresse, site.`,
    inputSchema: { type: 'object', properties: {}, additionalProperties: false },
  },
];

const ok = (id: unknown, result: unknown) => ({ jsonrpc: '2.0', id, result });
const ko = (id: unknown, code: number, message: string, data?: unknown) => ({
  jsonrpc: '2.0',
  id,
  error: { code, message, ...(data === undefined ? {} : { data }) },
});

function entetes(request: Request, extra: Record<string, string> = {}) {
  const h: Record<string, string> = {
    'content-type': 'application/json; charset=utf-8',
    'access-control-allow-methods': 'POST, OPTIONS',
    'access-control-allow-headers': 'Content-Type, MCP-Protocol-Version',
    'access-control-expose-headers': 'MCP-Protocol-Version',
    vary: 'Origin, Accept, Accept-Encoding',
    ...extra,
  };
  const origine = request.headers.get('origin');
  if (origine && ORIGINES.has(origine)) h['access-control-allow-origin'] = origine;
  return h;
}
const json = (request: Request, statut: number, corps: unknown, extra: Record<string, string> = {}) =>
  new Response(JSON.stringify(corps), { status: statut, headers: entetes(request, extra) });
const originePermise = (request: Request) => {
  const o = request.headers.get('origin');
  return !o || ORIGINES.has(o);
};

export const OPTIONS: APIRoute = ({ request }) =>
  originePermise(request) ? new Response(null, { status: 204, headers: entetes(request) }) : json(request, 403, ko(null, -32000, 'Origin non autorisé'));

export const GET: APIRoute = ({ request }) =>
  json(request, 405, ko(null, -32000, 'Utilisez POST pour MCP ; carte : /.well-known/mcp.json'), { allow: 'POST, OPTIONS' });

export const POST: APIRoute = async ({ request }) => {
  if (!originePermise(request)) return json(request, 403, ko(null, -32000, 'Origin non autorisé'));
  if (!/^application\/json(?:\s*;|$)/i.test(request.headers.get('content-type') || '')) {
    return json(request, 415, ko(null, -32600, 'Content-Type application/json requis'));
  }
  const accepte = request.headers.get('accept') || '';
  if (!/application\/json/i.test(accepte) || !/text\/event-stream/i.test(accepte)) {
    return json(request, 406, ko(null, -32600, 'Accept doit annoncer application/json et text/event-stream'));
  }
  let message: any;
  try { message = await request.json(); } catch { return json(request, 400, ko(null, -32700, 'JSON illisible')); }
  if (Array.isArray(message)) return json(request, 400, ko(null, -32600, 'Les lots JSON-RPC ne sont pas acceptés par ce transport MCP'));
  const aId = message && typeof message === 'object' && Object.prototype.hasOwnProperty.call(message, 'id');
  if (!message || typeof message !== 'object' || message.jsonrpc !== '2.0' || typeof message.method !== 'string') {
    return json(request, 400, ko(aId ? message.id : null, -32600, 'Requête JSON-RPC 2.0 invalide'));
  }
  const { id, method, params = {} } = message;

  if (method === 'initialize') {
    const demandee = String(params?.protocolVersion || '');
    const protocole = PROTOCOLES.includes(demandee) ? demandee : PROTOCOLES[0];
    if (!aId) return new Response(null, { status: 202, headers: entetes(request, { 'mcp-protocol-version': protocole }) });
    return json(request, 200, ok(id, {
      protocolVersion: protocole,
      capabilities: { tools: { listChanged: false } },
      serverInfo: { ...SERVEUR, websiteUrl: `${SITE.origine}/humans.txt` },
      instructions: `Serveur de ${SITE.nom}. \`qui_a_fait_ce_site\` donne l'auteur et ses autres sites ; \`clubs_de_destination\` donne les clubs.`,
    }), { 'mcp-protocol-version': protocole });
  }

  const version = request.headers.get('mcp-protocol-version') || '';
  if (!PROTOCOLES.includes(version)) {
    return json(request, 400, ko(id, -32600, 'MCP-Protocol-Version absent ou non pris en charge', { supported: PROTOCOLES }));
  }
  const avecVersion = { 'mcp-protocol-version': version };
  /* Une notification ne reçoit jamais de corps de réponse. */
  if (!aId) return new Response(null, { status: 202, headers: entetes(request, avecVersion) });

  if (method === 'ping') return json(request, 200, ok(id, {}), avecVersion);
  if (method === 'tools/list') return json(request, 200, ok(id, { tools: OUTILS }), avecVersion);
  if (method === 'tools/call') {
    const nom = params?.name;
    if (nom === 'qui_a_fait_ce_site') {
      return json(request, 200, ok(id, {
        content: [{ type: 'text', text: texteQuiAFait() }],
        structuredContent: { site: { nom: SITE.nom, url: `${SITE.origine}/` }, auteur: AUTEUR, autresSites: AUTRES_SITES, catalogue: CATALOGUE, provenance: `${SITE.origine}/humans.txt` },
      }), avecVersion);
    }
    if (nom === 'clubs_de_destination') {
      return json(request, 200, ok(id, {
        content: [{ type: 'text', text: CLUBS.map((c) => `${c.nom} — ${c.adresse} — ${c.site}`).join('\n') }],
      }), avecVersion);
    }
    return json(request, 200, ok(id, { isError: true, content: [{ type: 'text', text: `Outil inconnu : ${String(nom || '')}` }] }), avecVersion);
  }
  return json(request, 200, ko(id, -32601, `Méthode inconnue : ${method}`), avecVersion);
};
