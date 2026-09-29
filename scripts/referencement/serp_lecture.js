/* Lit une page de résultats Google déjà chargée dans le navigateur et rend :
   la requête, le blocage éventuel, les résultats organiques dans l'ordre
   (hôte + chemin), et la position de l'hôte cible s'il y figure.
   À coller dans javascript_tool après navigation ; CIBLE est remplacé. */
(() => {
  const CIBLE = 'boutique-de-boxe.com';
  const t = document.body.innerText;
  const bloque = /\/sorry\//.test(location.href) || /trafic inhabituel|unusual traffic/i.test(t);
  const q = new URLSearchParams(location.search).get('q');
  const vus = [];
  for (const a of document.querySelectorAll('#rso a[href^="http"], #search a[href^="http"]')) {
    const h = a.getAttribute('href');
    if (!h || /google\.|gstatic|youtube\.com\/redirect|webcache|translate\./.test(h)) continue;
    if (!a.querySelector('h3')) continue;
    let u; try { u = new URL(h); } catch { continue; }
    const k = u.hostname.replace(/^www\./, '') + u.pathname.replace(/\/$/, '');
    if (!vus.includes(k)) vus.push(k);
  }
  const pos = vus.findIndex((k) => k.startsWith(CIBLE)) + 1;
  return { q, bloque, position: pos || 'absent', url: pos ? vus[pos - 1] : '', top: vus.slice(0, 10) };
})()
