# -*- coding: utf-8 -*-
"""
Le lot du 13/09 au soir (2/2) :
  1. LES NUMÉROS (Eddy : « les numéros ont changé ») — ceux que les sites
     satellites publient déjà : Ramonville 09 39 03 67 48 (celui de Labège
     pour Ramonville), Portet 09 56 65 37 82 (celui des satellites pour
     Portet, et du Noble Art Portésien). Trois écritures chacun.
  2. RAMONVILLE — 259 € D'ABORD, PUIS 29 € : chaque plaque et chaque bouton
     de l'offre 29 € montre deux faces qui alternent (offres.js), mène à
     https://boutique.boxingcenter.fr/offres-speciales ; la barre, le menu, le
     pied de page aussi. La plaque de /tarifs/ reste celle des conditions du
     29 € (son amorce l'énonce mot pour mot : changer l'offre y changerait le
     texte d'Eddy).
  3. RAMONVILLE — la carte qui reste (offres.js) et le passage secret (CSS).
  4. RAMONVILLE — la légende heure · plateau extérieur · température, centrée.
Chaque remplacement vérifie son nombre ; fins de ligne laissées telles quelles.
"""
import glob, io, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
BC = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center')
R = os.path.join(BC, 'Deployment', 'bc-ramonville')
P = os.path.join(BC, 'Portet', 'boxing-center-portet')
EXCLUS = {'.git', 'node_modules', 'dist', '.vercel', '.astro', '.research'}


def f(*c):
    return os.path.join(R, *c)


def lire(p):
    return io.open(p, encoding='utf-8', newline='').read()


def ecrire(p, t):
    io.open(p, 'w', encoding='utf-8', newline='').write(t)


def rem(t, avant, apres, nom, n=1):
    """Rejouable : une étape déjà passée est sautée. Les « 29 € » du site
    s'écrivent tantôt avec une espace, tantôt avec une insécable."""
    variantes = []
    for a, b in ((avant, apres), (avant.replace(' €', '\xa0€'), apres.replace(' €', '\xa0€'))):
        variantes += [(a, b), (a.replace('\n', '\r\n'), b.replace('\n', '\r\n'))]
    for a, b in variantes:
        if t.count(a) == n:
            return t.replace(a, b)
    if all(t.count(a) == 0 for a, _ in variantes) and any(b in t for _, b in variantes):
        print(f'  (déjà fait : {nom})')
        return t
    raise AssertionError(f'{nom} : {t.count(avant)} occurrence(s) au lieu de {n} pour {avant[:90]!r}')


def patch(p, *ops):
    t = lire(p)
    for op in ops:
        t = op(t)
    ecrire(p, t)
    print('  ok', os.path.relpath(p, BC))


# ── 1. les numéros ────────────────────────────────────────────────────────
def remplacer_numeros(racine, paires):
    total, fichiers = 0, 0
    for dossier, sous, noms in os.walk(racine):
        sous[:] = [s for s in sous if s not in EXCLUS]
        for nom in noms:
            if not re.search(r'\.(astro|html|js|mjs|ts|json|txt|md|py|css)$', nom):
                continue
            p = os.path.join(dossier, nom)
            try:
                t = lire(p)
            except UnicodeDecodeError:
                continue
            t2, k = t, 0
            for a, b in paires:
                k += t2.count(a)
                t2 = t2.replace(a, b)
            if k:
                ecrire(p, t2)
                total += k
                fichiers += 1
    return total, fichiers


print('Ramonville → 09 39 03 67 48 :', remplacer_numeros(R, [
    ('+33 5 62 24 46 82', '+33 9 39 03 67 48'), ('+33562244682', '+33939036748'),
    ('05 62 24 46 82', '09 39 03 67 48'), ('0562244682', '0939036748')]))
print('Portet → 09 56 65 37 82 :', remplacer_numeros(P, [
    ('+33 6 87 90 02 16', '+33 9 56 65 37 82'), ('+33687900216', '+33956653782'),
    ('06 87 90 02 16', '09 56 65 37 82'), ('0687900216', '0956653782')]))

# ── 2. Ramonville : les plaques et les boutons de l'offre ─────────────────
PROMOS = 'https://boutique.boxingcenter.fr/offres-speciales'
ARIA = 'Offres spéciales : l’année complète à 259 € au lieu de 400 €, ou l’offre de rentrée à 29 € par personne pour 4 semaines, au lieu de 44 €'


