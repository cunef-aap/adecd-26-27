# Hojas de problemas, ejercicios de examen y cuadernos

## Estado actual

`problemas/` **está publicado**: el índice, las hojas 1 y 2 con sus solucionarios, y los
nueve esqueletos de las hojas 3 a 11. `evaluacion/` sigue fuera del libro, con el banco y los
ejercicios tipo examen escritos contra la estructura antigua de dieciséis capítulos y con
referencias cruzadas rotas. Al reescribir ese material hay que renumerarlo y comprobar que
todo `@...` resuelve.

**Todo lo que se enlace tiene que estar listado en `_quarto.yml`.** Un fichero enlazado y no
listado no se renderiza: Quarto lo copia como `.qmd` al directorio de salida y el enlace
descarga el fuente. Por eso los esqueletos se listan aunque estén vacíos.

## Hoja de problemas

**Una hoja por capítulo**, no una por semana. Un capítulo suele ocupar dos semanas y su hoja
se reparte entre las dos sesiones de problemas. La numeración es directa: `hoja-NN`
corresponde al capítulo NN. Cada hoja tiene **dos ficheros**: los enunciados y la versión
resuelta.

    problemas/hoja-02.qmd              enunciados del capítulo 2
    problemas/hoja-02-soluciones.qmd   los mismos enunciados, cada uno con su ::: {.sol}

Los dos se publican, listados en `_quarto.yml` bajo la parte "Hojas de problemas". Para no
publicar las soluciones basta con comentar sus líneas ahí y quitar el enlace del pie de cada
hoja.

El enunciado se duplica a propósito. Con una decena de ejercicios por hoja es más robusto que
un include compartido, que obligaría a separar cada solución de su enunciado. La solución
resuelta se genera desde la hoja con el ayudante de la skill, de modo que las dos versiones
no se desincronizan mientras se edite solo la de enunciados.

### Los ejercicios vienen de dos sitios

- Los que ya están **planteados en el capítulo**, en el punto del texto que los motiva. Se
  recogen en la hoja tal cual, con el identificador de la hoja.
- Los que existen **solo en la hoja**: conceptuales, cálculo a mano, código con errores y
  completar código.

Los del capítulo se quedan también en el capítulo: el hilo los necesita ahí.

### Bloques

| Sección | Bloque de examen | Contenido |
|---|---|---|
| `## 1. Conceptual` | A | respuesta breve, tres o cuatro frases por apartado |
| `## 2. Demostración` | B | resultados del índice de resultados |
| `## 3. Cálculo a mano` | C | números redondos, sin calculadora |
| `## 4. Encuentra los errores` | D | fragmento con tres errores conceptuales |
| `## 5. Completar código` | laboratorio | huecos numerados `# (1)`, `# (2)`, ... |
| `## 6. Ampliación` | fuera | opcional |

Un bloque puede llevar **más de un ejercicio**. Los cuatro primeros son los que entrenan el
examen.

