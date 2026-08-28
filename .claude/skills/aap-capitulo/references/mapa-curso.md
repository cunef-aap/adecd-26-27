# Mapa del curso

## La asignatura

Aprendizaje automático: predicción. Código **G244**. Doble Grado en ADE y Ciencia de Datos,
Escuela Politécnica Superior, CUNEF. Tercer curso, primer semestre, obligatoria, **6 ECTS**.
Departamento de Métodos Cuantitativos. Guía docente 2026-27.

Quince semanas, tres sesiones por semana. Unas 41 horas de clase y unas 109 de trabajo
autónomo, según el reparto propio del curso; la guía docente oficial no desglosa
horas.

## Temario oficial

Literal de la guía docente. Once epígrafes más el complemento.

**Tema 1. Introducción al Aprendizaje Automático**
- Conceptos básicos de aprendizaje automático
- Estado del arte

**Tema 2. Metodologías de Aprendizaje Automático para predicción**
- Análisis y tratamiento de datos
- Reducción de dimensiones y selección de variables
- Validación y métricas de evaluación

**Tema 3. Algoritmos Aprendizaje Automático para predicción**
- Descenso de gradiente
- Métodos lineales
- Métodos no lineales
- Métodos basados en reglas

**Tema 4. Implementación y aplicación**
- Librerías de programación para Aprendizaje Automático
- Casos de uso y aplicaciones

Complemento: "una breve introducción al uso de agentes de IA para la asistencia en la
implementación de modelos de aprendizaje automático".

El mapeo epígrafe por epígrafe a capítulos estaba en `curso/trazabilidad.qmd`, retirado en
agosto de 2026 y recuperable del historial de git. Al escribir un
capítulo hay que comprobar que ese mapeo sigue siendo cierto.

## Resultados de aprendizaje

Siete códigos, con numeración salteada; la guía no explica por qué. **No son RA ni CE. No se
inventan los intermedios.** Los enunciados literales, agrupados en 2.1 Conocimientos o
contenidos, 2.2 Habilidades o destrezas y 2.3 Competencias, están en el PDF. Abajo van
abreviados.

| Código | Enunciado (abreviado) |
|---|---|
| **C1** | Conoce los fundamentos matemáticos y estadísticos de la Ciencia de Datos |
| **C6** | Conoce las principales técnicas de análisis exploratorio preliminar de los datos |
| **H1** | Analiza, valida e interpreta modelos matemáticos de situaciones reales con herramientas de álgebra lineal, cálculo diferencial e integral, estadística y cálculo numérico |
| **H4** | Aplica los modelos adecuados de probabilidad y estadística al análisis de datos de todo tipo de fuentes |
| **H8** | Maneja los métodos de aprendizaje estadísticos y automáticos aplicados a conjuntos de datos |
| **CO1** | Piensa críticamente sobre los datos: almacenamiento, preprocesamiento y análisis adecuados a los objetivos |
| **CO3** | Utiliza procesos teóricos y aplicados para extraer información de conjuntos homogéneos o heterogéneos, en particular de gran volumen |

## Evaluación

Evaluación continua **40 %** (examen parcial 1, 20 %, semanas 6-7, más proyecto desarrollado
parcialmente con agentes de IA, 20 %, semanas 12-13) y examen final escrito **60 %**, sobre
todo el contenido. El examen final requiere **5 sobre 10** para optar a aprobado.

Cómo sale la nota de actas:

| Situación | Nota |
|---|---|
| Examen final mayor o igual que 5 | 40 % continua más 60 % final |
| Examen final menor que 5 | la calificación del examen final |
| No se presenta al examen final | la nota de continua, ponderada al 40 % |
| No ha calificado ninguna prueba | No Presentado |

En convocatoria extraordinaria, la nota de evaluación continua puede sustituirse, cuando
favorezca al estudiante, por la ponderación entre la continua (40 %) y el examen final de la
convocatoria ordinaria (60 %).

Evaluación continua obligatoria, también para repetidores y estudiantes de intercambio. Los
parciales y trabajos no son liberatorios. Asistencia obligatoria: por debajo del 80 % se
pierde el derecho a examen en convocatoria ordinaria. Software declarado: Python y
herramientas de IA generativa.

## Alcance

**Solo regresión.** La clasificación se imparte en otra asignatura y no entra aquí.

Fuera del núcleo, por decisión de `PLAN_CURSO.md:58-68`: capítulo autónomo de convexidad,
capítulo autónomo de álgebra matricial, GLM como capítulo, inferencia sobre coeficientes,
intervalos conformes, teoría avanzada de optimización, ensambles y doble descenso como
materia evaluable.

## Los nueve capítulos

Secuencia: formular una distribución generadora, aprender una señal, evaluar fuera de
muestra, preparar datos sin fugas, aumentar y controlar la complejidad, comparar métodos
dentro de un flujo reproducible.

---

### 1 · Datos = señal + ruido  (2 semanas) · escrito

**Pregunta**: ¿qué intentamos aprender?
**Núcleo**: señal, ruido, sobreajuste por interpolación, distribución normal, modelo
lineal-gaussiano, distribución generadora, verosimilitud, log-verosimilitud, MLE por rejilla.
**Deja abierto**: la rejilla no escala con el número de parámetros.
**Datos**: sintéticos.

---

### 2 · Aprender minimizando  (2 semanas) · escrito, pendiente de reordenar

**Pregunta**: ¿cómo se convierten los datos en un problema de optimización?
**Núcleo**: pérdida, riesgo verdadero, riesgo empírico, MLE como minimización del riesgo,
derivadas parciales, gradiente, dirección de descenso, puntos críticos, descenso de
gradiente, tasa de aprendizaje, autodiferenciación, estimación de $\noise$.
**Deja abierto**: la recta tiene dos parámetros; con muchos hace falta notación matricial.
**Datos**: sintéticos, los mismos del capítulo 1.

