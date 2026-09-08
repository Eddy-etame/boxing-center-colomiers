/**
 * Pipeline image : lot WeTransfer brut (431 Mo, jusqu'à 28 Mo par fichier)
 * → AVIF + WebP + JPEG de repli, 4 largeurs, noms de fichiers SEO.
 *
 * On pré-cuit ici plutôt que de laisser Astro le faire au build : les sources
 * sont des JPEG plein capteur (6016 px), les faire traverser le build à chaque
 * déploiement coûterait des minutes pour un résultat identique.
 *
 *   node scripts/build-images.mjs          # ne refait que ce qui manque
 *   node scripts/build-images.mjs --force  # tout refaire
 */

import { mkdirSync, existsSync, readFileSync, writeFileSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import sharp from 'sharp';

const ICI = dirname(fileURLToPath(import.meta.url));
const RACINE = join(ICI, '..');
const SOURCE = join(RACINE, '..', 'wetransfer_dsc_3218-jpg_2026-09-07_1104');
const SORTIE = join(RACINE, 'public', 'photos');

const LARGEURS = [480, 768, 900, 1440, 2000];
const FORCE = process.argv.includes('--force');

/**
 * Les 25 fichiers du lot portent tous la signature « B.M.Photographie » en
 * bas à droite. On rogne le bandeau inférieur : une signature de photographe
 * n'a rien à faire dans l'interface d'un site client, et le crédit se porte
 * dans le pied de page, en texte, ce qui est plus honnête et lisible.
 *
 * 6 % : mesuré sur le fichier le plus haut du lot ; en dessous la signature
 * reste visible sur les cadrages portrait.
 */
const ROGNE_BAS = 0.06;

/** Ouvre la source déjà débarrassée de son bandeau signé. */
function ouvrir(chemin, l, h) {
  return sharp(chemin, { limitInputPixels: false })
    .rotate()
    .extract({ left: 0, top: 0, width: l, height: Math.round(h * (1 - ROGNE_BAS)) });
}

/** Lit le manifeste TypeScript sans compilateur : on extrait slug + source. */
function lireManifeste() {
  const src = readFileSync(join(RACINE, 'src', 'data', 'medias.ts'), 'utf8');
  const entrees = [];
  const re = /slug:\s*'([^']+)',\s*\n\s*source:\s*'([^']+)'/g;
  let m;
  while ((m = re.exec(src))) entrees.push({ slug: m[1], source: m[2] });
  return entrees;
}

const octets = (n) => (n / 1024 < 1000 ? `${(n / 1024).toFixed(0)} ko` : `${(n / 1048576).toFixed(1)} Mo`);

async function main() {
  const medias = lireManifeste();
  if (!medias.length) throw new Error('Manifeste vide — src/data/medias.ts n’a rien donné.');
  mkdirSync(SORTIE, { recursive: true });

  let totalAvant = 0;
  let totalApres = 0;
  let faits = 0;
  let sautes = 0;
  const lqip = {};

  for (const { slug, source } of medias) {
    const chemin = join(SOURCE, source);
    if (!existsSync(chemin)) {
      console.warn(`  MANQUANT  ${source} — ignoré`);
      continue;
    }
    totalAvant += statSync(chemin).size;

    const meta = await sharp(chemin, { limitInputPixels: false }).metadata();
    const L = meta.width;
    const H = Math.round(meta.height * (1 - ROGNE_BAS));

    for (const l of LARGEURS) {
      if (l > L) continue;
      for (const [ext, opts] of [
        ['avif', { quality: 52, effort: 5 }],
        ['webp', { quality: 74 }],
        ['jpg', { quality: 78, mozjpeg: true, progressive: true }],
      ]) {
        const dest = join(SORTIE, `${slug}-${l}.${ext}`);
        if (!FORCE && existsSync(dest)) {
          totalApres += statSync(dest).size;
          sautes++;
          continue;
        }
        await ouvrir(chemin, L, meta.height)
          .resize(l, null, { withoutEnlargement: true })
          .toFormat(ext === 'jpg' ? 'jpeg' : ext, opts)
          .toFile(dest);
        totalApres += statSync(dest).size;
        faits++;
      }
    }

    // Aperçu flou en base64 : évite le trou blanc pendant le chargement,
    // sans requête réseau supplémentaire.
    const flou = await ouvrir(chemin, L, meta.height)
      .resize(20, null)
      .blur(1.2)
      .webp({ quality: 30 })
      .toBuffer();
    lqip[slug] = {
      lqip: `data:image/webp;base64,${flou.toString('base64')}`,
      w: L,
      h: H,
      ratio: +(L / H).toFixed(4),
    };

    console.log(`  ${slug.padEnd(46)} ${L}×${H}`);
  }

  writeFileSync(join(RACINE, 'src', 'data', 'photos.json'), JSON.stringify(lqip, null, 2) + '\n', 'utf8');

  console.log(
    `\n  ${faits} fichiers générés, ${sautes} déjà à jour.` +
      `\n  source ${octets(totalAvant)}  →  web ${octets(totalApres)}` +
      `  (${((1 - totalApres / totalAvant) * 100).toFixed(1)} % de moins)\n`
  );
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
