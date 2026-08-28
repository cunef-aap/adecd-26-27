#!/usr/bin/env python3
"""Comprueba las convenciones estructurales de un capitulo de aap-cunef.

Complementa a `scripts/check-centinelas.py` y `scripts/check-estilo.py`, que ya cubren
la paridad global de centinelas y las reglas mecanicas de prosa. Aqui se comprueba lo
que aquellos no ven:

  1. la cabecera obligatoria de 17 lineas;
  2. que el primer bloque {python} visible traiga los imports (sin eso el cuaderno no
     se ejecuta, porque el preambulo .content-hidden no llega al ipynb);
  3. que los centinelas #--- esten emparejados DENTRO de cada bloque, no solo por
     fichero, que es lo unico que garantiza check-centinelas.py;
  4. que toda macro LaTeX usada este definida en assets/includes/_macros.tex;
  5. que toda referencia cruzada @tipo-slug resuelva contra las etiquetas del proyecto;
  6. que cada entorno numerado abra con un titulo `## `;
  7. que cada resultado enunciado lleve demostracion o marca de fuera de alcance.

Los puntos 1 a 5 son errores. Los puntos 6 y 7 son avisos.

Uso:  python .claude/skills/aap-capitulo/scripts/check-capitulo.py [ficheros...]
      Sin argumentos, comprueba capitulos/*.qmd.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# --- Localizacion del proyecto ---------------------------------------------


def raiz_proyecto(desde: Path) -> Path:
    for p in [desde, *desde.parents]:
        if (p / "_quarto.yml").exists():
            return p
    raise SystemExit("no encuentro _quarto.yml: ejecuta desde dentro del repositorio")


RAIZ = raiz_proyecto(Path(__file__).resolve())
MACROS = RAIZ / "assets" / "includes" / "_macros.tex"

CABECERA = """::: {.content-hidden}
## Preámbulo: macros de LaTeX y estilo de figuras
$$
{{< include ../assets/includes/_macros.tex >}}
$$

