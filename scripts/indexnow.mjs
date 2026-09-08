/**
 * IndexNow — prévenir Bing, Yandex, Seznam et les moteurs qui partagent le
 * protocole qu'une page a changé, au lieu d'attendre leur passage.
 *
 * Google n'y participe pas : pour lui, le sitemap et la Search Console.
 *
 * À lancer après un déploiement de PRODUCTION, jamais après un aperçu :
 *
 *   npm run indexnow
 *
 * La clé est publiée dans public/<clé>.txt ; c'est ainsi que le moteur
 * vérifie qu'on parle bien au nom du domaine.
 */
import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const RACINE = join(dirname(fileURLToPath(import.meta.url)), '..');
const HOTE = 'www.boxingcenter-colomiers.fr';
const CLE = '7f3a9c2e5b8d4f1a6c0e9b3d2a5f8c1e';

/** Les URL indexables, lues dans le sitemap produit — jamais une liste à part. */
function urlsDuSitemap() {
  const xml = readFileSync(join(RACINE, '.vercel/output/static/sitemap.xml'), 'utf8');
  return [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
}

const urlList = urlsDuSitemap();
if (!urlList.length) {
  console.error('Aucune URL dans le sitemap — lance « npm run build » d’abord.');
  process.exit(1);
}

const reponse = await fetch('https://api.indexnow.org/indexnow', {
  method: 'POST',
  headers: { 'content-type': 'application/json; charset=utf-8' },
  body: JSON.stringify({
    host: HOTE,
    key: CLE,
    keyLocation: `https://${HOTE}/${CLE}.txt`,
    urlList,
  }),
});

console.log(`IndexNow : ${reponse.status} ${reponse.statusText} — ${urlList.length} URL soumises`);
if (!reponse.ok) {
  console.error(await reponse.text());
  process.exit(1);
}
