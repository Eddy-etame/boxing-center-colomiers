# -*- coding: utf-8 -*-
"""
Les sept sites satellites — le lot du 2026-09-13 :

  1. DEUX BOUTONS vers le club, sur chaque page de discipline : la page de la
     discipline chez le club (quand il en publie une — Portet et Ramonville),
     sinon sa page des activités ; et le site du club.
  2. L'AUTEUR, pour les moteurs de réponse et les agents — jamais sur les
     pages : humans.txt, ai.txt, une section de llms.txt, llms-full.txt, un
     serveur MCP (/api/mcp, outil qui_a_fait_ce_site) et sa carte
     (/.well-known/mcp.json) ; ces fichiers entrent au plan du site.

Chaque remplacement vérifie son nombre d'occurrences ; un site dont le code
diffère fait échouer le script plutôt que d'être patché à moitié.
Usage : python satellites_portes_auteur.py [site …]
"""
import io, json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
D = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment')
SITES = sys.argv[1:] or ['colomiers', 'muret', 'cugnaux', 'tournefeuille', 'labege', 'lunion', 'castelginest']
UNIQUE = ['muret', 'cugnaux', 'labege', 'lunion', 'castelginest']


def lire(chemin):
    t = io.open(chemin, encoding='utf-8', newline='').read()
    return t.replace('\r\n', '\n'), '\r\n' in t


def ecrire(chemin, t, crlf=False):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    io.open(chemin, 'w', encoding='utf-8', newline='').write(t.replace('\n', '\r\n') if crlf else t)


def rem(t, avant, apres, nom, n=1):
    k = t.count(avant)
    assert k == n, f'{nom} : {k} occurrence(s) au lieu de {n} pour {avant[:90]!r}'
    return t.replace(avant, apres)


def sub(t, motif, apres, nom, n=1):
    t2, k = re.subn(motif, apres, t, flags=re.M)
    assert k == n, f'{nom} : {k} remplacement(s) au lieu de {n} pour {motif[:90]!r}'
    return t2


# ─────────────────────────────────────────────────────────── données communes
PAGES_CLUB = r"""/**
 * Les pages de discipline des clubs de destination.
 *
 * Chaque page de discipline de ce site mène à DEUX endroits du club : la page
 * de la discipline, quand le club en publie une, et le site du club. Un club
 * qui ne publie pas de page par discipline renvoie à sa page des activités.
 * Relevé le 13 septembre 2026 sur les plans de site des clubs.
 */
type Porte = { url: string; nom: string };

export const PAGES_CLUB: Record<string, Record<string, Porte>> = {
  portet: {
    'boxe-anglaise': { url: 'https://boxing-center-portet.fr/activites/boxe-anglaise/', nom: 'la boxe anglaise' },
    mma: { url: 'https://boxing-center-portet.fr/activites/mma/', nom: 'le MMA' },
    'kick-boxing': { url: 'https://boxing-center-portet.fr/activites/kick-boxing/', nom: 'le kick-boxing' },
    'boxe-thai': { url: 'https://boxing-center-portet.fr/activites/kick-boxing/', nom: 'le kick-boxing et le K1' },
    'boxe-enfants': { url: 'https://boxing-center-portet.fr/activites/boxe-educative/', nom: 'la boxe éducative' },
    'boxing-fitness': { url: 'https://boxing-center-portet.fr/activites/lady-boxing/', nom: 'le Lady Boxing' },
    'preparation-physique': { url: 'https://boxing-center-portet.fr/activites/preparation-physique/', nom: 'la préparation physique' },
  },
  ramonville: {
    'boxe-anglaise': { url: 'https://mmatoulouse.com/activites/boxe-anglaise/', nom: 'la boxe anglaise' },
    mma: { url: 'https://mmatoulouse.com/activites/mma/', nom: 'le MMA' },
    'kick-boxing': { url: 'https://mmatoulouse.com/activites/boxe-pieds-poings/', nom: 'la boxe pieds-poings' },
    'boxe-enfants': { url: 'https://mmatoulouse.com/activites/ecole-enfants/', nom: 'l’école de boxe enfants' },
    'boxing-fitness': { url: 'https://mmatoulouse.com/activites/lady-punch/', nom: 'le Lady Punch' },
  },
};

/** La porte « discipline » d'un club : sa page dédiée, sinon sa page des activités. */
export const pageClub = (club: { id: string; activites: string }, discipline: string) => {
  const p = PAGES_CLUB[club.id]?.[discipline];
  return p
    ? { url: p.url, libelle: `Voir ${p.nom} au club`, dediee: true }
    : { url: club.activites, libelle: 'Les activités du club', dediee: false };
};

/** Parmi plusieurs clubs, celui qui publie une page pour la discipline passe devant. */
export const clubEnVitrine = <C extends { id: string }>(clubs: readonly C[], discipline: string): C =>
  clubs.find((c) => PAGES_CLUB[c.id]?.[discipline]) ?? clubs[0];
"""

