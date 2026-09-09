# -*- coding: utf-8 -*-
"""
Équipe un site satellite de sa vignette OG par page, de son favicon et de sa
teinte : polices TTF, src/data/teinte.ts (lu dans jetons.css), l'endpoint
src/pages/og/[page].png.ts avec LE dessin du site, public/favicon.svg, et
Base.astro branché. Usage : python equiper_og.py <muret|cugnaux|labege|lunion|castelginest>
"""
import io, os, re, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"C:\Users\Mommy Jayce\Desktop\Boxing Center\Deployment"
REF = os.path.join(BASE, 'boxing-center-tournefeuille')
site = sys.argv[1]
R = os.path.join(BASE, f'boxing-center-{site}')

# ── 1. les polices ────────────────────────────────────────────────────────
os.makedirs(os.path.join(R, 'src', 'og', 'fonts'), exist_ok=True)
for f in os.listdir(os.path.join(REF, 'src', 'og', 'fonts')):
    shutil.copyfile(os.path.join(REF, 'src', 'og', 'fonts', f), os.path.join(R, 'src', 'og', 'fonts', f))

# ── 2. la teinte, lue dans jetons.css ────────────────────────────────────
jetons = io.open(os.path.join(R, 'src', 'styles', 'jetons.css'), encoding='utf-8').read()
def jeton(nom):
    m = re.search(r'^\s*--' + re.escape(nom) + r':\s*([^;]+);', jetons, re.M)
    return m.group(1).strip() if m else ''
T = {k: jeton(k) for k in ['papier', 'papier-creuse', 'papier-vif', 'encre', 'graphite', 'trait', 'signal', 'signal-texte', 'signal-profond']}
manque = [k for k, v in T.items() if not v]
assert not manque, f'jetons absents : {manque}'
teinte_ts = f"""/**
 * LA TEINTE DU SITE — les mêmes valeurs que `styles/jetons.css`, lisibles
 * depuis un script de build : la vignette OG et le favicon se dessinent avec
 * la couleur du site, pas avec une couleur retapée.
 *
 * Une valeur change ici ET dans jetons.css, jamais dans un seul des deux.
 */
export const TEINTE = {{
  papier: '{T['papier']}',
  papierCreuse: '{T['papier-creuse']}',
  papierVif: '{T['papier-vif']}',
  encre: '{T['encre']}',
  graphite: '{T['graphite']}',
  trait: '{T['trait']}',
  signal: '{T['signal']}',
  signalTexte: '{T['signal-texte']}',
  signalProfond: '{T['signal-profond']}',
}} as const;
"""
io.open(os.path.join(R, 'src', 'data', 'teinte.ts'), 'w', encoding='utf-8', newline='\n').write(teinte_ts)

