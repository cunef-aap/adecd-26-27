#!/usr/bin/env python3
"""Genera las listas independientes de los perfiles de Quarto.

La base _quarto.yml no debe contener chapters ni appendices: esas listas se
combinan con las del perfil y pueden introducir paginas que no le corresponden.
El perfil revision es el predeterminado del editor y nunca escribe en docs/.

    python scripts/publicado.py --sitio      # contenido.txt -> perfil publica
    python scripts/publicado.py --revision   # publico + revision.txt -> privado
    python scripts/publicado.py --completo   # todo el libro -> privado
    python scripts/publicado.py --estado
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CONTENIDO = RAIZ / "contenido.txt"
REVISION = RAIZ / "revision.txt"
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


def selecciona_revision(capitulos: list, apendices: list) -> tuple[list, list]:
    extras = {
        linea.strip() for linea in REVISION.read_text(encoding="utf-8").splitlines()
        if linea.strip() and not linea.lstrip().startswith("#")
    }
    conocidos = {ruta for _, ruta, _ in capitulos + apendices}
    desconocidos = extras - conocidos
    if desconocidos:
        raise SystemExit("revision.txt contiene rutas ajenas a contenido.txt: "
                         + ", ".join(sorted(desconocidos)))
    def incluye(filas):
        return [(parte, ruta, publico or ruta in extras)
                for parte, ruta, publico in filas]
    return incluye(capitulos), incluye(apendices)


def escribe(todo: bool = False, revision: bool = False) -> tuple[int, int]:
    if todo and revision:
        raise ValueError("elige revision o completo, no ambos")
    perfil = "completo" if todo else "revision" if revision else "publica"
    config = RAIZ / f"_quarto-{perfil}.yml"
    capitulos, apendices = lee_contenido()
    if revision:
        capitulos, apendices = selecciona_revision(capitulos, apendices)
    if config.exists():
        texto = config.read_text(encoding="utf-8")
    else:
        salida = "_completo" if todo else "_completo/local" if revision else "docs"
        texto = (
            f"project:\n  output-dir: {salida}\n\n"
            "format:\n  html:\n    filters:\n"
            "      - scripts/strip-delims.lua\n"
            "      - scripts/enlaces-publicados.lua\n\n"
            f"book:\n{ABRE}\n{CIERRA}\n"
        )
    nuevo = f"{ABRE}\n{bloque(capitulos, apendices, todo)}\n{CIERRA}"
    if ABRE in texto:
        patron = re.compile(re.escape(ABRE) + r".*?" + re.escape(CIERRA), re.S)
        texto = patron.sub(lambda _: nuevo, texto)
    else:
        # primera vez: sustituye el bloque chapters/appendices escrito a mano
        patron = re.compile(r"^  chapters:\n.*?(?=^\S|\Z)", re.S | re.M)
        if not patron.search(texto):
            raise SystemExit(f"no encuentro el bloque chapters en {config.name}")
        texto = patron.sub(nuevo + "\n", texto, count=1)
    config.write_text(texto, encoding="utf-8")
    total = len(capitulos) + len(apendices)
    dentro = sum(1 for _, _, p in capitulos + apendices if todo or p)
    return dentro, total


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "--estado"
    if arg == "--sitio":
        d, t = escribe(todo=False)
        print(f"_quarto-publica.yml: {d} de {t} documentos, salida docs/")
    elif arg == "--revision":
        d, t = escribe(revision=True)
        print(f"_quarto-revision.yml: {d} de {t} documentos, salida _completo/local/")
    elif arg == "--completo":
        d, t = escribe(todo=True)
        print(f"_quarto-completo.yml: {d} de {t} documentos, salida _completo/")
    elif arg == "--estado":
        caps, aps = lee_contenido()
        pub = [r for _, r, p in caps + aps if p]
        print(f"contenido.txt publica {len(pub)} de {len(caps) + len(aps)}:")
        print("\n".join(f"  {r}" for r in pub))
    else:
        raise SystemExit(__doc__)
