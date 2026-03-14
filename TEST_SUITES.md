# Test-Suiten Übersicht – Media Web Viewer

**Datum:** 13.03.2026
**Autor:** Copilot

## Überblick
Das Projekt verfügt über mehrere automatisierte Test-Suiten, die verschiedene Ebenen abdecken und die Qualität, Stabilität und Integrität des Media Web Viewer sicherstellen.

---

## Unit-Tests
- **Ort:** `tests/` (z.B. test_parser_pipeline.py, test_db_logic.py)
- **Fokus:** Einzelne Funktionen, Parser, Datenbanklogik
- **Ausführung:** `pytest tests/` oder `python tests/test_*.py`

## Integrationstests
- **Ort:** `tests/integration/`
- **Fokus:** Zusammenspiel mehrerer Komponenten (Build, Session, Transcoding, Stream)
- **Ausführung:** `pytest tests/integration/`

## E2E-Tests (End-to-End)
- **Ort:** `tests/test_e2e_packages_*.py`, `tests/e2e/`
- **Fokus:** Vollständiger Datenfluss (z.B. Package-Anzeige, Backend↔Frontend)
- **Details:** Siehe [README_E2E_PACKAGES.md](tests/README_E2E_PACKAGES.md)

## GUI-Tests (Selenium)
- **Ort:** `tests/run_gui_tests.py`, `tests/pages/`, `tests/selenium/`
- **Fokus:** UI-Interaktion, Event-Handling, visuelle Regression
- **Details:** Siehe [README_GUI_TESTS.md](tests/README_GUI_TESTS.md), [GUI_TEST_SUITE.md](tests/GUI_TEST_SUITE.md)

## Test-Artefakte
- **Ort:** `tests/artifacts/`
- **Beschreibung:** Logs, Reports, Screenshots, Vergleichsdaten
- **Details:** Siehe [TEST_ARTIFACTS.md](tests/TEST_ARTIFACTS.md)

## Vollständige Testdokumentation
Eine vollständige Dokumentation und Übersicht aller Tests findet sich in [TEST_DOCUMENTATION.md](tests/TEST_DOCUMENTATION.md).

---

**Fazit:**
Die strukturierte Testlandschaft ermöglicht eine kontinuierliche Qualitätssicherung und schnelle Fehlererkennung im gesamten Entwicklungsprozess des Media Web Viewer.
