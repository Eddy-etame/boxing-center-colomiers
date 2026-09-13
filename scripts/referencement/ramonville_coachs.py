# -*- coding: utf-8 -*-
"""
Ramonville — les pages de coach (/coachs/<slug>/), branchées partout :
  1. le build lance scripts/generer-coachs.mjs ;
  2. l'accueil : Jérôme, coach principal, prend toute la rangée, portrait
     entier et son texte ; les quatre autres tombent juste (Eddy, 13/09 :
     jamais un coach seul en bas) ; chaque carte mène à la page du coach ;
  3. /coachs/ : chaque fiche mène à sa page (version hydratée ET version
     cuite) ; la version cuite ne publie plus les créneaux nominatifs (la
     version hydratée ne les montre pas : planning des coachs interne) ;
     JSON-LD : chaque Person porte l'URL de sa page, et Valentin Guth est
     3e français chez les super-coqs (sa fiche boxingcenter.fr), plus 2e ;
  4. les pages de discipline : le nom du coach mène à sa page ;
  5. sitemap et llms : une ligne par page de coach ;
  6. les versions des fichiers touchés montent.
Chaque remplacement vérifie son nombre d'occurrences.
"""
import glob, io, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
R = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment', 'bc-ramonville')


def lire(chemin):
    t = io.open(chemin, encoding='utf-8', newline='').read()
    return t.replace('\r\n', '\n'), '\r\n' in t


def ecrire(chemin, t, crlf):
    io.open(chemin, 'w', encoding='utf-8', newline='').write(t.replace('\n', '\r\n') if crlf else t)


def rem(t, avant, apres, nom, n=1):
    k = t.count(avant)
    assert k == n, f'{nom} : {k} occurrence(s) au lieu de {n} pour {avant[:90]!r}'
    return t.replace(avant, apres)


def sub(t, motif, apres, nom, n=1):
    t2, k = re.subn(motif, apres, t, flags=re.M)
    assert k == n, f'{nom} : {k} remplacement(s) au lieu de {n} pour {motif[:90]!r}'
    return t2


def f(*c):
    return os.path.join(R, *c)


def patch(chemin, *ops):
    t, crlf = lire(chemin)
    for op in ops:
        t = op(t)
    ecrire(chemin, t, crlf)


# 1. le build
patch(f('package.json'), lambda t: rem(t, 'node scripts/generer-disciplines.mjs && astro build',
                                       'node scripts/generer-disciplines.mjs && node scripts/generer-coachs.mjs && astro build', 'build'))

# 2. l'accueil
patch(f('public', 'assets', 'js', 'home.js'),
      lambda t: sub(t, r'^(import \{ STATS, DISCIPLINES, COACHES, SALLE \} from "\./data\.js\?v=\d+";\n)',
                    r'\1import { lienCoach } from "./coachs-liens.js?v=1";\n', 'home import'),
      lambda t: rem(t, 'data-sizes="(max-width: 700px) 160px, 240px"',
                    'data-sizes="${c.pillar ? "(max-width: 760px) 92vw, 460px" : "(max-width: 700px) 160px, 240px"}"', 'home sizes'),
      lambda t: rem(t, '''    return `<a class="staff__card ${c.pillar ? "is-pillar" : ""}" href="/coachs/">
      ${face}
      <div class="staff__meta">
        <b>${c.name}</b>
        <span class="mono">${c.role}</span>
        <i>${c.tag}</i>
        ${c.devise ? `<em class="staff__devise">${c.devise}</em>` : ""}
      </div>
    </a>`;''', '''    /* Chaque carte mène à la page du coach. Le coach principal prend toute
       la rangée et porte son texte ; les autres restent des vignettes. */
    return `<a class="staff__card ${c.pillar ? "is-pillar" : ""}" href="${lienCoach(c.name) || "/coachs/"}">
      ${face}
      <div class="staff__meta">
        <b>${c.name}</b>
        <span class="mono">${c.role}</span>
        <i>${c.tag}</i>
        ${c.pillar && c.note ? `<p class="staff__note">${c.note}</p>` : ""}
        ${c.devise ? `<em class="staff__devise">${c.devise}</em>` : ""}
        <span class="staff__go">${c.pillar ? `Le parcours de ${c.name}` : "Voir sa page"} <span aria-hidden="true">→</span></span>
      </div>
    </a>`;''', 'home carte'))
