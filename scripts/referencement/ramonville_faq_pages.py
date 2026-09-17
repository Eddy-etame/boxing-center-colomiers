# -*- coding: utf-8 -*-
"""
Ramonville, 17/09 (Eddy : « you've forgotten FAQs on a lot of websites ») —
une FAQ sur les cinq pages qui n'en avaient pas : /tarifs/, /plannings/,
/coachs/, /activites/, /la-salle/. Pour chacune : une section <details> écrite
en dur (lisible sans JavaScript) juste avant le piège de l'offre, et un nœud
FAQPage ajouté au @graph JSON-LD existant de la page.

Questions PROPRES à chaque page (jamais la même deux fois sur le site), réponses
tirées des faits déjà publiés (data.js : tarifs, badge, rôles des coachs,
octogone de 7 m, accès). Aucune heure de cours en dur : la réponse renvoie à la
grille de la page, qui reste la référence. Rien sur le chauffage ni la clim :
les deux sources du bot se contredisent (question posée à Eddy).

Les règles .faq quittent page.css pour base.css (identiques, chargées partout) :
coachs, activites et la-salle ne chargent pas page.css. Rejouable.
"""
import io, json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
R = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment', 'bc-ramonville')
BASE = 'https://mmatoulouse.com'

FAQS = {
    'tarifs': ('Les questions sur les tarifs.', [
        ('Quelle formule revient le moins cher sur l’année ?',
         'L’Offre Saison : 259 € au lieu de 400 €, payés comptant, pour 12 mois. Elle ouvre aussi les quatre autres clubs du réseau.'),
        ('Peut-on payer la Saison en plusieurs fois ?',
         'Le tarif de 259 € se règle comptant. Un paiement en quatre fois n’existe que par PayPal, si PayPal le propose et si tu es éligible.'),
        ('L’offre à 29 € engage-t-elle sur une durée ?',
         'Non, elle est sans engagement : 29 € par personne toutes les 4 semaines, au lieu de 44 €. La première échéance passe par carte, les suivantes par prélèvement, et les coordonnées d’un proche sont demandées.'),
        ('Y a-t-il des frais en plus de l’abonnement ?',
         'Un badge nominatif à 34,99 € s’ajoute aux abonnements sans engagement de 4 semaines. Il est facturé 72 heures après le début.'),
        ('Combien coûte l’école enfants ?',
         '295 € l’année pour les 7/11 ans et les 12/16 ans, 250 € l’année pour la Baby Boxe dès 3 ans.'),
    ]),
    'plannings': ('Les questions sur le planning.', [
        ('Quels jours la salle est-elle ouverte ?',
         'Du lundi au samedi, de 10h00 à 21h30. Elle est fermée le dimanche. L’étage muscu et cardio suit les mêmes horaires.'),
        ('Y a-t-il des cours le midi et le soir ?',
         'Oui, les deux. La grille ci-dessus donne l’heure de début de chaque cours, et le cours en train de se dérouler y est mis en avant.'),
        ('Quand ont lieu les cours pour les enfants ?',
         'Le mercredi et le samedi après-midi : la Baby Boxe dès 3 ans, puis les 7/11 ans et les 12/16 ans. Le filtre « Enfants » de la grille n’affiche qu’eux.'),
        ('Faut-il faire quelque chose en arrivant ?',
         'Oui : avant chaque cours, tu valides ta présence à l’accueil. C’est un émargement, et il vaut pour tout le monde.'),
        ('Peut-on suivre plusieurs cours dans la même semaine ?',
         'Oui. L’abonnement ouvre tous les cours de la semaine, autant que tu veux, et l’étage muscu et cardio en accès libre.'),
    ]),
    'coachs': ('Les questions sur les coachs.', [
        ('Combien de coachs encadrent les cours ?',
         'Cinq : Jérôme, Sonia, Hicham, Farouk et Valentin Guth. Chacun a sa page, avec son parcours et ses cours.'),
        ('Qui est le coach principal ?',
         'Jérôme. Il tient le MMA et le grappling dans l’octogone ; il a combattu en MMA aux États-Unis et au Canada.'),
        ('Qui s’occupe des enfants ?',
         'Valentin Guth, boxeur professionnel. Il tient toute l’école, de la Baby Boxe aux 12/16 ans.'),
        ('Qui encadre le cours réservé aux femmes ?',
         'Sonia. Elle tient le Lady Punch, 100 % féminin, et la boxe pieds-poings.'),
        ('Qui donne la boxe anglaise ?',
         'Hicham le midi, Farouk le soir. Les créneaux de chacun sont sur la page du planning.'),
    ]),
    'activites': ('Les questions sur les cours.', [
        ('Quel cours choisir pour débuter ?',
         'Le Boxing Camp : un peu de tout, aucun prérequis. Sept cours sur huit s’ouvrent sans expérience, et un coach t’oriente le premier soir.'),
        ('Quelle différence entre la boxe anglaise et la boxe pieds-poings ?',
         'La boxe anglaise se pratique avec les poings seulement, sur le grand ring. La boxe pieds-poings ajoute les jambes, sur le tatami.'),
        ('Le MMA est-il ouvert aux débutants ?',
         'Oui, le cours s’appelle MMA tous niveaux. Pour commencer sans frappe, le grappling — le combat au sol — est la bonne porte d’entrée.'),
        ('Y a-t-il un cours réservé aux femmes ?',
         'Oui : le Lady Punch, 100 % féminin, sans prérequis.'),
        ('La musculation est-elle comprise ?',
         'Oui. L’étage muscu et cardio est en accès libre aux heures d’ouverture, avec le même abonnement que les cours.'),
    ]),
    'la-salle': ('Les questions sur la salle.', [
        ('On s’entraîne vraiment dehors ?',
         'Oui : le plateau fait 300 m² en extérieur, aménagés et couverts. On s’y entraîne toute l’année, et c’est la seule salle du réseau dans ce cas.'),
        ('Quelle taille fait l’octogone ?',
         '7 mètres. Il sert au MMA et au grappling.'),
        ('Y a-t-il un ring de boxe ?',
         'Oui, un grand ring, pour la boxe anglaise. La boxe pieds-poings se pratique sur le tatami du plateau.'),
        ('Y a-t-il de quoi faire de la musculation ?',
         'Oui : un étage de musculation et de cardio, en accès libre aux heures d’ouverture.'),
        ('Comment venir à la salle ?',
         'Par le métro : la salle est au pied du terminus Ramonville de la ligne B. Le bus s’arrête à Ramonville Sud, juste devant. L’adresse : 33 rue des Ormes, Ramonville-Saint-Agne.'),
    ]),
}