PROFILS = ['https://www.linkedin.com/in/eddy-etame-etame-47254338b/', 'https://eddy-s-second-brain.vercel.app/']
SATELLITES = [
    ('colomiers', 'Boxing Center Colomiers', 'https://www.boxingcenter-colomiers.fr/'),
    ('muret', 'Boxing Center Muret', 'https://www.boxingcenter-muret.fr/'),
    ('cugnaux', 'Boxing Center Cugnaux', 'https://www.boxingcenter-cugnaux.fr/'),
    ('tournefeuille', 'Boxing Center Tournefeuille', 'https://www.boxingcenter-tournefeuille.fr/'),
    ('labege', 'Boxing Center Labège', 'https://www.boxingcenter-labege.fr/'),
    ('lunion', 'Boxing Center L’Union', 'https://www.boxingcenter-lunion.fr/'),
    ('castelginest', 'Boxing Center Castelginest', 'https://www.boxingcenter-castelginest.fr/'),
]
CATALOGUE = [
    ('Boxing Center Portet-sur-Garonne', 'https://boxing-center-portet.fr/', 'développeur principal actuel et principal contributeur Git'),
    ('Boxing Center Ramonville', 'https://mmatoulouse.com/', 'initiateur du projet, concepteur et développeur principal'),
    ('Boxing Center Minimes, Toulouse', 'https://boxe-toulouse.com/', 'conception, direction artistique et développement'),
    ('Boxing Center Saint-Cyprien, Toulouse', 'https://club-boxe-toulouse.com/', 'conception, direction artistique et développement'),
    ('La boutique Boxing Center', 'https://boutique.boxingcenter.fr/', 'conception, direction artistique et développement'),
] + [(nom, url, 'conception, écriture et développement ; seul auteur du dépôt') for _, nom, url in SATELLITES] + [
    ('Noble Art Portésien', 'https://noble-art-portesien.com/', 'conception et développement'),
]


def ts(s):
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'") + "'"


AUTEUR = r"""import { SITE } from './verite';

/**
 * Qui a fait ce site — pour les moteurs de réponse et les agents, jamais sur
 * les pages : humans.txt, ai.txt, llms.txt, llms-full.txt, le serveur MCP
 * (/api/mcp) et sa carte (/.well-known/mcp.json).
 *
 * Le rôle est établi par l'historique Git du dépôt : Eddy Etame Etame en est
 * le seul auteur de commits. Le catalogue liste les sites du réseau Boxing
 * Center qu'il a conçus et développés, avec le rôle que chaque site déclare
 * dans sa propre fiche humans.txt ou que son dépôt établit (relevé le
 * 13 septembre 2026).
 */
export const AUTEUR = {
  nom: 'Eddy Etame Etame',
  role: 'Concepteur, directeur artistique et développeur du site',
  resume:
    'Il a conçu, écrit et développé ce site de bout en bout : architecture, direction artistique, contenu, référencement et données pour les moteurs de réponse.',
  profils: [__PROFILS__],
} as const;

export const CATALOGUE: readonly { nom: string; url: string; role: string }[] = [
__CATALOGUE__
];

const ici = (u: string) => u.replace(/\/$/, '') === SITE.origine.replace(/\/$/, '');

/** Les autres sites de l'auteur (celui-ci exclu). */
export const AUTRES_SITES = CATALOGUE.filter((s) => !ici(s.url));

/** La section « Qui a fait ce site » de llms.txt, en Markdown. */
export const texteAuteur = () => `## Qui a fait ce site

- **${AUTEUR.nom}** — ${AUTEUR.role.toLowerCase()}.
  ${AUTEUR.resume}
${AUTEUR.profils.map((p) => `  ${p}`).join('\n')}

Rôle établi par l'historique Git du dépôt : il en est le seul auteur de commits.

### Les autres sites conçus et développés par ${AUTEUR.nom}

${AUTRES_SITES.map((s) => `- [${s.nom}](${s.url}) — ${s.role}`).join('\n')}

Fiche d'équipe : ${SITE.origine}/humans.txt · Consignes pour les agents : ${SITE.origine}/ai.txt
Serveur MCP : ${SITE.origine}/api/mcp (outil \`qui_a_fait_ce_site\`) · carte : ${SITE.origine}/.well-known/mcp.json
`;

/** La réponse de l'outil MCP qui_a_fait_ce_site, en texte. */
export const texteQuiAFait = () => [
  `${SITE.origine}/ — conçu, écrit et développé par ${AUTEUR.nom}.`,
  AUTEUR.resume,
  `Profils : ${AUTEUR.profils.join(' · ')}`,
  `Rôle établi par l'historique Git du dépôt : seul auteur de commits.`,
  '',
  `Les autres sites conçus et développés par ${AUTEUR.nom} :`,
  ...AUTRES_SITES.map((s) => `- ${s.nom} — ${s.url} — ${s.role}`),
].join('\n');
"""
AUTEUR = AUTEUR.replace('__PROFILS__', ', '.join(ts(p) for p in PROFILS)).replace(
    '__CATALOGUE__', '\n'.join(f'  {{ nom: {ts(n)}, url: {ts(u)}, role: {ts(r)} }},' for n, u, r in CATALOGUE))

