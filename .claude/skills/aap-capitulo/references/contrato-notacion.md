# Contrato de notación

Fuente única: `assets/includes/_macros.tex`. Se incluye en todos los capítulos, en las
hojas y en `index.qmd`. Dentro de `$$...$$` solo sobreviven `\newcommand`,
`\renewcommand` y `\DeclareMathOperator`. No caben `\usepackage`,
`\DeclarePairedDelimiter` ni `\newenvironment`.

**Regla única**: no se redefine un símbolo en un capítulo y no se escribe a pelo lo que
tiene macro. Cambiar $w$ por $\beta$ en todo el libro tiene que ser una línea de
`_macros.tex`, no quince ficheros.

## Coeficientes

| Macro | Sale como | Uso |
|---|---|---|
| `\coef` | $\boldsymbol{w}$ | vector de coeficientes. Todo coeficiente pasa por aquí |
| `\coefhat` | $\hat{\boldsymbol{w}}$ | estimación |
| `\coefj` | $w_j$ | componente |
| `\coefzero` | $w_0$ | intercepto |
| `\coefols` | $\hat{\boldsymbol{w}}_{\mathrm{MCO}}$ | mínimos cuadrados ordinarios |
| `\coefridge` | $\hat{\boldsymbol{w}}_{\lambda}$ | ridge |

Se usa `\boldsymbol` y no `\mathbf` para que el interruptor funcione también con letras
griegas.

## Datos y matriz de diseño

`\X` $\mathbf X$ · `\Xt` $\mathbf X^{\mathsf T}$ · `\xv` $\mathbf x$ · `\yv` $\mathbf y$ ·
`\Phimat` $\boldsymbol\Phi$ · `\onesv` $\mathbf 1$ · `\zerov` $\mathbf 0$ · `\Id` $\mathbf I$ ·
`\Zbf` · `\Vbf` · `\Wbf` · `\Hbf` · `\Hess` ($\nabla^2$).

## Respuestas y residuos

`\yi` $y_i$ · `\yhat` $\hat y$ · `\yhati` $\hat y_i$ · `\ybar` $\bar y$ ·
`\resid` $\mathbf r$ · `\residi` $r_i$.

## Tamaños

`\nobs` $n$ · `\nfeat` $p$ · `\ntrain` · `\nval` · `\ntest` · `\ncal`.

## Riesgo y pérdidas

| Macro | Sale como | Nota |
|---|---|---|
| `\Risk` | $R$ | riesgo **verdadero** o poblacional |
| `\Riskh` | $\hat R$ | riesgo **empírico** |
| `\Riskproc{\nobs}` | $\bar R_n$ | **riesgo esperado del procedimiento** con muestras de tamaño $\nobs$, `def-riesgo-procedimiento` del cap. 4; es lo que estima $\CV$ y lo que descompone el cap. 6 |
| `\loss` | $\ell$ | función de pérdida |
| `\MSE` | MSE | error cuadrático medio |
| `\RMSE` | RMSE | raíz del error cuadrático medio |
| `\MAE` | MAE | error absoluto medio |
| `\RSS` | RSS | suma de cuadrados de los residuos |
| `\SSE` `\SST` `\SSR` | SSE, SST, SS_reg | descomposición de la suma de cuadrados |
| `\Rsq` | $R^2$ | |
| `\CV` | CV | validación cruzada |

La macro `\modelh` entra en el capítulo 4, en `def-riesgo-procedimiento`: el riesgo del
procedimiento es el de la función que produce el ajuste, $\modelh_{\data}$, no el de un vector
de parámetros. Antes de esa definición el capítulo 4 habla siempre de $\coef$ y $\coefhat$.

$\Riskh$ va **siempre** normalizado por $1/\nobs$. Es una convención dura del curso, fijada
en `curso/glosario.qmd`, y afecta a la escala del gradiente y por tanto a la tasa de
aprendizaje.

Los acrónimos van **en inglés**, que es lo que los estudiantes verán en `scikit-learn` y en
la bibliografía. Los **nombres completos van en español**: se escribe "error cuadrático
medio" y la sigla es $\MSE$. En econometría varias de estas cantidades llevan sigla española
(SCR, SCT, SCE); la correspondencia está en `curso/glosario.qmd`.

Ojo con `\SSR`, que sale como $\mathrm{SS_{reg}}$ y no como SSR: en inglés esa sigla se usa
también para la suma de cuadrados de los residuos, que aquí es `\RSS`.

Ojo con `\loss` y `\loglik`: los dos son $\ell$. La distinción viene del contexto y de los
argumentos. Si en un capítulo aparecen juntos y se confunden, se dice en el texto cuál es
cuál.

## Verosimilitud

`\Lik` $L$ · `\loglik` $\ell$ · `\logliksp` $\ell_{\mathrm p}$ (perfilada) · `\pdf` $p$ ·
`\Normal` $\mathcal N$ · `\Laplacedist` · `\given` (barra de condicionamiento con espaciado)
· `\iid` ($\overset{\text{iid}}{\sim}$).

