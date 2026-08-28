# Estilo de código

## Reparto de herramientas

`PLAN_CURSO.md:95` lo fija: **PyTorch para optimización, scikit-learn para flujos de
trabajo**. En la práctica:

| Tarea | Herramienta |
|---|---|
| Definir un modelo, una pérdida, un gradiente, un bucle de entrenamiento | PyTorch |
| Comprobar una derivación analítica | `backward()` de PyTorch |
| Particiones, validación cruzada, métricas, pipelines, preprocesado | scikit-learn |
| Manipulación tabular | pandas |
| Figuras | matplotlib, con `import style` |

Nada de escribir a mano lo que scikit-learn ya hace bien (particiones, codificación,
escalado), y nada de usar scikit-learn para esconder lo que el capítulo está enseñando (un
descenso de gradiente que el estudiante tiene que ver).

Disponible en el entorno `aap`: torch 2.13, scikit-learn 1.9, pandas 3.0.5, numpy 2.5.2,
matplotlib 3.11.1, scipy 1.18, statsmodels 0.14. **No hay seaborn ni graphviz.** Si un
capítulo los necesita, se dice y se añade a `environment.yml` antes.

## Nombres

**La API va en inglés; el resto, en español.** Las clases, sus métodos y las funciones que
forman la interfaz del curso se escriben en inglés, porque son los nombres que el estudiante
va a reconocer en PyTorch y en scikit-learn:

| Pieza | Nombre |
|---|---|
| clase del modelo | `LinearRegression`, con método `predict` |
| pérdida | `mse` |
| gradiente analítico | `grad_mse` |
| optimizadores | `GradientDescentOptimizer`, `AutogradOptimizer`, `SGDOptimizer`, con método `step` |
| bucle de entrenamiento | `train` |
| ajuste en forma cerrada | `fit(modelo, X, y)` |

`LinearRegression` y `predict` coinciden a propósito con los de scikit-learn, y `step` con el
de `torch.optim`: la interfaz del curso imita la de las bibliotecas, y conviene decirlo en el
texto la primera vez que aparece.

**Todo lo demás va en español y sin tildes**, incluidos los parámetros de esas funciones y las
variables locales. Del corpus: `senal`, `ruido`, `prediccion`, `densidad_normal`, `modelo`,
`optimizador`, `residuos`, `historia_riesgo`, `historia_w`, `w_verdadero`, `n_parametros`,
`mejores_coeficientes`, `mejor_loglik`, `sigma_supuesto`, `w_inicial`, `soporte`, `muestras`,
`kw_puntos`, `dibuja_normal_vertical`.

Las excepciones son los nombres que vienen de la biblioteca (`lr`, `n_iter`,
`torch.manual_seed`) y los símbolos matemáticos de una letra cuando corresponden a la fórmula
que se acaba de escribir (`x`, `y`, `w`, `n`, `X`).

Antes de esta regla el curso usaba `RegresionLineal`, `predecir`, `riesgo_cuadratico`,
`gradiente_riesgo`, `DescensoGradiente`, `paso` y `entrenar`. Si alguno aparece en un fichero,
es que quedó sin renombrar.

**El código usa los mismos nombres que las matemáticas.** La pérdida se llama `mse` porque
la notación la llama $\MSE$, y no `loss`. Si la fórmula habla de $\residi$, la variable es
`residuos` y no `r`.

## La API de modelos, pérdidas y optimizadores

Nace en el capítulo 2 y sobrevive sin cambios de firma hasta el 8. Tres piezas y un bucle
fuera de ellas.

    class LinearRegression:
        def __init__(self, n_parametros=2):
            self.w = torch.zeros(n_parametros)

        def predict(self, x):
            ...

    def mse(y_pred, y):
        return ((y_pred - y) ** 2).mean()

    class GradientDescentOptimizer:
        def __init__(self, modelo, lr):
            self.modelo = modelo
            self.lr = lr

        def step(self, x, y):
            ...

Invariantes que no se rompen:

1. El modelo posee los parámetros en **un único vector `w`** y expone `predict`. Chodrow
   empieza con `w0` y `w1` sueltos y los junta un capítulo después; aquí no, para que el
   paso a muchas variables no obligue a reescribir la clase.
2. La pérdida es una **función libre** `(y_pred, y) -> escalar`. No conoce el modelo, así que
   se puede cambiar sin tocar nada más.
