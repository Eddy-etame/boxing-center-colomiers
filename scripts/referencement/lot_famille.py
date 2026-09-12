# -*- coding: utf-8 -*-
"""
Le lot de famille, appliqué à UN site : python lot_famille.py <site>

1. la vignette photo (og/[page].jpg.ts + data/vignettes.ts), l'ancienne carte PNG retirée ;
2. les favicons carrés (public/), le layout qui les annonce ;
3. le layout : max-image-preview:large sur les pages indexables, l'image carrée
   dans le JSON-LD, l'og:image en JPEG ;
4. robots.txt : les moteurs de réponse nommés un par un, aucune phrase négative ;
5. IndexNow : le vrai domaine, une clé propre, le fichier de clé publié ;
6. noindex sur les pages juridiques et sur les pages dupliquées d'un site à l'autre.

Chaque remplacement qui ne trouve pas sa cible fait échouer le script : rien en silence.
"""
import io, os, re, sys, secrets, shutil, subprocess
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"C:\Users\Mommy Jayce\Desktop\Boxing Center\Deployment"
ICI = os.path.dirname(os.path.abspath(__file__))
site = sys.argv[1]
R = os.path.join(BASE, f'boxing-center-{site}')
COLOMIERS = site == 'colomiers'

def lire(rel): return io.open(os.path.join(R, rel), encoding='utf-8').read()
def ecrire(rel, t): io.open(os.path.join(R, rel), 'w', encoding='utf-8', newline='\n').write(t)
def remplacer(rel, paires):
    t = lire(rel)
    for o, n in paires:
        if n in t and o not in t: continue
        if o not in t: raise SystemExit(f'✗ {rel} : cible introuvable « {o[:70]} »')
        t = t.replace(o, n)
    ecrire(rel, t)

CODES = {'colomiers': 'CO', 'muret': 'MU', 'cugnaux': 'CU', 'tournefeuille': 'TO', 'labege': 'LA', 'lunion': 'LU', 'castelginest': 'CA'}
VILLES = {'colomiers': 'Colomiers', 'muret': 'Muret', 'cugnaux': 'Cugnaux', 'tournefeuille': 'Tournefeuille', 'labege': 'Labège', 'lunion': 'L’Union', 'castelginest': 'Castelginest'}

# ── 1. la vignette ────────────────────────────────────────────────────────
a_communes = os.path.exists(os.path.join(R, 'src/data/communes.ts'))
SUJETS = """const SUJETS: Record<string, string> = {
  accueil: 'Club de boxe · MMA',
  'boxe-anglaise': 'Boxe anglaise',
  mma: 'Club MMA',
  'kick-boxing': 'Kick-boxing',
  'boxe-pieds-poings': 'Boxe pieds-poings',
  'boxe-thai': 'Boxe thaï · K1',
  'boxe-enfants': 'Boxe enfant',
  'boxing-fitness': 'Boxing fitness',
  'preparation-physique': 'Préparation physique',
  'premiere-seance': 'Première séance',
  'ta-seance': 'Ta séance',
  'quel-club': 'Quel club',
  transports: 'Y aller en bus',
  contact: 'Contact',
  plannings: 'Plannings',
  tarifs: 'Tarifs',
};
const DEPUIS = new Set(['transports', 'contact', 'quel-club', 'ta-seance']);

/** « BOXE ANGLAISE · PRÈS DE », « Y ALLER EN BUS · DEPUIS » : la ligne au-dessus du lieu. */
export function etiquetteDeLaRoute(id: string): string {
  return `${SUJETS[id] ?? 'Club de boxe · MMA'} · ${DEPUIS.has(id) ? 'depuis' : 'près de'}`;
}"""
if COLOMIERS:
    vignettes = f"""/**
 * CE QUE MONTRE LA VIGNETTE DE CHAQUE PAGE — la photo de la page, le sujet,
 * le lieu, les clubs et la ligne. Lu par pages/og/ (l'image) et par le layout
 * (le JSON-LD) : l'image annoncée et l'image servie sont la même.
 */
import {{ CLUBS }} from './verite';
import {{ CONTEXTE_GEO }} from './mots-cles';
import {{ CONTENUS }} from './contenus';
import {{ MEILLEUR }} from './transports';

/** Colomiers est le point de départ, jamais une adresse de club. */
export const VILLE_SITE: string = CONTEXTE_GEO.ville;
export const CLUB_VIGNETTE: string = CLUBS.map((c) => c.nomCourt).join(' · ');
export const LIGNE_VIGNETTE: string = MEILLEUR.etapes.map((e) => e.code).join(' → ');

{SUJETS}

export function photoDeLaRoute(id: string): string {{
  const c = CONTENUS.find((x) => x.id === id);
  if (c) return c.photoHero;
  if (id === 'premiere-seance' || id === 'contact') return 'premiere-seance-boxe-colomiers';
  if (id === 'transports') return 'ambiance-club-boxe-colomiers';
  if (id === 'plannings' || id === 'tarifs') return 'salle-boxing-center-colomiers';
  return 'club-boxe-colomiers-boxing-center';
}}

export const lieuDeLaRoute = (_id: string): string => VILLE_SITE;
"""
else:
    club = "CLUBS.map((c) => c.nomCourt).join(' · ')" if site == 'tournefeuille' else 'DESTINATION.nom'
    imp_verite = "import { SITE, CLUBS } from './verite';" if site == 'tournefeuille' else "import { SITE, DESTINATION } from './verite';"
    vignettes = f"""/**
 * CE QUE MONTRE LA VIGNETTE DE CHAQUE PAGE — la photo de la page, le sujet,
 * le lieu, le club et la ligne. Lu par pages/og/ (l'image) et par le layout
 * (le JSON-LD) : l'image annoncée et l'image servie sont la même.
 */
{imp_verite}
import {{ ROLES }} from './medias';
import {{ CONTENUS }} from './contenus';
{"import { COMMUNES } from './communes';" if a_communes else ''}
import {{ MEILLEUR }} from './transports';

export const VILLE_SITE: string = SITE.ville;
export const CLUB_VIGNETTE: string = {club};
export const LIGNE_VIGNETTE: string = MEILLEUR.etapes.map((e) => e.code).join(' → ');

{SUJETS}

export function photoDeLaRoute(id: string): string {{
  const c = CONTENUS.find((x) => x.id === id);
  if (c) return c.photoHero;
{"  const m = COMMUNES.find((x) => x.id === id);" + chr(10) + "  if (m) return m.photo;" if a_communes else ''}
  if (id === 'contact' || id === 'premiere-seance') return ROLES.premiereSeance;
  if (id === 'quel-club') return ROLES.calme;
  if (id === 'transports') return ROLES.effort;
  return ROLES.hero;
}}

/** Sur une page de commune, le lieu est la commune ; partout ailleurs, la ville du site. */
export function lieuDeLaRoute(id: string): string {{
  {"return COMMUNES.find((x) => x.id === id)?.nom ?? VILLE_SITE;" if a_communes else "return VILLE_SITE;"}
}}
"""
ecrire('src/data/vignettes.ts', re.sub(r'\n{3,}', '\n\n', vignettes))
os.makedirs(os.path.join(R, 'src/pages/og'), exist_ok=True)
shutil.copyfile(os.path.join(ICI, 'og_gabarit.ts'), os.path.join(R, 'src/pages/og/[page].jpg.ts'))
ancienne = os.path.join(R, 'src/pages/og/[page].png.ts')
if os.path.exists(ancienne): os.remove(ancienne)

