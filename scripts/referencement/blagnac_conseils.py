# -*- coding: utf-8 -*-
"""
Deux pages de conseil sur Club de Boxe Blagnac (Eddy, 1er/10/2026 : des
articles sur chaque site, qui mènent à la boutique de matériel).

Blagnac a son propre gabarit — IntentPage, nourri par src/data/copy.json — et
ses propres règles : vouvoiement, aucun prix, aucune adresse, gants et
protections prêtés pour commencer. Les deux pages répondent chacune à une
question que le site ne possédait pas :
  · /gants-de-boxe-enfant/  quelle taille de gants selon l'âge (éveil, éducative, ados)
  · /sac-de-sport-boxe/     que mettre dans son sac, dans l'ordre des achats
Chaque section porte ses liens : vers les pages du club, et vers Boutique de
Boxe (les rayons, les guides, l'outil).

Le script écrit les deux entrées de copy.json, les deux pages, et pose les
raccords (routes, pages publiques, plan du site, pied de page, bloc réseau,
contrat de mots-clés). Rejouable : il remplace ses propres entrées.
Usage : python blagnac_conseils.py
"""
import io, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
R = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment', 'club-de-boxe-blagnac')
B = 'https://www.boutique-de-boxe.com'


def lire(p):
    return io.open(os.path.join(R, p), encoding='utf-8', newline='').read()


def ecrire(p, s):
    os.makedirs(os.path.dirname(os.path.join(R, p)), exist_ok=True)
    io.open(os.path.join(R, p), 'w', encoding='utf-8', newline='').write(s)


def poser(p, ancre, neuf, avant=False, marque=None):
    s = lire(p)
    if (marque or neuf.strip()) in s:
        return
    nl = '\r\n' if '\r\n' in s else '\n'
    a = ancre.replace('\n', nl)
    if s.count(a) != 1:
        raise SystemExit('✗ %s : ancre trouvée %d fois — %s' % (p, s.count(a), ancre[:70]))
    n = neuf.replace('\n', nl)
    ecrire(p, s.replace(a, n + a if avant else a + n))


