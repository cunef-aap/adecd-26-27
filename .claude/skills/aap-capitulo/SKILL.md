---
name: aap-capitulo
description: Escribir, revisar, reordenar o ampliar material del libro "Aprendizaje Automático - Predicción" (G244, CUNEF) en el repositorio aap-cunef. Úsala siempre que se toque un .qmd de capitulos/, problemas/ o evaluacion/, o cuando el usuario pida "escribe el capítulo N", "sigue el estilo del capítulo 1", "revisa el hilo de este capítulo", "haz la hoja del capítulo N" o cualquier trabajo sobre estos apuntes. Cubre el arco narrativo, el ritmo matemático, el contrato de notación, la mecánica de Quarto y el estilo de código. La voz en español la aporta `write-roinaveiro-es`, que hay que cargar además de esta.
---

# El modelo editorial de aap-cunef

`PLAN_CURSO.md:8` fija que **el capítulo 1 es el modelo editorial**. Esta skill extrae ese
modelo de `capitulos/01-senal-ruido.qmd` y `capitulos/02-aprender-minimizando.qmd`, que son
los dos únicos capítulos escritos, para que los nueve restantes salgan con la misma
factura.

## Qué cubre esta skill y qué no

Esta skill **no** describe la voz. La voz la fija `write-roinaveiro-es`, que hay que cargar
siempre junto a esta: prosa neutra, sin lenguaje publicitario, nosotros en la exposición y
tú en los enunciados, cero rayas largas, cero comillas latinas, cero emoji y ningún
tratamiento de cortesía.
Esas reglas las verifica `scripts/check-estilo.py` y **abortan el render**.

Lo que aporta esta skill es lo demás: cómo se ordena un capítulo, qué se define, qué se
demuestra, qué figura va antes de qué fórmula, qué macro se usa para cada símbolo, cómo se
escribe una celda de código y qué hace falta para que el cuaderno derivado se ejecute solo.

## Regla de entrega

**Todo lo que se escribe o se reescribe se entrega marcado con `.nuevo`**, para que el autor
revise solo lo cambiado. No hace falta que lo pida. Los detalles, en
`references/marcado-de-revision.md`.

## Antes de escribir, cinco lecturas

1. El **stub del capítulo** en `capitulos/`. Sus encabezados `##` y el comentario HTML de
   cada sección son el guion cerrado, no una sugerencia. Si hay que apartarse de él, se
   dice y se justifica antes de escribir.
2. El **capítulo anterior completo**. La primera sección del capítulo nuevo tiene que
   recoger literalmente el problema que dejó abierto el anterior.
3. `references/mapa-curso.md`: pregunta central, qué debe quedar definido y demostrado,
   dependencias, datos y de dónde sale el material.
4. `assets/includes/_macros.tex`: el contrato de notación. Es de lectura obligada aunque
   se crea recordarlo.
5. `PLAN_CURSO.md`, para el criterio de terminado y para lo que se ha decidido dejar fuera.

### Cuando el capítulo anterior no está escrito

Solo están escritos el 1 y el 2, así que la lectura 2 no siempre es posible. En ese caso se
usa el campo **Deja abierto** de la ficha del capítulo anterior en `mapa-curso.md`, que
contiene la frase literal con la que ese capítulo terminará. El capítulo nuevo la recoge. Si
al escribirlo se decide cambiarla, se actualiza el mapa en el mismo momento, para que el
capítulo anterior la cumpla cuando se escriba.

## El arco de un capítulo

Cinco movimientos, en este orden:

1. **Continuidad.** Se abre recogiendo el problema abierto del capítulo anterior y se
   convierte en un plan explícito. Modelo: `capitulos/02-aprender-minimizando.qmd:19-39`,
   que recoge el fracaso de la búsqueda por rejilla y lo desdobla en tres pasos.
2. **Fenómeno antes que fórmula.** El lector ve el problema en una figura o en un número
   antes de que aparezca la notación que lo formaliza. Modelo: la interpolación del
   capítulo 1, que se ve fallar sobre datos nuevos (`fig-trampa`) antes de que se defina
   nada.
