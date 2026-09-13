# -*- coding: utf-8 -*-
"""
Pages de commune : chaque site reçoit sa propre micro-copie de gabarit, et
Castelginest ses propres réponses de légende (elles étaient celles de
L'Union mot pour mot). Les descriptions de cours changent là où aucun
classement n'est en jeu (Castelginest, Cugnaux).

Règle d'Eddy : on ne touche pas un texte qui porte un classement acquis.
Labège est exclu (sa page Saint-Orens sort en page 1 de Google). Muret,
L'Union, Labège et Tournefeuille gardent leurs descriptions de cours (leur
accueil tient une place).

Jamais touchés : le H1 « Club de boxe et MMA à proximité de … », les
recherches de la légende (les clés), les URL, les photos.
Chaque ancienne chaîne doit exister une fois, sinon rien n'est écrit pour
ce fichier.
Usage : python communes_retouches.py [site…]
"""
import io, os, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment')

# ── La micro-copie du gabarit, identique sur les cinq sites ──────────────
A_DEPUIS = '<h2 id="t-depuis">Comment tu y vas.</h2>'
A_DEPUIS_LEAD = ('{c.population}, {c.intercommunalite}. Voilà la route, les bus, et les\n'
                 '          communes autour — de quoi savoir en trente secondes si c’est jouable\n'
                 '          deux fois par semaine.')
A_LEGENDE = '<h2 id="t-legende">Les questions qu’on nous pose le plus.</h2>'
A_LEGENDE_LEAD = ('À gauche, ce que les gens cherchent. À droite, la réponse en une\n'
                  '          phrase.')
A_AUCLUB = '<h2 id="t-auclub">Ce que le club publie.</h2>'
A_AUCLUB_LEAD = ('Voilà tout ce qui se pratique, avec les noms exacts que tu verras sur\n'
                 '          le planning. {DESTINATION.singularite}')
A_QUESTIONS = '<h2 id="t-questions">Ce qu’on nous demande<br />depuis {c.nom}.</h2>'
A_VOISINES = '<h2 id="t-voisines">Tu pars d’une autre commune&nbsp;?</h2>'
A_NOTE = '<span class="carte__note">La ville du site — {SITE.gentile}</span>'
A_CONV = ('Tu sais où c’est.<br />\n'
          '        <span class="convergence__accent">Reste à choisir ton cours.</span>')
A_CONV_LEAD = ('Réponds à deux questions et on te dit quoi viser et quand venir. Si tu\n'
               '        préfères demander, écris-nous en deux lignes&nbsp;: on te répond avec un\n'
               '        créneau.')


def gabarit(depuis, depuis_lead, legende, legende_lead, auclub, auclub_lead, questions, voisines, note, conv, conv_lead):
    return [
        (A_DEPUIS, f'<h2 id="t-depuis">{depuis}</h2>'),
        (A_DEPUIS_LEAD, depuis_lead),
        (A_LEGENDE, f'<h2 id="t-legende">{legende}</h2>'),
        (A_LEGENDE_LEAD, legende_lead),
        (A_AUCLUB, f'<h2 id="t-auclub">{auclub}</h2>'),
        (A_AUCLUB_LEAD, auclub_lead),
        (A_QUESTIONS, f'<h2 id="t-questions">{questions}</h2>'),
        (A_VOISINES, f'<h2 id="t-voisines">{voisines}</h2>'),
        (A_NOTE, f'<span class="carte__note">{note}</span>'),
        (A_CONV, conv),
        (A_CONV_LEAD, conv_lead),
    ]


