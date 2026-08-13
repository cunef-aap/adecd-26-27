#!/usr/bin/env python3
"""Genera un .ipynb por capitulo con el codigo entre centinelas sustituido
por un hueco, para completar en vivo en clase.

Adaptado de PhilChodrow/ml-notes-update (scripts/create-ipynb.py), sin la
importacion de dotenv que alli sobra y no esta en requirements.txt.
"""
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "docs" / "live-notebooks"
SALIDA.mkdir(parents=True, exist_ok=True)

fallos = []
for qmd in sorted((RAIZ / "capitulos").glob("*.qmd")):
    print(f"-> {qmd.name}")
    r = subprocess.run(
        ["quarto", "render", str(qmd), "--profile", "notebooks",
         "--to", "ipynb", "--output", f"{qmd.stem}.ipynb", "--no-execute"],
        cwd=RAIZ,
    )
    if r.returncode:
        fallos.append(qmd.name)

if fallos:
    print("FALLARON: " + ", ".join(fallos), file=sys.stderr)
    sys.exit(1)
