# -*- coding: utf-8 -*-
"""Ramonville, 19/09 : toute la carte d'un coach mène à sa page, chaque discipline
à la sienne. Aucun texte ne change : on relie les libellés existants.
Rejouable : chaque remplacement est compté, un fichier déjà patché est sauté."""
import io, sys

R = r"C:/Users/Mommy Jayce/Desktop/Boxing Center/Deployment/bc-ramonville/"


def patch(f, pairs, marque):
    p = R + f
    s = io.open(p, encoding="utf-8", newline="").read()
    if marque in s:
        print("déjà fait", f)
        return
    crlf = "\r\n" in s
    for a, b in pairs:
        if crlf:
            a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
        n = s.count(a)
        assert n == 1, (f, a[:70], n)
        s = s.replace(a, b)
    io.open(p, "w", encoding="utf-8", newline="").write(s)
    print("ok", f)


# A. L'accueil : la carte n'est plus une ancre (une ancre n'en contient pas d'autre).
patch("public/assets/js/home.js", [
    ('import { lienDiscipline } from "./disciplines-liens.js?v=1";',
     'import { lienDiscipline } from "./disciplines-liens.js?v=1";\nimport { roleHtml } from "./role-liens.js?v=1";'),
    ('return `<a class="staff__card ${c.pillar ? "is-pillar" : ""}" href="${lienCoach(c.name) || "/coachs/"}">',
     'return `<article class="staff__card carte-lien ${c.pillar ? "is-pillar" : ""}">'),
    ('        <b>${c.name}</b>\n        <span class="mono">${c.role}</span>',
     '        <b><a class="carte-lien__tout" href="${lienCoach(c.name) || "/coachs/"}">${c.name}</a></b>\n        <span class="mono">${roleHtml(c.role, c.name)}</span>'),
    ('        <span class="staff__go">${c.pillar', '        <span class="staff__go" aria-hidden="true">${c.pillar'),
    ('      </div>\n    </a>`;\n  }).join("");\n}', '      </div>\n    </article>`;\n  }).join("");\n}'),
], "role-liens.js")

# B. /coachs/ : la fiche entière, le rôle et les pastilles.
patch("src/pages/coachs/index.astro", [
    ('    import { lienCoach } from "/assets/js/coachs-liens.js?v=1";',
     '    import { lienCoach } from "/assets/js/coachs-liens.js?v=1";\n    import { roleHtml, pastilleHtml } from "/assets/js/role-liens.js?v=1";'),
    ('return `<article class="coach ${c.pillar ? "coach--pillar" : ""}">',
     'return `<article class="coach ${lienCoach(c.name) ? "carte-lien" : ""} ${c.pillar ? "coach--pillar" : ""}">'),
    ('<h3>${lienCoach(c.name) ? `<a href="${lienCoach(c.name)}">${c.name}</a>` : c.name}</h3>\n            <span class="coach__role">${c.role}</span>',
     '<h3>${lienCoach(c.name) ? `<a class="carte-lien__tout" href="${lienCoach(c.name)}">${c.name}</a>` : c.name}</h3>\n            <span class="coach__role">${roleHtml(c.role, c.name)}</span>'),
    ('c.disciplines.map((d) => `<li>${d}</li>`)', 'c.disciplines.map((d) => `<li>${pastilleHtml(d, c.name)}</li>`)'),
    ('`<a class="coach__page" href="${lienCoach(c.name)}">La page de',
     '`<a class="coach__page carte-lien__dessus" href="${lienCoach(c.name)}" tabindex="-1" aria-hidden="true">La page de'),
], "role-liens.js")

