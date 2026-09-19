/* Générique : sur chaque page donnée, chaque carte `.carte-lien` (ou le sélecteur
   passé) doit mener à la page du coach depuis sa photo et son texte, et chaque
   `.role-lien` à une page /activites/. Sondé au doigt (elementFromPoint), cible
   amenée au milieu de l'écran. Usage :
     node cartes_liens.mjs <origine> [bureau|mobile] <chemin> [<chemin> …]   (CAPTURES=dossier) */
import { ouvrir } from "./cdp.mjs";
import { mkdirSync } from "node:fs";
import { join } from "node:path";

const [origine, mode, ...chemins] = process.argv.slice(2);
const MOBILE = mode === "mobile";
const OUT = process.env.CAPTURES || "";
if (OUT) mkdirSync(OUT, { recursive: true });
const p = await ouvrir(MOBILE ? { w: 390, h: 844, mobile: true, dpr: 2 } : { w: 1440, h: 900 });
let fautes = 0;
for (const chemin of chemins) {
  await p.aller(origine + chemin);
  await p.attendre(MOBILE ? 5000 : 3500);
  const r = await p.evalue(`
    const sous = (x, y) => { const el = document.elementFromPoint(x, y); const a = el && el.closest("a"); return a ? a.getAttribute("href") : (el ? "<" + el.tagName.toLowerCase() + "." + (el.className || "") + ">" : "rien"); };
    const viser = async (el) => { el.scrollIntoView({ block: "center" }); await new Promise((r) => setTimeout(r, 300)); const q = el.getClientRects()[0]; if (!q) return "invisible"; return sous(q.left + q.width / 2, q.top + q.height / 2); };
    const out = [];
    for (const c of document.querySelectorAll(".carte-lien")) {
      const tout = c.querySelector(".carte-lien__tout");
      const visuel = c.querySelector("img, .media, .coach__face, .staff__face");
      const o = { nom: tout.textContent.trim(), attendu: tout.getAttribute("href"), photo: visuel ? await viser(visuel) : "(sans photo)", bas: null, liens: [] };
      const dernier = [...c.querySelectorAll("p, span, i, em, blockquote")].filter((e) => !e.closest("a") && !e.querySelector("a") && e.getClientRects().length).pop();
      o.bas = dernier ? await viser(dernier) : "(rien)";
      for (const a of c.querySelectorAll(".role-lien")) o.liens.push([a.textContent, a.getAttribute("href"), await viser(a)]);
      out.push(o);
    }
    const pastilles = [];
    for (const a of document.querySelectorAll(".phero__meta .role-lien")) pastilles.push([a.textContent, a.getAttribute("href"), await viser(a)]);
    return { cartes: out, pastilles };`);
  for (const c of r.cartes) {
    const ko = [];
    if (c.photo !== c.attendu && c.photo !== "(sans photo)") ko.push(`photo → ${c.photo}`);
    if (c.bas !== c.attendu && c.bas !== "(rien)") ko.push(`texte → ${c.bas}`);
    for (const [t, h, vu] of c.liens) if (vu !== h || !h.startsWith("/activites/")) ko.push(`« ${t} » → ${vu} (attendu ${h})`);
    fautes += ko.length;
    console.log(`${chemin}  ${c.nom}  →  ${c.attendu}  | ${c.liens.map((l) => l[0] + "→" + l[1].replace("/activites/", "")).join(", ")}${ko.length ? "   ✗ " + ko.join(" ; ") : "   ✓"}`);
  }
  for (const [t, h, vu] of r.pastilles) { const ok = vu === h; if (!ok) fautes++; console.log(`${chemin}  pastille « ${t} » → ${h}${ok ? "   ✓" : "   ✗ sous le doigt : " + vu}`); }
  if (!r.cartes.length && !r.pastilles.length) { fautes++; console.log(`${chemin}  ✗ aucune carte-lien ni pastille`); }
  if (OUT) await p.capture(join(OUT, `liens-${MOBILE ? "m" : "b"}-${chemin.replace(/\W+/g, "_")}.png`));
}
console.log(`\nerreurs JS : ${JSON.stringify(p.erreurs)}\n${fautes ? fautes + " faute(s)" : "tout mène où il faut"}`);
await p.fermer();
