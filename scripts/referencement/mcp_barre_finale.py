# -*- coding: utf-8 -*-
"""
Les satellites forcent la barre finale (trailingSlash: 'always') : /api/mcp
répond 308 vers /api/mcp/, et un agent qui ne suit pas la redirection ne
trouve rien. Constaté en ligne le 13/09 sur Cugnaux ; le serveur, lui,
répond bien à /api/mcp/. On annonce donc partout l'adresse qui répond :
carte /.well-known/mcp.json, ai.txt, humans.txt, section auteur de llms.txt,
et le script générateur (pour que le défaut ne revienne pas), plus le playbook.
Le fichier src/pages/api/mcp.ts n'est pas touché : c'est la route, pas une adresse.
"""
import io, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
D = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment')
SITES = ['colomiers', 'muret', 'cugnaux', 'tournefeuille', 'labege', 'lunion', 'castelginest']
MOTIF = re.compile(r'/api/mcp(?![/\w.])')


def corriger(chemin, attendu_min=1):
    t = io.open(chemin, encoding='utf-8', newline='').read()
    t2, k = MOTIF.subn('/api/mcp/', t)
    assert k >= attendu_min, f'{chemin} : {k} adresse(s) corrigée(s)'
    io.open(chemin, 'w', encoding='utf-8', newline='').write(t2)
    return k


for s in SITES:
    R = os.path.join(D, f'boxing-center-{s}')
    n = sum(corriger(os.path.join(R, *p)) for p in (
        ('src', 'data', 'auteur.ts'), ('src', 'pages', 'humans.txt.ts'),
        ('src', 'pages', 'ai.txt.ts'), ('public', '.well-known', 'mcp.json')))
    print(f'  {s:13s} {n} adresse(s) → /api/mcp/')

ICI = os.path.dirname(os.path.abspath(__file__))
print(f'  générateur    {corriger(os.path.join(ICI, "satellites_portes_auteur.py"))} adresse(s)')
PLAYBOOK = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', '.research', 'playbook-seo', 'PLAYBOOK-SEO.md')
print(f'  playbook      {corriger(PLAYBOOK)} adresse(s)')