# ── 3. le dessin propre à chaque site (nœuds satori) ─────────────────────
DESSINS = {
  'muret': """/** L'Éole : un seul bus, de la gare de Muret à la rue du club. */
const dessin = () =>
  h(
    'div',
    { style: { position: 'relative', width: 380, height: 300, display: 'flex' } },
    h(
      'svg',
      { width: 380, height: 300, viewBox: '0 0 380 300' },
      h('path', { d: 'M 40 150 H 340', stroke: T.trait, strokeWidth: 2, fill: 'none' }),
      h('path', { d: 'M 40 150 H 340', stroke: T.signalTexte, strokeWidth: 4, fill: 'none' }),
      h('rect', { x: 28, y: 138, width: 24, height: 24, rx: 3, fill: T.encre }),
      h('circle', { cx: 120, cy: 150, r: 6, fill: T.papier, stroke: T.signalTexte, strokeWidth: 3 }),
      h('circle', { cx: 200, cy: 150, r: 6, fill: T.papier, stroke: T.signalTexte, strokeWidth: 3 }),
      h('circle', { cx: 280, cy: 150, r: 6, fill: T.papier, stroke: T.signalTexte, strokeWidth: 3 }),
      h('circle', { cx: 340, cy: 150, r: 18, fill: 'none', stroke: T.signalTexte, strokeWidth: 2.5 }),
      h('circle', { cx: 340, cy: 150, r: 8, fill: T.signalTexte })
    ),
    etiquette(`${SITE.ville.toUpperCase()} · GARE`, 0, 176, 'flex-start', T.encre),
    pastille(CODES, 190, 105),
    etiquette(ARRIVEE.arret.toUpperCase(), 190, 176, 'flex-end', T.encre),
    etiquette(CLUB.adresse.split(',')[0].toUpperCase(), 190, 196, 'flex-end', T.graphite, 12)
  );""",
  'cugnaux': """/** La limite : Cugnaux touche Portet, le club est de l'autre côté du trait. */
const dessin = () =>
  h(
    'div',
    { style: { position: 'relative', width: 380, height: 300, display: 'flex' } },
    h(
      'svg',
      { width: 380, height: 300, viewBox: '0 0 380 300' },
      h('path', { d: 'M 40 250 L 340 50', stroke: T.signalTexte, strokeWidth: 3, strokeDasharray: '14 8', fill: 'none' }),
      h('path', { d: 'M 60 270 L 360 70', stroke: T.trait, strokeWidth: 1.5, fill: 'none' }),
      h('path', { d: 'M 20 230 L 320 30', stroke: T.trait, strokeWidth: 1.5, fill: 'none' }),
      h('rect', { x: 178, y: 138, width: 24, height: 24, fill: T.papier, stroke: T.encre, strokeWidth: 2, transform: 'rotate(45 190 150)' }),
      h('circle', { cx: 100, cy: 100, r: 9, fill: T.encre }),
      h('circle', { cx: 280, cy: 210, r: 18, fill: 'none', stroke: T.signalTexte, strokeWidth: 2.5 }),
      h('circle', { cx: 280, cy: 210, r: 8, fill: T.signalTexte })
    ),
    etiquette(SITE.ville.toUpperCase(), 10, 62, 'flex-start', T.encre),
    etiquette('LA LIMITE', 200, 176, 'flex-start', T.graphite, 12),
    etiquette(CLUB.ville.toUpperCase(), 190, 238, 'flex-end', T.encre),
    pastille(CODES, 95, 250)
  );""",
  'labege': """/** Le terminus : trois lignes finissent au même endroit, l'octogone du club. */
const dessin = () =>
  h(
    'div',
    { style: { position: 'relative', width: 380, height: 300, display: 'flex' } },
    h(
      'svg',
      { width: 380, height: 300, viewBox: '0 0 380 300' },
      h('path', { d: 'M 40 60 L 300 150', stroke: T.signalTexte, strokeWidth: 4, fill: 'none' }),
      h('path', { d: 'M 40 150 L 300 150', stroke: T.signalTexte, strokeWidth: 4, fill: 'none' }),
      h('path', { d: 'M 40 240 L 300 150', stroke: T.signalTexte, strokeWidth: 4, fill: 'none' }),
      h('circle', { cx: 40, cy: 60, r: 8, fill: T.encre }),
      h('circle', { cx: 40, cy: 150, r: 8, fill: T.encre }),
      h('circle', { cx: 40, cy: 240, r: 8, fill: T.encre }),
      h('polygon', { points: '300,124 318,132 326,150 318,168 300,176 282,168 274,150 282,132', fill: T.papier, stroke: T.signalTexte, strokeWidth: 3 }),
      h('circle', { cx: 300, cy: 150, r: 7, fill: T.signalTexte }),
      h('path', { d: 'M 340 128 V 172', stroke: T.encre, strokeWidth: 4, fill: 'none' })
    ),
    etiquette(SITE.ville.toUpperCase(), 0, 30, 'flex-start', T.encre),
    pastille(LIGNES[0] ?? CODES, 150, 105),
    pastille(LIGNES[1] ?? '', 130, 150),
    pastille(LIGNES[2] ?? '', 150, 195),
    etiquette(CLUB.nomCourt.toUpperCase(), 150, 196, 'flex-end', T.encre),
    etiquette('TERMINUS', 150, 216, 'flex-end', T.graphite, 12)
  );""",
  'lunion': """/** Le plan de la salle : trois espaces de 400 m², une seule adresse. */
const dessin = () =>
  h(
    'div',
    { style: { position: 'relative', width: 380, height: 300, display: 'flex' } },
    h(
      'svg',
      { width: 380, height: 300, viewBox: '0 0 380 300' },
      h('rect', { x: 30, y: 90, width: 100, height: 120, fill: T.papierVif, stroke: T.encre, strokeWidth: 2.5 }),
      h('rect', { x: 140, y: 90, width: 100, height: 120, fill: T.papierVif, stroke: T.encre, strokeWidth: 2.5 }),
      h('rect', { x: 250, y: 90, width: 100, height: 120, fill: T.papierVif, stroke: T.encre, strokeWidth: 2.5 }),
      h('rect', { x: 52, y: 118, width: 56, height: 56, fill: 'none', stroke: T.signalTexte, strokeWidth: 3 }),
      h('rect', { x: 162, y: 118, width: 56, height: 56, rx: 28, fill: 'none', stroke: T.signalTexte, strokeWidth: 3 }),
      h('polygon', { points: '300,116 322,125 330,150 322,175 300,184 278,175 270,150 278,125', fill: 'none', stroke: T.signalTexte, strokeWidth: 3 }),
      h('path', { d: 'M 30 232 H 350', stroke: T.trait, strokeWidth: 2, fill: 'none' })
    ),
    etiquette('BOXE', 30, 60, 'flex-start', T.graphite, 12),
    etiquette('FITNESS', 140, 60, 'flex-start', T.graphite, 12),
    etiquette('MMA & SOL', 250, 60, 'flex-start', T.graphite, 12),
    etiquette('1 200 M²', 30, 244, 'flex-start', T.encre),
    etiquette('3 ESPACES DE 400 M²', 160, 246, 'flex-end', T.graphite, 12)
  );""",
  'castelginest': """/** La ligne 60 : six arrêts dans la commune, le métro, puis le 59 jusqu'au 388. */
const dessin = () =>
  h(
    'div',
    { style: { position: 'relative', width: 380, height: 300, display: 'flex' } },
    h(
      'svg',
      { width: 380, height: 300, viewBox: '0 0 380 300' },
      h('path', { d: 'M 30 150 H 200', stroke: T.signalTexte, strokeWidth: 4, fill: 'none' }),
      h('path', { d: 'M 200 150 H 250', stroke: T.encre, strokeWidth: 6, fill: 'none' }),
      h('path', { d: 'M 250 150 H 340', stroke: T.signalTexte, strokeWidth: 4, fill: 'none' }),
      ...[40, 70, 100, 130, 160, 190].map((x) => h('circle', { cx: x, cy: 150, r: 5, fill: T.papier, stroke: T.signalTexte, strokeWidth: 3 })),
      h('rect', { x: 191, y: 141, width: 18, height: 18, fill: T.papier, stroke: T.encre, strokeWidth: 2.5, transform: 'rotate(45 200 150)' }),
      h('rect', { x: 241, y: 141, width: 18, height: 18, fill: T.papier, stroke: T.encre, strokeWidth: 2.5, transform: 'rotate(45 250 150)' }),
      h('circle', { cx: 340, cy: 150, r: 18, fill: 'none', stroke: T.signalTexte, strokeWidth: 2.5 }),
      h('circle', { cx: 340, cy: 150, r: 8, fill: T.signalTexte })
    ),
    etiquette(SITE.ville.toUpperCase(), 0, 176, 'flex-start', T.encre),
    etiquette('SIX ARRÊTS', 0, 196, 'flex-start', T.graphite, 12),
    pastille(CODES, 190, 105),
    etiquette(ARRIVEE.arret.toUpperCase(), 170, 176, 'flex-end', T.encre, 13),
    etiquette(`AU ${CLUB.adresse.split(' ')[0]}`, 190, 196, 'flex-end', T.graphite, 12)
  );""",
}