---

### 3 · Modelos lineales con muchas variables  (2 semanas) · escrito

*Subtítulo del stub*: Matrices, gradientes y una implementación reutilizable.

**Pregunta**: ¿cómo generalizamos a muchas variables?
**Secciones fijadas por el stub**: de una recta a muchas características · la matriz de
diseño · predicciones, residuos y riesgo en forma matricial · el gradiente del riesgo
cuadrático · ajustar un modelo lineal · existencia, unicidad y colinealidad · una interfaz
común para entrenar modelos · caso con datos reales.
**Debe quedar demostrado**: gradiente $\frac{2}{\nobs}\Xt(\X\coef-\yv)$ por componentes y en
forma vectorial, verificado con autodiferenciación. Ecuaciones normales como solución
particular, no como centro. Rango y predicciones identificables con el mínimo aparato
algebraico.
**Datos**: primer caso real, `prostate.data`.
**Fuente**: `ml-notes-update-main/chapters/04-more-gradients.qmd`, íntegro y sin usar.
Especialmente reutilizables las dos identidades vectoriales ($\grad\norm{v}^2=2v$ y la
composición con una aplicación afín) y la verificación entrada a entrada con la delta de
Kronecker, que encaja con el nivel matemático del grupo.
**Apoyo**: `curso/algebra.qmd` tiene `lem-grad-lineal` y `lem-grad-cuadratica` demostrados y
anuncia que se usan en este capítulo. Hoy ningún capítulo los cita. Conviene citarlos.
**Deja abierto**: sabemos ajustar un modelo con muchas variables, pero hemos medido su
calidad sobre los mismos datos con los que lo hemos entrenado.

---

### 4 · Evaluar para generalizar  (2 semanas) · escrito, pendiente la hoja 4

*Subtítulo del stub*: Métricas, particiones y validación cruzada.

