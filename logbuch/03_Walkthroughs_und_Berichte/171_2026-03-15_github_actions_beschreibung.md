# GitHub Actions – Beschreibung & Einsatz im Projekt

## Ziel
GitHub Actions automatisiert Build-, Test- und Release-Prozesse direkt im Repository. Sie sorgt für reproduzierbare Abläufe, kontinuierliche Qualitätssicherung und eine nahtlose Integration von CI/CD.

## Funktionsweise
- **Workflows** werden als YAML-Dateien im Verzeichnis `.github/workflows/` definiert.
- Jeder Workflow besteht aus Jobs (z.B. build, test, release), die auf GitHub-Runnern (z.B. Ubuntu) ausgeführt werden.
- Workflows werden durch Events ausgelöst (z.B. push, pull_request, release).

## Typische Schritte im Media Web Viewer Projekt
1. **Checkout & Setup**
   - Quellcode wird ausgecheckt (`actions/checkout`)
   - Python-Umgebung wird eingerichtet (`actions/setup-python`)
2. **Abhängigkeiten installieren**
   - Installation der benötigten Pakete (z.B. via `pip install -r requirements-dev.txt`)
3. **Linting & Type-Check**
   - Statische Codeanalyse und Typprüfung
4. **Tests ausführen**
   - Unit-, Integrations- und UI-Tests (ggf. mit Xvfb für Headless-GUI)
5. **Build & Release**
   - Erstellen von Artefakten (Wheel, sdist, PyInstaller, Debian)
   - Optional: Upload zu GitHub Releases

## Beispiel-Workflow (Ausschnitt)
```yaml
name: Build & Test
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements-dev.txt
      - name: Lint & Type-Check
        run: python infra/build_system.py --lint --type-check
      - name: Run Tests
        run: python infra/build_system.py --test
```

## Besonderheiten im Projekt
- Test-Gate: Nur bei erfolgreichem Testlauf werden Artefakte gebaut und veröffentlicht
- Headless-Tests: Xvfb für GUI-Tests im CI
- Automatische Versionierung und Release-Pipeline
- Fehlerprotokolle und Artefakte werden als Build-Outputs gespeichert

## Vorteile
- Automatisierte, nachvollziehbare Abläufe
- Schnelle Rückmeldung bei Fehlern
- Einfache Integration in bestehende GitHub-Workflows

---

**Siehe auch:**
- Logbuch: Build-Pipeline Beschreibung
- [GitHub Actions Doku](https://docs.github.com/en/actions)
- `.github/workflows/` im Repository
