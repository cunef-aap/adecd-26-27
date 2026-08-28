#!/usr/bin/env python3
"""Genera un .ipynb por capitulo con el codigo entre centinelas sustituido
por un hueco, para completar en vivo en clase.

Solo genera los cuadernos de los capitulos PUBLICADOS en contenido.txt: docs/ se sube a un
repositorio publico, asi que un cuaderno de un capitulo todavia inedito se publicaria con el.

Adaptado de PhilChodrow/ml-notes-update (scripts/create-ipynb.py), sin la
importacion de dotenv que alli sobra y no esta en requirements.txt.
"""
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

# El fichero lleva guion, que no es un nombre de modulo valido, asi que se carga a mano.
_spec = importlib.util.spec_from_file_location(
    "macros_mathjax", Path(__file__).resolve().parent / "macros-mathjax.py")
_macros = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_macros)
celda_notacion, nombres_definidos = _macros.celda, _macros.nombres_definidos

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
# El anexo de Colab no es un capitulo, pero es el cuaderno con el que se aprende a usar
# la herramienta, asi que se genera igual.
if "curso/colab.qmd" in DENTRO:
    capitulos.append(RAIZ / "curso" / "colab.qmd")
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


def notacion_al_principio(ruta: Path) -> None:
    """Mete la celda de notación como primera celda, y sin duplicarla."""
    nb = json.loads(ruta.read_text(encoding="utf-8"))
    marca = "scripts/macros-mathjax.py"
    nb["cells"] = [c for c in nb["cells"] if marca not in "".join(c["source"])]
    nb["cells"].insert(0, {"cell_type": "markdown", "metadata": {},
                           "source": celda_notacion().split("\n")})
    # `source` es una lista de líneas y cada una lleva su salto, salvo la última.
    fuente = nb["cells"][0]["source"]
    nb["cells"][0]["source"] = [l + "\n" for l in fuente[:-1]] + [fuente[-1]]
    ruta.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def macros_sin_expandir(ruta: Path) -> list[str]:
    """Macros del contrato que Pandoc no llegó a expandir. Deberían ser cero: si aparece
    alguno, en Colab se vería la secuencia en crudo."""
    nb = json.loads(ruta.read_text(encoding="utf-8"))
    md = "\n".join("".join(c["source"]) for c in nb["cells"][1:]
                   if c["cell_type"] == "markdown")
    # Solo letras: `\w+` se comeria el subrayado y `\argmin_w` escaparia como
    # `argmin_w`, que no esta en la lista.
    return sorted({m for m in re.findall(r"\\([A-Za-z]+)", md)
                   if m in nombres_definidos()})


sucios = {}
for qmd in capitulos:
    ruta = SALIDA / f"{qmd.stem}.ipynb"
    if not ruta.exists():
        continue
    notacion_al_principio(ruta)
    restos = macros_sin_expandir(ruta)
    if restos:
        sucios[ruta.name] = restos

if sucios:
    print("MACROS SIN EXPANDIR (se verían en crudo en Colab):", file=sys.stderr)
    for nombre, restos in sucios.items():
        print(f"  {nombre}: {', '.join(restos)}", file=sys.stderr)
    sys.exit(1)

if fallos:
    print("FALLARON: " + ", ".join(fallos), file=sys.stderr)
    sys.exit(1)

# El directorio contiene solo artefactos generados: elimina cuadernos cuyos capítulos ya
# no formen parte del curso.
esperados = {f"{qmd.stem}.ipynb" for qmd in capitulos}
for notebook in SALIDA.glob("*.ipynb"):
    if notebook.name not in esperados:
        notebook.unlink()