**Pregunta**: ¿cómo estimamos el rendimiento futuro sin engañarnos?
**Siete secciones de nivel 2, y este esqueleto lo fijó él en agosto de 2026**: el problema de la
generalización · las dos tareas (con `### Empezar por una referencia sencilla` dentro, que trae el
modelo nulo y monta los datos y el código) · **Tarea 1**, estimar el riesgo de un modelo ya
ajustado (con `sec-precision` dentro) · **Tarea 2**, elegir el mejor procedimiento entre $M$
alternativas (con `### Validación`, `### K-fold cross validation` = `sec-kfold` y
`### Comparar candidatos bloque a bloque` = `sec-comparar` dentro, y los dos `#### Cómo elegir
entre …` dentro de este último) · métricas de regresión · caso práctico · el protocolo
reproducible, `sec-protocolo` · más los ejercicios.
**El orden interno de `### Validación` es suyo y NO se toca**: el test es intocable → hay que
fraccionar $\Dtrain$ → validación simple, `def-particiones` y `fig-particiones` → ¿por qué no
entregar el modelo ya ajustado? → el reajuste con todo $\Dtrain$ → **de ahí** sale que el modelo
evaluado no es el entregado, y de ahí que lo que se compara son procedimientos, con
`def-riesgo-procedimiento` → qué estima la validación simple, con `exr-validacion-insesgada` → el
ideal con $P^\star$ conocida. **El riesgo del procedimiento tiene que aparecer empujado por el
reajuste, no antes.** En agosto de 2026 se probó a subirlo delante de la validación simple, para
resolver el To Do que pide poner el caso ideal primero, y él lo rechazó: "antes el riesgo del
procedimiento aparecía de forma natural, ahora no". Ese To Do sigue abierto a propósito, en la
línea 584; cualquier intento de cerrarlo tiene que dejar la llegada del concepto donde está.
**Los tres subconjuntos se llaman $\Dajuste$, $\Dval$ y $\Dtest$**, con
$\Dtrain=\Dajuste\cup\Dval$. Antes el de ajuste se escribía $\Dtrain\setminus\Dval$ y él lo
marcó como confuso; la macro `\Dajuste` existe por eso.
**Dos pasajes van en `.cajanegra`** porque son material avanzado y no evaluable: el límite de la
corrección de sesgo de K-fold y la no independencia de las $K$ diferencias emparejadas.
**Nada de subir K-fold ni la comparación emparejada a nivel 2**: son partes de la Tarea 2 y
sacarlas de ahí disuelve el esqueleto de dos tareas que el capítulo promete en su segunda
sección. Los títulos de las dos secciones centrales empiezan por `Tarea 1:` y `Tarea 2:`.
**Las métricas van entre `sec-comparar` y el caso práctico, y ahí hay que dejarlas.** Estuvieron
al final del capítulo y eso rompía el render: la celda del caso práctico llama a `metricas()`, que
se define en esa sección, y el paso 2 del protocolo cita `@def-metricas`. Si alguien las vuelve a
mover, `quarto render` falla con `NameError: name 'metricas' is not defined`.
**La introducción declara las dos tareas y el capítulo se estructura sobre ellas**, decisión suya
de agosto de 2026. La apertura dice qué quedó cerrado en los capítulos 1 a 3 (el ajuste: familia,
riesgo empírico, minimización), qué falta (el riesgo verdadero), y muestra el problema con las dos
cifras $0.4392$ y $0.5213$. Después, `## Las dos tareas de este capítulo` enuncia la tarea 1
(estimar el riesgo de un modelo ya ajustado) y la tarea 2 (elegir entre candidatos), declara el
esquema de cuatro pasos con que se resuelven las dos, y coloca lo que va antes (modelo nulo y
métricas) y lo que va al final (el protocolo). **Los títulos de las dos secciones centrales
nombran la tarea, no la respuesta**, y cada una abre con `**Tarea 1**:` / `**Tarea 2**:`. Fuera la
antigua agenda de "tres decisiones": la primera era un preliminar y las otras dos eran estas
tareas.
**Cada conjunto nace del error que lo justifica**: el capítulo resuelve dos tareas seguidas con el mismo esquema de cuatro pasos, **qué se
quiere estimar → por qué falla la forma directa → qué sería lo ideal y por qué no está disponible
→ cómo se hace en su lugar, con la demostración**. De la primera tarea, estimar el riesgo de un
modelo dado, sale $\Dtest$ (`def-train-test`, dos conjuntos). De la segunda, elegir entre
procedimientos, sale el tercero (`def-particiones`), que por eso vive **dentro** de
`sec-seleccionar`, detrás de `prp-minimo-sesgado` y del experimento, con `fig-particiones` y las
proporciones pegadas. **No subir `def-particiones` al principio del capítulo**: así estaba antes y
el conjunto de validación llegaba 355 líneas antes de su justificación. Los rótulos `###` de
`sec-seleccionar` (la opción ingenua · qué querríamos y por qué no se puede · cómo hacerlo bien)
hacen visible ese esquema; no quitarlos. Copia del capítulo anterior a la reordenación en
`_referencia/04-evaluacion-antes-de-reordenar.qmd`.
**La segunda mitad sigue una narrativa fijada por él en agosto de 2026, y hay que respetarla**:
un procedimiento produce un modelo y el test lo mide sin sesgo → con $N$ procedimientos la
opción ingenua elige por test → `prp-minimo-sesgado` dice por qué eso está sesgado y quema el
test → de ahí la necesidad de $\Dval$ → qué se estima para elegir, que es
$\Riskproc{\ntrain}$ de `def-riesgo-procedimiento` → cómo se estima, validación simple frente a
K-fold, con el sesgo y la precisión de cada una → el ruido de la estimación obliga a la regla de
un error típico → el protocolo de cinco pasos, con el resultado que justifica cada paso.
**Distinción dura de vocabulario**: "procedimiento" es lo que evalúa la validación cruzada y
"modelo concreto" lo que evalúa el test. No usar "modelo" para un candidato de la tabla.
**La cadena que justifica elegir por $\Riskproc{}$ está escrita entera en `sec-dos-preguntas` y
`sec-kfold`, y no hay que dejarla implícita**: lo que interesa es $\Risk(\modelh_{\Dtrain})$, el
riesgo del único modelo que se entrega; ese número no puede ser el criterio, porque estimarlo
exige datos ajenos al ajuste y el modelo entregado usa $\Dtrain$ entero, mientras que medirlo en
$\Dtest$ para los $N$ candidatos es la opción ingenua que `prp-minimo-sesgado` descarta; de ahí
la primera sustitución, del modelo concreto al procedimiento, que además promedia el azar del
ajuste; y de ahí la segunda, de $\Riskproc{\ntrain}$ a $\Riskproc{\ntrain(K-1)/K}$, que supone
que el orden de los candidatos no cambia con el tamaño de la muestra. Ese supuesto puede fallar,
y la razón está en el capítulo 6: el sesgo no se atenúa con $\nobs$ y la varianza sí, así que un
candidato flexible puede adelantar a uno rígido al crecer la muestra. Dicho sin metáforas: nada
de fábricas, actos de fe ni simulacros.
**Lo que NO hace**: no vuelve a explicar que el error de entrenamiento es optimista. Eso está
en el capítulo 1 (interpolador y `def-sobreajuste`), en el 2 (por qué lo es) y en el 3 (con
números: $0.2476$ frente a $0.2588$). Se citan los tres y se pasa a cómo se mide. Su
aportación propia es **el sesgo de selección**, que es otro fenómeno.
**Demostrado, tal como quedó tras la revisión**: `lem-media-optima` (la mejor constante es la
media), `thm-test-insesgado`, `prp-train-optimista` (la cadena
$\E{\Riskh_{\Dtrain}(\coefhat)}\leq\Risk(\coef^\star)\leq\E{\Risk(\coefhat)}$, que cierra
por fin lo que los capítulos 1 a 3 solo afirmaban), `prp-precision-test` (el error típico
$\noise^2\sqrt{2/\ntest}$, que decide el tamaño del test) y `prp-minimo-sesgado`. Definiciones:
`def-modelo-nulo`, `def-metricas`, `def-particiones`, `def-validacion-cruzada`,
`def-diferencia-emparejada`, `def-regla-un-error-tipico` y `def-riesgo-procedimiento`,
el riesgo esperado
$\Riskproc{\nobs}=\Esub{\data}{\Risk(\modelh_{\data})}$, que va en `sec-dos-preguntas` por una
razón concreta: el capítulo 6 usaba trece veces la expresión "riesgo esperado" sin que el curso
la hubiera definido, y su `eq-descomposicion-global` descompone exactamente esa cantidad. La
sección de K-fold justifica desde agosto de 2026 la elección entre validación simple y
validación cruzada con el sesgo y la precisión del estimador, y con la salvedad de que los $K$
bloques están correlacionados, que es lo que dice el apartado b de `exr-h4-cv-bloques` y lo que
explica que se usen 5 o 10 y no $K=\ntrain$. No quitar esa salvedad: sin ella el capítulo
contradice a su hoja.
$\RMSE\geq\MAE$ está planteado como ejercicio, `exr-rmse-mae`, por decisión suya: la
desigualdad no es central y la demostración cabe en un ejercicio.
**Once ejercicios incrustados**, seis de lápiz y papel dentro de las secciones y cinco de
laboratorio en la sección final. El último, `exr-regla-un-error-tipico`, guarda la entrega
alternativa: **el caso práctico entrega el candidato que elige la regla de un error típico**, el
de tres variables, y no el mínimo de la curva, que es el de cinco. Consecuencia que hay que
respetar: el riesgo en test del modelo entregado, $0.4428$, cae por debajo de su riesgo en train,
$0.6159$, y el capítulo lo explica en su sitio; no es un error que haya que arreglar. La hoja 4 los recoge y añade el resto.
**El orden dentro de la Tarea 1**: `prp-train-optimista` con su demostración (que se apoya en
`lem-esperanza-funcion`, **no** en `thm-test-insesgado`, porque el teorema viene después),
`thm-test-insesgado`, `def-train-test` (solo train y test), el
párrafo del reparto al azar, `thm-test-insesgado` con su demostración, el paso exacto de esa
demostración que falla en train, `prp-train-optimista`, y solo entonces `### Con qué precisión se
mide`, `sec-precision`. La antigua `### La variabilidad del propio corte` ya no existe: la
reestructuración de agosto de 2026 movió su contenido, las dos fuentes de variabilidad, a
`sec-dos-preguntas`, donde sirve para motivar `def-riesgo-procedimiento`. No restaurarla.
**`thm-test-insesgado` está enunciado para una muestra genérica $\data'$** de tamaño $\nobs'$
fijada sin mirarla, no solo para $\Dtest$, porque el capítulo lo aplica cuatro veces: a
$\Dtest$, a $\Dval$, a los bloques de la validación cruzada y, por contraste, a $\Dtrain$, donde
falla. Si se vuelve a estrechar el enunciado, tres de esas aplicaciones quedan sin justificar.
**Macros que estrena**: `\Dtrain`, `\Dval`, `\Dtest`, `\fold{k}`, `\CV`, `\nullmodel`,
`\MAE`, `\RMSE`, `\Rsq`. Se dice **train** y **test**, no prueba.
**Cita del capítulo 2**: el suelo de ruido $\noise^2$, en la sección de métricas, para
responder a qué es un RMSE bueno. Es una cita, no la descomposición.
**Datos**: `prostate.data`.
**Fuente**: casi nada. De Chodrow solo la línea base (`06-regularization.qmd:739-755`), que
se anticipa aquí desde el capítulo de regularización. No tiene validación cruzada, ni métricas
de regresión, ni fugas. **Se escribe de cero**, con ESL como apoyo bibliográfico.
**La sección `sec-comparar`, "Comparar candidatos"**, es la dueña
del emparejamiento en todo el libro, y la citan los capítulos 5 a 9. Es deliberadamente práctica:
el número que sale mal al no emparejar, la figura, `def-diferencia-emparejada` y
`def-regla-un-error-tipico`, con su tabla. **La regla es una definición con etiqueta desde
agosto de 2026**, y todas las citas del libro apuntan a ella (capítulos 5 y 6, hoja 6); antes
apuntaban a `@sec-comparar`, que es la sección y no el resultado. Al citarla no escribir "la
regla de un error típico de @sec-comparar". **Nada de teoría de la varianza de una
diferencia**: se probó con la identidad, la covarianza y un contraejemplo, y el autor lo cortó por
excesivo. Dos reglas duras de su diseño: no toca el test, porque va antes del paso 5 del
protocolo, y no entra en contrastes ni en valores p.

