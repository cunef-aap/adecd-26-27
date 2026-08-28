#!/usr/bin/env python3
"""Traduce assets/includes/_macros.tex a un bloque que MathJax entienda.

MathJax es el motor que renderiza matematicas en Google Colab y en Jupyter, y no conoce
todo LaTeX. Dos cosas del contrato de notacion se le atragantan:

  - `\\DeclareMathOperator`, que no implementa. Se traduce a `\\newcommand` con
    `\\operatorname`, que si conoce.
  - `\\coloneqq`, que vive en la extension mathtools y Colab no carga. Se sustituye
    por `\\mathrel{:=}`, que se ve igual.

El resultado se inyecta como primera celda de cada cuaderno (scripts/crear-ipynb.py), de
modo que la notacion del curso funciona en cualquier celda que se anada en clase.

    python scripts/macros-mathjax.py            # imprime el bloque
    python scripts/macros-mathjax.py --celda    # lo imprime como celda de markdown
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FUENTE = RAIZ / "assets" / "includes" / "_macros.tex"

# MathJax parte su tipografia en un fichero por variante y los carga por separado. Cuando
# el de la variante caligrafica no llega, `\mathcal{D}` sale como un cuadrado. La fuente
# base siempre carga, asi que en el cuaderno las letras caligraficas pasan a redonda.
# Solo afecta al cuaderno: los apuntes y el PDF se renderizan con KaTeX, que escribe la
# letra ASCII con una clase de fuente y no depende de esto. A False para volver atras.
CALIGRAFICA_A_REDONDA = True


def sin_caligrafica(texto: str) -> tuple[str, int]:
    """Pasa `\mathcal{L}` a `\mathrm{L}`. Devuelve el texto y cuantas ha cambiado."""
    if not CALIGRAFICA_A_REDONDA:
        return texto, 0
    return re.subn(r"\\mathcal\{(\w)\}", r"\\mathrm{\1}", texto)


AVISO = (
    "<!-- Notacion del curso: define los macros de LaTeX del libro para que la matematica\n"
    "     de este cuaderno, y la de cualquier celda que se escriba en clase, se vea bien\n"
    "     en Colab. No hay nada que ejecutar y no se ve nada al renderizar: va en una\n"
    "     sola linea de matematica en linea, que sale vacia. Generado desde\n"
    "     assets/includes/_macros.tex por scripts/macros-mathjax.py. -->"
)


def traduce(texto: str) -> list[str]:
    """Devuelve las definiciones, una por linea, en la forma que MathJax acepta."""
    lineas = []
    for cruda in texto.split("\n"):
        l = cruda.split("%")[0].strip()          # fuera los comentarios de LaTeX
        if not l:
            continue
        m = re.match(r"\\DeclareMathOperator(\*?)\{\\(\w+)\}\{(.*)\}$", l)
        if m:
            estrella, nombre, cuerpo = m.groups()
            lineas.append(f"\\newcommand{{\\{nombre}}}"
                          f"{{\\operatorname{estrella}{{{cuerpo}}}}}")
            continue
        if re.match(r"\\(?:new|renew)command\{", l):
            lineas.append(l.replace(r"\coloneqq", r"\mathrel{:=}"))
            continue
        raise SystemExit(f"linea que no se sabe traducir a MathJax: {l!r}")
    return lineas


def bloque() -> str:
    """Las definiciones en un solo `$...$`, que MathJax procesa y no dibuja."""
    definiciones = "".join(traduce(FUENTE.read_text(encoding="utf-8")))
    return "$" + sin_caligrafica(definiciones)[0] + "$"


def celda() -> str:
    return AVISO + "\n\n" + bloque()


def nombres_definidos() -> set[str]:
    """Los nombres del contrato de notación, para comprobar que nadie se cuela sin
    expandir en un cuaderno."""
    texto = FUENTE.read_text(encoding="utf-8")
    return (set(re.findall(r"\\(?:new|renew)command\{\\(\w+)\}", texto))
            | set(re.findall(r"\\DeclareMathOperator\*?\{\\(\w+)\}", texto)))


if __name__ == "__main__":
    print(celda() if "--celda" in sys.argv else bloque())
