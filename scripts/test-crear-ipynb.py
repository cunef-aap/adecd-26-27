#!/usr/bin/env python3
"""Las rutas de datos del cuaderno funcionan sin los archivos locales del curso."""
import ast
import importlib.util
from pathlib import Path
import tempfile
import unittest


spec = importlib.util.spec_from_file_location(
    "crear_ipynb", Path(__file__).with_name("crear-ipynb.py"))
cuadernos = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cuadernos)


class DatosColabTest(unittest.TestCase):
    def setUp(self):
        temporal = tempfile.TemporaryDirectory()
        self.addCleanup(temporal.cleanup)
        self.datos = Path(temporal.name)
        (self.datos / "prueba.csv").touch()

    def test_ruta_con_comillas_simples_o_dobles(self):
        for comilla in ("'", '"'):
            codigo = f"datos = pd.read_csv({comilla}../datos/prueba.csv{comilla})\n"
            nuevo, n = cuadernos.datos_para_colab(codigo, self.datos)
            self.assertEqual(n, 1)
            arbol = ast.parse(nuevo)
            self.assertEqual(arbol.body[0].value.args[0].value,
                             f"{cuadernos.DATOS_PUBLICOS}/prueba.csv")

    def test_no_toca_comentarios_ni_otros_literales(self):
        codigo = '# "../datos/prueba.csv"\nx = "otro.csv"\n'
        self.assertEqual(cuadernos.datos_para_colab(codigo, self.datos), (codigo, 0))

    def test_sin_datos_no_cambia_nada(self):
        codigo = "import torch\nX = torch.ones(3, 2)\n"
        self.assertEqual(cuadernos.datos_para_colab(codigo), (codigo, 0))

    def test_falla_si_no_existe_el_dato(self):
        with self.assertRaises(ValueError):
            cuadernos.datos_para_colab('x = "../datos/ausente.csv"', self.datos)

    def test_rechaza_salir_de_la_carpeta(self):
        with self.assertRaises(ValueError):
            cuadernos.datos_para_colab('x = "../datos/../privado.csv"', self.datos)

    def test_es_idempotente_y_conserva_el_resto_de_la_celda(self):
        codigo = 'x = pd.read_csv("../datos/prueba.csv", sep=",")  # comentario\n'
        nuevo, _ = cuadernos.datos_para_colab(codigo, self.datos)
        self.assertEqual(cuadernos.datos_para_colab(nuevo, self.datos), (nuevo, 0))
        self.assertIn('sep=","', nuevo)
        self.assertTrue(nuevo.endswith("  # comentario\n"))
        ast.parse(nuevo)


if __name__ == "__main__":
    unittest.main()
