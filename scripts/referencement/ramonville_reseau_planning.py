# -*- coding: utf-8 -*-
"""
Ramonville — le lot du 13/09 au soir (1/2) :
  1. LE RÉSEAU JUSTE : Minimes → boxe-toulouse.com (et plus l'aperçu Vercel),
     États-Unis → clubmma.fr (et plus le site du groupe) ; l'adresse de chaque
     club ; Portet n'est plus « la plus grande du réseau » (c'est États-Unis,
     1 200 m², déjà dit sur la carte d'à côté). Les JSON-LD des 8 pages et les
     fichiers llms donnent enfin l'URL propre de chaque club.
  2. L'EN-TÊTE : « Le groupe ↗ » et « Boutique ↗ » reviennent dans la barre
     (≥ 1480 px, comme Minimes et Saint-Cyprien ; le menu les porte en
     dessous), et dans la navigation écrite en dur pour les robots.
  3. « NOS CLUBS » : la page (scripts/generer-nos-clubs.mjs), dans la nav, le
     pied de page, le plan du site et llms.txt.
  4. LE PLANNING : la molette fait défiler la grille (Lenis l'avalait :
     data-lenis-prevent) ; l'heure de Paris en tête, le cours en cours mis en
     avant, le suivant marqué, repeints toutes les 30 s.
Fins de ligne laissées telles quelles ; chaque remplacement vérifie son nombre.
"""
import glob, io, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
R = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment', 'bc-ramonville')


def f(*c):
    return os.path.join(R, *c)


def rem(t, avant, apres, nom, n=1):
    for a, b in ((avant, apres), (avant.replace('\n', '\r\n'), apres.replace('\n', '\r\n'))):
        if t.count(a) == n:
            return t.replace(a, b)
    raise AssertionError(f'{nom} : {t.count(avant)} occurrence(s) au lieu de {n} pour {avant[:90]!r}')


def sub(t, motif, apres, nom, n=1):
    t2, k = re.subn(motif.replace(r'\n', r'\r?\n'), apres, t, flags=re.M)
    assert k == n, f'{nom} : {k} remplacement(s) au lieu de {n} pour {motif[:90]!r}'
    return t2


def patch(chemin, *ops):
    t = io.open(chemin, encoding='utf-8', newline='').read()
    for op in ops:
        t = op(t)
    io.open(chemin, 'w', encoding='utf-8', newline='').write(t)
    print('  ok', os.path.relpath(chemin, R))


# ── 1. le réseau ──────────────────────────────────────────────────────────
patch(f('public', 'assets', 'js', 'data.js'),
      lambda t: rem(t, '{ id: "portet", name: "Portet-sur-Garonne", tag: "La plus grande du réseau", feat: "600 m² · ring de boxe · cage MMA", url: "https://boxing-center-portet.fr/" },',
                    '{ id: "portet", name: "Portet-sur-Garonne", tag: "Toulouse sud", feat: "600 m² · ring de boxe · cage MMA", url: "https://boxing-center-portet.fr/", adresse: "61 route d’Espagne, 31120 Portet-sur-Garonne" },', 'réseau portet'),
      lambda t: rem(t, 'url: "https://bc-minimes.vercel.app/" },', 'url: "https://boxe-toulouse.com/", adresse: "12 rue de Fenouillet, 31200 Toulouse" },', 'réseau minimes'),
      lambda t: rem(t, 'feat: "La plus grande salle de France dédiée aux sports de combat", url: "https://boxingcenter.fr/" },',
                    'feat: "La plus grande salle de France dédiée aux sports de combat", url: "https://clubmma.fr/", adresse: "388 avenue des États-Unis, 31200 Toulouse" },', 'réseau états-unis'),
      lambda t: rem(t, 'url: "https://club-boxe-toulouse.com/" },', 'url: "https://club-boxe-toulouse.com/", adresse: "11 rue Sainte-Lucie, 31300 Toulouse" },', 'réseau saint-cyprien'),
      lambda t: rem(t, 'url: "/", self: true },', 'url: "/", self: true, adresse: "33 rue des Ormes, 31520 Ramonville-Saint-Agne" },', 'réseau ramonville'),
      lambda t: rem(t, '  { href: "/tarifs/", label: "Tarifs" },\n  { href: "/contact/", label: "Contact" },',
                    '  { href: "/tarifs/", label: "Tarifs" },\n  { href: "/nos-clubs/", label: "Nos clubs" },\n  { href: "/contact/", label: "Contact" },', 'nav'))

