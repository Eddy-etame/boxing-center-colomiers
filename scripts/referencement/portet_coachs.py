# -*- coding: utf-8 -*-
"""
Portet — les pages de coach (/coachs/<slug>/), branchées partout :
  1. le build lance scripts/generate-coachs.mjs, Vite les déclare ;
  2. /coachs/ : chaque carte mène à la page du coach ;
  3. les pages de discipline : le nom du coach mène à sa page ;
  4. plan du site (avec portraits et photos) et llms : une ligne par coach ;
  5. les styles des pages de coach ; et la rangée « Et aussi, au club » des
     pages de discipline tombe juste (auto-fill laissait une case vide).
Fins de ligne laissées telles quelles ; chaque remplacement vérifie son nombre.
"""
import io, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
P = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Portet', 'boxing-center-portet')


def f(*c):
    return os.path.join(P, *c)


def rem(t, avant, apres, nom, n=1):
    for a, b in ((avant, apres), (avant.replace('\n', '\r\n'), apres.replace('\n', '\r\n'))):
        if t.count(a) == n:
            return t.replace(a, b)
    raise AssertionError(f'{nom} : {t.count(avant)} occurrence(s) au lieu de {n} pour {avant[:90]!r}')


def patch(chemin, *ops):
    t = io.open(chemin, encoding='utf-8', newline='').read()
    for op in ops:
        t = op(t)
    io.open(chemin, 'w', encoding='utf-8', newline='').write(t)


patch(f('package.json'), lambda t: rem(t, 'node scripts/generate-disciplines.mjs && ',
                                       'node scripts/generate-disciplines.mjs && node scripts/generate-coachs.mjs && ', 'build'))

patch(f('vite.config.ts'),
      lambda t: rem(t, '''  return p ? `/activites/${p.slug}/` : "";
};
''', '''  return p ? `/activites/${p.slug}/` : "";
};

/* Les pages de coach (/coachs/<slug>/) : écrites par scripts/generate-coachs.mjs.
   Avant le tout premier build la table n'existe pas encore : elle vaut []. */
let COACH_PAGES: { slug: string; nom: string }[] = [];
try { COACH_PAGES = JSON.parse(readFileSync(page("src/coachs-liens.json"), "utf8")); } catch { COACH_PAGES = []; }
const lienC = (nom: string) => { const p = COACH_PAGES.find((x) => x.nom === nom); return p ? `/coachs/${p.slug}/` : ""; };
''', 'vite lienC'),
      lambda t: rem(t, '''        ...Object.fromEntries(DISC_PAGES.map((p) => [`disc-${p.slug}`, page(`activites/${p.slug}/index.html`)])),
''', '''        ...Object.fromEntries(DISC_PAGES.map((p) => [`disc-${p.slug}`, page(`activites/${p.slug}/index.html`)])),
        ...Object.fromEntries(COACH_PAGES.map((p) => [`coach-${p.slug}`, page(`coachs/${p.slug}/index.html`)])),
''', 'vite inputs'),
      lambda t: rem(t, '''            + `<div class="tcard__body"><h3>${e(m.name)}</h3><p class="tcard__role">${e(m.role)}</p><p class="tcard__desc">${e(m.desc)}</p></div></article>`).join(""));''',
                    '''            + `<div class="tcard__body"><h3>${lienC(m.name) ? `<a href="${lienC(m.name)}">${e(m.name)}</a>` : e(m.name)}</h3><p class="tcard__role">${e(m.role)}</p><p class="tcard__desc">${e(m.desc)}</p>`
            /* Chaque carte mène à la page du coach. */
            + (lienC(m.name) ? `<a class="tcard__page" href="${lienC(m.name)}">${/&/.test(m.name) ? "Leur page" : "Sa page"} <span aria-hidden="true">→</span></a>` : "")
            + `</div></article>`).join(""));''', 'vite cartes'))

