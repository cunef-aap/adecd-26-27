#!/usr/bin/env python3
"""Descarga, submuestrea y ESPEJA los datos en datos/, con procedencia.

Regla del curso: si un dato no esta en datos/ el 31 de agosto, no se usa.
Ningun cuaderno debe leer una URL remota al renderizar.
"""
import gzip
import io
import urllib.request
from datetime import date
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
DATOS = RAIZ / "datos"
DATOS.mkdir(exist_ok=True)

FUENTES = {
    "airbnb_madrid.csv": dict(
        url="https://data.insideairbnb.com/spain/comunidad-de-madrid/madrid/"
            "2026-06-20/data/listings.csv.gz",
        licencia="CC BY 4.0",
        nota="Inside Airbnb, snapshot 2026-06-20. Submuestreado a 15.000 filas.",
    ),
}

COLUMNAS = [
    "id", "host_id", "neighbourhood_group_cleansed", "neighbourhood_cleansed",
    "latitude", "longitude", "property_type", "room_type", "accommodates",
    "bathrooms", "bedrooms", "beds", "price", "minimum_nights",
    "number_of_reviews", "review_scores_rating", "availability_365",
]


def precio_a_float(s):
    return pd.to_numeric(
        s.astype(str).str.replace(r"[$,]", "", regex=True), errors="coerce"
    )


def main(semilla=42, n=15_000):
    proc = ["# Procedencia de los datos", ""]
    for nombre, meta in FUENTES.items():
        print(f"descargando {nombre} ...")
        with urllib.request.urlopen(meta["url"]) as r:
            crudo = r.read()
        with gzip.open(io.BytesIO(crudo), "rt", encoding="utf-8") as fh:
            df = pd.read_csv(fh, low_memory=False)
        df = df[[c for c in COLUMNAS if c in df.columns]].copy()
        df["price"] = precio_a_float(df["price"])
        df = df.dropna(subset=["price"])
        df = df[(df["price"] > 10) & (df["price"] < 1000)]
        if len(df) > n:
            df = df.sample(n, random_state=semilla)
        df.to_csv(DATOS / nombre, index=False)
        proc += [
            f"## {nombre}",
            f"- URL: {meta['url']}",
            f"- Descargado: {date.today().isoformat()}",
            f"- Licencia: {meta['licencia']}",
            f"- Nota: {meta['nota']}",
            f"- Filas x columnas: {df.shape[0]} x {df.shape[1]}",
            "",
        ]
        print(f"  -> {DATOS / nombre}  {df.shape}")

    proc += [
        "## prostate.data",
        "- Origen: Elements of Statistical Learning (Hastie, Tibshirani, Friedman).",
        "- Copiado de ~/CUNEF/teaching/INTRO-ML/curso-ml-R/data/prostate.data",
        "- 97 x 11. Objetivo: `lpsa`. Columna `train` (T/F) con la particion de ESL.",
        "",
    ]
    (DATOS / "PROCEDENCIA.md").write_text("\n".join(proc), encoding="utf-8")
    print("escrito datos/PROCEDENCIA.md")


if __name__ == "__main__":
    main()
