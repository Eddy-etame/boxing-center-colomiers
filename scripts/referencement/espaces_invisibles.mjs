/* Avant de corriger des « mots collés » dans le code, on prouve dans un vrai
   navigateur que la correction ne change RIEN à l'écran.

   Pour chaque page : on fige les animations, on capture la page entière, puis
   on insère un nœud texte " " entre chaque paire d'éléments frères qui se
   touchent sans blanc à l'intérieur des conteneurs ciblés (exactement ce que
   fera le correctif React), on recapture, et on compare pixel à pixel. On
   relève aussi le texte que lit un moteur avant/après sur les mêmes conteneurs.

   Usage : node espaces_invisibles.mjs <url> [bureau|mobile]  (CAPTURES=dossier) */
import { ouvrir } from "./cdp.mjs";
import { mkdirSync } from "node:fs";
import { join } from "node:path";

const url = process.argv[2];
const mobile = process.argv[3] === "mobile";
const OUT = process.env.CAPTURES || ".";
mkdirSync(OUT, { recursive: true });
const nom = url.replace(/^https?:\/\/[^/]+/, "").replace(/\W+/g, "_") || "_accueil";
const suff = mobile ? "mobile" : "bureau";

const CIBLES = [
  ".brand > span", ".launch-strip", ".desktop-nav", ".footer-routes", ".footer-route",
  ".footer-route > span:not(.footer-route-index)", ".footer-grid nav", ".footer-queries",
  ".footer-bottom", ".footer-bottom nav", ".product-image", ".product-meta", ".price-row",
  ".catalog-count", ".catalog-pagination", ".detail-assurances", ".subfamily-links",
  ".product-facts > div", ".equipment-rows", ".equipment-list", ".practice-index",
];

const p = await ouvrir(mobile ? { w: 390, h: 844, mobile: true, dpr: 2 } : { w: 1440, h: 900 });
await p.aller(url);
await p.attendre(5000);
/* Le bandeau de consentement couvre et floute la page : une preuve prise
   dessous ne prouve rien (29/09, première série à refaire). On le ferme par
   le choix le plus respectueux, « Continuer sans mesure », et on vérifie. */
const bandeau = await p.evalue(`
  const b = [...document.querySelectorAll('button')].find(x => /continuer sans mesure/i.test(x.textContent));
  if (b) b.click();
  await new Promise(r => setTimeout(r, 1200));
  const reste = [...document.querySelectorAll('button')].some(x => /continuer sans mesure/i.test(x.textContent) && x.offsetParent);
  return { trouve: !!b, resteVisible: reste };`);
if (bandeau.resteVisible) { console.error("BANDEAU TOUJOURS VISIBLE — preuve invalide"); process.exit(2); }
await p.evalue(`
  const s = document.createElement('style');
  s.textContent = '*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}';
  document.head.appendChild(s);
  document.querySelectorAll('video').forEach(v => { try { v.pause(); v.currentTime = 0; } catch {} });
  window.scrollTo(0, 0);
  await new Promise(r => setTimeout(r, 800));
  return 1;`);

const lire = `
  const CIBLES = ${JSON.stringify(CIBLES)};
  const out = {};
  for (const sel of CIBLES) {
    const els = [...document.querySelectorAll(sel)];
    if (!els.length) continue;
    out[sel] = { n: els.length, display: getComputedStyle(els[0]).display, texte: els[0].textContent.replace(/\\s+/g, ' ').trim().slice(0, 90) };
  }
  return out;`;

const hauteur = await p.evalue(`return document.documentElement.scrollHeight;`);
const avant = await p.evalue(lire);
await p.evalue(`window.scrollTo(0,0); return 1;`);
const f1 = join(OUT, `${nom}-${suff}-avant.png`);
await p.captureEntiere?.(f1) ?? await p.capture(f1);
/* TÉMOIN : la même page, recapturée sans rien changer. Ce qui diffère entre
   f1 et f0 est le bruit de rendu (images qui finissent de se décoder,
   textures) ; seul ce qui dépasse ce bruit peut venir des blancs. */
await p.attendre(1500);
const f0 = join(OUT, `${nom}-${suff}-temoin.png`);
await p.captureEntiere?.(f0) ?? await p.capture(f0);

const inseres = await p.evalue(`
  const CIBLES = ${JSON.stringify(CIBLES)};
  let n = 0;
  const vu = new Set();
  for (const sel of CIBLES) for (const el of document.querySelectorAll(sel)) {
    if (vu.has(el)) continue; vu.add(el);
    const kids = [...el.childNodes];
    for (let i = 0; i < kids.length - 1; i++) {
      const a = kids[i], b = kids[i + 1];
      const finA = (a.textContent || '').slice(-1), debB = (b.textContent || '').slice(0, 1);
      if (!finA || !debB || /\\s/.test(finA) || /\\s/.test(debB)) continue;
      el.insertBefore(document.createTextNode(' '), b); n++;
    }
  }
  await new Promise(r => setTimeout(r, 500));
  return n;`);
const apres = await p.evalue(lire);
await p.evalue(`window.scrollTo(0,0); return 1;`);
const f2 = join(OUT, `${nom}-${suff}-apres.png`);
await p.captureEntiere?.(f2) ?? await p.capture(f2);
const hauteur2 = await p.evalue(`return document.documentElement.scrollHeight;`);

console.log(JSON.stringify({ url, mode: suff, bandeau, espacesInseres: inseres, hauteurAvant: hauteur, hauteurApres: hauteur2, avant, apres, f0, f1, f2 }));
await p.fermer();
