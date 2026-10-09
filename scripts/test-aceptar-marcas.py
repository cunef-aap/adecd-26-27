#!/usr/bin/env python3
"""Aceptar la revision conserva el contenido y los atributos ajenos a `.nuevo`."""
import importlib.util
from pathlib import Path
import unittest


spec = importlib.util.spec_from_file_location(
    "aceptar_marcas", Path(__file__).with_name("aceptar-marcas.py"))
marcas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(marcas)


class AceptarMarcasTest(unittest.TestCase):
    def comprueba(self, original, esperado, cantidad):
        self.assertEqual(len(marcas.marcas(original)), cantidad)
        self.assertEqual(marcas.acepta(original), (esperado, cantidad))
        self.assertEqual(marcas.marcas(esperado), [])
        self.assertEqual(marcas.acepta(esperado), (esperado, 0))

    def test_div_con_solo_nuevo_se_desenvuelve(self):
        self.comprueba("::: {.nuevo}\nTexto.\n:::\n", "Texto.\n", 1)

    def test_div_con_clase_mixta_conserva_la_estructura(self):
        for atributos, resultado in (
            (".codigo-clave .nuevo", ".codigo-clave"),
            (".nuevo .cajanegra", ".cajanegra"),
            ("#id .nuevo", "#id"),
            ('.proof .nuevo #prueba title="Dos  palabras"',
             '.proof  #prueba title="Dos  palabras"'),
        ):
            with self.subTest(atributos=atributos):
                self.comprueba(
                    f":::: {{{atributos}}}\nContenido.\n::::\n",
                    f":::: {{{resultado}}}\nContenido.\n::::\n", 1)

    def test_div_mixto_dentro_de_marca_pura(self):
        self.comprueba(
            "::: {.nuevo}\n::: {.proof .nuevo}\nPrueba.\n:::\n:::\n",
            "::: {.proof}\nPrueba.\n:::\n", 2)

    def test_marca_pura_dentro_de_div_mixto(self):
        self.comprueba(
            "::: {.proof .nuevo}\n::: {.nuevo}\nPrueba.\n:::\n:::\n",
            "::: {.proof}\nPrueba.\n:::\n", 2)

    def test_hermanos_y_div_sin_marca(self):
        self.comprueba(
            "::: {#thm-ejemplo}\n::: {.nuevo}\nTeorema.\n:::\n"
            "::: {.proof .nuevo}\nPrueba.\n:::\n:::\n"
            "::: {.nuevo}\nDespues.\n:::\n",
            "::: {#thm-ejemplo}\nTeorema.\n"
            "::: {.proof}\nPrueba.\n:::\n:::\nDespues.\n", 3)

    def test_span_y_encabezado_conservan_comportamiento(self):
        self.comprueba(
            "## Titulo {.nuevo #sec-ejemplo}\n[Texto.]{.nuevo}\n",
            "## Titulo {#sec-ejemplo}\nTexto.\n", 2)

    def test_no_confunde_nombres_similares(self):
        texto = "::: {.nuevo-ejemplo #nuevo title=\".nuevo\"}\nTexto.\n:::\n"
        self.comprueba(texto, texto, 0)

    def test_encabezado_conserva_separacion_antes_de_div(self):
        self.comprueba(
            "## Ejercicios {.nuevo}\n\n::: {#exr-ejemplo}\nEnunciado.\n:::\n",
            "## Ejercicios\n\n::: {#exr-ejemplo}\nEnunciado.\n:::\n", 1)

    def test_encabezado_conserva_lineas_en_blanco_entre_bloques(self):
        self.comprueba(
            "## Titulo {.nuevo #sec-ejemplo}  \n\n\nParrafo.\n",
            "## Titulo {#sec-ejemplo}\n\n\nParrafo.\n", 1)

    def test_listado_indica_numero_de_linea(self):
        self.assertEqual(marcas.marcas("Texto.\n::: {.proof .nuevo}\nPrueba.\n:::\n"),
                         [(2, "div")])


if __name__ == "__main__":
    unittest.main()
