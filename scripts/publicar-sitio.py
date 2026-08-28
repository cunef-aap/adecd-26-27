#!/usr/bin/env python3
"""Publica docs/ en el repositorio publico del sitio.

El repositorio publico contiene SOLO el sitio renderizado, sin fuentes. La razon es que
este repositorio lleva material de evaluacion (banco de preguntas, parcial, ejercicios tipo
examen con solucion) y los solucionarios de las hojas, y la organizacion esta en plan free,
donde GitHub Pages exige que el repositorio sea publico. Separandolos, lo sensible no puede
filtrarse por descuido: en el publico no hay nada mas que HTML.

    python scripts/publicar-sitio.py            # sincroniza y sube
    python scripts/publicar-sitio.py --seco     # dice que cambiaria, sin subir

El clon del repositorio publico vive en _sitio-publicado/, que git ignora.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DOCS = RAIZ / "docs"
CLON = RAIZ / "_sitio-publicado"
REMOTO = "https://github.com/cunef-aap/adecd-26-27.git"


def sh(*orden, cwd=None, comprobar=True):
    r = subprocess.run(orden, cwd=cwd or RAIZ, capture_output=True, text=True)
    if comprobar and r.returncode:
        raise SystemExit(f"falló {' '.join(orden)}\n{r.stdout}\n{r.stderr}")
    return r.stdout.strip()


def main() -> int:
    seco = "--seco" in sys.argv
    if not (DOCS / "index.html").exists():
        raise SystemExit("no hay docs/index.html: ejecuta antes `make sitio`")
    # Un .qmd en docs/ significa que una pagina publicada enlaza a otra que no lo esta:
    # Quarto la trata como recurso y copia el FUENTE. Es la via por la que se publicaria un
    # capitulo inedito o un solucionario. Lo evita scripts/enlaces-publicados.lua, y esta
    # guarda esta aqui por si alguien lo quita del perfil.
    fuentes = sorted(DOCS.rglob("*.qmd"))
    if fuentes:
        raise SystemExit("hay fuentes .qmd en docs/, no publico:\n  "
                         + "\n  ".join(str(f.relative_to(DOCS)) for f in fuentes))
    colados = sorted(DOCS.rglob("*soluciones*"))
    if colados:
        raise SystemExit("los solucionarios están en docs/: revisa contenido.txt")
    if (DOCS / "evaluacion").exists():
        raise SystemExit("docs/evaluacion existe: material de examen en el sitio, aborto")
    if not list((DOCS / "live-notebooks").glob("*.ipynb")):
        raise SystemExit("faltan los cuadernos en docs/live-notebooks: `quarto render` "
                         "limpia docs/, asi que ejecuta `make notebooks` DESPUES del render")

    if not (CLON / ".git").exists():
        CLON.mkdir(exist_ok=True)
        sh("git", "clone", REMOTO, str(CLON))

    # `--delete` para que las paginas retiradas desaparezcan tambien del sitio publicado
    sh("rsync", "-a", "--delete", "--exclude", ".git/", "--exclude", ".DS_Store",
       f"{DOCS}/", f"{CLON}/")
    sh("git", "add", "-A", cwd=CLON)
    estado = sh("git", "status", "--porcelain", cwd=CLON)
    if not estado:
        print("el sitio publicado ya está al día")
        return 0
    print(f"{len(estado.splitlines())} ficheros cambian en el sitio publicado")
    if seco:
        print(estado[:1500])
        return 0
    sh("git", "-c", "user.name=Roi Naveiro", "-c", "user.email=roi.naveiro@cunef.edu",
       "commit", "-q", "-m", "Actualiza el sitio", cwd=CLON)
    sh("git", "push", "-q", "origin", "main", cwd=CLON)
    print("subido a https://cunef-aap.github.io/adecd-26-27/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