COPIES = {
    'gants-de-boxe-enfant': {
        'key': 'gants-de-boxe-enfant',
        'path': '/gants-de-boxe-enfant/',
        'label': 'Gants de boxe enfant',
        'question': 'Quels gants de boxe pour un enfant, et à partir de quand en acheter ?',
        'title': 'Gants de boxe enfant : quelle taille selon l’âge ? | Blagnac',
        'ogTitle': 'Gants de boxe pour un enfant : la bonne taille, au bon moment',
        'description': 'Gants de boxe enfant : 4 oz de 5 à 7 ans, 6 oz de 7 à 10 ans, 8 oz de 10 à 13 ans, 10 oz pour les ados. Au club de Blagnac, on les prête pour commencer.',
        'h1Main': 'Gants de boxe enfant',
        'h1Em': 'par âge',
        'eyebrow': 'Conseil · de 3 à 17 ans',
        'lead': 'Un enfant ne choisit pas ses gants comme un adulte : c’est son âge qui donne le poids. Comptez 4 oz de 5 à 7 ans, 6 oz de 7 à 10 ans, 8 oz de 10 à 13 ans et 10 oz pour un adolescent. Au Club de Boxe Blagnac, les gants sont prêtés pour commencer : n’achetez rien avant d’en avoir parlé à l’entraîneur.',
        'note': 'Repères repris du guide de Boutique de Boxe, la boutique de matériel du réseau Boxing Center. Le cours de votre enfant fixe le reste.',
        'sections': [
            {
                'eyebrow': 'Avant d’acheter',
                'h2': 'Au club, les gants sont prêtés pour débuter',
                'paragraphs': [
                    'Pour ses premières séances, votre enfant vient en tenue de sport : nous prêtons les gants et les protections à sa taille. C’est pour cela que nous demandons à être prévenus de sa venue.',
                    'L’achat vient ensuite, une fois inscrit, et après un mot avec l’entraîneur : il a vu la main de votre enfant dans un gant, et il sait ce que son cours lui demande.',
                ],
                'links': [
                    {'label': 'Comment se passe une première séance', 'href': '/premiere-seance/'},
                    {'label': 'Boxe enfant à Blagnac, de 3 à 17 ans', 'href': '/boxe-enfant-blagnac/'},
                ],
            },
            {
                'eyebrow': 'Le poids',
                'h2': '4, 6, 8 ou 10 oz : le poids suit l’âge',
                'paragraphs': [
                    'L’once mesure la quantité de mousse du gant, pas sa pointure. Chez l’enfant, on la choisit d’abord selon l’âge, puis on ajuste au gabarit.',
                    'Ce sont des repères, pas des règles : un enfant grand pour son âge passe plus tôt à la taille suivante, un enfant menu y reste une saison de plus. Un gant trop lourd fatigue l’épaule avant la fin du cours ; trop grand, il tourne autour du poignet.',
                ],
                'bullets': ['De 5 à 7 ans : 4 oz', 'De 7 à 10 ans : 6 oz', 'De 10 à 13 ans : 8 oz', 'Adolescents : 10 oz'],
                'links': [
                    {'label': 'Les tailles de gants, expliquées par Boutique de Boxe', 'href': B + '/guides/quelle-taille-gants-de-boxe/'},
                ],
            },
            {
                'eyebrow': 'Selon le cours',
                'h2': 'Éveil, boxe éducative, ados : trois besoins différents',
                'paragraphs': [
                    'En éveil, de 3 à 6 ans, il n’y a aucun contact et rien à acheter : les gants légers du club suffisent.',
                    'En boxe éducative, de 7 à 12 ans, la touche est légère : une paire à sa taille devient utile quand il vient chaque semaine. Dans le groupe ados, de 13 à 17 ans, l’opposition est encadrée, et le poids des gants se décide avec l’entraîneur, comme chez les adultes.',
                ],
                'links': [
                    {'label': 'Éveil baby boxing, dès 3 ans', 'href': '/cours-de-boxe-blagnac/eveil-baby-boxing/'},
                    {'label': 'Boxe éducative, de 7 à 12 ans', 'href': '/cours-de-boxe-blagnac/boxe-educative/'},
                    {'label': 'Boxe ados, de 13 à 17 ans', 'href': '/cours-de-boxe-blagnac/boxe-ados/'},
                ],
            },
            {
                'eyebrow': 'L’essayage',
                'h2': 'Vérifier un gant sur la main d’un enfant',
                'paragraphs': [
                    'Faites-lui fermer le poing dans le gant : les doigts arrivent au fond sans se replier, le pouce se loge sans forcer, et le scratch se ferme sur le poignet, pas sur l’avant-bras.',
                    'Préférez une fermeture à scratch, qu’il manipule seul. Et n’achetez pas une taille au-dessus pour gagner une saison : un gant trop grand ne protège ni sa main, ni celle du partenaire.',
                ],
                'links': [
                    {'label': 'Les gants de boxe enfant, Boutique de Boxe', 'href': B + '/gants-de-boxe-enfant/'},
                    {'label': 'Tout le matériel de boxe enfant, Boutique de Boxe', 'href': B + '/materiel-boxe-enfant/'},
                ],
            },
            {
                'eyebrow': 'Avec les gants',
                'h2': 'Ce qui s’achète en même temps, et ce que le club prête',
                'paragraphs': [
                    'Le premier achat n’est pas le gant : ce sont les bandes, puis, à partir de 7 ans, un protège-dents, obligatoire avant la première opposition, même légère. Les casques, les coquilles et les protège-tibias sont prêtés par le club.',
                ],
                'links': [
                    {'label': 'Le guide de l’équipement de boxe enfant, Boutique de Boxe', 'href': B + '/guides/equipement-enfant/'},
                    {'label': 'Que mettre dans le sac de sport', 'href': '/sac-de-sport-boxe/'},
                ],
            },
        ],
        'faq': [
            {'question': 'Quelle taille de gants de boxe pour un enfant de 8 ans ?', 'answer': '6 oz : c’est le repère de 7 à 10 ans. S’il est grand pour son âge ou proche de 10 ans, demandez à l’entraîneur s’il faut passer à 8 oz.'},
            {'question': 'Faut-il acheter des gants avant le premier cours de boxe d’un enfant ?', 'answer': 'Non. Au Club de Boxe Blagnac, les gants et les protections sont prêtés pour les premières séances : votre enfant vient en tenue de sport.'},
            {'question': 'Un enfant peut-il boxer avec des gants d’adulte ?', 'answer': 'Non : ils sont trop larges et trop lourds pour lui. La main flotte, le poignet n’est pas tenu, et l’épaule fatigue.'},
            {'question': 'Scratch ou lacets pour des gants d’enfant ?', 'answer': 'Scratch. Il met et retire ses gants seul, et le cours ne s’arrête pas pour un laçage.'},
        ],
        'networkHeading': 'D’autres clubs du réseau accueillent les enfants',
        'networkIntro': 'Le Club de Boxe Blagnac appartient au réseau Boxing Center, qui a aussi sa boutique de matériel en ligne, Boutique de Boxe. Si la semaine de votre enfant se passe côté Toulouse, ces clubs du réseau l’accueillent.',
        'formHeading': 'Une question sur la taille ? Écrivez-nous.',
        'formText': 'Indiquez l’âge de votre enfant et le cours qui l’intéresse. Nous vous répondons sous 24 h, avec la taille de gants à prévoir.',
        'ogWord': 'Gants enfant',
        'ogKicker': '4, 6, 8, 10 oz · selon l’âge',
        'priority': ['gants de boxe enfant', 'le poids suit l’âge', 'prêtés pour commencer'],
    },
    'sac-de-sport-boxe': {
        'key': 'sac-de-sport-boxe',
        'path': '/sac-de-sport-boxe/',
        'label': 'Le sac de sport du boxeur',
        'question': 'Que mettre dans son sac de sport pour aller à la boxe ?',
        'title': 'Sac de sport pour la boxe : que mettre dedans ? | Blagnac',
        'ogTitle': 'Que mettre dans son sac pour aller boxer : la liste, sans superflu',
        'description': 'Tenue, chaussures d’intérieur, eau, bandes, protège-dents : ce qu’il faut dans un sac de sport pour la boxe, dans l’ordre des achats, et ce que le club prête.',
        'h1Main': 'Dans le sac de sport',
        'h1Em': 'd’un boxeur',
        'eyebrow': 'Conseil · le matériel, dans l’ordre',
        'lead': 'Pour boxer, un sac de sport contient une tenue, des chaussures propres réservées à l’intérieur, de l’eau et une serviette. Les bandes s’y ajoutent dès la deuxième séance, les gants une fois inscrit, le protège-dents avant la première opposition. Le reste, le club le prête.',
        'note': 'Gants et protections prêtés pour les premières séances : n’achetez rien avant d’être venu.',
        'sections': [
            {
                'eyebrow': 'Le premier jour',
                'h2': 'Le contenu du sac à la première séance',
                'paragraphs': [
                    'Un short ou un legging, un tee-shirt, une bouteille d’eau, une serviette. Et une paire de chaussures propres, qui ne sert qu’à l’intérieur : c’est la seule exigence de la salle.',
                    'Tout le reste est prêté. Ajoutez un élastique si vos cheveux sont longs, et laissez montre et bijoux à la maison.',
                ],
                'links': [{'label': 'Votre première séance, étape par étape', 'href': '/premiere-seance/'}],
            },
            {
                'eyebrow': 'Dès la deuxième séance',
                'h2': 'Les bandes, premier achat d’un boxeur',
                'paragraphs': [
                    'Elles tiennent le poignet et les jointures sous le gant, et elles gardent propres les gants que le club vous prête. Comptez deux paires si vous venez plusieurs fois par semaine : une sur les mains, une au lavage.',
                    'Une main d’adulte demande une bande longue ; une petite main, une bande courte. Elles se lavent après chaque séance, dans un filet.',
                ],
                'links': [{'label': 'Les bandes de boxe, Boutique de Boxe', 'href': B + '/bandes-de-boxe/'}],
            },
            {
                'eyebrow': 'Une fois inscrit',
                'h2': 'Les gants, choisis avec votre entraîneur',
                'paragraphs': [
                    'Le poids d’une paire dépend de votre gabarit et de ce que vous faites : le cardio boxe sans contact, la boxe anglaise loisir et le groupe compétition ne demandent pas le même gant. Posez la question avant de commander : l’entraîneur vous évite d’acheter deux fois.',
                ],
                'links': [
                    {'label': 'Le calculateur de poids de gants, Boutique de Boxe', 'href': B + '/outils/poids-de-gants/'},
                    {'label': 'Cardio boxe à Blagnac, sans contact', 'href': '/cours-de-boxe-blagnac/cardio-boxe/'},
                ],
            },
            {
                'eyebrow': 'Avant la première opposition',
                'h2': 'Le protège-dents, obligatoire dès qu’il y a contact',
                'paragraphs': [
                    'Même en touche légère, il est obligatoire. Un modèle à mouler dans l’eau chaude suffit : préparez-le chez vous, la veille, et rangez-le dans sa boîte — jamais au fond d’un gant.',
                    'Les casques, les coquilles et les protège-tibias, eux, sont prêtés par le club : inutile de les acheter.',
                ],
                'links': [{'label': 'Les protège-dents, Boutique de Boxe', 'href': B + '/protege-dents/'}],
            },
            {
                'eyebrow': 'Après la séance',
                'h2': 'Ce qui sort du sac en rentrant',
                'paragraphs': [
                    'Les gants et les bandes ne passent pas la nuit dans le sac : ouvrez les gants, étendez les bandes ou lancez une machine. C’est l’humidité enfermée qui donne leur odeur aux sacs de sport.',
                    'Rincez la bouteille et le protège-dents, changez la serviette. Un sac vidé le soir même est prêt pour la séance suivante.',
                ],
                'links': [{'label': 'Gants de boxe enfant : la taille par âge', 'href': '/gants-de-boxe-enfant/'}],
            },
        ],
        'faq': [
            {'question': 'Que faut-il apporter à un premier cours de boxe ?', 'answer': 'Une tenue de sport, des chaussures propres réservées à l’intérieur, une bouteille d’eau et une serviette. Les gants et les protections sont prêtés.'},
            {'question': 'Dans quel ordre acheter son matériel de boxe ?', 'answer': 'Les bandes dès la deuxième séance, les gants une fois inscrit, le protège-dents avant la première opposition. Le club prête les casques, les coquilles et les protège-tibias.'},
            {'question': 'Faut-il des chaussures de boxe pour commencer ?', 'answer': 'Non : une paire de chaussures de sport propres, qui ne sert qu’à l’intérieur, suffit.'},
            {'question': 'Comment éviter qu’un sac de boxe sente mauvais ?', 'answer': 'Videz-le en rentrant : gants ouverts à l’air, bandes au lavage, serviette changée. L’odeur vient de l’humidité enfermée.'},
        ],
        'networkHeading': 'Le matériel, dans tout le réseau',
        'networkIntro': 'Les clubs Boxing Center de Toulouse et de Portet publient leurs activités et leurs plannings ; Boutique de Boxe, la boutique en ligne du réseau, réunit le matériel.',
        'formHeading': 'Une hésitation avant d’acheter ?',
        'formText': 'Écrivez-nous ce que vous comptez acheter, et pour quel cours. Nous vous répondons sous 24 h, avec l’avis de l’entraîneur.',
        'ogWord': 'Le sac',
        'ogKicker': 'Tenue, bandes, protège-dents',
        'priority': ['sac de sport', 'réservées à l’intérieur', 'premier achat'],
    },
}

