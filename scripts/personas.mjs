/**
 * LA PASSE PERSONA — sur le HTML livré des sept sites.
 *
 * Chaque persona pose ses questions au fichier produit, pas au code source.
 * On ne cherche pas ce qui compile : on cherche ce qu'un visiteur verrait.
 *
 *   node personas.mjs
 */

import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const BASE = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const SITES = [
  'boxing-center-colomiers',
  'boxing-center-muret',
  'boxing-center-cugnaux',
  'boxing-center-tournefeuille',
  'boxing-center-labege',
  'boxing-center-lunion',
  'boxing-center-castelginest',
];

const pages = (dir, base = dir) => {
  const out = [];
  for (const e of readdirSync(dir)) {
    const p = join(dir, e);
    if (statSync(p).isDirectory()) out.push(...pages(p, base));
    else if (e === 'index.html') {
      const r = p.slice(base.length).replace(/\\/g, '/').replace(/index\.html$/, '') || '/';
      out.push([r, p]);
    }
  }
  return out;
};

const texteVisible = (html) =>
  html
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(+n))
    .replace(/&[a-z]+;/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

/* ─────────────────────  Les questions de chaque persona  ───────────────────── */

const FIGURES = [
  // métaphores et comparaisons qu'Eddy a explicitement bannies
  /\bcomme (?:un|une|le|la|si)\b/gi,
  /\bà l'image d(?:e|u|es)\b/gi,
  /\bvéritable\b/gi,
  /\bau cœur d(?:e|u|es)\b/gi,
  /\bune histoire de\b/gi,
  /\ble temple\b/gi,
  /\bl'écrin\b/gi,
  /\bplonger dans\b/gi,
];

const MOTS_CREUX = [
  'n’hésitez pas',
  'n’hésite pas',
  'notre équipe de professionnels',
  'depuis de nombreuses années',
  'à votre écoute',
  'lorem',
  'TODO',
  'à compléter',
  'texte à venir',
];

const rapport = [];

for (const site of SITES) {
  const dist = join(BASE, site, '.vercel', 'output', 'static');
  if (!existsSync(dist)) {
    rapport.push({ site, erreur: 'build absent' });
    continue;
  }
  const toutes = pages(dist);
  const constats = [];
  /* Le favicon : la marque du site dans l'onglet. Sept sites, sept signes. */
  const favicon = join(dist, 'favicon-192.png');
  const faviconMd5 = existsSync(favicon)
    ? createHash('md5').update(readFileSync(favicon)).digest('hex').slice(0, 8)
    : '';
  const vignettes = new Map();
  const titres = new Map();
  const h1s = new Map();
  let motsTotal = 0;

  for (const [route, fichier] of toutes) {
    const html = readFileSync(fichier, 'utf8');
    const txt = texteVisible(html);
    const mots = txt.split(/\s+/).length;
    motsTotal += mots;

    // ── Le robot : une page = un titre, un h1, une description ──
    const titre = /<title>([^<]*)<\/title>/.exec(html)?.[1] ?? '';
    const desc = /<meta name="description" content="([^"]*)"/.exec(html)?.[1] ?? '';
    const nbH1 = (html.match(/<h1[\s>]/g) || []).length;
    if (nbH1 !== 1) constats.push(`${route} — ${nbH1} <h1>`);
    if (titres.has(titre)) constats.push(`${route} — titre identique à ${titres.get(titre)}`);
    titres.set(titre, route);
    const h1 = /<h1[^>]*>([\s\S]*?)<\/h1>/.exec(html)?.[1];
    if (h1) {
      const plat = texteVisible(h1);
      if (h1s.has(plat)) constats.push(`${route} — même <h1> que ${h1s.get(plat)} : « ${plat.slice(0, 50)} »`);
      h1s.set(plat, route);
    }
    if (!desc) constats.push(`${route} — sans description`);

    // ── Le robot : ordre des titres ──
    const niveaux = [...html.matchAll(/<h([1-6])[\s>]/g)].map((m) => +m[1]);
    for (let i = 1; i < niveaux.length; i++) {
      if (niveaux[i] - niveaux[i - 1] > 1) {
        constats.push(`${route} — saut de titre h${niveaux[i - 1]} → h${niveaux[i]}`);
        break;
      }
    }

    // ── Le prospect : une image sans alt est une image muette ──
    for (const m of html.matchAll(/<img\b[^>]*>/g)) {
      if (!/\salt=/.test(m[0])) constats.push(`${route} — <img> sans alt`);
    }

    // ── Le hater : le lien qui ne dit pas où il va ──
    for (const m of html.matchAll(/<a\b[^>]*>([\s\S]*?)<\/a>/g)) {
      const libelle = texteVisible(m[1]).toLowerCase();
      if (['ici', 'cliquez ici', 'en savoir plus', 'lire la suite', 'voir'].includes(libelle)) {
        constats.push(`${route} — lien opaque : « ${libelle} »`);
      }
      if (!libelle && !/aria-label=/.test(m[0]) && !/<img/.test(m[1])) {
        constats.push(`${route} — lien sans texte`);
      }
    }

    // ── Eddy : aucune figure de style ──
    for (const re of FIGURES) {
      for (const m of txt.matchAll(re)) {
        constats.push(`${route} — figure de style : « ${m[0]} »`);
      }
    }

    // ── Le hater : le mot creux, le reste de gabarit ──
    for (const mot of MOTS_CREUX) {
      if (txt.toLowerCase().includes(mot.toLowerCase())) {
        constats.push(`${route} — formule creuse : « ${mot} »`);
      }
    }

    // ── Le prospect : une page trop courte ne répond à rien ──
    if (mots < 220 && !['/merci/', '/404/'].includes(route)) {
      constats.push(`${route} — ${mots} mots seulement`);
    }

    // ── Le partage : une vignette composée pour cette page, et pour elle seule ──
    const ogImage = /<meta property="og:image" content="([^"]*)"/.exec(html)?.[1] ?? '';
    if (!ogImage) constats.push(`${route} — sans og:image`);
    else {
      const chemin = ogImage.replace(/^https?:\/\/[^/]+/, '');
      if (!chemin.startsWith('/og/')) {
        constats.push(`${route} — og:image est une photo partagée, pas une vignette de page : ${chemin}`);
      } else if (!existsSync(join(dist, chemin))) {
        constats.push(`${route} — vignette absente du build : ${chemin}`);
      }
      if (vignettes.has(ogImage)) constats.push(`${route} — même og:image que ${vignettes.get(ogImage)}`);
      else vignettes.set(ogImage, route);
    }

    // ── Le robot : le lien interne qui ne mène nulle part ──
    for (const m of html.matchAll(/href="(\/[^"#?]*)"/g)) {
      const cible = m[1].endsWith('/') ? m[1] : m[1] + '/';
      if (/\.(png|jpe?g|webp|avif|svg|xml|txt|ico|json|webmanifest|woff2?|css|js|mjs|pdf|mp4)$/.test(m[1])) continue;
      if (m[1].startsWith('/_astro/') || m[1].startsWith('/photos/') || m[1].startsWith('/fonts/')) continue;
      if (!toutes.some(([r]) => r === cible)) {
        constats.push(`${route} — lien interne mort : ${m[1]}`);
      }
    }
  }

  rapport.push({ site, pages: toutes.length, mots: motsTotal, constats, faviconMd5 });
}

