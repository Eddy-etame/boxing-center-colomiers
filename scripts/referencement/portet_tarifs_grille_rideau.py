# -*- coding: utf-8 -*-
"""
Portet — le lot du 2026-09-13 :
  1. les formules enfants et Baby Boxe mènent à l'onglet « Enfants & ados » de
     la boutique (abonnements#enfants), plus à la page générale ;
  2. chaque formule de /tarifs/ porte une ancre (#tarif-baby-boxe…) ;
  3. chaque page de discipline montre ses formules et pousse vers /tarifs/ ;
  4. la grille des neuf disciplines : la boxe anglaise à l'horizontale en tête,
     les huit autres en 4 (ou 2) colonnes, photos carrées (têtes entières) ;
  5. la galerie des pages de discipline sans recadrage (colonnes au ratio) ;
  6. le rideau d'entrée se lève tout seul (CSS du nouveau enter.ts).
Chaque remplacement vérifie son nombre d'occurrences : rien ne passe à moitié.
"""
import io, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
P = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Portet', 'boxing-center-portet')


def lire(*c):
    t = io.open(os.path.join(P, *c), encoding='utf-8', newline='').read()
    return t.replace('\r\n', '\n'), '\r\n' in t


def ecrire(t, crlf, *c):
    io.open(os.path.join(P, *c), 'w', encoding='utf-8', newline='').write(t.replace('\n', '\r\n') if crlf else t)


def rem(t, avant, apres, n=1, nom=''):
    k = t.count(avant)
    assert k == n, f'{nom} : {k} occurrence(s) au lieu de {n} pour {avant[:80]!r}'
    return t.replace(avant, apres)


def sub(t, motif, apres, n=1, nom=''):
    t2, k = re.subn(motif, apres, t, flags=re.M)
    assert k == n, f'{nom} : {k} remplacement(s) au lieu de {n} pour {motif[:80]!r}'
    return t2


ANCRE_JS = r'''"tarif-" + String(nom || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "")'''

# ── 1. content.json : les deux formules enfants ──────────────────────────
t, crlf = lire('src', 'content.json')
t = rem(t, '"https://boutique.boxingcenter.fr/abonnements"', '"https://boutique.boxingcenter.fr/abonnements#enfants"', 2, 'content.json')
ecrire(t, crlf, 'src', 'content.json')

# ── 2. l'ancre, partagée ─────────────────────────────────────────────────
t, crlf = lire('src', 'liens-disciplines.ts')
t = t.rstrip('\n') + '\n\n' + r'''/**
 * L'ancre d'une formule sur /tarifs/ : « Baby Boxe » → tarif-baby-boxe.
 * Même règle dans vite.config.ts (cuisson) et scripts/generate-disciplines.mjs.
 */
export const ancreTarif = (nom: string) =>
  ''' + ANCRE_JS + ';\n'
ecrire(t, crlf, 'src', 'liens-disciplines.ts')

t, crlf = lire('src', 'pages.ts')
t = rem(t, 'import { ouvreCarte, fermeCarte, voirCarte } from "./liens-disciplines";',
        'import { ouvreCarte, fermeCarte, voirCarte, ancreTarif } from "./liens-disciplines";', 1, 'pages.ts import')
t = rem(t, '<div class="tarif ${t.feature ? "tarif--feature" : ""}" data-reveal>',
        '<div class="tarif ${t.feature ? "tarif--feature" : ""}" id="${ancreTarif(t.name)}" data-reveal>', 1, 'pages.ts carte')
ecrire(t, crlf, 'src', 'pages.ts')

t, crlf = lire('vite.config.ts')
t = rem(t, '''          const esc = (s: string) => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
          const cartes = content.tarifs.map(''',
        '''          const esc = (s: string) => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
          /* L'ancre de la formule (#tarif-baby-boxe) : les pages de discipline y renvoient. */
          const ancre = (nom: string) => ''' + ANCRE_JS + ''';
          const cartes = content.tarifs.map(''', 1, 'vite ancre')
t = rem(t, '<div class="tarif ${t.feature ? "tarif--feature" : ""}" data-reveal>${badge}',
        '<div class="tarif ${t.feature ? "tarif--feature" : ""}" id="${ancre(t.name)}" data-reveal>${badge}', 1, 'vite carte')
ecrire(t, crlf, 'vite.config.ts')

