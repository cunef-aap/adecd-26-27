#!/usr/bin/env python3
"""Comprueba el filtro real con Pandoc: conserva enlaces públicos y oculta privados."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

FILTRO = Path(__file__).with_name("enlaces-publicados.lua").resolve()


class EnlacesTest(unittest.TestCase):
    def setUp(self):
        temporal = tempfile.TemporaryDirectory()
        self.addCleanup(temporal.cleanup)
        self.raiz = Path(temporal.name)
        (self.raiz / "capitulos").mkdir()
        (self.raiz / "contenido.txt").write_text(
            "capitulos/uno.qmd\ncurso/publico.qmd\n"
            "- problemas/soluciones.qmd\n- capitulos/borrador.qmd\n")
        (self.raiz / "revision.txt").write_text("problemas/soluciones.qmd\n")

    def filtra(self, texto, perfiles=("publica",)):
        adaptador = self.raiz / "adaptador.lua"
        adaptador.write_text(
            "quarto = {project = {directory = " + json.dumps(str(self.raiz))
            + ", profile = {" + ", ".join(json.dumps(p) for p in perfiles) + "}},"
            + "doc = {input_file = "
            + json.dumps(str(self.raiz / "capitulos/uno.qmd")) + "}}\n"
            + "dofile(" + json.dumps(str(FILTRO)) + ")\n")
        resultado = subprocess.run(
            ["quarto", "pandoc", "--from", "markdown", "--to", "json",
             "--lua-filter", str(adaptador)], input=texto,
            capture_output=True, text=True, check=True, cwd=self.raiz / "capitulos")
        return json.loads(resultado.stdout)["blocks"][0]["c"][0]

    def test_enlace_publico_con_subida_de_directorio(self):
        nodo = self.filtra("[repaso](../curso/publico.qmd#teorema)")
        self.assertEqual(nodo["t"], "Link")
        self.assertEqual(nodo["c"][2][0], "../curso/publico.qmd#teorema")

    def test_enlace_desde_raiz_del_proyecto(self):
        self.assertEqual(self.filtra("[repaso](/curso/publico.qmd)")["t"], "Link")

    def test_solucionario_no_se_publica(self):
        self.assertEqual(self.filtra("[sol](../problemas/soluciones.qmd)")["t"], "Span")

    def test_revision_permite_solo_el_extra_indicado(self):
        for ruta, tipo in [("../problemas/soluciones.qmd", "Link"),
                           ("borrador.qmd", "Span")]:
            self.assertEqual(self.filtra(f"[texto]({ruta})", ("revision",))["t"], tipo)

    def test_perfil_publico_prevalece(self):
        self.assertEqual(self.filtra("[sol](../problemas/soluciones.qmd)",
                                    ("revision", "publica"))["t"], "Span")

    def test_completo_permite_inactivos(self):
        self.assertEqual(self.filtra("[texto](borrador.qmd)", ("completo",))["t"], "Link")


if __name__ == "__main__":
    unittest.main()