patch(f('scripts', 'generate-disciplines.mjs'),
      lambda t: rem(t, 'const MANIFESTE = lireJSON("src/img-manifest.json");\n',
                    'const MANIFESTE = lireJSON("src/img-manifest.json");\n/* Le texte des pages de coach : le nom d\'un coach mène à sa page. */\nconst TC = lireJSON("src/coachs.json").pages;\n', 'gen TC'),
      lambda t: rem(t, '<div class="tcard__body"><h3>${e(m.name)}</h3>',
                    '<div class="tcard__body"><h3>${TC[m.name] ? `<a href="/coachs/${TC[m.name].slug}/">${e(m.name)}</a>` : e(m.name)}</h3>', 'gen coach'))

patch(f('scripts', 'sitemap-images.mjs'),
      lambda t: rem(t, '''      ...p.photos.map((ph) => img(ph.src, `${ph.legende} — ${LIEU}`, ph.alt))] })),
''', '''      ...p.photos.map((ph) => img(ph.src, `${ph.legende} — ${LIEU}`, ph.alt))] })),
  // Une page par coach, avec son portrait et ses photos.
  ...Object.values(JSON.parse(readFileSync(join(ROOT, "src", "coachs.json"), "utf8")).pages).map((p) => ({ url: `/coachs/${p.slug}/`, freq: "monthly", prio: "0.7", images: [
      img(p.photo.src, `${p.nom} — ${LIEU}`, p.photo.alt),
      ...(p.photos || []).map((ph) => img(ph.src, `${ph.legende} — ${LIEU}`, ph.alt))] })),
''', 'sitemap'))

patch(f('scripts', 'generate-llms.mjs'),
      lambda t: rem(t, 'const SITE = "https://boxing-center-portet.fr";\n',
                    '/* Une page par coach : son parcours, ses diplômes, ses disciplines, ses questions. */\n'
                    'const PAGES_C = Object.values(JSON.parse(readFileSync(join(ROOT, "src/coachs.json"), "utf8")).pages);\n'
                    'const SITE = "https://boxing-center-portet.fr";\n', 'llms const'),
      lambda t: rem(t, '- Coachs : ${SITE}/coachs/\n',
                    '- Coachs : ${SITE}/coachs/\n${PAGES_C.map((p) => `- ${p.nom}, ${p.poste.charAt(0).toLowerCase()}${p.poste.slice(1)} : ${SITE}/coachs/${p.slug}/`).join("\\n")}\n', 'llms liste'),
      lambda t: rem(t, '\n\n## Publics\n\n',
                    '\n\n## Pages des coachs (une page par coach)\n\n${PAGES_C.map((p) => `### ${p.nom}\\nPage : ${SITE}/coachs/${p.slug}/\\n${p.description}`).join("\\n\\n")}\n\n## Publics\n\n', 'llms section'))