# ── 2. les favicons ───────────────────────────────────────────────────────
teinte = lire('src/data/teinte.ts')
def jeton(nom): return re.search(nom + r": '([^']+)'", teinte).group(1)
def lum(hx):
    n = int(hx.lstrip('#')[:6], 16); rgb = [(n >> 16) & 255, (n >> 8) & 255, n & 255]
    c = [v / 255 for v in rgb]; c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
encre, papier, signal = jeton('encre'), jeton('papier'), jeton('signal')
sombre, clair = (encre, papier) if lum(encre) < lum(papier) else (papier, encre)
nom_site = re.search(r"nom: '([^']+)'", lire('src/data/verite.ts')).group(1)
os.makedirs(os.path.join(R, 'scripts'), exist_ok=True)
shutil.copyfile(os.path.join(ICI, 'favicons.mjs'), os.path.join(R, 'scripts', 'favicons.mjs'))
subprocess.run(['node', 'scripts/favicons.mjs', CODES[site], sombre, signal, clair, nom_site, f'Boxing Center {VILLES[site]}'],
               cwd=R, check=True)

# ── 3. le layout ──────────────────────────────────────────────────────────
base = 'src/layouts/Base.astro'
b = lire(base)
b = b.replace("/** La vignette de partage : composée pour cette page au build (voir pages/og/). */\nconst og = new URL(`/og/${r.id}.png`, SITE.origine).href;",
              "/** Les vignettes de la page, composées au build (voir pages/og/) : paysage pour les partages, carrée pour Google. */\nconst og = new URL(`/og/${r.id}.jpg`, SITE.origine).href;\nconst ogCarre = new URL(`/og/${r.id}-carre.jpg`, SITE.origine).href;")
if 'ogCarre' not in b: raise SystemExit('✗ Base.astro : ligne og introuvable')
b = re.sub(r"      !r\.index && <meta name=\"robots\" content=\"noindex, follow\" />",
           "      <meta name=\"robots\" content={r.index ? 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1' : 'noindex, follow'} />", b)
if 'max-image-preview:large' not in b: raise SystemExit('✗ Base.astro : meta robots introuvable')
if 'og:image:type' not in b:
  b = b.replace('    <meta property="og:image:alt" content={r.titre} />',
              '    <meta property="og:image:type" content="image/jpeg" />\n    <meta property="og:image:alt" content={r.titre} />\n    <link rel="image_src" href={ogCarre} />')