GABARITS = {
    'lunion': gabarit(
        'Le chemin jusqu’à l’avenue des États-Unis.',
        '{c.population}, {c.intercommunalite}. La route, les lignes de bus et les communes autour :\n'
        '          tout ce qu’il faut pour juger si deux séances par semaine tiennent dans ton agenda.',
        'Ce que les gens tapent, et la réponse.',
        'Chaque recherche fréquente, et le fait qui y répond, en une phrase.',
        'Les cours de la salle.',
        'La liste complète, sous les noms affichés au planning. {DESTINATION.singularite}',
        'Les questions qui arrivent<br />de {c.nom}.',
        'Une autre commune de départ&nbsp;?',
        'Point de départ du site — {SITE.gentile}',
        'L’adresse, tu l’as.<br />\n'
        '        <span class="convergence__accent">Il reste le cours à choisir.</span>',
        'Deux questions, et tu sais quel cours viser et à quel moment venir. Tu préfères\n'
        '        écrire&nbsp;? Envoie deux lignes, on te répond avec un créneau.',
    ),
    'castelginest': gabarit(
        'Du nord toulousain à l’avenue des États-Unis.',
        '{c.population}, {c.intercommunalite}. Voici la voiture, le bus et le voisinage de la commune,\n'
        '          pour voir d’un coup d’œil si l’aller-retour tient deux soirs par semaine.',
        'Les recherches les plus fréquentes.',
        'Une recherche à gauche, le fait qui y répond à droite.',
        'Tout ce qui s’y pratique.',
        'Chaque cours sous le nom exact du planning du club. {DESTINATION.singularite}',
        'Ce que demandent<br />les habitants de {c.nom}.',
        'Tu viens d’ailleurs dans le secteur&nbsp;?',
        'La commune du site — {SITE.gentile}',
        'Le trajet est clair.<br />\n'
        '        <span class="convergence__accent">Le cours, maintenant.</span>',
        'Deux réponses de ta part, et on t’indique la discipline et le moment qui te vont. Un\n'
        '        message de deux lignes marche aussi&nbsp;: on revient vers toi avec un créneau.',
    ),
    'cugnaux': gabarit(
        'Rejoindre {DESTINATION.ville}.',
        '{c.population}, {c.intercommunalite}. La voiture, les bus et les communes qui entourent\n'
        '          {c.nom} : de quoi mesurer si le trajet tient toute la saison.',
        'Ce qu’on cherche, et ce qu’on trouve.',
        'En face de chaque recherche courante, le fait qui la règle.',
        'Les cours publiés à {DESTINATION.ville}.',
        'Les intitulés sont ceux du planning, mot pour mot. {DESTINATION.singularite}',
        'Les questions venues<br />de {c.nom}.',
        'Ton départ est ailleurs&nbsp;?',
        'Là où commence le site — {SITE.gentile}',
        'Le chemin est tracé.<br />\n'
        '        <span class="convergence__accent">À toi de choisir le cours.</span>',
        'Réponds à deux questions : on te propose une discipline et un moment pour venir. Un\n'
        '        message court fonctionne aussi&nbsp;: la réponse vient avec un créneau.',
    ),
    'tournefeuille': gabarit(
        'La route depuis {c.nom}.',
        '{c.population}, {c.intercommunalite}. Routes, lignes de bus, communes voisines :\n'
        '          l’essentiel pour décider si deux entraînements par semaine restent tenables.',
        'Les recherches, une par une.',
        'Ce que les gens cherchent, et en face, la réponse courte.',
        'Au programme du club.',
        'Les cours, sous les noms que porte le planning. {DESTINATION.singularite}',
        'Les questions qu’on reçoit<br />de {c.nom}.',
        'Tu démarres d’une autre commune&nbsp;?',
        'Le site de départ — {SITE.gentile}',
        'Tu connais le chemin.<br />\n'
        '        <span class="convergence__accent">Choisis ton cours.</span>',
        'Deux questions, et on t’oriente vers le bon cours et le bon moment. Pour demander\n'
        '        directement, écris-nous deux lignes&nbsp;: on te répond avec un créneau.',
    ),
}

