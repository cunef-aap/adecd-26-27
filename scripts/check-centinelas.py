#!/usr/bin/env python3
"""Comprueba que los centinelas `#---` estan emparejados en cada .qmd.

Un numero impar borra en silencio codigo entero al generar los cuadernos:
ni los filtros Lua ni Quarto avisan. Este script es la unica red.
Uso:  python scripts/check-centinelas.py   (sale con codigo 1 si hay error)
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PATRON = re.compile(r"^\s*#---\s*$")
errores = []

for qmd in sorted(RAIZ.rglob("*.qmd")):
    if "_referencia" in qmd.parts or "docs" in qmd.parts:
        continue
    lineas = qmd.read_text(encoding="utf-8").splitlines()
    marcas = [i + 1 for i, l in enumerate(lineas) if PATRON.match(l)]
    if len(marcas) % 2:
        errores.append(
            f"{qmd.relative_to(RAIZ)}: {len(marcas)} centinelas (impar). "
            f"Lineas: {marcas}"
        )

if errores:
    print("CENTINELAS DESEMPAREJADOS:", file=sys.stderr)
    for e in errores:
        print("  " + e, file=sys.stderr)
    sys.exit(1)

print("centinelas: OK")