**Dos matices del caso práctico que están verificados y no hay que "arreglar"**: los candidatos
de 1 y 2 variables quedan a un cociente de $1.04$, que la columna redondea a $1.0$, así que la
regla los descarta justo en el límite; y con `semilla=0` en el reparto en bloques entran los dos
y la regla entregaría el candidato de una sola variable (barrido de semillas: entrega 1, 5, 1, 5,
4, 3 y 5 con las semillas 0, 1, 2, 3, 7, 42 y 123). La comparación final con el modelo nulo,
$-0.6139\pm0.3092$, da un cociente de $1.98$, justo por debajo del umbral de $2$ que el propio
capítulo fija para dos candidatos, y el texto lo dice así.

**Cifras del capítulo, para que el 5 las pueda citar**: partición 67/30 de `prostate.data`,
riesgo de entrenamiento $0.4392$ frente a $0.5213$ de test; modelo nulo $1.0567$ en test;
$\Rsq$ de test $-0.0068$ para el nulo; error típico de la estimación de test $\pm0.1787$; el
experimento de selección con 2000 repeticiones, donde la validación del elegido baja de
$1.084$ a $0.956$ y cruza el suelo de ruido $\noise^2=1$ mientras su test se queda en
$1.078$-$1.095$; y el protocolo final, tres variables entregadas por la regla de un error
típico, $0.4428\pm0.1136$ en test frente a $0.5213$ con las ocho.
**Deja abierto**, con las palabras del cierre: el protocolo es honesto sobre una tabla de
números limpia, donde lo único que se aprende de los datos son los coeficientes. En una tabla
real hay que imputar, escalar y codificar, y esas transformaciones se aprenden también de los
datos: si se aprenden antes de separar, el test deja de ser test.

---

### 5 · Preparar datos sin contaminar la evaluación  (2 semanas) · tercera versión, con hoja 5

*Subtítulo del stub*: Exploración, transformaciones y pipelines reproducibles.

**Pregunta**: ¿qué transformaciones forman parte del modelo?
**Secciones (6)**: los datos crudos y los problemas que traen · un tratamiento para cada
problema, con cinco subsecciones · los parámetros de un tratamiento son parámetros del modelo ·
el pipeline reúne los tratamientos y el modelo · cuando las filas no son independientes · caso
práctico de principio a fin.

**Hubo tres versiones y las dos primeras las rechazó.** La segunda cayó por falta de sistema: al
haberla acortado por petición suya, cada tratamiento se explicaba de una forma distinta y varios
quedaban en una frase. Lo que pidió, y que hay que aplicar a cualquier capítulo aplicado, es un
**esquema fijo por problema**, repetido literalmente en las cinco subsecciones:

