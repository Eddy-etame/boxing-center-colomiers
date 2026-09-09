/**
 * LA VIGNETTE DE PARTAGE — une par page, dessinée au build.
 *
 * Quand une page de ce site est partagée, collée dans une messagerie ou citée
 * par un moteur de réponse, c'est cette image qu'on voit en premier. Elle
 * n'est donc jamais une photo de salle interchangeable : elle dit, avec la
 * couleur et le trait de CE site, ce que CETTE page répond — le titre, la
 * ville, les deux clubs et les lignes qui y mènent — sur l'encre du site.
 *
 * Composée par satori depuis le registre (titre, description, clubs, lignes,
 * teinte), tramée par resvg, servie en PNG 1200 × 630. Les polices sont
 * celles du site, en TTF pour le rendu hors navigateur. Aucun texte n'est
 * tapé ici : une page qui change de titre change de vignette.
 */
import type { APIRoute, GetStaticPaths } from 'astro';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import satori from 'satori';
import { Resvg } from '@resvg/resvg-js';
import { ROUTES } from '../../data/routes';
import { SITE, CLUBS } from '../../data/verite';
import { CONTEXTE_GEO } from '../../data/mots-cles';

/** Colomiers est le point de départ, jamais une adresse de club : la ville vit dans le contexte géographique. */
const VILLE = CONTEXTE_GEO.ville;
const CODE_POSTAL = CONTEXTE_GEO.codePostal;
import { itineraireDuClub } from '../../data/transports';
import { TEINTE as T } from '../../data/teinte';

export const prerender = true;

/** Toutes les routes, y compris celles hors index : une page partagée a toujours sa vignette. */
export const getStaticPaths: GetStaticPaths = () => ROUTES.map((r) => ({ params: { page: r.id } }));

const police = (nom: string) => readFileSync(resolve(process.cwd(), 'src/og/fonts', nom));
const POLICES = [
  { name: 'Bricolage Grotesque', data: police('bricolage-grotesque-700.ttf'), weight: 700 as const, style: 'normal' as const },
  { name: 'Instrument Sans', data: police('instrument-sans-400.ttf'), weight: 400 as const, style: 'normal' as const },
  { name: 'Instrument Sans', data: police('instrument-sans-600.ttf'), weight: 600 as const, style: 'normal' as const },
  { name: 'JetBrains Mono', data: police('jetbrains-mono-400.ttf'), weight: 400 as const, style: 'normal' as const },
  { name: 'JetBrains Mono', data: police('jetbrains-mono-700.ttf'), weight: 700 as const, style: 'normal' as const },
];

/** Un nœud satori : le même arbre que JSX, sans JSX. */
type Noeud = { type: string; props: Record<string, unknown> };
const h = (type: string, props: Record<string, unknown>, ...enfants: unknown[]): Noeud => ({
  type,
  props: { ...props, children: enfants.length === 1 ? enfants[0] : enfants },
});

const MONO = 'JetBrains Mono';
const TITRE = 'Bricolage Grotesque';
const TEXTE = 'Instrument Sans';

const [SC, PT] = CLUBS;
const codes = (id: (typeof CLUBS)[number]['id']) =>
  itineraireDuClub(id)?.etapes.map((e) => e.code).join(' → ') ?? '';

/** Le titre, avec le lieu en couleur : la ville du site, sinon la commune de la page. */
function titreColore(titre: string, lieu: string): unknown[] {
  const i = titre.indexOf(lieu);
  if (i < 0) return [titre];
  return [
    titre.slice(0, i),
    h('span', { style: { color: T.signalTexte } }, lieu),
    titre.slice(i + lieu.length),
  ].filter((x) => x !== '');
}

/** L'aiguillage, réduit : une route, deux branches, deux clubs. */
const aiguillage = () =>
  h(
    'div',
    { style: { position: 'relative', width: 380, height: 300, display: 'flex' } },
    h(
      'svg',
      { width: 380, height: 300, viewBox: '0 0 380 300' },
      h('path', { d: 'M 40 150 H 180', stroke: T.trait, strokeWidth: 2, fill: 'none' }),
      h('path', { d: 'M 40 150 H 180', stroke: T.signalTexte, strokeWidth: 4, fill: 'none' }),
      h('path', { d: 'M 180 150 L 340 60', stroke: T.signalTexte, strokeWidth: 4, fill: 'none' }),
      h('path', { d: 'M 180 150 L 340 240', stroke: T.signalTexte, strokeWidth: 4, fill: 'none' }),
      h('circle', { cx: 40, cy: 150, r: 9, fill: T.encre }),
      h('circle', { cx: 180, cy: 150, r: 13, fill: T.papier, stroke: T.signalTexte, strokeWidth: 2 }),
      h('circle', { cx: 340, cy: 60, r: 18, fill: 'none', stroke: T.signalTexte, strokeWidth: 2.5 }),
      h('circle', { cx: 340, cy: 60, r: 8, fill: T.signalTexte }),
      h('circle', { cx: 340, cy: 240, r: 18, fill: 'none', stroke: T.signalTexte, strokeWidth: 2.5 }),
      h('circle', { cx: 340, cy: 240, r: 8, fill: T.signalTexte })
    ),
    etiquette(VILLE.toUpperCase(), 0, 118, 'flex-start', T.encre),
    etiquette('DEUX CLUBS', 40, 162, 'flex-start', T.graphite, 12),
    etiquette(SC.nomCourt.toUpperCase(), 170, 14, 'flex-end', T.encre),
    /* Les codes de ligne se posent SUR la branche, comme sur un plan de réseau :
       le papier derrière le texte interrompt le trait. */
    pastille(codes(SC.id), 260, 105),
    etiquette(PT.nomCourt.toUpperCase(), 170, 268, 'flex-end', T.encre),
    pastille(codes(PT.id), 260, 195)
  );

