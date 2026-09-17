/**
 * Les vignettes de /about/, /boxeurs/, /partenaires/ et /privacy/ de Portet
 * (public/og/pages/<slug>.jpg, 1200 × 630). Les quatre partageaient og.png —
 * la même image sur quatre pages, contre la règle d'Eddy (audit du 13/09).
 * Même gabarit que og_portet_coachs.mjs ; chaque carte sur une photo de la
 * salle distincte, et n'imprime que ce que la page dit déjà.
 * Usage : node og_portet_pages.mjs
 */
import { createRequire } from "node:module";
import { mkdirSync, writeFileSync } from "node:fs";

const DEP = "C:/Users/Mommy Jayce/Desktop/Boxing Center";
const PORTET = `${DEP}/Portet/boxing-center-portet`;
const LABEGE = `${DEP}/Deployment/boxing-center-labege`;
const { Resvg } = createRequire(`${LABEGE}/package.json`)("@resvg/resvg-js");
const sharp = createRequire(`${PORTET}/package.json`)("sharp");

const POLICES = ["C:/Windows/Fonts/arialbd.ttf", `${LABEGE}/src/og/fonts/jetbrains-mono-400.ttf`];
const W = 1200, H = 630;
const x = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

const PAGES = [
  { slug: "about", photo: "img/gym-11.jpg", sur: "LE CLUB · PORTET-SUR-GARONNE", titre: "La salle phare du groupe", puces: ["600 m² de combat", "Depuis 2016"] },
  { slug: "boxeurs", photo: "img/gym-10.jpg", sur: "TEAM TAPIA · PORTET-SUR-GARONNE", titre: "Nos boxeurs", puces: ["De l’école de boxe", "à l’Équipe de France"] },
  { slug: "partenaires", photo: "img/gym-16.jpg", sur: "PARTENAIRES · PORTET-SUR-GARONNE", titre: "Ils font grandir le club", puces: ["KFC", "O2 Portet-sur-Garonne", "Karting 2 Muret"] },
  { slug: "club-de-boxe-portet", photo: "img/gym-01.jpg", sur: "LE CLUB DE BOXE · PORTET-SUR-GARONNE", titre: "600 m² depuis 2016", puces: ["Ring · cage · tatamis", "9 disciplines"] },
  { slug: "privacy", photo: "img/gym-18.jpg", sur: "CONFIDENTIALITÉ · PORTET", titre: "Vos données", puces: ["Pas de compte", "Pas de pisteur"] },
];

function lignes(t, max) {
  const out = [];
  let cur = "";
  for (const mot of t.split(" ")) {
    if ((cur + " " + mot).trim().length > max && cur) { out.push(cur); cur = mot; }
    else cur = (cur + " " + mot).trim();
  }
  if (cur) out.push(cur);
  return out;
}

const logo = await sharp(`${PORTET}/public/logo-1100.png`).resize({ width: 250 }).png().toBuffer();
const logoMeta = await sharp(logo).metadata();
mkdirSync(`${PORTET}/public/og/pages`, { recursive: true });

/* « node og_portet_pages.mjs club-de-boxe-portet » ne refait que cette vignette */
const SEULES = process.argv.slice(2);
for (const p of PAGES.filter((q) => !SEULES.length || SEULES.includes(q.slug))) {
  const fond = await sharp(`${PORTET}/public/${p.photo}`)
    .resize(W, H, { fit: "cover", position: sharp.strategy.attention })
    .modulate({ saturation: 0.85 })
    .jpeg({ quality: 90 })
    .toBuffer();
  const titre = lignes(p.titre, 20);
  const taille = titre.length > 1 ? 64 : 72;
  const yPuces = H - 70;
  const yTitreBas = yPuces - 44;
  const yTitreHaut = yTitreBas - titre.length * taille * 1.08 + taille * 0.82;
  const ySurtitre = yTitreHaut - taille * 0.82 - 26;
  let xPuce = 72;
  const puces = p.puces.map((t) => {
    const larg = Math.round(t.length * 11.2 + 44);
    const g = `<g><rect x="${xPuce}" y="${yPuces - 28}" width="${larg}" height="44" rx="8" fill="rgba(10,16,32,0.55)" stroke="rgba(255,255,255,0.38)" stroke-width="1.5"/>
      <text x="${xPuce + larg / 2}" y="${yPuces + 1}" font-family="JetBrains Mono" font-size="18.5" fill="#f4f6fb" text-anchor="middle">${x(t)}</text></g>`;
    xPuce += larg + 14;
    return g;
  }).join("\n");
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  <defs>
    <linearGradient id="bas" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0" stop-color="#0a1020" stop-opacity="0.96"/><stop offset="0.42" stop-color="#0a1020" stop-opacity="0.72"/>
      <stop offset="0.78" stop-color="#0a1020" stop-opacity="0.12"/><stop offset="1" stop-color="#0a1020" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="gauche" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0a1020" stop-opacity="0.55"/><stop offset="0.6" stop-color="#0a1020" stop-opacity="0"/></linearGradient>
    <linearGradient id="haut" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a1020" stop-opacity="0.55"/><stop offset="0.35" stop-color="#0a1020" stop-opacity="0"/></linearGradient>
  </defs>
  <image href="data:image/jpeg;base64,${fond.toString("base64")}" x="0" y="0" width="${W}" height="${H}"/>
  <rect width="${W}" height="${H}" fill="url(#bas)"/><rect width="${W}" height="${H}" fill="url(#gauche)"/><rect width="${W}" height="${H}" fill="url(#haut)"/>
  <rect x="${W - 72 - 250 - 18}" y="30" width="${250 + 36}" height="${logoMeta.height + 64}" rx="10" fill="#ffffff" fill-opacity="0.94"/>
  <image href="data:image/png;base64,${logo.toString("base64")}" x="${W - 72 - 250}" y="44" width="250" height="${logoMeta.height}"/>
  <text x="${W - 72 - 125}" y="${44 + logoMeta.height + 34}" font-family="Arial" font-weight="bold" font-size="22" letter-spacing="6" fill="#b7791f" text-anchor="middle">PORTET</text>
  <rect x="72" y="${ySurtitre - 15}" width="14" height="14" fill="#aebccf" transform="rotate(45 79 ${ySurtitre - 8})"/>
  <text x="100" y="${ySurtitre}" font-family="JetBrains Mono" font-size="21" letter-spacing="4" fill="#d0d8e8">${x(p.sur)}</text>
  ${titre.map((l, i) => `<text x="72" y="${yTitreHaut + i * taille * 1.08}" font-family="Arial" font-weight="bold" font-size="${taille}" fill="#ffffff">${x(l)}</text>`).join("\n  ")}
  ${puces}
</svg>`;
  const png = new Resvg(svg, { fitTo: { mode: "width", value: W }, font: { fontFiles: POLICES, loadSystemFonts: false, defaultFontFamily: "Arial" } }).render().asPng();
  writeFileSync(`${PORTET}/public/og/pages/${p.slug}.jpg`, await sharp(png).jpeg({ quality: 84, mozjpeg: true }).toBuffer());
  console.log(`[og] pages/${p.slug}.jpg`);
}
