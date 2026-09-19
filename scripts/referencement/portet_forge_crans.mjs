/* Une capture par coach de la forge 3D (un cran de défilement chacun), et la
   mesure de ce que le visuel recouvre : le rectangle du plan projeté à l'écran
   contre la colonne de texte. Usage :
     node portet_forge_crans.mjs [url] [bureau|mobile]   (CAPTURES=dossier) */
import { ouvrir } from "./cdp.mjs";
import { mkdirSync } from "node:fs";
import { join } from "node:path";

const URL_ = process.argv[2] || "http://localhost:4330/coachs/";
const MOBILE = process.argv[3] === "mobile";
const OUT = process.env.CAPTURES || ".";
mkdirSync(OUT, { recursive: true });
const p = await ouvrir(MOBILE ? { w: 390, h: 844, mobile: true, dpr: 2 } : { w: 1440, h: 900 });
await p.aller(URL_);
await p.attendre(MOBILE ? 9000 : 7000);
for (let i = 0; i < 5; i++) {
  const r = await p.evalue(`
    const f = document.querySelector(".forge");
    const haut = f.getBoundingClientRect().top + scrollY, H = f.offsetHeight - innerHeight;
    scrollTo(0, haut + H * (${i} + 0.5) / 5);
    await new Promise((r) => setTimeout(r, 1800));
    const b = (s) => { const e = f.querySelector(s); if (!e) return null; const q = e.getBoundingClientRect(); return [Math.round(q.left), Math.round(q.top), Math.round(q.right), Math.round(q.bottom)]; };
    return { nom: f.querySelector(".forge__name").textContent, carte: b(".forge__card"), tete: b(".forge__head"), ecran: [innerWidth, innerHeight] };`);
  console.log(JSON.stringify(r));
  await p.capture(join(OUT, `cran-${MOBILE ? "mobile" : "bureau"}-${i + 1}.png`));
}
await p.fermer();
