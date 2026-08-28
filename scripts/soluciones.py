#!/usr/bin/env python3
"""Muestra u oculta los solucionarios en el libro.

El sitio publico no los lleva: se reparten por el Campus Virtual en PDF, que es lo que
prometen los pies de las hojas. Pero para IMPRIMIR esos PDF hacen falta renderizados
dentro del libro, porque sus referencias cruzadas (@thm-test-insesgado y compania) solo
resuelven con los capitulos presentes. Este script conmuta las lineas correspondientes de
`book.chapters` en _quarto.yml para poder hacer el viaje de ida y vuelta.

    python scripts/soluciones.py --mostrar   # antes de renderizar para imprimir
    python scripts/soluciones.py --ocultar   # antes de renderizar para publicar
    python scripts/soluciones.py --estado

El estado normal del repositorio es OCULTAS.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CONFIG = RAIZ / "_quarto.yml"
PATRON = re.compile(r"^(\s*)(#\s*)?(- problemas/hoja-\d+-soluciones\.qmd)\s*$")


def conmuta(mostrar: bool) -> int:
    lineas = CONFIG.read_text(encoding="utf-8").split("\n")
    tocadas = 0
    for i, l in enumerate(lineas):
        m = PATRON.match(l)
        if not m:
            continue
        sangria, comentada, entrada = m.groups()
        nueva = f"{sangria}{'' if mostrar else '# '}{entrada}"
        if nueva != l:
            lineas[i] = nueva
            tocadas += 1
    CONFIG.write_text("\n".join(lineas), encoding="utf-8")
    return tocadas


def estado() -> str:
    lineas = CONFIG.read_text(encoding="utf-8").split("\n")
    hay = [PATRON.match(l) for l in lineas]
    hay = [m for m in hay if m]
    if not hay:
        return "no encuentro ninguna linea de solucionario en _quarto.yml"
    visibles = sum(1 for m in hay if not m.group(2))
    return f"{visibles} de {len(hay)} solucionarios visibles en el libro"


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "--estado"
    if arg == "--mostrar":
        print(f"solucionarios visibles ({conmuta(True)} lineas cambiadas)")
    elif arg == "--ocultar":
        print(f"solucionarios ocultos ({conmuta(False)} lineas cambiadas)")
    elif arg == "--estado":
        print(estado())
    else:
        raise SystemExit(__doc__)