PAGES = {
    'gants-de-boxe-enfant': ('''---
/**
 * Gants de boxe enfant — la taille selon l'âge, calée sur les trois cours du
 * club (éveil, boxe éducative, ados). Rien à acheter pour commencer : le club
 * prête. Copy: src/data/copy.json ("gants-de-boxe-enfant").
 */
import IntentPage from '@/components/IntentPage.astro';
---

<IntentPage
  copyKey="gants-de-boxe-enfant"
  photo={{
    file: 'boxe-ados-blagnac',
    widths: [480, 960, 1600],
    width: 1600,
    height: 1066,
    alt: 'Un adolescent, gants bleus aux mains, frappe les pattes d’ours orange que lui présente un entraîneur',
    caption: 'Des gants à sa main, aux pattes d’ours'
  }}
/>
'''),
    'sac-de-sport-boxe': ('''---
/**
 * Le sac de sport du boxeur — ce qu'on y met, dans l'ordre réel des achats, et
 * ce que le club prête. Copy: src/data/copy.json ("sac-de-sport-boxe").
 */
import IntentPage from '@/components/IntentPage.astro';
---

<IntentPage
  copyKey="sac-de-sport-boxe"
  photo={{
    file: 'boxe-detail',
    widths: [240, 480, 700, 1000],
    width: 1000,
    height: 606,
    alt: 'Un jeune boxeur en débardeur blanc, mains bandées de rouge, se tient en garde devant les cordes d’un ring',
    caption: 'Les bandes, sous les gants'
  }}
/>
'''),
}

