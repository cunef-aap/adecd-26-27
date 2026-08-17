"""Estilo de figuras del curso y localización de los datos.

Misma gramática que la web: tinta, un único acento naranja CUNEF y grises.
El color se usa para señalar UNA cosa por figura, no para decorar.
"""

import os
from pathlib import Path

from matplotlib import pyplot as plt

# --- Dónde están los datos --------------------------------------------------
# Los capítulos se leen en dos sitios con rutas distintas: al renderizar el
# libro, `capitulos/` tiene `../datos/` al lado; en Colab, el cuaderno está
# solo y no hay ningún fichero. `ruta_datos()` resuelve los dos casos.
#
# Se prefiere SIEMPRE la copia local, para que el render no dependa de la red
# y sea reproducible sin conexión.

URL_DATOS = os.environ.get(
    "URL_DATOS",
    "https://raw.githubusercontent.com/cunef-aap-fall2026/"
    "cunef-aap-fall2026.github.io/main/datos",
)


def ruta_datos(nombre):
    """Ruta local del fichero de datos si existe, y si no su URL pública."""
    for candidata in (Path("../datos") / nombre, Path("datos") / nombre):
        if candidata.exists():
            return candidata
    return f"{URL_DATOS}/{nombre}"


TINTA = "#1b1d21"
AZUL = "#151f6c"
NARANJA = "#ff5700"
GRIS = "#8b8e95"
GRIS_TENUE = "#dcdcd8"

plt.rcParams.update({
    "figure.dpi": 130,
    "savefig.dpi": 130,
    "font.family": "serif",
    "font.serif": ["Charter", "Iowan Old Style", "Palatino", "Georgia", "DejaVu Serif"],
    "font.size": 10,
    "axes.prop_cycle": plt.cycler(color=[AZUL, NARANJA, GRIS, TINTA, "#5b8c5a"]),
    "axes.edgecolor": GRIS,
    "axes.labelcolor": TINTA,
    "axes.titlesize": 10.5,
    "axes.titleweight": "normal",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": GRIS_TENUE,
    "grid.linewidth": 0.6,
    "text.color": TINTA,
    "xtick.color": GRIS,
    "ytick.color": GRIS,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.frameon": False,
    "legend.fontsize": 9,
})
