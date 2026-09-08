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
 *   8. chaque page porte ses mots-clés prioritaires (src/data/mots-cles.ts)
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

/**
 * FAITS FAUX — des affirmations qui ont déjà été publiées une fois et qui
 * contredisent les pages activités officielles des clubs. Le MMA, le
 * grappling et le JJB n'existent qu'à Portet ; les écrire aux deux clubs
 * envoie quelqu'un dans une salle qui ne propose pas ce qu'il cherche.
 */
const FAITS_FAUX = [
  'mma se pratique dans les deux',
  'deux clubs proposent le mma',
  'les deux proposent la boxe anglaise, le mma',
  'mma à toulouse minimes',
  'mma à minimes',
  'grappling à minimes',
];

/** Liens sortants que le cahier des charges impose, et où. */
const BACKLINKS = [
  ['/plannings/', 'boxe-toulouse.com'],
  ['/tarifs/', 'boxe-toulouse.com'],
  ['/', 'boxing-center-portet.fr'],
];

/**
 * Le registre des mots-clés vit dans src/data/mots-cles.ts. On le lit ici
 * sans compilateur, comme build-images.mjs lit le manifeste média : une seule
 * source, pas de copie à maintenir dans ce script.
 */
function lireClusters() {
  const src = readFileSync(join(RACINE, 'src', 'data', 'mots-cles.ts'), 'utf8');
  const clusters = [];
  const re = /page:\s*'([^']+)',\s*prioritaires:\s*\[([\s\S]*?)\]/g;
  let m;
  while ((m = re.exec(src))) {
    const mots = [...m[2].matchAll(/'([^']+)'/g)].map((x) => x[1]);
    clusters.push({ page: m[1], prioritaires: mots });
  }
  return clusters;
}

/** Comparaison insensible à la casse et aux accents. */
const plat = (t) => t.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();

const CHEMIN_PAR_PAGE = {
  accueil: '/',
  'boxe-anglaise': '/boxe-anglaise/',
  mma: '/mma/',
  'boxing-fitness': '/boxing-fitness/',
  'boxe-enfants': '/boxe-enfants/',
  plannings: '/plannings/',
  tarifs: '/tarifs/',
  'premiere-seance': '/premiere-seance/',
  'quel-club': '/quel-club/',
  contact: '/contact/',
};