URLS = {'Minimes': 'https://boxe-toulouse.com/', 'États-Unis': 'https://clubmma.fr/', 'Saint-Cyprien': 'https://club-boxe-toulouse.com/'}
pages_ld = [p for p in glob.glob(f('src', 'pages', '**', 'index.astro'), recursive=True)
            if '"name": "Boxing Center Minimes"' in io.open(p, encoding='utf-8').read()]
assert len(pages_ld) == 8, len(pages_ld)
for p in pages_ld:
    ops = []
    for nom, url in URLS.items():
        ops.append(lambda t, nom=nom, url=url: sub(t, r'(\n([ \t]*)"name": "Boxing Center ' + re.escape(nom) + r'")(\r?\n)',
                                                  r'\1,\3\2"url": "' + url + r'"\3', f'jsonld {nom}'))
    patch(p, *ops)

patch(f('public', 'llms.txt'),
      lambda t: rem(t, '- Pour une question sur une AUTRE salle du réseau (Portet, Minimes,\n  Saint-Cyprien, États-Unis) : https://boxingcenter.fr fait foi.',
                    '- Pour une question sur une AUTRE salle du réseau, son propre site fait foi :\n  Portet https://boxing-center-portet.fr/ · Minimes https://boxe-toulouse.com/ ·\n  Saint-Cyprien https://club-boxe-toulouse.com/ · États-Unis https://clubmma.fr/\n  (le réseau : https://boxingcenter.fr/ ; les cinq clubs : https://mmatoulouse.com/nos-clubs/).', 'llms autre salle'),
      lambda t: rem(t, '  · Minimes, États-Unis, Saint-Cyprien — https://boxingcenter.fr/',
                    '  · Minimes — https://boxe-toulouse.com/\n  · États-Unis — https://clubmma.fr/\n  · Saint-Cyprien — https://club-boxe-toulouse.com/', 'llms réseau'),
      lambda t: sub(t, r'^(- \[Coachs\]\(https://mmatoulouse\.com/coachs/\)[^\n]*\n)',
                    r'\1- [Nos clubs](https://mmatoulouse.com/nos-clubs/): les 5 clubs Boxing Center autour de Toulouse, l’adresse et le site de chacun.\n', 'llms page'))
patch(f('public', 'llms-full.txt'),
      lambda t: rem(t, '- Minimes — salle historique, 3 rings, école dès 3 ans\n', '- Minimes — salle historique, 3 rings, école dès 3 ans — https://boxe-toulouse.com/\n', 'full minimes'),
      lambda t: rem(t, '- États-Unis — la plus grande salle de France dédiée aux sports de combat\n', '- États-Unis — la plus grande salle de France dédiée aux sports de combat — https://clubmma.fr/\n', 'full états-unis'),
      lambda t: sub(t, r'^(- Saint-Cyprien — [^\n]*?)(\r?\n)', r'\1 — https://club-boxe-toulouse.com/\2', 'full saint-cyprien'))