3. El optimizador guarda el modelo y la tasa, y expone `step(x, y)`, que **muta** los
   parámetros del modelo. La firma no cambia al pasar a autodiferenciación: lo único que
   cambia es cómo se obtiene el gradiente dentro de `step`.
4. El bucle de entrenamiento y el historial viven **fuera** de las clases.

Cómo crece: en el capítulo 3, `predict` pasa a `X @ self.w` y el resto queda igual; en el 4
aparece `fit(modelo, X, y)`, que resuelve las ecuaciones normales con `torch.linalg.lstsq` y
devuelve el modelo mutado, para que el capítulo pueda reajustar sin repetir el bucle de
descenso; en el 6 la matriz de características sustituye a la de diseño; en el 7 se suma un
término de penalización a la pérdida.

`fit` es una función libre y no un método, igual que `mse`, porque el capítulo 4 necesita
reajustar el mismo modelo sobre particiones distintas y conviene que el verbo aparezca en la
llamada. Su firma es `(modelo, X, y) -> modelo`.

## El pipeline canónico, del capítulo 5 en adelante

A partir del capítulo 5 el modelo **es** un `Pipeline` de `scikit-learn`, transformaciones
incluidas, y la interfaz manual de los capítulos 2 a 4 deja de usarse para los casos con datos
reales. La función que lo construye se llama `modelo_completo` y su firma es
`(categoricas, numericas) -> Pipeline`:

    Pipeline([("preparar", ColumnTransformer([
                  ("num", Pipeline([("imputar", SimpleImputer(strategy="median",
                                                              add_indicator=True)),
                                    ("escalar", StandardScaler())]), numericas),
                  ("cat", OneHotEncoder(drop="first", handle_unknown="ignore",
                                        sparse_output=False), categoricas)])),
              ("modelo", LinearRegression())])

Cuatro detalles que no son opcionales y que conviene no volver a decidir:

- **`drop="first"`** en el codificador, por `prp-trampa-ficticia`: sin él la matriz de diseño no
  tiene rango completo.
- **`handle_unknown="ignore"`**, porque hay categorías que solo aparecen en test y porque dentro
  de la validación cruzada ocurre en cada bloque. Con 127 barrios el aviso de `scikit-learn`
  aparece en la salida, y el capítulo lo silencia con `warnings.simplefilter` y una nota que
  explica por qué.
- **`add_indicator=True`**, porque la ausencia lleva información: en `airbnb_madrid.csv` los
  anuncios sin `bedrooms` cuestan la mitad.
- **Imputar antes de escalar**. `StandardScaler` no admite ausentes, así que el orden inverso
  falla.

`scikit-learn` se presenta al final del capítulo 3, en `### La misma interfaz en scikit-learn`,
comprobando que reproduce los coeficientes exactos con `fit_intercept=False`. Antes de ese punto
no se menciona por su nombre.

Los repartos con grupos van con `GroupShuffleSplit` para el reparto exterior y `GroupKFold`
para los bloques, los dos con `groups=`. Usar `KFold` cuando hay grupos es uno de los errores
del bloque D de la hoja 5.

## El ejemplo sintético canónico

Hay **dos** generadores lineales, uno por capítulo, y cada capítulo que los use **los
regenera** para que su cuaderno se ejecute solo. La diferencia está en el centrado de la
entrada, y no es cosmética.

El del **capítulo 1**, con la entrada en $[0,10]$:

    import torch
    from matplotlib import pyplot as plt

    torch.manual_seed(42)

    n = 20
    x = torch.linspace(0, 10, n)
    senal = 2 * x + 1
    ruido = 3 * torch.randn(n)
    y = senal + ruido

    kw_puntos = dict(color="black", facecolors="none", s=40, alpha=0.65)

El del **capítulo 2**, con la entrada centrada:

    torch.manual_seed(42)

    n = 40
    x = torch.linspace(-2, 2, n)
    senal = 1 + 2 * x
    ruido = torch.randn(n)          # nivel de ruido sigma = 1
    y = senal + ruido

El motivo del segundo es geométrico. Con la entrada en $[0,10]$ la hessiana del riesgo tiene
número de condición 133, de modo que las curvas de nivel son una elipse de razón de ejes 11
a 1: la tasa de aprendizaje que converge es como mucho 0.029, hacen falta cientos de
iteraciones y la trayectoria del descenso es una L en la que casi ningún paso se distingue.
Con la entrada centrada la condición baja a 1.4, las curvas de nivel son casi
circunferencias y el descenso llega al mínimo en unas veinte iteraciones. El capítulo 2 mira
mucho la forma del criterio, así que necesita la segunda; el capítulo 1 no dibuja el plano
de los parámetros y le sirve la primera.