# ── Les réponses de la légende ───────────────────────────────────────────
ETATS_UNIS = {
    'club de boxe': "  [`club de boxe ${c.nom}`]: `${DESTINATION.nom}, ${DESTINATION.adresse}, à côté de la sortie 33b « Lalande » du périphérique. 1 200 m² en trois espaces.`,",
    'boxe anglaise': "  [`boxe anglaise ${c.nom}`]: `La boxe anglaise se travaille sur deux rings de compétition, dans l’espace boxe de 400 m².`,",
    'club MMA': "  [`club MMA ${c.nom}`]: `Le club publie le MMA, le grappling et le jiu-jitsu brésilien sur 400 m² de tatamis, avec une cage surélevée officielle.`,",
    'salle MMA': "  [`salle MMA ${c.nom}`]: `La cage est au 388 avenue des États-Unis, avec des panneaux de séparation pour travailler le cage control.`,",
    'sport de combat': "  [`sport de combat ${c.nom}`]: `Cette salle réunit toutes les disciplines du réseau : boxe, pieds-poings, Muay Thai, full contact, MMA, grappling, cours enfants et préparation physique.`,",
    'club kick boxing': "  [`club kick boxing ${c.nom}`]: `Le club publie la boxe pieds-poings et le full contact, sur les deux rings de compétition.`,",
    'boxe pieds poings': "  [`boxe pieds poings ${c.nom}`]: `C’est le nom exact du cours. Poings et jambes, en garde haute et sur appuis.`,",
    'club boxe thaï': "  [`club boxe thaï ${c.nom}`]: `Cette salle publie la boxe pieds-poings et le full contact. Si tu cherches précisément le Muay Thaï, dis-le dans ton message : on te répond avec ce qui existe dans le réseau.`,",
}
PORTET = {
    'club de boxe': "  [`club de boxe ${c.nom}`]: `${DESTINATION.nom}, ${DESTINATION.adresse}. ${voisinage}, et le club accueille ${DESTINATION.horairesCourt}.`,",
    'boxe anglaise': "  [`boxe anglaise ${c.nom}`]: `La boxe anglaise est l’un des intitulés publiés par le club. Les poings seuls, aucun niveau demandé à l’entrée.`,",
    'club MMA': "  [`club MMA ${c.nom}`]: `Le MMA s’entraîne dans la cage du club — la seule du réseau Boxing Center. Le grappling et le jiu-jitsu brésilien y sont publiés à part, sans aucune frappe.`,",
    'salle MMA': "  [`salle MMA ${c.nom}`]: `La cage est à ${DESTINATION.ville}, ${DESTINATION.adresse}. C’est la salle MMA à viser depuis ${c.nom}.`,",
    'sport de combat': "  [`sport de combat ${c.nom}`]: `Toutes les disciplines publiées, de la Baby boxe à la préparation physique. On commence par celle qui correspond à ce qu’on cherche, on change en cours d’année si besoin.`,",
    'club kick boxing': "  [`club kick boxing ${c.nom}`]: `Le kick-boxing est publié pour les adultes et pour les enfants/ados. C’est la boxe pieds-poings du club.`,",
    'boxe pieds poings': "  [`boxe pieds poings ${c.nom}`]: `Même chose : c’est le kick-boxing. Poings et jambes, en garde haute, sur appuis.`,",
    'club boxe thaï': "  [`club boxe thaï ${c.nom}`]: `Le club publie le kick-boxing : poings et jambes, en garde haute. La thaï ajoute coudes et genoux — dis-le dans ton message si c’est elle que tu cherches, on te répond avec ce qui existe dans le réseau.`,",
}


def cle(k):
    return "  [`" + k + " ${c.nom}`]: `"


