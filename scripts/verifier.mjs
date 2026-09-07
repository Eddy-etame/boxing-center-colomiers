/**
 * CONTRÔLE QUALITÉ du build.
 *
 * Ce script tourne sur le HTML réellement produit, pas sur les sources : il
 * voit ce que verront Google et le visiteur. Il échoue le build quand une
 * règle du projet est violée, pour qu'une régression ne parte jamais en ligne
 * sur la foi d'une relecture humaine.
 *
 *   node scripts/verifier.mjs
 *
 * Il vérifie :
 *   1. aucune formulation interdite (« salle à Colomiers »)
 *   2. aucun lien interne cassé
 *   3. un H1 unique par page, hiérarchie de titres sans saut
 *   4. aucune image sans texte alternatif
 *   5. titles et meta descriptions uniques, présents, de longueur tenable
 *   6. présence du canonique et du JSON-LD, JSON-LD parsable
 *   7. les liens sortants attendus par le cahier des charges sont bien là
 */

import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const RACINE = join(dirname(fileURLToPath(import.meta.url)), '..');
const DIST = existsSync(join(RACINE, '.vercel/output/static'))
  ? join(RACINE, '.vercel/output/static')
  : join(RACINE, 'dist');

/** Laisser croire qu'une salle est DANS Colomiers — cahier des charges §2. */
const INTERDIT = [
  'salle de Colomiers',
  'notre salle à Colomiers',
  'notre club à Colomiers',
  'situé à Colomiers',
  'située à Colomiers',
  'basé à Colomiers',
  'Boxing Center Colomiers vous accueille',
];

/**
 * VENDRE L'ABSENCE — la faute inverse, et la plus coûteuse des deux.
 *
 * Quelqu'un qui cherche « club de boxe Colomiers » ne doit jamais lire, en
 * arrivant, qu'il s'est trompé d'endroit. On dit ce qui existe — deux clubs
 * à proximité qui l'accueillent — jamais ce qui manque.
 *
 * Ces tournures restent légitimes dans un commentaire de code ou une phrase
 * qui ne parle pas des clubs (« n'a pas de sens ») : le contrôle ne les
 * cherche que dans le texte visible, et uniquement quand Colomiers ou une
 * salle sont dans la même phrase.
 */
const VENTE_NEGATIVE = [
  'pas de salle',
  'pas de club',
  'aucune salle',
  'aucun club',
  'n’existe pas de salle',
  "n'existe pas de salle",
  'ne se trouve dans cette commune',
];

/** Liens sortants que le cahier des charges impose, et où. */
const BACKLINKS = [
  ['/plannings/', 'boxe-toulouse.com'],
  ['/tarifs/', 'boxe-toulouse.com'],
  ['/', 'boxing-center-portet.fr'],
];

const erreurs = [];
const avertissements = [];

function pages(dir, base = '') {
  const out = [];
  for (const e of readdirSync(dir)) {
    const p = join(dir, e);
    if (statSync(p).isDirectory()) out.push(...pages(p, `${base}/${e}`));
    else if (e === 'index.html') out.push([`${base}/` || '/', p]);
    else if (e.endsWith('.html')) out.push([`${base}/${e}`, p]);
  }
  return out;
}