FAVICONS = {
  'muret': """<rect width="32" height="32" rx="7" fill="{encre}"/>
  <path d="M6 16h20" fill="none" stroke="{signal}" stroke-width="2.4" stroke-linecap="round"/>
  <rect x="4" y="13.5" width="5" height="5" rx="1" fill="{papier}"/>
  <circle cx="24" cy="16" r="4.2" fill="none" stroke="{clair}" stroke-width="1.8"/>
  <circle cx="24" cy="16" r="1.9" fill="{clair}"/>""",
  'cugnaux': """<rect width="32" height="32" rx="7" fill="{encre}"/>
  <path d="M5 26L27 6" fill="none" stroke="{signal}" stroke-width="2.2" stroke-dasharray="4 2.5" stroke-linecap="round"/>
  <rect x="13.2" y="13.2" width="5.6" height="5.6" fill="{papier}" transform="rotate(45 16 16)"/>
  <circle cx="23" cy="22" r="3.2" fill="{clair}"/>""",
  'labege': """<rect width="32" height="32" rx="7" fill="{encre}"/>
  <path d="M5 8l16 8M5 16h16M5 24l16-8" fill="none" stroke="{signal}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  <polygon points="21,11.5 24.5,13 26,16.5 24.5,20 21,21.5 17.5,20 16,16.5 17.5,13" fill="{clair}"/>
  <path d="M28.5 12v9" stroke="{papier}" stroke-width="2" stroke-linecap="round"/>""",
  'lunion': """<rect width="32" height="32" rx="7" fill="{encre}"/>
  <rect x="4.5" y="10" width="6.5" height="12" fill="none" stroke="{signal}" stroke-width="1.8"/>
  <rect x="12.75" y="10" width="6.5" height="12" fill="none" stroke="{signal}" stroke-width="1.8"/>
  <rect x="21" y="10" width="6.5" height="12" fill="none" stroke="{signal}" stroke-width="1.8"/>
  <circle cx="24.25" cy="16" r="2" fill="{clair}"/>""",
  'castelginest': """<rect width="32" height="32" rx="7" fill="{encre}"/>
  <path d="M4 16h24" fill="none" stroke="{signal}" stroke-width="2.2" stroke-linecap="round"/>
  <circle cx="7" cy="16" r="1.4" fill="{papier}"/><circle cx="11" cy="16" r="1.4" fill="{papier}"/><circle cx="15" cy="16" r="1.4" fill="{papier}"/>
  <rect x="18.5" y="14.5" width="3" height="3" fill="{papier}" transform="rotate(45 20 16)"/>
  <circle cx="26" cy="16" r="3" fill="{clair}"/>""",
}