LEGENDES = {
    # L'Union garde ses réponses, sauf la thaï : le club publie le Muay Thai (clubmma.fr/disciplines).
    'lunion': [
        (ETATS_UNIS['club boxe thaï'],
         cle('club boxe thaï') + "Le club publie le Muay Thai, l’art des huit membres, sur sa page des disciplines ; les créneaux pieds-poings sont au planning de la salle Boxe.`,"),
    ],
    'castelginest': [
        (ETATS_UNIS['club de boxe'],
         cle('club de boxe') + "Le club du réseau à viser, c’est ${DESTINATION.nom}, ${DESTINATION.adresse}. ${voisinage}.`,"),
        (ETATS_UNIS['boxe anglaise'],
         cle('boxe anglaise') + "Deux rings de compétition dans un espace de 400 m² consacré à la boxe : c’est là que se donne la Boxe Anglaise.`,"),
        (ETATS_UNIS['club MMA'],
         cle('club MMA') + "MMA, grappling et jiu-jitsu brésilien se partagent 400 m² de tatamis et une cage officielle surélevée.`,"),
        (ETATS_UNIS['salle MMA'],
         cle('salle MMA') + "La salle MMA est au 388 de l’avenue des États-Unis. Des panneaux de séparation y servent au travail contre la paroi.`,"),
        (ETATS_UNIS['sport de combat'],
         cle('sport de combat') + "Boxe, pieds-poings, Muay Thai, full contact, MMA, grappling, cours enfants et préparation physique : toutes les disciplines du réseau, dans une seule salle.`,"),
        (ETATS_UNIS['club kick boxing'],
         cle('club kick boxing') + "Pieds-poings et full contact se pratiquent sur les deux rings de compétition du club.`,"),
        (ETATS_UNIS['boxe pieds poings'],
         cle('boxe pieds poings') + "Le cours porte ce nom au planning : poings et jambes, garde haute, travail sur appuis.`,"),
        (ETATS_UNIS['club boxe thaï'],
         cle('club boxe thaï') + "Le Muay Thai figure parmi les disciplines publiées par le club : poings, pieds, coudes, genoux et clinch.`,"),
    ],
    'cugnaux': [
        (PORTET['club de boxe'],
         cle('club de boxe') + "Le club à viser est ${DESTINATION.nom}, ${DESTINATION.adresse}, ouvert ${DESTINATION.horairesCourt}. ${voisinage}.`,"),
        (PORTET['boxe anglaise'],
         cle('boxe anglaise') + "Publiée sous ce nom par le club, la boxe anglaise se commence sans niveau : les poings, la garde, les appuis.`,"),
        (PORTET['club MMA'],
         cle('club MMA') + "Seule cage du réseau Boxing Center, c’est là que s’entraîne le MMA. Grappling et jiu-jitsu brésilien ont leurs propres cours, sans frappe.`,"),
        (PORTET['salle MMA'],
         cle('salle MMA') + "Depuis ${c.nom}, la salle MMA du réseau à viser est à ${DESTINATION.ville}, ${DESTINATION.adresse}.`,"),
        (PORTET['sport de combat'],
         cle('sport de combat') + "Le club publie tout, de la Baby boxe à la préparation physique : on choisit la discipline qui répond à ce qu’on cherche, et on peut en changer en cours d’année.`,"),
        (PORTET['club kick boxing'],
         cle('club kick boxing') + "Kick-boxing adultes et kick-boxing enfants/ados : les deux cours de pieds-poings du club.`,"),
        (PORTET['boxe pieds poings'],
         cle('boxe pieds poings') + "Au club, la boxe pieds-poings s’appelle kick-boxing : poings et jambes, garde haute, sur appuis.`,"),
        (PORTET['club boxe thaï'],
         cle('club boxe thaï') + "Le club publie le kick-boxing, poings et jambes. Coudes et genoux appartiennent à la thaï : si c’est elle que tu cherches, précise-le dans ton message et on te dit où elle se pratique dans le réseau.`,"),
    ],
}

