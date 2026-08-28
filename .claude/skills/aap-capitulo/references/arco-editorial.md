# Arco editorial

Destilado de `capitulos/01-senal-ruido.qmd` (745 líneas) y
`capitulos/02-aprender-minimizando.qmd` (1170 líneas).

## 1. El hilo del capítulo 1, sección a sección

Este es el patrón. Cada sección se resume con la frase *"hasta aquí sabemos X; nos falta
Y"*, y el Y de cada una es el X de la siguiente.

| # | Sección | Hasta aquí sabemos | Nos falta |
|---|---|---|---|
| 1 | Introducción: datos, señal y ruido | que queremos $\widehat y = f(\xv)\approx y$ | reconocer que la relación observada no es exacta, y nombrar sus dos partes |
| 2 | Sobreajuste | que hay una señal estable y un ruido que la oculta | ver por qué no basta con ajustar bien los datos observados |
| 3 | Modelizar el ruido | que ajustar el ruido empeora la predicción | poder hablar del ruido en términos matemáticos |
| 4 | Propiedades de la distribución normal | qué es una densidad normal y cómo se simula | las propiedades que permiten pasar del ruido a la respuesta |
| 5 | La normal estándar | traslación, escala, media y varianza | construir cualquier normal a partir de una sola |
| 6 | Ruido gaussiano | manipular variables normales | volver al modelo $\yi=f(x_i)+\varepsilon_i$ y decir qué distribución tiene $\yi$ |
| 7 | Verosimilitud del modelo | un modelo generador completo | un criterio para comparar unos parámetros con otros |

Cierre (`01-senal-ruido.qmd:742-745`): la rejilla permite ver qué significa maximizar la
verosimilitud, pero deja de ser viable en cuanto aumenta el número de parámetros. Ese es el
problema abierto que hereda el capítulo 2.

Apertura del capítulo 2 (`02-aprender-minimizando.qmd:19-39`): recoge esa frase, la
cuantifica ($m^q$ evaluaciones) y la convierte en un plan de tres pasos que son las tres
primeras secciones del capítulo. Ese es el enganche que hay que reproducir.

Nota: el orden del capítulo 2 está pendiente de revisión. No se usa como patrón de orden;
sí como patrón de ritmo matemático.

## 2. Los cinco movimientos

1. **Continuidad.** Recoger el problema abierto del capítulo anterior y convertirlo en un
   plan explícito.
2. **Fenómeno antes que fórmula.** Una figura o un número enseñan el problema antes de que
   aparezca la notación. El caso verificado es el capítulo 1: el interpolador se ve fallar
   sobre datos nuevos (`fig-trampa`, :142) antes de que se defina el sobreajuste. El
   capítulo 2 **no** sigue el patrón: `fig-gradiente-riesgo` (:527) llega después de
   `prp-direccion-descenso` (:498) y de su demostración, como confirmación visual de un
   resultado ya probado. Lo mismo con `fig-tasa-aprendizaje` (:741) frente a
   `prp-caso-cuadratico` (:704). Un capítulo de método puede permitírselo; uno que introduce
   vocabulario, no.
3. **Objeto, resultado, demostración, lectura.** Definición del objeto que hace falta,
   resultado sobre él, demostración, y después la lectura del resultado en palabras.
4. **Código que materializa la fórmula.** Viene después, usa los mismos nombres, y cuando
   hay derivación analítica se comprueba contra autodiferenciación
   (`02-aprender-minimizando.qmd:898-911`).
5. **Transición.** El cierre crea la necesidad del capítulo siguiente.

## 3. Huella cuantitativa

Medida sobre los dos capítulos. Es un rango orientativo, no una cuota.

| | cap. 1 | cap. 2 |
|---|---:|---:|
| secciones `##` reales | 7 | 10 |
| definiciones `#def-` | 8 | 8 |
| teoremas, lemas, corolarios y proposiciones | 4 | 12 |
| bloques `.proof` | 1 | 12 |
| figuras (`#fig-` en div más `#| label: fig-` en margen) | 8 (6 + 2) | 4 (4 + 0) |
| bloques `{python}` | 16 | 14 |
| ejercicios `#exr-` | 0 | 4 |
| pares de centinelas `#---` | 4 | 8 |
| mediana de palabras por frase | 13 | 13 |
| mediana de palabras por párrafo | 18 | 22 |
| párrafo más largo | 84 | 81 |
| rayas largas, comillas latinas, emoji, tratamiento de cortesía | 0 | 0 |

Lectura de la tabla:

- **Párrafos de tres o cuatro frases cortas.** La complejidad va en las matemáticas, no en
  la sintaxis. Un párrafo de más de 90 palabras es señal de que hay dos ideas juntas.
- **El capítulo 1 define mucho y demuestra poco**, porque introduce el vocabulario del
  curso. El capítulo 2 demuestra casi todo lo que enuncia. Un capítulo aplicado se parecerá
  al 1; un capítulo de método, al 2.