def typo(v, cle=None):
    """L'espace insécable devant : ; ? ! » et après «, comme le reste de copy.json — un titre ne passe pas à la ligne sur un deux-points."""
    if isinstance(v, str):
        if cle in ('key', 'path', 'href', 'title', 'ogTitle', 'description', 'question', 'ogWord', 'ogKicker'):
            return v
        import re
        return re.sub(r'« ', '« ', re.sub(r' ([:;?!»])', ' \\1', v))
    if isinstance(v, list):
        return [typo(x, cle) for x in v]
    if isinstance(v, dict):
        return {k: (x if k == 'priority' else typo(x, k)) for k, x in v.items()}
    return v


COPIES = {k: typo(c) for k, c in COPIES.items()}

# ── copy.json : les deux entrées, à la suite des autres ─────────────────────
brut = lire('src/data/copy.json')
nl = '\r\n' if '\r\n' in brut else '\n'
copy = json.loads(brut)
copy.update(COPIES)
for c in COPIES.values():
    assert len(c['title']) <= 68, (c['key'], len(c['title']))
    assert 80 <= len(c['description']) <= 158, (c['key'], len(c['description']))
ecrire('src/data/copy.json', json.dumps(copy, ensure_ascii=False, indent=2).replace('\n', nl) + nl)