def plaque_duo(ind):
    i = ind
    return (f'<a class="plaque plaque--duo" data-reveal href="{PROMOS}"\n'
            f'{i}   aria-label="{ARIA}">\n'
            f'{i}  <span class="plaque__faces alt" data-alterne>\n'
            f'{i}    <span class="plaque__face alt__face is-on">\n'
            f'{i}      <span class="plaque__sur">L’année complète</span>\n'
            f'{i}      <span class="plaque__prix"><b>259</b><i>€</i></span>\n'
            f'{i}      <span class="plaque__unit">12 mois · les 5 clubs</span>\n'
            f'{i}      <span class="plaque__barre">au lieu de 400 €</span>\n'
            f'{i}    </span>\n'
            f'{i}    <span class="plaque__face alt__face" aria-hidden="true">\n'
            f'{i}      <span class="plaque__sur">Offre de rentrée</span>\n'
            f'{i}      <span class="plaque__prix"><b>29</b><i>€</i></span>\n'
            f'{i}      <span class="plaque__unit">par personne · 4 semaines</span>\n'
            f'{i}      <span class="plaque__barre">au lieu de 44 €</span>\n'
            f'{i}    </span>\n'
            f'{i}  </span>\n'
            f'{i}  <span class="plaque__go">Voir les offres spéciales <i aria-hidden="true">→</i></span>\n'
            f'{i}</a>')


RX_PLAQUE = re.compile(r'(?m)^([ \t]*)<a class="plaque" data-reveal href="https://boutique\.boxingcenter\.fr/inscription\?product=offre-duo[^"]*"\s*aria-label="[^"]*">[\s\S]*?</a>')
RX_BOUTON = re.compile('<a class="btn btn--primary" data-magnetic href="https://boutique\\.boxingcenter\\.fr/inscription\\?product=offre-duo[^"]*"><span>(Je profite de l\'offre — 29[  ]€)</span></a>')


def BOUTON(m):
    # la face 29 € garde le libellé d'origine, à l'espace près
    return (f'<a class="btn btn--primary" data-magnetic href="{PROMOS}" aria-label="Offres spéciales : l’année complète à 259 €, ou 29 € par personne pour 4 semaines">'
            '<span class="alt" data-alterne><span class="alt__face is-on">L’année complète · 259 €</span>'
            f'<span class="alt__face" aria-hidden="true">{m.group(1)}</span></span></a>')
n_plaques = n_boutons = 0
for p in sorted(glob.glob(f('src', 'pages', '**', '*.astro'), recursive=True)):
    if os.sep + 'tarifs' + os.sep in p:
        continue
    t = lire(p)
    t2, kp = RX_PLAQUE.subn(lambda m: m.group(1) + plaque_duo(m.group(1)), t)
    t2, kb = RX_BOUTON.subn(BOUTON, t2)
    if kp or kb:
        ecrire(p, t2)
        n_plaques += kp
        n_boutons += kb
        print(f'  {os.path.relpath(p, R)} : {kp} plaque(s), {kb} bouton(s)')
pages = [lire(p) for p in glob.glob(f('src', 'pages', '**', '*.astro'), recursive=True)]
assert sum(t.count('class="plaque plaque--duo"') for t in pages) == 7, 'plaques duo ≠ 7'
assert sum(t.count('Je profite de l\'offre — 29') - t.count('aria-hidden="true">Je profite de l\'offre — 29') for t in pages) == 0, 'bouton 29 € resté seul'
print(f'  bilan : 7 plaques duo, {sum(t.count("data-alterne") for t in pages)} alternances dans les pages')
patch(f('src', 'pages', 'index.astro'), lambda t: rem(t,
      '<p data-reveal class="offre__detail">29&nbsp;€ par personne · 4 semaines · gants et bandes prêtés</p>',
      '<p data-reveal class="offre__detail alt" data-alterne><span class="alt__face is-on">259&nbsp;€ comptant · 12 mois · les 5 clubs</span>'
      '<span class="alt__face" aria-hidden="true">29&nbsp;€ par personne · 4 semaines · gants et bandes prêtés</span></p>', 'détail hero'))