/* Un favicon partagé par deux sites est un défaut de barre : la marque de
   l'onglet doit dire lequel des sept on a ouvert. */
const parFavicon = new Map();
for (const r of rapport) {
  if (!r.faviconMd5) continue;
  parFavicon.set(r.faviconMd5, [...(parFavicon.get(r.faviconMd5) ?? []), r.site]);
}
for (const [md5, sites] of parFavicon) {
  if (sites.length < 2) continue;
  for (const r of rapport) {
    if (sites.includes(r.site)) r.constats.push(`favicon-192.png (${md5}) identique à : ${sites.filter((s) => s !== r.site).join(', ')}`);
  }
}

/* ─────────────────────────────  Sortie  ───────────────────────────── */

let total = 0;
for (const r of rapport) {
  if (r.erreur) {
    console.log(`\n══ ${r.site} : ${r.erreur}`);
    continue;
  }
  const uniques = [...new Set(r.constats)];
  total += uniques.length;
  console.log(`\n══ ${r.site} — ${r.pages} pages, ${r.mots} mots`);
  if (!uniques.length) console.log('   rien à signaler');
  for (const c of uniques.slice(0, 25)) console.log(`   · ${c}`);
  if (uniques.length > 25) console.log(`   … et ${uniques.length - 25} autres`);
}
console.log(`\n${total} constat(s) au total\n`);