1. qué es el problema, con definición general y no atada a estos datos;
2. qué daño hace, es decir, qué operación del capítulo 3 deja de funcionar o se degrada;
3. qué tratamientos existen, en tabla, y de qué depende elegir entre ellos;
4. cómo se implementa en `scikit-learn`, nombrando la clase y sus argumentos;
5. qué sale sobre nuestros datos.

La repetición del molde es deliberada: es lo que convierte cinco temas sueltos en un método.
También pidió **el problema enumerado antes del tratamiento** y **más de una solución por
problema**, incluida una para la alta cardinalidad, que la versión anterior mencionaba sin
resolver.

**La primera versión estaba mal ordenada y él la rechazó entera.** El error, y hay que no
repetirlo: presentaba la regla (separar antes de transformar, fuga de información) **antes** de
presentar las transformaciones que la regla gobierna, de modo que la sección de la fuga hablaba
de escalado, imputación y codificación sin haberlos definido, y usaba `Pipeline` y la
distinción numéricas/categóricas doscientas líneas antes de introducirlas. Es el no negociable
número 6 de la skill, incumplido cuatro veces en el mismo capítulo.

**El orden que funciona**, con la prueba de la regla de orden pasada sección a sección:

| Sección | Hasta aquí sabemos | Nos falta |
|---|---|---|
| 1 | ajustar y evaluar sobre una tabla de números | una tabla real, y qué hay que arreglar en ella |
| 2 | qué problemas tiene la tabla | resolver cada uno |
| 3 | cómo se hace cada transformación | con qué datos se estiman sus parámetros |
| 4 | la regla, y que a mano se incumple | un objeto que la cumpla por construcción |
| 5 | un pipeline correcto sobre filas intercambiables | qué pasa si las filas se agrupan |
| 6 | todas las piezas | encadenarlas con el protocolo del capítulo 4 |

Dos decisiones que sostienen ese orden. **El reparto se hace al final de la sección 1**, citando
el paso 1 del protocolo del capítulo 4, que ya lo pedía: así la sección 2 puede estimar cada
transformación con `train` sin necesitar todavía la teoría de la fuga, y no hay ninguna
referencia hacia delante. Y **la sección 3 se queda con lo genuinamente nuevo**, que es que los
parámetros de una transformación cuentan como parámetros del modelo, cosa que el capítulo 4 no
dijo; llega cuando el lector ya sabe cuáles son esos parámetros.
**Cambios respecto al plan antiguo**: recibe del capítulo 4 la sección de **grupos y series
temporales**, porque la dependencia entre filas es una fuga más y los grupos viven en
`host_id`; y **transformar la respuesta** pasa al bloque de ampliación de su hoja.
**Debe quedar demostrado**: que imputar por la media contrae la varianza, la trampa de la
variable ficticia como resultado de rango (cita `@lem-norma-cero` del repaso de álgebra), y
que tomar logaritmos cambia el modelo de ruido.
**Cierra una promesa del capítulo 3**: escalar las columnas endereza el descenso.
**Datos**: `airbnb_madrid.csv`, que por sí solo cubre casi todo el capítulo. Ausencias con
estructura (`bedrooms` 22,7 %, `review_scores_rating` 13,7 % y no al azar, porque falta
cuando no hay reseñas), categóricas de baja cardinalidad (`room_type`, 4) y de alta
(`neighbourhood_cleansed`, 127), extremos (`beds` hasta 167), y objetivo `price` muy
asimétrico. Grupos: `host_id`, 5.622 valores.
**Fuente**: nada en Chodrow. Lo que sí tiene son **dos antipatrones documentables**: aplica
`pd.get_dummies` al dataframe completo antes de partir, en `06-regularization.qmd:689` y en
`12-decision-theory.qmd:188`. Sirven de material para el bloque D.
**Este capítulo produce el pipeline canónico** que reutilizan los capítulos 6 a 9.
**Aviso de calendario**: la S3 de la semana 9 es el taller de agentes, así que el capítulo
tiene tres laboratorios y no cuatro. **Su caso práctico es el material de ese taller**:
construir el pipeline es justo lo que se supervisa a un agente, y el proyecto exige bitácora.
**Deja abierto**, con las palabras del cierre: ya hay una matriz de diseño construida a partir
de una tabla real sin que ninguna decisión haya mirado el test, y a la vez un modelo claramente
insuficiente. La causa no está en la preparación de los datos sino en la clase de hipótesis,
porque seguimos suponiendo que el precio crece de forma proporcional a cada variable y sin
interacción entre ellas.

**Demostrado, tal como quedó escrito**: `cor-fuga-rompe-test` (una línea, es la hipótesis
de `thm-test-insesgado` incumplida), `prp-imputacion-contrae-varianza` (la varianza queda
multiplicada por **exactamente** $m/\nobs$, lo que hace el resultado comprobable con dos
líneas de código), `prp-log-mediana` y `prp-trampa-ficticia`. Definiciones: `def-fuga`,
`def-imputacion`.
**Desviación de la ficha**: `prp-trampa-ficticia` **no** cita `@lem-norma-cero`, porque exhibir
el vector del núcleo es directo y meter el lema sería relleno. En su lugar el capítulo estrena
`def-cuantil` y `lem-cuantil-creciente`, que se han sacado del `.sinusar` del repaso de
probabilidad y ahora tienen etiqueta propia y demostración; los cita `prp-log-mediana`.
**Cifras del capítulo, para que el 6 las pueda citar**: reparto por anfitrión al 25 %, train
11216 anuncios de 4216 anfitriones y test 3784 de 1406, sin anfitriones compartidos. Modelo
nulo en test RMSE $107.38$ euros; el entregado, ocho numéricas más `room_type` y distrito, 36
columnas, test $6948.7\pm592.1$ y RMSE $83.36$ euros. CV(5) por grupos: nulo $13742$, solo
numéricas $8137$, más `room_type` $7915$, más distrito $7569$, más barrio $7637$, con errores
típicos entre bloques de unos $600$.
**El experimento que hay que conservar** es el de la sección de grupos: sin variable de
anfitrión los dos repartos son indistinguibles ($+273\pm260$), y con el precio medio del
anfitrión se separan un 24 % ($+1457\pm263$). Es lo que impide dar la regla simplista de
repartir siempre por grupos sin decir de qué depende.

