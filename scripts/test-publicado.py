#!/usr/bin/env python3
"""Comprueba que revisar en local no amplia la lista publica ni modifica la base."""
import importlib.util
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch


RAIZ = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("publicado", RAIZ / "scripts/publicado.py")
publicado = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publicado)

PUBLICOS = ["index.qmd", "capitulos/01.qmd", "curso/algebra.qmd"]
PRIVADOS = ["capitulos/03.qmd", "problemas/hoja-03-soluciones.qmd"]


class PerfilesTest(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)
        self.raiz = Path(self.temporal.name)
        for nombre in PUBLICOS + PRIVADOS:
            ruta = self.raiz / nombre
            ruta.parent.mkdir(parents=True, exist_ok=True)
            ruta.touch()
        (self.raiz / "contenido.txt").write_text(
            "index.qmd\n[Capitulos]\ncapitulos/01.qmd\n- capitulos/03.qmd\n"
            "[Hojas]\n- problemas/hoja-03-soluciones.qmd\n"
            "{apendices}\ncurso/algebra.qmd\n", encoding="utf-8")
        (self.raiz / "revision.txt").write_text(
            "\n".join(reversed(PRIVADOS)) + "\n", encoding="utf-8")
        (self.raiz / "_quarto.yml").write_text("base intacta\n", encoding="utf-8")
        for atributo, valor in [
            ("RAIZ", self.raiz), ("CONTENIDO", self.raiz / "contenido.txt"),
            ("REVISION", self.raiz / "revision.txt"),
        ]:
            cambio = patch.object(publicado, atributo, valor)
            cambio.start()
            self.addCleanup(cambio.stop)

    def texto(self, perfil):
        return (self.raiz / f"_quarto-{perfil}.yml").read_text(encoding="utf-8")

    def rutas(self, perfil):
        return re.findall(r"^\s+- ([\w/-]+\.qmd)$", self.texto(perfil), re.M)

    def test_publica_solo_publicos(self):
        self.assertEqual(publicado.escribe(), (3, 5))
        self.assertEqual(self.rutas("publica"), PUBLICOS)
        self.assertIn("output-dir: docs", self.texto("publica"))

    def test_revision_incluye_extras_en_orden_del_libro(self):
        self.assertEqual(publicado.escribe(revision=True), (5, 5))
        self.assertEqual(self.rutas("revision"), PUBLICOS[:2] + PRIVADOS + PUBLICOS[2:])
        self.assertIn("output-dir: _completo/local", self.texto("revision"))

    def test_generar_publicacion_no_cambia_revision(self):
        publicado.escribe(revision=True)
        anterior = self.texto("revision")
        publicado.escribe()
        self.assertEqual(self.texto("revision"), anterior)
        self.assertFalse(set(self.rutas("publica")) & set(PRIVADOS))

    def test_completo_no_cambia_la_base(self):
        publicado.escribe(todo=True)
        self.assertEqual(set(self.rutas("completo")), set(PUBLICOS + PRIVADOS))
        self.assertIn("output-dir: _completo\n", self.texto("completo"))
        self.assertEqual((self.raiz / "_quarto.yml").read_text(), "base intacta\n")

    def test_generacion_idempotente(self):
        for argumentos, perfil in [({}, "publica"), ({"revision": True}, "revision"),
                                   ({"todo": True}, "completo")]:
            publicado.escribe(**argumentos)
            anterior = self.texto(perfil)
            publicado.escribe(**argumentos)
            self.assertEqual(self.texto(perfil), anterior)

    def test_rechaza_ruta_desconocida(self):
        (self.raiz / "revision.txt").write_text("../fuera.qmd\n")
        with self.assertRaises(SystemExit):
            publicado.escribe(revision=True)

    def test_rechaza_modos_incompatibles(self):
        with self.assertRaises(ValueError):
            publicado.escribe(todo=True, revision=True)

    def test_configuracion_base_no_impone_listas(self):
        base = (RAIZ / "_quarto.yml").read_text(encoding="utf-8")
        self.assertNotRegex(base, r"(?m)^  (?:chapters|appendices):")
        self.assertIn("default: revision", base)
        self.assertIn("output-dir: _completo/local", base)


if __name__ == "__main__":
    unittest.main()