# ── les deux pages ──────────────────────────────────────────────────────────
for cle, page in PAGES.items():
    ecrire('src/pages/%s/index.astro' % cle, page)

# ── routes.ts : deux routes, avant la première séance ───────────────────────
poser('src/data/routes.ts', "  {\n    path: '/premiere-seance/',", '''  /* Two advice pages on equipment (2026-10-02): each owns one question and
     links out, from its sections, to the network's equipment shop. */
  ...(['gants-de-boxe-enfant', 'sac-de-sport-boxe'] as const).map((key) => {
    const copy = copyFor(key);
    if (!copy?.path || !copy.question || !copy.label || !copy.ogWord || !copy.ogKicker) throw new Error(`routes.ts: no page copy for advice page "${key}"`);
    return {
      path: copy.path,
      label: copy.label,
      question: copy.question,
      answers: copy.description,
      og: { word: copy.ogWord, kicker: copy.ogKicker, photo: key === 'gants-de-boxe-enfant' ? 'cours-debout-groupe-1600.jpg' : 'espace-renforcement-1400.jpg' }
    };
  }),
''', avant=True, marque="'gants-de-boxe-enfant', 'sac-de-sport-boxe'")

# ── site.ts : pages publiques ───────────────────────────────────────────────
poser('src/data/site.ts', "  ...COMMUNE_PAGES,\n", "  '/gants-de-boxe-enfant/',\n  '/sac-de-sport-boxe/',\n", marque="'/gants-de-boxe-enfant/',")

# ── sitemap : la photo que chaque page affiche vraiment ─────────────────────
poser('src/pages/sitemap.xml.ts', "  '/inscription/': ['conseil-coach-1400.jpg'],\n",
      "  '/gants-de-boxe-enfant/': ['boxe-ados-blagnac-1600.jpg'],\n  '/sac-de-sport-boxe/': ['boxe-detail-1000.jpg'],\n", marque="'/gants-de-boxe-enfant/':")

# ── pied de page : les deux conseils, sous les cours ────────────────────────
poser('src/components/Footer.astro', '          <li><a href="/boxe-femme-blagnac/">Boxe femme à Blagnac, sur tous nos cours</a></li>\n',
      '          <li><a href="/gants-de-boxe-enfant/">Gants de boxe enfant : la taille par âge</a></li>\n'
      '          <li><a href="/sac-de-sport-boxe/">Dans le sac de sport d’un boxeur</a></li>\n', marque='href="/gants-de-boxe-enfant/"')

# ── bloc réseau : la page des gants d'enfant renvoie vers les clubs qui accueillent les enfants ──
poser('src/data/network.ts', "  'boxe-enfant-blagnac': KIDS,\n", "  'gants-de-boxe-enfant': KIDS,\n", marque="'gants-de-boxe-enfant': KIDS,")
poser('src/data/network.ts', "  'boxe-enfant-blagnac': KIDS_POPUP,\n", "  'gants-de-boxe-enfant': KIDS_POPUP,\n", marque="'gants-de-boxe-enfant': KIDS_POPUP,")

# ── contrat de mots-clés : ce que chaque page doit garder dans son texte ────
brut = lire('src/data/mots-cles.json')
nlm = '\r\n' if '\r\n' in brut else '\n'
contrat = json.loads(brut)
contrat['/gants-de-boxe-enfant/'] = {
    'priority': COPIES['gants-de-boxe-enfant']['priority'],
    'secondary': ['gants de boxe enfant taille', 'gants de boxe 6 oz enfant', 'quelle taille de gants de boxe pour un enfant', 'gants de boxe enfant 8 ans', 'gants de boxe ado'],
}
contrat['/sac-de-sport-boxe/'] = {
    'priority': COPIES['sac-de-sport-boxe']['priority'],
    'secondary': ['sac de sport boxe', 'que mettre dans son sac de boxe', 'matériel boxe débutant', 'quoi apporter à un cours de boxe', 'ordre des achats boxe'],
}
ecrire('src/data/mots-cles.json', json.dumps(contrat, ensure_ascii=False, indent=2).replace('\n', nlm) + nlm)

print('✓ blagnac : /gants-de-boxe-enfant/ et /sac-de-sport-boxe/ écrits et raccordés')