- **La cadencia de figura depende del tipo de capítulo.** El expositivo (el 1) va a una
  figura cada 90 líneas; el de método (el 2), a una cada 290. Toda figura enseña un
  fenómeno; ninguna decora.

## 4. Ritmo matemático

- **Los resultados se enuncian para el caso concreto que se está tratando**, no en
  generalidad máxima. `thm-gradiente-riesgo-1d` es "gradiente del riesgo cuadrático de una
  recta", no un teorema de cálculo vectorial. La generalidad llega cuando hace falta, en el
  capítulo 3.
- **Las demostraciones son completas y breves**, entre cinco y quince líneas, con el álgebra
  explícita en `\begin{aligned}` y una frase final que dice qué se ha usado. Modelo:
  `02-aprender-minimizando.qmd:115-143` (riesgo bajo señal más ruido) y `:599-610`
  (condición de primer orden).
- **Un lema instrumental se enuncia justo antes de usarse.** `lem-invarianza-afin`
  (`:297-319`) existe para poder demostrar `cor-mle-minimos-cuadrados` dos párrafos
  después, y se dice explícitamente: "Para extraer el problema de optimización de esta
  expresión utilizaremos un hecho sencillo".
- **El contraejemplo va inmediatamente después del resultado que lo necesita.** Tras la
  condición de primer orden: "El recíproco no es cierto para una función cualquiera:
  $h(w)=w^3$ tiene gradiente cero en $w=0$, pero ese punto no es un mínimo".
- **Una demostración puede convertirse en ejercicio, y entonces va donde estaba.** El
  resultado se sigue enunciando en su sitio, porque el hilo lo necesita, y el
  `::: {#exr-slug}` ocupa el lugar de la demostración, de modo que el lector encuentra la
  tarea con el contexto todavía fresco. Se deja además el marcador
  `<!-- demostracion: exr-slug -->` tras el resultado, para que `check-capitulo.py` no avise.
  La sección final de ejercicios se reserva para los de laboratorio, que necesitan el
  capítulo entero.
- La presentación de un resultado (motivo, enunciado, display, lectura en palabras,
  consecuencia) la fija `write-roinaveiro-es`. Aquí no se repite.

## 5. Qué se demuestra y qué no

Convenio de `README.md:67-75`: se demuestra todo lo que se enuncia. Las dos salidas
legítimas cuando una demostración no cabe:

