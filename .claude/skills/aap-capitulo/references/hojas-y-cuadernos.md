# Hojas de problemas, ejercicios de examen y cuadernos

## Estado actual

`problemas/` **está publicado**: el índice, las hojas 1 y 2 con sus solucionarios, y los
nueve esqueletos de las hojas 3 a 11. `evaluacion/` sigue fuera del libro, con el banco y
los ejercicios tipo examen escritos contra la estructura antigua de dieciséis capítulos y
con referencias cruzadas rotas. Al reescribir ese material hay que renumerarlo y comprobar
que todo `@...` resuelve.

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

El enunciado se duplica a propósito. Con una decena de ejercicios por hoja es más robusto
que un include compartido, que obligaría a separar cada solución de su enunciado. La
solución resuelta se genera desde la hoja con el ayudante de la skill, de modo que las dos
versiones no se desincronizan mientras se edite solo la de enunciados.

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
   índice: no aparecen en ningún fichero del repositorio y nadie los cita todavía. Al
   revisar los capítulos 1 y 2 hay que escribirlos o retirarlos del índice.
3. Sus números de capítulo son los de la **estructura antigua de dieciséis capítulos**.
   Antes de fiarse de una fila hay que traducirla a la estructura de nueve.

Las filas del índice se nombran hoy en prosa ("Teo. interpolación exacta"), no con la
etiqueta del entorno, así que no hay forma mecánica de casarlas. Al añadir filas nuevas,
poner la etiqueta entre paréntesis.

## Los cuadernos van completos

**Decidido en agosto de 2026: los cuadernos de los capítulos llevan el código entero**, el
mismo que los apuntes. Antes el perfil `notebooks` aplicaba `scripts/strip-code.lua`, que
sustituía lo que hubiera entre centinelas `#---` por un `# TODO: completar en clase`; ahora
aplica `scripts/strip-delims.lua`, que solo borra las líneas `#---` y deja el código.

Los centinelas siguen en las fuentes y `check-centinelas.py` sigue comprobando que están
emparejados, pero su significado ha cambiado: ya no marcan un hueco, marcan **el trozo que
se escribe en directo al explicar**. Con eso, el presupuesto de huecos por sesión que había
aquí deja de tener sentido y se retira.

Lo que sí sigue vigente es qué bloques se explican, y eso se marca en el propio capítulo con
`.codigo-clave`. El criterio está en `estilo-codigo.md`.

**No decir en ningún sitio que el cuaderno tiene huecos.** Se corrigió en `curso/colab.qmd`
y en la primera página del capítulo 1.

## Cuadernos

**No se escriben a mano.** Salen del mismo `.qmd` del capítulo con `make notebooks`, que
llama a `scripts/crear-ipynb.py`. Consecuencias al escribir el capítulo:

- Lo que hay entre un par de `#---` **se conserva**; solo desaparecen las dos líneas
  centinela. Marcan el trozo que se escribe en directo al explicar, no un hueco.
- El preámbulo `.content-hidden` **no llega**, así que el primer bloque visible lleva los
  imports reales y la semilla.
- **Los macros del contrato de notación no hacen falta en el cuaderno: Pandoc los expande**
  al escribir el `ipynb`, los 100, incluidos los nueve `\DeclareMathOperator`. Medido sobre
  los cinco capítulos escritos: cero macros sin expandir, y las 1065 expresiones
  matemáticas de sus cuadernos válidas bajo MathJax, que es el motor de Colab.
  `scripts/crear-ipynb.py` lo comprueba en cada generación y falla si aparece alguno.
- Aun así, cada cuaderno lleva como **primera celda** la notación del curso, generada por
  `scripts/macros-mathjax.py`. No es para el cuaderno, es para las celdas nuevas que se
  teclean **en clase**: sin ella, `$\Riskproc{n}$` escrito en Colab no renderiza. Va en un solo
  `$...$` de una línea, que MathJax procesa y no dibuja (medido: cero glifos).
- Ese script traduce dos cosas que MathJax no acepta: `\DeclareMathOperator` pasa a
  `\newcommand` con `\operatorname`, y **`\coloneqq` pasa a `\mathrel{:=}`**. El segundo
  falla incluso en la configuración por defecto de MathJax 3, porque vive en la extensión
  `mathtools`, que Colab no carga. Es decir: **pegar `_macros.tex` tal cual en Colab no
  funciona**, y por eso existe el traductor.
- Al buscar macros sin expandir, la regex es `\\([A-Za-z]+)` y **no** `\\(\w+)`: el
  subrayado es carácter de palabra, así que `\w+` lee `\argmin_w` como `argmin_w` y el
  macro escapa a la comprobación.
- **El enlace a Colab se activa por documento**, desde agosto de 2026. Dos pasos: declarar
  `cuaderno: <nombre>.ipynb` en la cabecera YAML del `.qmd` y poner `{{< include
  ../assets/includes/_colab-link.qmd >}}` donde deba salir el enlace. El include construye
  la URL con `{{< meta cuaderno >}}` sobre el repositorio público, y se oculta en formato
  `ipynb` para que el cuaderno no se enlace a sí mismo. Lo tienen el capítulo 1 y
  `curso/colab.qmd`; los demás capítulos lo ganan cuando se publiquen. **No usar
  `QUARTO_DOCUMENT_FILE`**: Quarto no lo define al renderizar, comprobado.
- Los divs de referencia cruzada se desanidan con `restore-cells.lua`, de modo que el código
  dentro de `::: {#fig-...}` sí sale como celda ejecutable.
- El cuaderno se genera con `--no-execute`, así que un error de ejecución no se detecta ahí.
  Se detecta en `make sitio`.

`curso/colab.qmd` es la excepción a la regla anterior: es un anexo, no
un capítulo, y genera cuaderno porque es donde se aprende a usar la herramienta. Está
declarado a mano en `_quarto-notebooks.yml` y en `scripts/crear-ipynb.py`, que por defecto
solo recorre `capitulos/*.qmd`. Se ejecuta entero, como todos desde agosto de 2026.

Después de tocar un capítulo, `make notebooks` y comprobar que el `.ipynb` tiene los
`# TODO: completar en clase` donde tocan y que se ejecuta de arriba abajo en un entorno
limpio.