---

### 6 · Complejidad, sesgo y varianza  (2 semanas) · escrito, con hoja 6 y solucionario

*Subtítulo del stub*: Aprender curvas y entender lo que cuestan.

**Es la fusión de los antiguos capítulos 6 y 7.** El motivo es que los dos contaban el mismo
fenómeno: el 6 dibujaba la curva en U de la validación y el 7 la explicaba, en capítulos
distintos y con una semana de separación. Fusionados, la curva se dibuja una vez y se lee con
la descomposición.

**Pregunta**: ¿cómo aprende curvas un modelo lineal, y qué se paga por ello?
**Secciones (6)**: la representación decide qué se puede aprender (con `def-mapa-caracteristicas`
y `prp-todo-sirve` dentro) · características polinómicas e interacciones · un algoritmo produce
modelos distintos con muestras distintas · la descomposición sesgo-varianza · la curva en U y lo
que la validación cruzada logra ver · caso práctico.
**Las curvas de aprendizaje no están en el cuerpo**, por decisión suya: borró la figura y su
celda al revisar. Viven en `exr-h6-curvas-aprendizaje` de la hoja. No reintroducirlas.
**La muestra simulada tiene 36 observaciones y la partición es `semilla=9`.** Las dos cosas se
fijaron en agosto de 2026, y por este orden: primero se vio que el capítulo afirmaba sin
comprobarlo que la regla de un error típico entregaba el grado 3 cuando con `semilla=42` entregaba
el 6, y después él pidió subir el tamaño de muestra para que la estimación de validación cruzada
se acercara al riesgo esperado. Con 30 observaciones el campeón se equivocaba por un factor de
veinte; con 36 el factor baja a quince, el mínimo del riesgo esperado sigue en el grado 3
($0.0512$) y la varianza del grado 9 pasa de $10.8390$ a $3.1114$, que es el precio: la rama
derecha es menos espectacular. **No subir más de 36**: con 50 o 60 el mínimo se va al grado 5 y
con 40 el campeón ya acierta, y en los dos casos el capítulo pierde su lección.
**La regla se ejecuta, no se afirma.** El capítulo imprime la tabla de cocientes contra el
campeón, que es el grado 8, y el grado que la regla entrega, que es el 3. La celda mide además
qué entrega en cuarenta particiones distintas de las mismas treinta y seis observaciones: el
grado 3 en 27, el grado 4 en 10 y un grado más alto en 3. Esa cuenta sostiene la salvedad de que
la regla es una heurística sin garantía; no quitarla.
**Las bases locales no están en el cuerpo**, por decisión suya de agosto de 2026: el capítulo ya
era demasiado y se quedaron en `exr-base-local`. No volver a explicarlas en el texto.
**El caso práctico es el experimento simulado con los datos del capítulo 5**, también por
decisión suya: una única función `pipeline_polinomio(grado)` y cuatro candidatos, grado 1 (que es
el modelo entregado allí), grado 2, grado 4 y grado 2 sin el recorte al percentil 99. Nada de
cruces a mano; el cruce con el tipo de habitación es `exr-interacciones-dirigidas`.
**Idea central**: $\model_{\coef}(\xv)=\coef\T\boldsymbol\varphi(\xv)$ es no lineal en la
entrada y lineal en los parámetros, de modo que toda la maquinaria del capítulo 3 sirve
sustituyendo $\X$ por $\Phimat$.
**Su descomposición es la de `def-riesgo-procedimiento`** del capítulo 4: el lado izquierdo de
`eq-descomposicion-global` es $\Riskproc{\nobs}$, y la primera vez que el capítulo dice "riesgo
esperado" lo cita.
**Debe quedar demostrado**: la descomposición del error cuadrático en un punto, con álgebra
elemental. Cita `@lem-esperanza-total` del repaso de probabilidad, que hoy está marcado como
sin usar y deja de estarlo aquí.
**Cierra una promesa del capítulo 2**: aquí se mide el suelo $\noise^2$ que allí se anunció.
**Antes de escribirlo hay que decidir la macro del vector de características**: `\basis` está
definida como escalar y el capítulo necesita el vector y sus componentes. Es una modificación
del contrato y la decide el autor. Ver `contrato-notacion.md`.
**Macros que estrena**: `\basis`, `\Phimat`, `\Esub` (la esperanza con subíndice: `\E` toma un
argumento y se come el `_`, así que `\E_{\data}[\cdot]` no compila y hay que escribir
`\Esub{\data}{\cdot}`).
**Fuente**: `ml-notes-update-main/chapters/06-regularization.qmd:106-397` para la parte de
características, con sus dos rejillas 2x3 que recorren de subajuste a sobreajuste, y
`07-bias-variance.qmd` íntegro para la descomposición, incluida su demostración completa. Su
experimento de Monte Carlo con 1.000 ajustes usa solución cerrada (`torch.linalg.lstsq`), no
descenso, y hay que conservar esa decisión por coste.
**Aviso**: el doble descenso va en `::: {.cajanegra}` y no es evaluable.
**Datos**: simulados con señal curva conocida (el generador de `estilo-codigo.md`), más uno de
los dos conjuntos del curso para el caso práctico.
**Deja abierto**: sabemos que la varianza crece con la complejidad, pero no tenemos ningún
mecanismo para reducirla sin renunciar a la flexibilidad. Hasta ahora la única forma de bajarla
ha sido quitar características, es decir, volver a una clase más pequeña.