assert site in DESSINS and site in FAVICONS, site

# ── 4. l'endpoint OG, depuis le gabarit de Tournefeuille ─────────────────
gabarit = io.open(os.path.join(REF, 'src', 'pages', 'og', '[page].png.ts'), encoding='utf-8').read()
tete, corps = gabarit.split("/** L'aiguillage, réduit", 1)
corps = "/** " + corps  # (non utilisé : on remplace tout le dessin)
endpoint = tete
endpoint = endpoint.replace("import { SITE, CLUBS } from '../../data/verite';", "import { SITE, DESTINATION } from '../../data/verite';")
endpoint = endpoint.replace("import { itineraireDuClub } from '../../data/transports';", "import { ITINERAIRES, MEILLEUR, ARRIVEE } from '../../data/transports';")
endpoint = endpoint.replace("""const [SC, PT] = CLUBS;
const codes = (id: (typeof CLUBS)[number]['id']) =>
  itineraireDuClub(id)?.etapes.map((e) => e.code).join(' → ') ?? '';
""", """const CLUB = DESTINATION;
/** Les codes du meilleur trajet, dans l'ordre : « 117 Express », « 60 → B → 59 »… */
const CODES = MEILLEUR.etapes.map((e) => e.code).join(' → ');
/** La première ligne de chaque itinéraire du registre, pour les dessins à plusieurs branches. */
const LIGNES = ITINERAIRES.map((it) => it.etapes[0]?.code ?? '');
""")
endpoint = endpoint.replace(" * ville, les deux clubs et les lignes qui y mènent.", " * ville, le club et les lignes qui y mènent.")
# le reste du gabarit après le dessin : les helpers et GET
reste = gabarit.split("function etiquette(", 1)[1]
reste = "function etiquette(" + reste
# la pastille vit entre le dessin et etiquette dans le gabarit : on la reprend
pastille = "function pastille(" + gabarit.split("function pastille(", 1)[1].split("function etiquette(", 1)[0]
reste = pastille + chr(10) + reste
reste = reste.replace("      aiguillage()\n", "      dessin()\n")
reste = reste.replace("""      h(
        'div',
        { style: { display: 'flex', flexDirection: 'column', gap: 6, flexShrink: 1 } },
        ...CLUBS.map((c) =>
          h(
            'div',
            { style: { display: 'flex', gap: 12 } },
            h('span', { style: { color: T.encre, fontWeight: 700 } }, c.nomCourt.toUpperCase()),
            h('span', {}, c.adresse)
          )
        )
      ),""", """      h(
        'div',
        { style: { display: 'flex', flexDirection: 'column', gap: 6, flexShrink: 1 } },
        h(
          'div',
          { style: { display: 'flex', gap: 12 } },
          h('span', { style: { color: T.encre, fontWeight: 700 } }, CLUB.nom.toUpperCase()),
          h('span', {}, CLUB.adresse)
        ),
        h(
          'div',
          { style: { display: 'flex', gap: 12 } },
          h('span', { style: { color: T.encre, fontWeight: 700 } }, `DEPUIS ${SITE.ville.toUpperCase()}`),
          h('span', {}, `${CODES} · ${ARRIVEE.arret}`)
        )
      ),""")