# ── 3. les pages de discipline ───────────────────────────────────────────
t, crlf = lire('scripts', 'generate-disciplines.mjs')
t = rem(t, '''const e = (s) => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
''', '''const e = (s) => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

/* L'ancre d'une formule sur /tarifs/ — même règle que src/liens-disciplines.ts. */
const ancreTarif = (nom) => ''' + ANCRE_JS + ''';
const versTarif = (t) => `/tarifs/#${ancreTarif(t.name)}`;
/* Le bouton dit ce qu'il ouvre : « Voir le tarif Baby Boxe », « Voir l’Offre Rentrée ». */
const voirTarif = (t) => (/^offre\\b/i.test(t.name) ? `Voir l’${t.name}`
  : /^saison\\b/i.test(t.name) ? `Voir l’offre ${t.name}` : `Voir le tarif ${t.name}`);
const boutonTarif = (t, cls = "btn btn--primary") => (t
  ? `<a class="${cls}" href="${versTarif(t)}">${e(voirTarif(t))}</a>`
  : `<a class="${cls}" href="/tarifs/">Les tarifs</a>`);
''', 1, 'gen helpers')
t = rem(t, '''  const tarifs = (C.tarifs || []).filter((t) => (p.tarifs || []).includes(t.name));
  const sections = [];''', '''  const tarifs = (C.tarifs || []).filter((t) => (p.tarifs || []).includes(t.name));
  const premier = tarifs[0];
  const sections = [];''', 1, 'gen premier')
t = rem(t, '''        <div class="dp-actions">
          <a class="btn btn--primary" href="/premiere-seance/">Ta première séance</a>
          <a class="btn btn--ghost" href="/plannings/">Tout le planning</a>
        </div>''', '''        <div class="dp-actions">
          ${boutonTarif(premier)}
          <a class="btn btn--ghost" href="/premiere-seance/">Ta première séance</a>
          <a class="btn btn--ghost" href="/plannings/">Tout le planning</a>
        </div>''', 1, 'gen héros')
t = rem(t, '''  if (coachs.length) sections.push(`''', '''  /* LES FORMULES DE LA DISCIPLINE — chaque carte mène à SA formule sur
     /tarifs/ (ancre), où se trouve le bouton de paiement. La page tarifs
     reste le seul endroit où l'on paie : on y envoie, on n'y double rien. */
  if (tarifs.length) sections.push(`
  <section class="section" id="formules">
    <div class="wrap">
      <div class="sec-head" data-reveal>
        <div>
          <span class="eyebrow">Les tarifs</span>
          <h2 class="display" style="margin-top:1rem">${tarifs.length > 1 ? "Ta formule." : "L’inscription."}</h2>
        </div>
        <p class="lead">${tarifs.length > 1
          ? "Chaque formule ouvre toutes les disciplines du club. Le détail et le paiement se font sur la page Tarifs."
          : "L’inscription se fait pour la saison. Le détail et le paiement se font sur la page Tarifs."}</p>
      </div>
      <div class="tarifs dp-tarifs${tarifs.length === 1 ? " dp-tarifs--seul" : ""}" data-reveal-group>
        ${tarifs.map((t) => `<a class="tarif${t.feature ? " tarif--feature" : ""}" href="${versTarif(t)}" data-reveal>`
          + (t.badge ? `<span class="tarif__badge">${e(t.badge)}</span>` : "")
          + `<span class="tarif__name">${e(t.name)}</span>`
          + `<span class="tarif__price">${t.old ? `<s class="tarif__old">${e(t.old)}</s> ` : ""}${e(t.price)}<small> ${e(t.unit || "")}</small></span>`
          + `<p class="tarif__note">${e(t.note || "")}</p>`
          + `<span class="btn ${t.feature ? "btn--primary" : "btn--ghost"} tarif__cta">${e(voirTarif(t))} <span aria-hidden="true">→</span></span></a>`).join("\\n        ")}
      </div>
      <p class="dp-lien"><a href="/tarifs/">Toutes les formules du club →</a></p>
    </div>
  </section>`);

  if (coachs.length) sections.push(`''', 1, 'gen formules')
