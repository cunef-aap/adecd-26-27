"""Genera la hoja resuelta a partir de la hoja de enunciados y un diccionario de soluciones."""
from pathlib import Path


def generar(hoja, destino, soluciones, encabezado_nuevo, frase_nueva=None, frase_vieja=None):
    lineas = Path(hoja).read_text(encoding="utf-8").splitlines()
    salida, i = [], 0
    while i < len(lineas):
        salida.append(lineas[i])
        etiqueta = None
        if lineas[i].startswith("::: {#exr-"):
            etiqueta = lineas[i][len("::: {#"):-1]
        if etiqueta and etiqueta in soluciones:
            j, prof = i + 1, 1
            while j < len(lineas) and prof:
                salida.append(lineas[j])
                if lineas[j].startswith(":::") and lineas[j].strip() != ":::":
                    prof += 1
                elif lineas[j].strip() == ":::":
                    prof -= 1
                j += 1
            salida.append("")
            salida.extend(soluciones[etiqueta].strip("\n").splitlines())
            i = j - 1
        i += 1
    texto = "\n".join(salida) + "\n"
    texto = texto.replace(lineas[0], encabezado_nuevo, 1)
    # Los dos ficheros del par se publican, asi que sus etiquetas no pueden coincidir:
    # Quarto resolveria las referencias de la hoja hacia la pagina de soluciones.
    import re as _re
    propias = set(_re.findall(r"\{#((?:exr|sec)-h\d+-[A-Za-z0-9_-]+)\}", texto))
    for etiqueta in sorted(propias, key=len, reverse=True):
        texto = texto.replace(f"{{#{etiqueta}}}", f"{{#{etiqueta}-sol}}")
        texto = _re.sub(rf"@{_re.escape(etiqueta)}(?![A-Za-z0-9_-])", f"@{etiqueta}-sol", texto)
    if frase_vieja and frase_nueva:
        assert frase_vieja in texto, "no encuentro la frase de encuadre"
        texto = texto.replace(frase_vieja, frase_nueva, 1)
    # el aviso de que las soluciones se publican despues no va en la hoja resuelta
    import re
    texto = re.sub(r"::: \{\.callout-note appearance=\"simple\"\}\n[^:]*?\n:::\n", "", texto)
    Path(destino).write_text(texto, encoding="utf-8")
    faltan = [e for e in soluciones if f"::: {{#{e}}}" not in texto]
    return texto.count("::: {.sol}"), faltan
