/**
 * L'ÉTAT SEO DES SEPT SITES — une ligne par page indexable.
 *
 * Longueur du titre et de la description, nombre de mots du <main>, liens
 * internes et sortants, types JSON-LD présents, canonique, et les motifs
 * prioritaires du registre qui MANQUENT au texte visible + titre + description.
 *
 *   node scripts/seo-etat.mjs
 */

import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const BASE = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const SITES = ['colomiers', 'muret', 'cugnaux', 'tournefeuille', 'labege', 'lunion', 'castelginest'];

const pages = (dir, base = dir) => {
  const out = [];
  for (const e of readdirSync(dir)) {
    const p = join(dir, e);
    if (statSync(p).isDirectory()) out.push(...pages(p, base));
    else if (e === 'index.html') {
      out.push([p.slice(base.length).replace(/\\/g, '/').replace(/index\.html$/, '') || '/', p]);
    }
  }
  return out;
};

const vis = (h) =>
  h
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(+n))
    .replace(/&amp;/g, '&')
    .replace(/\s+/g, ' ')
    .trim();

const plat = (t) => t.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

for (const d of SITES) {
  const racine = join(BASE, `boxing-center-${d}`);
  const dist = join(racine, '.vercel', 'output', 'static');
  if (!existsSync(dist)) { console.log(`\n══════ ${d.toUpperCase()} — build absent`); continue; }
  const mcPath = join(racine, 'src', 'data', 'mots-cles.ts');
  const mc = existsSync(mcPath) ? readFileSync(mcPath, 'utf8') : '';

  console.log(`\n══════ ${d.toUpperCase()}`);
  for (const [r, f] of pages(dist)) {
    if (/^\/(merci|404|mentions-legales|confidentialite)\//.test(r)) continue;
    const h = readFileSync(f, 'utf8');
    const t = (h.match(/<title>([^<]*)</) || ['', ''])[1];
    const desc = (h.match(/<meta name="description" content="([^"]*)"/) || ['', ''])[1];
    const canon = (h.match(/<link rel="canonical" href="([^"]*)"/) || ['', ''])[1];
    const ld = [...new Set([...h.matchAll(/"@type":\s*"([A-Za-z]+)"/g)].map((m) => m[1]))];
    const main = h.slice(h.indexOf('<main'), h.indexOf('</main>'));
    const mots = vis(main).split(' ').length;
    const inter = new Set([...main.matchAll(/href="(\/[a-z0-9-]+\/)"/g)].map((m) => m[1])).size;
    const ext = [...main.matchAll(/href="https?:\/\/(?!www\.boxingcenter-)[^"]+"/g)].length;

    const id = r === '/' ? 'accueil' : r.replace(/\//g, '');
    const re = new RegExp(`page: '${id}',\\s*\\n?\\s*prioritaires: \\[([\\s\\S]*?)\\]`);
    const cl = mc.match(re);
    const prio = cl ? [...cl[1].matchAll(/'([^']+)'/g)].map((m) => m[1]) : [];
    const txt = plat(vis(main) + ' ' + t + ' ' + desc);
    const manque = prio.filter((p) => !txt.includes(plat(p)));

    console.log(
      r.padEnd(22) +
        ' t' + String(t.length).padStart(3) +
        ' d' + String(desc.length).padStart(4) +
        ' m' + String(mots).padStart(5) +
        ' int' + String(inter).padStart(3) +
        ' ext' + String(ext).padStart(3) +
        ' ld[' + ld.join(',') + ']' +
        (canon ? '' : ' SANS-CANON') +
        (manque.length ? ' MANQUE:' + manque.join('|') : '') +
        ' | ' + t.slice(0, 60)
    );
  }
}
