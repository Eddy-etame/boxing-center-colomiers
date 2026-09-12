/**
 * Les favicons d'un site : une pastille ronde-sûre (Google la découpe en
 * cercle), la teinte sombre du site en fond, un anneau à la couleur du site
 * — les cordes du ring —, et le code de la ville en blanc.
 *
 * Usage (depuis le dépôt du site, pour ses node_modules) :
 *   node favicons.mjs <CODE> <sombre> <accent> <clair> "<nom>" "<nom court>"
 * Écrit dans public/ : favicon.ico (16, 32, 48), favicon-{16,32,48,96,192,512}.png,
 * apple-touch-icon.png (180), site.webmanifest.
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { Resvg } from '@resvg/resvg-js';
import sharp from 'sharp';

const [code, sombre, accent, clair, nom, nomCourt] = process.argv.slice(2);
if (!code || !sombre || !accent || !clair) {
  console.error('usage: node favicons.mjs CODE sombre accent clair "nom" "nom court"');
  process.exit(1);
}
const police = resolve(process.cwd(), 'src/og/fonts/bricolage-grotesque-700.ttf');
readFileSync(police);

const taille = code.length > 1 ? 206 : 280;
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <rect width="512" height="512" fill="${sombre}"/>
  <circle cx="256" cy="256" r="214" fill="none" stroke="${accent}" stroke-width="30"/>
  <text x="256" y="256" dy="${Math.round(taille * 0.35)}" text-anchor="middle" font-family="Bricolage Grotesque" font-weight="700"
        font-size="${taille}" letter-spacing="-6" fill="${clair}">${code}</text>
</svg>`;

const png512 = new Resvg(svg, {
  fitTo: { mode: 'width', value: 512 },
  font: { fontFiles: [police], loadSystemFonts: false, defaultFontFamily: 'Bricolage Grotesque' },
}).render().asPng();

const pub = resolve(process.cwd(), 'public');
const tailles = [16, 32, 48, 96, 192, 512];
const pngs = {};
for (const t of tailles) {
  pngs[t] = await sharp(png512).resize(t, t, { kernel: 'lanczos3' }).png({ compressionLevel: 9 }).toBuffer();
  writeFileSync(resolve(pub, `favicon-${t}.png`), pngs[t]);
}
writeFileSync(resolve(pub, 'apple-touch-icon.png'), await sharp(png512).resize(180, 180).png().toBuffer());

/* favicon.ico : des PNG empilés dans un conteneur ICO (16, 32, 48). */
const entrees = [16, 32, 48];
const tete = Buffer.alloc(6 + 16 * entrees.length);
tete.writeUInt16LE(0, 0); tete.writeUInt16LE(1, 2); tete.writeUInt16LE(entrees.length, 4);
let decalage = tete.length;
entrees.forEach((t, i) => {
  const o = 6 + i * 16;
  tete.writeUInt8(t, o); tete.writeUInt8(t, o + 1); tete.writeUInt8(0, o + 2); tete.writeUInt8(0, o + 3);
  tete.writeUInt16LE(1, o + 4); tete.writeUInt16LE(32, o + 6);
  tete.writeUInt32LE(pngs[t].length, o + 8); tete.writeUInt32LE(decalage, o + 12);
  decalage += pngs[t].length;
});
writeFileSync(resolve(pub, 'favicon.ico'), Buffer.concat([tete, ...entrees.map((t) => pngs[t])]));

writeFileSync(resolve(pub, 'site.webmanifest'), JSON.stringify({
  name: nom,
  short_name: nomCourt,
  icons: [
    { src: '/favicon-192.png', sizes: '192x192', type: 'image/png' },
    { src: '/favicon-512.png', sizes: '512x512', type: 'image/png' },
  ],
  theme_color: sombre,
  background_color: sombre,
  display: 'browser',
}, null, 2) + '\n');

console.log(`favicons ${code} : ico, 6 png, apple-touch, manifest`);
