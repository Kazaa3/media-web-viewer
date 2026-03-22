# Fehler: pytest wird nicht installiert

**Datum:** 15.03.2026

## Problem
- Trotz Build- oder Setup-Prozess wird das Test-Framework `pytest` nicht automatisch im venv installiert.
- Beim Testlauf erscheint weiterhin:
  ```
  /home/xc/#Coding/gui_media_web_viewer/.venv_run/bin/python: No module named pytest
  [Python Tests - Exit Code: 1]
  ```

## Analyse
- Die Installation von `pytest` (und ggf. weiteren Test-Abhängigkeiten) ist nicht Teil des Standard-Builds oder wird im Setup-Skript nicht automatisch ausgeführt.
- Mögliche Ursachen:
  - `requirements-test.txt` oder `requirements-dev.txt` wird nicht automatisch installiert.
  - Die Build-Logik (z. B. `build_system.py`) installiert keine Test-Abhängigkeiten im venv.
  - Es fehlt ein expliziter Installationsschritt für Testpakete im Onboarding/CI-Prozess.

## Lösungsvorschlag
- Ergänze die Build- oder Setup-Dokumentation um einen klaren Schritt zur Installation der Test-Abhängigkeiten:
  ```bash
  pip install -r infra/requirements-test.txt
  # oder
  pip install pytest
  ```
- Optional: Passe das Build- oder Testsystem an, sodass vor jedem Testlauf automatisch die benötigten Pakete installiert werden.

## Ergebnis
- Erst nach manueller oder automatisierter Installation von `pytest` im venv können die Tests erfolgreich ausgeführt werden.