patch(f('src', 'styles', 'main.css'), lambda t: t.rstrip('\r\n') + '''

/* ============================== PAGES DE COACH (/coachs/<slug>/) ============================== */
.cp-tete h1 .tint { white-space: normal; }
.cp-photo img { object-position: 50% 22%; }
.cp-faits { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(210px, 100%), 1fr)); gap: 1px; margin: 0;
  background: var(--line); border: 1px solid var(--line); border-radius: var(--radius-lg); overflow: hidden; }
.cp-fait { display: flex; flex-direction: column-reverse; justify-content: flex-end; gap: .55rem; padding: clamp(1.4rem, 2.6vw, 2.2rem); background: var(--bg-1); }
.cp-fait dd { margin: 0; font-family: var(--font-cond); font-weight: 600; font-size: clamp(1.9rem, 3.4vw, 3rem); line-height: 1; text-transform: uppercase; color: var(--fg); }
.cp-fait dt { font-family: var(--font-mono); font-size: .72rem; letter-spacing: .14em; text-transform: uppercase; color: var(--accent); }
.cp-texte { display: grid; grid-template-columns: minmax(0, .85fr) minmax(0, 1.15fr); gap: clamp(1.4rem, 4vw, 4rem); align-items: start; }
.cp-texte .sec-head { margin-bottom: 0; }
@media (max-width: 900px) { .cp-texte { grid-template-columns: minmax(0, 1fr); } }
.cp-paras { display: grid; gap: 1rem; max-width: 64ch; color: var(--fg-soft); font-size: 1.05rem; line-height: 1.7; }
.cp-devise { margin: 2rem 0 0; padding-left: 1.2rem; border-left: 2px solid var(--accent); max-width: 36ch; }
.cp-devise p { font-family: var(--font-cond); font-weight: 600; font-size: clamp(1.5rem, 2.6vw, 2.2rem); line-height: 1.12; text-transform: uppercase; color: var(--fg); }
.cp-devise cite { display: block; margin-top: .6rem; font-family: var(--font-mono); font-size: .72rem; letter-spacing: .14em; text-transform: uppercase; font-style: normal; color: var(--accent); }
/* Les grilles des pages de coach tombent juste : jamais une carte seule sur sa rangée. */
.cp-cartes { display: grid; gap: 1px; margin-top: 2.4rem; }
.cp-cartes--1 { grid-template-columns: minmax(0, 520px); }
.cp-cartes--2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.cp-cartes--3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.cp-cartes--4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
@media (max-width: 1099px) {
  .cp-cartes--3, .cp-cartes--4 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .cp-cartes--3 > :first-child { grid-column: 1 / -1; }
}
@media (max-width: 619px) {
  .cp-cartes--2, .cp-cartes--3, .cp-cartes--4 { grid-template-columns: minmax(0, 1fr); }
  .cp-cartes--3 > :first-child { grid-column: auto; }
}
.cp-equipe { gap: clamp(1rem, 2.5vw, 1.6rem); }
.cp-coach { color: inherit; text-decoration: none; display: flex; flex-direction: column; }
.cp-coach img { aspect-ratio: 4 / 3; object-fit: cover; object-position: 50% 22%; }
.cp-coach .tcard__body { display: flex; flex-direction: column; flex: 1; }
.cp-coach .disc__go { margin-top: auto; padding-top: .8rem; }
.cp-boxeurs { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: clamp(1rem, 2.5vw, 1.6rem); margin-top: 2.4rem; }
@media (max-width: 1099px) { .cp-boxeurs { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 619px) { .cp-boxeurs { grid-template-columns: minmax(0, 1fr); } }
.cp-boxeur { display: flex; flex-direction: column; gap: .35rem; color: inherit; text-decoration: none; }
.cp-boxeur img { display: block; width: 100%; height: auto; aspect-ratio: 4 / 5; object-fit: cover; object-position: 50% 25%;
  border-radius: var(--radius-lg); border: 1px solid var(--line); margin-bottom: .5rem; }
.cp-boxeur__nom { font-family: var(--font-cond); font-weight: 600; font-size: 1.35rem; text-transform: uppercase; }
.cp-boxeur__fait { font-family: var(--font-mono); font-size: .74rem; letter-spacing: .06em; color: var(--muted); }
.cp-boxeur:hover .cp-boxeur__nom { color: var(--accent); }
.cp-galerie--seule { max-width: 560px; }
/* Sur /coachs/, chaque carte mène à la page du coach. */
.tcard__body h3 a { color: inherit; text-decoration: none; }
.tcard__body h3 a:hover { color: var(--accent); }
.tcard__page { display: inline-flex; gap: .4em; margin-top: .7rem; font-family: var(--font-mono); font-size: .72rem;
  letter-spacing: .12em; text-transform: uppercase; color: var(--accent); text-decoration: none; }
.tcard__page:hover { text-decoration: underline; text-underline-offset: .3em; }
/* « Et aussi, au club » : trois cartes, trois colonnes. En auto-fill, une
   quatrième colonne restait vide à côté d'elles sur un grand écran. */
.dp-voisines { grid-template-columns: repeat(3, minmax(0, 1fr)); }
@media (max-width: 900px) { .dp-voisines { grid-template-columns: minmax(0, 1fr); } }
''')
print('patch coachs Portet appliqué')
