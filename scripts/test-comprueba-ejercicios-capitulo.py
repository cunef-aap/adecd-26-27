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

    def prepara_seleccion(self, cabecera):
        cuerpos = [self.cuerpo, "## Segundo\n\nEnunciado B.",
                   "## Tercero\n\nEnunciado C."]
        self.capitulo.write_text("".join(
            ejercicio(f"exr-{clave}", cuerpo)
            for clave, cuerpo in zip("abc", cuerpos)
        ), encoding="utf-8")
        self.hoja.write_text(f"---\n{cabecera}\n---\n" +
                             ejercicio("exr-h-a", "Enunciado con $x^2$.") +
                             ejercicio("exr-h-c", "Enunciado C."), encoding="utf-8")

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

    def test_hoja_sin_titulo_descriptivo(self):
        cuerpo = "Enunciado con $x^2$."
        self.hoja.write_text(ejercicio("exr-h-a", cuerpo), encoding="utf-8")
        self.solucionario(cuerpo)
        self.assertEqual(self.ejecuta()[0], 0)

    def test_solo_ignora_el_primer_heading_inicial(self):
        cuerpo = "## Título\n\n## Apartado\n\nEnunciado con $x^2$."
        self.capitulo.write_text(ejercicio("exr-a", cuerpo), encoding="utf-8")
        self.hoja.write_text(ejercicio("exr-h-a", cuerpo.replace("Apartado", "Otro")),
                             encoding="utf-8")
        self.assertEqual(self.ejecuta()[0], 1)

    def test_no_ignora_headings_tras_prosa_divs_o_fences(self):
        for prefijo in ["Introducción.\n\n", "::: {.nuevo}\n", "```python\n", "    "]:
            with self.subTest(prefijo=prefijo):
                original = prefijo + "## Contenido\nOtra línea."
                distinto = prefijo + "## Cambiado\nOtra línea."
                self.assertNotEqual(COMPRUEBA.normaliza_sin_titulo(original),
                                    COMPRUEBA.normaliza_sin_titulo(distinto))

    def test_sin_titulo_no_relaja_formulas_codigo_ni_marcas(self):
        for original, distinto in [
            ("Enunciado con $x^2$.", "Enunciado con $x^3$."),
            ("```python\n    x = 1\n```", "```python\nx = 1\n```"),
            ("Texto.", "::: {.nuevo}\nTexto.\n:::"),
        ]:
            with self.subTest(original=original):
                self.capitulo.write_text(ejercicio("exr-a", "## Título\n\n" + original),
                                         encoding="utf-8")
                self.hoja.write_text(ejercicio("exr-h-a", distinto), encoding="utf-8")
                self.assertEqual(self.ejecuta()[0], 1)

    def test_seleccion_explicita_en_lista_y_en_bloque(self):
        for cabecera in ["ejercicios-capitulo: [exr-a, exr-c]",
                         "title: Hoja\nejercicios-capitulo:\n  - exr-a\n  - exr-c"]:
            with self.subTest(cabecera=cabecera):
                self.prepara_seleccion(cabecera)
                estado, salida, errores = self.ejecuta()
                self.assertEqual((estado, errores), (0, ""))
                self.assertIn("primeros 2 enunciados", salida)

    def test_sin_seleccion_exige_todos_los_ejercicios(self):
        self.prepara_seleccion("title: Hoja")
        estado, _, errores = self.ejecuta()
        self.assertEqual(estado, 1)
        self.assertIn("falta ejercicio 3", errores)

    def test_seleccion_valida_no_admite_otro_orden_en_la_hoja(self):
        self.prepara_seleccion("ejercicios-capitulo: [exr-a, exr-c]")
        texto = self.hoja.read_text(encoding="utf-8")
        texto = texto.replace("Enunciado con $x^2$.", "TEMPORAL")
        texto = texto.replace("Enunciado C.", "Enunciado con $x^2$.")
        self.hoja.write_text(texto.replace("TEMPORAL", "Enunciado C."), encoding="utf-8")
        self.assertEqual(self.ejecuta()[0], 1)

    def test_seleccion_con_ids_desconocidos_repetidos_o_desordenados(self):
        for seleccion, esperado in [
            ("[exr-a, exr-inexistente]", "ausentes del capítulo"),
            ("[exr-a, exr-a]", "identificadores repetidos"),
            ("[exr-c, exr-a]", "conservar el orden"),
        ]:
            with self.subTest(seleccion=seleccion):
                self.prepara_seleccion(f"ejercicios-capitulo: {seleccion}")
                estado, _, errores = self.ejecuta()
                self.assertEqual(estado, 1)
                self.assertIn(esperado, errores)

    def test_seleccion_requiere_lista_no_vacia_de_ids(self):
        for seleccion in ["[]", "null", "exr-a", "{exr-a: true}",
                          "[exr-a, 2]", "[exr-a, false]", "[no-es-un-id]"]:
            with self.subTest(seleccion=seleccion):
                self.prepara_seleccion(f"ejercicios-capitulo: {seleccion}")
                estado, _, errores = self.ejecuta()
                self.assertEqual(estado, 1)
                self.assertIn("lista no vacía de identificadores", errores)

    def test_cabecera_yaml_invalida(self):
        self.prepara_seleccion("ejercicios-capitulo: [exr-a,")
        self.assertIn("cabecera YAML inválida", self.ejecuta()[2])

    def test_cabecera_yaml_sin_cerrar(self):
        self.hoja.write_text("---\ntitle: Hoja\n" + ejercicio("exr-h-a", self.cuerpo),
                             encoding="utf-8")
        self.assertIn("cabecera YAML sin cerrar", self.ejecuta()[2])

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

    def test_identificadores_repetidos_en_capitulo(self):
        self.capitulo.write_text(ejercicio("exr-a", self.cuerpo) * 2, encoding="utf-8")
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

    def test_solucionario_no_puede_conservar_un_titulo_ausente_en_hoja(self):
        self.hoja.write_text(ejercicio("exr-h-a", "Enunciado con $x^2$."), encoding="utf-8")
        self.solucionario()
        estado, _, errores = self.ejecuta()
        self.assertEqual(estado, 1)
        self.assertIn("título o enunciado distintos", errores)

    def test_solucionario_no_puede_cambiar_solo_el_titulo(self):
        self.solucionario(self.cuerpo.replace("Título", "Otro título"))
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
