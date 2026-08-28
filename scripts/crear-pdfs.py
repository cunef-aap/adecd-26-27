#!/usr/bin/env python3
"""Imprime a PDF las paginas ya renderizadas del sitio, para subirlas al Campus Virtual.

Imprime desde docs/ con Chrome en modo headless en lugar de renderizar a PDF con LaTeX,
y la razon es que asi las paginas salen con el mismo aspecto que la web y, sobre todo,
con las referencias cruzadas resueltas: `@thm-test-insesgado` sale como "Teorema 4.1"
porque el HTML se renderizo con el libro entero. Un render a PDF de cada capitulo por
separado las dejaria como "?@thm-test-insesgado", y las cajas .sol, .trampa y .cajanegra
perderian su estilo, que vive en assets/styles.css.

    python scripts/crear-pdfs.py                 # capitulos, hojas y apendices
    python scripts/crear-pdfs.py --solo hoja     # solo las hojas de problemas
    python scripts/crear-pdfs.py --solo capitulo # solo los capitulos

Los nombres de salida llevan delante el numero de capitulo o de hoja para que en el
Campus Virtual salgan en orden.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DOCS = RAIZ / "docs"
SALIDA = RAIZ / "pdf"
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

# (glob dentro de docs, subcarpeta de salida, etiqueta para --solo)
GRUPOS = [
    ("capitulos/*.html", "capitulos", "capitulo"),
    ("problemas/hoja-*.html", "problemas", "hoja"),
    ("curso/*.html", "curso", "curso"),
]


def imprime(html: Path, pdf: Path) -> bool:
    pdf.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(
        [str(CHROME), "--headless", "--disable-gpu", "--no-pdf-header-footer",
         "--virtual-time-budget=20000",          # espera a que KaTeX pinte las formulas
         f"--print-to-pdf={pdf}", html.as_uri()],
        capture_output=True, text=True, timeout=300,
    )
    return pdf.exists() and pdf.stat().st_size > 20000 and r.returncode == 0


def main() -> int:
    if not CHROME.exists():
        raise SystemExit(f"no encuentro Chrome en {CHROME}")
    if not DOCS.exists():
        raise SystemExit("no hay docs/: ejecuta antes `make sitio`")
    solo = None
    if "--solo" in sys.argv:
        solo = sys.argv[sys.argv.index("--solo") + 1]

    hechos, fallos = [], []
    for patron, carpeta, etiqueta in GRUPOS:
        if solo and solo != etiqueta:
            continue
        for html in sorted(DOCS.glob(patron)):
            pdf = SALIDA / carpeta / f"{html.stem}.pdf"
            if imprime(html, pdf):
                hechos.append((pdf, pdf.stat().st_size))
            else:
                fallos.append(html)

    for pdf, tam in hechos:
        print(f"  {pdf.relative_to(RAIZ)}  {tam // 1024} KB")
    print(f"\n{len(hechos)} PDF en {SALIDA.relative_to(RAIZ)}/")
    if fallos:
        print("FALLARON:", *[f.name for f in fallos], sep="\n  ")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