const erreurs = [];
const avertissements = [];
const textesParRoute = new Map();

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
  textesParRoute.set(route, txt);
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

  // 1 ter — un fait contredit par les sites officiels des clubs
  for (const f of FAITS_FAUX) {
    if (plat(bas).includes(plat(f))) erreurs.push(ou(`fait faux : « ${f} » — voir src/data/offres.ts`));
  }

  // 1 quater — une heure de fermeture écrite ailleurs que dans le registre
  for (const h of ['21h15', '21h00', '21h45', '22h']) {
    if (bas.includes(h)) erreurs.push(ou(`heure de fermeture en dur : « ${h} » — le registre dit 21h30`));
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

// 8 — chaque page porte son territoire de recherche
for (const { page, prioritaires } of lireClusters()) {
  const chemin = CHEMIN_PAR_PAGE[page];
  const txt = textesParRoute.get(chemin);
  if (!txt) {
    erreurs.push(`${chemin.padEnd(22)} page absente du build — mots-clés invérifiables`);
    continue;
  }
  const plan = plat(txt);
  for (const mot of prioritaires) {
    if (!plan.includes(plat(mot))) {
      erreurs.push(`${chemin.padEnd(22)} mot-clé prioritaire absent du texte visible : « ${mot} »`);
    }
  }
}

/* ───────────────  La source : ce qu'elle n'a pas le droit de savoir  ───────────────
   Les contrôles ci-dessus lisent le HTML produit. Deux défauts leur échappent
   parce qu'ils vivent dans la source : une heure écrite en dur dans un script
   qui ne s'exécute qu'au clic, et une règle CSS qui nomme un identifiant du
   registre — elle compile, elle passe, et elle n'affiche rien.
   Voir la loi commune §13.9. */

function fichiersSource(dossier) {
  const out = [];
  for (const e of readdirSync(dossier, { withFileTypes: true })) {
    const chemin = join(dossier, e.name);
    if (e.isDirectory()) out.push(...fichiersSource(chemin));
    else if (/\.(ts|astro|mjs|js)$/.test(e.name)) out.push(chemin);
  }
  return out;
}

const DOSSIER_SRC = join(RACINE, 'src');
if (existsSync(DOSSIER_SRC)) {
  /* Les identifiants que le registre des transports connaît, s'il existe. */
  const cheminTransports = join(RACINE, 'src', 'data', 'transports.ts');
  const idsItineraires = existsSync(cheminTransports)
    ? [...readFileSync(cheminTransports, 'utf8').matchAll(/^\s{4}id:\s*'([^']+)'/gm)].map((m) => m[1])
    : [];

  for (const fichier of fichiersSource(DOSSIER_SRC)) {
    const rel = fichier.slice(RACINE.length + 1).replace(/\\/g, '/');
    const estRegistre = rel.startsWith('src/data/');
    const src = readFileSync(fichier, 'utf8');

    /* A — une heure en dur hors du registre. Le registre est la seule source
       d'une heure : un club qui change d'amplitude ne doit pas laisser une
       phrase fausse dans un script. */
    if (!estRegistre) {
      for (const m of src.matchAll(/\b\d{1,2}\s?h\s?\d{2}\b/g)) {
        const ligne = src.slice(0, m.index).split('\n').length;
        erreurs.push(`${rel}:${ligne} — heure en dur : « ${m[0]} ». Une heure vit dans src/data/.`);
      }
    }

    /* B — une règle CSS qui nomme un identifiant d'itinéraire. Ces règles se
       génèrent depuis le registre, sinon un identifiant renommé laisse un
       onglet muet. */
    for (const m of src.matchAll(/#trajet-([a-z0-9-]+):checked/g)) {
      if (src.slice(Math.max(0, m.index - 400), m.index).includes('${')) continue;
      const ligne = src.slice(0, m.index).split('\n').length;
      erreurs.push(
        `${rel}:${ligne} — règle CSS écrite à la main pour « ${m[1]} ». ` +
          `Génère-la depuis ITINERAIRES (loi commune §13.9).`
      );
    }

    /* C — un nombre en lettres devant un décompte que le registre connaît. */
    const NOMBRES_ECRITS =
      /\b(deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|vingt)\s+(intitulés|trajets|itinéraires|disciplines publiées)\b/gi;
    for (const m of src.matchAll(NOMBRES_ECRITS)) {
      const ligne = src.slice(0, m.index).split('\n').length;
      avertissements.push(`${rel}:${ligne} — « ${m[0]} » : ce nombre se compte depuis le registre.`);
    }
  }

  /* D — chaque itinéraire du registre doit avoir sa règle d'affichage. */
  if (idsItineraires.length) {
    const transportsAstro = join(RACINE, 'src', 'components', 'Transports.astro');
    if (existsSync(transportsAstro)) {
      const c = readFileSync(transportsAstro, 'utf8');
      if (!c.includes('CSS_PANNEAUX')) {
        erreurs.push(
          'src/components/Transports.astro — les règles d’affichage des panneaux ne sont pas générées depuis le registre.'
        );
      }
    }
  }
}


console.log(`\n  ${toutes.length} pages analysées dans ${DIST.replace(RACINE, '.')}\n`);
for (const a of avertissements) console.log(`  ⚠  ${a}`);
for (const e of erreurs) console.log(`  ✗  ${e}`);

if (!erreurs.length && !avertissements.length) console.log('  Rien à signaler.\n');
else console.log(`\n  ${erreurs.length} erreur(s), ${avertissements.length} avertissement(s)\n`);

process.exit(erreurs.length ? 1 : 0);
