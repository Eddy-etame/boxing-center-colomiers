# -*- coding: utf-8 -*-
"""
Portet, 19/09 — les captures d'Eddy : sections VIDES (« Le ring est à tout le
monde », « Sans détour », l'appel final), billet coupé sur téléphone, « Hors des
cordes » posé sur le 404, mot-symbole coupé sous la barre.

MESURÉ dans un Chrome réellement rendu (portet_diag_revelations.mjs) : la page
fait 30 420 px quand ScrollTrigger mesure ses déclencheurs ; quand la forge 3D
se monte, html.forge-live cache les cartes de repli et la page tombe à 28 586 px
(téléphone : 32 853 → 29 128). Tout ce qui est SOUS les coachs garde un
déclencheur 1 834 px (3 725 px) trop bas : le contenu est à l'écran, invisible.
Depuis le 13/09 le filet ne couvrait plus ce que GSAP tient : plus rien ne
rattrapait.

  1. main.ts   — forge-live posé DÈS LE DÉPART quand la forge est attendue (la
                 page ne rétrécit plus en cours de visite) ; retiré si la forge
                 échoue (les cartes reviennent).
  2. scroll.ts — ScrollTrigger remesure à chaque changement de hauteur de la
                 page (ResizeObserver, temporisé) ; LE FILET DE GSAP : tout ce
                 qui entre dans les trois quarts hauts de l'écran et n'a pas
                 commencé son entrée la joue tout de suite.
  3. main.css  — le billet sur téléphone : ses mentions passent à la ligne.
  4. 404.html  — « Hors des cordes » sous les chiffres, plus dessus.
  5. hero.ts   — la garantie du HAUT : le mot-symbole reste sous la barre.
CRLF conservés ; chaque remplacement vérifie son compte ; rejouable.
"""
import io, os, sys
sys.stdout.reconfigure(encoding='utf-8')
P = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Portet', 'boxing-center-portet')


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


def patch(rel, *ops):
    p = os.path.join(P, rel)
    t = lire(p)
    for op in ops:
        t = op(t)
    ecrire(p, t)
    print('  ok', rel)


# ── 1. main.ts ─────────────────────────────────────────────────────────────
patch('src/main.ts',
      lambda t: rem(t, '''  initLazyBackgrounds();
  /* Le filet repasse APRES la peinture''', '''  /* LA FORGE EST ATTENDUE : ses cartes de repli s'effacent TOUT DE SUITE (19/09).
     Elles s'effaçaient au montage de la forge, des secondes plus tard : la page
     perdait 1 834 px (3 725 sur téléphone) APRÈS que ScrollTrigger avait mesuré
     ses déclencheurs, et tout ce qui suit les coachs — publics, tarifs, appel
     final — restait invisible à l'écran. Si la forge échoue, la classe tombe
     et les cartes reviennent (voir plus bas). */
  if (hasWebGL && document.querySelector(".forge")) document.documentElement.classList.add("forge-live");

  initLazyBackgrounds();
  /* Le filet repasse APRES la peinture''', 'forge-live au départ'),
      lambda t: rem(t, '''function lazy3D<T>(el: Element | null, loader: () => Promise<T>, init: (m: T) => void) {
  if (!el) return;
  const scene: Scene3D = { run: () => loader().then(init).catch(() => {}), faite: false };''',
                    '''function lazy3D<T>(el: Element | null, loader: () => Promise<T>, init: (m: T) => void, echec?: () => void) {
  if (!el) return;
  const scene: Scene3D = { run: () => loader().then(init).catch(() => { echec?.(); }), faite: false };''', 'lazy3D : échec'),
      lambda t: rem(t, '''        document.documentElement.classList.add("forge-live");
      });''', '''        document.documentElement.classList.add("forge-live");
      }, () => {
        /* la forge n'a pas pu se monter : les cartes de repli reviennent */
        document.documentElement.classList.remove("forge-live");
      });''', 'forge : repli'))