# C. Les fiches discipline : la table des liens porte ses coachs, et sert dès le début.
patch("scripts/generer-disciplines.mjs", [
    ('import { ROOT, BASE, donnees, textes, creneaux, joursEnMots, remplir, lienDe, JOUR, JOUR_SCHEMA } from "./disciplines-lib.mjs";',
     'import { ROOT, BASE, donnees, textes, creneaux, joursEnMots, remplir, lienDe, JOUR, JOUR_SCHEMA } from "./disciplines-lib.mjs";\nimport { pathToFileURL } from "node:url";'),
    ('const PUBLIC = join(ROOT, "public");',
     'const PUBLIC = join(ROOT, "public");\n'
     '/* La table des liens (écrite en fin de script) sert aussi ici : le rôle d\'un\n'
     '   coach relie chaque discipline à sa page. Elle porte les coachs de chaque\n'
     '   page : « Boxe loisirs » mène à la page qui nomme ce coach-là. */\n'
     'const table = DISCIPLINES.filter((d) => T[d.key]).map((d) => ({ key: d.key, nom: d.name, href: lienDe(d.key, T), coachs: T[d.key].coachs || [] }));\n'
     'const { creerLiens } = await import(pathToFileURL(join(PUBLIC, "assets", "js", "role-liens.js")).href);\n'
     'const LIENS = creerLiens(table);'),
    ('const table = DISCIPLINES.filter((d) => T[d.key]).map((d) => ({ key: d.key, nom: d.name, href: lienDe(d.key, T) }));\n', ''),
    ('`<article class="dp-coach">${await img(', '`<article class="dp-coach${TC[c.name] ? " carte-lien" : ""}">${await img('),
    ('<h3>${TC[c.name] ? `<a href="/coachs/${TC[c.name].slug}/">${e(c.name)}</a>` : e(c.name)}</h3><p class="dp-role">${e(c.role)}</p>',
     '<h3>${TC[c.name] ? `<a class="carte-lien__tout" href="/coachs/${TC[c.name].slug}/">${e(c.name)}</a>` : e(c.name)}</h3><p class="dp-role">${LIENS.roleHtml(c.role, c.name, lienDe(d.key, T))}</p>'),
], "creerLiens")

# D. La page du club.
patch("scripts/generer-club-de-boxe.mjs", [
    ('const { PAGES_COACHS } = await import(pathToFileURL(join(ROOT, "public", "assets", "js", "coachs-liens.js")).href);',
     'const { PAGES_COACHS } = await import(pathToFileURL(join(ROOT, "public", "assets", "js", "coachs-liens.js")).href);\n'
     'const { roleHtml } = await import(pathToFileURL(join(ROOT, "public", "assets", "js", "role-liens.js")).href);'),
    ('const carteCoach = (c) => `<a class="dp-carte dp-carte--lien" href="${hrefCoach(c)}"><span class="dp-tag">${e(c.tag)}</span><h3>${e(c.name)}</h3><p>${e(c.role)}</p></a>`;',
     'const carteCoach = (c) => `<article class="dp-carte dp-carte--lien carte-lien"><span class="dp-tag">${e(c.tag)}</span><h3><a class="carte-lien__tout" href="${hrefCoach(c)}">${e(c.name)}</a></h3><p>${roleHtml(c.role, c.name)}</p></article>`;'),
], "role-liens.js")

# E. Les pages de coach : les pastilles du héros, et « Les autres coachs ».
patch("scripts/generer-coachs.mjs", [
    ('import { ROOT, BASE, donnees, textes as textesDisciplines, lienDe } from "./disciplines-lib.mjs";',
     'import { ROOT, BASE, donnees, textes as textesDisciplines, lienDe } from "./disciplines-lib.mjs";\nimport { pathToFileURL } from "node:url";\n'
     'const { roleHtml, pastilleHtml } = await import(pathToFileURL(join(ROOT, "public", "assets", "js", "role-liens.js")).href);'),
    ('(c.disciplines || []).map((x) => `<span>${e(x)}</span>`)', '(c.disciplines || []).map((x) => `<span>${pastilleHtml(x, c.name)}</span>`)'),
    ('`<a class="dp-carte dp-carte--lien cp-autre" href="/coachs/${slugDe(x.name)}/">${await portrait(',
     '`<article class="dp-carte dp-carte--lien cp-autre carte-lien">${await portrait('),
    ('<span class="dp-tag">${e(x.tag)}</span><h3>${e(x.name)}</h3><p>${e(x.role)}</p><span class="dp-go">Voir sa page <span aria-hidden="true">→</span></span></a>`',
     '<span class="dp-tag">${e(x.tag)}</span><h3><a class="carte-lien__tout" href="/coachs/${slugDe(x.name)}/">${e(x.name)}</a></h3><p>${roleHtml(x.role, x.name)}</p><span class="dp-go" aria-hidden="true">Voir sa page <span aria-hidden="true">→</span></span></article>`'),
], "role-liens.js")

