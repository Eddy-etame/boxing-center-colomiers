# -*- coding: utf-8 -*-
"""
Satellites (7), 17/09 — suite de satellites_txt_noindex.py : le bloc « fichiers »
du plan du site n'avait pas été retiré (le motif, passé par le shell, avait
perdu ses barres obliques inverses). Ici par expression régulière, écrite dans
un fichier : on retire la constante `fichiers` et sa ligne dans le gabarit XML.
Rejouable.
"""
import io, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment')
SITES = sys.argv[1:] or ['colomiers', 'muret', 'cugnaux', 'tournefeuille', 'labege', 'lunion', 'castelginest']
RX = re.compile(r"[ \t]*/\* Les fichiers pour les moteurs de r[\s\S]*?\*/\r?\n[ \t]*const fichiers = [\s\S]*?\.join\('\\n'\);\r?\n\r?\n")
for s in SITES:
    p = os.path.join(BASE, f'boxing-center-{s}', 'src', 'pages', 'sitemap.xml.ts')
    t = io.open(p, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in t else '\n'
    if 'const fichiers' not in t:
        print(f'  {s:13s} déjà fait')
        continue
    note = ('  /* Les fichiers pour les IA (llms, humans, ai) ne sont PAS dans le plan du' + nl +
            '     site : Google les explorait comme des pages et les rangeait en « non' + nl +
            '     indexée ». Ils reçoivent X-Robots-Tag: noindex (vercel.json). */' + nl + nl)
    t2, k = RX.subn(lambda m: note, t)
    t2 = t2.replace(nl + '${fichiers}' + nl, nl)
    propre = k == 1 and 'fichiers}' not in t2 and 'const fichiers' not in t2
    if propre:
        io.open(p, 'w', encoding='utf-8', newline='').write(t2)
    print(f'  {s:13s} bloc retiré={k} propre={propre}')