**Escrito con 7 secciones y no con las 10 del stub**, y la reducción se acordó por la petición
suya de acortar el bloque. Las fusiones: *la representación* y *mapas de características* van
juntas, porque la segunda es la herramienta que resuelve el problema que plantea la primera;
*funciones de base locales* es media sección dentro de las características, con su figura;
*descomposición* y *ruido irreducible* van juntas, porque el ruido es uno de los tres términos
de la descomposición y separarlo era artificial; y *curvas de aprendizaje* va con la curva en U.

**Decisión de notación tomada aquí**, la que la ficha dejaba al autor: `\basis` sigue siendo la
característica escalar con subíndice, y se añaden `\basisv` para el vector y `\nbasis` para su
dimensión. Está en `contrato-notacion.md`.
**Corrección del generador canónico**: la señal es $\sin(\pi x)$ y no $\sin(2\pi x)$. Con dos
periodos completos la curva del riesgo sale dentada por la simetría de la señal y no se puede
leer. Documentado en `estilo-codigo.md` con las cifras.
**Cifras del capítulo**: suelo $\noise^2=0.04$; la mejor recta posible tiene riesgo $0.2364$,
casi seis veces el suelo, y con $\nobs=30$ ya se está a un 19 % de ese límite. Descomposición
con $\nobs=30$: mínimo del riesgo esperado en grado 3 con $0.0527$, sesgo$^2$ de $0.4988$ en
grado 0 y varianza de $22.39$ en grado 9. La validación cruzada sobre una sola muestra elige el
grado 7, cuyo riesgo esperado es $1.5362$ frente a $0.0527$ del grado 3: es
`prp-minimo-sesgado` otra vez, y la regla del capítulo 5 de preferir el simple ante un empate
lleva a la respuesta correcta. Curvas de aprendizaje: el grado 1 se aplana en $0.239$ y el
grado 9 baja de $82751$ a $0.0409$.
**Caso práctico**: sobre `airbnb_madrid.csv`, el cuadrado de las variables de tamaño empeora la
estimación de $7568.6$ a $9669.6$, y el cruce de tamaño con tipo de habitación la mejora a
$7269.9$; test $6619.4\pm576.0$, RMSE $81.36$ euros frente a $83.36$ del lineal. La mejora está
dentro del ruido y el capítulo lo dice.

---

### 7 · Regularización  (1 semana) · semana 13

*Subtítulo del stub*: Controlar la complejidad mediante penalizaciones.

**Pregunta**: ¿cómo restringimos modelos flexibles?
**Secciones (6)**: del riesgo empírico al riesgo penalizado · ridge · lasso · el parámetro de
regularización · elegir lambda con validación cruzada · caso práctico.
**Recortes respecto al plan antiguo**: *por qué la escala importa* se funde con ridge, y
*regularización y selección de variables* se cede al capítulo 8, que trata de eso.
**Macros que estrena**: `\reg`, `\coefridge`, `\coefols`, `\pos{}`, `\softthr`.
**Aviso obligatorio**: $\reg$ es $\lambda$ en las matemáticas y `alpha=` en scikit-learn,
mientras que $\lr$ es $\alpha$. Hay que declararlo en el texto.
**Fuente**: `06-regularization.qmd:399-643`. Reutilizables la figura de la geometría de las
penalizaciones (círculos frente a rombo, con el minimizador cayendo sobre un eje) y las dos
figuras con trayectorias de coeficientes. **Hay que sustituir su validación única por
validación cruzada**, para ser coherente con el capítulo 4, y excluir el intercepto de la
penalización como él hace. El caso bikeshare de `:644-917` se cede a la guía del proyecto.
**Datos**: `prostate.data`, que es el caso canónico para ridge y lasso.
**Aviso de calendario**: la semana 13 es la de la entrega y defensa del proyecto.
**Deja abierto**: la penalización controla la complejidad y de paso anula coeficientes, pero
no hemos decidido qué variables conservar o construir.

---

### 8 · Selección de variables y reducción de dimensión  (1 semana) · semana 14

*Subtítulo del stub*: Elegir o construir representaciones de menor dimensión.

**Pregunta**: ¿qué variables conservamos o construimos?
**Secciones fijadas por el stub**: dos objetivos diferentes · estrategias de selección de
variables · componentes principales · varianza explicada y número de componentes · escalado y
fuga de información · regresión sobre componentes principales · qué se gana y qué se pierde.
**Recibe del capítulo 7**: qué selección produce el lasso, cuándo es inestable y por qué cero
no equivale a irrelevancia.
**Aviso conceptual del stub**: la varianza explicada describe $\X$ y no garantiza capacidad
predictiva sobre $\yv$. Evitar presentar PCA como limpieza universal.
**Fuente**: **PCA se escribe de cero**. Chodrow no lo trata. Apoyo bibliográfico: Deisenroth,
Faisal y Ong, y ESL capítulo 14.
**Nivel**: motivación geométrica primero, centrado y producto matriz por vector, y SVD solo lo
imprescindible. El repaso de álgebra **no** tiene SVD; si se necesita, hay que añadirlo allí.
**Datos**: `prostate.data` para la selección con pocas variables y `airbnb_madrid.csv` para la
dimensión alta que aparece al codificar las categóricas.
**Aviso de calendario**: la S3 de la semana 14 es el segundo taller de agentes, así que este
capítulo se queda sin laboratorio propio. Su parte práctica tiene que caber en la S2 o en el
trabajo autónomo.
**Deja abierto**: todos los modelos vistos son una fórmula global sobre alguna representación;
falta ver qué ocurre cuando la señal tiene umbrales e interacciones.

---

### 9 · Árboles de regresión  (1 semana) · semana 15, compartida con el repaso

