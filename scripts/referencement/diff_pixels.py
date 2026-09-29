# -*- coding: utf-8 -*-
"""Compare deux captures pixel à pixel.
Usage : python diff_pixels.py avant.png apres.png [sortie-diff.png]
Rend : tailles, nombre de pixels différents, boîte englobante des écarts,
et (si demandé) une image où les écarts sont en rouge."""
import sys
from PIL import Image, ImageChops

a = Image.open(sys.argv[1]).convert("RGB")
b = Image.open(sys.argv[2]).convert("RGB")
print("tailles : avant %dx%d · après %dx%d" % (a.width, a.height, b.width, b.height))
if a.size != b.size:
    h = min(a.height, b.height)
    print("⚠ HAUTEURS DIFFÉRENTES : la page a bougé (%+d px)" % (b.height - a.height))
    a, b = a.crop((0, 0, a.width, h)), b.crop((0, 0, b.width, h))
d = ImageChops.difference(a, b)
bbox = d.getbbox()
if not bbox:
    print("IDENTIQUES : 0 pixel différent")
    sys.exit(0)
L = d.convert("L")
hist = L.histogram()
strict = sum(hist[1:])
n = sum(hist[17:])
g = L.point(lambda v: 255 if v > 16 else 0)
print("pixels différents : %d au total (strict) · %d avec écart > 16 · zone : x %d–%d, y %d–%d" % (strict, n, bbox[0], bbox[2], bbox[1], bbox[3]))
if len(sys.argv) > 3:
    rouge = Image.new("RGB", a.size, (255, 0, 0))
    out = Image.composite(rouge, a.point(lambda v: v // 3), g)
    out.save(sys.argv[3])
    print("image des écarts :", sys.argv[3])
