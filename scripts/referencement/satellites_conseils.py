# -*- coding: utf-8 -*-
"""
Pose la section /conseils/ sur un site de proximité (Eddy, 1er/10/2026 : des
articles sur chaque site, qui mènent à la boutique de matériel).

Le TEXTE est propre à chaque site : scripts/referencement/conseils/<site>.json
(une phrase, un site — mesuré par conseils_doublons.py). Le CODE est commun :
  · src/data/conseils.ts               écrit depuis le JSON du site
  · src/components/PageConseil.astro   le gabarit d'un article
  · src/pages/conseils.astro           l'index
  · src/pages/conseils/<slug>.astro    une page par article
et quatre raccords, posés une fois, vérifiés à chaque passage :
  · src/data/routes.ts      les routes (donc le plan du site, llms.txt, la vignette)
  · src/data/vignettes.ts   le sujet et la photo de chaque vignette — jamais la même
  · src/layouts/Base.astro  le JSON-LD Article et le fil d'Ariane à trois niveaux
  · src/components/PiedDePage.astro  le lien, sur chaque page du site

Usage : python satellites_conseils.py colomiers [muret …]
Le script refuse d'écrire si un titre déborde, si une description sort de
80–158 caractères, si une photo n'existe pas, ou si un raccord ne trouve plus
son point d'ancrage.
"""
import io, json, os, re, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')

ICI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ICI, 'conseils')
DEPLOIEMENT = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment')


def lire(p):
    return io.open(p, encoding='utf-8', newline='').read()


