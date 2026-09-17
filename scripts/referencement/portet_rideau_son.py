# -*- coding: utf-8 -*-
"""
Portet, 17/09 (Eddy) : le rideau se lève tout seul, mais le son arrivait
APRÈS le mot-symbole — l'ambiance (3,9 Mo !) n'était même pas demandée avant
le premier clic — et la page bégayait pendant la formation du mot-symbole :
les scènes 3D suivantes compilaient leurs shaders (150 à 400 ms chacune,
mesuré) au même moment.

  1. audio.ts  — préchargement SANS geste pendant le rideau (l'ambiance en
     mémoire, les coups en brut) ; tentative de lecture automatique à la
     levée ; repli au premier geste ; le whoosh quand le mot-symbole part,
     le boom quand il se verrouille.
  2. enter.ts  — la barre attend aussi l'ambiance ; à la levée, le son part ;
     le rideau parti, il le dit (bcp:rideau-parti).
  3. hero.ts   — deux événements : bcp:crest-debut, bcp:crest.
  4. main.ts   — la fenêtre du mot-symbole : les scènes 3D attendent qu'il
     soit verrouillé, puis se montent une par une, au repos.
  5. scroll.ts — ScrollTrigger remesure quand le rideau est parti (overflow
     hidden retiré = la page change de taille).
Fins de ligne CRLF conservées ; chaque remplacement vérifie son compte.
"""
import io, os, sys
sys.stdout.reconfigure(encoding='utf-8')
P = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Portet', 'boxing-center-portet')


def lire(p):
    return io.open(p, encoding='utf-8', newline='').read()


def ecrire(p, t):
    io.open(p, 'w', encoding='utf-8', newline='').write(t)


def rem(t, avant, apres, nom, n=1):
    for a, b in ((avant, apres), (avant.replace('\n', '\r\n'), apres.replace('\n', '\r\n'))):
        if t.count(a) == n:
            return t.replace(a, b)
    if avant not in t and avant.replace('\n', '\r\n') not in t and (apres in t or apres.replace('\n', '\r\n') in t):
        print('  (déjà fait :', nom + ')')
        return t
    raise AssertionError(f'{nom} : {t.count(avant)} / {t.count(avant.replace(chr(10), chr(13) + chr(10)))} occurrence(s) pour {avant[:80]!r}')


def patch(rel, *ops):
    p = os.path.join(P, rel)
    t = lire(p)
    for op in ops:
        t = op(t)
    ecrire(p, t)
    print('  ok', rel)


