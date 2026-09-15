#!/usr/bin/env python3
"""Comprueba la correspondencia entre capítulo, hoja y solucionario sin modificarlos.

Los primeros N ejercicios de la hoja deben repetir los N ejercicios del capítulo,
incluidos sus títulos y en el mismo orden. La hoja puede añadir ejercicios después.
Si existe un solucionario junto a la hoja, también se comprueba su correspondencia.

    python scripts/comprueba-ejercicios-capitulo.py \\
        capitulos/02-aprender-minimizando.qmd problemas/hoja-02.qmd
"""
from __future__ import annotations

import argparse
from collections import Counter
import importlib.util
from pathlib import Path
import re
import sys


def carga_extractor():
    ruta = Path(__file__).with_name("sincroniza-enunciados.py")
    spec = importlib.util.spec_from_file_location("sincroniza_enunciados", ruta)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"no se puede cargar {ruta}")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


EXTRACTOR = carga_extractor()
EJERCICIO = re.compile(r"::: \{#(exr-[\w-]+)\}")
SOLUCION = re.compile(r":::+\s+\{[^}]*\.sol(?:\s|\})")


def normaliza(cuerpo: str) -> str:
    """Ignora espacios de fin de línea y líneas vacías exteriores, no el contenido.

    Conserva la indentación del código, los saltos internos y todas las fórmulas.
    splitlines también iguala los finales de línea de Windows y Unix.
    """
    return "\n".join(linea.rstrip() for linea in cuerpo.splitlines()).strip("\n")


def titulo(cuerpo: str) -> str:
    for linea in cuerpo.splitlines():
        if linea.strip():
            return re.sub(r"^#+\s*", "", linea.strip())
    return "(sin título ni enunciado)"


def lee_ejercicios(ruta: Path) -> tuple[str, list[tuple[str, str]]]:
    texto = ruta.read_text(encoding="utf-8")
    ids = [m.group(1) for linea in texto.splitlines()
           if (m := EJERCICIO.fullmatch(linea.rstrip()))]
    repetidos = [clave for clave, n in Counter(ids).items() if n > 1]
    if repetidos:
        raise ValueError(f"{ruta}: identificadores repetidos: {', '.join(repetidos)}")
    ejercicios = list(EXTRACTOR.enunciados(texto).items())
    if not ejercicios:
        raise ValueError(f"{ruta}: no se han encontrado ejercicios #exr-")
    return texto, ejercicios


def compara_capitulo(capitulo: Path, hoja: Path,
                     origen: list[tuple[str, str]],
                     destino: list[tuple[str, str]]) -> list[str]:
    fallos = []
    for numero, (clave, cuerpo) in enumerate(origen, 1):
        etiqueta = f"ejercicio {numero}, «{titulo(cuerpo)}» ({clave})"
        if numero > len(destino):
            fallos.append(f"{hoja}: falta {etiqueta} de {capitulo.name}")
            continue
        destino_id, destino_cuerpo = destino[numero - 1]
        if normaliza(cuerpo) != normaliza(destino_cuerpo):
            fallos.append(
                f"{hoja}: {etiqueta} no coincide con el capítulo; en esa posición "
                f"figura «{titulo(destino_cuerpo)}» ({destino_id}). "
                "Deben coincidir título y enunciado, no solo el tema.")
    return fallos


def comprueba_cajas_solucion(ruta: Path, texto: str) -> list[str]:
    """Exige una caja .sol por ejercicio, fuera de su enunciado y no vacía.

    Cada bloque se consume entero con el mismo contador de divs anidados que usa
    sincroniza-enunciados.py. Una figura interna no corta la solución ni el ejercicio.
    """
    fallos = []
    lineas = texto.splitlines()
    actual = None
    cantidad = 0
    numero = 0
    i = 0

    def cierra_ejercicio():
        if actual is not None and cantidad != 1:
            fallos.append(f"{ruta}: {actual}: se esperaba una caja .sol; "
                          f"hay {cantidad}")

    while i < len(lineas):
        linea = lineas[i].rstrip()
        m = EJERCICIO.fullmatch(linea)
        if m:
            cierra_ejercicio()
            cuerpo, cierre = EXTRACTOR.cuerpo_del_div(lineas, i)
            numero += 1
            actual = f"ejercicio {numero}, «{titulo(cuerpo)}» ({m.group(1)})"
            cantidad = 0
            if any(SOLUCION.match(l.rstrip()) for l in cuerpo.splitlines()):
                fallos.append(f"{ruta}: {actual}: la caja .sol está dentro del enunciado")
            i = cierre + 1
            continue
        if SOLUCION.match(linea):
            cuerpo, cierre = EXTRACTOR.cuerpo_del_div(lineas, i)
            if actual is None:
                fallos.append(f"{ruta}: caja .sol sin ejercicio previo (línea {i + 1})")
            else:
                cantidad += 1
                if not normaliza(cuerpo).strip():
                    fallos.append(f"{ruta}: {actual}: caja .sol vacía")
            i = cierre + 1
            continue
        i += 1
    cierra_ejercicio()
    return fallos


def compara_solucionario(hoja: Path, origen: list[tuple[str, str]]) -> list[str]:
    ruta = hoja.with_name(hoja.stem + "-soluciones.qmd")
    if not ruta.exists():
        return []
    texto, destino = lee_ejercicios(ruta)
    fallos = []
    if len(origen) != len(destino):
        fallos.append(f"{ruta}: hay {len(destino)} enunciados; "
                      f"la hoja tiene {len(origen)}")
    for numero, (clave, cuerpo) in enumerate(origen, 1):
        etiqueta = f"ejercicio {numero}, «{titulo(cuerpo)}»"
        esperado = clave + "-sol"
        if numero > len(destino):
            fallos.append(f"{ruta}: falta {etiqueta} ({esperado})")
            continue
        destino_id, destino_cuerpo = destino[numero - 1]
        if destino_id != esperado:
            fallos.append(f"{ruta}: {etiqueta}: se esperaba {esperado}, "
                          f"pero figura {destino_id}; revisar el orden")
        if normaliza(cuerpo) != normaliza(EXTRACTOR.sin_sufijo(destino_cuerpo)):
            fallos.append(f"{ruta}: {etiqueta} ({destino_id}): "
                          "título o enunciado distintos de la hoja")
    fallos.extend(comprueba_cajas_solucion(ruta, texto))
    return fallos


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("capitulo", type=Path)
    parser.add_argument("hoja", type=Path)
    args = parser.parse_args()
    try:
        _, capitulo = lee_ejercicios(args.capitulo)
        _, hoja = lee_ejercicios(args.hoja)
        fallos = compara_capitulo(args.capitulo, args.hoja, capitulo, hoja)
        fallos.extend(compara_solucionario(args.hoja, hoja))
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if fallos:
        for fallo in fallos:
            print(f"ERROR: {fallo}", file=sys.stderr)
        return 1
    sol = args.hoja.with_name(args.hoja.stem + "-soluciones.qmd")
    detalle_sol = "; solucionario alineado y una solución por ejercicio" if sol.exists() else ""
    print(f"{args.hoja}: primeros {len(capitulo)} ejercicios idénticos al capítulo "
          f"y en el mismo orden ({len(hoja)} en total){detalle_sol}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