patch(f('src', 'pages', 'index.astro'),
      lambda t: rem(t, '        <div class="staff" id="staff" data-reveal-group></div>\n',
                    '        <div class="staff" id="staff" data-reveal-group></div>\n'
                    '        <p class="staff__plus" data-reveal><a href="/coachs/">Toute l’équipe, coach par coach <span aria-hidden="true">→</span></a></p>\n', 'accueil lien'))
patch(f('public', 'assets', 'css', 'home.css'),
      lambda t: sub(t, r'^(\.staff__meta i \{[^\n]*\}\n)', r'''\1
/* LE COACH PRINCIPAL, À L'HORIZONTALE — Eddy, 13/09 : jamais un coach seul en
   bas de la bande. Cinq cartes dans quatre colonnes laissaient la cinquième
   seule sur sa rangée. Jérôme prend toute la rangée, portrait entier et son
   texte ; les quatre autres tombent juste, en 4 colonnes comme en 2. */
.staff__card.is-pillar { grid-column: 1 / -1; }
@media (min-width: 760px) {
  .staff__card.is-pillar { display: grid; grid-template-columns: minmax(280px, 40%) minmax(0, 1fr); gap: clamp(1.2rem, 3vw, 2.8rem); align-items: center; padding: .9rem; }
  .staff__card.is-pillar .staff__meta { gap: .55rem; padding: .6rem clamp(.4rem, 2vw, 1.6rem) .6rem 0; }
  .staff__card.is-pillar .staff__meta b { font-size: clamp(2.2rem, 1.2rem + 3vw, 3.8rem); line-height: 1; }
  .staff__card.is-pillar .staff__meta .mono { font-size: .8rem; }
}
.staff__note { color: var(--ink-soft); font-size: 1rem; line-height: 1.6; max-width: 56ch; margin: .5rem 0 0; }
.staff__go { margin-top: auto; padding-top: .5rem; font: 600 .6rem/1 var(--f-mono); letter-spacing: .12em; text-transform: uppercase; color: var(--accent); }
.staff__card.is-pillar .staff__go { font-size: .72rem; margin-top: .4rem; }
.staff__plus { margin-top: 1.4rem; font: 600 .72rem/1 var(--f-mono); letter-spacing: .12em; text-transform: uppercase; }
.staff__plus a { color: var(--accent); text-decoration: none; }
.staff__plus a:hover { text-decoration: underline; text-underline-offset: .3em; }
''', 'home.css'))

# 3. /coachs/
patch(f('src', 'pages', 'coachs', 'index.astro'),
      lambda t: sub(t, r'^(    import \{ COACHES \} from "/assets/js/data\.js\?v=\d+";\n)',
                    r'\1    import { lienCoach } from "/assets/js/coachs-liens.js?v=1";\n', 'roster import'),
      lambda t: rem(t, '            <h3>${c.name}</h3>\n',
                    '            <h3>${lienCoach(c.name) ? `<a href="${lienCoach(c.name)}">${c.name}</a>` : c.name}</h3>\n', 'roster h3'),
      lambda t: rem(t, '            ${c.devise ? `<blockquote class="coach__devise">${c.devise}</blockquote>` : ""}\n',
                    '            ${c.devise ? `<blockquote class="coach__devise">${c.devise}</blockquote>` : ""}\n'
                    '            ${lienCoach(c.name) ? `<a class="coach__page" href="${lienCoach(c.name)}">La page de ${c.name} <span aria-hidden="true">→</span></a>` : ""}\n', 'roster lien'),
      lambda t: sub(t, r'^(\s*)("@id": "https://mmatoulouse\.com/coachs/#([a-z-]+)",\n)',
                    r'\1\2\1"url": "https://mmatoulouse.com/coachs/\3/",\n', 'jsonld url', 5),
      lambda t: rem(t, '2ᵉ français chez les super-coqs', '3ᵉ français chez les super-coqs', 'guth rang'))
