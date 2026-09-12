/**
 * LA VIGNETTE — l'image à côté du résultat Google, dans un partage WhatsApp
 * ou Facebook, et dans les réponses des moteurs d'IA qui montrent une image.
 *
 * Google la recadre en carré au centre et l'affiche vers 100 px : à cette
 * taille, seuls une photo forte et un mot énorme se lisent. Elle est donc
 * composée depuis le centre : la vraie salle en fond (la photo de CETTE
 * page), assombrie dans la teinte du site, et le lieu en très grand au
 * milieu. Le sujet, le club et la ligne se lisent dans un partage en grand
 * et tombent sans dommage quand le carré les coupe.
 *
 * Deux formats par page, servis en JPEG : 1200 × 630 (og:image, partages)
 * et 1200 × 1200 (carré, annoncé dans le JSON-LD : c'est celui que Google
 * préfère pour une vignette). Tout vient du registre : une page qui change
 * de photo ou de sujet change de vignette.
 */
import type { APIRoute, GetStaticPaths } from 'astro';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import sharp from 'sharp';
import satori from 'satori';
import { Resvg } from '@resvg/resvg-js';
import { ROUTES } from '../../data/routes';
import { SITE } from '../../data/verite';
import { TEINTE as T } from '../../data/teinte';
import {
  VILLE_SITE,
  CLUB_VIGNETTE,
  LIGNE_VIGNETTE,
  photoDeLaRoute,
  lieuDeLaRoute,
  etiquetteDeLaRoute,
} from '../../data/vignettes';

export const prerender = true;

const FORMATS: Record<string, readonly [number, number]> = { '': [1200, 630], '-carre': [1200, 1200] };

export const getStaticPaths: GetStaticPaths = () =>
  ROUTES.flatMap((r) => Object.keys(FORMATS).map((f) => ({ params: { page: `${r.id}${f}` } })));

const police = (nom: string) => readFileSync(resolve(process.cwd(), 'src/og/fonts', nom));
const POLICES = [
  { name: 'Bricolage Grotesque', data: police('bricolage-grotesque-700.ttf'), weight: 700 as const, style: 'normal' as const },
  { name: 'Instrument Sans', data: police('instrument-sans-600.ttf'), weight: 600 as const, style: 'normal' as const },
  { name: 'JetBrains Mono', data: police('jetbrains-mono-700.ttf'), weight: 700 as const, style: 'normal' as const },
];

type Noeud = { type: string; props: Record<string, unknown> };
const h = (type: string, props: Record<string, unknown>, ...enfants: unknown[]): Noeud => ({
  type,
  props: { ...props, children: enfants.length === 1 ? enfants[0] : enfants },
});

