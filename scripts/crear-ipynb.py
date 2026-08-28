#!/usr/bin/env python3
"""Genera un .ipynb por capitulo con el codigo entre centinelas sustituido
por un hueco, para completar en vivo en clase.

Solo genera los cuadernos de los capitulos PUBLICADOS en contenido.txt: docs/ se sube a un
repositorio publico, asi que un cuaderno de un capitulo todavia inedito se publicaria con el.

Adaptado de PhilChodrow/ml-notes-update (scripts/create-ipynb.py), sin la
importacion de dotenv que alli sobra y no esta en requirements.txt.
"""
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

# El fichero lleva guion, que no es un nombre de modulo valido, asi que se carga a mano.
_spec = importlib.util.spec_from_file_location(
    "macros_mathjax", Path(__file__).resolve().parent / "macros-mathjax.py")
_macros = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_macros)
celda_notacion, nombres_definidos = _macros.celda, _macros.nombres_definidos
sin_caligrafica = _macros.sin_caligrafica

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "docs" / "live-notebooks"
SALIDA.mkdir(parents=True, exist_ok=True)

def publicados() -> set[str]:
    """Rutas de contenido.txt sin el `-` que marca lo no publicado."""
    fichero = RAIZ / "contenido.txt"
    if not fichero.exists():
        return set()
    dentro = set()
    for cruda in fichero.read_text(encoding="utf-8").split("\n"):
        l = cruda.strip()
        if not l or l.startswith(("#", "-", "[", "{")):
            continue
        dentro.add(l)
    return dentro


DENTRO = publicados()
capitulos = [q for q in sorted((RAIZ / "capitulos").glob("*.qmd"))
             if f"capitulos/{q.name}" in DENTRO]
# El anexo de Colab no es un capitulo, pero es el cuaderno con el que se aprende a usar
# la herramienta, asi que se genera igual.
if "curso/colab.qmd" in DENTRO:
    capitulos.append(RAIZ / "curso" / "colab.qmd")
if not capitulos:
    print("ningun capitulo publicado en contenido.txt: no hay cuadernos que generar")
fallos = []
for qmd in capitulos:
    print(f"-> {qmd.name}")
    r = subprocess.run(
        ["quarto", "render", str(qmd), "--profile", "notebooks",
         "--to", "ipynb", "--output", f"{qmd.stem}.ipynb", "--no-execute"],
        cwd=RAIZ,
    )
    if r.returncode:
        fallos.append(qmd.name)

# Quarto crea este redirect al renderizar un capítulo de un proyecto `book`, pero su
# destino no existe dentro del directorio de cuadernos.
(SALIDA / "index.html").unlink(missing_ok=True)


def notacion_al_principio(ruta: Path) -> None:
    """Mete la celda de notación como primera celda, y sin duplicarla."""
    nb = json.loads(ruta.read_text(encoding="utf-8"))
    marca = "scripts/macros-mathjax.py"
    nb["cells"] = [c for c in nb["cells"] if marca not in "".join(c["source"])]
    nb["cells"].insert(0, {"cell_type": "markdown", "metadata": {},
                           "source": celda_notacion().split("\n")})
    # `source` es una lista de líneas y cada una lleva su salto, salvo la última.
    fuente = nb["cells"][0]["source"]
    nb["cells"][0]["source"] = [l + "\n" for l in fuente[:-1]] + [fuente[-1]]
    ruta.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


SITIO = "https://cunef-aap.github.io/adecd-26-27"

# El articulo va en la tabla: la referencia sustituye a `?@etiqueta` dentro de la prosa,
# y sin articulo queda coja («de definicion Riesgo»).
TIPOS = {"eq": "la ecuación", "thm": "el teorema", "def": "la definición",
         "prp": "la proposición", "lem": "el lema", "cor": "el corolario",
         "exm": "el ejemplo", "exr": "el ejercicio", "fig": "la figura",
         "tbl": "la tabla", "sec": "la sección"}


def indice_etiquetas() -> dict[str, tuple[str, str]]:
    """etiqueta -> (fichero fuente, titulo). Sirve para convertir en enlaces utiles las
    referencias que un render suelto de un capitulo no sabe resolver."""
    indice = {}
    for carpeta in ("capitulos", "curso", "problemas"):
        for qmd in sorted((RAIZ / carpeta).glob("*.qmd")):
            lineas = qmd.read_text(encoding="utf-8").split("\n")
            for i, l in enumerate(lineas):
                m = re.search(r"\{#((?:" + "|".join(TIPOS) + r")-[\w-]+)\}", l)
                if not m:
                    continue
                titulo = ""
                for siguiente in lineas[i + 1:i + 3]:
                    t = siguiente.strip()
                    if t.startswith("#"):
                        titulo = t.lstrip("# ").strip()
                        break
                indice[m.group(1)] = (f"{carpeta}/{qmd.name}", titulo)
    return indice


