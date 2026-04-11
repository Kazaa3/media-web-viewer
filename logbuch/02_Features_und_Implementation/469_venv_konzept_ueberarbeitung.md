# Überarbeitung: venv-Konzept & Build-/Test-Umgebungen

**Datum:** 15.03.2026

## Aktuelles Problem
- Die Trennung von Build-, Test- und Laufzeit-Umgebungen ist nicht konsequent umgesetzt.
- Test- und Build-Abhängigkeiten (wie `pytest`, `pyinstaller`) werden nicht automatisch in die jeweils richtige venv installiert.
- Das führt zu Fehlern wie fehlenden Modulen beim Test- oder Buildlauf.

## Überarbeitetes venv-Konzept

### 1. Laufzeit-Umgebung (`.venv_run`)
- Enthält nur die für den Betrieb der Anwendung notwendigen Pakete.
- Wird für das Starten der App und die normale Nutzung verwendet.

### 2. Build-Umgebung (`.venv_build`)
- Enthält alle Pakete, die für das Bauen von Artefakten (z. B. PyInstaller, wheel) benötigt werden.
- Wird vom Build-System (`infra/build_system.py`) bevorzugt verwendet, falls vorhanden.
- Trennung von Build- und Laufzeit-Abhängigkeiten verhindert Konflikte und unnötige Pakete im Produktivbetrieb.

### 3. Test-Umgebung (`.venv_test` oder `.venv_run` mit Testpaketen)
- Enthält alle Pakete, die für das Ausführen von Tests benötigt werden (z. B. `pytest`, `pytest-cov` etc.).
- Tests sollten immer in einer Umgebung laufen, in der alle Test-Abhängigkeiten installiert sind.
- Empfehlung: Entweder separate `.venv_test` oder Installation der Testpakete temporär in `.venv_run`.

## Empfehlungen für die Praxis
- Dokumentation und Onboarding-Prozess anpassen:
  - Klare Schritte zur Erstellung und Pflege der verschiedenen venvs.
  - Beispiel:
    ```bash
    # Laufzeit-Umgebung
    python -m venv .venv_run
    source .venv_run/bin/activate
    pip install -r infra/requirements-run.txt
    
    # Build-Umgebung
    python -m venv .venv_build
    source .venv_build/bin/activate
    pip install -r infra/requirements-build.txt
    
    # Test-Umgebung
    python -m venv .venv_test
    source .venv_test/bin/activate
    pip install -r infra/requirements-test.txt
    ```
- Build- und Testsysteme so anpassen, dass sie die jeweils spezialisierte venv erkennen und nutzen.
- Optional: Automatische Prüfung und Hinweis, falls eine venv nicht die nötigen Pakete enthält.

## Ergebnis
- Saubere Trennung von Build-, Test- und Laufzeit-Abhängigkeiten.
- Weniger Fehler durch fehlende oder falsche Pakete.
- Bessere Wartbarkeit und Nachvollziehbarkeit der Entwicklungs- und Deployment-Prozesse.