/** La teinte sombre et la teinte claire du site, quel que soit le sens du thème. */
const luminance = (hex: string) => {
  const n = parseInt(hex.replace('#', '').slice(0, 6), 16);
  const [r, g, b] = [(n >> 16) & 255, (n >> 8) & 255, n & 255].map((v) => {
    const c = v / 255;
    return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};
const SOMBRE = luminance(T.encre) < luminance(T.papier) ? T.encre : T.papier;
const CLAIR = SOMBRE === T.encre ? T.papier : T.encre;
const rgba = (hex: string, a: number) => {
  const n = parseInt(hex.replace('#', '').slice(0, 6), 16);
  return `rgba(${(n >> 16) & 255}, ${(n >> 8) & 255}, ${n & 255}, ${a})`;
};

/** Un nom long se coupe en deux lignes à un trait d'union, au plus près du milieu. */
function lignesDuLieu(lieu: string): string[] {
  const L = lieu.toUpperCase();
  if (L.length <= 13 || !L.includes('-')) return [L];
  const tirets = [...L.matchAll(/-/g)].map((m) => m.index ?? 0);
  const coupe = tirets.reduce((a, b) => (Math.abs(b - L.length / 2) < Math.abs(a - L.length / 2) ? b : a));
  return [L.slice(0, coupe + 1), L.slice(coupe + 1)];
}

async function fond(slug: string, w: number, h2: number) {
  const src = resolve(process.cwd(), 'public/photos', `${slug}-1440.jpg`);
  const buf = await sharp(src)
    .resize(w, h2, { fit: 'cover', position: sharp.strategy.attention })
    .modulate({ saturation: 0.92 })
    .jpeg({ quality: 86 })
    .toBuffer();
  return `data:image/jpeg;base64,${buf.toString('base64')}`;
}

export const GET: APIRoute = async ({ params }) => {
  const brut = String(params.page);
  const suffixe = brut.endsWith('-carre') ? '-carre' : '';
  const id = suffixe ? brut.slice(0, -suffixe.length) : brut;
  const r = ROUTES.find((x) => x.id === id);
  if (!r) return new Response('Page inconnue', { status: 404 });
  const [W, H] = FORMATS[suffixe];
  const carre = W === H;

  const lignes = lignesDuLieu(lieuDeLaRoute(id));
  const plusLongue = Math.max(...lignes.map((l) => l.length));
  const largeurUtile = carre ? 1040 : 1000;
  const taille = Math.min(carre ? 250 : 190, Math.floor(largeurUtile / (plusLongue * 0.64)));
  const domaine = SITE.origine.replace(/^https?:\/\/(www\.)?/, '');
  const sousTitre = [CLUB_VIGNETTE, LIGNE_VIGNETTE].filter(Boolean).join('  ·  ');

  const arbre = h(
    'div',
    { style: { width: W, height: H, display: 'flex', position: 'relative', background: SOMBRE, fontFamily: 'Instrument Sans' } },
    h('img', { src: await fond(photoDeLaRoute(id), W, H), width: W, height: H, style: { position: 'absolute', left: 0, top: 0 } }),
    /* La teinte du site descend sur la photo : le texte se lit, la salle reste. */
    h('div', {
      style: {
        position: 'absolute', left: 0, top: 0, width: W, height: H, display: 'flex',
        backgroundImage: `linear-gradient(180deg, ${rgba(SOMBRE, 0.28)} 0%, ${rgba(SOMBRE, 0.5)} 42%, ${rgba(SOMBRE, 0.9)} 86%, ${rgba(SOMBRE, 0.97)} 100%)`,
      },
    }),
    h('div', {
      style: {
        position: 'absolute', left: 0, top: 0, width: W, height: H, display: 'flex',
        backgroundImage: `radial-gradient(ellipse at center, ${rgba(SOMBRE, 0.55)} 0%, ${rgba(SOMBRE, 0)} 62%)`,
      },
    }),
    /* Le centre : ce que le carré garde. */
    h(
      'div',
      {
        style: {
          position: 'absolute', left: 0, top: 0, width: W, height: H, display: 'flex',
          flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: carre ? 26 : 18,
          paddingBottom: carre ? 40 : 30,
        },
      },
      h(
        'div',
        {
          style: {
            display: 'flex', alignItems: 'center', gap: 14, fontFamily: 'JetBrains Mono', fontWeight: 700,
            fontSize: carre ? 30 : 24, letterSpacing: 5, color: CLAIR,
            textShadow: `0 2px 12px ${rgba(SOMBRE, 0.8)}`,
          },
        },
        h('div', { style: { width: 14, height: 14, borderRadius: 7, background: T.signal, display: 'flex' } }),
        etiquetteDeLaRoute(id).toUpperCase()
      ),
      h(
        'div',
        {
          style: {
            display: 'flex', flexDirection: 'column', alignItems: 'center',
            fontFamily: 'Bricolage Grotesque', fontWeight: 700, fontSize: taille, lineHeight: 0.92,
            letterSpacing: -taille * 0.03, color: CLAIR, textShadow: `0 6px 36px ${rgba(SOMBRE, 0.85)}`,
          },
        },
        ...lignes.map((l) => h('div', { style: { display: 'flex' } }, l))
      ),
      h('div', { style: { width: carre ? 150 : 120, height: carre ? 10 : 8, background: T.signal, display: 'flex', borderRadius: 2 } }),
      h(
        'div',
        {
          style: {
            display: 'flex', fontSize: carre ? 34 : 28, fontWeight: 600, color: CLAIR, opacity: 0.94,
            textShadow: `0 2px 14px ${rgba(SOMBRE, 0.9)}`, maxWidth: largeurUtile, textAlign: 'center',
          },
        },
        sousTitre
      )
    ),
    /* La marque et le domaine, en bas : lisibles en grand, coupés sans dommage en carré. */
    h(
      'div',
      {
        style: {
          position: 'absolute', left: 0, bottom: 0, width: W, height: carre ? 110 : 84, display: 'flex',
          alignItems: 'center', justifyContent: 'space-between', padding: carre ? '0 56px' : '0 48px',
          fontFamily: 'JetBrains Mono', fontWeight: 700, fontSize: carre ? 24 : 20, letterSpacing: 3, color: CLAIR,
        },
      },
      h('div', { style: { display: 'flex', color: T.signal } }, 'BOXING CENTER'),
      h('div', { style: { display: 'flex', opacity: 0.9 } }, carre ? `À PROXIMITÉ DE ${VILLE_SITE.toUpperCase()}` : domaine)
    )
  );

  const svg = await satori(arbre as never, { width: W, height: H, fonts: POLICES });
  const png = new Resvg(svg, { fitTo: { mode: 'width', value: W }, font: { loadSystemFonts: false } }).render().asPng();
  const jpg = await sharp(png).jpeg({ quality: 84, mozjpeg: true }).toBuffer();

  return new Response(new Uint8Array(jpg), {
    headers: { 'content-type': 'image/jpeg', 'cache-control': 'public, max-age=86400' },
  });
};