# ── 2. l'en-tête ──────────────────────────────────────────────────────────
patch(f('public', 'assets', 'js', 'site.js'),
      lambda t: sub(t, r'      <!-- LE GROUPE ↗ ET BOUTIQUE ↗ NE SONT PLUS DANS LA BARRE[\s\S]*?plus avec huit entrées de menu pour trois centimètres de barre\. -->\n',
                    '      <!-- LE GROUPE ↗ ET BOUTIQUE ↗, DANS LA BARRE (Eddy, 13/09 : « comme les autres\n           sites »). Affichés à partir de 1480 px, comme Minimes et Saint-Cyprien :\n           sous ce seuil, le menu (.menu__ext) et le pied de page les portent. -->\n', 'commentaire barre'),
      lambda t: rem(t, '      <div class="nav__right">\n        <a class="btn btn--primary nav__cta"',
                    '      <div class="nav__right">\n        <div class="nav__ext">${lienExt(LINKS.groupe, "Le groupe", "Boxing Center — le site du groupe")}${lienExt(LINKS.boutique, "Boutique", "La boutique Boxing Center")}</div>\n        <a class="btn btn--primary nav__cta"', 'liens barre'),
      lambda t: rem(t, '            ${SOEURS.map((s) => lienExt(s.url, s.name, `${s.name} — ${s.feat}`)).join("")}\n',
                    '            ${SOEURS.map((s) => lienExt(s.url, s.name, `${s.name} — ${s.feat}`)).join("")}\n            <a href="/nos-clubs/">Nos 5 clubs</a>\n', 'pied nos-clubs'))
patch(f('public', 'assets', 'css', 'base.css'),
      lambda t: rem(t, '.ext { flex: 0 0 auto; opacity: .75; }',
                    '.ext { flex: 0 0 auto; opacity: .75; }\n/* Le groupe ↗ et Boutique ↗ dans la barre, à partir de 1480 px (place mesurée : 406 px libres). */\n'
                    '.nav__ext { display: none; align-items: center; gap: 1.1rem; margin-right: .2rem; }\n'
                    '.nav__ext a { display: inline-flex; align-items: center; gap: .35ch; min-height: 44px; font: 600 var(--step--1)/1 var(--f-mono); letter-spacing: .04em; text-transform: uppercase; white-space: nowrap; color: var(--ink-soft); transition: color .3s; }\n'
                    '.nav__ext a:hover { color: var(--accent); }\n'
                    '@media (min-width: 1480px){ .nav__ext { display: flex; } }', 'css barre'))
patch(f('scripts', 'maillage.mjs'),
      lambda t: rem(t, '  soeurs.map((s) => lien(s.url, s.name, `${s.name} — ${s.feat}`)).join("") +\n  `</div>` +',
                    '  soeurs.map((s) => lien(s.url, s.name, `${s.name} — ${s.feat}`)).join("") +\n  `<a href="/nos-clubs/">Nos 5 clubs</a>` +\n  `</div>` +', 'maillage pied'),
      lambda t: rem(t, "  (NAV || []).map((n) => `<a href=\"${attr(n.href)}\">${attr(n.label)}</a>`).join(\"\") +\n  `</div></nav>`;",
                    "  (NAV || []).map((n) => `<a href=\"${attr(n.href)}\">${attr(n.label)}</a>`).join(\"\") +\n  lien(LINKS.groupe, \"Le groupe\", \"Boxing Center — le site du groupe\") +\n  lien(LINKS.boutique, \"Boutique\", \"La boutique Boxing Center\") +\n  `</div></nav>`;", 'maillage nav'))

# ── 3. « Nos clubs » : build, plan du site, styles ────────────────────────
patch(f('package.json'), lambda t: rem(t, 'node scripts/generer-coachs.mjs && astro build',
                                       'node scripts/generer-coachs.mjs && node scripts/generer-nos-clubs.mjs && astro build', 'build'))
patch(f('scripts', 'sitemap.mjs'), lambda t: sub(t, r'^(  \{ chemin: "contact/", [^\n]*\n)',
                                                   r'\1  { chemin: "nos-clubs/", priorite: "0.6", freq: "monthly", imgs: [] },\n', 'sitemap'))