El capítulo 2 conserva el mal condicionamiento donde sirve para algo: en
`fig-valle-mal-escalado` pone las dos superficies lado a lado, y de ahí sale el adelanto al
capítulo de preparación de datos. **No se unifican los dos generadores** sin decidirlo
expresamente: hacerlo obliga a recalibrar la rejilla de verosimilitud del capítulo 1, el
interpolador y sus ocho figuras.

Cuando el capítulo necesita una señal curva y conocida (capítulo 6), el generador
canónico es este, y tampoco cuenta como conjunto de datos nuevo:

    torch.manual_seed(42)

    n = 30
    x = torch.rand(n) * 2
    senal = torch.sin(torch.pi * x)      # media onda: sube y vuelve a bajar
    y = senal + 0.2 * torch.randn(n)

**Es $\sin(\pi x)$ y no $\sin(2\pi x)$**, y la diferencia importa. Con $2\pi$ la señal
completa dos periodos en $[0,2]$, ningún polinomio de grado bajo se le acerca y la curva del
riesgo esperado sale dentada, porque los grados pares y los impares aproximan de forma muy
distinta una función con esa simetría. Medido: con $2\pi$ el riesgo esperado va 0.56, 0.49,
0.51, 0.52, 0.93, 0.19, 1.08, y de ahí no sale una U que se pueda leer. Con $\pi$ el sesgo
baja de forma limpia hasta el grado 3 y la varianza toma el relevo, que es lo que el capítulo
necesita enseñar.

Dos detalles más del capítulo 6, por si hay que reproducirlo:

- **Las potencias se toman de $x-1$**, no de $x$. Con la entrada en $[0,2]$ la columna $x^9$
  llega a 512 y el sistema queda mal condicionado. Centrar no cambia el espacio de funciones.
- **La varianza del grado 9 con $\nobs=30$ es del orden de 22**, y con $\nobs=15$ del orden
  de $10^5$. Cualquier figura que la incluya necesita el eje en escala logarítmica, y con
  `xscale="log"` hay que llamar a `ax.minorticks_off()` o las marcas menores se solapan con
  las etiquetas.

Semilla siempre. Cualquier experimento que dependa del azar se fija con
`torch.manual_seed` o con `random_state=42` en scikit-learn, y se dice en el texto cuando
el resultado concreto importa.

## Figuras

`import style` (en el preámbulo oculto) fija tipografía serif, tamaños, rejilla gris tenue,
ejes sin líneas superior ni derecha, leyenda sin marco y el ciclo de color.

Paleta, de `capitulos/style.py`:

| Constante | Valor | Papel |
|---|---|---|
| `TINTA` | `#1b1d21` | texto y líneas neutras |
| `AZUL` | `#151f6c` | primer color del ciclo |
| `NARANJA` | `#ff5700` | acento CUNEF, segundo color del ciclo |
| `GRIS` | `#8b8e95` | ejes, marcas, curvas de nivel |
| `GRIS_TENUE` | `#dcdcd8` | rejilla |

Regla del fichero: **el color señala una cosa por figura**, no decora. En la práctica: negro
o tinta para los datos observados, negro discontinuo para la señal verdadera, naranja para
lo que el capítulo está enseñando (el ajuste, la dirección de descenso, la trayectoria),
gris para lo auxiliar (curvas de nivel).

El **capítulo 1** usa además `#b33b2e`, `#7aa6c2` y `#4c78a8`, fuera de la paleta. El
capítulo 2 ya solo usa colores del tema, aunque cableados como literales.

**En las etiquetas de figura no valen las macros de `_macros.tex`.** Las macros solo existen
para MathJax en el HTML. `matplotlib` tiene su propio intérprete de matemáticas, que no las
conoce, y un `ax.set_xlabel(r"$\nfeat$")` **aborta el render** con
`ParseSyntaxException: Unknown symbol`. En las figuras se escribe LaTeX corriente:

| En la prosa | En la figura |
|---|---|
| `$\nobs$`, `$\nfeat$` | `$n$`, `$p$` |
| `$\X$`, `$\coef$` | `$\mathbf{X}$`, `$\mathbf{w}$` |
| `$\Real^{\nobs}$` | `$\mathbb{R}^{n}$` |
| `$\yhati$`, `$\Riskh$` | `$\hat{y}_i$`, `$\hat{R}$` |

