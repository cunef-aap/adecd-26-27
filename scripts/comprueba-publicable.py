#!/usr/bin/env python3
"""Aborta si algo que no debe publicarse ha llegado al indice de git o a docs/.

El repositorio es publico y lleva las fuentes del libro. Solo dos cosas se quedan fuera, y
.gitignore las excluye: los examenes de evaluacion/ y los solucionarios de las hojas. Esta
comprobacion es la red por si alguien las anade con `git add -f` o por si un enlace desde
una pagina publicada arrastra un .qmd inedito a docs/, que es algo que Quarto hace solo.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DOCS = RAIZ / "docs"


def rastreados() -> list[str]:
    r = subprocess.run(["git", "ls-files"], cwd=RAIZ, capture_output=True, text=True)
    return r.stdout.split("\n")


def main() -> int:
    problemas = []

    prohibidos = [f for f in rastreados()
                  if f.startswith("evaluacion/") or "-soluciones.qmd" in f]
    if prohibidos:
        problemas.append("git rastrea material que no puede ser publico:\n  "
                         + "\n  ".join(prohibidos))

    if DOCS.exists():
        fuentes = sorted(DOCS.rglob("*.qmd"))
        if fuentes:
            problemas.append(
                "hay fuentes .qmd en docs/: una pagina publicada enlaza a otra que no lo\n"
                "esta, y Quarto copia el fuente como recurso. Revisa contenido.txt y que\n"
                "scripts/enlaces-publicados.lua siga en el perfil publica.\n  "
                + "\n  ".join(str(f.relative_to(DOCS)) for f in fuentes))
        colados = sorted(DOCS.rglob("*soluciones*"))
        if colados:
            problemas.append("solucionarios en docs/:\n  "
                             + "\n  ".join(str(f.relative_to(DOCS)) for f in colados))
        if (DOCS / "evaluacion").exists():
            problemas.append("docs/evaluacion existe: material de examen en el sitio")

    if problemas:
        print("\n\n".join(problemas), file=sys.stderr)
        return 1
    print("nada prohibido en el indice ni en docs/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