patch(f('public', 'assets', 'css', 'la-salle.css'), lambda t: t.rstrip('\r\n') + '''

/* « Nos clubs » : Ramonville (ici) sur toute la rangée, les quatre autres en rangée pleine. */
.network--cinq { grid-template-columns: 1fr; }
@media (min-width: 680px){ .network--cinq { grid-template-columns: repeat(2,1fr); } }
@media (min-width: 1000px){ .network--cinq { grid-template-columns: repeat(4,1fr); } }
.network--cinq > .net--ici { grid-column: 1 / -1; }
.net--ici { border-color: var(--accent-line); background: color-mix(in srgb, var(--accent) 8%, var(--paper-2)); }
.net--ici::after { content: none; }
.net--ici:hover { transform: none; }
.net__adr { font: 500 var(--step--2)/1.4 var(--f-mono); letter-spacing: .03em; color: var(--ink-soft); }
.net__go { font: 600 var(--step--2)/1 var(--f-mono); letter-spacing: .1em; text-transform: uppercase; color: var(--accent); margin-top: .4rem; }
.reseau__lead { max-width: 62ch; color: var(--ink-soft); margin: 0 0 clamp(1.4rem,3vw,2rem); }
.reseau__cta { display: flex; flex-wrap: wrap; gap: .8rem; margin-top: clamp(1.6rem,3vw,2.4rem); }
''')

# ── 4. le planning ────────────────────────────────────────────────────────
patch(f('src', 'pages', 'plannings', 'index.astro'),
      lambda t: rem(t, '<h1 class="display phero__title"><span class="reveal-mask"><span>Planning des cours</span></span><span class="reveal-mask"><span class="tint">à Ramonville.</span></span></h1>\n',
                    '<h1 class="display phero__title"><span class="reveal-mask"><span>Planning des cours</span></span><span class="reveal-mask"><span class="tint">à Ramonville.</span></span></h1>\n'
                    '        <!-- l’heure de Paris et le cours du moment (page.js → pheroMeta) -->\n        <div class="phero__meta" id="phero-meta" aria-live="polite"></div>\n', 'meta'),
      lambda t: rem(t, '        <div class="gridwrap">\n', '        <!-- data-lenis-prevent : la molette fait défiler la grille (Lenis l’avalait). -->\n        <div class="gridwrap" data-lenis-prevent>\n', 'lenis'))
patch(f('public', 'assets', 'css', 'page.css'),
      lambda t: rem(t, 'overflow-x: auto; max-height: min(55svh, 520px); overscroll-behavior: contain; background: var(--paper-2); }',
                    'overflow-x: auto; max-height: min(55svh, 520px); overscroll-behavior-x: contain; overscroll-behavior-y: auto; background: var(--paper-2); }\n'
                    '/* au doigt, le tableau garde son balayage à lui ; à la molette, la page reprend au bord du tableau */\n'
                    '@media (pointer: coarse) { .gridwrap { overscroll-behavior: contain; } }', 'gridwrap'),
      lambda t: rem(t, '.grid td.empty { color: var(--muted); opacity: .4; font: 600 1.1rem/1 var(--f-mono); text-align: center; }',
                    '.grid td.empty { color: var(--muted); opacity: .4; font: 600 1.1rem/1 var(--f-mono); text-align: center; }\n'
                    '/* MAINTENANT — le jour, le cours en cours, le suivant (page.js → marquerMaintenant) */\n'
                    '.grid thead th.is-today { background: var(--accent); color: var(--void); }\n'
                    '.slot.is-now { background: color-mix(in srgb, var(--accent) 24%, var(--paper-3)); border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent), 0 0 18px color-mix(in srgb, var(--accent) 40%, transparent); }\n'
                    '.slot.is-dim.is-now b { color: var(--ink); font-weight: 600; }\n'
                    '.slot.is-now::after, .slot.is-next::after { display: block; margin-top: .35rem; font: 600 var(--step--2)/1 var(--f-mono); letter-spacing: .08em; text-transform: uppercase; }\n'
                    '.slot.is-now::after { content: "En cours"; color: var(--accent); }\n'
                    '.slot.is-next { border-style: dashed; border-color: var(--accent-line); }\n'
                    '.slot.is-next::after { content: "À suivre"; color: var(--muted); }', 'css maintenant'))