## Escalares fijos

| Macro | Sale como | Aviso |
|---|---|---|
| `\noise` | $\sigma$ | nivel de ruido |
| `\noisehat` | $\hat\sigma$ | |
| `\lr` | $\alpha$ | tasa de aprendizaje |
| `\reg` | $\lambda$ | penalización. **En scikit-learn el argumento se llama `alpha=`** |
| `\defeq` | $\coloneqq$ | |

La colisión entre `\lr` ($\alpha$ en las matemáticas) y `alpha=` de scikit-learn ($\lambda$
en las matemáticas) hay que declararla explícitamente en los capítulos 7 y 8, que son donde
aparecen juntos. Es un error frecuente y es material de bloque D.

## Cálculo

`\grad` $\nabla$ · `\pd{h}{w_j}` derivada parcial · `\dd` diferencial recto ·
`\argmax` · `\argmin` (ambos con límites debajo).

## Álgebra

`\T` traspuesta · `\norm{v}` · `\abs{a}` · `\inner{a}{b}` · `\rank` (sale como "rank") ·
`\tr` · `\diag` · `\kernelop` (sale como "null") · `\sign` · `\Real` $\mathbb R$ ·
`\Realn` · `\Realp` · `\Rbb`.

## Probabilidad

`\E{X}` $\mathbb E[X]$ · `\Esub{P}{X}` · `\Var{X}` · `\Varsub{P}{X}` · `\Cov{X}{Y}` ·
`\Prob{A}` · `\med` (sale como "median"). **Todos con llaves, no con corchetes.**

## Conjuntos y modelos

`\data` $\mathcal D$ · `\Dtrain` · `\Dval` · `\Dtest` · `\fold{k}` $\mathcal F_k$ ·
`\model` $f$ · `\modelh` $\hat f$ · `\nullmodel` $\bar f$ (modelo nulo o línea base) ·
`\hyp` $\mathcal F$ (clase de hipótesis) · `\Xcal` · `\Ycal`.

## Reservadas para capítulos posteriores

Ya definidas, sin usar todavía. Al llegar a su capítulo se usan estas y no otras.

| Macro | Capítulo | Significado |
|---|---|---|
| `\Dtrain` `\Dval` `\Dtest` `\fold{k}` | 4 | particiones y bloques de validación cruzada |
| `\nullmodel` | 4 | línea base, el mejor modelo constante |
| `\basis` $\varphi$ | 6 | función de base, **escalar** |
| `\Phimat` | 6 | matriz de características |
| `\coefols` `\coefridge` | 8 | soluciones de mínimos cuadrados y de ridge |
| `\pos{a}` $(a)_+$, `\softthr` $S$ | 8 | parte positiva y umbral blando del lasso |
| `\pinball` $\rho_\tau$ | fuera de alcance | pérdida de cuantiles |

**Hueco detectado, pendiente de decidir.** `\basis` está definida como $\varphi$ sin negrita,
es decir como escalar, pero el capítulo 6 necesita escribir
$\model_{\coef}(\xv)=\coef\T\boldsymbol\varphi(\xv)$, que exige un vector, y también sus
componentes $\varphi_j$. No hay macro para ninguno de los dos. Antes de escribir el capítulo
6 hay que añadir a `_macros.tex` algo del tipo `\basisv` y `\basisj`, o decidir otra
notación. **Es una modificación del contrato y la decide el autor**, no se improvisa dentro
de un capítulo.

## El mapa de características, decidido en el capítulo 6

`\basis` estaba definida como `\varphi`, un escalar, y el capítulo 6 necesitaba además el
vector y su dimensión. La decisión tomada al escribirlo, y que hay que respetar de aquí en
adelante:

| Macro | Símbolo | Qué es |
|---|---|---|
| `\basis` | $\varphi$ | una característica, siempre con subíndice: `\basis_j(\xv)` |
| `\basisv` | $\boldsymbol{\varphi}$ | el vector de las $\nbasis$ características |
| `\Phimat` | $\boldsymbol{\Phi}$ | la matriz con $\basisv(\xv_i)\T$ por filas |
| `\nbasis` | $d$ | cuántas características hay |

Y se mantiene la distinción del apartado siguiente: `\nfeat` cuenta **variables predictoras**,
las columnas que traen los datos, y `\nbasis` cuenta **características**, las columnas que
construye el mapa. En el capítulo 6, ocho variables predictoras dan 44 características a
grado 2.

## Train y test, no "prueba"

Las particiones se llaman **train** y **test**, en inglés y en cursiva la primera vez de cada
capítulo. "Conjunto de prueba" no se usa: el estudiante va a ver `train_test_split`,
`X_train` y `X_test` en scikit-learn, y el texto tiene que decir lo mismo que el código. En
las matemáticas siguen siendo `\Dtrain` y `\Dtest`, con `\ntrain` y `\ntest` para sus
tamaños.