anciens = ['    <link rel="icon" href="/favicon.svg" type="image/svg+xml" />\n', '    <link rel="icon" href="/logo.png" sizes="any" />\n']
for a in anciens:
    if a not in b and 'favicon-192.png' not in b: raise SystemExit(f'✗ Base.astro : {a.strip()} introuvable')
    b = b.replace(a, '')
if 'favicon-192.png' not in b:
    ICONES = ('    <link rel="icon" href="/favicon.ico" sizes="48x48" />\n'
              '    <link rel="icon" href="/favicon-96.png" type="image/png" sizes="96x96" />\n'
              '    <link rel="icon" href="/favicon-192.png" type="image/png" sizes="192x192" />\n'
              '    <link rel="apple-touch-icon" href="/apple-touch-icon.png" />\n'
              '    <link rel="manifest" href="/site.webmanifest" />\n')
    b = b.replace('    <meta name="theme-color"', ICONES + '    <meta name="theme-color"', 1)
b = b.replace("      primaryImageOfPage: photo,",
              "      primaryImageOfPage: { '@type': 'ImageObject', url: ogCarre, width: 1200, height: 1200 },\n      image: [ogCarre, og, photo],")
for attendu in ['favicon-192.png', "image: [ogCarre, og, photo]", 'image_src']:
    if attendu not in b: raise SystemExit(f'✗ Base.astro : {attendu} absent après patch')
ecrire(base, b)

# ── 4. robots.txt ─────────────────────────────────────────────────────────
rob = 'src/pages/robots.txt.ts'
t = lire(rob)
debut = t.index('    : new Response(\n    `') + len('    : new Response(\n    `')
fin = t.index('`,\n    { headers:', debut)
AGENTS = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot', 'Claude-User', 'PerplexityBot',
          'Perplexity-User', 'Google-Extended', 'Applebot', 'Applebot-Extended', 'Bingbot', 'DuckAssistBot',
          'MistralAI-User', 'Meta-ExternalAgent', 'Amazonbot', 'CCBot']
corps = ("User-agent: *\nAllow: /\nDisallow: /api/\n\n"
         "# Moteurs de réponse et assistants : ce site leur est ouvert en entier.\n"
         "# Les faits à citer (adresse du club, lignes de bus, disciplines publiées) sont dans /llms.txt.\n"
         + ''.join(f'User-agent: {a}\n' for a in AGENTS) + "Allow: /\nDisallow: /api/\n\n"
         "Sitemap: ${SITE.origine}/sitemap.xml\n")
ecrire(rob, t[:debut] + corps + t[fin:])

# ── 5. IndexNow ───────────────────────────────────────────────────────────
inx = 'scripts/indexnow.mjs'
t = lire(inx)
origine = re.search(r"origine: '(https://[^']+)'", lire('src/data/verite.ts')).group(1)
hote = origine.replace('https://', '')
cle_existante = [f[:-4] for f in os.listdir(os.path.join(R, 'public')) if re.fullmatch(r'[0-9a-f]{32}\.txt', f)]
if cle_existante and (COLOMIERS or f"const HOTE = '{hote}';" in t): cle = cle_existante[0]
else:
    for f in cle_existante: os.remove(os.path.join(R, 'public', f + '.txt'))
    cle = secrets.token_hex(16)
t = re.sub(r"const HOTE = '[^']*';", f"const HOTE = '{hote}';", t)
t = re.sub(r"const CLE = '[^']*';", f"const CLE = '{cle}';", t)
ecrire(inx, t)
io.open(os.path.join(R, 'public', f'{cle}.txt'), 'w', encoding='utf-8', newline='').write(cle)

# ── 5 bis. le portail : un fichier statique n'est pas une page ─────────────
ver = 'scripts/verifier.mjs'
t = lire(ver)
t = t.replace("/\.[a-z0-9]{2,5}$/i.test(cible)", "/\.[a-z0-9]{2,12}$/i.test(cible)")
if '{2,12}' not in t: raise SystemExit('✗ verifier.mjs : règle des liens introuvable')
ecrire(ver, t)

# ── 6. noindex : juridique partout ; doublons inter-sites sur les satellites ─
rt = 'src/data/routes.ts'
t = lire(rt)
cibles = ['mentions-legales', 'confidentialite'] + ([] if COLOMIERS else ['ta-seance', 'contact', 'premiere-seance'])
fait = []
for rid in cibles:
    # Le motif ne franchit jamais la route suivante : il s'arrête au premier « id: ».
    m = re.search(r"(    id: '" + re.escape(rid) + r"',(?:(?!    id: ')[\s\S])*?\n    index: )(true|false),", t)
    if m and m.group(2) == 'true':
        t = t[:m.start()] + m.group(1) + 'false,' + t[m.end():]
        fait.append(rid)
ecrire(rt, t)
print(f'{site} : vignette photo · favicons {CODES[site]} · layout · robots · IndexNow {hote} ({cle[:6]}…) · noindex {fait}')
