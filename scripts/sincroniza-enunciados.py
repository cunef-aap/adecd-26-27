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


def enunciados(texto: str, sufijo: str = "") -> dict[str, str]:
    patron = re.compile(r"::: \{#(exr-[\w-]+)\}\n(.*?)\n:::\n", re.S)
    return {m.group(1): m.group(2) for m in patron.finditer(texto)}


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
            if destino[destino_id] == cuerpo:
                continue
            cambiados.append(destino_id)
            viejo = f"::: {{#{destino_id}}}\n{destino[destino_id]}\n:::\n"
            nuevo = f"::: {{#{destino_id}}}\n{cuerpo}\n:::\n"
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
