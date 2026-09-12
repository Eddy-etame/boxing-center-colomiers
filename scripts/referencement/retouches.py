# -*- coding: utf-8 -*-
"""
Retouches ciblées des pages disciplines : chaque phrase partagée avec un
autre site est réécrite sur un seul des deux. Colomiers (l'origine) garde
tout ; Muret réécrit ce qu'il partage avec Colomiers ; Cugnaux réécrit ce
qu'il partage avec Muret, Colomiers ou Tournefeuille ; Tournefeuille
réécrit ce qu'il partage avec Colomiers ou Muret.

Aucun h1, aucune URL, aucune photo, aucun titre qui nomme la ville n'est
touché. Chaque ancienne phrase doit exister exactement une fois, sinon
rien n'est écrit pour ce site.
"""
import io, os, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment')

R = {
    'muret': [
        # boxe anglaise
        ("La boxe anglaise se pratique aux poings, avec des gants, dans un cadre encadré. Aucun niveau n'est demandé pour commencer. Depuis Muret,",
         "Les poings, des gants, un coach : la boxe anglaise se commence sans aucun passé sportif. Depuis Muret,"),
        ("Un débutant travaille au sac, à la corde, aux pattes d'ours avec un coach, et sur le déplacement à vide. Beaucoup de pratiquants s'entraînent des mois sans jamais faire d'opposition — et progressent énormément.",
         "Au début, tout se fait au sac, à la corde, aux pattes d'ours tenues par un coach et en déplacement à vide. Certains s'entraînent des mois sans jamais choisir l'opposition, et leur boxe avance quand même."),
        ("Deux séances par semaine suffisent à sentir une différence en un mois : sur le souffle d'abord, sur la posture ensuite, sur la façon de gérer la fatigue enfin. La boxe a ceci de particulier qu'elle occupe complètement la tête. Il est très difficile de penser à sa journée de travail pendant un round au sac. Beaucoup viennent au départ pour la forme et restent pour cette raison-là.",
         "À raison de deux séances par semaine, un mois suffit pour que le souffle change, puis la posture, puis la manière d'encaisser la fatigue. Pendant un round au sac, on pense au geste et à rien d'autre. C'est souvent la forme qui fait venir, et ce moment-là qui fait rester."),
        ("'Technique : un geste, décomposé, répété lentement puis en rythme'",
         "'Technique : un coup montré par le coach, puis répété jusqu’au rythme'"),
        ("'Renforcement : gainage, abdominaux, travail au poids du corps'",
         "'Renforcement : gainage et abdominaux, sans charge'"),
        ("titre: 'Il me faut du matériel pour la première séance ?'",
         "titre: 'Qu’apporter à la première séance à Portet ?'"),
        ("Une tenue de sport, une bouteille d'eau, et c'est tout pour découvrir. Pour les gants",
         "Pour découvrir, une tenue de sport et une bouteille d'eau suffisent. Pour les gants"),
        ("titre: 'J’ai plus de 40 ans, c’est trop tard ?'",
         "titre: 'Commencer la boxe à 45 ans, c’est possible ?'"),
        ("La boxe se pratique à l'intensité qu'on lui donne. Un coach",
         "Oui : la boxe se règle à l'intensité que tu lui donnes. Un coach"),
        ("Tout le monde a été le débutant essoufflé du fond de la salle. C'est même la situation la plus banale d'un club de boxe : chacun est occupé à sa propre séance, chacun est occupé à sa propre séance.",
         "Chaque pratiquant de la salle a connu sa première séance, essoufflé au fond du groupe. Personne ne te regarde : chacun est pris par sa propre séance."),
        # MMA
        ("Le MMA combine la frappe debout, le corps à corps et le travail au sol. Depuis Muret,",
         "Frappe, lutte debout, travail au sol : le MMA réunit les trois. Depuis Muret,"),
        ("promesse: 'La discipline la plus complète, construite étape par étape, même en partant de zéro.'",
         "promesse: 'La seule cage du réseau, et un apprentissage par étapes, même en partant de zéro.'"),
        ("titre: 'Pourquoi le MMA fait peur, et pourquoi c’est un malentendu'",
         "titre: 'Le MMA de la télévision, et celui du cours'"),
        ("L'image publique du MMA vient des combats professionnels : une cage, deux athlètes préparés, et une intensité qui n'a rien à voir avec un entraînement. Un cours en club, c'est autre chose : de la technique décomposée, des répétitions à vitesse lente, du travail de placement, et une progression par étapes. Ce qu'on voit à la télévision est le sommet d'une pyramide dont la base est un cours d'apprentissage tout à fait ordinaire.",
         "Les combats diffusés montrent deux athlètes préparés depuis des années, dans une cage, à pleine intensité. Un cours en club travaille autrement : des techniques décomposées, répétées lentement, un placement corrigé par le coach, et des étapes franchies une à une. La compétition reste une option pour ceux qui la cherchent ; le cours s'adresse à tout le monde."),
        ("Debout, c'est la frappe : poings, pieds, genoux, avec la même logique de distance et de garde qu'en boxe.",
         "Debout, on frappe des poings, des pieds et des genoux, en gardant la distance et la garde apprises en boxe."),
        ("Au sol, c'est le contrôle, les positions et les soumissions. Un débutant",
         "Au sol, on contrôle, on change de position, on cherche la soumission. Un débutant"),
        ("Ce qu'il faut, c'est accepter de mal faire pendant plusieurs semaines. Le MMA est la discipline où la sensation d'incompétence dure le plus longtemps, parce qu'il y a le plus de choses à intégrer — et c'est aussi celle où les progrès sont les plus visibles une fois le cap passé.",
         "La vraie condition, c'est d'accepter quelques semaines de maladresse. Avec trois terrains à apprendre, le MMA démarre lentement, puis les progrès deviennent très visibles."),
        ("Le jiu-jitsu brésilien travaille le même terrain avec le kimono et un système de ceintures. Le MMA réunit les deux et y ajoute la frappe debout.",
         "Le jiu-jitsu brésilien se pratique en kimono, avec une progression par ceintures. Le MMA ajoute à ce travail au sol la frappe debout."),
        # boxe enfant
        ("promesse: 'Un cadre qui apprend le geste, la maîtrise et le respect — et ça se voit hors de la salle.'",
         "promesse: 'Le geste, la maîtrise, le respect : ce que l’enfant apprend à Portet, et qu’il rapporte à la maison.'"),
        ("titre: 'À partir de quel âge ?'",
         "titre: 'Dès quel âge inscrire un enfant à Portet ?'"),
        # boxing fitness
        ("Le boxing fitness reprend les gestes de la boxe — frappe, déplacement, garde — sans aucune opposition. On ne prend pas de coup et on ne combat pas.",
         "Frappe, déplacement, garde : le boxing fitness garde les gestes de la boxe et retire l'opposition. Tu ne reçois aucun coup et tu ne combats pas."),
    ],
    'cugnaux': [
        # boxe anglaise
        ("La boxe anglaise se pratique aux poings, avec des gants, dans un cadre encadré. Aucun niveau n'est demandé pour commencer. Depuis Cugnaux,",
         "Deux mains gantées et un coach : c'est tout ce qu'il faut pour commencer la boxe anglaise, quel que soit ton niveau. Depuis Cugnaux,"),
        ("promesse: 'Apprendre à boxer pour de vrai, encadré, sans avoir rien à prouver à personne.'",
         "promesse: 'Une boxe apprise geste par geste, dans la commune qui touche Cugnaux.'"),
        ("titre: 'Quatre coups à apprendre'",
         "titre: 'Quatre frappes, et tout le reste dans les jambes'"),
        ("Uniquement les poings : direct, crochet, uppercut, et le jab qui prépare tout le reste. Ce qui ressemble à une limite est en réalité ce qui rend la discipline si dense — quand on ne dispose que de quatre coups, tout se joue ailleurs : dans les appuis, la distance, la garde et la lecture de celui d'en face. C'est un sport de placement bien plus que de puissance, et c'est exactement pour ça qu'une personne qui n'a jamais fait de sport peut y progresser vite.",
         "Direct, crochet, uppercut, et le jab qui ouvre la voie : la boxe anglaise s'arrête là. Avec si peu de coups, la différence se fait sur les appuis, la distance, la garde et la lecture de l'adversaire. On y gagne par le placement plus que par la force, et c'est ce qui permet à un débutant sans passé sportif de progresser vite."),
        ("titre: 'Tu ne prendras pas de coups le premier jour'",
         "titre: 'Le sac d’abord, le partenaire plus tard'"),
        ("L'opposition arrive plus tard, et seulement pour celles et ceux qui la souhaitent. Un débutant travaille au sac, à la corde, aux pattes d'ours avec un coach, et sur le déplacement à vide. Beaucoup de pratiquants s'entraînent des mois sans jamais faire d'opposition — et progressent énormément.",
         "Au début, on frappe le sac, on saute à la corde, on travaille aux pattes d'ours avec le coach et on se déplace à vide. L'opposition vient ensuite, et seulement pour qui la demande. Des pratiquants passent des saisons entières sans elle, et progressent quand même."),
        ("titre: 'Ce que ça change dans ta semaine'",
         "titre: 'Ce que deux séances par semaine changent'"),
        ("Deux séances par semaine suffisent à sentir une différence en un mois : sur le souffle d'abord, sur la posture ensuite, sur la façon de gérer la fatigue enfin. La boxe a ceci de particulier qu'elle occupe complètement la tête — il est très difficile de penser à sa journée de travail pendant un round au sac. Beaucoup viennent au départ pour la forme et restent pour cette raison-là.",
         "À ce rythme, les premiers effets arrivent vite : le souffle en premier, puis la posture. Pendant un round au sac, le geste prend toute la place, et la journée de travail s'efface. Beaucoup s'inscrivent pour la forme et restent pour ce moment-là."),
        ("titre: 'Comment tu y vas',\n        texte:\n          \"C'est l'avantage",
         "titre: 'De Cugnaux à la route d’Espagne',\n        texte:\n          \"C'est l'avantage"),
        ("Le vrai critère n'est jamais la distance, c'est l'habitude — quand la salle est dans la commune d'à côté, on y va aussi les soirs où on n'en a pas envie. Et c'est cela, et rien d'autre, qui fait qu'on tient en novembre.",
         "Ce qui fait tenir une saison, c'est l'habitude plus que le trajet : avec la salle dans la commune d'à côté, on y va aussi les soirs sans envie, et on est encore là en novembre."),
        ("'Technique : un geste, décomposé, répété lentement puis en rythme'",
         "'Technique : un coup, montré au ralenti puis enchaîné'"),
        ("'Renforcement : gainage, abdominaux, travail au poids du corps'",
         "'Renforcement : gainage et abdominaux au sol'"),
        ("titre: 'Je suis débutant complet, à 40 ans passés. C’est trop tard ?'",
         "titre: 'Commencer la boxe à 40 ans passés, c’est raisonnable ?'"),
        ("C'est le profil le plus fréquent chez les nouveaux inscrits. La boxe se règle",
         "Tout à fait. La boxe se règle"),
        ("Les gants et le matériel collectif sont sur place pour découvrir.",
         "Pour découvrir, tu trouves les gants et le matériel collectif sur place."),
        # MMA
        ("Le MMA combine la frappe debout, le corps à corps et le combat au sol. Depuis Cugnaux,",
         "Frappe debout, corps à corps, combat au sol : le MMA passe de l'un à l'autre. Depuis Cugnaux,"),
        ("titre: 'Debout, au corps à corps, au sol'",
         "titre: 'Frapper, saisir, contrôler'"),
        ("Le MMA se joue sur trois zones : debout, où l'on frappe ; au corps à corps, où l'on projette ; et au sol, où l'on contrôle et où l'on soumet. Un pratiquant progresse en apprenant à passer de l'une à l'autre — et la plupart des débutants découvrent qu'ils sont déjà à l'aise sur l'une des trois sans le savoir.",
         "Trois terrains se succèdent en MMA : la frappe à distance, la saisie et la projection au contact, puis le contrôle et la soumission au sol. Tout le travail consiste à passer de l'un à l'autre, et la plupart des débutants se découvrent à l'aise sur l'un des trois dès les premières semaines."),
        ("'Debout : une situation de frappe, en gants, à intensité choisie'",
         "'Debout, en gants : une séquence de frappe dosée par le coach'"),
        ("'Corps à corps : la saisie, l’amenée au sol, la sortie'",
         "'Au contact : saisir, amener au sol, se dégager'"),
        ("'Sol : un contrôle et une soumission, décomposés'",
         "'Au sol : tenir une position, puis finir par une soumission'"),
        ("'Mise en situation encadrée, puis retour au calme'",
         "'Un passage dans la cage, puis le retour au calme'"),
        ("titre: 'On peut débuter sans rien connaître ?'",
         "titre: 'Jamais fait de MMA : on peut s’y mettre ?'"),
        ("Oui. Un débutant ne fait pas de combat : il apprend à chuter, à se relever, à tenir une position. Le contact est progressif et l'intensité se règle.",
         "Oui. Les premières séances apprennent à chuter, à se relever et à tenir une position, sans combat. Le contact arrive par étapes, et l'intensité se règle."),
        ("Si l'idée de recevoir un coup te bloque, commence par le grappling ou le jiu-jitsu brésilien : ils sont publiés par le club et ne comportent aucune frappe. Si c'est la frappe qui t'attire, le MMA en cage t'ira directement.",
         "Si recevoir un coup t'inquiète, le grappling et le jiu-jitsu brésilien sont faits pour toi : le club publie les deux, et aucun ne comporte de frappe. Si c'est la frappe qui te plaît, va directement au MMA en cage."),
        # kick-boxing
        ("Le kick-boxing ajoute les jambes aux poings : c'est la boxe pieds-poings.",
         "Poings et jambes à la fois : le kick-boxing est une boxe pieds-poings."),
        ("promesse: 'Ajouter les jambes, sans perdre la garde. Le sport le plus complet du club, debout.'",
         "promesse: 'Les jambes en renfort des poings, et une garde qui reste en place.'"),
        ("titre: 'Les jambes en plus des poings'",
         "titre: 'Poings et jambes : ce qui change'"),
        ("À l'entraînement, la différence tient à quelques consignes ; à l'échauffement, à la technique et au sac, on fait exactement le même travail.",
         "À l'entraînement, seules quelques consignes changent ; l'échauffement, la technique et le sac restent identiques."),
        ("'Étirements longs — indispensables quand on frappe avec les jambes'",
         "'Étirements longs des hanches et des jambes'"),
        # boxe enfant
        ("Les parents qui viennent chercher un défouloir repartent souvent surpris : ce que la boxe éducative installe en premier, c'est un cadre — et c'est précisément ce cadre qui calme les enfants qu'on lui amène pour ça.",
         "Beaucoup de parents amènent leur enfant pour qu'il se dépense, et découvrent que la boxe éducative commence par poser un cadre. C'est ce cadre, plus que la dépense, qui calme les enfants qu'on lui confie pour ça."),
        ("La Baby boxe est une première approche : le jeu, l'équilibre, la notion de distance. La boxe éducative ajoute le geste, la règle et le respect du partenaire.",
         "La Baby boxe fait découvrir, par le jeu, l'équilibre et la distance. Vient ensuite la boxe éducative, avec le geste, la règle et le respect de celui d'en face."),
        ("titre: 'Ton enfant ne prendra pas de coups'",
         "titre: 'Un contact toujours contrôlé'"),
        ("Le travail se fait au touché contrôlé : on cible, on effleure, on dose. Les protections sont adaptées à la taille et l'opposition libre n'existe pas dans ces créneaux.",
         "Chaque touche est contrôlée : l'enfant vise, effleure et retient son geste. Il porte des protections à sa taille, et ces créneaux excluent toute opposition libre."),
        ("'Rappel de la règle : la garde, la distance, le signal d’arrêt'",
         "'La règle redite : garde haute, bonne distance, arrêt au signal'"),
        ("'Technique : un geste simple, répété, corrigé un par un'",
         "'Un geste simple, que le coach corrige chez chacun'"),
        ("'Application au sac ou aux pattes, en touché contrôlé'",
         "'Le même geste au sac, en touchant sans frapper'"),
        ("'Retour au calme, et le mot du coach sur la séance'",
         "'Retour au calme, et un mot du coach pour finir'"),
        ("titre: 'À partir de quel âge ?'",
         "titre: 'À partir de quel âge à Portet ?'"),
        ("C'est souvent lui qui en tire le plus. Un cours de boxe éducative n'oblige personne à s'exposer : on travaille par deux, sur une consigne précise, et le coach circule.",
         "Souvent, c'est même lui qui en profite le plus. Un cours de boxe éducative n'oblige personne à s'exposer : le travail se fait en binôme, sur une consigne claire, pendant que le coach passe de l'un à l'autre."),
        ("titre: 'Il faut acheter des gants tout de suite ?'",
         "titre: 'Faut-il acheter des gants dès le début ?'"),
    ],
    'tournefeuille': [
        ("Aucun niveau n’est demandé pour commencer. Depuis Tournefeuille,",
         "Tu peux commencer sans aucun passé sportif. Depuis Tournefeuille,"),
        ("titre: 'Tu ne prendras pas de coups le premier jour'",
         "titre: 'Le premier jour, au sac et à la corde'"),
        ("Un débutant travaille au sac, à la corde, aux pattes d’ours avec un coach, et sur le déplacement à vide.",
         "Les premières séances se passent au sac, à la corde, aux pattes d’ours tenues par un coach, et en déplacement à vide."),
        ("titre: 'Ce que ça change dans ta semaine'",
         "titre: 'Deux séances par semaine, et ce qu’elles changent'"),
        ("Deux séances par semaine suffisent à sentir une différence en un mois : le souffle d’abord, la posture ensuite.",
         "En un mois à ce rythme, le souffle change d’abord, puis la posture."),
        ("'Technique : un geste, décomposé, répété lentement puis en rythme'",
         "'Technique : le geste du jour, lent d’abord, puis en rythme'"),
        ("titre: 'À partir de quel âge ?'",
         "titre: 'À partir de quel âge, à Saint-Cyprien et à Portet ?'"),
    ],
}

sites = sys.argv[1:] or list(R)
for site in sites:
    p = os.path.join(BASE, 'boxing-center-' + site, 'src', 'data', 'contenus.ts')
    crlf = b'\r\n' in io.open(p, 'rb').read()
    t = io.open(p, encoding='utf-8').read()
    fautes = []
    for vieux, neuf in R[site]:
        n = t.count(vieux)
        if n != 1:
            fautes.append(f'{n}× « {vieux[:70]} »')
            continue
        t = t.replace(vieux, neuf)
    if fautes:
        print(f'{site} : RIEN ÉCRIT —', *fautes, sep='\n  ')
        continue
    io.open(p, 'w', encoding='utf-8', newline='\r\n' if crlf else '\n').write(t)
    print(f'{site} : {len(R[site])} retouches écrites')