**Nunca se escribe `import style` ni `from style import ...` en un bloque visible.** Ese
bloque llega al cuaderno, y en Colab no existe `capitulos/style.py`: el cuaderno fallaría en
la primera celda. El tema se aplica desde el preámbulo oculto, que no viaja al cuaderno pero
tampoco hace falta allí. Si un color hay que nombrarlo, se escribe el literal con el nombre
en un comentario:

    color="#ff5700",  # NARANJA de style.py

Tamaños en uso:

| Situación | `figsize` |
|---|---|
| figura principal en el cuerpo | `(6, 4)` |
| figura de margen | `(3, 2)` |
| dos paneles lado a lado | `(9, 3.6)` |

Y el resto de hábitos, verificados en los dos capítulos:

- `fig, ax = plt.subplots(...)`, nunca la interfaz de estado de `pyplot`.
- `ax.set(xlabel="$x$", ylabel="$y$")` en una sola llamada.
- `.numpy()` antes de pasar un tensor a matplotlib.
- `ax.legend()` solo si hay más de una serie, y con etiquetas que usan LaTeX cuando nombran
  un objeto matemático: `label=r"señal: $f(x_i)=2x_i+1$"`.
- `plt.tight_layout()` al final, siempre.
- Escala logarítmica cuando el fenómeno lo pide (`ax.set_yscale("log")` para el exceso de
  riesgo), y se dice en el pie.

## Traducir una fórmula a código

El patrón de los dos capítulos: la fórmula, y a continuación la celda que la calcula, con
los mismos nombres y en forma vectorizada.

    def grad_mse(w, x, y):
        residuos = y - predict(w, x)
        return torch.stack((
            -2 * residuos.mean(),
            -2 * (x * residuos).mean(),
        ))

Nada de bucles sobre observaciones cuando la operación es vectorizable. El bucle se reserva
para lo que es intrínsecamente iterativo: las iteraciones del descenso, la búsqueda en
rejilla.

**Toda derivación analítica se comprueba contra autodiferenciación** y se enseña la
comprobación:

    print("coinciden:", torch.allclose(gradiente_manual, gradiente_auto))

## Ancho de las líneas de código

**78 caracteres.** Es lo que cabe en el bloque de código del tema, con 760 px de cuerpo y la
fuente monoespaciada a 0.82 rem. El libro renderiza con `code-overflow: wrap`, así que una
línea más larga no queda cortada: se parte en dos líneas visuales, y la continuación arranca en
la columna cero, donde parece el comienzo de una sentencia. Se lee peor, de modo que las líneas
se escriben para que quepan.

La comprobación se automatiza sobre el HTML ya renderizado: un bloque cuyo `scrollWidth` supera
su `clientWidth` tiene alguna línea que se parte.

## Anotaciones de código

Los números `# <1>` al final de una línea, con la lista de notas debajo del bloque. Dos cosas
que hay que saber, las dos ya resueltas en `assets/custom.scss` y que no hay que volver a
tocar:

- Quarto crea el resaltado de la línea anotada como un `div` con `position: absolute` y lo
  cuelga del `<pre>`, dando por hecho que el `<pre>` es un bloque contenedor. No lo es por
  defecto, y entonces la banda se posiciona respecto de un ancestro lejano y aparece como una
  raya horizontal fuera de sitio, cruzando el bloque de código y la barra lateral. Lo arregla
  `pre.code-annotation-code { position: relative; }`.
- El canal de la derecha donde van los números (`.code-annotation-gutter`) se pinta opaco por
  encima del código y tapa el final de las líneas largas. En el tema va transparente.

## Salidas

- `print` con f-strings y precisión explícita: `print(f"w0 = {w_manual[0]:.4f}")`.
- Para enseñar un tensor pequeño, `torch.round(t, decimals=3)`.
- Las salidas largas no se imprimen enteras.

## Código en las hojas y en el bloque D

El fragmento del bloque D (encontrar los errores) va en ` ```python ` **sin llaves**, de
modo que no se ejecuta. Puede llamar a funciones que no existen (`cargar_datos()`) porque su
única función es contener errores conceptuales localizables.

## Coste de ejecución

`freeze: auto` guarda los resultados, pero el capítulo se ejecuta entero cada vez que
cambia. Un experimento que tarde más de unos segundos hay que justificarlo o reducirlo. Los
1.000 ajustes del experimento de sesgo y varianza del capítulo 6 necesitan solución cerrada
(`torch.linalg.lstsq`), no descenso de gradiente.