# ── 1. audio.ts ────────────────────────────────────────────────────────────
patch('src/audio.ts',
      lambda t: rem(t, '''function ensureAmbient() {
  if (!ambient) {
    ambient = new Audio("/sfx/ambient.mp3");
    ambient.loop = true;
    ambient.volume = 0;
    ambient.preload = "auto";
  }
  return ambient;
}''', '''/* L'ambiance : ambiance.mp3, mono 64 kbit/s (948 Ko). L'ancien fichier
   pesait 3,9 Mo en stéréo 256 kbit/s — pour un fond qu'on met à 16 %. */
const AMBIANCE = "/sfx/ambiance.mp3";
function ensureAmbient(src: string = AMBIANCE) {
  if (!ambient) {
    ambient = new Audio();
    ambient.loop = true;
    ambient.volume = 0;
    ambient.preload = "auto";
    ambient.src = src;
  }
  return ambient;
}

/* PRÉCHARGEMENT SANS GESTE — autorisé par tous les navigateurs : seul le
   JOUER exige un geste, pas le charger. Appelé par le rideau dès qu'il
   apparaît : l'ambiance arrive en mémoire (blob), les coups en brut, et la
   barre du rideau attend l'ambiance. À la levée, tout est prêt à partir
   dans la même image que le mot-symbole. */
let ambiancePrete: Promise<void> | null = null;
const brut: Record<string, ArrayBuffer> = {};
export function preloadSound(): Promise<void> {
  if (ambiancePrete) return ambiancePrete;
  ambiancePrete = fetch(AMBIANCE)
    .then((r) => r.blob())
    .then((b) => { ensureAmbient(URL.createObjectURL(b)).load(); })
    .catch(() => {});
  ["whoosh", "boom", "bell"].forEach((n) =>
    fetch(`/sfx/${n}.mp3`).then((r) => r.arrayBuffer()).then((ab) => { brut[n] = ab; }).catch(() => {})
  );
  return ambiancePrete;
}

/* LA TENTATIVE À LA LEVÉE DU RIDEAU. Il n'y a plus de clic pour entrer, et
   un navigateur refuse un son sans geste… sauf s'il connaît déjà le site
   (Chrome : score d'engagement) ou si la visite vient d'un clic dans la
   session. On essaie : si ça passe, l'ambiance monte pendant que le
   mot-symbole se forme ; sinon on rend `false` et l'appelant arme le
   premier geste. Rien n'est marqué « activé » tant que rien ne joue. */
export async function tryAutoplay(): Promise<boolean> {
  if (enabled) return true;
  if (prefMuted()) return false;
  const a = ensureAmbient();
  try { await a.play(); } catch { return false; }
  enabled = true;
  ensure();
  fadeTo(AMB_GAIN);
  sync();
  chauffer();
  return true;
}

/* LE MOT-SYMBOLE ET LE SON, ENSEMBLE (Eddy, 17/09) : le whoosh quand les
   particules partent, le boom quand le mot se verrouille (hero.ts émet les
   deux). Silencieux si le son n'a pas encore le droit de jouer. */
window.addEventListener("bcp:crest-debut", () => whoosh());
window.addEventListener("bcp:crest", () => boom());''', 'ambiance + préchargement'),
      lambda t: rem(t, '''async function load(name: string) {
  if (name in buffers) return;
  buffers[name] = null;
  try {
    const res = await fetch(`/sfx/${name}.mp3`);
    buffers[name] = await ensure().decodeAudioData(await res.arrayBuffer());
  } catch {
    buffers[name] = null;
  }
}''', '''async function load(name: string) {
  if (name in buffers) return;
  buffers[name] = null;
  try {
    /* déjà en mémoire si le rideau l'a préchargé : pas de réseau */
    const ab = brut[name] || (await (await fetch(`/sfx/${name}.mp3`)).arrayBuffer());
    buffers[name] = await ensure().decodeAudioData(ab.slice(0));
  } catch {
    buffers[name] = null;
  }
}
/* les buffers se décodent au premier moment de repos, jamais dans le geste (INP) */
function chauffer() {
  const warm = () => FILES.forEach(load);
  if ("requestIdleCallback" in window) (window as any).requestIdleCallback(warm, { timeout: 1500 });
  else setTimeout(warm, 200);
}''', 'load depuis le brut'),
      lambda t: rem(t, '''export function resumeSound() {
  enabled = true;
  ensure();
  const a = ensureAmbient();
  a.play().then(() => fadeTo(AMB_GAIN)).catch(() => {});
  sync();
  // warm the SFX buffers AFTER the interaction returns (avoids a long task → INP hit)
  const warm = () => FILES.forEach(load);
  if ("requestIdleCallback" in window) (window as any).requestIdleCallback(warm, { timeout: 1500 });
  else setTimeout(warm, 200);
}''', '''export function resumeSound() {
  if (enabled) return;   // déjà parti à la levée du rideau : rien à refaire
  enabled = true;
  ensure();
  const a = ensureAmbient();
  a.play().then(() => fadeTo(AMB_GAIN)).catch(() => {});
  sync();
  chauffer();
}''', 'resumeSound idempotent'),
      lambda t: rem(t, 'const FILES = ["punch", "bell", "whoosh", "boom"];',
                    'const FILES = ["whoosh", "boom", "bell", "punch"];   // ordre du décodage : les coups du mot-symbole d\'abord', 'ordre FILES'))