patch(f('public', 'assets', 'js', 'site.js'),
      lambda t: rem(t, 'import { initPlaces } from "./places.js?v=19";\n',
                    'import { initPlaces } from "./places.js?v=19";\nimport { demarrerOffres } from "./offres.js?v=1";\n', 'import offres'),
      lambda t: rem(t, '<a class="btn btn--primary nav__cta" data-magnetic href="${LINKS.rentree}"><span>Offre · 29 € / 4 sem.</span></a>',
                    '<a class="btn btn--primary nav__cta" data-magnetic href="${LINKS.promos}" aria-label="Offres spéciales : l’année complète à 259 €, ou 29 € par personne pour 4 semaines">'
                    '<span class="alt" data-alterne><span class="alt__face is-on">L’année · 259 €</span><span class="alt__face" aria-hidden="true">Offre · 29 € / 4 sem.</span></span></a>', 'cta barre'),
      lambda t: rem(t, '<a class="btn btn--primary" data-magnetic href="${LINKS.rentree}"><span>Voir l’offre · 29 € / 4 sem.</span></a>',
                    '<a class="btn btn--primary" data-magnetic href="${LINKS.promos}" aria-label="Offres spéciales : l’année complète à 259 €, ou 29 € par personne pour 4 semaines">'
                    '<span class="alt" data-alterne><span class="alt__face is-on">L’année complète · 259 €</span><span class="alt__face" aria-hidden="true">Voir l’offre · 29 € / 4 sem.</span></span></a>', 'cta menu et pied', 2),
      lambda t: rem(t, 'mountNav();\nmountFooter();\n', 'mountNav();\nmountFooter();\n/* les deux offres en alternance et la carte qui reste (offres.js) */\ndemarrerOffres();\n', 'démarrage'))

# ── 3. le passage secret, la carte qui reste ──────────────────────────────
patch(f('public', 'assets', 'css', 'base.css'), lambda t: t if 'LES DEUX OFFRES, EN ALTERNANCE' in t else t.rstrip('\r\n') + '''

/* ===================== LES DEUX OFFRES, EN ALTERNANCE =====================
   Eddy, 13/09 : 259 € d'abord, puis 29 €, et ainsi de suite (offres.js).
   Les deux faces occupent la même case : la plus large donne la taille,
   rien ne saute. LE PASSAGE SECRET : la face sortante se referme sur une
   fente de lumière au milieu, la face entrante s'ouvre de la fente vers
   les bords — une porte dérobée, pas un fondu. */
.alt { display: inline-grid; position: relative; }
.alt > .alt__face { grid-area: 1 / 1; }
.alt > .alt__face:not(.is-on) { visibility: hidden; }
.offre__detail.alt { display: grid; }
.plaque__faces.alt { display: grid; justify-items: center; }
.plaque__face { display: grid; gap: .1rem; justify-items: center; }
.alt.is-passage > .alt__face.is-sort { visibility: visible; animation: altSort .9s cubic-bezier(.7,0,.3,1) forwards; }
.alt.is-passage > .alt__face.is-entre { animation: altEntre .9s cubic-bezier(.7,0,.3,1) forwards; }
.alt.is-passage::after { content: ""; position: absolute; top: 6%; bottom: 6%; left: 50%; width: 2px; pointer-events: none;
  background: linear-gradient(180deg, transparent, currentColor 28%, currentColor 72%, transparent);
  box-shadow: 0 0 12px currentColor, 0 0 26px currentColor; opacity: 0; transform: translateX(-50%) scaleY(0);
  animation: altFente .9s cubic-bezier(.7,0,.3,1) forwards; }
@keyframes altSort { 0% { clip-path: inset(0 0 0 0); opacity: 1; } 50% { clip-path: inset(0 50% 0 50%); opacity: 1; } 100% { clip-path: inset(0 50% 0 50%); opacity: 0; } }
@keyframes altEntre { 0%, 42% { clip-path: inset(0 50% 0 50%); opacity: 0; transform: scale(.97); } 48% { opacity: 1; } 100% { clip-path: inset(0 0 0 0); opacity: 1; transform: none; } }
@keyframes altFente { 0% { opacity: 0; transform: translateX(-50%) scaleY(0); } 34%, 58% { opacity: .95; transform: translateX(-50%) scaleY(1); } 100% { opacity: 0; transform: translateX(-50%) scaleY(1); } }
@media (prefers-reduced-motion: reduce) { .alt.is-passage > .alt__face, .alt.is-passage::after { animation: none; } }

/* ===================== LA CARTE QUI RESTE (Eddy, 13/09) =====================
   Toujours à l'écran, en bas à gauche, sur toutes les pages : la plaque en
   format de poche, 259 € d'abord puis 29 €, vers les offres spéciales.
   Elle s'efface quand une grande plaque est déjà à l'écran (offres.js) et
   quand le menu est ouvert. */
.flotte { position: fixed; left: clamp(.7rem, 2vw, 1.4rem); bottom: clamp(.7rem, 2vw, 1.4rem); z-index: 7980;
  width: clamp(150px, 14vw, 186px); padding: .95rem .8rem .8rem; --coin: 11px;
  transition: opacity .35s, transform .35s cubic-bezier(.2,.7,.3,1), filter .35s, box-shadow .35s; }
.flotte::before { inset: 8px; }
.flotte .plaque__sur { font-size: .54rem; letter-spacing: .18em; }
.flotte .plaque__prix { margin: .3rem 0 .05rem; }
.flotte .plaque__prix b { font-size: clamp(2.2rem, 3.6vw, 2.8rem); }
.flotte .plaque__prix i { font-size: 1rem; }
.flotte .plaque__unit { font-size: .58rem; }
.flotte .plaque__go { margin-top: .5rem; font-size: .72rem; }
.flotte.is-cachee { opacity: 0; transform: translateY(14px); pointer-events: none; }
.is-menu-open .flotte { opacity: 0; pointer-events: none; }
@media (max-width: 600px) {
  .flotte { width: 128px; padding: .7rem .6rem .6rem; --coin: 9px; }
  .flotte .plaque__prix b { font-size: 1.9rem; }
  .flotte .plaque__unit { display: none; }
}
@media (prefers-reduced-motion: reduce) { .flotte { transition: none; } }
''')

