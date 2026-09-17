# -*- coding: utf-8 -*-
"""
Ramonville /tarifs/, 17/09 — correction de ramonville_faq_pages.py : la page
AVAIT déjà ses six questions (« Ce que tu paies. Avant de valider. ») ; il ne
lui manquait que les données FAQPage. La section ajoutée les répétait (règle
d'Eddy : jamais la même chose deux fois sur une page). On la retire, et le
nœud FAQPage du JSON-LD reprend mot pour mot les six questions existantes.
Rejouable.
"""
import html, io, json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
P = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment', 'bc-ramonville',
                 'src', 'pages', 'tarifs', 'index.astro')
t = io.open(P, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in t else '\n'

# 1. retirer la section ajoutée
i = t.find('    <!-- LA FAQ DE LA PAGE (17/09)')
if i > 0:
    j = t.find('</section>', t.find('id="t-faq"', i)) + len('</section>')
    debut = i
    while t[debut - len(nl):debut] == nl:      # les lignes vides posées avant le commentaire
        debut -= len(nl)
    t = t[:debut] + t[j:]
    print('  section répétée : retirée')
else:
    print('  section répétée : absente')

# 2. les six questions déjà sur la page
k = t.find('aria-labelledby="argent-titre"')
assert k > 0
bloc = t[k:t.find('</section>', k)]
propre = lambda s: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).replace('\xa0', ' ').strip()
qa = [(propre(q), propre(a)) for q, a in re.findall(r'<summary>([\s\S]*?)</summary>([\s\S]*?)</details>', bloc)]
assert len(qa) == 6, len(qa)

# 3. le nœud FAQPage
ms = re.search(r'(<script is:inline type="application/ld\+json">)([\s\S]*?)(</script>)', t)
data = json.loads(ms.group(2))
url = 'https://mmatoulouse.com/tarifs/'
data['@graph'] = [n for n in data['@graph'] if n.get('@type') != 'FAQPage']
noeud = {'@type': 'FAQPage', '@id': url + '#faq'}
if any(n.get('@id') == url + '#webpage' for n in data['@graph']):
    noeud['isPartOf'] = {'@id': url + '#webpage'}
noeud['mainEntity'] = [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in qa]
data['@graph'].append(noeud)
corps = json.dumps(data, ensure_ascii=False, indent=2)
corps = nl + nl.join('  ' + l for l in corps.split('\n')) + nl + '  '
t = t[:ms.start(2)] + corps + t[ms.end(2):]
io.open(P, 'w', encoding='utf-8', newline='').write(t)
for q, a in qa:
    print('   ·', q, '→', a[:70] + '…')
print('  FAQPage de /tarifs/ : les 6 questions de la page')
