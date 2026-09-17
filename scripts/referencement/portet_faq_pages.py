# -*- coding: utf-8 -*-
"""
Portet, 17/09 (Eddy : « you've forgotten FAQs on a lot of websites ») — une FAQ
sur les six pages qui n'en avaient pas : /tarifs/, /plannings/, /coachs/,
/activites/, /salles/, /contact/. Aucune n'avait d'accordéon (vérifié avant
d'écrire : on ne répète rien). Pour chacune : une section <details> en dur,
juste avant l'appel final (cta-block), et un script FAQPage dans la tête.

Questions PROPRES à chaque page ; réponses tirées de ce que le site publie déjà
(content.json : tarifs et anciens prix, équipe ; /about/ et /premiere-seance/ :
600 m², ring, cage, tatamis, 24 sacs ; llms : fédérations, durée des cours).
Rien sur les gants (Eddy, 13/09). Aucune heure de cours en dur : la grille de
/plannings/ reste la référence. Rejouable.
"""
import io, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
P = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Portet', 'boxing-center-portet')
BASE = 'https://boxing-center-portet.fr'

FAQS = {
    'tarifs': ('Les questions sur les tarifs.', [
        ('Quelle formule est la plus avantageuse sur l’année ?',
         'La saison : 259 € au lieu de 400 €, payés comptant, pour 12 mois. Elle ouvre les cinq salles du groupe.'),
        ('Peut-on payer la saison en plusieurs fois ?',
         'Le prix de 259 € se règle comptant. Un paiement en 4× peut être proposé par PayPal, uniquement s’il est disponible et si tu es éligible.'),
        ('L’offre rentrée à 29 € engage-t-elle sur une durée ?',
         'Non, elle est sans engagement : 29 € par personne toutes les 4 semaines, au lieu de 44 €. La première échéance passe par carte, les suivantes par prélèvement, et les coordonnées d’un proche sont demandées.'),
        ('Y a-t-il des frais en plus de l’abonnement ?',
         'Un badge d’accès à 34,99 €. Pour l’offre à 29 €, il est facturé 72 heures après le début ; pour les abonnements classiques sans engagement, il s’ajoute sauf exception affichée à la commande.'),
        ('Combien coûte l’inscription d’un enfant ?',
         '295 € l’année pour les enfants et les ados, t-shirt officiel du club inclus, et 250 € l’année pour la baby boxe.'),
    ]),
    'plannings': ('Les questions sur le planning.', [
        ('Quels jours le club est-il ouvert ?',
         'Du lundi au samedi, de 10h00 à 21h30, samedi compris. L’heure du dernier cours n’est pas l’heure de fermeture.'),
        ('Combien de temps dure un cours ?',
         'Une heure. Les créneaux des amateurs et des pros durent une heure et demie.'),
        ('Y a-t-il des cours le midi et le soir ?',
         'Oui, les deux. La grille donne l’horaire de chaque cours, et le cours en train de se dérouler y est signalé en direct.'),
        ('Quand ont lieu les cours pour les enfants ?',
         'Le mercredi et le samedi. Chaque groupe figure dans la grille avec sa tranche d’âge.'),
        ('Peut-on garder le planning sur son téléphone ?',
         'Oui : le bouton « Télécharger le planning », sous la grille, l’enregistre en image.'),
    ]),
    'coachs': ('Les questions sur les coachs.', [
        ('Qui dirige l’équipe ?',
         'Valentin Tapia, head coach et responsable sportif. Il encadre la boxe loisirs, la boxe éducative et les compétiteurs.'),
        ('Qui encadre le kick-boxing ?',
         'Samuel Pinto : kick-boxing et K1, boxe française, Lady Boxing, kick enfants et ados, et préparation physique.'),
        ('Qui encadre le MMA et le grappling ?',
         'Enzo Pioppo et Nicolas Tramaçon, dans la cage et sur les tatamis.'),
        ('Qui s’occupe des enfants et des ados ?',
         'Mourad et Ingrid pour la boxe anglaise et le kick-boxing des enfants et des ados, avec Valentin Tapia pour la boxe éducative.'),
        ('Les coachs sont-ils diplômés ?',
         'Oui. L’équipe est diplômée dans ses fédérations : FFBoxe, FFKMDA et FMMAF. Chaque coach a sa page, avec son parcours.'),
    ]),
    'activites': ('Les questions sur les cours.', [
        ('Par quoi commencer quand on n’a jamais boxé ?',
         'Par le cours qui te fait envie : aucun niveau n’est demandé. La page « Ta première séance » raconte l’heure entière, minute par minute.'),
        ('Fait-on du sparring dès le début ?',
         'Non. Le sparring n’est jamais imposé : tu montes sur le ring quand tu le demandes.'),
        ('Y a-t-il un cours réservé aux femmes ?',
         'Oui : le Lady Boxing, 100 % femmes.'),
        ('À partir de quel âge peut-on s’inscrire ?',
         'La baby boxe accueille les petits, la boxe éducative commence à 7 ans, et le kick-boxing a ses groupes enfants et ados. Les tranches d’âge de la saison sont au planning.'),
        ('Peut-on pratiquer plusieurs disciplines ?',
         'Oui. L’abonnement ouvre toutes les disciplines, sans limite de cours.'),
    ]),
    'salles': ('Les questions sur la salle.', [
        ('Quelle surface fait le club ?',
         '600 m², tous dédiés aux sports de combat.'),
        ('Quels équipements trouve-t-on sur place ?',
         'Un ring de boxe anglaise, une cage de MMA, des tatamis, 24 sacs de frappe et un espace de préparation physique.'),
        ('L’abonnement donne-t-il accès aux autres salles du groupe ?',
         'Oui avec la saison : elle ouvre les cinq salles Boxing Center — Portet-sur-Garonne, Minimes, Saint-Cyprien, Ramonville et États-Unis.'),
        ('Depuis quand la salle existe-t-elle ?',
         'Depuis 2016. C’est la salle phare du groupe.'),
        ('Peut-on visiter avant de s’inscrire ?',
         'Le club est ouvert du lundi au samedi, de 10h00 à 21h30 : tu peux passer, ou appeler avant de venir.'),
    ]),
    'contact': ('Les questions avant de nous écrire.', [
        ('Comment joindre le club rapidement ?',
         'Par téléphone au 09 56 65 37 82, aux heures d’ouverture : du lundi au samedi, de 10h00 à 21h30.'),
        ('Où se trouve le club ?',
         'Au 61 route d’Espagne, 31120 Portet-sur-Garonne, au sud de Toulouse.'),
        ('Que faut-il apporter pour une première séance ?',
         'Une tenue de sport — t-shirt, short ou legging, baskets propres — et une bouteille d’eau.'),
        ('À qui s’adresser pour privatiser la salle ou proposer un partenariat ?',
         'Au formulaire de la page Partenaires : tu y décris ton projet — entreprise, association, école, médias — et le club te rappelle.'),
    ]),
}