1. **Desplazarla a un apéndice** y citarla desde allí. Los tres teoremas de la normal del
   capítulo 1 se demuestran en `curso/probabilidad.qmd`. Al hacerlo, se cita la etiqueta
   del apéndice; no se reenuncia el teorema con una etiqueta nueva (ver "Excepciones al
   canon" en `SKILL.md`). Y se deja el marcador

       <!-- demostracion: curso/probabilidad.qmd#thm-traslacion -->

   inmediatamente después del div del resultado, que es lo que busca `check-capitulo.py`
   para no avisar. Hoy el capítulo 1 no lo tiene y por eso da tres avisos.
2. **Declararla fuera de alcance** en `::: {.cajanegra}`, con el motivo en una frase.
   Modelo literal, `curso/probabilidad.qmd:110-115`: la constante de normalización de la
   gaussiana se omite porque exige coordenadas polares y no enseña nada de aprendizaje
   automático.

Lo que no se hace: enunciar un resultado y dejarlo colgado sin ninguna de las dos marcas.

## 6. Avisos y honestidad de alcance

Dos patrones vigentes, ambos con `::: {.callout-warning title="..."}` y el título en el
atributo:

- **Aviso conceptual**, cuando el lector puede tomar una hipótesis por un hecho.
  `01-senal-ruido.qmd:521-528`, "El modelo generador es una hipótesis": la distribución que
  genera los datos es desconocida, y las conclusiones son condicionales a la elección.
- **Aviso de método**, cuando la herramienta puede engañar. `02-aprender-minimizando.qmd:923-928`,
  "Se deriva el programa que se ejecuta": la autodiferenciación derivará correctamente una
  implementación errónea.

`::: {.callout-note}` se reserva para precisiones que no cambian el resultado. Modelo:
`02-aprender-minimizando.qmd:1079-1084`, sobre el divisor $\nobs$ frente a $\nobs-2$.

`::: {.trampa}` (rótulo automático "Error frecuente", filete naranja) está definido en
`assets/styles.css` y todavía no se usa en ningún capítulo. Es el bloque adecuado para el
error que se repite en los exámenes, y conviene empezar a usarlo.

## 7. Autonomía del capítulo

Cada capítulo se lee y se ejecuta solo, porque de él sale un cuaderno independiente.

- **Regenera sus datos.** El capítulo 2 vuelve a simular los datos del 1 y lo dice:
  "Volver a generarlos hace que este capítulo y su cuaderno se puedan ejecutar de manera
  independiente" (`:41-42`).
- **Repite sus imports en un bloque visible.** El preámbulo `.content-hidden` no llega al
  cuaderno.
- **Recuerda la notación que reutiliza**, con una frase y una referencia cruzada, no
  repitiendo la definición.

## 8. Errores de arco que hay que evitar

- **Explicar cada tema de una forma distinta.** En un capítulo aplicado, donde se recorren
  varios problemas independientes, hay que fijar un **esquema y repetirlo literalmente** en
  todos: problema, daño, tratamientos posibles en tabla, implementación con el nombre de la
  clase y sus argumentos, y resultado sobre los datos del capítulo. El capítulo 5 hubo que
  rehacerlo dos veces por esto: sin el molde, cada subsección salía con una profundidad
  distinta, un problema se quedaba sin solución y otro sin implementación. Y una regla que sale
  de la misma queja: **no se menciona un problema sin dar al menos un tratamiento**.
- **Presentar una regla antes que los objetos que la regla gobierna.** Es la forma en que el
  error siguiente aparece en los capítulos aplicados, y costó rehacer el capítulo 5 entero. Su
  primera versión definía la fuga de información y la regla de estimar con `train` en la
  sección 2, y las transformaciones a las que la regla se aplica en las secciones 3 a 5: la
  definición hablaba de medias de un escalado, medianas de una imputación y listas de categorías
  de una codificación que el lector todavía no había visto. La prueba para detectarlo antes de
  escribir: si el enunciado de una regla necesita nombrar tres objetos, esos tres objetos tienen
  que estar ya presentados. Y el orden correcto casi siempre es el operativo, primero la
  herramienta y después la disciplina con la que se usa.
- **Mencionar un concepto antes de explicarlo.** Es el error que más rompe la lectura y no
  admite excepciones. El capítulo 2 lo cometía: hablaba de autodiferenciación al presentar el
  descenso de gradiente, doscientas líneas antes de decir qué era. Cuando el texto necesita
  nombrar algo que aún no se ha contado hay dos salidas, explicarlo ahí mismo en una frase o
  reordenar para que llegue antes. Anunciar el futuro sí vale ("volveremos a esto en el
  capítulo 4"); apoyarse en él, no.
- Una sección de prerrequisitos sin una pregunta predictiva detrás. `PLAN_CURSO.md:11` lo
  prohíbe: por eso no hay capítulo de convexidad ni de álgebra matricial, y las matrices
  aparecen en el capítulo 3 porque hacen falta para expresar el modelo con muchas variables.
- Definir un concepto que no se reutiliza después.
- Enunciar un resultado general del que solo se usa un caso particular.
- Un conjunto de datos nuevo por capítulo. Los del curso son `prostate.data` y
  `airbnb_madrid.csv`, y solo se añade otro si ninguno de los dos permite mostrar
  limpiamente el fenómeno. Los datos simulados no cuentan como conjunto nuevo: se usan
  cuando el capítulo necesita conocer la señal verdadera, que es el caso de los capítulos
  1, 2 y 6.
- Un cierre que resume lo dicho en lugar de abrir lo siguiente. Y, en el mismo sitio, el cierre
  que no da el diagnóstico con el que el capítulo siguiente dice abrir. La comprobación es
  mecánica: leer la primera frase del capítulo siguiente y ver si lo que atribuye al anterior
  está escrito allí.
- **Heredar un procedimiento y enmendarlo sin decirlo.** El capítulo 5 escribía "aplicamos el
  protocolo del capítulo 4 sin cambiarle nada" y le cambiaba los pasos 1 y 3, que era justo lo
  que la sección anterior acababa de justificar. Cuando un capítulo enmienda algo que hereda, la
  frase tiene que nombrar la enmienda; si no, anula el trabajo de la sección que la justificó y
  el estudiante aplica el procedimiento original.
- **No declarar las consecuencias del orden expositivo.** Si el capítulo explora los datos y
  después rehace el reparto, las decisiones se tomaron mirando filas que acaban en test, y la
  estimación final arrastra optimismo. El orden puede ser el correcto para explicar, pero la
  consecuencia se dice, con el número: en el capítulo 5, 2874 de las 3784 filas del test
  definitivo estaban en el train con el que se exploró.
- **Atribuir a la última decisión una diferencia emparejada contra la referencia.** En una tabla
  de candidatos donde cada uno añade algo al anterior, la diferencia frente al candidato de
  referencia acumula todos los cambios intermedios. La que mide una decisión es la diferencia
  frente al candidato **inmediatamente anterior**, y hay que calcularla aparte: en el capítulo 5
  el recorte valía $-472\pm107$ frente a la referencia y $-420\pm141$ frente a su anterior, y
  con ello pasaba de cuatro errores típicos a tres.