# ── 2. enter.ts ────────────────────────────────────────────────────────────
patch('src/enter.ts',
      lambda t: rem(t, 'import { resumeSound, prefMuted } from "./audio";',
                    'import { resumeSound, prefMuted, preloadSound, tryAutoplay } from "./audio";', 'import'),
      lambda t: rem(t, '''  if (!prefMuted()) armGestureResume();

  let entered = false;
  try {
    entered = sessionStorage.getItem(KEY) === "1";
  } catch {}
  if (entered) return;''', '''  if (!prefMuted()) armGestureResume();   // un geste PENDANT le rideau débloque le son

  let entered = false;
  try {
    entered = sessionStorage.getItem(KEY) === "1";
  } catch {}
  if (entered) {
    /* pas de rideau dans la session : on essaie quand même de partir tout de
       suite (une visite venue d'un clic y a droit) ; sinon le geste attend */
    if (!prefMuted()) void tryAutoplay();
    return;
  }''', 'entrée sans rideau'),
      lambda t: rem(t, '''  /* +1 les polices, +1 la photo du hero. */
  const total = PRELOAD.length + 2;''', '''  /* +1 les polices, +1 la photo du hero, +1 l'ambiance sonore (Eddy, 17/09 :
     « give it time, the audio needs to load » — le son doit partir DANS LA
     MÊME IMAGE que le mot-symbole, pas après). */
  const total = PRELOAD.length + 3;''', 'total'),
      lambda t: rem(t, '''  (document.fonts?.ready || Promise.resolve()).then(bump).catch(bump);
''', '''  (document.fonts?.ready || Promise.resolve()).then(bump).catch(bump);
  /* L'AMBIANCE, en mémoire avant la levée. Son coupé par le visiteur : on ne
     charge rien et la case est cochée d'office. Le plafond de 6 s protège
     un réseau trop lent. */
  if (prefMuted()) bump();
  else preloadSound().then(bump, bump);
''', 'bump ambiance'),
      lambda t: rem(t, '''    gate.classList.add("gate--leve");
''', '''    gate.classList.add("gate--leve");
    /* LE SON PART ICI, avec le mot-symbole — pas au premier clic. Refusé
       par le navigateur (première visite, aucun geste) : le premier geste
       le lancera, il est déjà armé. */
    if (!prefMuted()) tryAutoplay().catch(() => false);
''', 'autoplay à la levée'),
      lambda t: rem(t, '''      document.documentElement.classList.remove("gated");
      disposeRing?.();
      gate.remove();
''', '''      document.documentElement.classList.remove("gated");
      disposeRing?.();
      gate.remove();
      /* la page retrouve sa vraie hauteur : ScrollTrigger doit remesurer */
      try { window.dispatchEvent(new Event("bcp:rideau-parti")); } catch {}
''', 'rideau parti'))

# ── 3. hero.ts ─────────────────────────────────────────────────────────────
patch('src/three/hero.ts',
      lambda t: rem(t, '''  let raf = 0;
  function frame() {''', '''  let raf = 0;
  let verrouille = false;
  function frame() {''', 'verrouille'),
      lambda t: rem(t, '''    if (!clock.running && !document.documentElement.classList.contains("gated")) clock.start();
    if (!clock.running) return;   // rideau encore là : les particules restent éparpillées
    const t = clock.getElapsedTime();
''', '''    if (!clock.running && !document.documentElement.classList.contains("gated")) {
      clock.start();
      /* les particules partent : le whoosh (audio.ts), et la fenêtre du
         mot-symbole s'ouvre (main.ts) */
      try { window.dispatchEvent(new Event("bcp:crest-debut")); } catch {}
    }
    if (!clock.running) return;   // rideau encore là : les particules restent éparpillées
    const t = clock.getElapsedTime();
    if (!verrouille && t >= FORM) {
      verrouille = true;
      /* le mot se verrouille : le boom, et les scènes 3D peuvent se monter */
      try { window.dispatchEvent(new Event("bcp:crest")); } catch {}
    }
''', 'événements crest'))

