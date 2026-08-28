# Marcado de revisión

Regla permanente: **todo lo que se escribe o se reescribe se entrega marcado en color**, para
que el autor pueda revisarlo sin releer el capítulo entero. Es lo que permite iterar rápido:
él lee solo lo marcado y va aceptando cambios.

## Cómo se marca

La clase es `.nuevo`, definida en `assets/styles.css`. Funciona con Pandoc de serie, sin
extensiones.

    Una frase con [un trozo cambiado]{.nuevo} en medio de un párrafo.

    ::: {.nuevo}
    Un párrafo entero, un resultado, una demostración o un apartado completo.
    :::

Se ve en verde al renderizar con `make sitio` o `make preview`. El verde es deliberadamente
ajeno a la identidad del libro: tiene que cantar y tiene que desaparecer. **No se usa el
naranja**, que está reservado a `::: {.trampa}`.

## La marca cubre el cambio, y nada más

Regla suya, de agosto de 2026: **el color va solo en lo que ha cambiado, nunca en secciones
enteras.** Marcar una sección completa porque se han reescrito dos frases obliga a releerla
entera, que es justo lo que el marcado pretende evitar.

La granularidad correcta:

| Lo que ha cambiado | Cómo se marca |
|---|---|
| una frase o un trozo de frase dentro de un párrafo que se conserva | span: `[la frase nueva]{.nuevo}` |
| un párrafo reescrito de arriba abajo | div alrededor de ese párrafo |
| un pasaje nuevo de varios párrafos, escrito de cero | un div alrededor del pasaje |
| un resultado, una demostración o un ejercicio nuevos | div alrededor del entorno |
| una sección en la que solo cambian tres frases | tres spans, **no** un div |

Nunca un div que abarque más de un encabezado, ni un div alrededor de texto que se conserva
sin tocar. Si al terminar un div contiene párrafos que no se han modificado, hay que partirlo.

### La trampa del apartado marcado

Al añadir un apartado nuevo a una lista de `a.`, `b.`, `c.`, el marcador de lista va **fuera**
del span:

    f. [El reparto se hace al azar. Razona por qué.]{.nuevo}      <- correcto

    [f. El reparto se hace al azar. Razona por qué.]{.nuevo}      <- roto

En la segunda forma el corchete abre un span antes de que Pandoc vea la `f.`, de modo que el
apartado deja de ser un elemento de lista y aparece como texto corrido dentro del apartado
anterior. No da ningún aviso al renderizar: hay que mirar el HTML y comprobar que el apartado
sale como `<li>`. El mismo cuidado vale para `- ` y para las listas numeradas.

## Qué se marca y qué no

- **Sí**: prosa nueva, prosa reescrita, resultados nuevos, ejercicios nuevos, apartados
  nuevos, código nuevo o reescrito.
- **No**: los cambios puramente mecánicos, como reajustar una línea a 92 columnas o
  renombrar una macro. Marcar eso solo añade ruido.
- **No**: las supresiones. Dejar tachado lo que se borra dobla la longitud del capítulo
  durante la revisión, que es lo contrario de lo que se busca. Lo suprimido se entrega en una
  tabla en el mensaje final, y se guarda una copia del fichero anterior para poder comparar.

## La trampa de las fórmulas

`scripts/clean-eqref.lua` colapsa cualquier `Span` que contenga matemáticas, para no romper
el `.ipynb`. Consecuencia: un span alrededor de una fórmula **pierde la marca en el
cuaderno**, aunque en el HTML se vea.

    [$\coef\T\xv$]{.nuevo}      <- la marca desaparece en el cuaderno

    ::: {.nuevo}
    $$
    \coef\T\xv
    $$
    :::                          <- correcto

Para marcar una ecuación se usa el div alrededor del `$$`.

## Qué le pasa al cuaderno

Comprobado sobre el repositorio: un span con clase se convierte en
`<span class="nuevo">…</span>`, que Jupyter y Colab renderizan sin problema (ya hay spans así
en los cuadernos actuales, generados por los entornos numerados). Un div con clase pierde el
envoltorio y conserva el contenido. En ninguno de los dos casos se pierde texto ni se rompe
la ejecución.

## Aceptar los cambios

    python scripts/aceptar-marcas.py --listar     # enumera las marcas con su línea
    python scripts/aceptar-marcas.py --aceptar    # las quita conservando el contenido
    make marcas                                   # lo mismo que --listar

`--aceptar` desenvuelve spans y divs, incluidos los divs anidados. Aceptar un cambio suelto
es más rápido a mano en el editor: se borran los corchetes y la clase.

`make marcas` sale con código 1 si queda alguna marca, y `make publicar` depende de él, de
modo que no se publica un capítulo a medio revisar. **No** forma parte de `make check`: eso
abortaría el render justo cuando hace falta renderizar para ver las marcas.

## Criterio de cierre

Un capítulo no está terminado mientras `make marcas` encuentre algo.