patch(f('public', 'assets', 'css', 'coachs.css'), lambda t: t.rstrip('\n') + '''

/* Chaque fiche mène à la page du coach (/coachs/<slug>/). */
.coach h3 a { color: inherit; text-decoration: none; }
.coach h3 a:hover { color: var(--accent); }
.coach__page { align-self: flex-start; display: inline-block; margin-top: .9rem; font: 600 .7rem/1 var(--f-mono); letter-spacing: .12em; text-transform: uppercase; color: var(--accent); text-decoration: none; }
.coach__page:hover { text-decoration: underline; text-underline-offset: .3em; }
''')
patch(f('scripts', 'cuire-pages.mjs'), lambda t: rem(t, '''const coachroster = COACHES.map((c) => {
  const slots = SCHEDULE.filter((s) => s.coach === c.name);
  return `<article><h3>${e(c.name)}</h3><p><b>${e(c.role || "")}</b>${
    c.tag ? ` · ${e(c.tag)}` : ""
  }</p>${c.note ? `<p>${e(c.note)}</p>` : ""}${ul(
    slots.map((s) => `${s.day} ${s.start} — ${s.cours}`)
  )}</article>`;
}).join("");''', '''/* Chaque fiche mène à la page du coach. Pas de créneaux nominatifs : le
   planning des coachs reste interne ; la version hydratée de /coachs/ ne
   les montre pas, la version cuite ne les publie plus non plus. */
const TC = JSON.parse(await readFile(join(ROOT, "src", "coachs-pages.json"), "utf8")).pages;
const coachroster = COACHES.map((c) => {
  const page = TC[c.name] ? `/coachs/${TC[c.name].slug}/` : "";
  return `<article><h3>${page ? `<a href="${page}">${e(c.name)}</a>` : e(c.name)}</h3><p><b>${e(c.role || "")}</b>${
    c.tag ? ` · ${e(c.tag)}` : ""
  }</p>${c.note ? `<p>${e(c.note)}</p>` : ""}${page ? `<p><a href="${page}">La page de ${e(c.name)}</a></p>` : ""}</article>`;
}).join("");''', 'cuire roster'))

# 4. les pages de discipline
patch(f('scripts', 'generer-disciplines.mjs'),
      lambda t: rem(t, 'const T = textes();\n', 'const T = textes();\nconst TC = JSON.parse(readFileSync(join(ROOT, "src", "coachs-pages.json"), "utf8")).pages;\n', 'gen TC'),
      lambda t: rem(t, '<div><h3>${e(c.name)}</h3>', '<div><h3>${TC[c.name] ? `<a href="/coachs/${TC[c.name].slug}/">${e(c.name)}</a>` : e(c.name)}</h3>', 'gen coach'))

# 5. sitemap et llms
patch(f('scripts', 'sitemap.mjs'),
      lambda t: rem(t, '\nconst PAGES = [\n', '''
/* Une page par coach, avec son portrait officiel. */
const TCOACHS = JSON.parse(await readFile(join(ROOT, "src", "coachs-pages.json"), "utf8")).pages;
const IMG_COACH = { jerome: I.jerome, sonia: I.sonia, hicham: I.hicham, farouk: I.farouk, "valentin-guth": I.valentin };
const LIGNES_COACHS = Object.values(TCOACHS).map((t) => ({
  chemin: `coachs/${t.slug}/`, priorite: "0.6", freq: "monthly", imgs: IMG_COACH[t.slug] ? [IMG_COACH[t.slug]] : [],
}));

const PAGES = [
''', 'sitemap const'),
      lambda t: sub(t, r'^(  \{ chemin: "coachs/", [^\n]*\n)', r'\1  ...LIGNES_COACHS,\n', 'sitemap ligne'))
patch(f('scripts', 'cuire-llms.mjs'),
      lambda t: rem(t, '\nconst SECTIONS = [\n', '''
/* Une page par coach : son parcours, ses diplômes, ses disciplines, ses questions. */
const TCOACHS = JSON.parse(await readFile(join(ROOT, "src", "coachs-pages.json"), "utf8")).pages;
function sectionPagesCoachs() {
  return COACHES.filter((c) => TCOACHS[c.name])
    .map((c) => `- ${c.name} — ${TCOACHS[c.name].poste} : https://mmatoulouse.com/coachs/${TCOACHS[c.name].slug}/`).join("\\n");
}

const SECTIONS = [
''', 'llms fonction'),
      lambda t: rem(t, '  ["pages-disciplines", sectionPagesDisciplines],\n',
                    '  ["pages-disciplines", sectionPagesDisciplines],\n  ["pages-coachs", sectionPagesCoachs],\n', 'llms section'))