Lo mismo con **validación**: se dice validación, y la macro es `\Dval`.

Consecuencias que el capítulo 4 fijó y que hay que respetar de aquí en adelante:

- **Los identificadores del código también son `train` y `test`.** Se escribe `X_train`,
  `y_train`, `media_train`, `es_train`. Antes del capítulo 4 se usaba `X_entrena` y
  `media_entrena`; quedó descartado, porque obligaba a traducir mentalmente entre el texto y el
  código. Es la excepción a la regla de que todo lo que no es la API va en español, y la razón
  es la misma que la del párrafo anterior: `train_test_split` devuelve `X_train`.
- **Nada de sinónimos para las particiones.** "Las reservadas", "las que no ha visto", "donde se
  ha ajustado" se sustituyen por "test" y "train", también en las cadenas que imprime el código
  y en los títulos de las figuras. Un sinónimo distinto en cada párrafo obliga al lector a
  comprobar cada vez de qué conjunto se habla.
- Los índices internos de un bloque de validación cruzada sí van en español, `indices_ajuste`
  e `indices_val`, para que no se confundan con la partición de fuera.

## K-fold cross validation, en inglés

El procedimiento se llama **K-fold cross validation**. El par se da una vez, "validación
cruzada de $K$ bloques o *K-fold cross validation*", y a partir de ahí se usa el nombre inglés,
que es el que aparece en `scikit-learn` (`KFold`, `cross_val_score`) y en la bibliografía. El
caso $K=\ntrain$ es *leave-one-out*, también en inglés. La macro de la estimación es `\CV` y la
del bloque $k$ es `\fold{k}`.

## Variable predictora frente a característica

Dos palabras para dos cosas distintas, y no se mezclan:

- **variable predictora**, o **predictor**, es una columna de $\X$ tal como viene en los
  datos. Es el término de los capítulos 3 a 5, y $\nfeat$ cuenta variables predictoras.
- **característica** es una variable **construida** a partir de las predictoras, que es lo
  que aparece en el capítulo 6 con los mapas $\basis$ y la matriz $\Phimat$.

El capítulo 3 se escribió primero con "característica" para las dos cosas y hubo que
corregirlo. Al escribir los capítulos 4 y 5, usar "variable predictora"; a partir del 6,
distinguir las dos.

## Números en español

- **Punto decimal, también en español**: se escribe `$\lr = 0.015$`, no `0{,}015`. El motivo
  es que el código y las salidas de Python usan punto, y el texto tiene que decir lo mismo
  que la consola. Es una desviación deliberada de la ortografía española.
- **Millares sin separador**: "2000 iteraciones", "15000 filas". Poner el punto de millar
  junto al punto decimal se lee mal.
- En código y en salidas de Python los números salen como salen. No se retocan.

## Traducción desde el material de Chodrow

Ninguna fórmula de `ml-notes-update-main/` se puede pegar sin reescribir. Tabla mínima:

| Chodrow | aap-cunef |
|---|---|
| `\vw` | `\coef` |
| `\vx` | `\xv` |
| `\mX` | `\X` |
| `\cL` | `\loglik` |
| `\iprod{a}{b}` | `\inner{a}{b}` |
| `\E[X]` | `\E{X}` |
| `\E_{\data}[X]` | `\Esub{\data}{X}` (la esperanza con subíndice: `\E` no admite subíndice, se come el `_`) |

**El subíndice de la esperanza se escribe siempre que haya más de un candidato.** La tabla está
en `curso/probabilidad.qmd`, tras `lem-esperanza-funcion`: $\Esub{P^\star}{\cdot}$ para una
observación nueva, $\Esub{X}{\cdot}$ para la marginal de las predictoras,
$\Esub{\varepsilon}{\cdot}$ para el ruido y $\Esub{\data}{\cdot}$, $\Esub{\Dtrain}{\cdot}$
o $\Esub{\Dtest}{\cdot}$ para las muestras. Con una sola variable aleatoria dentro, como
$\E{\varepsilon}$, el subíndice se omite. **Lo mismo vale para la varianza**: `\Varsub`
existe por el mismo motivo, y `prp-precision-test` del capítulo 4 la usa a los dos lados de la
igualdad, con medidas distintas a cada lado.
| `\R` | `\Real` |

Y además: sus capítulos enuncian sin demostrar en varios puntos ("beyond our scope"), y el
curso español demuestra. Sus figuras llevan color cableado (`steelblue`, `firebrick`,
`C0`), y aquí el color lo pone `capitulos/style.py`.

## Comprobación

`python .claude/skills/aap-capitulo/scripts/check-capitulo.py <fichero>` avisa de toda macro
usada que no esté definida en `_macros.tex`.
