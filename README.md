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
make notebooks   # cuadernos completos -> docs/live-notebooks/
make preview     # revisión privada -> _completo/local/
make pdfs        # PDF de capitulos, hojas y anexos -> pdf/
```

## Publicación

Un solo repositorio, **público**, con las fuentes y el sitio. GitHub Pages lo sirve desde la
carpeta `docs/` de la rama `main`, así que **`docs/` se versiona**: lo que hay commiteado es
lo que se ve publicado.

```bash
make publicar    # render + cuadernos + commit + push
```

### Lo único que no va al repositorio

`.gitignore` excluye el material privado:

1. **`evaluacion/`**: banco de preguntas, parcial, simulacro y ejercicios tipo examen.
2. **`problemas/hoja-*-soluciones.qmd`**: los solucionarios de las hojas.
3. **`banco/`** y **`pdf/`**: ejercicios resueltos y documentos para el Campus Virtual.

Estos materiales se reparten por el Campus Virtual, en PDF, nunca por la web. Viven en local y en
OneDrive; el historial de git está limpio de ellas. `scripts/comprueba-publicable.py` aborta
la publicación si alguna llega al índice de git o a `docs/`, y `make publicar` lo ejecuta
siempre.

### Qué se renderiza: `contenido.txt`

Las fuentes de todo el libro están en el repositorio, pero el **sitio** solo muestra el
material con versión definitiva. Quién entra y quién no se declara en **`contenido.txt`**: las
rutas que empiezan por `-` no se renderizan.

```bash
make publicado   # lista lo que se publica ahora mismo
```

Al aceptar un capítulo para la web, quita el `-` de su línea y ejecuta `make publicar`. Dos piezas lo
sostienen:

- `scripts/publicado.py --sitio` genera con `contenido.txt` la lista de capítulos de
  `_quarto-publica.yml`. La configuración base no contiene listas de capítulos: así cada
  perfil tiene su propio contenido, sin arrastrar páginas de otro.
- `scripts/enlaces-publicados.lua` desactiva los enlaces a páginas todavía sin renderizar.
  Sin él no solo quedarían 404: Quarto trata ese `.qmd` como un recurso y **copia el fuente**
  a `docs/`, que es la vía por la que se publicaría un solucionario.

`scripts/crear-ipynb.py` genera cuaderno solo de los capítulos renderizados, porque
`docs/live-notebooks/` se publica con el sitio.

### Revisar en local desde el editor

El perfil predeterminado es `revision`. Abre `capitulos/03-modelos-lineales.qmd` y usa
el botón de vista previa o render del editor. También puedes ejecutar:

```bash
quarto preview capitulos/03-modelos-lineales.qmd
```

La salida queda en `_completo/local/`, fuera de Git y de la web. Incluye el material
público y las rutas de `revision.txt`: ahora, las soluciones de la hoja 3.
Si cambias esa lista, ejecuta `make revision`. Para previsualizar el libro local completo,
usa `make preview`.

`make sitio` sigue usando el perfil `publica` y escribe únicamente el contenido público
en `docs/`. No desactiva el perfil predeterminado del editor. Añadir algo a `revision.txt`
no lo publica; los solucionarios siguen siendo privados.

Esta separación usa los [perfiles de proyecto de Quarto](https://quarto.org/docs/projects/profiles.html),
sin listas de capítulos compartidas en `_quarto.yml`.

### Los PDF salen del libro completo

`make pdfs` no imprime del sitio, sino de un render aparte con **todo** el libro, en
`_completo/`, mediante el perfil `completo`. Permite subir al Campus Virtual capítulos y
solucionarios que aún no están en la web.

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
curso/         evaluación, anexos de repaso (Colab y Python, álgebra, probabilidad),
               proyecto, glosario
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
