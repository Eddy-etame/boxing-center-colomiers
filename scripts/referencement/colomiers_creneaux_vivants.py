# -*- coding: utf-8 -*-
"""
Colomiers — /plannings/ en direct (Eddy, 13/09 : l'heure réelle sur la page
planning, le moment présent mis en avant).

Le site ne recopie pas les grilles des clubs : il propose quatre créneaux de
vie (midi, après-midi, soir, week-end). On allume donc CELUI DU MOMENT, à
l'heure de Paris, avec une ligne d'horloge au-dessus de la liste : « 14h39
samedi — c'est « L'après-midi » : les clubs sont ouverts », ou, fermé,
« Les clubs rouvrent lundi à 10h ».

Règle du vérificateur : aucune heure écrite en dur hors de src/data/ — les
bornes d'ouverture et de fermeture sont LUES dans HORAIRES (verite.ts), les
bornes des créneaux sont des minutes (12 * 60…), et le texte de l'heure est
composé à l'exécution. Rejouable ; fins de ligne conservées.
"""
import io, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
P = os.path.join('C:' + os.sep, 'Users', 'Mommy Jayce', 'Desktop', 'Boxing Center', 'Deployment',
                 'boxing-center-colomiers', 'src', 'pages', 'plannings.astro')
t = io.open(P, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in t else '\n'
if 'BORNES' in t:
    print('déjà fait'); sys.exit(0)

# 1. les bornes, juste avant la fin du frontmatter
bornes = nl.join([
    '',
    '/* LE CRÉNEAU DU MOMENT — bornes en minutes ; ouverture et fermeture lues dans',
    '   le registre (HORAIRES), jamais recopiées. Le script plus bas allume celui',
    '   qui correspond à l\'heure de Paris. */',
    "const enMinutes = (hhmm: string) => { const [h, m] = hhmm.split(':').map(Number); return h * 60 + m; };",
    'const OUVRE = enMinutes(HORAIRES.ouverture.valeur);',
    'const FERME = enMinutes(HORAIRES.fermeture.valeur);',
    "const BORNES: Record<string, { de: number; a: number; jours: string }> = {",
    "  midi: { de: 12 * 60, a: 14 * 60, jours: '1-6' },",
    "  'apres-midi': { de: 14 * 60, a: 18 * 60, jours: '1-6' },",
    "  soir: { de: 18 * 60, a: FERME, jours: '1-6' },",
    "  'week-end': { de: OUVRE, a: FERME, jours: '6' },",
    '};',
])
m = re.search(r'\r?\n\];\r?\n---', t)
assert m, 'fin de CRENEAUX introuvable'
t = t[:m.start()] + nl + '];' + bornes + nl + '---' + t[m.end():]

# 2. les boutons portent leurs bornes
a = '<button type="button" class="creneau" data-choix={`creneau:${c.id}`}>'
assert t.count(a) == 1, 'bouton'
t = t.replace(a, '<button type="button" class="creneau" data-choix={`creneau:${c.id}`} data-de={BORNES[c.id]?.de} data-a={BORNES[c.id]?.a} data-jours={BORNES[c.id]?.jours}>')

# 3. la ligne d'horloge, au-dessus de la liste
b = '<ul class="creneaux__liste">'
assert t.count(b) == 1, 'liste'
t = t.replace(b, '<p class="creneaux__maintenant mono" id="creneau-maintenant" data-ouvre={OUVRE} data-ferme={FERME} data-ouverture={HORAIRES.ouvertureTexte} aria-live="polite" hidden></p>' + nl + '      ' + b)

# 4. le script et le style, en fin de fichier
fin = nl.join([
    '',
    '<script>',
    '  /* Heure de PARIS (Intl), pas celle du téléphone. Relu toutes les 30 s. */',
    "  const JOURS = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];",
    "  const EN = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];",
    "  const F = new Intl.DateTimeFormat('en-US', { timeZone: 'Europe/Paris', weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' });",
    "  const hh = (m: number) => `${Math.floor(m / 60)}h${String(m % 60).padStart(2, '0')}`;",
    '  function maj() {',
    "    const box = document.getElementById('creneau-maintenant');",
    '    if (!box) return;',
    '    const p = Object.fromEntries(F.formatToParts(new Date()).map((v) => [v.type, v.value]));',
    '    const j = EN.indexOf(p.weekday);',
    '    const mins = (+p.hour % 24) * 60 + +p.minute;',
    '    const ouvre = Number(box.dataset.ouvre), ferme = Number(box.dataset.ferme);',
    '    const ouvert = j >= 1 && j <= 6 && mins >= ouvre && mins < ferme;',
    '    let actif = \'\';',
    "    document.querySelectorAll<HTMLElement>('.creneau[data-de]').forEach((b) => {",
    "      const [d, f] = (b.dataset.jours || '').split('-').map(Number);",
    '      const dansLeJour = f ? j >= d && j <= f : j === d;',
    '      const on = ouvert && dansLeJour && mins >= Number(b.dataset.de) && mins < Number(b.dataset.a);',
    "      b.classList.toggle('is-maintenant', on);",
    "      if (on && !actif) actif = b.querySelector('.creneau__nom')?.textContent || '';",
    '    });',
    '    let texte = `${hh(mins)} ${JOURS[j]}`;',
    '    if (ouvert) texte += actif ? ` — c’est « ${actif} » : les clubs sont ouverts.` : \' — les clubs sont ouverts.\';',
    "    else if (j >= 1 && j <= 6 && mins < ouvre) texte += ` — les clubs ouvrent à ${box.dataset.ouverture}.`;",
    '    else texte += ` — les clubs rouvrent ${j === 6 || j === 0 ? \'lundi\' : \'demain\'} à ${box.dataset.ouverture}.`;',
    '    box.textContent = texte;',
    '    box.hidden = false;',
    '  }',
    '  maj();',
    '  setInterval(maj, 30000);',
    "  document.addEventListener('visibilitychange', () => { if (!document.hidden) maj(); });",
    '</script>',
    '',
    '<style>',
    '  .creneaux__maintenant { margin: 0 0 var(--e-5); color: var(--acier); letter-spacing: 0.06em; }',
    '  .creneau.is-maintenant { position: relative; border-color: var(--signal); box-shadow: inset 0 0 0 1px var(--signal); }',
    "  .creneau.is-maintenant::before { content: 'En ce moment'; position: absolute; top: var(--e-3); right: var(--e-3); font-family: var(--f-mono, monospace); font-size: 0.68rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--signal-texte); }",
    '</style>',
    '',
])
t = t.rstrip('\r\n') + nl + fin.replace('\n', nl) if nl == '\r\n' else t.rstrip('\n') + nl + fin
io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('créneaux vivants posés')