BLOC = '''

## Pages des coachs

Une page par coach : son parcours, ses diplômes, ses disciplines, ses questions fréquentes.

<!--calcule:pages-coachs-->
<!--/calcule:pages-coachs-->'''
for nom in ('llms.txt', 'llms-full.txt'):
    patch(f('public', nom), lambda t: rem(t, '<!--/calcule:pages-disciplines-->', '<!--/calcule:pages-disciplines-->' + BLOC, nom))

# les styles des pages de coach, dans la feuille des pages de discipline
patch(f('public', 'assets', 'css', 'discipline.css'), lambda t: t.rstrip('\n') + '''

/* Le nom du coach mène à sa page. */
.dp-coach h3 a { color: inherit; text-decoration: none; }
.dp-coach h3 a:hover { color: var(--accent); }

/* ── Les pages de coach (/coachs/<slug>/) — même plateau que les disciplines ── */
.cp-hero .phero__title .tint { white-space: normal; }
.cp-photo img { object-position: 50% 28%; }
.cp-faits { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(220px, 100%), 1fr)); gap: 1px; margin: 0;
  background: var(--line); border: 1px solid var(--line); border-radius: var(--radius); overflow: hidden; }
.cp-fait { display: flex; flex-direction: column-reverse; justify-content: flex-end; gap: .6rem; padding: clamp(1.4rem, 3vw, 2.2rem); background: var(--paper); }
.cp-fait dd { margin: 0; font: 700 clamp(2rem, 1.2rem + 3vw, 3.4rem) / 1 var(--f-display); letter-spacing: -.02em; color: var(--ink); text-transform: uppercase; }
.cp-fait dt { font: 600 .72rem / 1.35 var(--f-mono); letter-spacing: .12em; text-transform: uppercase; color: var(--accent); }
.cp-texte { display: grid; grid-template-columns: minmax(0, .8fr) minmax(0, 1.2fr); gap: clamp(1.4rem, 4vw, 4rem); align-items: start; }
@media (max-width: 860px) { .cp-texte { grid-template-columns: minmax(0, 1fr); } }
.cp-paras { display: grid; gap: 1rem; max-width: 64ch; color: var(--ink-soft); font-size: 1.05rem; line-height: 1.65; }
.cp-devise { margin: 2rem 0 0; padding-left: 1.2rem; border-left: 2px solid var(--accent); max-width: 34ch; }
.cp-devise p { font: 700 clamp(1.4rem, 1rem + 1.6vw, 2.2rem) / 1.15 var(--f-display); text-transform: uppercase; color: var(--ink); }
.cp-devise cite { display: block; margin-top: .6rem; font: 600 .7rem / 1 var(--f-mono); letter-spacing: .12em; text-transform: uppercase; font-style: normal; color: var(--accent); }
.cp-autre img { display: block; width: 100%; height: auto; aspect-ratio: 4 / 3; object-fit: cover; object-position: 50% 28%; border-radius: var(--radius); margin-bottom: .4rem; }
''')

# 6. les versions montent
fichiers = [p for motif in ('public/**/*.js', 'public/**/*.html', 'src/**/*.astro', 'scripts/*.mjs')
            for p in glob.glob(os.path.join(R, motif), recursive=True)]
for actif in ('home.js', 'home.css', 'coachs.css', 'discipline.css'):
    rx = re.compile(r'(?<![\w.-])' + re.escape(actif) + r'\?v=(\d+)')
    vus = [int(v) for p in fichiers for v in rx.findall(io.open(p, encoding='utf-8', errors='ignore').read())]
    if not vus:
        print(f'  {actif} : aucune référence versionnée')
        continue
    nv = max(vus) + 1
    touches = 0
    for p in fichiers:
        t, crlf = lire(p)
        t2 = rx.sub(f'{actif}?v={nv}', t)
        if t2 != t:
            ecrire(p, t2, crlf)
            touches += 1
    print(f'  {actif} : v={nv} dans {touches} fichier(s) (versions vues : {sorted(set(vus))})')
print('patch coachs Ramonville appliqué')