# ── Les descriptions de cours (offres.ts) ────────────────────────────────
OFFRES = {
    'castelginest': [
        ("'La discipline reine des poings : précision, vitesse de réaction, esquive et déplacement, sur l’un des deux rings de compétition.'",
         "'Sur les deux rings de compétition : précision, esquive, déplacement et vitesse de réaction.'"),
        ("'Les jambes en plus des poings, au planning de la salle Boxe.'", "'Poings et jambes ensemble, au planning de la salle Boxe.'"),
        ("'Le règlement pieds-poings au-dessus de la ceinture, nouveau dans l’espace Boxe.'", "'Pieds-poings sans coup sous la ceinture, ajouté à l’espace Boxe.'"),
        ("'L’art des huit membres : poings, pieds, coudes, genoux, et le clinch.'", "'Poings, pieds, coudes, genoux et clinch : les huit armes de la boxe thaï.'"),
        ("'Debout, projections et sol, dans la cage officielle et sur 400 m² de tatamis. Les cours accueillent débutants et confirmés.'",
         "'Frappe, projections et sol, sur 400 m² de tatamis et dans la cage officielle, du débutant au confirmé.'"),
        ("'Contrôle, projections, soumissions, sur les tatamis de la salle MMA.'", "'Soumissions, contrôles et projections, sans aucune frappe, sur les tatamis MMA.'"),
        ("'Le sol, en kimono : le règlement exclut la frappe.'", "'Le combat au sol en kimono, sans frappe par règlement.'"),
        ("'Le cours Boxing Lady : exclusivement féminin, sans opposition, au planning Fitness.'", "'Boxing Lady, réservé aux femmes et sans opposition, au planning Fitness.'"),
        ("'Cours mixtes, du débutant au confirmé, dans l’espace préparation physique.'", "'Préparation mixte au format Hyrox, tous niveaux, dans l’espace préparation physique.'"),
        ("'Le cardio de la boxe, en circuit, sans opposition.'", "'Un circuit cardio construit sur les gestes de boxe, sans adversaire.'"),
        ("'Haltérophilie, gymnastique et cardio, en séance intense et fonctionnelle.'", "'Haltères, gymnastique et cardio, enchaînés en séance intense.'"),
        ("'La cage de cross-training et de callisthénie, en accès libre.'", "'Tractions et poids du corps sur la cage de callisthénie, en accès libre.'"),
        ("'Musculation, cardio et cross-training, six jours sur sept, pour les membres.'", "'Musculation, cardio et cross-training ouverts aux membres, six jours sur sept.'"),
        ("'Trois groupes d’âge au planning de la salle Boxe, en touché contrôlé.'", "'Trois groupes, 3/6, 7/11 et 12/16 ans, en touché contrôlé au planning Boxe.'"),
        ("'Le créneau MMA des jeunes, au planning de la salle MMA.'", "'Les 10/16 ans sur les tatamis de la salle MMA, à leur propre créneau.'"),
    ],
    'cugnaux': [
        ("'Les poings, la garde, les déplacements. La porte d’entrée la plus simple.'", "'Poings seuls, garde et déplacements : le cours le plus simple pour commencer.'"),
        ("'Les jambes en plus des poings, en garde haute et sur appuis.'", "'Poings et jambes, garde haute, travail sur appuis.'"),
        ("'Debout, au corps à corps et au sol — et l’entraînement se fait dans la cage.'", "'Frappe debout, corps à corps et sol, travaillés dans la cage du club.'"),
        ("'Le contrôle, les projections et les soumissions. Aucune frappe : on n’y prend pas de coup.'", "'Contrôles, projections et soumissions, sans aucune frappe reçue.'"),
        ("'Le geste de boxe et le cardio, entre femmes.'", "'Boxe et cardio dans un groupe réservé aux femmes.'"),
        ("'Le moteur : gainage, force, souffle. Ce qui fait tenir les trois derniers rounds.'", "'Gainage, force et souffle : la base qui fait tenir un combat jusqu’au bout.'"),
        ("'La première approche : le jeu, l’équilibre, la notion de distance.'", "'Un premier contact par le jeu : équilibre et notion de distance.'"),
        ("'Le geste, la règle et le respect du partenaire. Touché contrôlé, jamais de mise en danger.'", "'Le geste, la règle et le respect de l’autre, en touché contrôlé et sans mise en danger.'"),
        ("'La suite éducative pour ceux qui veulent aussi travailler les jambes.'", "'Pour les jeunes qui veulent ajouter les jambes après la boxe éducative.'"),
    ],
}


def appliquer(p, paires, etiquette):
    crlf = b'\r\n' in io.open(p, 'rb').read()
    t = io.open(p, encoding='utf-8').read()
    fautes = [f'{t.count(v)}× « {v[:70]} »' for v, _ in paires if t.count(v) != 1]
    if fautes:
        print(f'  {etiquette} : RIEN ÉCRIT', *fautes, sep='\n    ')
        return False
    for v, n in paires:
        t = t.replace(v, n)
    io.open(p, 'w', encoding='utf-8', newline='\r\n' if crlf else '\n').write(t)
    print(f'  {etiquette} : {len(paires)} retouches')
    return True


SITES = sys.argv[1:] or ['lunion', 'castelginest', 'cugnaux', 'tournefeuille']
for s in SITES:
    assert s != 'labege', 'Labège est exclu : sa page Saint-Orens tient la page 1'
    print(s)
    R = os.path.join(BASE, 'boxing-center-' + s, 'src')
    paires = GABARITS.get(s, []) + LEGENDES.get(s, [])
    if paires:
        appliquer(os.path.join(R, 'components', 'PageCommune.astro'), paires, 'PageCommune.astro')
    if s in OFFRES:
        appliquer(os.path.join(R, 'data', 'offres.ts'), OFFRES[s], 'offres.ts')
