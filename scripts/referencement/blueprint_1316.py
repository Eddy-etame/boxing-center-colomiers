# -*- coding: utf-8 -*-
"""Ajoute §13.16 au blueprint racine et le reporte dans les sept BLUEPRINT-FAMILLE.md."""
import io, os, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment')
RACINE = os.path.join(BASE, 'BLUEPRINT-SATELLITES-BOXING-CENTER.md')
SITES = ['colomiers', 'muret', 'cugnaux', 'tournefeuille', 'labege', 'lunion', 'castelginest']

SECTION = """
### 13.16 — Une phrase, un site (2026-09-12, soir)

**Le constat.** `partage_source.py` ne lisait que les chaînes entre apostrophes simples : les contenus de Muret et de Cugnaux, écrits entre guillemets doubles, lui échappaient presque entièrement. Corrigé, il a compté 141 phrases de discipline présentes sur au moins deux sites. Muret et Cugnaux reprenaient Colomiers mot pour mot (boxe anglaise : 23 et 24 phrases ; MMA de Muret : 13). Tournefeuille, Labège et L'Union partageaient un même gabarit, jusqu'à 22 phrases par page.

**La règle.** Une phrase de discipline de six mots ou plus, ville neutralisée, n'existe que sur un site. Colomiers, l'origine, garde les siennes ; un satellite réécrit ce qu'il partage avec l'origine ; entre deux satellites, un seul réécrit. Exemptés : les titres-mots-clés (H1, questions du type « Où est la salle MMA la plus proche de X ? »), où la ville change et qui portent la requête. Une réécriture garde les ids, les H1, les photos et tout titre qui nomme la ville (`remplacer_contenus2.py` refuse d'écrire sinon), et part des faits du club : la 79 et l'octogone de sept mètres à Ramonville ; les deux rings, la cage surélevée, les seize sacs et le MMA jeunes avenue des États-Unis.

**Résultat.** 141 phrases partagées, puis 11, dont 6 titres-mots-clés ; les 5 autres réécrites. Au passage : la FAQ « pas en forme » de Muret répétait sa dernière phrase ; les âges de l'École de boxe de L'Union différaient d'une page à l'autre.

**Ce que les moteurs voient (relevé du 2026-09-12).** Les sept domaines portent déjà un code `google-site-verification` dans leur zone DNS chez OVH : la Search Console est vérifiée, reste à savoir sur quel compte Google. Brave, l'index de Claude, n'a encore aucune page des satellites : soumission à la main sur search.brave.com/submit-url, et des liens depuis des pages déjà indexées. Aucun site de club (boxingcenter.fr, boxing-center-portet.fr, clubmma.fr, mmatoulouse.com, club-boxe-toulouse.com, boxe-toulouse.com) ne pointe vers un satellite. Bing ne sort encore aucun satellite en page 1 sur « club de boxe muret » ni « club mma l'union ».

**Outils.** `partage_source.py` lit les deux styles de chaîne ; `retouches.py` remplace une phrase exacte présente une seule fois, sinon n'écrit rien ; `remplacer_contenus2.py` remplace le tableau entier sous garde. Le Bash de session réduit une double barre oblique à une seule dans un heredoc, et casse les longs blocs à apostrophes typographiques : un chemin s'écrit avec `os.path.join`, un contenu avec l'outil d'écriture.
"""


def lire(p):
    brut = io.open(p, 'rb').read()
    return brut.decode('utf-8'), (b'\r\n' in brut)


def ecrire(p, t, crlf):
    io.open(p, 'w', encoding='utf-8', newline='\r\n' if crlf else '\n').write(t)


racine, crlf_r = lire(RACINE)
racine_n = racine.replace('\r\n', '\n')
if '### 13.16' in racine_n:
    print('racine : §13.16 déjà présent')
    nouvelle = racine_n
else:
    nouvelle = racine_n.rstrip('\n') + '\n' + SECTION
    ecrire(RACINE, nouvelle, crlf_r)
    print('racine : §13.16 ajouté')

for s in SITES:
    p = os.path.join(BASE, 'boxing-center-' + s, 'BLUEPRINT-FAMILLE.md')
    t, crlf = lire(p)
    t_n = t.replace('\r\n', '\n')
    if '### 13.16' in t_n:
        print(f'{s:13s} déjà à jour')
    elif t_n.rstrip('\n') == racine_n.rstrip('\n'):
        ecrire(p, nouvelle, crlf)
        print(f'{s:13s} copie conforme mise à jour')
    else:
        ecrire(p, t_n.rstrip('\n') + '\n' + SECTION, crlf)
        print(f'{s:13s} copie divergente : §13.16 ajouté en fin')