assert "dessin()" in reste and "CLUB.nom" in reste, 'gabarit inattendu'
endpoint = endpoint + DESSINS[site] + "\n\n" + reste
os.makedirs(os.path.join(R, 'src', 'pages', 'og'), exist_ok=True)
io.open(os.path.join(R, 'src', 'pages', 'og', '[page].png.ts'), 'w', encoding='utf-8', newline='\n').write(endpoint)

# ── 5. le favicon ────────────────────────────────────────────────────────
clair = T['signal']
fav = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  {FAVICONS[site].format(encre=T['encre'], signal=T['signal'], papier=T['papier'], clair=clair)}
</svg>
"""
io.open(os.path.join(R, 'public', 'favicon.svg'), 'w', encoding='utf-8', newline='\n').write(fav)

# ── 6. Base.astro ────────────────────────────────────────────────────────
pb = os.path.join(R, 'src', 'layouts', 'Base.astro')
b = io.open(pb, encoding='utf-8').read()
rep = [
  ("const og = new URL(`/photos/${ogPhoto}-1440.jpg`, SITE.origine).href;",
   "/** La vignette de partage : composée pour cette page au build (voir pages/og/). */\nconst og = new URL(`/og/${r.id}.png`, SITE.origine).href;\n/** La photo de la page, pour le JSON-LD. */\nconst photo = new URL(`/photos/${ogPhoto}-1440.jpg`, SITE.origine).href;"),
  ("""    <meta property="og:image" content={og} />
    <meta name="twitter:card" content="summary_large_image" />

    <meta name="theme-color" content="#f3efe6" />""",
   """    <meta property="og:image" content={og} />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content={r.titre} />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:image" content={og} />

    <meta name="theme-color" content={TEINTE.papier} />"""),
  ("primaryImageOfPage: og,", "primaryImageOfPage: photo,"),
]
for o, n in rep:
    if n in b:
        continue  # déjà branché : le générateur peut se relancer sans casser
    assert o in b, ('Base.astro', o[:40])
    b = b.replace(o, n)
if "from '../data/teinte'" not in b:
    b = b.replace("import { ROLES", "import { TEINTE } from '../data/teinte';\nimport { ROLES", 1)
    assert "from '../data/teinte'" in b
io.open(pb, 'w', encoding='utf-8', newline='\n').write(b)
print(f'{site} : polices, teinte.ts, og/[page].png.ts, favicon.svg, Base.astro — équipé')