3. **Objeto, resultado, demostración.** Definición del objeto que hace falta, resultado
   sobre él, demostración breve y completa, y a continuación la lectura del resultado en
   palabras. Ninguna expresión se deja sin comentar.
4. **Código que materializa la fórmula.** La traducción a PyTorch o a scikit-learn viene
   después de la fórmula y usa los mismos nombres. Cuando hay derivación analítica, se
   comprueba contra autodiferenciación.
5. **Transición.** El capítulo cierra creando la necesidad del siguiente. Modelo:
   `capitulos/01-senal-ruido.qmd:742-745` y `capitulos/02-aprender-minimizando.qmd:1129-1132`.

## La regla de orden

Es la regla que decide un capítulo, y la que hay que auditar antes que ninguna otra.

> Un concepto se introduce en el punto en que hace falta para resolver el problema que
> está abierto, nunca antes.

Prueba operativa, aplicable a cualquier borrador: escribir **una frase por sección** con la
forma *"hasta aquí sabemos X; nos falta Y"*. Después:

- Si dos secciones consecutivas producen la misma frase, una de las dos sobra o hay que
  fundirlas.
- Si una sección no admite esa frase, está colocada antes de que exista la necesidad que la
  justifica y hay que moverla.
- Si el Y de una sección no es el X de la siguiente, falta una transición o falta una
  sección.

El hilo del capítulo 1 resuelto así, sección a sección, está en
`references/arco-editorial.md` y sirve de patrón.

## Los cinco no negociables

| | Regla | Referencia |
|---|---|---|
| 1 | Todo símbolo sale de `_macros.tex`. Nunca se redefine ni se escribe a pelo. | `references/contrato-notacion.md` |
| 2 | Se demuestra todo lo que se enuncia. Lo que no, va a un apéndice citado por su etiqueta o a `::: {.cajanegra}` con el motivo en una frase. | `references/arco-editorial.md` |
| 3 | Cabecera de 15 líneas intacta, entornos numerados, figuras en div o de margen con `#| label: fig-`, centinelas `#---` emparejados por bloque. | `references/mecanica-quarto.md` |
| 4 | PyTorch para optimización, scikit-learn para flujos. Identificadores en español. El capítulo regenera sus datos. | `references/estilo-codigo.md` |
| 5 | Ningún dato se descarga al renderizar. Todo sale de `datos/` por ruta relativa. | `references/mecanica-quarto.md` |
| 6 | **Nada se menciona antes de explicarse.** Si un término hace falta antes de su apartado, se explica ahí o se reordena. | `references/arco-editorial.md` |

## Excepciones al canon

El capítulo 1 es el modelo, con tres desviaciones que **no** hay que imitar:

1. **Colores fuera de paleta** en el capítulo 1, con la lista en
   `references/estilo-codigo.md`. El capítulo 2 ya solo usa colores del tema. Los capítulos
   nuevos usan la paleta.
2. **Cero ejercicios.** El criterio de terminado pide hoja de problemas y ejercicios; el
   capítulo 2 sí los tiene (cuatro, en una sección final). Ese es el patrón correcto.
3. **Resultados duplicados con el apéndice.** Los tres teoremas de la normal se enuncian en
   el capítulo con las etiquetas `thm-traslacion-normal`, `thm-escala-normal`,
   `thm-momentos-normal` y **se vuelven a enunciar** en `curso/probabilidad.qmd` con
   `thm-traslacion`, `thm-escala`, `thm-momentos`. Quarto los numera como seis resultados
   independientes y el capítulo no enlaza a su propia demostración. Al remitir a un
   apéndice, se cita la etiqueta del apéndice; no se reenuncia.

## Criterio de terminado

De `PLAN_CURSO.md:86-98`, en forma verificable. Un capítulo está terminado cuando:

- [ ] la pregunta central cabe en una frase y aparece en la primera sección;
- [ ] la apertura recoge el problema abierto del capítulo anterior y el cierre crea el del
      siguiente;