function pastille(texte: string, cx: number, cy: number): Noeud {
  return h(
    'div',
    {
      style: {
        position: 'absolute',
        left: cx - 95,
        top: cy - 12,
        width: 190,
        display: 'flex',
        justifyContent: 'center',
      },
    },
    h(
      'span',
      {
        style: {
          padding: '2px 10px',
          background: T.papier,
          fontFamily: MONO,
          fontWeight: 700,
          fontSize: 14,
          letterSpacing: 1.5,
          color: T.signalTexte,
        },
      },
      texte
    )
  );
}

function etiquette(texte: string, left: number, top: number, justify: string, couleur: string, taille = 15): Noeud {
  return h(
    'div',
    {
      style: {
        position: 'absolute',
        left,
        top,
        width: 190,
        display: 'flex',
        justifyContent: justify,
        fontFamily: MONO,
        fontWeight: 700,
        fontSize: taille,
        letterSpacing: 1.5,
        color: couleur,
      },
    },
    texte
  );
}

export const GET: APIRoute = async ({ params }) => {
  const r = ROUTES.find((x) => x.id === params.page);
  if (!r) return new Response('Page inconnue', { status: 404 });

  const titre = r.titre.split('|')[0].trim();
  const lieu = titre.includes(VILLE) ? VILLE : r.nav;
  const domaine = SITE.origine.replace(/^https?:\/\/(www\.)?/, '');

  const arbre = h(
    'div',
    {
      style: {
        width: 1200,
        height: 630,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        padding: '56px 64px 52px',
        background: T.papier,
        color: T.encre,
        fontFamily: TEXTE,
      },
    },
    /* Le cartouche */
    h(
      'div',
      {
        style: {
          display: 'flex',
          alignItems: 'center',
          gap: 14,
          paddingBottom: 18,
          borderBottom: `2px solid ${T.trait}`,
          fontFamily: MONO,
          fontSize: 20,
          letterSpacing: 3,
          color: T.graphite,
        },
      },
      h('span', { style: { color: T.signalTexte, fontWeight: 700 } }, 'BOXING CENTER'),
      h('span', {}, '·'),
      h('span', {}, `À PROXIMITÉ DE ${VILLE.toUpperCase()}`)
    ),
    /* Le corps : le titre à gauche, le dessin à droite */
    h(
      'div',
      { style: { display: 'flex', alignItems: 'center', gap: 40, flex: 1 } },
      h(
        'div',
        {
          style: {
            display: 'flex',
            flexDirection: 'column',
            gap: 22,
            width: 700,
            paddingLeft: 26,
            borderLeft: `5px solid ${T.signal}`,
          },
        },
        h(
          'div',
          {
            style: {
              display: 'flex',
              flexWrap: 'wrap',
              fontFamily: TITRE,
              fontWeight: 700,
              fontSize: titre.length > 44 ? 54 : 62,
              lineHeight: 1.04,
              letterSpacing: -1.5,
            },
          },
          ...titreColore(titre, lieu)
        ),
        h(
          'div',
          { style: { display: 'flex', fontSize: 25, lineHeight: 1.35, color: T.graphite } },
          r.description
        )
      ),
      aiguillage()
    ),
    /* Le pied : les deux clubs, et le domaine */
    h(
      'div',
      {
        style: {
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-end',
          gap: 32,
          paddingTop: 18,
          borderTop: `2px solid ${T.trait}`,
          fontFamily: MONO,
          fontSize: 15,
          letterSpacing: 0.5,
          color: T.graphite,
        },
      },
      h(
        'div',
        { style: { display: 'flex', flexDirection: 'column', gap: 6, flexShrink: 1 } },
        ...CLUBS.map((c) =>
          h(
            'div',
            { style: { display: 'flex', gap: 12 } },
            h('span', { style: { color: T.encre, fontWeight: 700 } }, c.nomCourt.toUpperCase()),
            h('span', {}, c.adresse)
          )
        )
      ),
      h('span', { style: { color: T.signalTexte, fontWeight: 700, whiteSpace: 'nowrap', flexShrink: 0 } }, domaine)
    )
  );

  const svg = await satori(arbre as never, { width: 1200, height: 630, fonts: POLICES });
  const png = new Resvg(svg, { fitTo: { mode: 'width', value: 1200 }, font: { loadSystemFonts: false } })
    .render()
    .asPng();

  return new Response(new Uint8Array(png), {
    headers: { 'content-type': 'image/png', 'cache-control': 'public, max-age=86400' },
  });
};
