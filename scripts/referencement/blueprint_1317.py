# -*- coding: utf-8 -*-
"""Ajoute §13.17 au blueprint racine et le reporte dans les sept BLUEPRINT-FAMILLE.md."""
import io, os, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment')
RACINE = os.path.join(BASE, 'BLUEPRINT-SATELLITES-BOXING-CENTER.md')
SITES = ['colomiers', 'muret', 'cugnaux', 'tournefeuille', 'labege', 'lunion', 'castelginest']

SECTION = """
### 13.17 — On ne fait que monter : mesurer avant de réécrire (2026-09-13)

**La règle d'Eddy.** « Si ces textes sont la raison pour laquelle le référencement est bon, on ne les modifie pas. On ne fait que monter, jamais descendre. » Avant toute réécriture, on relève quelle URL tient quel rang ; une page qui sort en page 1 sur sa requête garde ses textes, même partagés.

**Le relevé du 2026-09-13 (Google, lu par Startpage).** Google oppose un contrôle anti-robot au navigateur de session : on ne le contourne pas, on lit les mêmes résultats par Startpage. Treize requêtes « club de boxe <commune> » : une seule page de commune classée, `boxingcenter-labege.fr/saint-orens-de-gameville/` (10e). « club mma l'union » : l'accueil de L'Union (5e), pas la page MMA. « club de boxe rouffiac-tolosan » : l'accueil de L'Union (7e). Les communes de Castelginest, Cugnaux et Tournefeuille ne sont pas classées ; boxingcenter.fr, le site du réseau, sort souvent entre la 2e et la 5e place.

**Ce qui a été retouché.** Les gabarits `PageCommune.astro` de L'Union, Castelginest, Cugnaux et Tournefeuille ont chacun leur micro-copie (titres de section, chapeaux, note de carte, bloc « Décider ») ; Labège garde la sienne, parce que Saint-Orens tient la page 1. Castelginest a ses propres réponses de légende (elles étaient celles de L'Union mot pour mot) ; Cugnaux aussi (identiques à Tournefeuille). Les descriptions de cours d'`offres.ts` sont réécrites sur Castelginest et Cugnaux seulement : Muret, Labège, L'Union et Tournefeuille ont un accueil classé et gardent les leurs. Jamais touchés : le H1 « Club de boxe et MMA à proximité de … », les recherches de la légende, les URL, les photos (`communes_retouches.py` refuse d'écrire sur Labège et sur toute chaîne absente ou doublée).

**Un fait corrigé.** La légende de L'Union disait que la salle publie « la boxe pieds-poings et le full contact » et renvoyait la thaï au réseau, alors que clubmma.fr publie le Muay Thai : la réponse le dit désormais.

**Les sites de club.** Portet (`boxing-center-portet`) et Ramonville (`bc-ramonville`) portent un travail non publié daté du 2026-09-03 (40 fichiers chacun) : attribution des auteurs du site, serveur MCP, llms, robots. Rien n'y est touché sans la décision d'Eddy. Le lien discret vers les satellites se pose, le jour venu, dans le pied de page cuit au build (Portet : `seoBakePlugin` de `vite.config.ts` et `footerMarkup` de `src/layout.ts` ; Ramonville : `scripts/maillage.mjs`) — un lien injecté seulement par JavaScript n'est pas lu par Bing ni par les robots des moteurs de réponse. Minimes, États-Unis et Saint-Cyprien sont hors périmètre jusqu'à nouvel ordre d'Eddy ; Blagnac est tenu par une autre session.
"""


def lire(p):
    brut = io.open(p, 'rb').read()
    return brut.decode('utf-8'), (b'\r\n' in brut)


def ecrire(p, t, crlf):
    io.open(p, 'w', encoding='utf-8', newline='\r\n' if crlf else '\n').write(t)


racine, crlf_r = lire(RACINE)
racine_n = racine.replace('\r\n', '\n')
if '### 13.17' in racine_n:
    print('racine : §13.17 déjà présent')
    nouvelle = racine_n
else:
    nouvelle = racine_n.rstrip('\n') + '\n' + SECTION
    ecrire(RACINE, nouvelle, crlf_r)
    print('racine : §13.17 ajouté')

for s in SITES:
    p = os.path.join(BASE, 'boxing-center-' + s, 'BLUEPRINT-FAMILLE.md')
    t, crlf = lire(p)
    t_n = t.replace('\r\n', '\n')
    if '### 13.17' in t_n:
        print(f'{s:13s} déjà à jour')
    elif t_n.rstrip('\n') == racine_n.rstrip('\n'):
        ecrire(p, nouvelle, crlf)
        print(f'{s:13s} copie conforme mise à jour')
    else:
        ecrire(p, t_n.rstrip('\n') + '\n' + SECTION, crlf)
        print(f'{s:13s} copie divergente : §13.17 ajouté en fin')
