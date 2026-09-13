# -*- coding: utf-8 -*-
"""
Ramonville — le lot du 2026-09-13 :
  1. l'École enfants et le lien « enfants » ouvrent l'onglet Enfants & ados de
     la boutique (abonnements#enfants) ; l'abonnement 4 semaines, l'onglet
     prélèvement (#prelevement) ;
  2. chaque formule de /tarifs/ porte une ancre (#tarif-ecole-enfants…), et un
     lien vers elle arrive sur SA carte ;
  3. chaque page de discipline montre ses formules et renvoie à la bonne carte
     de /tarifs/. Jamais la séance d'essai : son prix ne vit que sur /tarifs/.
  4. les numéros de version des fichiers touchés montent, pour que les
     navigateurs ne gardent pas les anciens liens en cache.
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


ANCRE = r'''"tarif-" + String(nom || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "")'''

# ── 1. data.js et chatbot.js : les bons onglets de la boutique ───────────
t, crlf = lire(f('public', 'assets', 'js', 'data.js'))
t = sub(t, r'(name: "Abonnement 4 semaines",[^{}]*?href: "https://boutique\.boxingcenter\.fr/abonnements)(")', r'\1#prelevement\2', 'data 4 semaines')
t = sub(t, r'(name: "École enfants",[^{}]*?href: "https://boutique\.boxingcenter\.fr/abonnements)(")', r'\1#enfants\2', 'data école')
t = rem(t, '  enfants: "https://boutique.boxingcenter.fr/abonnements",', '  enfants: "https://boutique.boxingcenter.fr/abonnements#enfants",', 'data LINKS')
ecrire(f('public', 'assets', 'js', 'data.js'), t, crlf)

t, crlf = lire(f('public', 'assets', 'js', 'chatbot.js'))
t = sub(t, r'(enfants:\s*\{[^}\n]*boutique\("https://boutique\.boxingcenter\.fr/abonnements)("\))', r'\1#enfants\2', 'chatbot enfants')
ecrire(f('public', 'assets', 'js', 'chatbot.js'), t, crlf)

# ── 2. /tarifs/ : une ancre par formule, et on y va ──────────────────────
t, crlf = lire(f('public', 'assets', 'js', 'page.js'))
t = rem(t, '''const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
''', '''const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

/* L'ancre d'une formule sur /tarifs/ : « École enfants » → tarif-ecole-enfants.
   Même règle dans scripts/cuire-pages.mjs et scripts/generer-disciplines.mjs. */
const ancreTarif = (nom) => ''' + ANCRE + ''';
''', 'page.js ancre')
t = rem(t, '<article class="tarif ${t.highlight ? "tarif--hot" : ""}">',
        '<article class="tarif ${t.highlight ? "tarif--hot" : ""}" id="${ancreTarif(t.name)}">', 'page.js carte')
t = rem(t, '''    </article>`).join("");

  const pbox = $("#promos");''', '''    </article>`).join("");
  viserFormule();

  const pbox = $("#promos");''', 'page.js appel')
t = rem(t, '''/* ------------------------------ TARIFS --------------------------- */
function renderTarifs() {''', '''/* ------------------------------ TARIFS --------------------------- */
/* Un lien vers une formule (/tarifs/#tarif-ecole-enfants) arrive sur SA
   carte. La grille vient d'être réécrite : le navigateur, lui, a visé
   l'ancienne, et Lenis garde en cache une hauteur de page périmée. */
function viserFormule() {
  let id = "";
  try { id = decodeURIComponent(location.hash.slice(1)); } catch {}
  if (!id.startsWith("tarif-")) return;
  const aller = () => {
    const el = document.getElementById(id);
    if (!el) return;
    const offset = -Math.round(Math.min(150, Math.max(96, innerHeight * 0.16)));
    const lenis = window.BC?.lenis;
    if (lenis) { lenis.resize?.(); lenis.scrollTo(el, { offset, duration: 1.1, force: true }); }
    else window.scrollTo({ top: el.getBoundingClientRect().top + scrollY + offset, behavior: reduce ? "auto" : "smooth" });
  };
  setTimeout(() => requestAnimationFrame(aller), 350);
}

function renderTarifs() {''', 'page.js viser')
ecrire(f('public', 'assets', 'js', 'page.js'), t, crlf)

t, crlf = lire(f('scripts', 'cuire-pages.mjs'))
t = rem(t, '''/* /tarifs — les offres et les avis */
const tarifs = TARIFS.map(
  (t) =>
    `<article><h3>''', '''/* /tarifs — les offres et les avis. Chaque formule porte son ancre
   (#tarif-ecole-enfants) : les pages de discipline y renvoient. */
const ancreTarif = (nom) => ''' + ANCRE + ''';
const tarifs = TARIFS.map(
  (t) =>
    `<article id="${ancreTarif(t.name)}"><h3>''', 'cuire ancre')
ecrire(f('scripts', 'cuire-pages.mjs'), t, crlf)

t, crlf = lire(f('public', 'assets', 'css', 'page.css'))
t = sub(t, r'^(\.tarif--hot \{ background[^\n]*\n)', r'''\1/* Une formule se vise : /tarifs/#tarif-ecole-enfants arrive sur SA carte, et la carte le montre. */
.tarif { scroll-margin-top: clamp(96px, 16vh, 150px); }
.tarif:target { border-color: var(--accent); animation: tarifVise 1.4s ease-out .35s 2; }
@keyframes tarifVise { 0% { box-shadow: 0 0 0 0 var(--accent-line, var(--accent)); } 60% { box-shadow: 0 0 0 14px transparent; } 100% { box-shadow: 0 0 0 0 transparent; } }
''', 'page.css')
ecrire(f('public', 'assets', 'css', 'page.css'), t, crlf)

# ── 3. les pages de discipline ───────────────────────────────────────────
t, crlf = lire(f('scripts', 'generer-disciplines.mjs'))
t = rem(t, 'function donneesStructurees(p, d, url, og, liste) {', '''/* L'ancre d'une formule sur /tarifs/ — même règle que public/assets/js/page.js. */
const ancreTarif = (nom) => ''' + ANCRE + ''';
const versTarif = (t) => `/tarifs/#${ancreTarif(t.name)}`;
/* Les formules d'une discipline : l'École enfants pour l'école, les formules
   adultes ailleurs. Jamais la séance d'essai : son prix ne vit que sur /tarifs/. */
const tarifsDe = (cle) => (TARIFS || [])
  .filter((t) => !/essai/i.test(t.name))
  .filter((t) => (cle === "ecole") === /enfant/i.test(t.name));
/* Le bouton dit ce qu'il ouvre : « Voir l’Offre Rentrée », « Voir le tarif École enfants ». */
const voirTarif = (t) => (/^offre\\b/i.test(t.name) ? `Voir l’${t.name}`
  : /^abonnement\\b/i.test(t.name) ? `Voir l’${t.name.charAt(0).toLowerCase()}${t.name.slice(1)}`
  : `Voir le tarif ${t.name}`);
const boutonTarif = (t) => (t
  ? `<a class="btn btn--primary" href="${versTarif(t)}"><span>${e(voirTarif(t))}</span></a>`
  : `<a class="btn btn--primary" href="/tarifs/"><span>Les tarifs</span></a>`);

function donneesStructurees(p, d, url, og, liste) {''', 'gen helpers')
t = rem(t, '''  const offre = (TARIFS || []).find((t) => /rentr/i.test(t.name));
  const service = {''', '''  const service = {''', 'gen jsonld const')
t = rem(t, '''  if (offre) service.offers = { "@type": "Offer", name: offre.name, price: String(offre.price).replace(/\\D/g, ""), priceCurrency: "EUR", url: offre.href, description: `${offre.price} ${offre.period || ""}`.trim() };''',
        '''  const formules = tarifsDe(d.key);
  if (formules.length) service.offers = formules.map((t) => ({ "@type": "Offer", name: t.name, price: String(t.price).replace(/\\D/g, ""), priceCurrency: "EUR", url: t.href, description: `${t.price} ${t.period || ""}`.trim() }));''', 'gen jsonld offres')
t = rem(t, '''            <a class="btn btn--primary" href="${e(LINKS.rentree)}"><span>Quatre semaines · 29 €</span></a>
            <a class="btn btn--ghost" href="/plannings/"><span>Voir le planning</span></a>''', '''            ${boutonTarif(tarifsDe(d.key)[0])}
            <a class="btn btn--ghost" href="/plannings/"><span>Voir le planning</span></a>''', 'gen héros')
t = rem(t, '''          <a class="btn btn--primary" href="${e(LINKS.rentree)}"><span>Quatre semaines · 29 €</span></a>
          <a class="btn btn--ghost" href="/activites/"><span>Toutes les activités</span></a>''', '''          ${boutonTarif(tarifsDe(d.key)[0])}
          <a class="btn btn--ghost" href="/activites/"><span>Toutes les activités</span></a>''', 'gen fin')
t = rem(t, '''  const offre = (TARIFS || []).find((t) => /rentr/i.test(t.name));
  s.push(`
    <section class="section dp-bande" aria-labelledby="t-infos">''', '''  /* LES FORMULES DE LA DISCIPLINE — chaque carte mène à SA formule sur
     /tarifs/ (ancre), où se trouve le bouton de paiement. */
  const formules = tarifsDe(d.key);
  const offre = formules[0];
  if (formules.length) s.push(`
    <section class="section" id="formules" aria-labelledby="t-formules">
      <div class="wrap">
        <div class="shead" data-reveal><span class="eyebrow">Les tarifs</span><h2 class="display" id="t-formules">${formules.length > 1 ? "Ta formule." : "L’inscription."}</h2></div>
        <div class="dp-grille dp-grille--3 dp-tarifs${formules.length === 1 ? " dp-tarifs--seul" : ""}" data-reveal-group>
          ${formules.map((t) => `<a class="dp-carte dp-carte--lien${t.highlight ? " dp-carte--hot" : ""}" href="${versTarif(t)}"><h3>${e(t.name)}</h3><p class="dp-prix">${e(t.price)} <small>${e(t.period || "")}</small></p>${t.feature ? `<p>${e(t.feature)}</p>` : ""}<span class="dp-go">${e(voirTarif(t))} <span aria-hidden="true">→</span></span></a>`).join("\\n          ")}
        </div>
        <p class="dp-lien"><a href="/tarifs/">Toutes les formules du club →</a></p>
      </div>
    </section>`);

  s.push(`
    <section class="section dp-bande" aria-labelledby="t-infos">''', 'gen formules')
t = rem(t, '''<a href="/tarifs/">Toutes les formules →</a></dd></div>` : ""}''',
        '''<a href="${versTarif(offre)}">La formule en détail →</a></dd></div>` : ""}''', 'gen infos')
ecrire(f('scripts', 'generer-disciplines.mjs'), t, crlf)

t, crlf = lire(f('public', 'assets', 'css', 'discipline.css'))
t = t.rstrip('\n') + '''

/* Les formules de la discipline — chaque carte mène à SA formule sur /tarifs/. */
.dp-tarifs .dp-carte { gap: 0.7rem; }
.dp-tarifs--seul { max-width: 520px; }
.dp-carte--hot { background: color-mix(in srgb, var(--accent) 10%, var(--paper)); }
.dp-prix { font: 700 clamp(1.9rem, 1.4rem + 1.6vw, 2.6rem) / 1 var(--f-display); letter-spacing: -0.02em; color: var(--ink); }
.dp-prix small { font: 600 0.68rem / 1.3 var(--f-mono); letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); }
'''
ecrire(f('public', 'assets', 'css', 'discipline.css'), t, crlf)

# ── 4. les versions des fichiers touchés montent ─────────────────────────
fichiers = [p for motif in ('public/**/*.js', 'public/**/*.html', 'src/**/*.astro', 'scripts/*.mjs')
            for p in glob.glob(os.path.join(R, motif), recursive=True)]
for actif in ('data.js', 'page.js', 'chatbot.js', 'page.css', 'discipline.css'):
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
print('patch Ramonville appliqué')
