#!/usr/bin/env python3
"""Escribe la lista de capitulos de _quarto.yml a partir de contenido.txt.

El sitio publico solo lleva el material con version definitiva; el resto se queda en el
repositorio privado. Quien decide que entra es contenido.txt, y este script lo traduce al
bloque de capitulos de _quarto.yml, entre dos centinelas.

Hace falta un script porque en un proyecto `book` de Quarto los perfiles NO pueden reducir
el libro: `book.chapters` y `project.render` declarados en un `_quarto-PERFIL.yml` se
ignoran, y Quarto renderiza todos los capitulos de _quarto.yml. Comprobado con Quarto
1.10.18.

    python scripts/publicado.py --sitio      # solo lo publicado -> para `make sitio`
    python scripts/publicado.py --completo   # todo el libro     -> para `make pdfs`
    python scripts/publicado.py --estado

`make sitio` deja siempre _quarto.yml en modo --sitio, que es el estado normal del
repositorio.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CONFIG = RAIZ / "_quarto.yml"
CONTENIDO = RAIZ / "contenido.txt"
ABRE = "  # <<< generado por scripts/publicado.py a partir de contenido.txt"
CIERRA = "  # >>> fin del bloque generado"


def lee_contenido() -> tuple[list, list]:
    """Devuelve (capitulos, apendices) como listas de (parte|None, ruta, publicado)."""
    capitulos, apendices = [], []
    destino, parte = capitulos, None
    for cruda in CONTENIDO.read_text(encoding="utf-8").split("\n"):
        l = cruda.strip()
        if not l or l.startswith("#"):
            continue
        if l.startswith("{") and l.endswith("}"):
            destino, parte = apendices, None
            continue
        if l.startswith("[") and l.endswith("]"):
            parte = l[1:-1]
            continue
        publicado = not l.startswith("- ")
        ruta = l[2:].strip() if not publicado else l
        if not (RAIZ / ruta).exists():
            raise SystemExit(f"contenido.txt apunta a un fichero que no existe: {ruta}")
        destino.append((parte, ruta, publicado))
    return capitulos, apendices


def bloque(capitulos: list, apendices: list, todo: bool) -> str:
    lineas = ["  chapters:"]
    parte_abierta = None
    for parte, ruta, publicado in capitulos:
        if not (todo or publicado):
            continue
        if parte != parte_abierta:
            if parte is not None:
                lineas.append(f'    - part: "{parte}"')
                lineas.append("      chapters:")
            parte_abierta = parte
        sangria = "        " if parte is not None else "    "
        lineas.append(f"{sangria}- {ruta}")
    visibles = [r for _, r, p in apendices if todo or p]
    if visibles:
        lineas.append("  appendices:")
        lineas += [f"    - {r}" for r in visibles]
    return "\n".join(lineas)


def escribe(todo: bool) -> tuple[int, int]:
    capitulos, apendices = lee_contenido()
    texto = CONFIG.read_text(encoding="utf-8")
    nuevo = f"{ABRE}\n{bloque(capitulos, apendices, todo)}\n{CIERRA}"
    if ABRE in texto:
        patron = re.compile(re.escape(ABRE) + r".*?" + re.escape(CIERRA), re.S)
        texto = patron.sub(lambda _: nuevo, texto)
    else:
        # primera vez: sustituye el bloque chapters/appendices escrito a mano
        patron = re.compile(r"^  chapters:\n.*?(?=^\S|\Z)", re.S | re.M)
        if not patron.search(texto):
            raise SystemExit("no encuentro el bloque `chapters:` de _quarto.yml")
        texto = patron.sub(nuevo + "\n", texto, count=1)
    CONFIG.write_text(texto, encoding="utf-8")
    total = len(capitulos) + len(apendices)
    dentro = sum(1 for _, _, p in capitulos + apendices if todo or p)
    return dentro, total


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "--estado"
    if arg == "--sitio":
        d, t = escribe(todo=False)
        print(f"_quarto.yml en modo sitio: {d} de {t} documentos")
    elif arg == "--completo":
        d, t = escribe(todo=True)
        print(f"_quarto.yml en modo completo: {d} de {t} documentos")
    elif arg == "--estado":
        caps, aps = lee_contenido()
        pub = [r for _, r, p in caps + aps if p]
        print(f"contenido.txt publica {len(pub)} de {len(caps) + len(aps)}:")
        print("\n".join(f"  {r}" for r in pub))
    else:
        raise SystemExit(__doc__)