def lire(p):
    return io.open(p, encoding='utf-8', newline='').read()


def ecrire(p, t):
    io.open(p, 'w', encoding='utf-8', newline='').write(t)


def e(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('{', '&#123;').replace('}', '&#125;')


# ── 1. les règles .faq : de page.css vers base.css ───────────────────────
pcss = os.path.join(R, 'public', 'assets', 'css', 'page.css')
bcss = os.path.join(R, 'public', 'assets', 'css', 'base.css')
tp, tb = lire(pcss), lire(bcss)
rx_bloc = re.compile(r'/\* FAQ accordion \*/\r?\n(?:\.faq[^\n]*\r?\n)+')
m = rx_bloc.search(tp)
if m and '/* FAQ accordion' not in tb:
    bloc = m.group(0)
    nlb = '\r\n' if '\r\n' in tb else '\n'
    note = ('/* FAQ accordion — venue de page.css le 17/09 : coachs, activites et la-salle' + nlb +
            '   portent désormais une FAQ et ne chargent pas page.css. Règles inchangées. */' + nlb)
    corps = re.sub(r'^/\* FAQ accordion \*/\r?\n', '', bloc)
    ecrire(bcss, tb.rstrip('\r\n') + nlb + nlb + note + corps.replace('\r\n', '\n').replace('\n', nlb))
    ecrire(pcss, tp.replace(bloc, ''))
    print('  .faq : page.css → base.css')
else:
    print('  .faq : déjà dans base.css' if '/* FAQ accordion' in tb else '  .faq : BLOC INTROUVABLE')

# ── 2. la section et le nœud FAQPage, page par page ───────────────────────
for page, (titre, qa) in FAQS.items():
    p = os.path.join(R, 'src', 'pages', page, 'index.astro')
    t = lire(p)
    nl = '\r\n' if '\r\n' in t else '\n'
    if 'id="t-faq"' in t or '"FAQPage"' in t:
        print(f'  {page:10s} déjà fait')
        continue
    i = t.find('<section class="piege"')
    assert i > 0, page
    j = t.rfind('</section>', 0, i) + len('</section>')
    details = nl.join(f'          <details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in qa)
    section = (f'{nl}{nl}    <!-- LA FAQ DE LA PAGE (17/09) : ses propres questions, écrites en dur — lisibles{nl}'
               f'         sans JavaScript, et reprises dans le nœud FAQPage du JSON-LD. -->{nl}'
               f'    <section class="section" aria-labelledby="t-faq">{nl}'
               f'      <div class="wrap">{nl}'
               f'        <div class="shead" data-reveal><span class="eyebrow">Questions</span><h2 class="display" id="t-faq">{e(titre)}</h2></div>{nl}'
               f'        <div class="faq" data-reveal>{nl}{details}{nl}        </div>{nl}'
               f'      </div>{nl}'
               f'    </section>')
    t = t[:j] + section + t[j:]
    # le JSON-LD
    ms = re.search(r'(<script is:inline type="application/ld\+json">)([\s\S]*?)(</script>)', t)
    assert ms, page
    data = json.loads(ms.group(2))
    url = f'{BASE}/{page}/'
    noeud = {'@type': 'FAQPage', '@id': f'{url}#faq'}
    if any(n.get('@id') == f'{url}#webpage' for n in data['@graph']):   # ne pointer que vers un nœud qui existe
        noeud['isPartOf'] = {'@id': f'{url}#webpage'}
    noeud['mainEntity'] = [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in qa]
    data['@graph'].append(noeud)
    corps = json.dumps(data, ensure_ascii=False, indent=2).replace('</', '<\\/')
    corps = nl + nl.join('  ' + l for l in corps.split('\n')) + nl + '  '
    t = t[:ms.start(2)] + corps + t[ms.end(2):]
    ecrire(p, t)
    print(f'  {page:10s} FAQ posée ({len(qa)} questions) + FAQPage')
print('FAQ des cinq pages : faites')