# F. Le HTML cuit pour les robots.
patch("scripts/cuire-pages.mjs", [
    ('const coachroster = COACHES.map((c) => {',
     'const { roleHtml } = await import(new URL("../public/assets/js/role-liens.js", import.meta.url).href);\nconst coachroster = COACHES.map((c) => {'),
    ('<p><b>${e(c.role || "")}</b>', '<p><b>${roleHtml(c.role || "", c.name)}</b>'),
], "role-liens.js")

# G. Les styles, une fois, dans base.css.
p = R + "public/assets/css/base.css"
s = io.open(p, encoding="utf-8", newline="").read()
if ".carte-lien__tout" not in s:
    nl = "\r\n" if "\r\n" in s else "\n"
    css = """
/* ── Cartes coach : toute la carte mène à la page du coach, chaque discipline à la sienne (19/09) ──
   Le lien du nom s'étire sur la carte (::after) ; les disciplines passent
   au-dessus. Une ancre ne peut pas en contenir une autre : la carte est un
   <article>. isolation: isolate garde l'empilement dans la carte. */
.carte-lien { position: relative; isolation: isolate; cursor: pointer; }
.carte-lien .carte-lien__tout { color: inherit; text-decoration: none; }
.carte-lien .carte-lien__tout::after { content: ""; position: absolute; inset: 0; z-index: 1; }
.carte-lien .role-lien, .carte-lien .carte-lien__dessus { position: relative; z-index: 2; }
.carte-lien .carte-lien__tout:focus-visible { outline: none; }
.carte-lien:has(.carte-lien__tout:focus-visible) { outline: 2px solid var(--accent); outline-offset: 3px; }
.carte-lien:hover .carte-lien__tout { color: var(--accent); }
.role-lien { color: inherit; text-decoration: underline; text-decoration-color: color-mix(in srgb, currentColor 38%, transparent);
  text-decoration-thickness: 1px; text-underline-offset: .28em; transition: color .2s ease, text-decoration-color .2s ease; }
.role-lien:hover, .role-lien:focus-visible { color: var(--accent); text-decoration-color: currentColor; }
/* zone de doigt : le rôle est petit, ses liens gagnent de la hauteur sans bouger la ligne */
@media (pointer: coarse) { .role-lien { display: inline-block; padding-block: .5em; margin-block: -.5em; } }
/* dans une pastille, le lien occupe la pastille et ne se souligne pas : la pastille est le bouton */
.phero__meta .role-lien, .coach__disc .role-lien { text-decoration: none; display: inline-flex; align-items: center; padding: 0; margin: 0; }
.phero__meta span:has(.role-lien), .coach__disc li:has(.role-lien) { transition: border-color .2s ease, color .2s ease; }
.phero__meta span:has(.role-lien:hover), .coach__disc li:has(.role-lien:hover) { border-color: var(--accent); color: var(--accent); }
"""
    s = s.rstrip("\r\n") + nl + css.replace("\n", nl)
    io.open(p, "w", encoding="utf-8", newline="").write(s)
    print("ok base.css")
else:
    print("déjà fait base.css")
