# -*- coding: utf-8 -*-
"""
19/09 — Eddy a dit OUI : Portet et Ramonville lient les sites de proximité depuis
leur pied de page. C'est le levier d'indexation le plus fort : Colomiers, Cugnaux
et Castelginest n'ont AUCUNE page dans Google, et aucun site indexé ne les liait.
Castelginest et L'Union dépendent d'États-Unis (gelé) : seule une ligne « près de
chez toi » qui nomme les SEPT villes, sur les deux sites ouverts, leur donne un
lien entrant aujourd'hui.

Une ligne discrète au-dessus du copyright, dans le pied JS ET dans le pied cuit
pour les robots (les deux sites en ont un). Liens suivis (pas de nofollow : c'est
le même réseau), nouvel onglet. Une seule liste par site : src/proches.json
(Portet), PROCHES dans data.js (Ramonville). CRLF conservés ; rejouable.
"""
import io, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
BC = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center')
P = os.path.join(BC, 'Portet', 'boxing-center-portet')
R = os.path.join(BC, 'Deployment', 'bc-ramonville')
VILLES = [('Colomiers', 'colomiers'), ('Muret', 'muret'), ('Cugnaux', 'cugnaux'), ('Tournefeuille', 'tournefeuille'),
          ('Labège', 'labege'), ('L’Union', 'lunion'), ('Castelginest', 'castelginest')]
PROCHES = [{'ville': v, 'url': f'https://www.boxingcenter-{s}.fr/'} for v, s in VILLES]


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


# ── PORTET ─────────────────────────────────────────────────────────────────
ecrire(os.path.join(P, 'src', 'proches.json'), json.dumps(PROCHES, ensure_ascii=False, indent=2) + '\n')
print('  ok Portet src/proches.json')
LIGNE_TS = ('      <!-- LES SITES DE PROXIMITÉ (Eddy, 19/09 : oui) — le réseau, ville par ville. Liens suivis. -->\n'
            '      <p class="footer__proches">Boxing Center près de chez toi : ${PROCHES.map((p) => `<a href="${p.url}" target="_blank" rel="noopener">${p.ville}</a>`).join(" · ")}</p>\n')
patch(os.path.join(P, 'src', 'layout.ts'),
      lambda t: rem(t, 'import { NAV, SITE, PREVIEW } from "./data";\n',
                    'import { NAV, SITE, PREVIEW } from "./data";\nimport PROCHES from "./proches.json";\n', 'import proches'),
      lambda t: rem(t, '      <div class="footer__bottom">\n        <span>© ${new Date().getFullYear()} ${SITE.name}',
                    LIGNE_TS + '      <div class="footer__bottom">\n        <span>© ${new Date().getFullYear()} ${SITE.name}', 'pied JS'))
patch(os.path.join(P, 'vite.config.ts'),
      lambda t: rem(t, '        const footerStatique = `<div id="site-footer">',
                    '        /* les sites de proximité, dans le pied CUIT aussi : c\'est lui que lisent les robots */\n'
                    '        const PROCHES: { ville: string; url: string }[] = JSON.parse(readFileSync(page("src/proches.json"), "utf8"));\n'
                    '        const footerStatique = `<div id="site-footer">', 'lecture proches'),
      lambda t: rem(t, '          <div class="footer__bottom"><span>© ${new Date().getFullYear()} ${site.name || "Boxing Center Portet"}</span></div>',
                    '          <p class="footer__proches">Boxing Center près de chez toi : ${PROCHES.map((p) => `<a href="${p.url}" rel="noopener">${p.ville}</a>`).join(" · ")}</p>\n'
                    '          <div class="footer__bottom"><span>© ${new Date().getFullYear()} ${site.name || "Boxing Center Portet"}</span></div>', 'pied cuit'))