- [ ] cada sección pasa la prueba de la regla de orden;
- [ ] solo se definen conceptos que se reutilizan;
- [ ] todo resultado enunciado tiene demostración o marca de fuera de alcance;
- [ ] hay al menos un experimento visual que muestra el fenómeno antes de formalizarlo;
- [ ] el código de optimización está en PyTorch y el de flujo de trabajo en scikit-learn;
- [ ] los datos que aparecen sirven para algo y no se ha introducido un conjunto nuevo sin
      necesidad;
- [ ] existe la hoja de problemas correspondiente y el cuaderno se genera del mismo `.qmd`;
- [ ] `curso/glosario.qmd` recoge la notación nueva y `problemas/index.qmd` el estado de la
      hoja;
- [ ] el capítulo marca con demostración los resultados evaluables, que es de donde
      sale el bloque B de las hojas y del examen;
- [ ] `make marcas` no encuentra marcas `.nuevo` sin aceptar;
- [ ] `make check` pasa y `check-capitulo.py` no da errores;
- [ ] el render no produce avisos ni referencias rotas.

## Modo revisión

Cuando el capítulo ya existe hay dos auditorías, y **siempre en este orden**.

### Auditoría de hilo

Es la que decide si el capítulo funciona. Procedimiento:

1. Extraer el orden actual. Cuidado: `##` es también el título de todo entorno numerado, de
   modo que un `grep` literal da 20 encabezados en el capítulo 1 y 35 en el 2, no las 7 y 10
   secciones reales. Se filtran los que están dentro de un div:

       awk '/^:::/{d=!d} /^## /&&!d' capitulos/NN-nombre.qmd

   Y dentro de cada sección, las subsecciones `###`, los entornos numerados y las figuras.
2. Escribir la frase *"hasta aquí sabemos X; nos falta Y"* de cada sección.
3. Producir una tabla `orden actual | problema detectado | orden propuesto`.
4. **Acordar la tabla con el usuario antes de mover una sola línea.** Reordenar rompe
   referencias cruzadas y dependencias entre resultados, así que el movimiento se ejecuta
   de una vez y con el destino ya decidido.
5. Al ejecutar: comprobar que ningún resultado se usa antes de enunciarse, y que las
   referencias `@...` siguen resolviendo.

### Auditoría de factura

Notación contra `_macros.tex`, entornos, figuras, código, centinelas, longitud de párrafo y
estilo. Se apoya en `scripts/check-capitulo.py` y en `make check`.

## Cierre

```bash
make check
python .claude/skills/aap-capitulo/scripts/check-capitulo.py capitulos/NN-nombre.qmd
make sitio
make notebooks
```

### Modo borrador

Sobre un fragmento suelto, fuera de `capitulos/`, sí se pueden comprobar la cabecera, las
macros, los centinelas, las referencias cruzadas y el estilo. `make sitio` y `make notebooks`
no aplican: necesitan el capítulo entero dentro del proyecto.

`make check` encadena `check-centinelas.py` y `check-estilo.py`, y cualquiera de los dos
aborta el build. `check-estilo.py` recorre también los `.md` de esta skill, así que sus
propios ficheros cumplen las reglas de voz. `check-capitulo.py` es complementario: comprueba la cabecera, los imports
visibles, el emparejamiento de centinelas dentro de cada bloque, las macros indefinidas y
las referencias cruzadas rotas.

## Ficheros de referencia

| Fichero | Cuándo cargarlo |
|---|---|
| `references/arco-editorial.md` | siempre, antes de escribir o reordenar |
| `references/mapa-curso.md` | al empezar un capítulo, para saber qué le toca |
| `references/contrato-notacion.md` | al escribir matemáticas o al reciclar de Chodrow |
| `references/mecanica-quarto.md` | al escribir el `.qmd`, y ante cualquier duda de sintaxis |
| `references/estilo-codigo.md` | al escribir celdas de código o figuras |
| `references/hojas-y-cuadernos.md` | al escribir una hoja, un ejercicio de examen o un cuaderno |
| `references/marcado-de-revision.md` | siempre que se entregue texto para revisar |
