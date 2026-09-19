/* Les cartes coach de Portet, vérifiées dans un vrai navigateur : ce qu'il y a
   sous le doigt au milieu de la photo, où mène chaque discipline, et une
   capture par sorte de carte. Usage :
     node portet_cartes_coachs.mjs [origine] [bureau|mobile]   (CAPTURES=dossier) */
import { ouvrir } from "./cdp.mjs";
import { mkdirSync } from "node:fs";
import { join } from "node:path";

const ORIGINE = process.argv[2] || "http://localhost:4330";
const MOBILE = process.argv[3] === "mobile";
const OUT = process.env.CAPTURES || ".";
mkdirSync(OUT, { recursive: true });
const p = await ouvrir(MOBILE ? { w: 390, h: 844, mobile: true, dpr: 2 } : { w: 1440, h: 900 });
const suff = MOBILE ? "mobile" : "bureau";

/* 1. Les cartes HTML : fiche discipline, page coach, page club, repli de /coachs/. */
const PAGES = [
  ["/activites/mma/", ".dp-coachs"],
  ["/coachs/samuel-pinto/", ".cp-equipe"],
  ["/club-de-boxe-portet/", ".cp-equipe"],
];
for (const [chemin, zone] of PAGES) {
  await p.aller(ORIGINE + chemin);
  await p.attendre(2500);
  const r = await p.evalue(`
    const z = document.querySelector(${JSON.stringify(zone)});
    if (!z) return { erreur: "zone absente" };
    z.scrollIntoView({ block: "center" });
    await new Promise((r) => setTimeout(r, 1200));
    /* Chaque cible est amenée au milieu de l'écran avant d'être sondée : sur
       téléphone les cartes s'empilent, un point hors écran ne répond rien. */
    const sous = (x, y) => { const el = document.elementFromPoint(x, y); const a = el && el.closest("a"); return a ? a.getAttribute("href") : (el ? el.tagName : "rien"); };
    const viser = async (el) => {
      el.scrollIntoView({ block: "center" }); await new Promise((r) => setTimeout(r, 260));
      const q = el.getClientRects()[0]; return sous(q.left + q.width / 2, q.top + q.height / 2);
    };
    const out = [];
    for (const c of z.querySelectorAll(".tcard")) {
      const disciplines = [];
      for (const a of c.querySelectorAll(".role-lien")) disciplines.push(a.textContent + " → " + await viser(a));
      out.push({
        nom: c.querySelector("h3").textContent.trim(),
        photo: await viser(c.querySelector("img")),
        texte: await viser(c.querySelector(".tcard__desc, .disc__go") || c.querySelector(".tcard__body")),
        disciplines,
        role: c.querySelector(".tcard__role").textContent,
      });
    }
    z.scrollIntoView({ block: "center" });
    await new Promise((r) => setTimeout(r, 400));
    return out;`);
  console.log("\n" + chemin, JSON.stringify(r, null, 1));
  await p.capture(join(OUT, `cartes-${chemin.replace(/\W+/g, "_")}${suff}.png`));
}

/* 2. La forge 3D de /coachs/ et de l'accueil : un cran par coach. */
for (const chemin of ["/coachs/", "/"]) {
  await p.aller(ORIGINE + chemin);
  await p.attendre(MOBILE ? 9000 : 7000);
  const vus = await p.evalue(`
    const f = document.querySelector(".forge"); if (!f) return { erreur: "pas de forge" };
    const haut = f.getBoundingClientRect().top + scrollY, H = f.offsetHeight - innerHeight, out = [];
    for (let i = 0; i < 5; i++) {
      scrollTo(0, haut + H * (i + 0.5) / 5);
      await new Promise((r) => setTimeout(r, 1400));
      const sous = (x, y) => { const el = document.elementFromPoint(x, y); const a = el && el.closest("a"); return a ? a.getAttribute("href") : (el ? el.className || el.tagName : "rien"); };
      const role = f.querySelector(".forge__role");
      out.push({
        nom: f.querySelector(".forge__name").textContent,
        lienNom: (f.querySelector(".forge__name a") || {}).href || "",
        milieuPhoto: sous(innerWidth * ${MOBILE ? 0.5 : 0.68}, innerHeight * 0.45),
        coinVide: sous(innerWidth * 0.92, innerHeight * 0.9),
        disciplines: [...role.querySelectorAll("a")].map((a) => { const q = a.getClientRects()[0]; return a.textContent + " → " + sous(q.left + q.width / 2, q.top + q.height / 2); }),
        role: role.textContent,
        live: document.documentElement.classList.contains("forge-live"),
      });
    }
    return out;`);
  console.log("\nforge " + chemin, JSON.stringify(vus, null, 1));
  await p.capture(join(OUT, `forge-${chemin === "/" ? "accueil" : "coachs"}-${suff}.png`));
}

/* 3. Le repli HTML de /coachs/ (ce que voit un visiteur sans WebGL, et les robots). */
await p.aller(ORIGINE + "/coachs/");
await p.attendre(5000);
await p.evalue(`
  document.documentElement.classList.remove("forge-live");
  const s = document.getElementById("team-cards").closest("section"); s.scrollIntoView({ block: "start" });
  s.querySelectorAll("[data-reveal]").forEach((e) => { e.style.opacity = 1; e.style.transform = "none"; });
  await new Promise((r) => setTimeout(r, 900)); return 1;`);
await p.capture(join(OUT, `repli-coachs-${suff}.png`));
console.log("\nerreurs JS :", JSON.stringify(p.erreurs));
await p.fermer();