# ── 4. la légende du hero, centrée ────────────────────────────────────────
patch(f('public', 'assets', 'css', 'home.css'),
      lambda t: rem(t, '.hero__cap { position: absolute; left: 0; bottom: -.4rem;',
                    '/* centrée sous l’octogone, dans l’axe de « il tourne » (elle collait au bord gauche).\n   Marges automatiques, pas de transform : le mouvement du hero garde la main sur transform. */\n.hero__cap { position: absolute; left: 0; right: 0; margin-inline: auto; width: max-content; max-width: 100%; text-align: center; bottom: -.4rem;', 'légende'),
      lambda t: rem(t, '.hero__cap { position: static; display: inline-block; margin-top: 2.4rem; }',
                    '.hero__cap { position: static; display: inline-block; justify-self: center; margin-top: 2.4rem; }', 'légende téléphone'))

patch(f('public', 'assets', 'js', 'page.js'), lambda t: rem(t,
      '<a class="btn btn--primary" data-magnetic href="${LINKS.rentree}"><span>Quatre semaines · 29 €</span></a>',
      '<a class="btn btn--primary" data-magnetic href="${LINKS.promos}" aria-label="Offres spéciales : l’année complète à 259 €, ou 29 € par personne pour 4 semaines">'
      '<span class="alt" data-alterne><span class="alt__face is-on">L’année complète · 259 €</span><span class="alt__face" aria-hidden="true">Quatre semaines · 29 €</span></span></a>', 'bouton disciplines'))

# ── 5. les versions montent ───────────────────────────────────────────────
fichiers = [p for motif in ('public/**/*.js', 'public/**/*.html', 'src/**/*.astro', 'scripts/*.mjs')
            for p in glob.glob(os.path.join(R, motif), recursive=True)]
for actif in ('site.js', 'base.css', 'home.css', 'data.js', 'chatbot.js', 'chatbot-kb.js'):
    rx = re.compile(r'(?<![\w.-])' + re.escape(actif) + r'\?v=(\d+)')
    vus = [int(v) for p in fichiers for v in rx.findall(io.open(p, encoding='utf-8', errors='ignore').read())]
    if not vus:
        continue
    nv, n = max(vus) + 1, 0
    for p in fichiers:
        t = lire(p)
        t2 = rx.sub(f'{actif}?v={nv}', t)
        if t2 != t:
            ecrire(p, t2)
            n += 1
    print(f'  {actif} → v={nv} ({n} fichiers)')
print('lot offres + numéros appliqué')
