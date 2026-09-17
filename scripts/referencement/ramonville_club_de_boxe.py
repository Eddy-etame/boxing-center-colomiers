# -*- coding: utf-8 -*-
"""
Ramonville, 17/09 — la page /club-de-boxe-ramonville/ (Eddy : « une page par
mot-clé, l'histoire du club, beaucoup de liens internes »). Le générateur est
scripts/generer-club-de-boxe.mjs ; ce script l'INSCRIT partout où une page
doit l'être, et lui donne des liens entrants :
  1. package.json  — le générateur tourne avant astro build ;
  2. sitemap.mjs   — la page entre au plan du site (0.8) ;
  3. site.js       — colonne « La salle » du pied de page ;
  4. maillage.mjs  — le même lien, écrit en dur pour les robots sans JS ;
  5. /about/       — un lien vers l'histoire du club ;
  6. /nos-clubs/   — la carte « Vous êtes ici » mène à l'histoire du club ;
  7. discipline.css — le texte courant (.dp-prose) et la rangée de suite.
Aucun texte existant n'est réécrit : uniquement des ajouts. CRLF conservés.
"""
import io, os, sys
sys.stdout.reconfigure(encoding='utf-8')
R = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment', 'bc-ramonville')


def lire(p):
    return io.open(p, encoding='utf-8', newline='').read()


def ecrire(p, t):
    io.open(p, 'w', encoding='utf-8', newline='').write(t)


def rem(t, avant, apres, nom, n=1):
    for a, b in ((avant, apres), (avant.replace('\n', '\r\n'), apres.replace('\n', '\r\n'))):
        if t.count(a) == n:
            return t.replace(a, b)
    if apres in t or apres.replace('\n', '\r\n') in t:
        print('  (déjà fait :', nom + ')')
        return t
    raise AssertionError(f'{nom} : motif introuvable ou multiple pour {avant[:70]!r}')


def patch(rel, *ops):
    p = os.path.join(R, rel)
    t = lire(p)
    for op in ops:
        t = op(t)
    ecrire(p, t)
    print('  ok', rel)


patch('package.json', lambda t: rem(t,
      'node scripts/generer-nos-clubs.mjs && astro build',
      'node scripts/generer-nos-clubs.mjs && node scripts/generer-club-de-boxe.mjs && astro build', 'build'))

patch('scripts/sitemap.mjs', lambda t: rem(t,
      '  { chemin: "nos-clubs/", priorite: "0.6", freq: "monthly", imgs: [] },\n',
      '  { chemin: "nos-clubs/", priorite: "0.6", freq: "monthly", imgs: [] },\n'
      '  /* la page du club pour « club de boxe ramonville » : son histoire, et des liens vers tout le site */\n'
      '  { chemin: "club-de-boxe-ramonville/", priorite: "0.8", freq: "monthly", imgs: [I.plateau, I.anglaise, I.octogone] },\n', 'sitemap'))

patch('public/assets/js/site.js', lambda t: rem(t,
      'const cols = [{ h: "La salle", links: NAV.slice(1, 6) }, ',
      'const cols = [{ h: "La salle", links: [...NAV.slice(1, 6), { href: "/club-de-boxe-ramonville/", label: "Le club, son histoire" }] }, ', 'pied de page'))

patch('scripts/maillage.mjs', lambda t: rem(t,
      '  `<a href="/about/">À propos</a>` +\n',
      '  `<a href="/club-de-boxe-ramonville/">Le club de boxe de Ramonville, son histoire</a>` +\n  `<a href="/about/">À propos</a>` +\n', 'maillage'))

patch('src/pages/about/index.astro', lambda t: rem(t,
      '      <h2>Le réseau</h2>\n',
      '      <p><a href="/club-de-boxe-ramonville/">L’histoire du club de boxe de Ramonville</a>, ouvert en septembre 2019.</p>\n      <h2>Le réseau</h2>\n', 'about'))

patch('scripts/generer-nos-clubs.mjs', lambda t: rem(t,
      '<p class="net__adr">${e(n.adresse || "")}</p></article>`',
      '<p class="net__adr">${e(n.adresse || "")}</p><a class="net__go" href="/club-de-boxe-ramonville/">L’histoire du club</a></article>`', 'carte ici'))

p = os.path.join(R, 'public', 'assets', 'css', 'discipline.css')
t = lire(p)
if '.dp-prose' not in t:
    bloc = '''
/* LE TEXTE COURANT des pages d'histoire (/club-de-boxe-ramonville/, 17/09) :
   une colonne de lecture, des liens qui se voient, et la rangée de suite
   sous une grille de cartes. */
.dp-prose { max-width: 68ch; display: grid; gap: 1.15rem; font-size: var(--step-0); line-height: 1.75; color: var(--ink); }
.dp-prose a, .dp-suite > a:not(.btn) { color: var(--accent); text-decoration: underline; text-underline-offset: .2em; text-decoration-thickness: 1px; transition: color .25s; }
.dp-prose a:hover, .dp-suite > a:not(.btn):hover { color: #fff; }
.dp-suite { margin-top: 1.6rem; display: flex; flex-wrap: wrap; gap: .8rem; align-items: center; justify-content: center; }
.piege .dp-suite { margin-top: 1.2rem; }
'''
    nl = '\r\n' if '\r\n' in t else '\n'
    ecrire(p, t.rstrip('\r\n') + nl + bloc.replace('\n', nl))
    print('  ok discipline.css (+ .dp-prose, .dp-suite)')
else:
    print('  (déjà fait : discipline.css)')
print('page du club : inscrite')