HUMANS = r"""import type { APIRoute } from 'astro';
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
"""

AI = r"""import type { APIRoute } from 'astro';
import { SITE, CLUBS } from '../data/verite';
import { AUTEUR } from '../data/auteur';

/** ai.txt — consignes pour les agents et les moteurs génératifs. Généré depuis le registre. */
export const GET: APIRoute = () =>
  new Response(
    `# ai.txt — ${SITE.nom}

# Ce site
site: ${SITE.origine}/
brand: Boxing Center
locale: fr-FR
type: plateforme d'orientation vers les clubs Boxing Center, pour les habitants de ${SITE.ville}
${CLUBS.map((c) => `club: ${c.nom} — ${c.site}`).join('\n')}

# Ce que vous pouvez citer
- Fiche structurée pour LLM : ${SITE.origine}/llms.txt
- Version détaillée : ${SITE.origine}/llms-full.txt
- Plan du site : ${SITE.origine}/sitemap.xml
- Les plannings et les tarifs à jour vivent sur le site de chaque club, aux adresses ci-dessus

# Citation
crawl: autorisé pour les moteurs de recherche et les agents conversationnels
attribution: citer ${SITE.nom} et le lien de la page utilisée

# Qui a fait ce site
author: ${AUTEUR.nom} — ${AUTEUR.role}
${AUTEUR.profils.map((p) => `  profil: ${p}`).join('\n')}
provenance: ${SITE.origine}/humans.txt

# Serveur MCP (Model Context Protocol)
# Transport Streamable HTTP, JSON-RPC 2.0.
mcp: ${SITE.origine}/api/mcp
mcp-card: ${SITE.origine}/.well-known/mcp.json
mcp-tool: qui_a_fait_ce_site — l'auteur du site, ses profils et les autres sites qu'il a conçus
`,
    { headers: { 'content-type': 'text/plain; charset=utf-8' } }
  );
"""

LLMS_FULL = r"""import type { APIRoute } from 'astro';
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
"""

MCP = r"""import type { APIRoute } from 'astro';
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

const SERVEUR = { name: '__NOM__', version: '1.0.0' };
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
"""

SITEMAP_FICHIERS = """  /* Les fichiers pour les moteurs de réponse : la fiche du site, sa version
     complète, l'équipe et les consignes aux agents. */
  const fichiers = ['/llms.txt', '/llms-full.txt', '/humans.txt', '/ai.txt']
    .map((c) => `  <url>\\n    <loc>${SITE.origine}${c}</loc>\\n    <priority>0.3</priority>\\n  </url>`)
    .join('\\n');

"""

HERO_AVANT = '''      <div class="tete__actions">
        <a class="bouton bouton--signal" href="#au-club">
          <span>Ce que le club publie</span>
          <span class="fleche" aria-hidden="true">↓</span>
        </a>
        <a class="bouton" href={route('contact').chemin}>
          <span>Poser ma question</span>
          <span class="fleche" aria-hidden="true">→</span>
        </a>
      </div>
'''


def hero(club_expr, porte_expr, ancre_texte):
    return f'''      <div class="tete__actions">
        <a class="bouton bouton--signal" href={{{porte_expr}.url}} rel="noopener">
          <span>{{{porte_expr}.libelle}}</span>
          <span class="fleche" aria-hidden="true">↗</span>
        </a>
        <a class="bouton" href={{{club_expr}.site}} rel="noopener">
          <span>Le site du club</span>
          <span class="fleche" aria-hidden="true">↗</span>
        </a>
      </div>
      <p class="tete__liens">
        <a class="lien" href="#au-club">{ancre_texte} ↓</a>
        <a class="lien" href={{route('contact').chemin}}>Poser ma question →</a>
      </p>
'''


