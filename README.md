# Aprendizaje Automático: Predicción (G244)

Apuntes, laboratorios y material de evaluación de la asignatura **Aprendizaje Automático:
Predicción**, 3.º del Doble Grado en ADE y Ciencia de Datos, CUNEF Universidad.

Sitio publicado: <https://cunef-aap-fall2026.github.io/>

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
```

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
capitulos/     los 15 capítulos (+ style.py, figuras)
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

La estructura y buena parte del enfoque de los capítulos 1 a 4 siguen las notas de
[Phil Chodrow](https://www.philchodrow.prof/ml-notes-update/) (CSCI 0451, Middlebury
College), usadas con agradecimiento para fines docentes.

Datos de Inside Airbnb (CC BY 4.0) y `prostate.data` de *The Elements of Statistical
Learning*.

Roi Naveiro · Departamento de Métodos Cuantitativos · CUNEF Universidad