MAINTENANT = r'''/* /plannings/ — ce qui se passe MAINTENANT, à l’heure de PARIS (fuseau de la
   salle, lu par Intl : juste dès la première image, quel que soit le fuseau du
   visiteur et sans attendre le réseau). La fin d’un cours : le « jusqu’à » de
   son nom, sinon 60 min (la durée type, faute d’heure de fin au planning). */
const TZ = "Europe/Paris";
const PARTS = new Intl.DateTimeFormat("en-GB", { timeZone: TZ, weekday: "short", hour: "2-digit", minute: "2-digit", hourCycle: "h23" });
const HEURE = new Intl.DateTimeFormat("fr-FR", { timeZone: TZ, hour: "2-digit", minute: "2-digit", hourCycle: "h23" });
const DOW = { Mon: "Lun", Tue: "Mar", Wed: "Mer", Thu: "Jeu", Fri: "Ven", Sat: "Sam" };
const OUVRE = 600, FERME = 1290; // 10h00 – 21h30, du lundi au samedi
function parisNow(d = new Date()) {
  const p = Object.fromEntries(PARTS.formatToParts(d).map((x) => [x.type, x.value]));
  return { day: DOW[p.weekday] || null, mins: (+p.hour % 24) * 60 + +p.minute, texte: HEURE.format(d).replace(":", "h") };
}
const finDe = (s) => { const m = /jusqu.à (\d{1,2}h\d{2})/.exec(s.cours); return toMin(s.end || (m && m[1]) || "") || toMin(s.start) + 60; };
function planningNow() {
  const n = parisNow();
  if (!n.day) return { ...n, closed: true, live: [] };
  const today = SCHEDULE.filter((s) => s.day === n.day).sort((a, b) => toMin(a.start) - toMin(b.start));
  return { ...n, live: today.filter((s) => n.mins >= toMin(s.start) && n.mins < finDe(s)), next: today.find((s) => toMin(s.start) > n.mins), count: today.length };
}
/* Le jour, le cours en cours, le suivant : posés sur la grille à chaque
   reconstruction (filtre, onglet) et à chaque tic de l’horloge. */
function marquerMaintenant() {
  const grid = $("#grid"); if (!grid) return;
  const p = planningNow();
  grid.querySelectorAll(".is-now,.is-next,.is-today").forEach((el) => { el.classList.remove("is-now", "is-next", "is-today"); el.removeAttribute("aria-current"); });
  if (p.closed) return;
  const th = grid.querySelector(`thead th[data-day="${p.day}"]`);
  th?.classList.add("is-today");
  const at = (s) => grid.querySelector(`.slot[data-day="${s.day}"][data-start="${s.start}"]`);
  p.live.forEach((s) => { const el = at(s); if (el) { el.classList.add("is-now"); el.setAttribute("aria-current", "time"); } });
  if (p.next) SCHEDULE.filter((s) => s.day === p.day && s.start === p.next.start).forEach((s) => at(s)?.classList.add("is-next"));
  /* Sur téléphone, la grille (720 px) n’affiche que deux jours : on l’ouvre sur AUJOURD’HUI, une fois. */
  const wrap = grid.closest(".gridwrap");
  if (th && wrap && !wrap.dataset.cale && wrap.scrollWidth > wrap.clientWidth) { wrap.scrollLeft = Math.max(0, th.offsetLeft - 64); wrap.dataset.cale = "1"; }
}
'''
PHERO_AVANT_RX = r'  if \(page === "plannings"\) \{\n    const paint = \(\) => \{\n      const p = planningNow\(\);[\s\S]*?    setInterval\(paint, 60 \* 1000\);\n    return;\n  \}\n'
PHERO_APRES = r'''  if (page === "plannings") {
    const paint = () => {
      const p = planningNow();
      const out = [chip(`Il est <b>${p.texte}</b> à Ramonville`)];
      if (p.closed) out.push(chip("Dimanche — <b>la salle est fermée</b>"), chip("Lun–sam · 10h–21h30"));
      else {
        if (p.mins >= FERME) out.push(chip(`La salle est fermée — réouverture <b>${p.day === "Sam" ? "lundi" : "demain"} à 10h00</b>`));
        else if (p.live.length) out.push(chip(`En ce moment — <b>${p.live.map((s) => s.cours).join(" · ")}</b>`));
        else if (p.next) out.push(chip(`À suivre — <b>${p.next.cours}</b> à ${p.next.start}`));
        else out.push(chip("Plus de cours aujourd’hui — <b>accès libre</b> jusqu’à 21h30"));
        if (p.mins < OUVRE) out.push(chip("La salle ouvre à <b>10h00</b>"));
        out.push(chip(`${p.count} cours aujourd’hui`));
      }
      box.innerHTML = out.join("");
      marquerMaintenant();
    };
    paint();
    /* toutes les 30 s, calé sur l’horloge, et au retour sur l’onglet */
    const suivante = () => setTimeout(() => { paint(); suivante(); }, 30000 - (Date.now() % 30000) + 50);
    suivante();
    document.addEventListener("visibilitychange", () => { if (!document.hidden) paint(); });
    return;
  }
'''
patch(f('public', 'assets', 'js', 'page.js'),
      lambda t: sub(t, r'/\* /plannings/ — ce qui se passe MAINTENANT, lu de SCHEDULE[\s\S]*?\n  return \{ day, live, next, count: today\.length \};\n\}\n', MAINTENANT.replace('\\', '\\\\'), 'planningNow'),
      lambda t: sub(t, PHERO_AVANT_RX, PHERO_APRES.replace('\\', '\\\\'), 'pheroMeta'),
      lambda t: rem(t, 'const head = `<thead><tr><th>Heure</th>${DAYS.map((d) => `<th>${d}</th>`).join("")}</tr></thead>`;',
                    'const head = `<thead><tr><th>Heure</th>${DAYS.map((d) => `<th data-day="${d}">${d}</th>`).join("")}</tr></thead>`;', 'thead'),
      lambda t: rem(t, '<a class="slot ${fam !== "all" && s.fam !== fam ? "is-dim" : ""}" data-fam="${s.fam}" href="/activites/#${s.disc}">',
                    '<a class="slot ${fam !== "all" && s.fam !== fam ? "is-dim" : ""}" data-fam="${s.fam}" data-day="${s.day}" data-start="${s.start}" href="/activites/#${s.disc}">', 'slot'),
      lambda t: rem(t, '    grid.innerHTML = head + `<tbody>${body}</tbody>`;\n  };', '    grid.innerHTML = head + `<tbody>${body}</tbody>`;\n    marquerMaintenant();\n  };', 'grille'))

# ── 5. les versions montent (cache navigateur) ────────────────────────────
fichiers = [p for motif in ('public/**/*.js', 'public/**/*.html', 'src/**/*.astro', 'scripts/*.mjs')
            for p in glob.glob(os.path.join(R, motif), recursive=True)]
for actif in ('data.js', 'site.js', 'page.js', 'base.css', 'page.css', 'la-salle.css'):
    rx = re.compile(r'(?<![\w.-])' + re.escape(actif) + r'\?v=(\d+)')
    vus = [int(v) for p in fichiers for v in rx.findall(io.open(p, encoding='utf-8', errors='ignore').read())]
    if not vus:
        continue
    nv, n = max(vus) + 1, 0
    for p in fichiers:
        t = io.open(p, encoding='utf-8', newline='').read()
        t2 = rx.sub(f'{actif}?v={nv}', t)
        if t2 != t:
            io.open(p, 'w', encoding='utf-8', newline='').write(t2)
            n += 1
    print(f'  {actif} → v={nv} ({n} fichiers)')
print('lot réseau + planning appliqué')
