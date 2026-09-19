# -*- coding: utf-8 -*-
"""Portet — on ne met plus en avant que les gants sont prêtés.

Eddy : « You can take out the fact that the gloves are lent. Even... they are,
but take out the fact that the gloves are lent. » Ramonville avait été nettoyé
le 13/09 (054d08d) ; Portet était resté en l'état.

Deux règles pendant l'opération :
  · on retire la PROMESSE, jamais en la remplaçant par un manque — « vendre la
    proximité, jamais l'absence ». Aucune phrase ne dit que les gants ne sont
    pas prêtés.
  · « rien à acheter avant de venir » reste : c'est toujours vrai, puisque les
    gants sont bien prêtés. On cesse de l'annoncer, on ne le contredit pas.

Rejouable."""
import io

R = r"C:/Users/Mommy Jayce/Desktop/Boxing Center/Portet/boxing-center-portet/"

REMPLACEMENTS = {
    "src/disciplines.json": [
        ('Les gants sont prêtés, et personne ne t’impose de sparring.',
         'Personne ne t’impose de sparring.'),
        ('le coach t’apprend la garde et les premiers coups dès la première séance, et les gants sont prêtés.',
         'le coach t’apprend la garde et les premiers coups dès la première séance.'),
        ('Les gants sont prêtés pour commencer ; si tu continues, le coach te conseillera une paire et des bandes.',
         'Si tu continues, le coach te conseillera une paire de gants et des bandes.'),
        ('Les gants sont prêtés, et le coach commence par la garde.',
         'Le coach commence par la garde.'),
        ('Le coach montre la garde et la position des poings dès la première séance, et les gants sont prêtés.',
         'Le coach montre la garde et la position des poings dès la première séance.'),
        ('Une tenue de sport et une bouteille d’eau. Les gants sont prêtés pour découvrir ; le coach conseillera le matériel si l’enfant continue.',
         'Une tenue de sport et une bouteille d’eau. Le coach conseillera le matériel si l’enfant continue.'),
        ('Une tenue de sport et une bouteille d’eau. Les gants sont prêtés pour découvrir.',
         'Une tenue de sport et une bouteille d’eau.'),
        ('Une tenue de sport, une bouteille d’eau et une serviette. Les gants sont prêtés pour ',
         'Une tenue de sport, une bouteille d’eau et une serviette. Le coach te dit quoi prévoir pour '),
        ('"puces": ["Gants prêtés", "Le ring du club"]',
         '"puces": ["Débutants bienvenus", "Le ring du club"]'),
        ('"puces": ["On touche, on ne frappe pas", "Gants prêtés"]',
         '"puces": ["On touche, on ne frappe pas", "Encadré du début à la fin"]'),
    ],
    "src/content.json": [
        ('Aucun niveau demandé, gants prêtés, pas de sparring imposé.',
         'Aucun niveau demandé, pas de sparring imposé.'),
    ],
    "src/chatbot-kb.ts": [
        ('un coach t’accueille, te prête les gants et te fait le tour de la salle.',
         'un coach t’accueille et te fait le tour de la salle.'),
        ('Les gants et les bandes sont prêtés pour la première séance — tu n’achètes rien avant de savoir si ça te plaît.',
         'Tu n’as rien à acheter avant de savoir si ça te plaît — le coach te dira quoi prévoir.'),
    ],
    "src/chatbot/widget.ts": [
        ('Gants prêtés, aucun niveau demandé, pas de sparring imposé.',
         'Aucun niveau demandé, pas de sparring imposé.'),
    ],
    "scripts/generate-llms.mjs": [
        ('Coachs diplômés FFBoxe, FFKMDA et FMMAF, gants prêtés, aucun niveau demandé, pas de sparring imposé.',
         'Coachs diplômés FFBoxe, FFKMDA et FMMAF, aucun niveau demandé, pas de sparring imposé.'),
        ('Un coach accueille, prête une paire de gants et fait ',
         'Un coach accueille et fait '),
        ('Accueil coach, gants prêtés, visite, échauffement, ',
         'Accueil coach, visite, échauffement, '),
    ],
    "premiere-seance/index.html": [
        ('Minute par minute : l’accueil, les gants prêtés, l’échauffement et le sac.',
         'Minute par minute : l’accueil, l’échauffement et le sac.'),
        ('Un coach t’accueille, te prête une paire de gants et te fait le tour de la salle.',
         'Un coach t’accueille et te fait le tour de la salle.'),
        ('Les gants sont prêtés par le club : il n’y a rien à acheter avant de venir.',
         'Il n’y a rien à acheter avant de venir.'),
        ('Il te serre la main, te prête une paire de gants, et te fait le tour : ',
         'Il te serre la main et te fait le tour : '),
        ('Aucun équipement à acheter avant de venir. Les gants du club sont prêtés — c’est la même paire que celle des autres, et elle t’attend au vestiaire.',
         'Aucun équipement à acheter avant de venir. Tu arrives en tenue de sport, le coach s’occupe du reste.'),
    ],
    "api/chat.js": [
        ('aucun niveau demandé, gants prêtés, et la saison donne le temps ',
         'aucun niveau demandé, et la saison donne le temps '),
    ],
    "premiere-seance/index.html#desc": [],
}

total = 0
for f, paires in REMPLACEMENTS.items():
    if "#" in f or not paires:
        continue
    p = R + f
    s = io.open(p, encoding="utf-8", newline="").read()
    faits = 0
    for a, b in paires:
        n = s.count(a)
        if n == 0:
            if b.split(" — ")[0][:30] in s or b[:30] in s:
                continue  # déjà passé
            raise SystemExit("MOTIF INTROUVABLE dans %s : %r" % (f, a[:70]))
        s = s.replace(a, b)
        faits += n
    if faits:
        io.open(p, "w", encoding="utf-8", newline="").write(s)
    total += faits
    print("%-30s %d remplacement(s)" % (f, faits))
print("\ntotal : %d" % total)