t = rem(t, '''<div class="dp-actions dp-actions--centre"><a class="btn btn--primary" href="/premiere-seance/">Ta première séance</a><a class="btn btn--ghost" href="/tarifs/">Les tarifs</a><a class="btn btn--ghost" href="/contact/">Nous écrire</a></div>''',
        '''<div class="dp-actions dp-actions--centre">${boutonTarif(premier)}<a class="btn btn--ghost" href="/premiere-seance/">Ta première séance</a><a class="btn btn--ghost" href="/contact/">Nous écrire</a></div>''', 1, 'gen cta final')
t = rem(t, '''      <div class="dp-galerie">''',
        '''      <div class="dp-galerie" style="--cols: ${p.photos.map((ph) => `minmax(0, ${(MANIFESTE[ph.src]?.ar || 1.5).toFixed(3)}fr)`).join(" ")}">''', 1, 'gen galerie')
ecrire(t, crlf, 'scripts', 'generate-disciplines.mjs')

# ── 4 à 6. main.css ──────────────────────────────────────────────────────
t, crlf = lire('src', 'styles', 'main.css')
t = rem(t, '''.disc__media {
  height: 168px;
  background: var(--disc-img) center/cover no-repeat;''', '''.disc__media {
  aspect-ratio: 1 / 1;
  background: var(--disc-img) center 38% / cover no-repeat;''', 1, 'css média')
t = rem(t, '''.disc--img .disc__name { margin-top: 0.8rem; }
''', '''.disc--img .disc__name { margin-top: 0.8rem; }

/* LA GRILLE DES NEUF (page Activités) — plus de case vide, plus de têtes
   coupées. En auto-fill, neuf cartes laissaient une carte seule sur la
   dernière rangée et un grand vide à côté. La première, la boxe anglaise — la
   discipline mère du club —, prend toute la rangée, à l'horizontale ; les huit
   autres tombent juste, en 4 colonnes comme en 2. Les photos sont des
   portraits (4:5) : une bande de 168 px leur coupait la tête, le carré les
   montre, et la carte large les montre entières. */
#act-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); }
#act-grid > :first-child { grid-column: 1 / -1; }
@media (max-width: 1099px) { #act-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 619px) { #act-grid { grid-template-columns: minmax(0, 1fr); } }
@media (min-width: 620px) {
  #act-grid > .disc--img:first-child { display: grid; grid-template-columns: minmax(240px, 32%) minmax(0, 1fr);
    grid-template-rows: auto 1fr; }
  #act-grid > .disc--img:first-child .disc__media { grid-row: 1 / span 2; aspect-ratio: 4 / 5; background-position: center; }
  #act-grid > .disc--img:first-child .disc__top { padding: clamp(1.4rem, 3vw, 2.6rem) clamp(1.6rem, 3.4vw, 3.2rem) 0; }
  #act-grid > .disc--img:first-child > div:last-child { align-self: end;
    padding: 1.4rem clamp(1.6rem, 3.4vw, 3.2rem) clamp(1.6rem, 3.4vw, 3rem); }
  #act-grid > :first-child .disc__name { font-size: clamp(2.6rem, 5.4vw, 5rem); margin-bottom: 1rem; }
  #act-grid > :first-child .disc__desc { font-size: 1.1rem; max-width: 46ch; }
}
''', 1, 'css grille')
t = sub(t, r'^(\.tarif--feature \{[^\n]*\}\n)', r'''\1/* Une formule se vise : /tarifs/#tarif-baby-boxe arrive sur SA carte, et la carte le montre. */
.tarif { scroll-margin-top: clamp(96px, 16vh, 150px); }
.tarif--vise { border-color: var(--accent); animation: tarifVise 1.4s var(--ease-out) 0.35s 2; }
@keyframes tarifVise { 0% { box-shadow: 0 0 0 0 var(--glow); } 60% { box-shadow: 0 0 0 14px transparent; } 100% { box-shadow: 0 0 0 0 transparent; } }
a.tarif { color: inherit; text-decoration: none; }
.dp-tarifs--seul { grid-template-columns: minmax(0, 520px); }
''', 1, 'css tarif')
t = rem(t, '.dp-valeurs, .dp-publics, .dp-planning, .dp-coachs, .dp-galerie, .dp-voisines { margin-top: 2.4rem; }',
        '.dp-valeurs, .dp-publics, .dp-planning, .dp-tarifs, .dp-coachs, .dp-galerie, .dp-voisines { margin-top: 2.4rem; }', 1, 'css marges')
