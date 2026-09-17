# -*- coding: utf-8 -*-
"""
Portet, 17/09 — la page /club-de-boxe-portet/ (générée par
scripts/generate-club.mjs). Ce script l'INSCRIT partout et lui donne ses liens
entrants — uniquement des ajouts, aucun texte existant réécrit :
  1. package.json          — le générateur tourne après generate-coachs ;
  2. vite.config.ts        — l'entrée de build ;
  3. sitemap-images.mjs    — la page au plan du site (0.8) ;
  4. generate-llms.mjs     — la ligne dans « Pages du site » ;
  5. src/data.ts (NAV)     — pied de page + tiroir (top: false, pas la barre) ;
  6. /about/               — un lien vers l'histoire du club ;
  7. generate-club.mjs     — l'ancre du réseau (#network-grid, la vraie) ;
  8. og_portet_pages.mjs   — la vignette propre + filtre par slug.
CRLF conservés ; chaque remplacement vérifie son compte ; rejouable.
"""
import io, os, sys
sys.stdout.reconfigure(encoding='utf-8')
BC = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center')
P = os.path.join(BC, 'Portet', 'boxing-center-portet')
OUTILS = os.path.join(BC, 'Deployment', 'boxing-center-colomiers', 'scripts', 'referencement')


def lire(p):
    return io.open(p, encoding='utf-8', newline='').read()


def ecrire(p, t):
    io.open(p, 'w', encoding='utf-8', newline='').write(t)


def rem(t, avant, apres, nom):
    for a, b in ((avant, apres), (avant.replace('\n', '\r\n'), apres.replace('\n', '\r\n'))):
        if t.count(a) == 1 and b not in t:
            return t.replace(a, b)
    if apres in t or apres.replace('\n', '\r\n') in t:
        print('  (déjà fait :', nom + ')')
        return t
    raise AssertionError(f'{nom} : motif introuvable ou multiple — {avant[:70]!r}')


def patch(p, *ops):
    t = lire(p)
    for op in ops:
        t = op(t)
    ecrire(p, t)
    print('  ok', os.path.relpath(p, BC))


patch(os.path.join(P, 'package.json'), lambda t: rem(t,
      'node scripts/generate-coachs.mjs && node scripts/optimize-images.mjs',
      'node scripts/generate-coachs.mjs && node scripts/generate-club.mjs && node scripts/optimize-images.mjs', 'build'))

patch(os.path.join(P, 'vite.config.ts'), lambda t: rem(t,
      '        about: page("about/index.html"),\n',
      '        about: page("about/index.html"),\n        club: page("club-de-boxe-portet/index.html"),\n', 'entrée vite'))

patch(os.path.join(P, 'scripts', 'sitemap-images.mjs'), lambda t: rem(t,
      '  { url: "/coachs/", freq: "monthly", prio: "0.8", images: equipe },\n',
      '  // La page du club pour « club de boxe portet » : son histoire, et des liens vers tout le site.\n'
      '  { url: "/club-de-boxe-portet/", freq: "monthly", prio: "0.8", images: [\n'
      '      img("/img/gym-21.jpg", `Le ring du club — ${LIEU}`, "Le ring de boxe anglaise du Boxing Center Portet, 600 m² dédiés aux sports de combat.")] },\n'
      '  { url: "/coachs/", freq: "monthly", prio: "0.8", images: equipe },\n', 'plan du site'))

patch(os.path.join(P, 'scripts', 'generate-llms.mjs'), lambda t: rem(t,
      '- Le club : ${SITE}/salles/\n',
      '- Le club : ${SITE}/salles/\n- L’histoire du club de boxe de Portet-sur-Garonne (600 m², depuis 2016) : ${SITE}/club-de-boxe-portet/\n', 'llms'))

patch(os.path.join(P, 'src', 'data.ts'), lambda t: rem(t,
      '  { href: "/salles/#network-grid", label: "Nos clubs", top: false },\n',
      '  { href: "/salles/#network-grid", label: "Nos clubs", top: false },\n'
      '  /* 17/09 : la page du club pour « club de boxe portet » — pied de page et tiroir, pas la barre */\n'
      '  { href: "/club-de-boxe-portet/", label: "Le club, son histoire", top: false },\n', 'NAV'))

patch(os.path.join(P, 'about', 'index.html'), lambda t: rem(t,
      '      <h2 class="display" style="font-size:clamp(1.3rem,3vw,1.8rem);margin-top:2.2rem">Le réseau</h2>',
      '      <p><a href="/club-de-boxe-portet/">L’histoire du club de boxe de Portet-sur-Garonne</a>, ouvert en 2016.</p>\n'
      '      <h2 class="display" style="font-size:clamp(1.3rem,3vw,1.8rem);margin-top:2.2rem">Le réseau</h2>', 'about'))

patch(os.path.join(P, 'scripts', 'generate-club.mjs'), lambda t: rem(t,
      '<a href="/salles/#reseau">Les cinq clubs</a>', '<a href="/salles/#network-grid">Les cinq clubs</a>', 'ancre réseau'))

patch(os.path.join(OUTILS, 'og_portet_pages.mjs'),
      lambda t: rem(t,
      '  { slug: "privacy", photo: "img/gym-18.jpg",',
      '  { slug: "club-de-boxe-portet", photo: "img/gym-01.jpg", sur: "LE CLUB DE BOXE · PORTET-SUR-GARONNE", titre: "600 m² depuis 2016", puces: ["Ring · cage · tatamis", "9 disciplines"] },\n'
      '  { slug: "privacy", photo: "img/gym-18.jpg",', 'vignette'),
      lambda t: rem(t,
      'for (const p of PAGES) {\n',
      '/* « node og_portet_pages.mjs club-de-boxe-portet » ne refait que cette vignette */\n'
      'const SEULES = process.argv.slice(2);\n'
      'for (const p of PAGES.filter((q) => !SEULES.length || SEULES.includes(q.slug))) {\n', 'filtre'))
print('page du club de Portet : inscrite')
