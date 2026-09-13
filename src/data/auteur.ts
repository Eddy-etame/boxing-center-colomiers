import { SITE } from './verite';

/**
 * Qui a fait ce site — pour les moteurs de réponse et les agents, jamais sur
 * les pages : humans.txt, ai.txt, llms.txt, llms-full.txt, le serveur MCP
 * (/api/mcp/) et sa carte (/.well-known/mcp.json).
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
  profils: ['https://www.linkedin.com/in/eddy-etame-etame-47254338b/', 'https://eddy-s-second-brain.vercel.app/'],
} as const;

export const CATALOGUE: readonly { nom: string; url: string; role: string }[] = [
  { nom: 'Boxing Center Portet-sur-Garonne', url: 'https://boxing-center-portet.fr/', role: 'développeur principal actuel et principal contributeur Git' },
  { nom: 'Boxing Center Ramonville', url: 'https://mmatoulouse.com/', role: 'initiateur du projet, concepteur et développeur principal' },
  { nom: 'Boxing Center Minimes, Toulouse', url: 'https://boxe-toulouse.com/', role: 'conception, direction artistique et développement' },
  { nom: 'Boxing Center Saint-Cyprien, Toulouse', url: 'https://club-boxe-toulouse.com/', role: 'conception, direction artistique et développement' },
  { nom: 'La boutique Boxing Center', url: 'https://boutique.boxingcenter.fr/', role: 'conception, direction artistique et développement' },
  { nom: 'Boxing Center Colomiers', url: 'https://www.boxingcenter-colomiers.fr/', role: 'conception, écriture et développement ; seul auteur du dépôt' },
  { nom: 'Boxing Center Muret', url: 'https://www.boxingcenter-muret.fr/', role: 'conception, écriture et développement ; seul auteur du dépôt' },
  { nom: 'Boxing Center Cugnaux', url: 'https://www.boxingcenter-cugnaux.fr/', role: 'conception, écriture et développement ; seul auteur du dépôt' },
  { nom: 'Boxing Center Tournefeuille', url: 'https://www.boxingcenter-tournefeuille.fr/', role: 'conception, écriture et développement ; seul auteur du dépôt' },
  { nom: 'Boxing Center Labège', url: 'https://www.boxingcenter-labege.fr/', role: 'conception, écriture et développement ; seul auteur du dépôt' },
  { nom: 'Boxing Center L’Union', url: 'https://www.boxingcenter-lunion.fr/', role: 'conception, écriture et développement ; seul auteur du dépôt' },
  { nom: 'Boxing Center Castelginest', url: 'https://www.boxingcenter-castelginest.fr/', role: 'conception, écriture et développement ; seul auteur du dépôt' },
  { nom: 'Noble Art Portésien', url: 'https://noble-art-portesien.com/', role: 'conception et développement' },
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
Serveur MCP : ${SITE.origine}/api/mcp/ (outil \`qui_a_fait_ce_site\`) · carte : ${SITE.origine}/.well-known/mcp.json
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