*Subtítulo del stub*: Predicción mediante particiones y reglas.

**Pregunta**: ¿cómo aprendemos reglas en lugar de una fórmula global?
**Secciones fijadas por el stub**: de una fórmula global a reglas locales · predicción dentro
de una hoja · elegir una división · construcción voraz del árbol · controlar la complejidad ·
seleccionar el árbol con validación · modelos lineales y árboles aprenden señales distintas ·
más allá de un árbol.
**Debe quedar demostrado**: que la media minimiza el error cuadrático dentro de cada región.
Es una demostración de tres líneas y es el resultado evaluable del capítulo.
**Cálculo a mano**: elegir la primera división de un conjunto pequeño, para el bloque C.
**Fuera de alcance declarado**: bagging, bosques aleatorios y boosting se mencionan en un mapa
breve y no se desarrollan.
**Fuente**: **nada**. Chodrow excluye árboles explícitamente en su `index.qmd`. ESL capítulo 9
e ISLR capítulo 8.
**Datos**: `airbnb_madrid.csv`, donde hay umbrales e interacciones naturales, más una tabla de
seis u ocho filas para el cálculo a mano del bloque C.
**Aviso de calendario**: comparte la semana 15 con el simulacro del examen final, así que es
el capítulo más corto del curso. El mapa ya pedía "árbol de regresión breve".

---

### `curso/proyecto.qmd` · sin semana asignada

No es un capítulo. Es la guía del proyecto (semanas 10 a 13, 20 % de la nota) y el cierre del
curso, y se usa en el repaso de la semana 15. Era el antiguo capítulo 11.

**Contenido**: formular el problema antes de abrir los datos · auditar los datos y fijar el
protocolo · construir candidatos reproducibles · comparar sin utilizar el test · reajustar y
evaluar una sola vez · analizar los errores · comunicar y reproducir · agentes de IA como
ayuda de implementación · estado del arte y qué queda fuera.
**No introduce materia nueva.** Encadena sobre un caso propio las decisiones que los capítulos
han tomado de una en una, y es el índice del informe que hay que entregar.
**Epígrafes oficiales que cubre**, y esto hay que mantenerlo cierto en
la trazabilidad retirada: "T1 · Estado del arte", "T4 · Casos de uso y aplicaciones" y el
complemento sobre agentes de IA, este último junto con los talleres de las semanas 9 y 14 y
la política de uso de IA, retirada del repositorio.
**Fuente**: el caso bikeshare de `06-regularization.qmd:644-917`, cedido por el capítulo de
regularización, sirve de esqueleto, con dos correcciones obligatorias: quitar la fuga del
`get_dummies` previo a la partición y sustituir la validación única por validación cruzada.

---

## Conjuntos de datos

Dos, y solo se añade un tercero si ninguno de los dos permite mostrar limpiamente el
fenómeno. Nada de un dataset por capítulo.

### `datos/prostate.data`

97 filas, 11 columnas, separado por comas. Cabecera:
`index,lcavol,lweight,age,lbph,svi,lcp,gleason,pgg45,lpsa,train`. De *The Elements of
Statistical Learning*.

- Objetivo: `lpsa`.
- `train` es `T` o `F`, no un booleano de pandas. Hay que convertirlo.
- `pgg45` viene con espacios de relleno delante del número.
- `svi` binaria 0/1, `gleason` ordinal de 6 a 9, el resto continuas y varias ya en logaritmo.
- Papel: hilo conductor de los capítulos 3, 4 y 8. Colinealidad moderada con $\nfeat\approx8$
  y $\nobs=97$.

### `datos/airbnb_madrid.csv`

15.000 filas, 17 columnas. Inside Airbnb, instantánea 2026-06-20, CC BY 4.0, filtrado a
precios entre 10 y 1000, muestreado con `random_state=42`.

| Columna | Interés docente |
|---|---|
| `price` | objetivo, muy asimétrico a la derecha (media 151, mediana 124, máximo 991) |
| `host_id` | variable de grupo, 5.622 valores, para particiones por grupos |
| `neighbourhood_group_cleansed` | 21 distritos, categórica de baja cardinalidad |
| `neighbourhood_cleansed` | 127 barrios, alta cardinalidad |
| `property_type` | 51 valores con cola larga |
| `room_type` | 4 valores |
| `bedrooms` | 22,7 % ausente, máximo 50 |
| `bathrooms` | 11,0 % ausente |
| `beds` | 6,7 % ausente, máximo 167 |
| `review_scores_rating` | 13,7 % ausente y **no al azar**: falta cuando no hay reseñas |
| `minimum_nights` | numérica, 1 ausente, máximo 365 |
| `accommodates`, `number_of_reviews`, `availability_365` | numéricas sin ausentes |
| `id` | identificador del anuncio, único por fila. Nunca es una característica |
| `latitude`, `longitude` | geográficas |

Papel: capítulos 5, 9 y 11, y el proyecto.

## Bibliografía oficial

Orden de la guía docente: Bishop, *Pattern Recognition and Machine Learning* · Giussani,
*Applied Machine Learning with Python* · Deisenroth, Faisal y Ong, *Mathematics for Machine
Learning* · Boehmke y Greenwell, *Hands-On Machine Learning* (que es de R, y la guía docente
lo advierte) · Hastie, Tibshirani y Friedman, *Elements of Statistical Learning*.

En `referencias.bib` hay clave para Hastie (`hastie2009elements`) y para Deisenroth
(`deisenroth2020mathematics`). **`bishop2023deep` no es el Bishop de la guía oficial**: es
*Deep Learning: Foundations and Concepts*, de Bishop y Bishop, que la guía docente lista
como bibliografía complementaria. No hay clave para *Pattern Recognition and Machine
Learning*, ni para Giussani, ni para Boehmke y Greenwell. Si se citan, hay que crearla.