### Enunciado y solución

    ::: {#exr-h3-conceptual}
    a. **Explica** por qué ...
    b. **Razona** qué cambia si ...
    :::

    ::: {.sol}
    a. ...
    :::

- Identificadores `#exr-hN-slug`, con **N el número de hoja, que es el del capítulo**.
- Verbos del banco en negrita: **Razona**, **Explica**, **Analiza**, **Define**,
  **Demuestra**, **Calcula**, **Compara**, **Identifica**, **Corrige**.
- Persona: tú.
- La solución cita los resultados del capítulo con `@`. Una solución que no cita ninguno
  indica que el ejercicio no está anclado al material.
- Los números de los cálculos a mano se comprueban ejecutándolos antes de escribir la
  solución. Nunca se publican sin verificar.

### Bloque D

Fragmento en ` ```python ` **sin llaves**, de modo que no se ejecuta. Exactamente **tres**
errores conceptuales, no de sintaxis. Puede llamar a funciones inexistentes
(`cargar_datos()`). La solución los numera con el título en negrita y la consecuencia; los
defectos menores van aparte, en cursiva y entre paréntesis.

### Bloque de completar código

Huecos marcados con `...` y un comentario numerado al final de la línea. La solución da el
bloque completo y añade al menos un apartado que pida razonar sobre el diseño, no solo
rellenar.

## Ejercicio tipo examen

`evaluacion/ejercicios-tipo-examen.qmd` agrupa los ejercicios por bloque
(`## Bloque A · Conceptuales`, y así hasta D). Formato de cada uno:

    ### Título descriptivo

    *Capítulo K · N minutos · @thm-..., @def-..., @cor-...*

    Enunciado en prosa.

    ::: {.sol}
    Solución completa, citando los resultados con @.
    :::

    ::: {.callout-note appearance="simple" collapse="true"}
    ## Rúbrica

    Aprueba quien ...

    Sube a la nota máxima quien ...

    No puntúa ...
    :::

La línea de metadatos en cursiva es obligatoria: capítulo, minutos y la lista de resultados
que el ejercicio evalúa. La rúbrica siempre en tres tramos, con esos tres verbos.

`evaluacion/banco.md` lleva una línea por pregunta con etiqueta `` `[capN][A|B|C|D]` ``.
Las etiquetas actuales usan la numeración antigua y hay que rehacerlas.

## Índice de resultados

El bloque B sale de los resultados que los capítulos demuestran, y de ningún
otro sitio. Al escribir un capítulo hay que **añadir sus resultados a ese índice**, con las
columnas `Resultado | Se demuestra | Depende de`.

Dos avisos comprobados sobre el estado actual:

1. El fichero no está listado en `_quarto.yml`, aunque lo enlazan `problemas/index.qmd` y
   `evaluacion/parcial-01.qmd`.
2. Promete en prosa ocho resultados que no existen como entornos en los capítulos. Seis
   están ya citados desde las hojas o desde los ejercicios de examen, y por tanto son
   referencias rotas hoy: `def-senal-ruido`, `def-errores`, `def-sobreajuste`,
   `thm-interpolacion`, `lem-media-optima` y `prp-laplace-mae`. Los otros dos,
   `cor-senal-media` y `cor-ruido-objetivo`, son nombres propuestos a partir de la prosa del
   índice: no aparecen en ningún fichero del repositorio y nadie los cita todavía. Al revisar
   los capítulos 1 y 2 hay que escribirlos o retirarlos del índice.
3. Sus números de capítulo son los de la **estructura antigua de dieciséis capítulos**. Antes
   de fiarse de una fila hay que traducirla a la estructura de nueve.

Las filas del índice se nombran hoy en prosa ("Teo. interpolación exacta"), no con la
etiqueta del entorno, así que no hay forma mecánica de casarlas. Al añadir filas nuevas,
poner la etiqueta entre paréntesis.

## Presupuesto de huecos por sesión de laboratorio

La S3 dura 55 minutos y en ella se completa el cuaderno en directo. Medido sobre los
capítulos escritos, un hueco consume entre seis y ocho minutos contando el enunciado, la
escritura y la corrección, de modo que **el presupuesto es de 6 a 8 huecos por sesión S3**.

Cuántas sesiones le tocan a cada capítulo lo fija el reparto del curso: los capítulos 1 a 6
duran dos semanas y tienen dos S3 cada uno; los capítulos 7, 8 y 9 duran una semana y tienen
una. En total, quince sesiones.

| Capítulo | Sesiones S3 | Huecos que le corresponden |
|---|---:|---:|
| 1 a 6 | 2 | 12 a 16 |
| 7 a 9 | 1 | 6 a 8 |

Dos avisos del calendario: la S3 de la semana 9 es el taller de agentes, de modo que el
capítulo 5 solo tiene tres S3 útiles en sus dos semanas, y la S3 de la semana 14 es el
segundo taller, de modo que el capítulo 8 se queda sin laboratorio propio.

Un capítulo por debajo de cuatro huecos por sesión deja la S3 medio vacía; por encima de
nueve, no se acaba. El recuento se comprueba con

    grep -c 'TODO: completar en clase' docs/live-notebooks/NN-nombre.ipynb

**Deuda medida en agosto de 2026**: el capítulo 1 tiene 4 huecos para dos sesiones, es decir
2 por sesión, y le faltan unos ocho. El 2 va a 5.5, el 3 a 6.5 y el 4 a 5.5, que están en
rango. Los del 4 se reparten así: la API (`predict`, `mse`, `fit`), la partición, la mejor
constante, las cuatro métricas, el error típico de la estimación, el experimento de selección,
las tres piezas de la validación cruzada y el reajuste final con la comparación.

## Cuadernos

**No se escriben a mano.** Salen del mismo `.qmd` del capítulo con `make notebooks`, que
llama a `scripts/crear-ipynb.py`. Consecuencias al escribir el capítulo:

- Lo que hay entre un par de `#---` se sustituye por `# TODO: completar en clase`. Ese es el
  hueco del laboratorio.
- El preámbulo `.content-hidden` **no llega**, así que el primer bloque visible lleva los
  imports reales y la semilla.
- **El enlace a Colab se activa por documento**, desde agosto de 2026. Dos pasos: declarar
  `cuaderno: <nombre>.ipynb` en la cabecera YAML del `.qmd` y poner
  `{{< include ../assets/includes/_colab-link.qmd >}}` donde deba salir el enlace. El include
  construye la URL con `{{< meta cuaderno >}}` sobre el repositorio público, y se oculta en
  formato `ipynb` para que el cuaderno no se enlace a sí mismo. Lo tienen el capítulo 1 y
  `curso/colab.qmd`; los demás capítulos lo ganan cuando se publiquen.
  **No usar `QUARTO_DOCUMENT_FILE`**: Quarto no lo define al renderizar, comprobado.
- Los divs de referencia cruzada se desanidan con `restore-cells.lua`, de modo que el código
  dentro de `::: {#fig-...}` sí sale como celda ejecutable.
- El cuaderno se genera con `--no-execute`, así que un error de ejecución no se detecta ahí.
  Se detecta en `make sitio`.

`curso/colab.qmd` es la excepción a «los cuadernos salen de los capítulos»: es un anexo, no
un capítulo, y genera cuaderno porque es donde se aprende a usar la herramienta. Está
declarado a mano en `_quarto-notebooks.yml` y en `scripts/crear-ipynb.py`, que por defecto
solo recorre `capitulos/*.qmd`. No tiene huecos `#---`: se ejecuta entero.

Después de tocar un capítulo, `make notebooks` y comprobar que el `.ipynb` tiene los
`# TODO: completar en clase` donde tocan y que se ejecuta de arriba abajo en un entorno
limpio.