def e(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


for page, (titre, qa) in FAQS.items():
    p = os.path.join(P, page, 'index.html')
    t = io.open(p, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in t else '\n'
    if 'class="faq-list"' in t or '"FAQPage"' in t:
        print(f'  {page:10s} déjà fait')
        continue
    i = t.find('class="cta-block')
    # pas d'appel final (coachs, activites, salles, contact finissent autrement) : la FAQ ferme la page
    j = t.rfind('<section', 0, i) if i > 0 else t.find('</main>')
    assert j > 0, page
    k = t.rfind(nl, 0, j) + len(nl)            # début de la ligne du <section> final
    details = nl.join(f'        <details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in qa)
    section = (f'  <!-- LA FAQ DE LA PAGE (17/09) : ses propres questions, écrites en dur, reprises dans le script FAQPage de la tête. -->{nl}'
               f'  <section class="section band">{nl}'
               f'    <div class="wrap">{nl}'
               f'      <div class="sec-head" data-reveal>{nl}'
               f'        <div>{nl}'
               f'          <span class="eyebrow">Questions</span>{nl}'
               f'          <h2 class="display" style="margin-top:1rem">{e(titre)}</h2>{nl}'
               f'        </div>{nl}'
               f'      </div>{nl}'
               f'      <div class="faq-list">{nl}{details}{nl}      </div>{nl}'
               f'    </div>{nl}'
               f'  </section>{nl}{nl}')
    t = t[:k] + section + t[k:]
    url = f'{BASE}/{page}/'
    ld = {'@context': 'https://schema.org', '@type': 'FAQPage', '@id': url + '#faq', 'inLanguage': 'fr-FR',
          'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in qa]}
    script = f'  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>{nl}'
    h = t.find('</head>')
    t = t[:h] + script + t[h:]
    io.open(p, 'w', encoding='utf-8', newline='').write(t)
    print(f'  {page:10s} FAQ posée ({len(qa)} questions) + FAQPage')
print('FAQ des six pages de Portet : faites')
