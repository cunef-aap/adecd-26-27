#!/usr/bin/env python3
"""Genera un .ipynb por capitulo con el codigo entre centinelas sustituido
por un hueco, para completar en vivo en clase.

Solo genera los cuadernos de los capitulos PUBLICADOS en contenido.txt: docs/ se sube a un
repositorio publico, asi que un cuaderno de un capitulo todavia inedito se publicaria con el.

Adaptado de PhilChodrow/ml-notes-update (scripts/create-ipynb.py), sin la
importacion de dotenv que alli sobra y no esta en requirements.txt.
"""
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "docs" / "live-notebooks"
SALIDA.mkdir(parents=True, exist_ok=True)

def publicados() -> set[str]:
    """Rutas de contenido.txt sin el `-` que marca lo no publicado."""
    fichero = RAIZ / "contenido.txt"
    if not fichero.exists():
        return set()
    dentro = set()
    for cruda in fichero.read_text(encoding="utf-8").split("\n"):
        l = cruda.strip()
        if not l or l.startswith(("#", "-", "[", "{")):
            continue
        dentro.add(l)
    return dentro


DENTRO = publicados()
capitulos = [q for q in sorted((RAIZ / "capitulos").glob("*.qmd"))
             if f"capitulos/{q.name}" in DENTRO]
if not capitulos:
    print("ningun capitulo publicado en contenido.txt: no hay cuadernos que generar")
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
