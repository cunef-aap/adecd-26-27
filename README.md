# Aprendizaje Automático: Predicción (G244)

Apuntes, laboratorios y material de evaluación de la asignatura **Aprendizaje Automático:
Predicción**, 3.º del Doble Grado en ADE y Ciencia de Datos, CUNEF Universidad.

Sitio publicado: <https://cunef-aap.github.io/adecd-26-27/>

## Puesta en marcha

```bash
# 1. Quarto >= 1.8  (el instalador pide contraseña de administrador)
brew install --cask quarto
quarto --version

# 2. Entorno de Python y kernel
conda env create -f environment.yml
conda activate aap
python -m ipykernel install --user --name aap --display-name "Python (aap)"

# 3. Datos (los espeja en datos/ y escribe PROCEDENCIA.md)
make datos

# 4. Construir
make check       # los centinelas #--- están emparejados
make sitio       # sitio -> docs/
make notebooks   # cuadernos con huecos -> docs/live-notebooks/
make preview     # servidor local
make pdfs        # PDF de capitulos, hojas y anexos -> pdf/
```

## Publicación

El sitio se sirve con GitHub Pages desde la carpeta `docs/` de la rama `main`, así que
**`docs/` se versiona**: lo que hay commiteado es lo que se ve publicado. Para actualizar:

```bash
make publicar    # render + notebooks + commit + push
```

### Los solucionarios no se publican

Las seis líneas `problemas/hoja-NN-soluciones.qmd` de `_quarto.yml` están **comentadas**, y
el perfil `publica` excluye además esos ficheros de `project.render` para que Quarto no
copie el `.qmd` crudo a `docs/`. Los solucionarios se reparten por el Campus Virtual, en
PDF, después de cada sesión de problemas, que es lo que promete el pie de cada hoja.

```bash
make soluciones-estado   # dice si se publicarían o no
make pdfs-soluciones     # los imprime a pdf/problemas/ y los vuelve a ocultar
```

`make pdfs-soluciones` los publica temporalmente porque sus referencias cruzadas
(`@thm-test-insesgado` y compañía) solo resuelven con el libro entero renderizado; al
terminar deja el repositorio como estaba. Para publicarlos de forma permanente,
descomenta esas líneas y borra el bloque `render` de `_quarto-publica.yml`.

### Por qué los PDF salen de imprimir el HTML

`scripts/crear-pdfs.py` usa Chrome en modo headless sobre las páginas ya renderizadas, en
lugar de renderizar cada capítulo a PDF con LaTeX. Dos razones: las referencias cruzadas
salen resueltas (`Teorema 4.1` en lugar de `?@thm-test-insesgado`, que es lo que da un
render suelto fuera del libro) y las cajas `.sol`, `.trampa` y `.cajanegra` conservan su
estilo, que vive en `assets/styles.css` y no existe en LaTeX.

## Cómo funciona el material

Cada capítulo es **un solo fichero** `.qmd` del que salen dos artefactos:

| Perfil | Salida | Qué hace con los bloques `#---` |
|---|---|---|
| `publica` | `docs/` (el sitio) | borra solo las líneas marcadoras; **el código se ve entero** |
| `notebooks`| `docs/live-notebooks/` (`.ipynb`) | sustituye el bloque por `# TODO: completar en clase` |

Así, lo que se completa en directo en el laboratorio y lo que queda publicado como
referencia **no pueden desincronizarse**: son el mismo fichero.

```python
```{python}
#---
# esto es un hueco en el cuaderno y código completo en el sitio
w = np.linalg.solve(X.T @ X, X.T @ y)
#---
```
```

OJO: los centinelas tienen que ir emparejados. `make check` lo comprueba; un número impar
borraría en silencio el código de un capítulo entero.

## Estructura

```
capitulos/     los 11 capítulos (+ style.py, figuras)
problemas/     hojas para las sesiones de lápiz y papel
evaluacion/    parcial, simulacro, banco de preguntas, proyecto
curso/         guía, calendario, evaluación, política de IA, anexos
assets/        _macros.tex (contrato de notación), estilos, fuentes, logo
scripts/       filtros Lua + utilidades de construcción
datos/         conjuntos de datos espejados, con PROCEDENCIA.md
_referencia/   material de consulta, no se publica (ignorado por git)
```

## Convenios

- **Notación**: todo símbolo sale de `assets/includes/_macros.tex`. Los coeficientes se
  escriben con la macro `\coef`, de modo que cambiar `w` por `β` es una línea, no quince
  ficheros.
- **Se demuestra todo lo que se enuncia.** Lo que no, va marcado como *fuera de alcance*, con
  el motivo.
- **Ningún cuaderno descarga datos al renderizar.** Todo se espeja en `datos/` con fecha y
  licencia.

## Créditos

La estructura y buena parte del enfoque de los capítulos 1-3 y 6-8 siguen las notas de
[Phil Chodrow](https://www.philchodrow.prof/ml-notes-update/) (CSCI 0451, Middlebury
College), usadas con agradecimiento para fines docentes.

Datos de Inside Airbnb (CC BY 4.0) y `prostate.data` de *The Elements of Statistical
Learning*.

Roi Naveiro · Departamento de Métodos Cuantitativos · CUNEF Universidad
