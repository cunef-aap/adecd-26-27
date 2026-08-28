#!/usr/bin/env python3
"""Comprueba las reglas mecánicas de estilo del curso.

Son las reglas verificables de la skill `write-roinaveiro-es`, contrastadas contra
el corpus propio (~/CUNEF/teaching/AEINF/aeinf_central): en él hay 0 rayas, 0
comillas latinas, 0 emoji y 0 formas de usted/ustedes.

Lo que NO comprueba: el tono. Que una frase venda o no venda no lo decide un
regex. Esto solo caza lo mecánico.

Uso:  python scripts/check-estilo.py [--fix]
      --fix aplica únicamente las sustituciones inequívocas (comillas latinas).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
EXCLUIR = {"_referencia", "docs", ".quarto", "_freeze"}

# --- Reglas ----------------------------------------------------------------
# (clave, patrón, explicación, ¿autocorregible?)
REGLAS = [
    (
        "raya",
        re.compile(r"—"),
        "raya (—) para incisos: usa paréntesis, coma, dos puntos o dos frases",
        False,
    ),
    (
        "comillas-latinas",
        re.compile(r"[«»]"),
        "comillas latinas: usa comillas rectas",
        True,
    ),
    (
        "usted",
        re.compile(
            r"\b(usted|ustedes|dígalo|díganlo|escríbanlo|escriban|léanlas|léanlo|"
            r"denle|fíjense|recuerden|tengan en cuenta|obsérvese que ustedes)\b",
            re.IGNORECASE,
        ),
        "tratamiento de usted/ustedes: la voz usa nosotros (exposición) y tú (ejercicios)",
        False,
    ),
    (
        # Ojo: las flechas matemáticas (↔, →, ⟹) son notación legítima y no van aquí.
        "emoji",
        re.compile(r"[\U0001F300-\U0001FAFF⬛-⬜⚠✅❌❗❓]"),
        "emoji",
        False,
    ),
    (
        "superlativo",
        re.compile(
            r"\b(el|la|lo)\s+(más|mejor|peor|único|única)\b[^.\n]{0,40}"
            r"\b(del curso|de la asignatura|del capítulo|de todo)\b",
            re.IGNORECASE,
        ),
        "superlativo sobre el propio material",
        False,
    ),
    (
        "autobombo",
        re.compile(
            r"\b(la inversión más rentable|la razón de ser|dígalo en voz alta|"
            r"díselo en voz alta|no lo cortes|no la corten|fíjate en lo que acaba|"
            r"fíjense en lo que acaba|y es el capítulo entero|hace todo el trabajo|"
            r"la bisagra|el andamio|la pieza que hace|el mejor argumento)\b",
            re.IGNORECASE,
        ),
        "frase de venta",
        False,
    ),
    (
        # El anuncio de la lectura: una frase que presenta la cifra o la tabla que viene
        # detras, en lugar de darla. Ver la seccion homonima de write-roinaveiro-es.
        "anuncio",
        re.compile(
            r"(ahí (está|están) (el|la|los|las)\b|ahí lo tienes|"
            r"la lectura es la que|cuenta la historia|"
            r"conviene leer(los|las) juntos|conviene leerlas juntas|"
            r"lo que falta es lo contrario|"
            r"^(eso|esto) ya (es|está)\b)",
            re.IGNORECASE | re.MULTILINE,
        ),
        "anuncio de la lectura: da la cifra o la tabla, no la presentes",
        False,
    ),
    (
        "intensificador",
        re.compile(
            r"\b(de verdad|sin parar|para nada|con enorme fluidez|"
            r"muchísimo|clarísimo|facilísimo)\b",
            re.IGNORECASE,
        ),
        "intensificador coloquial: sustitúyelo por el dato concreto",
        False,
    ),
]

SUSTITUCIONES = {"«": '"', "»": '"'}


def ficheros():
    for p in sorted(RAIZ.rglob("*.qmd")):
        if not EXCLUIR & set(p.parts):
            yield p
    for p in sorted(RAIZ.rglob("*.md")):
        if not EXCLUIR & set(p.parts) and p.name != "PROCEDENCIA.md":
            yield p


def main(arreglar: bool = False) -> int:
    total = 0
    por_regla: dict[str, int] = {}

    for p in ficheros():
        texto = p.read_text(encoding="utf-8")
        original = texto
        rel = p.relative_to(RAIZ)

        for clave, patron, explica, autofix in REGLAS:
            for m in patron.finditer(texto):
                linea = texto[: m.start()].count("\n") + 1
                ctx = texto.splitlines()[linea - 1].strip()[:88]
                print(f"{rel}:{linea}: {explica}\n    {ctx}")
                total += 1
                por_regla[clave] = por_regla.get(clave, 0) + 1

        if arreglar:
            for a, b in SUSTITUCIONES.items():
                texto = texto.replace(a, b)
            if texto != original:
                p.write_text(texto, encoding="utf-8")

    print()
    if total == 0:
        print("estilo: OK")
        return 0
    print(f"estilo: {total} avisos")
    for k, v in sorted(por_regla.items(), key=lambda kv: -kv[1]):
        print(f"  {v:4d}  {k}")
    return 1


if __name__ == "__main__":
    sys.exit(main(arreglar="--fix" in sys.argv))