t = rem(t, '.dp-galerie { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }',
        '/* Deux photos, deux formats : chaque colonne prend la largeur de SON ratio (--cols, écrit au build),\n   les deux images ont la même hauteur, et aucune n\'est recadrée. */\n'
        '.dp-galerie { display: grid; grid-template-columns: var(--cols, repeat(2, minmax(0, 1fr))); gap: 1rem; align-items: start; }', 1, 'css galerie')
t = rem(t, '.dp-galerie__item img { display: block; width: 100%; height: auto; aspect-ratio: 3 / 2; object-fit: cover; }',
        '.dp-galerie__item img { display: block; width: 100%; height: auto; }', 1, 'css galerie img')
t = rem(t, '.dp-photo img { display: block; width: 100%; height: 100%; object-fit: cover; }',
        '.dp-photo img { display: block; width: 100%; height: 100%; object-fit: cover; object-position: center 35%; }', 1, 'css photo')
t = rem(t, '  .dp-photo { aspect-ratio: 16 / 10; max-width: 760px; }', '  .dp-photo { aspect-ratio: 1 / 1; max-width: 560px; }', 1, 'css photo mobile')

# le rideau
t = rem(t, '''  transition: opacity 1.1s var(--ease-io);
  overflow: hidden;
}''', '''  /* Le rideau se lève d'un seul tenant. Durée = DUREE_LEVER dans enter.ts. */
  transition: transform 0.95s cubic-bezier(0.76, 0, 0.24, 1);
  overflow: hidden;
}
/* Le bas du rideau : un fil d'accent, visible pendant qu'il monte. */
.gate::after { content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 2px; z-index: 6; pointer-events: none;
  background: linear-gradient(90deg, transparent, var(--accent) 18%, var(--accent) 82%, transparent);
  box-shadow: 0 0 22px var(--glow); opacity: 0; transition: opacity 0.25s; }
.gate--leve { transform: translateY(-100%); pointer-events: none; }
.gate--leve::after { opacity: 1; }
.gate--leve .gate__inner { animation: gateMonte 0.95s cubic-bezier(0.76, 0, 0.24, 1) forwards; }
.gate--leve .gate__ring-host { animation: ringRush 0.95s var(--ease-io) forwards; }
@keyframes gateMonte { to { opacity: 0; transform: translateY(-16vh); } }''', 1, 'css rideau')
for motif, nom in [
    (r'^\.gate--entering [^\n]*\n', 'entering'),
    (r'^\.gate--out \{[^\n]*\}\n', 'out'),
]:
    t = sub(t, motif, '', 4 if nom == 'entering' else 1, nom)
t = sub(t, r'^\n?\.gate__flash \{[^}]*\}\n@keyframes gateFlashBurst \{[\s\S]*?\n\}\n', '', 1, 'flash')
t = sub(t, r'^  \.gate__flash \{ display: none; \}\n', '', 1, 'flash réduit')
for motif in [r'^\.gate__enter \{[^}]*\}\n', r'^\.gate__enter:hover \{[^}]*\}\n', r'^\.gate__hint \{[^}]*\}\n',
              r'^/\* 118 x 18 px[\s\S]*?\*/\n', r'^\.gate__silent \{[^}]*\}\n', r'^\.gate__enter\[disabled\] \{[^}]*\}\n',
              r'^\.gate__enter\[disabled\]:hover \{[^}]*\}\n', r'^\.gate--ready \.gate__enter \{[^}]*\}\n',
              r'^@keyframes gatePulse [^\n]*\n', r'^\.gate__silent\[disabled\] \{[^}]*\}\n']:
    t = sub(t, motif, '', 1, motif)
t = rem(t, '''  .gate__bar::after, .gate__spotlight { animation: none !important; }
''', '''  .gate__bar::after, .gate__spotlight { animation: none !important; }
  .gate { transition: opacity 0.3s ease; }
  .gate--leve { transform: none; opacity: 0; }
  .gate--leve .gate__inner, .gate--leve .gate__ring-host { animation: none; }
''', 1, 'css rideau réduit')
for reste in ['gate__enter', 'gate__silent', 'gate__hint', 'gate--entering', 'gate--out', 'gate__flash', 'gatePulse']:
    assert reste not in t, f'reste dans main.css : {reste}'
ecrire(t, crlf, 'src', 'styles', 'main.css')
print('patch Portet appliqué')
