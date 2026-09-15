#!/usr/bin/env python3
"""Pruebas del comprobador de alineación con documentos sintéticos temporales."""
import contextlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


RUTA = Path(__file__).with_name("comprueba-ejercicios-capitulo.py")
SPEC = importlib.util.spec_from_file_location("comprueba_ejercicios", RUTA)
COMPRUEBA = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COMPRUEBA)


def ejercicio(clave, cuerpo):
    return f"::: {{#{clave}}}\n{cuerpo}\n:::\n"


class AlineacionTest(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)
        self.carpeta = Path(self.temporal.name)
        self.capitulo = self.carpeta / "capitulo.qmd"
        self.hoja = self.carpeta / "hoja.qmd"
        self.sol = self.carpeta / "hoja-soluciones.qmd"
        self.cuerpo = "## Título\n\nEnunciado con $x^2$."
        self.capitulo.write_text(ejercicio("exr-a", self.cuerpo), encoding="utf-8")
        self.hoja.write_text(ejercicio("exr-h-a", self.cuerpo), encoding="utf-8")

    def ejecuta(self):
        salida, errores = io.StringIO(), io.StringIO()
        with patch("sys.argv", [str(RUTA), str(self.capitulo), str(self.hoja)]), \
                contextlib.redirect_stdout(salida), contextlib.redirect_stderr(errores):
            estado = COMPRUEBA.main()
        return estado, salida.getvalue(), errores.getvalue()

    def solucionario(self, cuerpo=None, cajas="::: {.sol}\nContenido.\n:::\n"):
        texto = ejercicio("exr-h-a-sol", cuerpo if cuerpo is not None else self.cuerpo)
        self.sol.write_text(texto + cajas, encoding="utf-8")

    def test_admite_ids_exteriores_distintos_y_ejercicios_adicionales(self):
        self.hoja.write_text(ejercicio("exr-h-a", self.cuerpo) +
                             ejercicio("exr-h-b", "## Otro\nEnunciado."), encoding="utf-8")
        self.assertEqual(self.ejecuta()[0], 0)

    def test_divs_anidados_y_etiquetas_del_solucionario(self):
        cuerpo = (self.cuerpo + "\n\n::: {#fig-h2-a}\nFigura.\n:::\n\n"
                  "Consultar @fig-h2-a.\n\n::: {.callout-note}\nNota.\n:::")
        self.capitulo.write_text(ejercicio("exr-a", cuerpo), encoding="utf-8")
        self.hoja.write_text(ejercicio("exr-h-a", cuerpo), encoding="utf-8")
        self.solucionario(COMPRUEBA.EXTRACTOR.con_sufijo(cuerpo),
                         "::: {.sol}\n::: {.callout-note}\nContenido.\n:::\n:::\n")
        self.assertEqual(self.ejecuta()[0], 0)

    def test_finales_de_linea_y_espacios_finales(self):
        cuerpo = "\r\n## Título  \r\n\r\nEnunciado con $x^2$.  \r\n"
        self.assertEqual(COMPRUEBA.normaliza(cuerpo), self.cuerpo)

    def test_no_normaliza_formulas_ni_indentacion_de_codigo(self):
        self.assertNotEqual(COMPRUEBA.normaliza("$x^2$"), COMPRUEBA.normaliza("$x^3$"))
        self.assertNotEqual(COMPRUEBA.normaliza("    x = 1"),
                            COMPRUEBA.normaliza("x = 1"))

    def test_desorden_del_capitulo(self):
        otro = "## Otro\nEnunciado distinto."
        self.capitulo.write_text(ejercicio("exr-a", self.cuerpo) +
                                 ejercicio("exr-b", otro), encoding="utf-8")
        self.hoja.write_text(ejercicio("exr-h-b", otro) +
                             ejercicio("exr-h-a", self.cuerpo), encoding="utf-8")
        estado, _, errores = self.ejecuta()
        self.assertEqual(estado, 1)
        self.assertIn("ejercicio 1, «Título»", errores)
        self.assertIn("ejercicio 2, «Otro»", errores)

    def test_identificadores_repetidos(self):
        self.hoja.write_text(ejercicio("exr-h-a", self.cuerpo) * 2, encoding="utf-8")
        self.assertIn("identificadores repetidos", self.ejecuta()[2])

    def test_solucionario_alineado(self):
        self.solucionario()
        self.assertEqual(self.ejecuta()[0], 0)

    def test_solucionario_en_orden_incorrecto(self):
        self.sol.write_text(ejercicio("exr-otro-sol", self.cuerpo) +
                            "::: {.sol}\nContenido.\n:::\n", encoding="utf-8")
        self.assertIn("revisar el orden", self.ejecuta()[2])

    def test_solucionario_con_enunciado_distinto(self):
        self.solucionario(self.cuerpo.replace("x^2", "x^3"))
        self.assertIn("título o enunciado distintos", self.ejecuta()[2])

    def test_solucion_ausente_duplicada_o_vacia(self):
        for cajas, esperado in [
            ("", "hay 0"),
            ("::: {.sol}\nUno.\n:::\n::: {.sol}\nDos.\n:::\n", "hay 2"),
            ("::: {.sol}\n\n:::\n", "caja .sol vacía"),
        ]:
            with self.subTest(cajas=cajas):
                self.solucionario(cajas=cajas)
                estado, _, errores = self.ejecuta()
                self.assertEqual(estado, 1)
                self.assertIn(esperado, errores)

    def test_solucion_dentro_del_enunciado(self):
        self.solucionario(self.cuerpo + "\n::: {.sol}\nContenido.\n:::", cajas="")
        self.assertIn("dentro del enunciado", self.ejecuta()[2])


if __name__ == "__main__":
    unittest.main()