def limpia_para_colab(ruta: Path, indice: dict[str, tuple[str, str]]) -> dict[str, int]:
    """Quita del cuaderno lo que en Colab no se ve o no se puede pulsar.

    Un cuaderno es un render suelto de un capitulo de un libro, de modo que arrastra tres
    cosas que en Colab sobran: las marcas de revision del repositorio, los enlaces internos
    a anclas que no existen en el cuaderno, y las referencias que Quarto no supo resolver y
    escribe como `?@etiqueta`. Las dos ultimas se convierten en enlaces a la pagina
    publicada cuando el capitulo de destino esta publicado, y en texto llano cuando no.
    """
    def pagina(fuente: str) -> str | None:
        return f"{SITIO}/{fuente[:-4]}.html" if fuente in DENTRO else None

    cuenta = {"marcas de revisión": 0, "referencias": 0, "enlaces internos": 0,
              "letras caligráficas": 0}

    def sin_marca(m):
        cuenta["marcas de revisión"] += 1
        return m.group(1)

    def referencia(m):
        cuenta["referencias"] += 1
        etiqueta = m.group(1)
        fuente, titulo = indice.get(etiqueta, ("", ""))
        nombre = TIPOS.get(etiqueta.split("-")[0], "el resultado")
        texto = f"{nombre} «{titulo}»" if titulo else f"{nombre} `{etiqueta}`"
        url = pagina(fuente) if fuente else None
        return f"[{texto}]({url}#{etiqueta})" if url else texto

    def interno(m):
        cuenta["enlaces internos"] += 1
        etiqueta, texto = m.group(1), m.group(2)
        fuente, _ = indice.get(etiqueta, ("", ""))
        url = pagina(fuente) if fuente else None
        return f"[{texto}]({url}#{etiqueta})" if url else texto

    nb = json.loads(ruta.read_text(encoding="utf-8"))
    for c in nb["cells"]:
        if c["cell_type"] not in ("markdown", "raw"):
            continue
        t = "".join(c["source"])
        t = re.sub(r'<span class="nuevo">(.*?)</span>', sin_marca, t, flags=re.S)
        t = re.sub(r'<a href="#([\w-]+)"[^>]*class="quarto-xref">(.*?)</a>', interno, t,
                   flags=re.S)
        t = re.sub(r"\?@([\w-]+)", referencia, t)
        t, caligraficas = sin_caligrafica(t)
        cuenta["letras caligráficas"] += caligraficas
        lineas = t.split("\n")
        c["source"] = [l + "\n" for l in lineas[:-1]] + [lineas[-1]]
    ruta.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return {k: v for k, v in cuenta.items() if v}


def macros_sin_expandir(ruta: Path) -> list[str]:
    """Macros del contrato que Pandoc no llegó a expandir. Deberían ser cero: si aparece
    alguno, en Colab se vería la secuencia en crudo."""
    nb = json.loads(ruta.read_text(encoding="utf-8"))
    md = "\n".join("".join(c["source"]) for c in nb["cells"][1:]
                   if c["cell_type"] == "markdown")
    # Solo letras: `\w+` se comeria el subrayado y `\argmin_w` escaparia como
    # `argmin_w`, que no esta en la lista.
    return sorted({m for m in re.findall(r"\\([A-Za-z]+)", md)
                   if m in nombres_definidos()})


sucios = {}
indice = indice_etiquetas()
for qmd in capitulos:
    ruta = SALIDA / f"{qmd.stem}.ipynb"
    if not ruta.exists():
        continue
    limpiado = limpia_para_colab(ruta, indice)
    if limpiado:
        print(f"   {ruta.name}: " + ", ".join(f"{v} {k}" for k, v in limpiado.items()))
    notacion_al_principio(ruta)
    restos = macros_sin_expandir(ruta)
    if restos:
        sucios[ruta.name] = restos

if sucios:
    print("MACROS SIN EXPANDIR (se verían en crudo en Colab):", file=sys.stderr)
    for nombre, restos in sucios.items():
        print(f"  {nombre}: {', '.join(restos)}", file=sys.stderr)
    sys.exit(1)

if fallos:
    print("FALLARON: " + ", ".join(fallos), file=sys.stderr)
    sys.exit(1)

# El directorio contiene solo artefactos generados: elimina cuadernos cuyos capítulos ya
# no formen parte del curso.
esperados = {f"{qmd.stem}.ipynb" for qmd in capitulos}
for notebook in SALIDA.glob("*.ipynb"):
    if notebook.name not in esperados:
        notebook.unlink()