patch(os.path.join(P, 'src', 'styles', 'main.css'),
      lambda t: t if '.footer__proches' in t else rem(t, '.footer__bottom { display: flex;',
                    '/* les sites de proximité : une ligne discrète au-dessus du copyright */\n'
                    '.footer__proches { margin-top: 2rem; font-family: var(--font-mono); font-size: .74rem; letter-spacing: .06em; line-height: 1.9; color: var(--muted); }\n'
                    '.footer__proches a { color: inherit; text-decoration: underline; text-underline-offset: .25em; text-decoration-thickness: 1px; transition: color .25s; }\n'
                    '.footer__proches a:hover { color: var(--accent); }\n'
                    '.footer__bottom { display: flex;', 'css proches'))

# ── RAMONVILLE ─────────────────────────────────────────────────────────────
pd = os.path.join(R, 'public', 'assets', 'js', 'data.js')
t = lire(pd)
if 'export const PROCHES' not in t:
    nl = '\r\n' if '\r\n' in t else '\n'
    bloc = ('', '/* LES SITES DE PROXIMITÉ du réseau (Eddy, 19/09 : oui) — liés depuis le pied de page,',
            '   dans site.js ET dans le HTML cuit par maillage.mjs. Liens suivis. */',
            'export const PROCHES = [') + tuple(f'  {{ ville: "{v}", url: "https://www.boxingcenter-{s}.fr/" }},' for v, s in VILLES) + ('];', '')
    ecrire(pd, t.rstrip('\r\n') + nl + nl.join(bloc))
    print('  ok Ramonville data.js (PROCHES)')
else:
    print('  (déjà fait : data.js)')
patch(os.path.join(R, 'public', 'assets', 'js', 'site.js'),
      lambda t: rem(t, 'import { NAV, LINKS, SALLE, SEASON_LABEL, NETWORK } from "./data.js?v=25";',
                    'import { NAV, LINKS, SALLE, SEASON_LABEL, NETWORK, PROCHES } from "./data.js?v=25";', 'import PROCHES'),
      lambda t: rem(t, '        <div class="footer__bottom">\n          <span>© ${new Date().getFullYear()} Boxing Center Ramonville.',
                    '        <p class="footer__reseau footer__proches">Boxing Center près de chez toi : ${(PROCHES || []).map((p) => `<a href="${p.url}" target="_blank" rel="noopener">${p.ville}</a>`).join(" · ")}</p>\n'
                    '        <div class="footer__bottom">\n          <span>© ${new Date().getFullYear()} Boxing Center Ramonville.', 'pied JS'))
patch(os.path.join(R, 'scripts', 'maillage.mjs'),
      lambda t: rem(t, 'const { LINKS, NETWORK, NAV } = await import(', 'const { LINKS, NETWORK, NAV, PROCHES } = await import(', 'import maillage'),
      lambda t: rem(t, '  `<a href="/privacy/">Confidentialité</a>` +\n  `</div></div></div></footer>`;',
                    '  `<a href="/privacy/">Confidentialité</a>` +\n  `</div></div>` +\n'
                    '  `<p class="footer__reseau footer__proches">Boxing Center près de chez toi : ` +\n'
                    '  (PROCHES || []).map((p) => `<a href="${p.url}" rel="noopener">${p.ville}</a>`).join(" · ") + `</p>` +\n'
                    '  `</div></footer>`;', 'pied cuit'))
pc = os.path.join(R, 'public', 'assets', 'css', 'base.css')
t = lire(pc)
if '.footer__proches' not in t:
    t = rem(t, '.footer__reseau { margin-top:', '.footer__proches { margin-top: .6rem !important; max-width: none !important; }\n'
            '.footer__proches a { color: inherit; text-decoration: underline; text-underline-offset: .25em; text-decoration-thickness: 1px; transition: color .25s; }\n'
            '.footer__proches a:hover { color: var(--accent); }\n.footer__reseau { margin-top:', 'css proches')
    ecrire(pc, t)
    print('  ok Ramonville base.css')
print('liens vers les sept sites de proximité : posés sur Portet et Ramonville')
