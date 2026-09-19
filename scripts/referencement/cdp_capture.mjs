/**
 * cdp_capture.mjs — une capture RÉELLE d'une page, à la taille voulue, après défilement.
 *   node cdp_capture.mjs <url> <sortie.png> [--w 1440] [--h 900] [--mobile] [--dpr 2]
 *        [--vers "<sélecteur CSS>"] [--y 1200] [--attendre 2500] [--js "<expression à évaluer avant la capture>"]
 * Descend À LA MOLETTE jusqu'à la cible (les révélations au défilement se jouent), puis capture.
 * Affiche aussi le résultat de --js (mesures : getBoundingClientRect, etc.).
 */
import { ouvrir } from "./cdp.mjs";
const a = process.argv.slice(2);
const opt = (n, d) => { const i = a.indexOf("--" + n); return i >= 0 ? a[i + 1] : d; };
const [url, sortie] = a;
const mobile = a.includes("--mobile");
const w = +opt("w", mobile ? 390 : 1440), h = +opt("h", mobile ? 844 : 900);
const p = await ouvrir({ w, h, mobile, dpr: +opt("dpr", mobile ? 2 : 1) });
await p.aller(url);
await p.attendre(+opt("attendre", 2500));
for (let i = 0; i < 40; i++) { if (!(await p.evalue("return document.documentElement.classList.contains('gated')"))) break; await p.attendre(500); }
const vers = opt("vers", ""), yCible = opt("y", "");
if (vers || yCible) {
  for (let i = 0; i < 300; i++) {
    const r = await p.evalue(vers
      ? `const e=document.querySelector(${JSON.stringify(vers)}); if(!e) return {fin:true, absent:true}; const t=e.getBoundingClientRect().top; return {reste: t - innerHeight*0.18, fin: Math.abs(t - innerHeight*0.18) < 60 || scrollY + innerHeight >= document.documentElement.scrollHeight - 4}`
      : `return {reste: ${+yCible} - scrollY, fin: Math.abs(${+yCible} - scrollY) < 60 || scrollY + innerHeight >= document.documentElement.scrollHeight - 4}`);
    if (r.absent) { console.log("cible absente :", vers); break; }
    if (r.fin) break;
    await p.molette(Math.max(-700, Math.min(700, r.reste)), 1, 140);
  }
  await p.attendre(1600);
}
const js = opt("js", "");
if (js) console.log(JSON.stringify(await p.evalue(js)));
await p.capture(sortie);
if (p.erreurs.length) console.log("erreurs JS :", p.erreurs.slice(0, 3));
await p.fermer();
console.log("→", sortie);