# ── 4. main.ts ─────────────────────────────────────────────────────────────
patch('src/main.ts',
      lambda t: rem(t, '''function lazy3D<T>(el: Element | null, loader: () => Promise<T>, init: (m: T) => void) {
  if (!el) return;
  const run = () => loader().then(init).catch(() => {});
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          io.disconnect();
          run();
        }
      },''', '''/* LA FENÊTRE DU MOT-SYMBOLE (Eddy, 17/09 : « le site lague »). Mesuré en
   ligne : chaque scène 3D (vitrine, ring, portails, forge) compile ses
   shaders en 150 à 400 ms d'un bloc, et les premières le faisaient PENDANT
   les 2,6 s où le mot-symbole se forme — la formation bégayait. Règle :
   tant que le mot-symbole n'est pas verrouillé (bcp:crest, ou 3,5 s après
   la levée du rideau), aucune scène ne se monte ; ensuite elles se montent
   UNE PAR UNE, chacune à un moment de repos du navigateur — jamais deux
   compilations dans la même image. Sur ordinateur, les scènes restantes se
   montent d'avance, dans l'ordre de la page : on ne compile plus rien
   pendant un défilement. Sur téléphone, elles restent paresseuses (mémoire). */
type Scene3D = { run: () => Promise<unknown>; faite: boolean };
const scenes3D: Scene3D[] = [];
const file3D: Scene3D[] = [];
let fenetreMotSymbole = false;
let pompe3D = false;
const auRepos = (fn: () => void, timeout = 900) => {
  const ric = (window as any).requestIdleCallback;
  if (typeof ric === "function") ric(fn, { timeout }); else window.setTimeout(fn, 120);
};
function pomper3D() {
  if (fenetreMotSymbole || pompe3D) return;
  const s = file3D.shift();
  if (!s) return;
  if (s.faite) { pomper3D(); return; }
  pompe3D = true;
  s.faite = true;
  auRepos(() => { Promise.resolve(s.run()).finally(() => auRepos(() => { pompe3D = false; pomper3D(); })); });
}
function ouvrirFenetre3D() {
  if (!fenetreMotSymbole) return;
  fenetreMotSymbole = false;
  if (window.innerWidth >= 1024) scenes3D.forEach((s) => { if (!s.faite && !file3D.includes(s)) file3D.push(s); });
  pomper3D();
}
function armerFenetre3D() {
  fenetreMotSymbole = document.documentElement.classList.contains("gated");
  if (!fenetreMotSymbole) return;
  window.addEventListener("bcp:crest", ouvrirFenetre3D, { once: true });
  window.addEventListener("bcp:entre", () => window.setTimeout(ouvrirFenetre3D, 3500), { once: true });
}

function lazy3D<T>(el: Element | null, loader: () => Promise<T>, init: (m: T) => void) {
  if (!el) return;
  const scene: Scene3D = { run: () => loader().then(init).catch(() => {}), faite: false };
  scenes3D.push(scene);
  const run = () => { if (!scene.faite && !file3D.includes(scene)) file3D.push(scene); pomper3D(); };
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          io.disconnect();
          run();
        }
      },''', 'fenêtre 3D'),
      lambda t: rem(t, '''function bootOnce() {
  initEnterGate();
''', '''function bootOnce() {
  initEnterGate();
  armerFenetre3D();   // juste après le rideau : c'est lui qui pose html.gated
''', 'armer fenêtre'))

# ── 5. scroll.ts ───────────────────────────────────────────────────────────
patch('src/scroll.ts',
      lambda t: rem(t, '''export function initScroll() {
  if (started) return lenis;
  started = true;
''', '''export function initScroll() {
  if (started) return lenis;
  started = true;
  /* le rideau parti, la page retrouve sa hauteur (overflow: hidden retiré) :
     les déclencheurs mesurés pendant le rideau seraient faux */
  window.addEventListener("bcp:rideau-parti", () => ScrollTrigger.refresh());
''', 'refresh après rideau'))
print('rideau + son + fenêtre 3D : appliqués')
