# Mecánica de Quarto

Proyecto `book`, salida en `docs/`, kernel `aap`, `freeze: auto`. De cada `.qmd` de
`capitulos/` salen **dos artefactos** con perfiles distintos, y esa dualidad condiciona
cómo se escribe el fichero.

| Perfil | Comando | Salida | Filtro |
|---|---|---|---|
| `publica` | `make sitio` | `docs/` con el código completo | `strip-delims.lua` borra las líneas `#---` |
| `notebooks` | `make notebooks` | `docs/live-notebooks/*.ipynb` | `strip-code.lua` sustituye cada par `#--- ... #---` por `# TODO: completar en clase` |

Todos los fragmentos de esta referencia van indentados cuatro espacios, para poder anidar
bloques de código dentro. Al copiarlos hay que quitar esa indentación.

## Cabecera obligatoria

Las quince primeras líneas de todo capítulo, literales. Solo cambian el título y el
subtítulo.

    ---
    title: 'Título del capítulo'
    subtitle: 'Subtítulo en una línea'
    ---

    ::: {.content-hidden}
    ## Preámbulo: macros de LaTeX y estilo de figuras
    $$
    {{< include ../assets/includes/_macros.tex >}}
    $$

    ```{python}
    import style
    ```
    :::

El bloque `.content-hidden` **no llega al cuaderno**. Por eso el primer bloque `{python}`
visible del capítulo tiene que traer los imports reales (`import torch`,
`from matplotlib import pyplot as plt`, la semilla y los datos). Sin eso el cuaderno no se
ejecuta.

El título va en `title:` y no como `#` en el cuerpo. Los encabezados del cuerpo empiezan en
`##`.

## Entornos numerados

