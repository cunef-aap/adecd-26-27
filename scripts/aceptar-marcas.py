#!/usr/bin/env python3
"""Gestiona las marcas de revision `.nuevo`.

Mientras un capitulo esta en revision, lo que se ha escrito o reescrito va
marcado para que el autor no tenga que releerlo entero:

    [una frase suelta]{.nuevo}

    ::: {.nuevo}
    un parrafo, un resultado, una demostracion o un apartado entero
    :::

Aceptar un cambio es quitarle la marca y dejar el contenido. Este script lo
hace en bloque, cuando ya se ha revisado el fichero. Para aceptar cambios uno a
uno basta con borrar la marca a mano en el editor.

OJO: un span alrededor de una formula se pierde al generar el cuaderno, porque
`scripts/clean-eqref.lua` colapsa los spans que contienen matematicas. Para
marcar una ecuacion se usa el div alrededor del `$$`.

Uso:  python scripts/aceptar-marcas.py --listar [ficheros...]
      python scripts/aceptar-marcas.py --aceptar [ficheros...]
      Sin ficheros, recorre capitulos/, problemas/, evaluacion/ y curso/.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIRECTORIOS = ("capitulos", "problemas", "evaluacion", "curso")

SPAN = re.compile(r"\[([^\[\]]*)\]\{\.nuevo\}", re.S)
ABRE = re.compile(r"^\s*:::+\s*\{\.nuevo\}\s*$")
CIERRA = re.compile(r"^\s*:::+\s*$")


def ficheros(argv: list[str]):
    sueltos = [Path(a) for a in argv if not a.startswith("--")]
    if sueltos:
        yield from (p.resolve() for p in sueltos)
        return
    for d in DIRECTORIOS:
        yield from sorted((RAIZ / d).glob("*.qmd"))


def marcas(texto: str):
    """(linea, tipo) de cada marca."""
    encontradas = []
    for m in SPAN.finditer(texto):
        encontradas.append((texto[: m.start()].count("\n") + 1, "span"))
    for i, linea in enumerate(texto.splitlines(), 1):
        if ABRE.match(linea):
            encontradas.append((i, "div"))
    return sorted(encontradas)


def acepta(texto: str) -> tuple[str, int]:
    """Quita las marcas conservando el contenido."""
    texto, n_spans = SPAN.subn(r"\1", texto)

    lineas = texto.splitlines()
    salida = []
    pila = []          # profundidad de divs abiertos desde una marca
    profundidad = 0
    n_divs = 0
    for linea in lineas:
        if ABRE.match(linea):
            pila.append(profundidad)
            profundidad += 1
            n_divs += 1
            continue
        if re.match(r"^\s*:::", linea):
            if CIERRA.match(linea):
                profundidad -= 1
                if pila and profundidad == pila[-1]:
                    pila.pop()
                    continue
            else:
                profundidad += 1
        salida.append(linea)
    return "\n".join(salida) + "\n", n_spans + n_divs


def main(argv: list[str]) -> int:
    aceptar = "--aceptar" in argv
    listar = "--listar" in argv or not aceptar

    total = 0
    for ruta in ficheros(argv):
        if not ruta.exists():
            print(f"{ruta}: no existe")
            return 1
        texto = ruta.read_text(encoding="utf-8")
        encontradas = marcas(texto)
        if not encontradas:
            continue
        rel = ruta.relative_to(RAIZ) if ruta.is_relative_to(RAIZ) else ruta
        if listar:
            for linea, tipo in encontradas:
                contexto = texto.splitlines()[linea - 1].strip()[:80]
                print(f"{rel}:{linea}: marca ({tipo})\n    {contexto}")
        total += len(encontradas)
        if aceptar:
            nuevo, n = acepta(texto)
            ruta.write_text(nuevo, encoding="utf-8")
            print(f"{rel}: {n} marcas aceptadas")

    print()
    if total == 0:
        print("marcas: ninguna")
        return 0
    if aceptar:
        print(f"marcas: {total} aceptadas")
        return 0
    print(f"marcas: {total} sin resolver")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
