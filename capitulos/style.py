"""Estilo de figuras del curso.

Misma gramática que la web: tinta, un único acento naranja CUNEF y grises.
El color se usa para señalar UNA cosa por figura, no para decorar.
"""

from matplotlib import pyplot as plt

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