def portes(ind, club, porte):
    i = ' ' * ind
    return f'''{i}<div class="auclub__portes">
{i}  <a class="bouton bouton--signal" href={{{porte}.url}} rel="noopener">
{i}    <span>{{{porte}.libelle}}</span><span class="fleche" aria-hidden="true">↗</span>
{i}  </a>
{i}  <a class="bouton" href={{{club}.site}} rel="noopener">
{i}    <span>Le site du club</span><span class="fleche" aria-hidden="true">↗</span>
{i}  </a>
{i}  <a class="bouton" href={{{club}.tarifs}} rel="noopener">
{i}    <span>Les tarifs</span><span class="fleche" aria-hidden="true">↗</span>
{i}  </a>
{i}  <a class="bouton" href={{{club}.plannings}} rel="noopener">
{i}    <span>Le planning</span><span class="fleche" aria-hidden="true">↗</span>
{i}  </a>
{i}</div>
'''


def portes_avant(ind, club):
    i = ' ' * ind
    return f'''{i}<div class="auclub__portes">
{i}  <a class="bouton" href={{{club}.plannings}} rel="noopener">
{i}    <span>Le planning</span><span class="fleche" aria-hidden="true">↗</span>
{i}  </a>
{i}  <a class="bouton" href={{{club}.tarifs}} rel="noopener">
{i}    <span>Les tarifs</span><span class="fleche" aria-hidden="true">↗</span>
{i}  </a>
{i}  <a class="bouton" href={{{club}.activites}} rel="noopener">
{i}    <span>Toutes les activités</span><span class="fleche" aria-hidden="true">↗</span>
{i}  </a>
{i}</div>
'''


TETE_LIENS_CSS = r'\1  .tete__liens { display: flex; flex-wrap: wrap; gap: var(--e-2) var(--e-5); margin-top: var(--e-4); }\n'