# ── 2. scroll.ts ───────────────────────────────────────────────────────────
patch('src/scroll.ts',
      lambda t: rem(t, '''  window.addEventListener("bcp:rideau-parti", () => ScrollTrigger.refresh());
''', '''  window.addEventListener("bcp:rideau-parti", () => ScrollTrigger.refresh());
  /* LA PAGE CHANGE DE HAUTEUR → ON REMESURE (19/09). Une scène 3D qui se monte,
     une image sans dimensions, une police qui arrive : tout ce qui déplace le
     contenu APRÈS la mesure laisse des déclencheurs au mauvais endroit, et des
     sections vides à l'écran (mesuré : 1 834 px d'écart sur l'accueil).
     Temporisé, et seulement quand la hauteur a VRAIMENT bougé. */
  if ("ResizeObserver" in window) {
    let hauteur = document.documentElement.scrollHeight;
    let minuteur = 0;
    new ResizeObserver(() => {
      const h = document.documentElement.scrollHeight;
      if (Math.abs(h - hauteur) < 8) return;
      hauteur = h;
      window.clearTimeout(minuteur);
      minuteur = window.setTimeout(() => ScrollTrigger.refresh(), 220);
    }).observe(document.body);
  }
''', 'remesure à chaque changement de hauteur'),
      lambda t: rem(t, '''  const rejouer = (tw: gsap.core.Tween, trigger: Element) =>
    ScrollTrigger.create({ trigger, start: "top bottom", onLeaveBack: () => { tw.pause(0); } });
''', '''  const rejouer = (tw: gsap.core.Tween, trigger: Element) =>
    ScrollTrigger.create({ trigger, start: "top bottom", onLeaveBack: () => { tw.pause(0); } });

  /* LE FILET DE GSAP (19/09). Depuis le 13/09 le filet général ne touche plus
     ce que GSAP tient — et si un déclencheur est mal placé, plus rien ne
     rattrape : la section reste vide sous les yeux du visiteur. Règle simple :
     ce qui est dans les TROIS QUARTS HAUTS de l'écran et n'a pas commencé son
     entrée la joue tout de suite. On joue le tween lui-même : l'animation
     reste la même, et le réarmement par le bas continue de marcher. */
  const filetGsap = "IntersectionObserver" in window
    ? track(new IntersectionObserver((es) => {
        for (const e of es) {
          const tw = (e.target as any)._tw as gsap.core.Tween | undefined;
          if (e.isIntersecting && tw && tw.progress() === 0 && !tw.isActive()) tw.play();
        }
      }, { rootMargin: "0px 0px -25% 0px" }))
    : null;
  const tenir = (els: Iterable<HTMLElement>, tw: gsap.core.Tween) => {
    for (const el of els) { (el as any)._tw = tw; filetGsap?.observe(el); }
  };
'''.replace('\n\n\n', '\n\n'), 'filet de GSAP'),
      lambda t: rem(t, '''    kids.forEach((k) => k.setAttribute("data-gsap", ""));
    rejouer(gsap.fromTo(kids, { opacity: 0, y: 28 }, {
      opacity: 1, y: 0, duration: 0.9, ease: "power3.out", stagger: 0.08,
      scrollTrigger: { trigger: group, start: "top 82%" },
    }), group);''', '''    kids.forEach((k) => k.setAttribute("data-gsap", ""));
    const tw = gsap.fromTo(kids, { opacity: 0, y: 28 }, {
      opacity: 1, y: 0, duration: 0.9, ease: "power3.out", stagger: 0.08,
      scrollTrigger: { trigger: group, start: "top 82%" },
    });
    tenir(kids, tw);
    rejouer(tw, group);''', 'groupes tenus'),
      lambda t: rem(t, '''      el.setAttribute("data-gsap", "");
      rejouer(gsap.fromTo(el, { opacity: 0, y: 28 }, {
        opacity: 1, y: 0, duration: 0.9, ease: "power3.out",
        scrollTrigger: { trigger: el, start: "top 88%" },
      }), el);''', '''      el.setAttribute("data-gsap", "");
      const tw = gsap.fromTo(el, { opacity: 0, y: 28 }, {
        opacity: 1, y: 0, duration: 0.9, ease: "power3.out",
        scrollTrigger: { trigger: el, start: "top 88%" },
      });
      tenir([el], tw);
      rejouer(tw, el);''', 'éléments tenus'))

# ── 3. le billet sur téléphone ─────────────────────────────────────────────
patch('src/styles/main.css', lambda t: rem(t, '''  .billet__go { margin: 0 0 0 auto; }
}''', '''  .billet__go { margin: 0 0 0 auto; }
  /* 19/09 : « COMPTANT · PAYPAL 4× SOUS CONDITIONS » tenait sur UNE ligne et
     poussait « Prendre ma place » hors du billet (capture d'Eddy, 360 px).
     Sur téléphone les mentions passent à la ligne, et rien ne dépasse. */
  .billet { min-width: 0; overflow: hidden; }
  .billet__talon > * { min-width: 0; }
  .billet__mention, .billet__serie { white-space: normal; }
}''', 'billet téléphone'))

# ── 4. la 404 ──────────────────────────────────────────────────────────────
p404 = os.path.join(P, '404.html')
t = lire(p404)
if '/* 19/09 : sous les chiffres */' not in t:
    i = t.find('.ko {')
    assert i > 0 and t.count('.ko {') == 1
    t = t[:i] + '/* 19/09 : sous les chiffres */ .code { line-height: 1; } ' + t[i:]
    t = t.replace('.ko { display: block; margin-top: .4rem;', '.ko { display: block; margin-top: .9rem; line-height: 1.25;', 1)
    assert 'margin-top: .9rem; line-height: 1.25;' in t
    ecrire(p404, t)
    print('  ok 404.html')
else:
    print('  (déjà fait : 404)')

# ── 5. la garantie du haut ─────────────────────────────────────────────────
patch('src/three/hero.ts', lambda t: rem(t, '''    crest.scale.setScalar(s);
    crest.position.y = py;
''', '''    /* LA GARANTIE DU HAUT (19/09). Celle du bas existait ; rien ne tenait le
       HAUT, et sur une fenêtre large et basse le mot-symbole passait sous la
       barre (capture d'Eddy). Même méthode : on lit le bas réel de la barre
       (offsetHeight : insensible à sa disparition au défilement), on réduit
       si la bande entre la barre et le texte est trop courte, puis on cale. */
    {
      const barre = document.getElementById("nav");
      const basBarre = (barre ? barre.offsetHeight : 72) + 14;
      const limiteHaute = (0.5 - basBarre / h) * visH;
      const accroche = document.querySelector(".hero__hook") as HTMLElement | null;
      const hautAccroche = accroche ? accroche.getBoundingClientRect().top : 0;
      const limiteBasse = hautAccroche > 0 ? (0.5 - (hautAccroche - 24) / h) * visH : -visH / 2;
      const bande = limiteHaute - limiteBasse;
      if (bande > 0 && crestH * s > bande) s = bande / crestH;
      py = Math.min(py, limiteHaute - (crestH * s) / 2);
      py = Math.max(py, limiteBasse + (crestH * s) / 2);
    }
    crest.scale.setScalar(s);
    crest.position.y = py;
''', 'garantie du haut'))
print('sections vides, billet, 404, mot-symbole : appliqués')