def ecrire(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


def q(t):
    """Une chaîne TypeScript entre apostrophes droites, comme le reste des registres."""
    return "'" + t.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n') + "'"


def typo(v):
    """L'espace insécable du français devant : ; ? ! » et après « — un titre ne passe jamais à la ligne sur un deux-points."""
    if isinstance(v, str):
        return re.sub(r'« ', '« ', re.sub(r' ([:;?!»])', ' \\1', v))
    if isinstance(v, list):
        return [typo(x) for x in v]
    if isinstance(v, dict):
        return {k: (x if k in ('id', 'photo', 'route', 'publie', 'maj') else typo(x)) for k, x in v.items()}
    return v


def ts(v, n=0):
    """Une valeur écrite en TypeScript, au style des registres : clés nues, chaînes entre apostrophes."""
    pad, pad2 = '  ' * n, '  ' * (n + 1)
    if isinstance(v, str):
        return q(v)
    if isinstance(v, (int, float)):
        return json.dumps(v)
    if isinstance(v, list):
        if all(isinstance(x, str) for x in v) and sum(len(x) for x in v) < 90:
            return '[' + ', '.join(q(x) for x in v) + ']'
        return '[\n' + ''.join('%s%s,\n' % (pad2, ts(x, n + 1)) for x in v) + pad + ']'
    if isinstance(v, dict):
        cle = lambda k: k if re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', k) else q(k)
        if all(isinstance(x, str) for x in v.values()) and sum(len(x) for x in v.values()) < 70:
            return '{ ' + ', '.join('%s: %s' % (cle(k), q(x)) for k, x in v.items()) + ' }'
        return '{\n' + ''.join('%s%s: %s,\n' % (pad2, cle(k), ts(x, n + 1)) for k, x in v.items()) + pad + '}'
    raise TypeError(type(v))


def poser(s, ancre, neuf, ou, avant=True):
    """Insère `neuf` avant (ou après) `ancre`, qui doit exister une seule fois."""
    n = s.count(ancre)
    if n != 1:
        raise SystemExit('✗ %s : ancre trouvée %d fois — « %s »' % (ou, n, ancre[:70]))
    return s.replace(ancre, neuf + ancre if avant else ancre + neuf)


def entre(s, debut, fin, neuf, ancre, ou):
    """Remplace le bloc entre deux repères ; le pose avant `ancre` s'il n'existe pas encore."""
    if debut in s:
        a, b = s.index(debut), s.index(fin) + len(fin)
        return s[:a] + debut + neuf + fin + s[b:]
    return poser(s, ancre, debut + neuf + fin + '\n  ', ou)


def installer(site):
    racine = os.path.join(DEPLOIEMENT, 'boxing-center-' + site)
    D = json.load(io.open(os.path.join(SRC, site + '.json'), encoding='utf-8'))
    fautes = []
    nl = '\r\n' if '\r\n' in lire(os.path.join(racine, 'src', 'data', 'routes.ts')) else '\n'

    # ── les garde-fous sur le contenu ──────────────────────────────────────
    medias = lire(os.path.join(racine, 'src', 'data', 'medias.ts'))
    pages = [('conseils', D['index'])] + [(a['id'], a) for a in D['articles']]
    for ident, p in pages:
        if len(p['titre']) > 60:
            fautes.append('%s : titre de %d caractères' % (ident, len(p['titre'])))
        if not 80 <= len(p['description']) <= 158:
            fautes.append('%s : description de %d caractères' % (ident, len(p['description'])))
        if "slug: '%s'" % p['photo'] not in medias:
            fautes.append('%s : photo inconnue du manifeste — %s' % (ident, p['photo']))
        # la vignette se compose depuis ce fichier : sans lui, le build s'arrête au milieu
        if not os.path.exists(os.path.join(racine, 'public', 'photos', p['photo'] + '-1440.jpg')):
            fautes.append('%s : public/photos/%s-1440.jpg absent' % (ident, p['photo']))
    photos = [p['photo'] for _, p in pages]
    if len(set(photos)) != len(photos):
        fautes.append('deux pages partagent la même photo de vignette')
    for a in D['articles']:
        for qr in a['faq']:
            if re.search(r'\d\s?€', qr['texte']) and not re.search(r'\d{4}', qr['texte']):
                fautes.append('%s : la réponse « %s » cite un prix sans date' % (a['id'], qr['titre']))
        if not 4 <= len(a['sections']) <= 7:
            fautes.append('%s : %d sections (4 à 7)' % (a['id'], len(a['sections'])))
    if fautes:
        raise SystemExit('✗ %s\n  ' % site + '\n  '.join(fautes))

    # ── src/data/conseils.ts ───────────────────────────────────────────────
    ids = [a['id'] for a in D['articles']]
    articles = [{
        'id': a['id'], 'carte': a['carte'], 'h1': a['h1'], 'chapeau': a['chapeau'], 'resume': a['resume'],
        'photo': a['photo'], 'sujet': a['sujet'], 'publie': a.get('publie', D['publie']), 'maj': a.get('maj', D['publie']),
        'sections': a['sections'], **({'tableau': a['tableau']} if a.get('tableau') else {}), 'faq': a['faq'],
    } for a in D['articles']]
    index = {k: D['index'][k] for k in ('h1', 'chapeau', 'photo', 'sujet', 'finH2', 'finTexte')}
    conseils_ts = '''/**
 * LES CONSEILS — le texte des articles sur le matériel (/conseils/).
 *
 * Écrit pour ce site, et pour lui seul : aucune phrase d'ici n'existe sur un
 * autre site du réseau. Chaque conseil part de ce que les clubs publient
 * (src/data/offres.ts) et renvoie, depuis son texte, vers la boutique de
 * matériel du groupe, vers les pages du site et vers le club. Le titre et la
 * description de chaque page vivent dans le registre des routes.
 *
 * Les prix cités portent leur date ; « maj » est la date de la dernière
 * relecture du conseil, affichée sur la page.
 */

export type ConseilId = %(union)s;

export type Conseil = {
  id: ConseilId;
  /** l'étiquette de la carte, sur l'index */
  carte: string;
  h1: string;
  /** la réponse, en deux phrases qui se lisent seules */
  chapeau: string;
  resume: string;
  photo: string;
  /** la ligne de la vignette de partage */
  sujet: string;
  publie: string;
  maj: string;
  sections: readonly { sur: string; h2: string; paras: readonly string[] }[];
  tableau?: { sur: string; h2: string; entetes: readonly string[]; lignes: readonly (readonly string[])[]; note: string };
  faq: readonly { titre: string; texte: string }[];
};

export const INDEX_CONSEILS = %(index)s as const;

export const LIBELLES = %(libelles)s as const;

export const CONSEILS: readonly Conseil[] = %(articles)s;

export function conseil(id: ConseilId): Conseil {
  const c = CONSEILS.find((x) => x.id === id);
  if (!c) throw new Error(`Conseil inconnu : ${id}`);
  return c;
}

/** Le sujet et la photo de la vignette d'une page de conseils — jamais ceux d'une autre page. */
export function vignetteDuConseil(id: string): { sujet: string; photo: string } | undefined {
  if (id === 'conseils') return { sujet: INDEX_CONSEILS.sujet, photo: INDEX_CONSEILS.photo };
  const c = CONSEILS.find((x) => x.id === id);
  return c && { sujet: c.sujet, photo: c.photo };
}

/** « 2 octobre 2026 », depuis une date ISO. */
export function dateFr(iso: string): string {
  const d = new Intl.DateTimeFormat('fr-FR', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' }).format(new Date(`${iso}T12:00:00Z`));
  return d.replace(/^1 /, '1er ');
}
''' % {
        'union': ' | '.join("'%s'" % i for i in ids),
        'index': ts(typo(index)), 'libelles': ts(typo(D['libelles'])), 'articles': ts(typo(articles)),
    }
    ecrire(os.path.join(racine, 'src', 'data', 'conseils.ts'), conseils_ts.replace('\n', nl))

    # ── le gabarit, l'index, une page par article ──────────────────────────
    shutil.copyfile(os.path.join(SRC, 'PageConseil.astro'), os.path.join(racine, 'src', 'components', 'PageConseil.astro'))
    shutil.copyfile(os.path.join(SRC, 'conseils-index.astro'), os.path.join(racine, 'src', 'pages', 'conseils.astro'))
    dossier = os.path.join(racine, 'src', 'pages', 'conseils')
    if os.path.isdir(dossier):
        for f in os.listdir(dossier):
            if f.endswith('.astro') and f[:-6] not in ids:
                os.remove(os.path.join(dossier, f))
    for i in ids:
        ecrire(os.path.join(dossier, i + '.astro'), "---\nimport PageConseil from '../../components/PageConseil.astro';\n---\n\n<PageConseil id=\"%s\" />\n" % i)

    # ── src/data/routes.ts ─────────────────────────────────────────────────
    p = os.path.join(racine, 'src', 'data', 'routes.ts')
    s = lire(p).replace('\r\n', '\n')
    union = ''.join("\n  | '%s'" % i for i in ['conseils'] + ids) + '\n  '
    s = entre(s, '/* conseils:début */', '/* conseils:fin */', union, "| 'contact'", 'routes.ts (type)')

    def bloc(ident, chemin, x):
        return '''
  {
    id: %s,
    chemin: %s,
    nav: %s,
    question: %s,
    titre: %s,
    description:
      %s,
    menu: false,
    index: true,
  },''' % tuple(q(v) for v in (ident, chemin, x['nav'], x['question'], x['titre'], x['description']))

    routes = bloc('conseils', '/conseils/', D['index']) + ''.join(bloc(a['id'], '/conseils/%s/' % a['id'], a) for a in D['articles']) + '\n  '
    s = entre(s, '/* conseils:routes */', '/* conseils:routes:fin */', routes, "{\n    id: 'contact',", 'routes.ts (routes)')
    ecrire(p, s.replace('\n', nl))

    # ── src/data/vignettes.ts ──────────────────────────────────────────────
    p = os.path.join(racine, 'src', 'data', 'vignettes.ts')
    s = lire(p).replace('\r\n', '\n')
    if 'vignetteDuConseil' not in s:
        s = poser(s, "import { CONTENUS } from './contenus';", "import { vignetteDuConseil } from './conseils';\n", 'vignettes.ts (import)')
        s = poser(s, 'export function etiquetteDeLaRoute(id: string): string {\n',
                  "  /* un conseil porte son sujet tel quel : « Conseil · Poids des gants » */\n  const conseil = vignetteDuConseil(id);\n  if (conseil) return conseil.sujet;\n", 'vignettes.ts (étiquette)', avant=False)
        s = poser(s, 'export function photoDeLaRoute(id: string): string {\n',
                  "  const conseil = vignetteDuConseil(id);\n  if (conseil) return conseil.photo;\n", 'vignettes.ts (photo)', avant=False)
        ecrire(p, s.replace('\n', nl))

    # ── src/layouts/Base.astro ─────────────────────────────────────────────
    p = os.path.join(racine, 'src', 'layouts', 'Base.astro')
    s = lire(p).replace('\r\n', '\n')
    if 'article?:' not in s:
        s = poser(s, '  faq?: readonly { titre: string; texte: string }[];\n',
                  "  /** un conseil : sa date de publication et sa date de relecture — la page devient un Article */\n  article?: { publie: string; maj: string };\n", 'Base.astro (props)', avant=False)
        m = re.search(r', faq \} = Astro\.props;', s)
        if not m:
            raise SystemExit('✗ Base.astro : la ligne des props a changé de forme')
        s = s.replace(', faq } = Astro.props;', ', faq, article } = Astro.props;', 1)
        s = poser(s, "              { '@type': 'ListItem', position: 2, name: r.nav, item: canonique },\n",
                  "", 'Base.astro (fil)')
        s = s.replace("              { '@type': 'ListItem', position: 2, name: r.nav, item: canonique },\n",
                      "              /* un conseil se range sous /conseils/ : trois niveaux */\n"
                      "              ...(article\n"
                      "                ? [\n"
                      "                    { '@type': 'ListItem', position: 2, name: route('conseils').nav, item: new URL(route('conseils').chemin, SITE.origine).href },\n"
                      "                    { '@type': 'ListItem', position: 3, name: r.nav, item: canonique },\n"
                      "                  ]\n"
                      "                : [{ '@type': 'ListItem', position: 2, name: r.nav, item: canonique }]),\n", 1)
        m = re.search(r'    /\* FAQPage[^\n]*\n(?=    \.\.\.\(faq\?\.length\n)', s)
        s = poser(s, m.group(0) if m else "    ...(faq?.length\n",
                  "    /* Article — uniquement pour un conseil : ses dates sont celles de la page. */\n"
                  "    ...(article\n"
                  "      ? [\n"
                  "          {\n"
                  "            '@type': 'Article',\n"
                  "            '@id': `${canonique}#article`,\n"
                  "            headline: r.titre,\n"
                  "            description: r.description,\n"
                  "            inLanguage: SITE.langue,\n"
                  "            datePublished: article.publie,\n"
                  "            dateModified: article.maj,\n"
                  "            image: [og, ogCarre],\n"
                  "            mainEntityOfPage: { '@id': `${canonique}#page` },\n"
                  "            author: { '@id': `${SITE.origine}/#organisation` },\n"
                  "            publisher: { '@id': `${SITE.origine}/#organisation` },\n"
                  "          },\n"
                  "        ]\n"
                  "      : []),\n", 'Base.astro (Article)')
        s = poser(s, '<meta property="og:type" content="website" />', '', 'Base.astro (og:type)')
        s = s.replace('<meta property="og:type" content="website" />', "<meta property=\"og:type\" content={article ? 'article' : 'website'} />", 1)
        for attendu in ("'@id': `${canonique}#page`", "'@id': `${SITE.origine}/#organisation`", 'SITE.langue'):
            if attendu not in s:
                raise SystemExit('✗ Base.astro : repère absent — %s' % attendu)
        ecrire(p, s.replace('\n', nl))

    # ── src/components/PiedDePage.astro ────────────────────────────────────
    p = os.path.join(racine, 'src', 'components', 'PiedDePage.astro')
    s = lire(p).replace('\r\n', '\n')
    if 'href="/conseils/"' not in s and "route('conseils')" not in s:
        # le lien suit l'écriture du site : chemin en clair (Colomiers) ou lu au registre (les six autres)
        m = re.search(r'''\n( *)<li><a class="lien" href=("/premiere-seance/"|\{route\('premiere-seance'\)\.chemin\})>[^\n]*</a></li>\n''', s)
        if not m:
            raise SystemExit('✗ PiedDePage.astro : la ligne « Première séance » a changé de forme')
        href = '"/conseils/"' if m.group(2).startswith('"') else "{route('conseils').chemin}"
        s = s.replace(m.group(0), m.group(0) + '%s<li><a class="lien" href=%s>%s</a></li>\n' % (m.group(1), href, D['index']['pied']), 1)
        ecrire(p, s.replace('\n', nl))

    print('✓ %-14s /conseils/ + %d articles : %s' % (site, len(ids), ', '.join(ids)))


for site in sys.argv[1:]:
    installer(site)
