/**
 * Portet — les sections VIDES des captures d'Eddy (19/09) : « Le ring est à tout
 * le monde », « Sans détour », les avis, un écran entièrement noir. Diagnostic EN
 * LIGNE, dans un Chrome réellement rendu : la hauteur de la page au fil du temps
 * (une page qui change de hauteur APRÈS la mesure de ScrollTrigger déclenche ses
 * révélations au mauvais endroit), puis une descente à la molette où l'on relève,
 * à chaque cran, ce qui est À L'ÉCRAN mais encore invisible.
 * Usage : node portet_diag_revelations.mjs [url] [bureau|mobile]
 */
import { ouvrir } from "./cdp.mjs";
const URL = process.argv[2] || "https://boxing-center-portet.fr/";
const mode = process.argv[3] || "bureau";
const DOSSIER = process.env.CAPTURES || ".";
const p = await ouvrir(mode === "mobile" ? { w: 390, h: 844, mobile: true, dpr: 2 } : { w: 1440, h: 900 });
await p.aller(URL);
const hauteurs = [];
for (let t = 0; t < 12; t++) {
  hauteurs.push(await p.evalue("return [Math.round(performance.now()/100)/10, document.documentElement.scrollHeight, document.documentElement.className.replace(/\\s+/g,' ').slice(0,60)]"));
  await p.attendre(1000);
}
console.log("HAUTEUR DE PAGE (s, px, classes html) :"); hauteurs.forEach((x) => console.log("  ", JSON.stringify(x)));

const RELEVE = `
  const vus = [...document.querySelectorAll('[data-reveal]')].filter(e => { const r = e.getBoundingClientRect(); return r.height > 0 && r.top < innerHeight * 0.7 && r.bottom > innerHeight * 0.1 && +getComputedStyle(e).opacity < 0.05; });
  const sec = [...document.querySelectorAll('main section')].find(s => { const r = s.getBoundingClientRect(); return r.top <= innerHeight * 0.5 && r.bottom >= innerHeight * 0.5; });
  return { y: Math.round(scrollY), h: document.documentElement.scrollHeight, section: sec ? (sec.className + ' ' + (sec.querySelector('h2')?.innerText || '').replace(/\\n/g,' ')).slice(0, 70) : '', invisibles: vus.length, ex: vus.slice(0, 3).map(e => (e.className || e.tagName).toString().slice(0, 30)) };`;
const fautes = [];
let dernier = -1, captures = 0;
for (let i = 0; i < 400; i++) {
  await p.molette(mode === "mobile" ? 500 : 400, 1, 260);
  const r = await p.evalue(RELEVE);
  if (r.invisibles) {
    fautes.push(r);
    if (captures < 4 && r.y - dernier > 1500) { await p.attendre(900); const r2 = await p.evalue(RELEVE); if (r2.invisibles) { await p.capture(`${DOSSIER}/portet-vide-${mode}-${++captures}.png`); dernier = r.y; console.log("  capture", captures, JSON.stringify(r2)); } }
  }
  if (r.y + (mode === "mobile" ? 844 : 900) >= r.h - 4) break;
}
const parSection = {};
fautes.forEach((f) => { parSection[f.section] = (parSection[f.section] || 0) + 1; });
console.log("CRANS OÙ DU CONTENU À L'ÉCRAN EST INVISIBLE, par section :"); console.log(parSection);
console.log("exemples :", JSON.stringify(fautes.slice(0, 6)));
console.log("erreurs JS :", p.erreurs.slice(0, 5));
await p.fermer();
