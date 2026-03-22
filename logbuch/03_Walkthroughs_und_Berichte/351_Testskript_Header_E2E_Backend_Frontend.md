# Testskript-Header: E2E Backend → Frontend

"""
KATEGORIE: E2E / Backend → Frontend (Unidirektional)
ZWECK: Testet ausschließlich die Datenfluss-Richtung Backend → Frontend (Parsing -> API -> Frontend reception).
EINGABEWERTE: src/core/main.py (_get_installed_packages, get_environment_info)
AUSGABEWERTE: Validierung Backend-Daten-Pipeline bis Frontend-Empfang
TESTDATEIEN: src/core/main.py, web/app.html
ERWEITERUNGEN (TODO): [ ] Mocking für verschiedene Python-Versionen, [ ] Backend-Timeout Tests
KOMMENTAR: Testet ausschließlich die Datenfluss-Richtung Backend → Frontend.
VERWENDUNG: python3 tests/e2e/packages/test_e2e_packages_backend_to_frontend.py
"""

---

## Hinweise
- Dieser Header dient als Vorlage für E2E-Testskripte, die den Datenfluss vom Backend zum Frontend prüfen.
- Erweiterungen/TODOs werden als Checkliste geführt.
- Die Verwendung gibt den typischen Aufruf des Skripts an.

---

**Letzte Aktualisierung:** 13. März 2026
