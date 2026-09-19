/* « Jamais une carte seule sur sa rangée » — mesuré, pas deviné. Pour chaque
   grille donnée, à chaque largeur, on range les enfants par rangée (même top)
   et on signale toute rangée d'une seule carte dans une grille de plusieurs
   colonnes. Usage :
     node cartes_seules.mjs <origine> "<chemin>|<sélecteur>" ["<chemin>|<sélecteur>" …]  (CAPTURES=dossier) */
import { ouvrir } from "./cdp.mjs";
import { mkdirSync } from "node:fs";
import { join } from "node:path";

const [origine, ...cibles] = process.argv.slice(2);
const OUT = process.env.CAPTURES || "";
if (OUT) mkdirSync(OUT, { recursive: true });
const LARGEURS = [[1440, 900], [1024, 768], [820, 1180], [390, 844]];
let fautes = 0;
for (const [w, h] of LARGEURS) {
  const p = await ouvrir({ w, h, mobile: w < 700, dpr: w < 700 ? 2 : 1 });
  for (const cible of cibles) {
    const [chemin, sel] = cible.split("|");
    await p.aller(origine + chemin);
    await p.attendre(w < 700 ? 6000 : 4000);
    const r = await p.evalue(`
      document.documentElement.classList.remove("forge-live");
      const g = document.querySelector(${JSON.stringify(sel)}); if (!g) return { erreur: "grille absente" };
      g.scrollIntoView({ block: "start" });
      g.querySelectorAll("[data-reveal]").forEach((e) => { e.style.opacity = 1; e.style.transform = "none"; });
      await new Promise((r) => setTimeout(r, 900));
      /* même rangée = même haut à 6 px près (pas de seaux : 1001,9 et 1002,1 tombaient dans deux seaux) */
      const lignes = []; let hautRang = -1e9;
      for (const c of g.children) { const q = c.getBoundingClientRect(); if (!q.width) continue;
        if (Math.abs(q.top - hautRang) > 6) { lignes.push([]); hautRang = q.top; }
        lignes[lignes.length - 1].push(Math.round(q.width)); }
      const pleine = g.getBoundingClientRect().width;
      return { lignes: lignes.map((l) => l.length).join("+"), seule: lignes.length > 1 && lignes.some((l) => l.length === 1 && l[0] < pleine * 0.9) };`);
    if (r.seule) fautes++;
    console.log(`${w}px  ${chemin}  ${sel}  →  ${r.erreur || r.lignes}${r.seule ? "   ✗ CARTE SEULE" : ""}`);
    if (OUT) await p.capture(join(OUT, `grille-${w}-${chemin.replace(/\W+/g, "_")}.png`));
  }
  await p.fermer();
}
console.log(fautes ? `\n${fautes} rangée(s) d'une seule carte` : "\naucune carte seule");
