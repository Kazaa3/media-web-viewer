#dict - Desktop Media Player and Library Manager v1.34

## Basic Tests - Übersicht & Konventionen

Dieses Dokument beschreibt die grundlegenden Tests (Basic Tests) im Media Web Viewer Projekt.

---

### Zweck der Basic Tests
- Schnelle Validierung der Kernfunktionen
- Sicherstellung der Stabilität nach jedem Build
- Abdeckung von Standardfällen und Smoke-Tests

---

### Typische Basic Testdateien
- test_dev_build.py
- test_custom_runner.py
- test_internationalization.py
- test_gui_presence_short.py
- test_options_configuration.py

---

### Header-Konvention
Jeder Basic Test muss mit folgendem Header beginnen:

```python
#dict - Desktop Media Player and Library Manager v1.34
```

---

### Ausführung
- Einzeltest: `python tests/<testfile>.py`
- Alle Basic Tests: `run_all_tests.sh` oder CI/CD Pipeline

---

### Kommentar
Basic Tests sind essenziell für schnelle Rückmeldung und Regression-Checks. Sie sollten regelmäßig ausgeführt und gepflegt werden.

*Letzte Aktualisierung: 13. März 2026*
