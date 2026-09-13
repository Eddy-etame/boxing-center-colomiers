# -*- coding: utf-8 -*-
"""
Portet — un lien vers une ancre (/tarifs/#tarif-baby-boxe) arrive sur SA carte :
après une navigation douce, sur la même page, et au chargement direct (une fois
le rideau d'entrée levé). Le routeur remontait toujours en haut de page.
"""
import io, os, sys
sys.stdout.reconfigure(encoding='utf-8')
P = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Portet', 'boxing-center-portet', 'src')


def lire(nom):
    t = io.open(os.path.join(P, nom), encoding='utf-8', newline='').read()
    return t.replace('\r\n', '\n'), '\r\n' in t


def ecrire(t, crlf, nom):
    io.open(os.path.join(P, nom), 'w', encoding='utf-8', newline='').write(t.replace('\n', '\r\n') if crlf else t)


def rem(t, avant, apres, nom):
    k = t.count(avant)
    assert k == 1, f'{nom} : {k} occurrence(s) pour {avant[:80]!r}'
    return t.replace(avant, apres)


t, crlf = lire('scroll.ts')
t = rem(t, '''export function scrollToTop(smooth = false) {
  if (lenis) {
    lenis.scrollTo(0, { immediate: !smooth });
  } else {
    window.scrollTo({ top: 0, behavior: smooth ? "smooth" : "auto" });
  }
}
''', '''export function scrollToTop(smooth = false) {
  if (lenis) {
    lenis.scrollTo(0, { immediate: !smooth });
  } else {
    window.scrollTo({ top: 0, behavior: smooth ? "smooth" : "auto" });
  }
}

/**
 * Va sur l'élément d'une ancre (#tarif-baby-boxe) et, si c'est une formule, la
 * fait signe. Renvoie false quand l'ancre n'existe pas sur la page.
 */
export function allerAncre(hash: string, smooth = true): boolean {
  let el: HTMLElement | null = null;
  try { el = document.getElementById(decodeURIComponent(String(hash || "").replace(/^#/, ""))); } catch {}
  if (!el) return false;
  const offset = -Math.round(Math.min(150, Math.max(96, window.innerHeight * 0.16)));
  if (lenis) lenis.scrollTo(el, { offset, immediate: !smooth, duration: 1.1 });
  else window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY + offset, behavior: smooth && !reduced ? "smooth" : "auto" });
  if (el.classList.contains("tarif")) {
    el.classList.remove("tarif--vise");
    void el.offsetWidth;
    el.classList.add("tarif--vise");
  }
  return true;
}

/**
 * Arrivée directe sur une URL à ancre (un lien depuis un autre site, un
 * favori) : on attend que le rideau d'entrée soit levé — html.gated bloque le
 * défilement —, puis on y va.
 */
export function allerAncreAuChargement() {
  const hash = location.hash;
  if (!hash || hash.length < 2) return;
  const debut = performance.now();
  const essai = () => {
    if (document.documentElement.classList.contains("gated") && performance.now() - debut < 12000) {
      window.setTimeout(essai, 150);
      return;
    }
    requestAnimationFrame(() => allerAncre(hash, true));
  };
  window.setTimeout(essai, 250);
}
''', 'scroll.ts')
ecrire(t, crlf, 'scroll.ts')

t, crlf = lire('router.ts')
t = rem(t, 'import { teardownPageScroll, scrollToTop } from "./scroll";',
        'import { teardownPageScroll, scrollToTop, allerAncre } from "./scroll";', 'router import')
t = rem(t, '''      if (url.pathname === cheminAffiche) {
        scrollToTop(true);
        return;''', '''      if (url.pathname === cheminAffiche) {
        if (url.hash && allerAncre(url.hash, true)) {
          history.replaceState({}, "", url.href);
          return;
        }
        scrollToTop(true);
        return;''', 'router même page')
t = rem(t, '''    scrollToTop(false);
    requestAnimationFrame(() => scrollToTop(false));''', '''    scrollToTop(false);
    requestAnimationFrame(() => {
      scrollToTop(false);
      /* Un lien vers une ancre (/tarifs/#tarif-baby-boxe) arrive sur SA
         carte, pas en haut de la page. */
      if (url.hash) requestAnimationFrame(() => allerAncre(url.hash, true));
    });''', 'router après rendu')
ecrire(t, crlf, 'router.ts')

t, crlf = lire('main.ts')
t = rem(t, 'import { initRouter } from "./router";\n',
        'import { initRouter } from "./router";\nimport { allerAncreAuChargement } from "./scroll";\n', 'main import')
t = rem(t, '''  initRouter(bootPage);
  if (import.meta.env.PROD) initGuard();''', '''  initRouter(bootPage);
  allerAncreAuChargement();
  if (import.meta.env.PROD) initGuard();''', 'main boot')
ecrire(t, crlf, 'main.ts')
print('ancres Portet appliquées')
