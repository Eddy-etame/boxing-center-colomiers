#!/usr/bin/env bash
# Après déploiement : chaque satellite doit servir /sitemap.xml en 200 aux DEUX
# adresses (apex et www), et tout le reste de l'apex doit toujours rediriger
# vers www. Une requête par URL, en Googlebot, jamais de boucle serrée.
#   bash verifier_sitemap_apex.sh [site …]
GB="Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
SITES=${*:-"colomiers muret cugnaux tournefeuille labege lunion castelginest"}
fautes=0
sonde() { # url attendu(code) [loc attendu]
  curl -s -o /tmp/vsa.b -D /tmp/vsa.h -A "$GB" --max-time 25 "$1"
  code=$(head -1 /tmp/vsa.h | awk '{print $2}')
  ct=$(grep -i '^content-type:' /tmp/vsa.h | tr -d '\r' | cut -d' ' -f2- | cut -d';' -f1)
  nloc=$(grep -c '<loc>' /tmp/vsa.b)
  ok=1; [ "$code" = "$2" ] || ok=0
  [ -n "$3" ] && { [ "$nloc" -ge "$3" ] || ok=0; }
  [ $ok = 1 ] && m="  ✓" || { m="  ✗"; fautes=$((fautes+1)); }
  printf "%s %-54s %s %-16s <loc>=%s\n" "$m" "$1" "$code" "$ct" "$nloc"
}
for s in $SITES; do
  echo "── $s"
  sonde "https://boxingcenter-$s.fr/sitemap.xml"      200 5     # le correctif : 200 à l'apex
  sonde "https://boxingcenter-$s.fr/"                 308       # le reste redirige toujours
  sonde "https://boxingcenter-$s.fr/mma/"             308
  sonde "https://www.boxingcenter-$s.fr/sitemap.xml"  200 5
done
echo; [ $fautes = 0 ] && echo "tout est en place" || echo "$fautes faute(s) — si l'apex /sitemap.xml répond encore 308 sur un site, c'est que le tableau de bord Vercel redirige avant vercel.json : la soumission www reste la seule voie sur ce site."
exit $fautes