const texteVisible = (html) =>
  html
    .replace(/<script[\s\S]*?<\/script>/g, ' ')
    .replace(/<style[\s\S]*?<\/style>/g, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;|&#160;/g, ' ')
    .replace(/\s+/g, ' ');

const toutes = pages(DIST);
const routes = new Set(toutes.map(([r]) => (r.endsWith('/') ? r : r + '/')));
const titres = new Map();
const descriptions = new Map();

for (const [route, fichier] of toutes) {
  const html = readFileSync(fichier, 'utf8');
  const txt = texteVisible(html);
  const ou = (m) => `${route.padEnd(22)} ${m}`;

  // 1 — formulations interdites : ne pas laisser croire à une salle à Colomiers
  const bas = txt.toLowerCase();
  for (const f of INTERDIT) {
    if (bas.includes(f.toLowerCase())) {
      erreurs.push(ou(`formulation interdite : « ${f} »`));
    }
  }

  // 1 bis — vente négative : ne jamais mettre en avant ce qui n'existe pas
  for (const f of VENTE_NEGATIVE) {
    let i = bas.indexOf(f.toLowerCase());
    while (i !== -1) {
      // On ne s'alarme que si la phrase parle bien des clubs ou de la ville.
      const phrase = bas.slice(Math.max(0, i - 140), i + 140);
      if (/colomiers|boxing center|salle|club/.test(phrase)) {
        erreurs.push(ou(`vente négative : « ${f} » — dire ce qui existe, pas ce qui manque`));
        break;
      }
      i = bas.indexOf(f.toLowerCase(), i + 1);
    }
  }

  // 2 — liens internes
  for (const m of html.matchAll(/href="(\/[^"#?]*)/g)) {
    let cible = m[1];
    if (cible.startsWith('/api/') || /\.[a-z0-9]{2,5}$/i.test(cible)) continue;
    if (!cible.endsWith('/')) cible += '/';
    if (!routes.has(cible)) erreurs.push(ou(`lien interne cassé : ${m[1]}`));
  }

  // 3 — titres
  const h1 = [...html.matchAll(/<h1[\s>]/g)].length;
  if (h1 === 0) erreurs.push(ou('aucun <h1>'));
  if (h1 > 1) erreurs.push(ou(`${h1} <h1> — il en faut exactement un`));

  const niveaux = [...html.matchAll(/<h([1-4])[\s>]/g)].map((m) => Number(m[1]));
  for (let i = 1; i < niveaux.length; i++) {
    if (niveaux[i] - niveaux[i - 1] > 1) {
      avertissements.push(ou(`saut de titre h${niveaux[i - 1]} → h${niveaux[i]}`));
      break;
    }
  }

  // 4 — images sans alt (alt="" est légitime : image décorative)
  for (const m of html.matchAll(/<img\b[^>]*>/g)) {
    if (!/\salt=/.test(m[0])) erreurs.push(ou(`<img> sans attribut alt : ${m[0].slice(0, 70)}…`));
  }

  // 5 — title et description
  const t = html.match(/<title>([^<]*)<\/title>/)?.[1] ?? '';
  const d = html.match(/<meta name="description" content="([^"]*)"/)?.[1] ?? '';
  if (!t) erreurs.push(ou('<title> vide'));
  if (!d) erreurs.push(ou('meta description absente'));
  if (t && titres.has(t)) erreurs.push(ou(`<title> en double avec ${titres.get(t)}`));
  if (d && descriptions.has(d)) erreurs.push(ou(`description en double avec ${descriptions.get(d)}`));
  titres.set(t, route);
  descriptions.set(d, route);
  if (t.length > 65) avertissements.push(ou(`title de ${t.length} caractères (tronqué au-delà de ~60)`));
  if (d.length > 165) avertissements.push(ou(`description de ${d.length} caractères`));

  // 6 — canonique et données structurées
  if (!/rel="canonical"/.test(html)) erreurs.push(ou('lien canonique absent'));
  const ld = html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)?.[1];
  if (!ld) erreurs.push(ou('JSON-LD absent'));
  else {
    try {
      JSON.parse(ld);
    } catch {
      erreurs.push(ou('JSON-LD invalide'));
    }
  }
}

// 7 — les liens sortants exigés
for (const [route, hote] of BACKLINKS) {
  const f = join(DIST, route === '/' ? 'index.html' : `${route.replace(/^\/|\/$/g, '')}/index.html`);
  if (!existsSync(f)) {
    erreurs.push(`${route} introuvable — lien sortant ${hote} invérifiable`);
    continue;
  }
  if (!readFileSync(f, 'utf8').includes(hote)) {
    erreurs.push(`${route.padEnd(22)} lien sortant manquant vers ${hote} (cahier des charges §9)`);
  }
}

console.log(`\n  ${toutes.length} pages analysées dans ${DIST.replace(RACINE, '.')}\n`);
for (const a of avertissements) console.log(`  ⚠  ${a}`);
for (const e of erreurs) console.log(`  ✗  ${e}`);

if (!erreurs.length && !avertissements.length) console.log('  Rien à signaler.\n');
else console.log(`\n  ${erreurs.length} erreur(s), ${avertissements.length} avertissement(s)\n`);

process.exit(erreurs.length ? 1 : 0);
