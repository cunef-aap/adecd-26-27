#!/usr/bin/env python3
"""Regenera assets/logo-impresion.html a partir de assets/img/cunef-logo.png.

El membrete de los PDF es un <img> con el logo incrustado en base64. Va incrustado, y no
por ruta, porque el fragmento se incluye en paginas a distinta profundidad dentro de docs/
y una ruta relativa no serviria para todas. Se reduce a 420 px de ancho, que sobra para los
26 mm que ocupa impreso.
"""
import base64
import io
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
ORIGEN = RAIZ / "assets" / "img" / "cunef-logo.png"
DESTINO = RAIZ / "assets" / "logo-impresion.html"

im = Image.open(ORIGEN)
im.thumbnail((420, 420), Image.LANCZOS)
buf = io.BytesIO()
im.save(buf, "PNG", optimize=True)
datos = base64.b64encode(buf.getvalue()).decode()

DESTINO.write_text(
    "<!-- Membrete de los PDF. El logo va incrustado porque este fragmento se incluye en\n"
    "     paginas a distinta profundidad y una ruta relativa no valdria para todas.\n"
    "     En pantalla no se ve: lo oculta .logo-impresion en assets/styles.css.\n"
    "     Se regenera con scripts/logo-impresion.py. -->\n"
    f'<img class="logo-impresion" alt="" aria-hidden="true" src="data:image/png;base64,{datos}">\n',
    encoding="utf-8",
)
print(f"{DESTINO.relative_to(RAIZ)}: {im.size[0]}x{im.size[1]}, "
      f"{DESTINO.stat().st_size // 1024} KB")
