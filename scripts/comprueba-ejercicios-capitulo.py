#!/usr/bin/env python3
"""Comprueba la correspondencia entre capítulo, hoja y solucionario sin modificarlos.

Los primeros N ejercicios de la hoja deben repetir los enunciados del capítulo,
en el mismo orden; el título inicial puede omitirse. La clave YAML opcional
`ejercicios-capitulo` selecciona qué ejercicios del capítulo se reproducen. Sin
esa clave se exigen todos. La hoja puede añadir ejercicios después.
Si existe un solucionario junto a la hoja, se compara estrictamente con la hoja,
incluidos los títulos que esta conserve.

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

import yaml


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


def normaliza_sin_titulo(cuerpo: str) -> str:
    """Omite solo un heading inicial; conserva los apartados y el resto del cuerpo.

    No busca headings tras párrafos, divs o fences de código. Una línea indentada
    tampoco se interpreta como título: puede formar parte de un bloque de código.
    Esta excepción solo se usa entre capítulo y hoja, nunca en el solucionario.
    """
    limpio = normaliza(cuerpo)
    lineas = limpio.splitlines()
    if lineas and re.fullmatch(r"#{1,6}(?:[ \t]+.*)?", lineas[0]):
        return normaliza("\n".join(lineas[1:]))
    return limpio


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


def selecciona_capitulo(hoja: Path, texto: str,
                       ejercicios: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Valida la selección explícita de la hoja sin alterar el orden del capítulo."""
    lineas = texto.splitlines()
    if not lineas or lineas[0].strip() != "---":
        return ejercicios
    cierre = next((i for i in range(1, len(lineas))
                   if lineas[i].strip() in {"---", "..."}), None)
    if cierre is None:
        raise ValueError(f"{hoja}: cabecera YAML sin cerrar")
    try:
        cabecera = yaml.safe_load("\n".join(lineas[1:cierre]))
    except yaml.YAMLError as exc:
        raise ValueError(f"{hoja}: cabecera YAML inválida: {exc}") from exc
    if cabecera is None:
        return ejercicios
    if not isinstance(cabecera, dict):
        raise ValueError(f"{hoja}: la cabecera YAML debe ser un mapa de claves")
    if "ejercicios-capitulo" not in cabecera:
        return ejercicios
    seleccion = cabecera["ejercicios-capitulo"]
    if (not isinstance(seleccion, list) or not seleccion
            or any(not isinstance(clave, str)
                   or not re.fullmatch(r"exr-[\w-]+", clave) for clave in seleccion)):
        raise ValueError(f"{hoja}: ejercicios-capitulo debe ser una lista no vacía "
                         "de identificadores exr-")
    repetidos = [clave for clave, n in Counter(seleccion).items() if n > 1]
    if repetidos:
        raise ValueError(f"{hoja}: ejercicios-capitulo contiene identificadores "
                         f"repetidos: {', '.join(repetidos)}")
    posiciones = {clave: i for i, (clave, _) in enumerate(ejercicios)}
    desconocidos = [clave for clave in seleccion if clave not in posiciones]
    if desconocidos:
        raise ValueError(f"{hoja}: ejercicios-capitulo contiene identificadores "
                         f"ausentes del capítulo: {', '.join(desconocidos)}")
    indices = [posiciones[clave] for clave in seleccion]
    if indices != sorted(indices):
        raise ValueError(f"{hoja}: ejercicios-capitulo debe conservar el orden "
                         "de los ejercicios del capítulo")
    return [ejercicios[i] for i in indices]


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
        if normaliza_sin_titulo(cuerpo) != normaliza_sin_titulo(destino_cuerpo):
            fallos.append(
                f"{hoja}: {etiqueta} no coincide con el capítulo; en esa posición "
                f"figura «{titulo(destino_cuerpo)}» ({destino_id}). "
                "Debe coincidir todo el enunciado, salvo el título inicial; "
                "no basta con que trate el mismo tema.")
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
        texto_hoja, hoja = lee_ejercicios(args.hoja)
        capitulo = selecciona_capitulo(args.hoja, texto_hoja, capitulo)
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
    print(f"{args.hoja}: primeros {len(capitulo)} enunciados idénticos a los del capítulo "
          f"exigidos por la hoja, salvo títulos, y en el mismo orden "
          f"({len(hoja)} en total){detalle_sol}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