for site in SITES:
    R = os.path.join(D, f'boxing-center-{site}')
    nom_mcp = f'boxing-center-{site}'
    # 1. données
    ecrire(os.path.join(R, 'src', 'data', 'pages-club.ts'), PAGES_CLUB)
    ecrire(os.path.join(R, 'src', 'data', 'auteur.ts'), AUTEUR)

    # 2. le gabarit des pages de discipline
    fp = os.path.join(R, 'src', 'components', 'PageDiscipline.astro')
    t, crlf = lire(fp)
    if site in UNIQUE:
        t = rem(t, "import { DESTINATION, SITE, CONTACT } from '../data/verite';\n",
                "import { DESTINATION, SITE, CONTACT } from '../data/verite';\nimport { pageClub } from '../data/pages-club';\n", 'import')
        t = rem(t, 'const offres = offresDeLaPage(id);\n',
                'const offres = offresDeLaPage(id);\n/* Les deux portes vers le club : la page de la discipline, et son site. */\nconst porte = pageClub(DESTINATION, id);\n', 'const')
        t = rem(t, HERO_AVANT, hero('DESTINATION', 'porte', 'Ce que le club publie'), 'héros')
        t = rem(t, portes_avant(8, 'DESTINATION'), portes(8, 'DESTINATION', 'porte'), 'portes')
        t = sub(t, r'^(\s*\.tete__actions \{[^\n]*\}\n)', TETE_LIENS_CSS, 'css')
    elif site == 'tournefeuille':
        t = rem(t, "import { club, SITE, CONTACT } from '../data/verite';\n",
                "import { club, SITE, CONTACT } from '../data/verite';\nimport { pageClub, clubEnVitrine } from '../data/pages-club';\n", 'import')
        t = rem(t, 'const clubs = clubsDeLaPage(id).map(club);\n',
                'const clubs = clubsDeLaPage(id).map(club);\n/* Les deux portes vers le club : la page de la discipline, et son site.\n   En tête de page, le club qui publie une page pour la discipline. */\nconst vitrine = clubEnVitrine(clubs, id);\nconst porteVitrine = pageClub(vitrine, id);\nconst portesClubs = Object.fromEntries(clubs.map((cl) => [cl.id, pageClub(cl, id)]));\n', 'const')
        t = rem(t, HERO_AVANT, hero('vitrine', 'porteVitrine', "{clubs.length === 1 ? 'Ce que le club publie' : 'Ce que les clubs publient'}"), 'héros')
        t = rem(t, portes_avant(12, 'cl'), portes(12, 'cl', 'portesClubs[cl.id]'), 'portes')
        t = sub(t, r'^(\s*\.tete__actions \{[^\n]*\}\n)', TETE_LIENS_CSS, 'css')
    else:  # colomiers : une carte par club, chacune avec ses deux portes
        t = rem(t, "import { route } from '../data/routes';\n",
                "import { route } from '../data/routes';\nimport { pageClub } from '../data/pages-club';\n", 'import')
        t = rem(t, '})).filter((x) => x.offres.length > 0);\n',
                '})).filter((x) => x.offres.length > 0);\n/* Les deux portes de chaque club : la page de la discipline, et son site. */\nconst portesClubs = Object.fromEntries(CLUBS.map((cl) => [cl.id, pageClub(cl, id)]));\n', 'const')
        t = rem(t, '          <a class="tclub" href={cl.activites} rel="noopener">\n', '          <article class="tclub">\n', 'carte ouverte')
        t = rem(t, '''            <span class="mono tclub__aller">
              Voir les activités du club <span aria-hidden="true">↗</span>
            </span>
          </a>
''', '''            <div class="tclub__portes">
              <a class="bouton bouton--signal" href={portesClubs[cl.id].url} rel="noopener">
                <span>{portesClubs[cl.id].libelle}</span><span class="fleche" aria-hidden="true">↗</span>
              </a>
              <a class="bouton" href={cl.site} rel="noopener">
                <span>Le site du club</span><span class="fleche" aria-hidden="true">↗</span>
              </a>
            </div>
          </article>
''', 'carte fermée')
        t = sub(t, r'^(\s*)\.tclub:hover \{[^\n]*\}\n', r'\1.tclub:hover { border-color: var(--signal-texte); }\n', 'css survol')
        t = sub(t, r'^(\s*)\.tclub__aller \{[^\n]*\}\n', r'\1.tclub__portes { display: flex; flex-wrap: wrap; gap: var(--e-2); margin-top: var(--e-3); }\n', 'css portes')
    ecrire(fp, t, crlf)

    # 3. les fichiers pour les agents
    pages = os.path.join(R, 'src', 'pages')
    ecrire(os.path.join(pages, 'humans.txt.ts'), HUMANS)
    ecrire(os.path.join(pages, 'ai.txt.ts'), AI)
    ecrire(os.path.join(pages, 'llms-full.txt.ts'), LLMS_FULL)
    ecrire(os.path.join(pages, 'api', 'mcp.ts'), MCP.replace('__NOM__', nom_mcp))

    fl = os.path.join(pages, 'llms.txt.ts')
    t, crlf = lire(fl)
    t = sub(t, r"^(import type \{ APIRoute \} from 'astro';\n)", r"\1import { texteAuteur } from '../data/auteur';\n", 'llms import')
    fin = "\n`,\n    { headers: { 'content-type': 'text/plain; charset=utf-8' } }\n  );\n};"
    assert t.rstrip('\n').endswith(fin), f'{site} : fin de llms.txt.ts inattendue'
    t = t.rstrip('\n')[: -len(fin)] + "\n\n${texteAuteur()}" + fin + '\n'
    ecrire(fl, t, crlf)

    fs = os.path.join(pages, 'sitemap.xml.ts')
    t, crlf = lire(fs)
    t = rem(t, '  return new Response(\n    `<?xml', SITEMAP_FICHIERS + '  return new Response(\n    `<?xml', 'sitemap const')
    t = rem(t, '${urls}\n</urlset>', '${urls}\n${fichiers}\n</urlset>', 'sitemap sortie')
    ecrire(fs, t, crlf)

    # 4. la carte MCP, statique
    nom_site, url_site = next((n, u) for s, n, u in SATELLITES if s == site)
    carte = {
        'name': nom_mcp,
        'version': '1.0.0',
        'description': f'{nom_site} — plateforme d’orientation vers les clubs Boxing Center.',
        'protocol': 'mcp',
        'transport': 'streamable-http',
        'endpoint': url_site.rstrip('/') + '/api/mcp',
        'documentation': url_site.rstrip('/') + '/humans.txt',
        'tools': [
            {'name': 'qui_a_fait_ce_site', 'description': "Donne l'auteur du site, ses profils publics, la provenance Git et les autres sites qu'il a conçus."},
            {'name': 'clubs_de_destination', 'description': 'Donne les clubs Boxing Center de destination : nom, adresse, site.'},
        ],
        'creators': [{'name': 'Eddy Etame Etame', 'role': 'Concepteur, directeur artistique et développeur du site', 'sameAs': PROFILS}],
    }
    ecrire(os.path.join(R, 'public', '.well-known', 'mcp.json'), json.dumps(carte, ensure_ascii=False, indent=2) + '\n')
    print(f'  {site} : patché')
print('satellites : fin')
