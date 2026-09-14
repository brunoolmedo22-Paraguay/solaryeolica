from __future__ import annotations

from pathlib import Path
import unittest

try:
    from streamlit.testing.v1 import AppTest
except ImportError:
    AppTest = None


@unittest.skipIf(AppTest is None, "Streamlit não instalado")
class AppSmokeTest(unittest.TestCase):
    def setUp(self):
        self.app_path = Path(__file__).resolve().parents[1] / "app.py"

    def test_landing_renders_and_has_five_sources(self):
        app = AppTest.from_file(str(self.app_path), default_timeout=30).run()
        self.assertEqual(len(app.exception), 0)
        labels = [b.label for b in app.button]
        self.assertIn("ANALISAR SOLAR →", labels)
        self.assertIn("ANALISAR EÓLICA →", labels)
        self.assertIn("ANALISAR TÉRMICA →", labels)
        self.assertIn("ANALISAR BATERIA →", labels)
        self.assertIn("ANALISAR H₂ →", labels)
        self.assertIsNone(app.session_state["energy_source"])

    def test_solar_module_still_opens(self):
        app = AppTest.from_file(str(self.app_path), default_timeout=30).run()
        next(b for b in app.button if b.label == "ANALISAR SOLAR →").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.session_state["energy_source"], "solar")
        self.assertEqual(app.session_state["current_page"], "Visão geral")
        self.assertIn("Entrada", [b.label for b in app.button])

    def test_wind_example_runs_end_to_end(self):
        app = AppTest.from_file(str(self.app_path), default_timeout=30).run()
        next(b for b in app.button if b.label == "ANALISAR EÓLICA →").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.session_state["energy_source"], "wind")

        next(b for b in app.button if b.label == "Simulação").click().run()
        source = next(r for r in app.radio if r.label == "Fonte")
        source.set_value("Exemplo sintético · Ceará").run()
        self.assertEqual(len(app.exception), 0)
        next(b for b in app.button if b.label == "▶ CALCULAR PERFIL EÓLICO").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertIsNotNone(app.session_state["wind_result"])
        self.assertEqual(len(app.session_state["wind_result"]), 1008)
        self.assertGreater(app.session_state["wind_kpis"]["energy_gross_kwh"], 0)

        next(b for b in app.button if b.label == "Catálogo de aerogeradores").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertGreaterEqual(len(app.get("plotly_chart")), 1)

    def test_thermal_module_opens(self):
        app = AppTest.from_file(str(self.app_path), default_timeout=30).run()
        next(b for b in app.button if b.label == "ANALISAR TÉRMICA →").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.session_state["energy_source"], "thermal")
        self.assertIn("Simulação", [b.label for b in app.button])

    def test_battery_module_opens(self):
        app = AppTest.from_file(str(self.app_path), default_timeout=30).run()
        next(b for b in app.button if b.label == "ANALISAR BATERIA →").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.session_state["energy_source"], "battery")
        self.assertIn("Simulação", [b.label for b in app.button])

    def test_h2_module_opens(self):
        app = AppTest.from_file(str(self.app_path), default_timeout=30).run()
        next(b for b in app.button if b.label == "ANALISAR H₂ →").click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.session_state["energy_source"], "h2")
        self.assertIn("Simulação", [b.label for b in app.button])


if __name__ == "__main__":
    unittest.main()