```{python}
import style
```
:::"""

TIPOS_CROSSREF = ("def", "thm", "lem", "cor", "prp", "exm", "exr", "fig", "eq", "sec",
                  "tbl", "lst", "rem")
TIPOS_RESULTADO = ("thm", "lem", "cor", "prp")
TIPOS_CON_TITULO = ("def", "thm", "lem", "cor", "prp", "exm", "rem")

# Ordenes de LaTeX y de amsmath que no salen de _macros.tex.
BUILTIN = set("""
frac dfrac tfrac sum prod int iint oint lim limits nolimits sqrt log ln exp sin cos tan
sinh cosh tanh min max sup inf det dim deg gcd hom ker Pr arg bmod pmod
left right big Big bigg Bigg bigl bigr Bigl Bigr biggl biggr Biggl Biggr middle
begin end quad qquad ; , ! : space hspace vspace phantom hfill
cdot cdots ldots dots vdots ddots dotsc dotsb
hat bar tilde vec dot ddot widehat widetilde overline underline overbrace underbrace
overset underset stackrel substack
mathbb mathcal mathrm mathbf mathsf mathtt mathit boldsymbol bm symbf
text textrm textbf textit textsf texttt mbox operatorname
alpha beta gamma delta epsilon varepsilon zeta eta theta vartheta iota kappa lambda mu
nu xi pi varpi rho varrho sigma varsigma tau upsilon phi varphi chi psi omega
Gamma Delta Theta Lambda Xi Pi Sigma Upsilon Phi Psi Omega
partial nabla infty emptyset varnothing forall exists nexists neg lnot
in notin ni subset supset subseteq supseteq setminus cup cap bigcup bigcap
leq geq neq ne le ge ll gg approx equiv sim simeq cong propto asymp
to rightarrow leftarrow Rightarrow Leftarrow leftrightarrow Leftrightarrow
longrightarrow longleftarrow Longrightarrow Longleftarrow longleftrightarrow
Longleftrightarrow mapsto implies impliedby iff
pm mp times div ast star circ bullet oplus otimes wedge vee
mid nmid parallel colon vert lvert rvert lVert rVert
prime ell hbar aleph Re Im angle perp parallel top bot vert Vert lvert rvert lVert rVert
langle rangle lfloor rfloor lceil rceil
colon coloneqq eqqcolon
displaystyle textstyle scriptstyle scriptscriptstyle
label ref eqref tag notag nonumber
hline midrule toprule bottomrule multicolumn multirow
color textcolor mathopen mathclose mathrel mathbin mathop
newcommand renewcommand DeclareMathOperator providecommand
binom choose pmatrix bmatrix vmatrix Bmatrix matrix cases aligned align alignedat
array split gathered
sfrac mathstrut strut smash raisebox
""".split())


def macros_definidas() -> set[str]:
    if not MACROS.exists():
        raise SystemExit(f"no encuentro {MACROS}")
    texto = MACROS.read_text(encoding="utf-8")
    nombres = set()
    for patron in (r"\\newcommand\{\\([A-Za-z]+)\}",
                   r"\\renewcommand\{\\([A-Za-z]+)\}",
                   r"\\DeclareMathOperator\*?\{\\([A-Za-z]+)\}"):
        nombres |= set(re.findall(patron, texto))
    return nombres


# --- Utilidades de troceado -------------------------------------------------


def bloques_codigo(texto: str):
    """Devuelve (linea_inicial, cabecera, cuerpo) de cada bloque ```...```."""
    fuera = []
    lineas = texto.splitlines()
    i = 0
    while i < len(lineas):
        m = re.match(r"^\s*```+\s*(\{[^}]*\}|[A-Za-z]*)\s*$", lineas[i])
        if m:
            inicio = i
            cabecera = m.group(1)
            i += 1
            cuerpo = []
            while i < len(lineas) and not re.match(r"^\s*```+\s*$", lineas[i]):
                cuerpo.append(lineas[i])
                i += 1
            fuera.append((inicio + 1, cabecera, cuerpo))
        i += 1
    return fuera


def sin_codigo(texto: str) -> str:
    """Sustituye cada bloque de codigo por lineas vacias, conservando la numeracion."""
    salida = []
    dentro = False
    for linea in texto.splitlines():
        if re.match(r"^\s*```", linea):
            dentro = not dentro if not re.match(r"^\s*```+\s*$", linea) or dentro else True
            salida.append("")
            continue
        salida.append("" if dentro else linea)
    return "\n".join(salida)


CIERRE_MATH = re.compile(r"^\$\$(\s*\{#eq-[A-Za-z0-9_-]+\})?$")


def regiones_matematicas(texto: str) -> list[tuple[int, str]]:
    """(linea, contenido) de cada region $$...$$ y de cada $...$ inline."""
    regiones = []
    lineas = texto.splitlines()
    i = 0
    while i < len(lineas):
        if CIERRE_MATH.match(lineas[i].strip()):
            inicio = i
            i += 1
            cuerpo = []
            while i < len(lineas) and not CIERRE_MATH.match(lineas[i].strip()):
                cuerpo.append(lineas[i])
                i += 1
            regiones.append((inicio + 1, "\n".join(cuerpo)))
        else:
            for m in re.finditer(r"(?<!\$)\$(?!\$)([^$\n]+)\$(?!\$)", lineas[i]):
                regiones.append((i + 1, m.group(1)))
        i += 1
    return regiones


def etiquetas_del_proyecto() -> set[str]:
    etiquetas = set()
    for p in RAIZ.rglob("*.qmd"):
        if {"docs", "_freeze", ".quarto", "_referencia", "ml-notes-update-main"} & set(p.parts):
            continue
        t = p.read_text(encoding="utf-8")
        etiquetas |= set(re.findall(r"\{#([a-z]+-[A-Za-z0-9_-]+)\}", t))
        etiquetas |= set(re.findall(r"^\s*#\|\s*label:\s*([a-z]+-[A-Za-z0-9_-]+)\s*$",
                                    t, re.M))
    return etiquetas


# --- Comprobaciones ---------------------------------------------------------


def revisa(ruta: Path, definidas: set[str], etiquetas: set[str]) -> tuple[int, int]:
    texto = ruta.read_text(encoding="utf-8")
    lineas = texto.splitlines()
    rel = ruta.relative_to(RAIZ) if ruta.is_relative_to(RAIZ) else ruta
    errores = avisos = 0

    def error(linea, msg):
        nonlocal errores
        print(f"{rel}:{linea}: {msg}")
        errores += 1

    def aviso(linea, msg):
        nonlocal avisos
        print(f"{rel}:{linea}: aviso: {msg}")
        avisos += 1

    es_capitulo = "capitulos" in ruta.parts

    # 1. Cabecera obligatoria (solo capitulos).
    if es_capitulo:
        if not lineas or lineas[0].strip() != "---":
            error(1, "falta el front matter YAML")
        else:
            fin = next((i for i, l in enumerate(lineas[1:], 1) if l.strip() == "---"), None)
            if fin is None:
                error(1, "front matter YAML sin cerrar")
            else:
                if not any(l.startswith("title:") for l in lineas[1:fin]):
                    error(1, "el front matter no tiene title:")
                if not any(l.startswith("subtitle:") for l in lineas[1:fin]):
                    aviso(1, "el front matter no tiene subtitle:")
                resto = "\n".join(lineas[fin + 1:]).lstrip("\n")
                if not resto.startswith(CABECERA):
                    error(fin + 2,
                          "la cabecera obligatoria no coincide: hace falta el bloque "
                          ".content-hidden con las macros e import style")

    bloques = bloques_codigo(texto)

    # 2. Primer bloque {python} visible con imports (solo capitulos).
    if es_capitulo:
        visibles = [b for b in bloques
                    if b[1].startswith("{python") and "import style" not in "\n".join(b[2])]
        if not visibles:
            aviso(1, "no hay ningun bloque {python} visible")
        elif not any(l.strip().startswith(("import ", "from ")) for l in visibles[0][2]):
            error(visibles[0][0],
                  "el primer bloque {python} visible no importa nada: el cuaderno no se "
                  "ejecutara, porque el preambulo .content-hidden no llega al ipynb")

    # 3. Centinelas emparejados dentro de cada bloque.
    for inicio, cabecera, cuerpo in bloques:
        marcas = [j for j, l in enumerate(cuerpo) if re.match(r"^\s*#---\s*$", l)]
        if not marcas:
            continue
        if len(marcas) % 2:
            error(inicio + marcas[-1] + 1,
                  f"{len(marcas)} centinelas #--- en este bloque: tienen que ir por pares "
                  "dentro del mismo bloque")
        if "code-fold: true" in "\n".join(cuerpo) or re.search(r"#\|\s*echo:\s*false", "\n".join(cuerpo)):
            aviso(inicio, "centinelas #--- en un bloque con code-fold o echo: false")

    for inicio, cabecera, cuerpo in bloques:
        for j, l in enumerate(cuerpo):
            if "#---" in l and not re.match(r"^\s*#---\s*$", l):
                error(inicio + j + 1,
                      "la cadena #--- aparece a mitad de linea: strip-code.lua no esta "
                      "anclado y se comera codigo del cuaderno sin avisar")

    # 3 bis. Divs emparejados. Un `:::` de mas o de menos no da error de render:
    # Quarto anida lo que viene despues y el capitulo sale mal desde ese punto.
    profundidad, en_codigo = 0, False
    abiertos: list[tuple[int, str]] = []
    for i, linea in enumerate(lineas, 1):
        if re.match(r"^\s*```", linea):
            en_codigo = not en_codigo
            continue
        if en_codigo:
            continue
        if re.match(r"^:::+\s*\{", linea):
            profundidad += 1
            abiertos.append((i, linea.strip()[:46]))
        elif re.match(r"^:::+\s*$", linea):
            profundidad -= 1
            if profundidad < 0:
                error(i, "cierre ::: sobrante: no hay ningun div abierto")
                profundidad = 0
            elif abiertos:
                abiertos.pop()
    for i, texto_div in abiertos:
        error(i, f"div sin cerrar: {texto_div}")

    # 3 ter. Una referencia cruzada al principio de linea dentro de una lista la interpreta
    # Pandoc como marcador de lista de ejemplos, y parte el elemento en dos.
    en_comentario = False
    for i, linea in enumerate(lineas, 1):
        if "<!--" in linea:
            en_comentario = "-->" not in linea.split("<!--", 1)[1]
            continue
        if en_comentario:
            en_comentario = "-->" not in linea
            continue
        if re.match(r"^\s*@[a-z]+-[A-Za-z0-9_-]+", linea):
            error(i, "referencia cruzada al principio de linea: Pandoc puede tomarla por "
                     "un marcador de lista. Reordena la frase para que no abra la linea")

    # 3 quater. El abridor de un div numerado no admite texto detras de la llave: Quarto
    # lo trata como cuerpo, el entorno se queda sin titulo y la comprobacion 6 no lo ve.
    for i, linea in enumerate(lineas, 1):
        m = re.match(r"^:::+\s*\{#([a-z]+)-([A-Za-z0-9_-]+)\}\s*(\S.*)$", linea)
        if m and m.group(1) in TIPOS_CON_TITULO:
            error(i, f"texto pegado al abridor de #{m.group(1)}-{m.group(2)}: "
                     f"{m.group(3)!r}. El titulo va en su propia linea, con '## '")

    # 3 quater bis. Un abridor de div necesita una linea en blanco delante, o Pandoc lo
    # absorbe como continuacion del parrafo anterior: la valla y el titulo salen literales y
    # la etiqueta no se registra, asi que toda referencia a ella queda rota en TODO el libro.
    en_codigo_div = False
    for i, linea in enumerate(lineas, 1):
        if linea.startswith("```"):
            en_codigo_div = not en_codigo_div
            continue
        if en_codigo_div or i < 2:
            continue
        previa = lineas[i - 2]
        if (re.match(r"^:{3,}\s*\{#", linea) and previa.strip()
                and not re.match(r"^:{3,}", previa.strip())
                and not previa.startswith("```")):
            error(i, "el abridor de un div necesita una linea en blanco delante: sin ella "
                     "Pandoc lo lee como parte del parrafo anterior y la etiqueta se pierde")

    # 3 quinquies. La etiqueta de un display va en la linea que lo CIERRA. Si se pega a la
    # que lo abre, Quarto no crea la etiqueta, la imprime dentro de la formula y cualquier
    # referencia a ella queda sin resolver. La comprobacion 5 no lo detecta, porque para
    # ella la etiqueta existe.
    en_display = False
    for i, linea in enumerate(lineas, 1):
        marcas = linea.count("$$")
        etiqueta = re.search(r"\{#(eq|tbl)-[A-Za-z0-9_-]+\}", linea)
        abre_aqui = not en_display and marcas == 1
        if etiqueta and abre_aqui:
            error(i, f"etiqueta {etiqueta.group(0)} pegada al $$ que ABRE el display: "
                     "tiene que ir en la linea del $$ que lo cierra")
        if marcas % 2:
            en_display = not en_display

    # 4. Macros indefinidas.
    prosa = sin_codigo(texto)
    vistas: dict[str, int] = {}
    for linea, contenido in regiones_matematicas(prosa):
        for nombre in re.findall(r"\\([A-Za-z]+)", contenido):
            if nombre not in definidas and nombre not in BUILTIN:
                vistas.setdefault(nombre, linea)
    for nombre, linea in sorted(vistas.items(), key=lambda kv: kv[1]):
        error(linea, f"macro no definida en _macros.tex: \\{nombre}")

    # 5. Referencias cruzadas rotas.
    rotas: dict[str, int] = {}
    for i, linea in enumerate(prosa.splitlines(), 1):
        for m in re.finditer(r"(?<![A-Za-z0-9_.])@([a-z]+)-([A-Za-z0-9_-]+)", linea):
            tipo, slug = m.group(1), m.group(2)
            if tipo not in TIPOS_CROSSREF:
                continue
            etiqueta = f"{tipo}-{slug}".rstrip(".,;:)")
            if etiqueta not in etiquetas:
                rotas.setdefault(etiqueta, i)
    for etiqueta, linea in sorted(rotas.items(), key=lambda kv: kv[1]):
        error(linea, f"referencia cruzada rota: @{etiqueta}")

    # 6 y 7. Entornos: titulo y demostracion.
    for i, linea in enumerate(lineas, 1):
        m = re.match(r"^:::\s*\{#([a-z]+)-([A-Za-z0-9_-]+)\}\s*$", linea)
        if not m:
            continue
        tipo = m.group(1)
        siguiente = next((l for l in lineas[i:i + 4] if l.strip()), "")
        if tipo in TIPOS_CON_TITULO and not siguiente.startswith("## "):
            aviso(i, f"el entorno #{tipo}-{m.group(2)} no abre con un titulo '## '")
        if tipo in TIPOS_RESULTADO:
            cierre = next((j for j in range(i, len(lineas))
                           if lineas[j].strip() == ":::"), None)
            if cierre is not None:
                cola = "\n".join(lineas[cierre + 1:cierre + 6])
                delegada = "<!-- demostracion:" in "\n".join(lineas[max(0, i - 3):cierre + 3])
                if not delegada and ".proof" not in cola and ".cajanegra" not in cola:
                    aviso(i, f"el resultado #{tipo}-{m.group(2)} no va seguido de "
                             "::: {.proof} ni de ::: {.cajanegra}. Si la demostracion "
                             "esta en un apendice, marcalo con "
                             "<!-- demostracion: ruta#etiqueta -->")

    return errores, avisos


def main(argv: list[str]) -> int:
    rutas = [Path(a).resolve() for a in argv[1:]]
    if not rutas:
        rutas = sorted((RAIZ / "capitulos").glob("*.qmd"))
    definidas = macros_definidas()
    etiquetas = etiquetas_del_proyecto()
    # Un borrador fuera del repositorio define sus propias etiquetas y no esta indexado.
    for ruta in rutas:
        if ruta.exists() and not ruta.is_relative_to(RAIZ):
            texto = ruta.read_text(encoding="utf-8")
            etiquetas |= set(re.findall(r"\{#([a-z]+-[A-Za-z0-9_-]+)\}", texto))
            etiquetas |= set(re.findall(r"^\s*#\|\s*label:\s*([a-z]+-[A-Za-z0-9_-]+)\s*$",
                                        texto, re.M))

    total_e = total_a = 0
    for ruta in rutas:
        if not ruta.exists():
            print(f"{ruta}: no existe")
            total_e += 1
            continue
        e, a = revisa(ruta, definidas, etiquetas)
        total_e += e
        total_a += a

    print()
    if total_e == 0 and total_a == 0:
        print("capitulo: OK")
        return 0
    print(f"capitulo: {total_e} errores, {total_a} avisos")
    return 1 if total_e else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