Sintaxis única: un div con identificador y el título como `##` en su primera línea.

    ::: {#def-residuo}
    ## Residuo y riesgo cuadrático empírico

    El **residuo** de la observación $i$ es
    ...
    :::

Prefijos disponibles, con el rótulo que Quarto pone en español (`language:` de
`_quarto.yml`): `def-` Definición · `thm-` Teorema · `lem-` Lema · `cor-` Corolario ·
`prp-` Proposición · `exm-` Ejemplo · `exr-` Ejercicio · `rem-` Observación ·
`fig-` Figura · `eq-` Ecuación.

Demostración inmediatamente después del resultado:

    ::: {.proof}
    ...
    :::

`.proof` no lleva identificador y no se numera. El símbolo de fin lo pone el CSS.

Ecuaciones: se etiquetan con `$$ ... $$ {#eq-slug}` **solo si se citan después**. Una
ecuación etiquetada y nunca citada añade un número que no sirve.

Referencias cruzadas: `@def-residuo`, `@eq-riesgo-empirico`, `@fig-trampa`, `@sec-autodiff`.
Se escriben sin corchetes y Quarto genera el rótulo.

**Una referencia cruzada no puede abrir una línea.** Pandoc interpreta `@etiqueta.` a
principio de línea como marcador de lista de ejemplos, y dentro de un elemento de lista parte
el elemento en dos. El síntoma es un salto de línea inexplicable en el HTML. La solución es
reordenar la frase o mover una palabra de la línea anterior, para que la referencia quede en
medio. `check-capitulo.py` lo detecta.

**Los `:::` tienen que estar emparejados.** Un cierre de más o de menos no produce ningún
error: Quarto anida lo que viene después y el capítulo sale mal desde ese punto hasta el
final, normalmente sin que se note hasta que se mira el HTML. Es el fallo más fácil de
introducir al aceptar marcas de revisión a mano. `check-capitulo.py` comprueba el balance.

## Figuras

Dos formas, según el sitio.

**Figura en el cuerpo**: div con identificador, el bloque de código dentro y el pie como
último párrafo antes del cierre.

    ::: {#fig-trayectoria-descenso}

    ```{python}
    #| code-fold: true
    ...código que produce la figura...
    ```

    Pie de figura, en una o dos frases, que dice qué se ve.
    :::

**Figura de margen**: sin div, con opciones de celda.

    ```{python}
    #| column: margin
    #| echo: false
    #| fig-cap: "Texto del pie."
    #| label: fig-area-normal
    ...
    ```

`reference-location: margin` y `fig-cap-location: margin` están activos en `_quarto.yml`,
de modo que los pies del cuerpo también se colocan en el margen. Ancho del cuerpo 760 px,
del margen 340 px.

## Celdas de código

- `#| code-fold: true` para el código que el lector no necesita leer para seguir el hilo: el
  que produce una figura y el que regenera los datos del capítulo. Lo puede desplegar, pero
  no interrumpe la lectura.
- Código sin `code-fold` cuando la celda **es** el contenido: una definición de función que
  traduce una fórmula, un experimento, una comprobación.
- **Anotaciones de línea**: se marca la línea con `# <1>` y debajo del bloque va una lista
  numerada. Modelo, `capitulos/02-aprender-minimizando.qmd:783-803`.

      ```{python}
      #---
      def ajustar_descenso_manual(x, y, w_inicial, lr, n_iter):
          ...
          gradiente = grad_mse(w, x, y)  # <1>
          w = w - lr * gradiente                 # <2>
      #---
      ```

      1. Evaluamos el gradiente en los parámetros actuales.
      2. Aplicamos exactamente la actualización de @eq-descenso.

  Las anotaciones explican **por qué**, no repiten lo que la línea dice.

## Centinelas `#---`

Marcan el trozo que se completa en directo en el laboratorio. En el sitio publicado
desaparecen las líneas; en el cuaderno, todo lo que hay entre ellas se sustituye por
`# TODO: completar en clase`.

Reglas:

1. La línea debe ser exactamente `#---`, sin nada más, **y la cadena `#---` no puede
   aparecer en ninguna otra posición de ningún bloque de código**. `strip-delims.lua`, el del
   sitio, está anclado, así que un comentario decorativo del tipo `# --- cálculo del R2 ---`
   sobrevive. `strip-code.lua`, el de los cuadernos, no lo está: sustituye desde cualquier
   `#---` hasta el siguiente, esté donde esté, y se come código del `.ipynb` sin avisar.
   `check-capitulo.py` da error si encuentra `#---` a mitad de línea.
2. **Un par por bloque**, y los dos centinelas en el mismo bloque. `check-centinelas.py`
   solo comprueba la paridad por fichero, así que dos bloques con un centinela cada uno
   pasan el control y no producen ningún hueco. `check-capitulo.py` cierra ese agujero.
3. Nunca en bloques con `#| code-fold: true` ni con `#| echo: false`.
4. El código que precede al par dentro del mismo bloque **sobrevive** en el cuaderno. Se usa
   para dejar visible una definición y abrir el hueco solo en la parte que el estudiante
   escribe. Modelo: `capitulos/01-senal-ruido.qmd:231-241`, donde `densidad_normal` queda
   escrita y el hueco se abre en la llamada.
5. Cuatro pares por capítulo en el 1, ocho en el 2. Es el orden de magnitud.

## Divs propios

Definidos en `assets/styles.css`, sin depender de ninguna extensión.

| Div | Rótulo automático | Uso |
|---|---|---|
| `::: {.trampa}` | Error frecuente | filete naranja, el único bloque con color. Para el error que se repite en los exámenes |
| `::: {.cajanegra}` | Fuera de alcance | resultado que se enuncia y no se demuestra, con el motivo en una frase |
| `::: {.sol}` | Solución | en hojas y ejercicios de examen, nunca en capítulos |
| `::: {.sinusar}` | Sin usar todavía | **temporal**, filete violeta discontinuo. Material de los apéndices que ningún capítulo cita aún |

`::: {.sinusar}` es una marca de trabajo, como `.nuevo`, y no forma parte de la identidad del
libro. Señala en `curso/algebra.qmd` y `curso/probabilidad.qmd` lo que está escrito y todavía
no se usa, con el capítulo que se espera que lo use, para poder quitarlo si ese capítulo acaba
sin necesitarlo. A diferencia de `.nuevo`, **no la gestiona `aceptar-marcas.py`** y no la
detecta `make marcas`: se quita a mano cuando el capítulo que la necesita la cita, o cuando se
decide borrar el material. Para saber qué sigue sin citarse:

    python - <<'FIN'
    import io, re, glob
    apend = {}
    for f in ("curso/algebra.qmd", "curso/probabilidad.qmd"):
        for m in re.finditer(r"\{#([a-z]+-[a-z0-9-]+)\}", io.open(f, encoding="utf-8").read()):
            apend[m.group(1)] = f
    fuentes = glob.glob("capitulos/*.qmd") + glob.glob("problemas/*.qmd")
    texto = {f: io.open(f, encoding="utf-8").read() for f in fuentes}
    for lab, orig in sorted(apend.items()):
        if not [f for f in fuentes if re.search(r"@" + lab + r"\b", texto[f])]:
            print("sin citar:", lab, "en", orig)
    FIN

Regla del CSS: **el título del bloque va en negrita en el primer párrafo, nunca como `##`**,
para que no entre en la tabla de contenidos.

Excepción declarada frente a `write-roinaveiro-es`, que prescribe la marca "OJO" en
mayúsculas y prohíbe las cajas de color: aquí el rótulo lo pone el CSS, sin icono ni relleno,
solo un filete. En este repositorio `::: {.trampa}` sustituye a esa marca.

Callouts nativos, con apariencia aplanada (`callout-icon: false`,
`callout-appearance: minimal`):

    ::: {.callout-warning title="El modelo generador es una hipótesis"}
    ...
    :::

`callout-warning` para el aviso que evita un malentendido; `callout-note` para la precisión
que no cambia el resultado.

## Bibliografía

`referencias.bib` en la raíz, cinco entradas: `hastie2009elements`, `bishop2023deep`,
`deisenroth2020mathematics`, `mitchell1997machine`, `bommasani2021opportunities`. Se cita
`[@clave]`. Los capítulos 1 y 2 no citan nada; a partir del 4 hay temas (validación cruzada,
PCA, árboles) donde conviene citar ESL. Si se añade una entrada, se usa el estilo de clave
existente (`autor+año+palabra`), no el de Chodrow.

## Datos

Siempre desde `datos/` por ruta relativa, y con el `cwd` en `capitulos/`:

    ruta = "../datos/prostate.data"

Ninguna URL en tiempo de render. `scripts/descargar-datos.py` es lo que baja los datos, una
vez, y regenera `datos/PROCEDENCIA.md`.

## Detalles del fuente

- **92 columnas** de anchura de línea. No hay comprobación automática:
  `.vscode/settings.json` solo pone la regla visual del editor. El capítulo 2 la cumple con
  una sola excepción; el capítulo 1 la incumple en catorce líneas, una de ellas de 573
  caracteres. Eso es deuda, no modelo. Las hojas y los ejercicios de examen no la respetan.
- El fichero se guarda en UTF-8 y con salto de línea final.
- Los identificadores de entorno son `tipo-slug-en-kebab`, en español, sin tildes.

## Comandos

    make check      # check-centinelas.py y check-estilo.py. Cualquiera aborta el build
    make sitio      # render con perfil publica a docs/
    make notebooks  # genera docs/live-notebooks/*.ipynb
    make preview    # servidor local
    make datos      # descarga y prepara datos/

**`freeze: auto` puede servir prosa vieja.** El directorio `_freeze/` guarda el documento ya
ejecutado, que incluye el texto, no solo las salidas del código. Se ha observado que un
capítulo con cambios de prosa se renderiza a partir de la versión cacheada y el HTML sale sin
los cambios, sin ningún aviso. El síntoma es que una referencia cruzada nueva no resuelve, o
que un párrafo recién escrito no aparece. La comprobación es un `grep` de una frase nueva
sobre el HTML; el arreglo, borrar el `_freeze` del capítulo y volver a renderizar:

    rm -rf _freeze/capitulos/NN-nombre && make sitio

Conviene hacerlo siempre antes de dar por buena una verificación sobre el HTML.

`check-estilo.py` recorre todos los `.qmd` y `.md` del repositorio fuera de `_referencia`,
`docs`, `.quarto` y `_freeze`. Eso incluye `.claude/skills/**/*.md`, de modo que los ficheros
de esta skill cumplen las mismas reglas de voz que los apuntes.

Después de tocar un capítulo, lo mínimo es `make check` más el verificador de la skill. El
render completo antes de dar el capítulo por cerrado.

Aviso: `make publicar` hace `git push origin main` y la rama local es `master`. No se usa
sin comprobarlo.
