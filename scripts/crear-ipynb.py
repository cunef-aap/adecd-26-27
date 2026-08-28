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

capitulos = sorted((RAIZ / "capitulos").glob("*.qmd"))
fallos = []
for qmd in capitulos:
    print(f"-> {qmd.name}")
    r = subprocess.run(
        ["quarto", "render", str(qmd), "--profile", "notebooks",
         "--to", "ipynb", "--output", f"{qmd.stem}.ipynb", "--no-execute"],
        cwd=RAIZ,
    )
    if r.returncode:
        fallos.append(qmd.name)

# Quarto crea este redirect al renderizar un capítulo de un proyecto `book`, pero su
# destino no existe dentro del directorio de cuadernos.
(SALIDA / "index.html").unlink(missing_ok=True)

if fallos:
    print("FALLARON: " + ", ".join(fallos), file=sys.stderr)
    sys.exit(1)

# El directorio contiene solo artefactos generados: elimina cuadernos cuyos capítulos ya
# no formen parte del curso.
esperados = {f"{qmd.stem}.ipynb" for qmd in capitulos}
for notebook in SALIDA.glob("*.ipynb"):
    if notebook.name not in esperados:
        notebook.unlink()
