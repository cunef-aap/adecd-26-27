#!/usr/bin/env python3
"""Copia los enunciados de una hoja a su solucionario.

El solucionario repite cada enunciado palabra por palabra, con el identificador acabado en
`-sol`. Mantenerlo a mano se desalinea en cuanto se retoca la hoja, asi que se copia.

    python scripts/sincroniza-enunciados.py problemas/hoja-01.qmd
    python scripts/sincroniza-enunciados.py --comprueba problemas/hoja-01.qmd
"""
import re
import sys
from pathlib import Path

CUERPO = r"::: \{{#{id}\}}\n(.*?)\n:::\n"


def cuerpo_del_div(lineas: list[str], apertura: int) -> tuple[str, int]:
    """Cuerpo de un div y la linea de su cierre, contando los divs anidados.

    Hace falta contar: un ejercicio puede llevar dentro una figura, que es otro div, y
    quedarse con el primer `:::` que aparezca corta el enunciado por la mitad. Paso por
    ese aro: el solucionario de la hoja 1 tenia la solucion metida entre la figura y los
    apartados, y el comparador no lo veia porque cometia el mismo error en los dos lados.
    """
    profundidad = 1
    for i in range(apertura + 1, len(lineas)):
        l = lineas[i].rstrip()
        if l.startswith(":::"):
            if re.fullmatch(r":::+", l):
                profundidad -= 1
                if profundidad == 0:
                    return "\n".join(lineas[apertura + 1:i]), i
            else:
                profundidad += 1
    raise ValueError(f"div sin cerrar que abre en la linea {apertura + 1}")


def enunciados(texto: str, sufijo: str = "") -> dict[str, str]:
    lineas = texto.split("\n")
    fuera = {}
    for i, l in enumerate(lineas):
        m = re.fullmatch(r"::: \{#(exr-[\w-]+)\}", l.rstrip())
        if m:
            fuera[m.group(1)] = cuerpo_del_div(lineas, i)[0]
    return fuera


# El solucionario repite el enunciado, pero todo lo que sea etiqueta suya tiene que llevar
# el sufijo -sol: si no, la misma etiqueta queda definida dos veces en el libro y Quarto
# resuelve la cita al documento equivocado sin avisar. Al comparar se quita el sufijo, de
# modo que ese renombrado no cuenta como desalineado.
SUFIJO_ETIQUETA = re.compile(r"(\{#[\w-]+?)-sol(\})")
SUFIJO_CITA = re.compile(r"(@(?:fig|tbl|exr|sec)-[\w-]+?)-sol\b")


def sin_sufijo(cuerpo: str) -> str:
    cuerpo = SUFIJO_ETIQUETA.sub(r"\1\2", cuerpo)
    return SUFIJO_CITA.sub(r"\1", cuerpo)


ETIQUETA_PROPIA = re.compile(r"\{#((?:fig|tbl|sec)-[\w-]+)\}")
CITA_PROPIA = re.compile(r"@((?:fig|tbl|sec)-h\d[\w-]+)\b")


def con_sufijo(cuerpo: str) -> str:
    """Pone -sol en las etiquetas y citas que el solucionario define él mismo."""
    cuerpo = ETIQUETA_PROPIA.sub(lambda m: "{#" + m.group(1) + "-sol}", cuerpo)
    return CITA_PROPIA.sub(lambda m: "@" + m.group(1) + "-sol", cuerpo)


def main() -> int:
    comprueba = "--comprueba" in sys.argv
    rutas = [a for a in sys.argv[1:] if not a.startswith("--")]
    fallos = 0
    for ruta in rutas:
        hoja = Path(ruta)
        sol = hoja.with_name(hoja.stem + "-soluciones.qmd")
        if not sol.exists():
            print(f"no existe {sol}", file=sys.stderr)
            return 1
        origen = enunciados(hoja.read_text(encoding="utf-8"))
        texto = sol.read_text(encoding="utf-8")
        destino = enunciados(texto)
        faltan = {f"{k}-sol" for k in origen} - set(destino)
        sobran = set(destino) - {f"{k}-sol" for k in origen}
        if faltan or sobran:
            print(f"{sol.name}: faltan {sorted(faltan)}, sobran {sorted(sobran)}",
                  file=sys.stderr)
            fallos += 1
        cambiados = []
        for clave, cuerpo in origen.items():
            destino_id = f"{clave}-sol"
            if destino_id not in destino:
                continue
            if sin_sufijo(destino[destino_id]) == cuerpo:
                continue
            cambiados.append(destino_id)
            viejo = f"::: {{#{destino_id}}}\n{destino[destino_id]}\n:::\n"
            nuevo = f"::: {{#{destino_id}}}\n{con_sufijo(cuerpo)}\n:::\n"
            assert texto.count(viejo) == 1, destino_id
            texto = texto.replace(viejo, nuevo)
        if comprueba:
            if cambiados:
                print(f"{sol.name}: enunciados desalineados: {', '.join(cambiados)}",
                      file=sys.stderr)
                fallos += 1
        elif cambiados:
            sol.write_text(texto, encoding="utf-8")
            print(f"{sol.name}: {len(cambiados)} enunciados copiados "
                  f"({', '.join(cambiados)})")
        else:
            print(f"{sol.name}: ya estaba al día")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
